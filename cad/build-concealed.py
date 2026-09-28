"""Build only the two concealed-drive variants; retain earlier deliverables."""
from pathlib import Path
import os,subprocess,json,zipfile,hashlib
import numpy as np
import trimesh
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/concealed';TMP=ROOT/'tmp/concealed'
for p in [OUT,TMP,OUT/'four-wheel',OUT/'wide-eight-wheel',OUT/'views']:p.mkdir(parents=True,exist_ok=True)
EXE='C:/Users/Jeremy/tools/openscad-nightly/openscad.exe'
ENV=dict(os.environ,FONTCONFIG_FILE=str(ROOT/'tmp/pdfs/fonts.conf'))
SCAD=ROOT/'cad/wopr-concealed.scad'
variants={'four-wheel':(False,155),'wide-eight-wheel':(True,210)}
parts=['concealed-shell','white-text','concealed-floor','robot-lid','concealed-tray','robot-cap','wheel-hood-front','wheel-hood-rear','concealed-pod-test','led-retainer','fit-coupon']
meshes={};evidence=[]
preserved={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'output/variants').rglob('*') if p.is_file()}
preserved['firmware/wopr-robot/wopr-robot.ino']=hashlib.sha256((ROOT/'firmware/wopr-robot/wopr-robot.ino').read_bytes()).hexdigest()
preserved['output/pdf/wopr-variants.pdf']=hashlib.sha256((ROOT/'output/pdf/wopr-variants.pdf').read_bytes()).hexdigest()
def scad(path,part,wide=False,width=155,extra=(),source=SCAD):
    args=[EXE,'--backend','Manifold','--hardwarnings','-o',str(path),'-D',f'part="{part}"','-D','panels_per_side=6','-D',f'hidden_wide={str(wide).lower()}','-D',f'W={width}',*extra,str(source)]
    r=subprocess.run(args,capture_output=True,text=True,env=ENV,timeout=180,creationflags=subprocess.CREATE_NO_WINDOW)
    if r.returncode or 'WARNING:' in r.stderr or 'ERROR:' in r.stderr:raise RuntimeError(part+': '+r.stderr)
    assert path.exists() and path.stat().st_size,path
for variant,(wide,width) in variants.items():
    for name in parts:
        raw=TMP/(variant+'-'+name+'.stl');scad(raw,name,wide,width,['--export-format','binstl'])
        m=trimesh.load(raw,force='mesh');assert m.is_watertight and m.is_winding_consistent and m.volume>0,name
        if name!='white-text':assert len(m.split())==1,(variant,name,'disconnected',len(m.split()))
        meshes[(variant,name)]=m
        printable=m.copy();printable.apply_translation([0,0,0] if name in ['concealed-shell','white-text'] else -m.bounds[0]);printable.export(OUT/variant/(name+'.stl'))
        line=f'{variant}/{name}: watertight; components={len(m.split())}; dimensions_mm='+str(np.round(m.extents,3).tolist());print(line,flush=True);evidence.append(line)
    probe_path=TMP/(variant+'-check.stl');scad(probe_path,'concealed-check',wide,width,['--export-format','binstl'])
    probe=trimesh.load(probe_path,force='mesh')
    assert np.allclose(probe.bounds,[[-100,-100,-100],[-99,-99,-99]],atol=.001) and abs(probe.volume-1)<.001,(variant,'interference',probe.bounds,probe.volume)
    assert np.allclose(meshes[(variant,'concealed-shell')].extents,[279.4,width,164.952],atol=.02)
    assert meshes[(variant,'concealed-floor')].bounds[0,1]>=3.3-.001 and meshes[(variant,'concealed-floor')].bounds[1,1]<=width-3.3+.001
    assert np.allclose(meshes[(variant,'led-retainer')].extents,[139.23,23.78,2.4],atol=.01)
    evidence.append(f'PASS {variant}: {8 if wide else 4} wheels,4 motors; all wheels inside {width}mm width;13.5mm tire projection; wheel top-insertion path clear; no wheel/shaft/battery/tray/shell/LCD/LED interference')
    print(evidence[-1],flush=True)
# The default shared-module parameters must retain the delivered eight-wheel shape.
for part in ['robot-shell','robot-lid']:
    raw=TMP/('regression-'+part+'.stl');scad(raw,part,False,155,['--export-format','binstl'],ROOT/'cad/wopr-variants.scad')
    m=trimesh.load(raw,force='mesh');old=trimesh.load(ROOT/'output/variants/robot'/(part+'.stl'),force='mesh')
    m.apply_translation(-m.bounds[0]);old.apply_translation(-old.bounds[0])
    assert np.allclose(m.extents,old.extents,atol=.001) and abs(m.volume-old.volume)<.02,(part,'regression')
    assert len(m.faces)==len(old.faces),(part,'topology changed')
evidence.append('PASS: delivered eight-wheel shell/lid volume, extents and face counts unchanged')
for name,digest in preserved.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
evidence.append('PASS: every previous variant deliverable byte-for-byte unchanged')
(OUT/'verification.txt').write_text('\n'.join(evidence)+'\n')
print('PASS: concealed geometry and preservation checks',flush=True)

# Self-contained source files open directly in the requested configuration.
for variant,(wide,width) in variants.items():
    base=(ROOT/'cad/wopr.scad').read_text().replace('panels_per_side=7;','panels_per_side=6;').replace('W=155;',f'W={width};').replace('part = "assembly";','part = "concealed";')
    middle=(ROOT/'cad/wopr-variants.scad').read_text().replace('include <wopr.scad>',base)
    source=SCAD.read_text().replace('include <wopr-variants.scad>',middle).replace('hidden_wide=false;',f'hidden_wide={str(wide).lower()};')
    (OUT/variant/('wopr-'+variant+'.scad')).write_text(source)
import xml.etree.ElementTree as ET
NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'; ET.register_namespace('',NS)
def tag(n):return '{'+NS+'}'+n
for variant in variants:
    model=ET.Element(tag('model'),{'unit':'millimeter'});res=ET.SubElement(model,tag('resources'))
    mats=ET.SubElement(res,tag('basematerials'),{'id':'1'})
    for n,col in [('Gray','#686E75FF'),('White','#FAFAF5FF')]:ET.SubElement(mats,tag('base'),{'name':n,'displaycolor':col})
    for i,name in enumerate([parts[0],'white-text']):
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


from concurrent.futures import ThreadPoolExecutor
angles=[('Front',(0,-1,0)),('Rear',(0,1,0)),('Low end',(-1,0,0)),('Tower end',(1,0,0)),('Top oblique',(.22,-.28,1)),('Bottom oblique',(.22,-.28,-1)),('Front oblique',(1,-1,.8)),('Rear oblique',(-1,1,.8))]
header='include <'+str(SCAD).replace('\\','/')+'>\n'
def imp(v,n,color='[.40,.43,.46]',move=''):
    return move+'color('+color+') import("'+str(TMP/(v+'-'+n+'.stl')).replace('\\','/')+'");\n'
scenes={};catalog=[]
for variant,(wide,width) in variants.items():
    for name in parts:
        if wide and name in ['robot-cap','wheel-hood-front','wheel-hood-rear','led-retainer','fit-coupon']:continue
        key=variant+'-'+name;scenes[key]=(variant,header+imp(variant,name),meshes[(variant,name)].bounds.mean(axis=0));catalog.append((variant,name,key))
    assembly=imp(variant,'concealed-shell')+imp(variant,'white-text','[.98,.98,.96]')+''.join(imp(variant,n) for n in ['concealed-floor','robot-lid','concealed-tray'])+'color([.5,.53,.56]) hidden_pods() motor_cap();color([.47,.50,.53]) hidden_hoods();hidden_hardware();reference_parts();'
    scenes[variant+'-assembly']=(variant,header+assembly,np.array([139.7,width/2,75]))
    exploded=imp(variant,'concealed-shell',move='translate([0,0,100]) ')+imp(variant,'white-text','[.98,.98,.96]','translate([0,0,100]) ')+imp(variant,'concealed-floor')+imp(variant,'robot-lid',move='translate([0,0,170]) ')+imp(variant,'concealed-tray',move='translate([0,0,65]) ')+'color([.5,.53,.56]) hidden_pods() motor_cap();color([.47,.50,.53]) hidden_hoods();hidden_hardware();'
    scenes[variant+'-exploded']=(variant,header+exploded,np.array([139.7,width/2,145]))
    scenes[variant+'-interior']=(variant,header+imp(variant,'concealed-floor')+imp(variant,'concealed-tray',move='translate([0,0,70]) ')+'color([.5,.53,.56]) hidden_pods() motor_cap();color([.47,.50,.53]) hidden_hoods();hidden_hardware();',np.array([139.7,width/2,70]))
for key,(variant,scene,center) in scenes.items():(TMP/(key+'.scad')).write_text(scene)
jobs=[(key,i) for key in scenes for i in range(8) if not(key.endswith(('exploded','interior')) and i!=6)]
def render(job):
    key,i=job;variant,scene,center=scenes[key];wide,width=variants[variant];eye=center+np.array(angles[i][1])*650
    path=OUT/'views'/f'{key}-{i}.png';source=TMP/(key+'.scad')
    if key.endswith('white-text') and i in [0,1]:
        clip=f'translate([-100,{-1 if i==0 else width/2},-100]) cube([500,{width/2+1 if i==0 else width},400]);'
        source=TMP/(key+f'-face-{i}.scad');source.write_text(header+'intersection(){'+imp(variant,'white-text')+clip+'}')
    camera=','.join(map(str,[*eye,*center]))
    scad(path,'scene',wide,width,['--imgsize','1000,750','--camera',camera,'--viewall','--autocenter','--projection','o','--colorscheme','Tomorrow','--render=true'],source)
    im=Image.open(path).convert('RGB');box=ImageChops.difference(im,Image.new('RGB',im.size,im.getpixel((0,0)))).getbbox();assert box,key
    im.crop(box).save(path);print('VIEW',key,i,flush=True)
with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(render,jobs))
subprocess.run(['node','C:/Users/Jeremy/.codex/plugins/cache/openai-primary-runtime/pdf/26.909.12148/skills/pdf/container_tools/mark_artifact_operation_started.mjs','--operation-kind','create','--expected-output-count','1','--output-format','pdf'],check=True,capture_output=True,text=True,timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,white
from reportlab.platypus import SimpleDocTemplate,Paragraph
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from xml.sax.saxutils import escape
import fitz
c=canvas.Canvas(str(TMP/'drawings.pdf'),pagesize=(792,612))
def title(kicker,name,subtitle):
    c.setFillColor(HexColor('#172535'));c.rect(0,0,792,612,fill=1,stroke=0);c.setFillColor(white);c.rect(22,43,748,493,fill=1,stroke=0)
    c.setFont('Helvetica',9);c.drawString(32,587,kicker.upper());c.setFont('Helvetica-Bold',23);c.drawString(32,557,name)
    c.setFillColor(HexColor('#334155'));c.setFont('Helvetica',10);c.drawString(34,517,subtitle)
    c.setFillColor(white);c.setFont('Helvetica',8);c.drawString(32,22,'WOPR CONCEALED DRIVE / 2026-09-28 / mm / physical fit and durability untested')
def pic(key,i,x,y,w,h):
    p=OUT/'views'/f'{key}-{i}.png';im=Image.open(p);scale=min(w/im.width,h/im.height);rw=im.width*scale;rh=im.height*scale
    c.drawImage(str(p),x+(w-rw)/2,y+(h-rh)/2,rw,rh)
def grid(key):
    for i,(label,_) in enumerate(angles):
        x=37+(i%4)*181;y=285 if i<4 else 66
        pic(key,i,x,y,170,174);c.setFillColor(HexColor('#334155'));c.setFont('Helvetica-Bold',9);c.drawString(x,y+181,label)
    c.showPage()
title('Two additional variants','Wheels tucked under the WOPR','Four motors in each. Previous eight-wheel robot retained. Six RGB modules per side.')
pic('four-wheel-assembly',6,40,182,338,295);pic('wide-eight-wheel-assembly',6,414,182,338,295)
c.setFillColor(HexColor('#334155'));c.setFont('Helvetica-Bold',12);c.drawString(44,156,'FOUR WHEELS / 155 mm wide');c.drawString(414,156,'EIGHT WHEELS / 210 mm wide')
c.setFont('Helvetica',10)
for j,line in enumerate(['Both versions: 279.4 mm long; 178.5 mm nominal total height.', 'Only 13.5 mm of tire projects below the skirt. Tire sides remain inside the body.', 'Closed wheel tubs, raised motor clamps, bolted main lid and retained battery.', 'This packet includes eight views per assembly and unique printed part.']):c.drawString(44,127-j*18,line)
c.showPage()
for variant,(wide,width) in variants.items():
    title('Eight-angle assembly',('Wide eight-wheel' if wide else 'Four-wheel')+' robot',f'Body width {width} mm; axle Z18; tire bottom Z-13.5; four upright motors.');grid(variant+'-assembly')
    title('Assembly breakdown',('Wide eight-wheel' if wide else 'Four-wheel')+' service access','Matching shell and floor required. Raised clamps anchor into the floor; unused shafts stay inside.')
    pic(variant+'-exploded',6,40,65,460,427);pic(variant+'-interior',6,508,166,244,300)
    c.setFillColor(HexColor('#334155'));c.setFont('Helvetica',9)
    for j,line in enumerate(['Main lid lifts separately','LCD tower stays closed','Tray above battery','Four braced motor cradles','Closed wheel tubs','Eight base fasteners']):c.drawString(521,150-j*14,line)
    c.showPage()
for variant,name,key in catalog:
    dims=' x '.join(f'{v:.2f}' for v in meshes[(variant,name)].extents)
    label='shared part' if name in ['robot-cap','wheel-hood-front','wheel-hood-rear','led-retainer','fit-coupon'] else variant
    sub='Front/rear show nearest lettering face; obliques show both.' if name=='white-text' else 'Actual mesh; top/bottom tilted to show pocket depth.'
    title('Printed part / '+label,name,'Bounds: '+dims+' mm. '+sub);grid(key)
c.save()
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='BodyW',fontName='Helvetica',fontSize=10,leading=14,spaceAfter=7,textColor=HexColor('#172535')))
styles['Heading1'].textColor=HexColor('#172535');styles['Heading2'].textColor=HexColor('#9A431C');flow=[]
for block in (ROOT/'cad/CONCEALED.md').read_text().split('\n\n'):
    block=block.strip()
    if not block:continue
    if block.startswith('# '):flow.append(Paragraph(escape(block[2:]),styles['Heading1']))
    elif block.startswith('## '):flow.append(Paragraph(escape(block[3:]),styles['Heading2']))
    else:
        for row in block.split('\n'):
            flow.append(Paragraph('<link href="'+escape(row)+'">'+escape(row)+'</link>' if row.startswith('https://') else escape(row),styles['BodyW']))
def footer(c,doc):
    c.setFont('Helvetica',8);c.setFillColor(HexColor('#475569'));c.drawString(36,24,'WOPR / concealed drive assembly and commissioning / 2026-09-28')
SimpleDocTemplate(str(TMP/'instructions.pdf'),pagesize=(792,612),rightMargin=42,leftMargin=42,topMargin=38,bottomMargin=43).build(flow,onFirstPage=footer,onLaterPages=footer)
final=fitz.open()
for p in ['drawings.pdf','instructions.pdf']:
    with fitz.open(TMP/p) as doc:final.insert_pdf(doc)
for i,p in enumerate(final):p.insert_text((722,590),f'{i+1}/{len(final)}',fontsize=8,color=(.5,.5,.5))
final.set_metadata({'title':'WOPR - concealed four-wheel and wide eight-wheel robots','author':'Jeremy Proffitt / WOPR'})
PDF=ROOT/'output/pdf/wopr-concealed.pdf';final.save(PDF);final.close()
with fitz.open(PDF) as doc:
    for i,p in enumerate(doc):
        assert len(p.get_text())>80;p.get_pixmap(matrix=fitz.Matrix(1.2,1.2),alpha=False).save(TMP/f'page-{i+1:02}.png')
    evidence.append(f'PDF: {len(doc)} pages; eight-angle assemblies and part catalog; text extraction and rasterization passed')
for name,digest in preserved.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
(OUT/'verification.txt').write_text('\n'.join(evidence)+'\n')
with zipfile.ZipFile(OUT/'wopr-concealed-kit.zip','w',zipfile.ZIP_DEFLATED) as z:
    for variant in variants:
        for p in (OUT/variant).iterdir():z.write(p,p.relative_to(ROOT))
    for p in [ROOT/'cad/wopr.scad',ROOT/'cad/wopr-variants.scad',SCAD,ROOT/'cad/build-concealed.py',ROOT/'cad/CONCEALED.md',ROOT/'firmware/wopr-robot/wopr-robot.ino',OUT/'verification.txt']:z.write(p,p.relative_to(ROOT))
with zipfile.ZipFile(OUT/'wopr-concealed-kit.zip') as z:assert z.testzip() is None
print('PASS: concealed variants, PDF and print kit',flush=True)
