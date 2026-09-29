"""Prepare complete, unsliced native Bambu projects for the two eight-wheel robots."""
from pathlib import Path
import json,subprocess,zipfile,xml.etree.ElementTree as ET
import trimesh,numpy as np
ROOT=Path(__file__).resolve().parents[1];TMP=ROOT/'tmp/unified-bambu';OUT=ROOT/'output/reinforced/bambu-projects'
TMP.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
EXE='C:/Program Files/Bambu Studio/bambu-studio.exe';PRESETS=Path('C:/Users/Jeremy/AppData/Roaming/BambuStudio/system/BBL')
def factory(kind,name):
    data=json.loads((PRESETS/kind/(name+'.json')).read_text());result={}
    if data.get('inherits'):result.update(factory(kind,data['inherits']))
    for included in data.get('include',[]):result.update(factory(kind,included))
    result.update({k:v for k,v in data.items() if k not in ['inherits','include']});return result
settings={'wall_loops':'5','top_shell_layers':'6','bottom_shell_layers':'6','sparse_infill_density':'35%','sparse_infill_pattern':'gyroid','enable_support':'1','support_type':'normal(auto)'}
for kind,name in [('machine','Bambu Lab H2D 0.4 nozzle'),('process','0.20mm Standard @BBL H2D'),('filament','Generic PETG @BBL H2D')]:
    data=factory(kind,name)
    if kind=='process':data.update(settings)
    (TMP/(kind+'.json')).write_text(json.dumps(data))
NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',NS)
def tag(s):return '{'+NS+'}'+s
def meta(node,key,value):
    m=next((m for m in node.findall('metadata') if m.get('key')==key),None)
    if m is None:m=ET.SubElement(node,'metadata',{'key':key})
    m.set('value',str(value))
def add_mesh(res,object_id,name,m):
    obj=ET.SubElement(res,tag('object'),{'id':str(object_id),'type':'model','name':name,'pid':'1','pindex':'0'});mesh=ET.SubElement(obj,tag('mesh'));vs=ET.SubElement(mesh,tag('vertices'));ts=ET.SubElement(mesh,tag('triangles'))
    for v in m.vertices:ET.SubElement(vs,tag('vertex'),dict(zip(['x','y','z'],[f'{a:.6f}' for a in v])))
    for f in m.faces:ET.SubElement(ts,tag('triangle'),dict(zip(['v1','v2','v3'],map(str,f))))
    return obj
evidence=[]
for edition in ['exposed','wide']:
    # CAD-defined regions are converted using the same raw-frame origin as the STL export.
    region_source=TMP/(edition+'-battery-regions.scad')
    region_source.write_text('include <'+str(ROOT/'cad/wopr-reinforced.scad').replace('\\','/')+'>\nr_shelves();')
    region_stl=TMP/(edition+'-battery-regions.stl')
    cmd=['C:/Users/Jeremy/tools/openscad-nightly/openscad.exe','--backend','Manifold','--hardwarnings','--export-format','binstl','-o',str(region_stl),'-D','part="infill-regions"','-D',f'edition="{edition}"','-D','W=220',str(region_source)]
    r=subprocess.run(cmd,cwd=TMP,capture_output=True,text=True,timeout=180,creationflags=subprocess.CREATE_NO_WINDOW)
    assert r.returncode==0 and 'WARNING:' not in r.stderr and 'ERROR:' not in r.stderr,r.stderr
    regions=trimesh.load(region_stl,force='mesh').split();assert len(regions)==2
    for retention in ['cap','zip']:
        label=edition+'-one-piece-'+retention;modifier_centers={}
        with zipfile.ZipFile(ROOT/'output/reinforced'/edition/'shell-two-color.3mf') as z:files={n:z.read(n) for n in z.namelist()}
        model=ET.fromstring(files['3D/3dmodel.model']);res=model.find(tag('resources'));build=model.find(tag('build'))
        build[0].set('transform','1 0 0 0 1 0 0 0 1 0 0 0')
        quantity={'r-frame-zip' if retention=='zip' else 'r-frame':1,'r-lid':1,'r-tray':1,'r-retainer':2}
        if retention=='cap':quantity['r-cap']=4
        expected=1;object_id=5
        for name,copies in quantity.items():
            m=trimesh.load(ROOT/'output/reinforced'/edition/(name+'.stl'),force='mesh')
            assert m.is_watertight and len(m.split())==1,(label,name)
            if name=='r-cap':m.apply_transform(trimesh.transformations.rotation_matrix(np.pi,[1,0,0]));m.apply_translation(-m.bounds[0])
            if name in ['r-frame','r-frame-zip']:
                raw=trimesh.load(ROOT/'tmp/reinforced'/(edition+'-'+name+'.stl'),force='mesh')
                assert np.allclose(raw.extents,m.extents,atol=.001),'Run build-reinforced.py first'
                parent=ET.SubElement(res,tag('object'),{'id':str(object_id),'type':'model','name':name});components=ET.SubElement(parent,tag('components'))
                add_mesh(res,1000,name,m);ET.SubElement(components,tag('component'),{'objectid':'1000'})
                for i,region in enumerate(regions):
                    modifier=region.copy();modifier.apply_translation(-raw.bounds[0]);assert modifier.is_watertight
                    modifier_centers[i+1]=modifier.bounds.mean(axis=0)
                    add_mesh(res,1001+i,'battery-block-solid-'+str(i+1),modifier);ET.SubElement(components,tag('component'),{'objectid':str(1001+i)})
            else:add_mesh(res,object_id,name,m)
            for i in range(copies):ET.SubElement(build,tag('item'),{'objectid':str(object_id),'transform':f'1 0 0 0 1 0 0 0 1 {expected*320} 0 0'});expected+=1
            object_id+=1
        files['3D/3dmodel.model']=ET.tostring(model,encoding='utf-8',xml_declaration=True)
        source=TMP/(label+'-parts.3mf')
        with zipfile.ZipFile(source,'w',zipfile.ZIP_DEFLATED) as z:
            for n,data in files.items():z.writestr(n,data)
        native=TMP/(label+'-native.3mf')
        command=[EXE,'--load-settings',str(TMP/'machine.json')+';'+str(TMP/'process.json'),'--load-filaments',str(TMP/'filament.json')+';'+str(TMP/'filament.json'),'--arrange','1','--orient','0','--export-3mf',str(native),str(source)]
        with (TMP/(label+'-import.log')).open('w') as log:r=subprocess.run(command,cwd=TMP,stdout=log,stderr=log,timeout=180,creationflags=subprocess.CREATE_NO_WINDOW)
        assert r.returncode==0,(label,r.returncode)
        with zipfile.ZipFile(native) as z:files={n:z.read(n) for n in z.namelist()}
        cfg=json.loads(files['Metadata/project_settings.config']);cfg.update(settings);cfg['filament_colour']=['#686E75','#FFFFFF'];cfg['filament_settings_id']=['Generic PETG @BBL H2D']*2;cfg['filament_map_mode']='Manual'
        for key in ['filament_map','filament_map_2','filament_nozzle_map']:cfg[key]=['1','2']
        cfg['filament_volume_map']=['0','0'];cfg['flush_volumes_matrix']=['0','280','280','0'];cfg['flush_volumes_vector']=['140']*4
        metadata=ET.fromstring(files['Metadata/model_settings.config']);shells=0;modifiers=0
        for obj in metadata.findall('object'):
            meta(obj,'extruder',1);material_parts=obj.findall('part')
            if len(material_parts)==2:
                shells+=1;meta(obj,'name','WOPR '+label+' body')
                for i,p in enumerate(material_parts):meta(p,'extruder',i+1);meta(p,'name',['Gray shell','White lettering'][i])
            else:
                for p in material_parts:
                    meta(p,'extruder',1)
                    oname=obj.find("metadata[@key='name']")
                    if len(material_parts)==3 and oname is not None and oname.get('value') in ['r-frame','r-frame-zip']:
                        index=int(p.find("metadata[@key='source_volume_id']").get('value'))
                        if index in [1,2]:
                            assert int(p.find('mesh_stat').get('face_count'))==12
                            center=[float(p.find("metadata[@key='source_offset_"+a+"']").get('value')) for a in ['x','y','z']]
                            assert np.allclose(center,modifier_centers[index],atol=.001),(label,'modifier alignment',center,modifier_centers[index])
                            p.set('subtype','modifier_part');meta(p,'name','Battery block '+str(index)+' - solid infill');meta(p,'sparse_infill_density','100%');meta(p,'sparse_infill_pattern','zig-zag');modifiers+=1
        assert shells==1 and modifiers==2,(label,shells,modifiers)
        for plate in metadata.findall('plate'):meta(plate,'filament_map_mode','Manual');meta(plate,'filament_maps','1 2')
        files['Metadata/project_settings.config']=json.dumps(cfg,indent=2).encode();files['Metadata/model_settings.config']=ET.tostring(metadata,encoding='utf-8',xml_declaration=True)
        final=OUT/('wopr-'+label+'.3mf')
        with zipfile.ZipFile(final,'w',zipfile.ZIP_DEFLATED) as z:
            for n,data in files.items():z.writestr(n,data)
        with zipfile.ZipFile(final) as z:
            assert z.testzip() is None and not any(n.endswith('.gcode') for n in z.namelist())
            actual=ET.fromstring(z.read('3D/3dmodel.model'));assert len(actual.findall('./'+tag('build')+'/'+tag('item')))==expected
            assert expected==(6 if retention=='zip' else 10)
        roundtrip=TMP/(label+'-roundtrip.3mf')
        with (TMP/(label+'-roundtrip.log')).open('w') as log:r=subprocess.run([EXE,'--arrange','0','--export-3mf',str(roundtrip),str(final)],cwd=TMP,stdout=log,stderr=log,timeout=180,creationflags=subprocess.CREATE_NO_WINDOW)
        assert r.returncode==0,label
        with zipfile.ZipFile(roundtrip) as z:
            assert z.testzip() is None
            check=ET.fromstring(z.read('3D/3dmodel.model'))
            assert len(check.findall('./'+tag('build')+'/'+tag('item')))==expected
            saved=ET.fromstring(z.read('Metadata/model_settings.config'))
            dense=[p for p in saved.findall('./object/part') if p.get('subtype')=='modifier_part']
            assert len(dense)==2
            for p in dense:
                assert p.find("metadata[@key='sparse_infill_density']").get('value')=='100%'
                assert p.find("metadata[@key='sparse_infill_pattern']").get('value')=='zig-zag'
        line=f'PASS {final.name}: {expected} print objects, one connected chassis, native Bambu import/export roundtrip, two100% battery-block modifiers, unsliced';print(line,flush=True);evidence.append(line)
(OUT/'one-piece-verification.txt').write_text('\n'.join(evidence)+'\n')
