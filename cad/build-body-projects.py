"""Package the verified body meshes as native single- and two-filament projects."""
from pathlib import Path
import json, os, subprocess, zipfile
import xml.etree.ElementTree as ET
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/body-projects'; TMP=ROOT/'tmp/body-projects'
OUT.mkdir(parents=True,exist_ok=True); TMP.mkdir(parents=True,exist_ok=True)
BAMBU=Path('C:/Program Files/Bambu Studio/bambu-studio.exe')
NS={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}

def run(args):
    with (TMP/'command.log').open('w',encoding='utf-8') as log:
        result=subprocess.run([str(BAMBU),*map(str,args)],cwd=TMP,stdout=log,
            stderr=subprocess.STDOUT,timeout=180,creationflags=subprocess.CREATE_NO_WINDOW)
    output=(TMP/'command.log').read_text(encoding='utf-8',errors='replace')
    assert result.returncode==0,output
    return output

def meta(parent,key,value):
    item=next((m for m in parent.findall('metadata') if m.get('key')==key),None)
    if item is None:item=ET.SubElement(parent,'metadata',{'key':key})
    item.set('value',str(value))

PRESETS=Path('C:/Users/Jeremy/AppData/Roaming/BambuStudio/system/BBL')
def factory(kind,name,stack=()):
    path=PRESETS/kind/(name+'.json');assert path not in stack
    data=json.loads(path.read_text(encoding='utf-8'));result={}
    if data.get('inherits'):result.update(factory(kind,data['inherits'],(*stack,path)))
    for included in data.get('include',[]):result.update(factory(kind,included,(*stack,path)))
    result.update({k:v for k,v in data.items() if k not in ['inherits','include']})
    return result
for kind,name in [('machine','Bambu Lab H2D 0.4 nozzle'),('process','0.20mm Standard @BBL H2D'),('filament','Generic PLA @BBL H2D')]:
    (TMP/f'{kind}.json').write_text(json.dumps(factory(kind,name)),encoding='utf-8')
meshes=[trimesh.load(ROOT/'output/model'/name,force='mesh') for name in ['gray-shell.stl','white-text.stl']]
assert all(m.is_watertight and m.is_winding_consistent and m.volume>0 for m in meshes)
assert len(meshes[0].split())==1
assert np.allclose(meshes[0].extents[:2],[279.342,155],atol=.01)
reports=[]
for label,count,source in [('single-filament',1,'gray-shell.stl'),('multi-color',2,'shell-two-color.3mf')]:
    native=TMP/f'{label}-native.3mf'
    (TMP/f'{label}-import.log').write_text(run(['--load-settings',f'{TMP / "machine.json"};{TMP / "process.json"}',
        '--load-filaments',';'.join([str(TMP/'filament.json')]*count),
        '--arrange','1','--export-3mf',native,ROOT/'output/model'/source]),encoding='utf-8')
    with zipfile.ZipFile(native) as z:files={n:z.read(n) for n in z.namelist()}
    settings=json.loads(files['Metadata/project_settings.config'])
    settings['filament_colour']=['#686E75','#FFFFFF'][:count]
    settings['filament_settings_id']=['Generic PLA @BBL H2D']*count
    settings['extruder_nozzle_stats']=['Standard#1','Standard#1']
    settings['filament_map_mode']='Manual'
    for key in ['filament_map','filament_map_2','filament_nozzle_map']:
        settings[key]=['1','2'][:count]
    settings['filament_volume_map']=['0']*count
    settings['flush_volumes_matrix']=['0'] if count==1 else ['0','280','280','0']
    settings['flush_volumes_vector']=['140']*(count*2)
    settings['enable_support']='1'
    settings['support_type']='normal(auto)'
    settings['wall_loops']='3'
    settings['wipe_tower_x']=['80'];settings['wipe_tower_y']=['270']
    settings['enable_prime_tower']='1' if count==2 else '0'
    metadata=ET.fromstring(files['Metadata/model_settings.config'])
    objects=metadata.findall('object');assert len(objects)==1
    obj=objects[0];parts=obj.findall('part');assert len(parts)==count
    meta(obj,'name','WOPR body - '+label);meta(obj,'extruder',1)
    for index,part in enumerate(parts):
        assert int(part.find('mesh_stat').get('face_count'))==len(meshes[index].faces)
        meta(part,'extruder',index+1)
        meta(part,'name','Gray body - recessed lettering' if count==1 else ['Gray body','White flush lettering'][index])
    for plate in metadata.findall('plate'):
        meta(plate,'filament_map_mode','Manual');meta(plate,'filament_maps','1' if count==1 else '1 2')
    files['Metadata/model_settings.config']=ET.tostring(metadata,encoding='utf-8',xml_declaration=True)
    files['Metadata/project_settings.config']=json.dumps(settings,indent=2).encode()
    assigned=TMP/f'{label}-assigned.3mf'
    with zipfile.ZipFile(assigned,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in files.items():z.writestr(name,data)
    final=OUT/f'wopr-body-{label}.3mf'
    (TMP/f'{label}-roundtrip.log').write_text(run(['--arrange','0','--export-3mf',final,assigned]),encoding='utf-8')
    with zipfile.ZipFile(final) as z:
        assert z.testzip() is None
        config=json.loads(z.read('Metadata/project_settings.config'))
        model=ET.fromstring(z.read('Metadata/model_settings.config'))
        assert len(model.findall('object'))==1
        actual=model.find('object').findall('part');assert len(actual)==count
        for index,part in enumerate(actual):
            object_filament=next((m.get('value') for m in model.find('object').findall('metadata') if m.get('key')=='extruder'),'1')
            assert next((m.get('value') for m in part.findall('metadata') if m.get('key')=='extruder'),object_filament)==str(index+1)
            assert int(part.find('mesh_stat').get('face_count'))==len(meshes[index].faces)
        assert config['filament_colour']==['#686E75','#FFFFFF'][:count]
        assert config['printer_settings_id']=='Bambu Lab H2D 0.4 nozzle'
        assert config['enable_support']=='1'
        assert not any(n.endswith('.gcode') for n in z.namelist())
        # Check the actual packaged triangle coordinates against the source meshes.
        packaged=[]
        for name in z.namelist():
            if not name.endswith('.model'):continue
            xml=ET.fromstring(z.read(name))
            for mesh in xml.findall('.//m:mesh',NS):
                vertices=np.array([[float(v.get(k)) for k in ['x','y','z']] for v in mesh.find('m:vertices',NS)])
                faces=np.array([[int(f.get(k)) for k in ['v1','v2','v3']] for f in mesh.find('m:triangles',NS)])
                packaged.append(trimesh.Trimesh(vertices=vertices,faces=faces))
        assert len(packaged)==count
        for index,mesh in enumerate(packaged):
            assert mesh.is_watertight and mesh.is_winding_consistent
            assert np.allclose(mesh.extents,meshes[index].extents,atol=.001)
            # Bambu recenters vertices and writes decimal coordinates; allow one ppm.
            assert np.isclose(mesh.volume,meshes[index].volume,rtol=1e-6,atol=.1)
    reports.append(f'PASS: {final.name}: one body, {count} material part(s), native Bambu round-trip exit 0, mesh extents/volume preserved within decimal precision, watertight')
    print(reports[-1],flush=True)
reports.append('H2D 0.4 mm, Generic PLA, 0.20 mm layers, three walls, automatic supports enabled. Single filament has recessed lettering; multi-color has flush white lettering. Editable projects are unsliced; verify supports, plate placement and actual spool mapping before printing.')
(OUT/'verification.txt').write_text('\n'.join(reports)+'\n',encoding='utf-8')
