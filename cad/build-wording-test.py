"""Create the small two-filament WOPR lettering test for Bambu Studio."""
from pathlib import Path
import os, subprocess, zipfile, json
import xml.etree.ElementTree as ET
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/wording-test'
TMP=ROOT/'tmp/wording-test'
OUT.mkdir(parents=True,exist_ok=True); TMP.mkdir(parents=True,exist_ok=True)
OPENSCAD=Path('C:/Users/Jeremy/tools/openscad-nightly/openscad.exe')
BAMBU=Path('C:/Program Files/Bambu Studio/bambu-studio.exe')
PRESETS=Path('C:/Users/Jeremy/AppData/Roaming/BambuStudio/system/BBL')
ENV={**os.environ,'FONTCONFIG_FILE':str(ROOT/'tmp/pdfs/fonts.conf')}
HIDDEN={'creationflags':subprocess.CREATE_NO_WINDOW} if os.name=='nt' else {}

def run(args,timeout=180):
    # Files avoid waiting for EOF on pipe handles retained by GUI helper processes.
    log_path=TMP/'command.log'
    with log_path.open('w',encoding='utf-8') as log:
        r=subprocess.run([str(x) for x in args],cwd=TMP,stdout=log,stderr=subprocess.STDOUT,env=ENV,timeout=timeout,**HIDDEN)
    output=log_path.read_text(encoding='utf-8',errors='replace')
    if r.returncode:raise RuntimeError(f'Exit {r.returncode}: {output}')
    return output

meshes={}
for name in ['gray','white','solid']:
    target=(TMP if name=='solid' else OUT)/f'wording-{name}.stl'
    run([OPENSCAD,'--backend','Manifold','--hardwarnings','--export-format','binstl','-o',target,'-D',f'part="wording-{name}"',ROOT/'cad/wopr.scad'])
    m=trimesh.load(target,force='mesh')
    assert m.is_watertight and m.is_winding_consistent and m.volume>0,name
    meshes[name]=m
assert len(meshes['gray'].split())==1
assert np.allclose(meshes['gray'].extents,[90,34,3],atol=.01)
assert np.allclose(meshes['white'].bounds[:,2],[2.2,3],atol=.001)
assert np.all(meshes['white'].bounds[0,:2]>0) and np.all(meshes['white'].bounds[1,:2]<[90,34])
assert abs(meshes['gray'].volume+meshes['white'].volume-meshes['solid'].volume)<.05
print('PASS: 90 x 34 x 3 mm panel; white inlay Z=2.2..3.0; watertight materials fill the solid panel',flush=True)

ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
ET.register_namespace('',ns)
def tag(s):return '{'+ns+'}'+s
model=ET.Element(tag('model'),{'unit':'millimeter','xml:lang':'en-US'})
resources=ET.SubElement(model,tag('resources'))
materials=ET.SubElement(resources,tag('basematerials'),{'id':'1'})
for name,color in [('Gray','#686E75FF'),('White','#FFFFFFFF')]:ET.SubElement(materials,tag('base'),{'name':name,'displaycolor':color})
for number,name in [(2,'gray'),(3,'white')]:
    obj=ET.SubElement(resources,tag('object'),{'id':str(number),'type':'model','name':f'Filament {number-1} - {name}','pid':'1','pindex':str(number-2)})
    mesh=ET.SubElement(obj,tag('mesh'));vertices=ET.SubElement(mesh,tag('vertices'));faces=ET.SubElement(mesh,tag('triangles'))
    for v in meshes[name].vertices:ET.SubElement(vertices,tag('vertex'),dict(zip(['x','y','z'],[f'{x:.6f}' for x in v])))
    for f in meshes[name].faces:ET.SubElement(faces,tag('triangle'),dict(zip(['v1','v2','v3'],[str(x) for x in f])))
assembly=ET.SubElement(resources,tag('object'),{'id':'4','type':'model','name':'WOPR wording test - two filaments'})
components=ET.SubElement(assembly,tag('components'))
for n in [2,3]:ET.SubElement(components,tag('component'),{'objectid':str(n)})
ET.SubElement(ET.SubElement(model,tag('build')),tag('item'),{'objectid':'4'})
geometry=TMP/'wording-geometry.3mf'
with zipfile.ZipFile(geometry,'w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))

def factory_profile(kind,name,stack=()):
    path=PRESETS/kind/(name+'.json')
    assert path not in stack,'Cyclic factory profile'
    data=json.loads(path.read_text(encoding='utf-8'))
    result={}
    if data.get('inherits'):result.update(factory_profile(kind,data['inherits'],(*stack,path)))
    for included in data.get('include',[]):result.update(factory_profile(kind,included,(*stack,path)))
    result.update({k:v for k,v in data.items() if k not in ['inherits','include']})
    return result

resolved={}
for kind,name in [('machine','Bambu Lab H2D 0.4 nozzle'),('process','0.20mm Standard @BBL H2D'),('filament','Generic PLA @BBL H2D')]:
    resolved[kind]=factory_profile(kind,name)
    (TMP/f'{kind}.json').write_text(json.dumps(resolved[kind]),encoding='utf-8')
machine=TMP/'machine.json';process=TMP/'process.json';filament=TMP/'filament.json'
native=TMP/'wording-native.3mf'
log=run([BAMBU,'--load-settings',f'{machine};{process}','--load-filaments',f'{filament};{filament}','--arrange','1','--export-3mf',native,geometry])
(TMP/'native-export.log').write_text(log,encoding='utf-8')
print('PASS: Bambu native project exported with H2D factory presets',flush=True)

with zipfile.ZipFile(native) as z:files={n:z.read(n) for n in z.namelist()}
config=json.loads(files['Metadata/project_settings.config'])
metadata=ET.fromstring(files['Metadata/model_settings.config'])
obj=metadata.find('object');parts=obj.findall('part')
assert len(parts)==2,'Expected gray and white material parts'
def set_meta(parent,key,value):
    item=next((m for m in parent.findall('metadata') if m.get('key')==key),None)
    if item is None:item=ET.SubElement(parent,'metadata',{'key':key})
    item.set('value',str(value))
for number,(part,name) in enumerate(zip(parts,['gray','white']),1):
    assert int(part.find('mesh_stat').get('face_count'))==len(meshes[name].faces)
    set_meta(part,'extruder',number)
    set_meta(part,'name',f'Filament {number} - {name.title()} '+('panel' if number==1 else 'wording'))
set_meta(obj,'extruder',1)
for key in resolved['filament']:
    value=config.get(key)
    if isinstance(value,list) and len(value)==1:config[key]=value*2
config['filament_colour']=['#686E75','#FFFFFF']
config['filament_settings_id']=['Generic PLA @BBL H2D']*2
config['filament_type']=['PLA','PLA']
config['extruder_nozzle_stats']=['Standard#1','Standard#1']
config['filament_map_mode']='Manual'
config['filament_map']=['1','2']
config['filament_map_2']=['1','2']
config['filament_nozzle_map']=['1','2']
config['filament_volume_map']=['0','0']
config['flush_volumes_matrix']=['0','280','280','0']
config['flush_volumes_vector']=['140']*4
# Keep the prime tower in the overlap of both H2D toolheads' printable areas.
config['wipe_tower_x']=['60']
config['wipe_tower_y']=['220']
for plate in metadata.findall('plate'):
    set_meta(plate,'filament_map_mode','Manual')
    set_meta(plate,'filament_maps','1 2')
files['Metadata/project_settings.config']=json.dumps(config,indent=2).encode()
files['Metadata/model_settings.config']=ET.tostring(metadata,encoding='utf-8',xml_declaration=True)
assigned=TMP/'wording-assigned.3mf'
with zipfile.ZipFile(assigned,'w',zipfile.ZIP_DEFLATED) as z:
    for name,data in files.items():z.writestr(name,data)

final=OUT/'wopr-two-filament-test.3mf'
log=run([BAMBU,'--arrange','0','--export-3mf',final,assigned])
(TMP/'assigned-roundtrip.log').write_text(log,encoding='utf-8')
with zipfile.ZipFile(final) as z:
    assert z.testzip() is None
    loaded_config=json.loads(z.read('Metadata/project_settings.config'))
    loaded_meta=ET.fromstring(z.read('Metadata/model_settings.config'))
    loaded_parts=loaded_meta.find('object').findall('part')
    actual=[next(m.get('value') for m in p.findall('metadata') if m.get('key')=='extruder') for p in loaded_parts]
    assert actual==['1','2'],actual
    assert loaded_config['filament_colour']==['#686E75','#FFFFFF']
    assert loaded_config['filament_settings_id']==['Generic PLA @BBL H2D']*2
    assert loaded_config['printer_settings_id']=='Bambu Lab H2D 0.4 nozzle'
    assert loaded_config['extruder_nozzle_stats']==['Standard#1','Standard#1']
print('PASS: Bambu round-trip retains filament 1 gray / filament 2 white on one two-part object',flush=True)
slice_log=run([BAMBU,'--slice','1','--arrange','0','--export-3mf',TMP/'sliced-test.3mf',final])
(TMP/'slice-check.log').write_text(slice_log,encoding='utf-8')
with zipfile.ZipFile(TMP/'sliced-test.3mf') as z:
    slice_info=ET.fromstring(z.read('Metadata/slice_info.config'))
plate=slice_info.find('plate')
plate_values={m.get('key'):m.get('value') for m in plate.findall('metadata')}
used=plate.findall('filament')
assert {f.get('id') for f in used}=={'1','2'}
assert all(float(f.get('used_m'))>0 and f.get('used_for_object')=='true' for f in used)
assert plate_values['outside']=='false'
assert plate_values['filament_maps']=='1 2'
layers=plate.find('layer_filament_lists').findall('layer_filament_list')
assert any(l.get('filament_list')=='0 1' and l.get('layer_ranges')=='11 14' for l in layers)
summary={'slicer_exit':0,'outside_printable_area':False,'estimated_seconds':int(plate_values['prediction']),
         'estimated_grams':float(plate_values['weight']),
         'filaments':[{k:f.get(k) for k in ['id','color','used_m','used_g','nozzle_diameter']} for f in used]}
(OUT/'slice-summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print('PASS: Bambu slice uses both filaments, with white on layers 11..14 and no outside-area toolpaths',flush=True)
run([OPENSCAD,'--backend','Manifold','-o',OUT/'preview.png','-D','part="wording-preview"','--camera','45,-80,125,45,17,1.5','--viewall','--autocenter','--projection','o','--imgsize','1400,900','--colorscheme','Tomorrow','--render=true',ROOT/'cad/wopr.scad'])
(OUT/'verification.txt').write_text('PASS: panel 90 x 34 x 3 mm; production font/size and wording reused\nPASS: 0.8 mm flush white inlay, face up, backed by 2.2 mm gray\nPASS: both material meshes watertight; gray base one solid; volumes fill the panel\nPASS: Bambu re-export retains two filament assignments: 1 gray, 2 white\nPASS: Bambu slice succeeds with both filaments used for the object and no outside-area toolpaths\nPrinter preset: Bambu Lab H2D 0.4 nozzle; two standard nozzles; Generic PLA; 0.20 mm Standard\nNo physical print has been run. Confirm loaded filament/AMS mapping before printing.\n',encoding='utf-8')
print('READY: '+str(final),flush=True)
