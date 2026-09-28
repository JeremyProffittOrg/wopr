"""Build the two WOPR variants; invoke on the verified private desktop."""
from pathlib import Path
import os, subprocess, json, zipfile
import numpy as np
import trimesh
from PIL import Image, ImageChops
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/variants'; TMP=ROOT/'tmp/variants'
for p in [OUT,TMP,OUT/'replica',OUT/'robot',OUT/'views']: p.mkdir(parents=True,exist_ok=True)
EXE='C:/Users/Jeremy/tools/openscad-nightly/openscad.exe'
ENV=dict(os.environ,FONTCONFIG_FILE=str(ROOT/'tmp/pdfs/fonts.conf'))
evidence=[]
def scad(path,part,extra=()):
    r=subprocess.run([EXE,'--backend','Manifold','--hardwarnings','-o',str(path),'-D',f'part="{part}"','-D','panels_per_side=6',*extra,str(ROOT/'cad/wopr-variants.scad')],capture_output=True,text=True,env=ENV,timeout=180,creationflags=subprocess.CREATE_NO_WINDOW)
    if r.returncode or 'WARNING:' in r.stderr or 'ERROR:' in r.stderr: raise RuntimeError(part+': '+r.stderr)
    assert path.exists() and path.stat().st_size,path
parts={'replica':['gray-shell','white-text','base','cup-main-shallow-left','cup-main-shallow-right','cup-tower','led-retainer','fit-coupon'], 'robot':['robot-shell','white-text','robot-floor','robot-lid','robot-tray','robot-cap','robot-pod-test','led-retainer','fit-coupon']}
meshes={}
for variant,names in parts.items():
    for name in names:
        raw=TMP/(variant+'-'+name+'.stl')
        scad(raw,name,['--export-format','binstl'])
        m=trimesh.load(raw,force='mesh'); assert m.is_watertight and m.is_winding_consistent and m.volume>0,name
        if name!='white-text': assert len(m.split())==1,(name,'disconnected',len(m.split()))
        meshes[(variant,name)]=m
        printable=m.copy();printable.apply_translation(-m.bounds[0] if name not in ['gray-shell','robot-shell','white-text'] else [0,0,0]);printable.export(OUT/variant/(name+'.stl'))
        line=f'{variant}/{name}: watertight; components={len(m.split())}; dimensions='+str(np.round(m.extents,3).tolist());evidence.append(line);print(line,flush=True)
scad(TMP/'robot-check.stl','robot-check',['--export-format','binstl'])
probe=trimesh.load(TMP/'robot-check.stl',force='mesh')
assert np.allclose(probe.bounds,[[-100,-100,-100],[-99,-99,-99]],atol=.001) and abs(probe.volume-1)<.001,('robot interference',probe.bounds,probe.volume)
evidence.append('PASS: wheel, shell/floor/lid/tray and battery interference checks')
assert np.allclose(meshes[('replica','led-retainer')].extents,[139.23,23.78,2.4],atol=.01)
evidence.append('PASS: six panels each side, twelve boards; 127.23 mm bank')
(OUT/'verification.txt').write_text('\n'.join(evidence)+'\n')
print('PASS: variant mesh and clearance checks',flush=True)

# Standalone source exports open with the correct variant and panel count.
base_source=(ROOT/'cad/wopr.scad').read_text().replace('panels_per_side=7;','panels_per_side=6;')
(OUT/'replica/wopr-six-per-side.scad').write_text(base_source)
robot_source=(ROOT/'cad/wopr-variants.scad').read_text().replace('include <wopr.scad>',base_source.replace('part = "assembly";','part = "robot";'))
(OUT/'robot/wopr-robot.scad').write_text(robot_source)
# Preserve shell/letter alignment in standard two-material 3MF containers.
import xml.etree.ElementTree as ET
NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'; ET.register_namespace('',NS)
def tag(n):return '{'+NS+'}'+n
for variant in parts:
    model=ET.Element(tag('model'),{'unit':'millimeter'});res=ET.SubElement(model,tag('resources'))
    mats=ET.SubElement(res,tag('basematerials'),{'id':'1'})
    for n,col in [('Gray','#686E75FF'),('White','#FAFAF5FF')]:ET.SubElement(mats,tag('base'),{'name':n,'displaycolor':col})
    for i,name in enumerate([parts[variant][0],'white-text']):
        m=meshes[(variant,name)];obj=ET.SubElement(res,tag('object'),{'id':str(i+2),'type':'model','pid':'1','pindex':str(i)})
        mesh=ET.SubElement(obj,tag('mesh'));vs=ET.SubElement(mesh,tag('vertices'));ts=ET.SubElement(mesh,tag('triangles'))
        for v in m.vertices:ET.SubElement(vs,tag('vertex'),dict(zip(['x','y','z'],map(str,v))))
        for v in m.faces:ET.SubElement(ts,tag('triangle'),dict(zip(['v1','v2','v3'],map(str,v))))
    obj=ET.SubElement(res,tag('object'),{'id':'4','type':'model'});comps=ET.SubElement(obj,tag('components'))
    for i in [2,3]:ET.SubElement(comps,tag('component'),{'objectid':str(i)})
    ET.SubElement(ET.SubElement(model,tag('build')),tag('item'),{'objectid':'4'})
    with zipfile.ZipFile(OUT/variant/'shell-two-color.3mf','w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr('_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        z.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))

# Render actual exported geometry, not concept art. Importing checked meshes avoids
# recomputing booleans for every camera and retains original assembly coordinates.
from concurrent.futures import ThreadPoolExecutor
angles=[('Front',(0,-1,0)),('Rear',(0,1,0)),('Low end',(-1,0,0)),('Tower end',(1,0,0)),('Top oblique',(.22,-.28,1)),('Bottom oblique',(.22,-.28,-1)),('Front oblique',(1,-1,.8)),('Rear oblique',(-1,1,.8))]
scenes={}
header='include <'+str(ROOT/'cad/wopr-variants.scad').replace('\\','/')+'>\n'
def imp(variant,name,color='[.40,.43,.46]',move=''):
    return move+'color('+color+') import("'+str(TMP/(variant+'-'+name+'.stl')).replace('\\','/')+'");\n'
rep=imp('replica','gray-shell')+imp('replica','white-text','[.98,.98,.96]')+''.join(imp('replica',n) for n in ['base','cup-main-shallow-left','cup-tower'])+'reference_parts();'
rob=imp('robot','robot-shell')+imp('robot','white-text','[.98,.98,.96]')+''.join(imp('robot',n) for n in ['robot-floor','robot-lid','robot-tray'])+'color([.55,.57,.6]) pods() motor_cap();drive_reference();onboard_reference();reference_parts();'
scenes['replica-assembly']=(header+rep,np.array([139.7,77.5,82.5]))
scenes['robot-assembly']=(header+rob,np.array([139.7,77.5,55]))
expl=imp('robot','robot-shell',move='translate([0,0,100]) ')+imp('robot','white-text','[.98,.98,.96]','translate([0,0,100]) ')+imp('robot','robot-floor')+imp('robot','robot-lid',move='translate([0,0,170]) ')+imp('robot','robot-tray',move='translate([0,0,55]) ')+'drive_reference();onboard_reference();color([.55,.57,.6]) pods() motor_cap();'
scenes['exploded']=(header+expl,np.array([139.7,77.5,125]))
scenes['interior']=(header+imp('robot','robot-floor')+imp('robot','robot-tray',move='translate([0,0,60]) ')+'drive_reference();onboard_reference();color([.55,.57,.6]) pods() motor_cap();',np.array([139.7,77.5,45]))
catalog=[]
for variant,names in parts.items():
    for name in names:
        if variant=='robot' and name in ['white-text','led-retainer','fit-coupon']:continue
        key=variant+'-'+name;scenes[key]=(header+imp(variant,name),meshes[(variant,name)].bounds.mean(axis=0));catalog.append((variant,name,key))
for key,(scene,center) in scenes.items():(TMP/(key+'.scad')).write_text(scene)
tasks=[]
for key,(scene,center) in scenes.items():
    for i,(label,direction) in enumerate(angles):
        if key in ['exploded','interior'] and i!=6:continue
        tasks.append((key,i,center,direction))
def render(task):
    key,i,center,direction=task;path=OUT/'views'/f'{key}-{i}.png';eye=center+np.array(direction)*650
    camera=','.join(map(str,[*eye,*center]));
    scene_path=TMP/(key+'.scad')
    if key=='replica-white-text' and i in [0,1]:
        clip='translate([-100,-1,-100]) cube([500,78.5,400]);' if i==0 else 'translate([-100,77.5,-100]) cube([500,200,400]);'
        scene_path=TMP/(key+f'-face-{i}.scad');scene_path.write_text(header+'intersection(){'+imp('replica','white-text')+clip+'}')
    r=subprocess.run([EXE,'--backend','Manifold','--hardwarnings','-o',str(path),'-D','part="scene"','-D','panels_per_side=6','--imgsize','1000,750','--camera',camera,'--viewall','--autocenter','--projection','o','--colorscheme','Tomorrow','--render=true',str(scene_path)],capture_output=True,text=True,env=ENV,timeout=180,creationflags=subprocess.CREATE_NO_WINDOW)
    if r.returncode or 'ERROR:' in r.stderr or 'WARNING:' in r.stderr:raise RuntimeError(key+': '+r.stderr)
    im=Image.open(path).convert('RGB');box=ImageChops.difference(im,Image.new('RGB',im.size,im.getpixel((0,0)))).getbbox();assert box,key
    im.crop(box).save(path);print('VIEW',key,i,flush=True)
with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(render,tasks))

# Mark artifact authoring exactly once, then create and render the full PDF.
subprocess.run(['node','C:/Users/Jeremy/.codex/plugins/cache/openai-primary-runtime/pdf/26.909.12148/skills/pdf/container_tools/mark_artifact_operation_started.mjs','--operation-kind','create','--expected-output-count','1','--output-format','pdf'],check=True,capture_output=True,text=True,timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,white
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from xml.sax.saxutils import escape
import fitz
C=canvas.Canvas(str(TMP/'drawings.pdf'),pagesize=(792,612));page=0
def title(kicker,name,sub):
    global page
    page+=1;C.setFillColor(HexColor('#172535'));C.rect(0,0,792,612,fill=1,stroke=0)
    C.setFillColor(white);C.rect(22,43,748,493,fill=1,stroke=0)
    C.setFont('Helvetica',9);C.drawString(32,587,kicker.upper());C.setFont('Helvetica-Bold',23);C.drawString(32,557,name)
    C.setFillColor(HexColor('#334155'));C.setFont('Helvetica',10);C.drawString(34,517,sub)
    C.setFillColor(white);C.setFont('Helvetica',8);C.drawString(32,22,'WOPR VARIANTS / 2026-09-28 / mm / prototype - physical fit and durability untested')
def pic(key,i,x,y,w,h):
    p=OUT/'views'/f'{key}-{i}.png';im=Image.open(p);a=min(w/im.width,h/im.height);rw=im.width*a;rh=im.height*a
    C.drawImage(str(p),x+(w-rw)/2,y+(h-rh)/2,rw,rh)
def grid(key):
    for i,(label,_) in enumerate(angles):
        x=37+(i%4)*181;y=285 if i<4 else 66
        pic(key,i,x,y,170,174);C.setFillColor(HexColor('#334155'));C.setFont('Helvetica-Bold',9);C.drawString(x,y+181,label)
    C.showPage()
title('Design and assembly','Two WOPR variants','Six RGB modules per side. Four upright motors and eight wheels in the robot.')
pic('robot-assembly',6,40,115,455,365);pic('replica-assembly',6,510,255,225,195)
C.setFillColor(HexColor('#334155'));C.setFont('Helvetica',10)
for j,line in enumerate(['ROBOT: bolted main lid; closed LCD tower; guarded wheels; retained battery.', 'REPLICA: original storage cups and LCD mount, with shorter six-module banks.', 'CAD checked. Print the motor coupon before committing to the full chassis.']):C.drawString(40,97-j*17,line)
C.showPage()
for key,name,sub in [('replica-assembly','Six-per-side replica','Same 279.4 x 155 x 165 body; twelve boards; original cups and LCD fit.'),('robot-assembly','Robot: eight assembly angles','Body 279.4 x 155 x 165; guard width 190; total height 218.5; ground clearance 14.5.')]:title('Eight-angle drawing',name,sub);grid(key)
title('Assembly breakdown','Main lid, fixed tower and drive floor','Exploded model: remove main lid for service; tower roof stays closed.')
pic('exploded',6,40,73,470,420);pic('interior',6,510,155,235,320)
C.setFillColor(HexColor('#334155'));C.setFont('Helvetica',9)
for j,line in enumerate(['Top: removable main lid','Middle: body and white text','Tray: ESP32 and two drivers','Center: strapped USB battery','Bottom: four motor cradles','Eight wheels, two per motor','Four caps retain motors']):C.drawString(520,147-j*12,line)
C.showPage()
for variant,name,key in catalog:
    m=meshes[(variant,name)];dims=' x '.join(f'{x:.2f}' for x in m.extents)
    title('Printed part / '+variant,name,'Bounds: '+dims+' mm. '+('Front/rear show nearest lettering face; obliques show both.' if name=='white-text' else 'Actual checked mesh; top/bottom tilted to show pocket depth.'));grid(key)
C.save()
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='BodyW',fontName='Helvetica',fontSize=10,leading=14,spaceAfter=7,textColor=HexColor('#172535')))
styles['Heading1'].textColor=HexColor('#172535');styles['Heading2'].textColor=HexColor('#9A431C')
flow=[]
for block in (ROOT/'cad/VARIANTS.md').read_text().split('\n\n'):
    block=block.strip()
    if not block:continue
    if block.startswith('# '):flow.append(Paragraph(escape(block[2:]),styles['Heading1']))
    elif block.startswith('## '):flow.append(Paragraph(escape(block[3:]),styles['Heading2']))
    else:
        for row in block.split('\n'):
            if row.startswith('http'):flow.append(Paragraph('<link href="'+escape(row)+'">'+escape(row)+'</link>',styles['BodyW']))
            else:flow.append(Paragraph(escape(row),styles['BodyW']))
def footer(c,doc):
    c.setFont('Helvetica',8);c.setFillColor(HexColor('#475569'));c.drawString(36,24,'WOPR / parts, assembly and commissioning / 2026-09-28')
SimpleDocTemplate(str(TMP/'instructions.pdf'),pagesize=(792,612),rightMargin=42,leftMargin=42,topMargin=38,bottomMargin=43).build(flow,onFirstPage=footer,onLaterPages=footer)
final=fitz.open()
for p in ['drawings.pdf','instructions.pdf']:
    with fitz.open(TMP/p) as d:final.insert_pdf(d)
PDF=ROOT/'output/pdf/wopr-variants.pdf'
for i,p in enumerate(final):p.insert_text((722,590),f'{i+1}/{len(final)}',fontsize=8,color=(.5,.5,.5))
final.set_metadata({'title':'WOPR - six-per-side replica and eight-wheel robot','author':'Jeremy Proffitt / WOPR'})
final.save(PDF);final.close()
with fitz.open(PDF) as d:
    for i,p in enumerate(d):
        assert len(p.get_text())>80
        p.get_pixmap(matrix=fitz.Matrix(1.2,1.2),alpha=False).save(TMP/f'page-{i+1:02}.png')
    evidence.append(f'PDF: {len(d)} pages; eight views per unique printed part and both assembled variants; text and page rendering passed')
(OUT/'verification.txt').write_text('\n'.join(evidence)+'\n')
with zipfile.ZipFile(OUT/'wopr-variants-kit.zip','w',zipfile.ZIP_DEFLATED) as z:
    for folder in ['replica','robot']:
        for p in (OUT/folder).iterdir():z.write(p,p.relative_to(ROOT))
    for p in [ROOT/'cad/wopr.scad',ROOT/'cad/wopr-variants.scad',ROOT/'cad/build-variants.py',ROOT/'cad/VARIANTS.md',ROOT/'firmware/wopr-robot/wopr-robot.ino',OUT/'verification.txt']:z.write(p,p.relative_to(ROOT))
print('PASS: variants, drawings, instructions and kit',flush=True)
