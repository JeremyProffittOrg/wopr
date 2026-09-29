"""Current reinforced print kits; all processes run on the verified private desktop."""
from pathlib import Path
import os,subprocess,json,hashlib,zipfile
import numpy as np
import trimesh
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/reinforced';TMP=ROOT/'tmp/reinforced'
for p in [OUT,TMP,OUT/'views']:p.mkdir(parents=True,exist_ok=True)
SCAD=ROOT/'cad/wopr-reinforced.scad';EXE='C:/Users/Jeremy/tools/openscad-nightly/openscad.exe'
ENV=dict(os.environ,FONTCONFIG_FILE=str(ROOT/'tmp/pdfs/fonts.conf'))
variants={'seven':(155,7),'six':(155,6),'exposed':(155,6),'four':(155,6),'wide':(220,6)}
common=['r-shell','r-white','r-frame','r-retainer','r-lcd-coupon']
parts={v:common+(['r-cup-left','r-cup-right','r-cup-tower'] if v in ['seven','six'] else ['r-lid','r-tray','r-cap','r-frame-zip']) for v in variants}
meshes={};evidence=[]
def scad(path,part,variant,extra=(),source=SCAD):
    width,panels=variants[variant]
    args=[EXE,'--backend','Manifold','--hardwarnings','-o',str(path),'-D',f'part="{part}"','-D',f'edition="{variant}"','-D',f'W={width}','-D',f'panels_per_side={panels}',*extra,str(source)]
    r=subprocess.run(args,capture_output=True,text=True,env=ENV,timeout=180,creationflags=subprocess.CREATE_NO_WINDOW)
    if r.returncode or 'ERROR:' in r.stderr or 'WARNING:' in r.stderr:raise RuntimeError(part+': '+r.stderr)
    assert path.exists() and path.stat().st_size,path
for variant in variants:
    (OUT/variant).mkdir(exist_ok=True)
    for name in parts[variant]:
        raw=TMP/(variant+'-'+name+'.stl');scad(raw,name,variant,['--export-format','binstl'])
        m=trimesh.load(raw,force='mesh');assert m.is_watertight and m.is_winding_consistent and m.volume>0,(variant,name)
        if name!='r-white':assert len(m.split())==1,(variant,name,'components',len(m.split()))
        meshes[(variant,name)]=m
        export=m.copy();export.apply_translation([0,0,0] if name in ['r-shell','r-white'] else -m.bounds[0]);export.export(OUT/variant/(name+'.stl'))
        line=f'{variant}/{name}: watertight; components={len(m.split())}; bounds_mm={np.round(m.extents,3).tolist()}'
        print(line,flush=True);evidence.append(line)
    probe=TMP/(variant+'-check.stl');scad(probe,'r-check',variant,['--export-format','binstl']);m=trimesh.load(probe,force='mesh')
    assert np.allclose(m.bounds,[[-100,-100,-100],[-99,-99,-99]],atol=.001) and abs(m.volume-1)<.001,(variant,'interference',m.bounds,m.volume)
    print('PASS',variant,'assembly clearances',flush=True);evidence.append('PASS '+variant+' assembly clearances')
    if variant not in ['seven','six']:
        scad(probe,'r-check-zip',variant,['--export-format','binstl']);m=trimesh.load(probe,force='mesh')
        assert np.allclose(m.bounds,[[-100,-100,-100],[-99,-99,-99]],atol=.001) and abs(m.volume-1)<.001,(variant,'zip-chassis interference',m.bounds,m.volume)
        evidence.append('PASS '+variant+': standard and zip-tie chassis are single solids; complete motor/wheel installation sweeps clear')
(OUT/'verification.txt').write_text('\n'.join(evidence)+'\n')
# Measure thickness on exported triangles, independently of parameter assertions.
def hits(mesh,axis,a,b):
    other=[i for i in range(3) if i!=axis];tri=mesh.triangles
    u=tri[:,1]-tri[:,0];v=tri[:,2]-tri[:,0];q=np.array([a,b])-tri[:,0,other]
    det=u[:,other[0]]*v[:,other[1]]-v[:,other[0]]*u[:,other[1]];valid=abs(det)>1e-10
    s=np.divide(q[:,0]*v[:,other[1]]-v[:,other[0]]*q[:,1],det,out=np.zeros_like(det),where=valid)
    t=np.divide(u[:,other[0]]*q[:,1]-q[:,0]*u[:,other[1]],det,out=np.zeros_like(det),where=valid)
    mask=valid&(s>=-1e-6)&(t>=-1e-6)&(s+t<=1.000001)
    return np.unique(np.round(tri[mask,0,axis]+s[mask]*u[mask,axis]+t[mask]*v[mask,axis],4))
def thickness(v,n,axis,a,b,expected,interval=0,tol=.06):
    h=hits(meshes[(v,n)],axis,a,b);assert len(h)>interval+1,(v,n,'missing section',h)
    value=h[interval+1]-h[interval];assert abs(value-expected)<tol,(v,n,'thickness',value,expected,h)
    return value
for v,(width,panels) in variants.items():
    robot=v not in ['seven','six'];axle=-22 if v=='exposed' else 18
    thickness(v,'r-shell',1,80,60,5)
    thickness(v,'r-shell',0,width/2,60,5)
    thickness(v,'r-shell',1,210,124,5)
    white_mesh=meshes[(v,'r-white')];assert white_mesh.bounds[0,2]>54 and white_mesh.bounds[1,2]<85
    candidates=np.where((white_mesh.face_normals[:,1]<-.99)&(white_mesh.triangles_center[:,1]<1)&(white_mesh.triangles_center[:,0]>215)&(white_mesh.triangles_center[:,0]<255)&(white_mesh.triangles_center[:,2]>73))[0]
    face=candidates[np.argmax(white_mesh.area_faces[candidates])];point=white_mesh.triangles_center[face]
    thickness(v,'r-shell',1,point[0],point[2],5)
    thickness(v,'r-frame',2,139,width/2,10)
    thickness(v,'r-retainer',2,0,12,5)
    if robot:
        mx=54 if v=='four' else 46.3;my=28 if v=='exposed' else 54
        for frame in ['r-frame','r-frame-zip']:
            foot=hits(meshes[(v,frame)],2,mx,my);assert foot[1]-foot[0]>=9.99,(v,'motor foot below10mm',foot)
            thickness(v,frame,0,my+9,axle+40,5)
            roof=hits(meshes[(v,frame)],2,mx,my-27-6.5);assert abs(roof[-1]-roof[-2]-5)<.06,(v,'wheel roof',roof)
            thickness(v,frame,1,mx+20,1 if v=='exposed' else axle+7,5)
        zip_post=hits(meshes[(v,'r-frame-zip')],2,mx+22,my);assert any(abs((b-a)-5.4)<.06 for a,b in zip(zip_post[::2],zip_post[1::2])),(v,'zip slot web',zip_post)
        thickness(v,'r-cap',2,18,8,5)
        thickness(v,'r-cap',1,0,axle+45,5)
        thickness(v,'r-tray',2,122,width/2,5)
        thickness(v,'r-lid',2,120,30,5)
        roof=hits(meshes[(v,'r-lid')],2,120,30);assert abs(roof[-1]-roof[-2]-5)<.06,(v,'roof',roof)
    else:
        thickness(v,'r-cup-left',2,50,40,5)
        thickness(v,'r-cup-left',2,120,40,5)
        thickness(v,'r-cup-left',1,50,110,5)
        thickness(v,'r-cup-tower',2,220,70,5)
        thickness(v,'r-cup-tower',0,70,110,5)
    evidence.append('PASS '+v+': exported structural5mm sections and '+('10mm one-piece chassis/motor base' if robot else '5mm cup floors/dividers and10mm base')+' measured')
(OUT/'verification.txt').write_text('\n'.join(evidence)+'\n')
print('PASS: all reinforced geometry and thickness checks',flush=True)

for v,(width,panels) in variants.items():
    base=(ROOT/'cad/wopr.scad').read_text().replace('part = "assembly";','part = "r-assembly";').replace('W=155;',f'W={width};').replace('panels_per_side=7;',f'panels_per_side={panels};')
    source=SCAD.read_text().replace('include <wopr.scad>',base).replace('edition="four";',f'edition="{v}";')
    (OUT/v/('wopr-reinforced-'+v+'.scad')).write_text(source)
import xml.etree.ElementTree as ET
NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'; ET.register_namespace('',NS)
def tag(n):return '{'+NS+'}'+n
for variant in parts:
    model=ET.Element(tag('model'),{'unit':'millimeter'});res=ET.SubElement(model,tag('resources'))
    mats=ET.SubElement(res,tag('basematerials'),{'id':'1'})
    for n,col in [('Gray','#686E75FF'),('White','#FAFAF5FF')]:ET.SubElement(mats,tag('base'),{'name':n,'displaycolor':col})
    for i,name in enumerate([parts[variant][0],'r-white']):
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
labels={'seven':'Seven-per-side organizer','six':'Six-per-side organizer','exposed':'Exposed eight-wheel robot','four':'Tucked four-wheel robot','wide':'Wide tucked eight-wheel robot'}
header='include <'+str(SCAD).replace('\\','/')+'>\n'
def imp(v,n,col='[.40,.43,.46]',move=''):
    return move+'color('+col+') import("'+str(TMP/(v+'-'+n+'.stl')).replace('\\','/')+'");\n'
scenes={}
catalog=[('seven','r-shell'),('six','r-shell'),('exposed','r-shell'),('four','r-shell'),('wide','r-shell'),('seven','r-frame'),('exposed','r-frame'),('four','r-frame'),('wide','r-frame'),('seven','r-retainer'),('six','r-retainer'),('seven','r-lcd-coupon'),('seven','r-cup-left'),('seven','r-cup-right'),('seven','r-cup-tower'),('four','r-lid'),('wide','r-lid'),('four','r-tray'),('exposed','r-frame-zip'),('four','r-frame-zip'),('wide','r-frame-zip'),('four','r-cap'),('four','r-white'),('wide','r-white')]
for v,n in catalog:scenes[v+'-'+n]=(v,header+imp(v,n),meshes[(v,n)].bounds.mean(axis=0))
for v,(width,panels) in variants.items():
    robot=v not in ['seven','six']
    fixed=imp(v,'r-frame')
    if robot:
        fixed+=imp(v,'r-tray','[.65,.68,.70]')+imp(v,'r-cap','[.53,.56,.59]','r_pods() ')
    else:fixed+=imp(v,'r-cup-left')+imp(v,'r-cup-tower')
    assembly=imp(v,'r-shell')+imp(v,'r-white','[.98,.98,.96]')+fixed+(imp(v,'r-lid') if robot else '')+'r_hardware();'
    scenes[v+'-assembly']=(v,header+assembly,np.array([139.7,width/2,65]))
    if robot:
        explode=imp(v,'r-shell',move='translate([0,0,100]) ')+imp(v,'r-white','[.98,.98,.96]','translate([0,0,100]) ')+fixed+imp(v,'r-lid',move='translate([0,0,170]) ')
        scenes[v+'-exploded']=(v,header+explode,np.array([139.7,width/2,130]))
for key,(v,code,center) in scenes.items():(TMP/(key+'.scad')).write_text(code)
jobs=[(key,i) for key in scenes for i in range(8) if not(key.endswith('exploded') and i!=6)]
def render(job):
    key,i=job;v,code,center=scenes[key];width,_=variants[v];eye=center+np.array(angles[i][1])*650;source=TMP/(key+'.scad')
    if key.endswith('r-white') and i in [0,1]:
        clip=f'translate([-100,{-1 if i==0 else width/2},-100]) cube([500,{width/2+1 if i==0 else width},400]);'
        source=TMP/(key+f'-face-{i}.scad');source.write_text(header+'intersection(){'+imp(v,'r-white')+clip+'}')
    path=OUT/'views'/f'{key}-{i}.png';camera=','.join(map(str,[*eye,*center]))
    scad(path,'scene',v,['--imgsize','1000,750','--camera',camera,'--viewall','--autocenter','--projection','o','--colorscheme','Tomorrow','--render=true'],source)
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
def title(kicker,name,sub):
    c.setFillColor(HexColor('#172535'));c.rect(0,0,792,612,fill=1,stroke=0);c.setFillColor(white);c.rect(22,43,748,493,fill=1,stroke=0)
    c.setFont('Helvetica',9);c.drawString(32,587,kicker.upper());c.setFont('Helvetica-Bold',22);c.drawString(32,557,name)
    c.setFillColor(HexColor('#334155'));c.setFont('Helvetica',10);c.drawString(34,517,sub)
    c.setFillColor(white);c.setFont('Helvetica',8);c.drawString(32,22,'WOPR REINFORCED / 2026-09-29 / mm / not to scale / physical strength untested')
def pic(key,i,x,y,w,h):
    p=OUT/'views'/f'{key}-{i}.png';im=Image.open(p);scale=min(w/im.width,h/im.height);rw=im.width*scale;rh=im.height*scale
    c.drawImage(str(p),x+(w-rw)/2,y+(h-rh)/2,rw,rh)
def grid(key):
    for i,(label,_) in enumerate(angles):
        x=37+(i%4)*181;y=285 if i<4 else 66
        pic(key,i,x,y,170,174);c.setFillColor(HexColor('#334155'));c.setFont('Helvetica-Bold',9);c.drawString(x,y+181,label)
    c.showPage()
title('Current print kits','One-piece WOPR chassis','5 mm structural walls. 10 mm bases and motor feet. Screw-cap and zip-tie choices.')
pic('wide-r-frame-zip',6,40,177,338,300);pic('wide-assembly',6,414,177,338,300)
c.setFillColor(HexColor('#334155'));c.setFont('Helvetica',10)
for j,line in enumerate(['Both organizers and all three robots are included.', 'Robot chassis, motor mounts and wheel wells form one structural print.', 'Use matching reinforced parts. Earlier thin-wall exports are historical references.', 'Fit coupons and assembly checks are supplied; no load, drop or driving test is claimed.']):c.drawString(44,135-j*19,line)
c.showPage()
for v,(width,panels) in variants.items():
    title('Eight-angle assembly',labels[v],f'Body 279.4 x {width} x 165 mm; {panels} RGB modules per side. Nominal walls 5 mm, base 10 mm.');grid(v+'-assembly')
for v in ['exposed','four','wide']:
    title('Printed assembly breakdown',labels[v],'Shell and lid lifted. Motor mounts and wheel wells are integral with the single-piece chassis.')
    pic(v+'-exploded',6,40,70,450,425);pic(v+'-r-frame-zip',6,520,247,220,215)
    c.setFillColor(HexColor('#334155'));c.setFont('Helvetica',10)
    for j,line in enumerate(['One structural chassis','Integral motor mounts and wells','10 mm base and motor feet','5 mm case and wheel-well walls','Bare motors fit from above','Wheels fit below, then slide inward','Alternative: two zip ties per motor']):c.drawString(508,218-j*20,line)
    c.showPage()
for v,n in catalog:
    dims=' x '.join(f'{a:.2f}' for a in meshes[(v,n)].extents)
    sub='Bounds: '+dims+' mm. '+('Nearest lettering face shown front/rear.' if n=='r-white' else 'Actual checked mesh; top/bottom tilted for depth.')
    title('Printed part / '+labels[v],n,sub);grid(v+'-'+n)
c.save()
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='BodyW',fontName='Helvetica',fontSize=10,leading=14,spaceAfter=7,textColor=HexColor('#172535')))
styles['Heading1'].textColor=HexColor('#172535');styles['Heading2'].textColor=HexColor('#9A431C');flow=[]
for block in (ROOT/'cad/REINFORCED.md').read_text().split('\n\n'):
    block=block.strip()
    if not block:continue
    if block.startswith('# '):flow.append(Paragraph(escape(block[2:]),styles['Heading1']))
    elif block.startswith('## '):flow.append(Paragraph(escape(block[3:]),styles['Heading2']))
    else:
        for row in block.split('\n'):flow.append(Paragraph('<link href="'+escape(row)+'">'+escape(row)+'</link>' if row.startswith('https://') else escape(row),styles['BodyW']))
def footer(c,doc):
    c.setFont('Helvetica',8);c.setFillColor(HexColor('#475569'));c.drawString(36,24,'WOPR / reinforced assembly and verification / 2026-09-29')
SimpleDocTemplate(str(TMP/'instructions.pdf'),pagesize=(792,612),rightMargin=42,leftMargin=42,topMargin=38,bottomMargin=43).build(flow,onFirstPage=footer,onLaterPages=footer)
final=fitz.open()
for p in ['drawings.pdf','instructions.pdf']:
    with fitz.open(TMP/p) as doc:final.insert_pdf(doc)
for i,p in enumerate(final):p.insert_text((722,590),f'{i+1}/{len(final)}',fontsize=8,color=(.5,.5,.5))
final.set_metadata({'title':'WOPR - all five reinforced editions','author':'Jeremy Proffitt / WOPR'})
PDF=ROOT/'output/pdf/wopr-reinforced.pdf';final.save(PDF);final.close()
with fitz.open(PDF) as doc:
    for i,p in enumerate(doc):
        assert len(p.get_text())>80;p.get_pixmap(matrix=fitz.Matrix(1.2,1.2),alpha=False).save(TMP/f'page-{i+1:02}.png')
    evidence.append(f'PDF: {len(doc)} pages; eight-angle assemblies and unique printed parts; text/raster checks passed')
(OUT/'verification.txt').write_text('\n'.join(evidence)+'\n')
with zipfile.ZipFile(OUT/'wopr-reinforced-kit.zip','w',zipfile.ZIP_DEFLATED) as z:
    for v in variants:
        for p in (OUT/v).iterdir():z.write(p,p.relative_to(ROOT))
    for p in [ROOT/'cad/wopr.scad',SCAD,ROOT/'cad/build-reinforced.py',ROOT/'cad/REINFORCED.md',ROOT/'firmware/wopr-robot/wopr-robot.ino',OUT/'verification.txt']:z.write(p,p.relative_to(ROOT))
with zipfile.ZipFile(OUT/'wopr-reinforced-kit.zip') as z:assert z.testzip() is None
print('PASS: all reinforced editions, print kit and PDF',flush=True)
