"""Rebuild the WOPR first-draft print kit and PDF from OpenSCAD."""
from pathlib import Path
import json
import os
import subprocess
import zipfile
import xml.etree.ElementTree as ET

import numpy as np
import trimesh
from PIL import Image, ImageChops
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
import fitz

ROOT = Path(__file__).resolve().parents[1]
SCAD = ROOT / 'cad/wopr.scad'
OUT = ROOT / 'output'
KIT = OUT / 'model'
VIEWS = OUT / 'views'
TMP = ROOT / 'tmp/pdfs'
EXE = os.environ.get('OPENSCAD', 'C:/Users/Jeremy/tools/openscad-nightly/openscad.exe')
HIDDEN = {'creationflags': subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {}
for folder in [KIT, VIEWS, TMP, OUT / 'pdf']:
    folder.mkdir(parents=True, exist_ok=True)

# Supply only font directories; no machine state is included in the kit.
fontconfig = TMP / 'fonts.conf'
fontconfig.write_text('<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig><dir>C:/Windows/Fonts</dir><cachedir>'+str(TMP/'font-cache')+'</cachedir></fontconfig>')
ENV = dict(os.environ, FONTCONFIG_FILE=str(fontconfig))
evidence = []

def scad(path, part='assembly', extra=()):
    args = [EXE, '--backend', 'Manifold', '--hardwarnings', '-o', str(path), '-D', f'part="{part}"', *extra, str(SCAD)]
    result = subprocess.run(args, capture_output=True, text=True, env=ENV, timeout=180, **HIDDEN)
    if result.returncode or 'ERROR:' in result.stderr or 'WARNING:' in result.stderr:
        raise RuntimeError(f'OpenSCAD {part}: {result.stderr}')
    if not path.exists() or not path.stat().st_size:
        raise RuntimeError(f'No output: {path}')

meshes = {}
offsets = {'gray-shell':[0,0,0], 'white-text':[0,0,0],
           'base':[3.3,3.3,3], 'fit-coupon':[199,0,93],
           'cup-main-shallow-left':[14,22,40], 'cup-main-shallow-right':[14,22,40], 'cup-tower':[199,43,65],
           'led-retainer':None}
for part, offset in offsets.items():
    raw = TMP / f'{part}.stl'
    scad(raw, part, ['--export-format', 'binstl'])
    mesh = trimesh.load(raw, force='mesh')
    assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume > 0, part
    if part != 'white-text':
        assert len(mesh.split()) == 1, f'{part} contains disconnected structure'
    mesh.apply_translation(-np.array(offset if offset is not None else mesh.bounds[0]))
    mesh.export(KIT / f'{part}.stl')
    meshes[part] = mesh
    line = f'{part}: watertight=True; bounds_mm=' + ' x '.join(f'{n:.3f}' for n in mesh.extents)
    evidence.append(line)
    print(line, flush=True)

body_bounds = np.array([meshes[name].bounds + offsets[name] for name in
                        ['gray-shell','white-text','base']])
envelope = body_bounds[:,1,:].max(axis=0) - body_bounds[:,0,:].min(axis=0)
assert np.allclose(envelope,[279.4,155,165],atol=.06), envelope
assert np.allclose(meshes['fit-coupon'].extents,[74,36.9,62],atol=.01)
# Slice the actual front lip, before the rear glass relief and blind screw holes.
lcd_section=meshes['fit-coupon'].section(plane_origin=[0,0.5,0],plane_normal=[0,1,0])
assert lcd_section is not None,'Missing LCD front section'
lcd_openings=[loop for loop in lcd_section.discrete
              if np.allclose(np.ptp(loop[:,[0,2]],axis=0),[50.1,39.6],atol=.01)]
assert len(lcd_openings)==1,'LCD opening must measure 50.1 x 39.6 mm'
assert np.allclose(lcd_openings[0][:,[0,2]].min(axis=0),[13.7,10.2],atol=.01),'LCD edge offsets incorrect'
evidence.append('PASS: LCD opening 50.10 x 39.60 mm; left +4.5, right -1.0, top -2.0, bottom unchanged')
assert all(m.extents[0] <= 279.41 and m.extents[1] <= 155.01 for m in meshes.values())
assert np.allclose(meshes['base'].extents,[272.8,148.4,6],atol=.01)
assert abs((meshes['base'].bounds[0,2]+offsets['base'][2])-meshes['gray-shell'].bounds[0,2]-3)<.01
for name in ['cup-main-shallow-left','cup-main-shallow-right']:
    assert np.allclose(meshes[name].extents,[169,111,88],atol=.01)
assert np.allclose(meshes['led-retainer'].extents,[160.485,23.78,2.4],atol=.01)

def floor_z(mesh,x,y):
    triangles=mesh.triangles
    a=triangles[:,1,:]-triangles[:,0,:]; b=triangles[:,2,:]-triangles[:,0,:]
    delta=np.array([x,y])-triangles[:,0,:2]
    det=a[:,0]*b[:,1]-b[:,0]*a[:,1]
    valid=abs(det)>1e-9
    u=np.divide(delta[:,0]*b[:,1]-b[:,0]*delta[:,1],det,out=np.zeros_like(det),where=valid)
    v=np.divide(a[:,0]*delta[:,1]-delta[:,0]*a[:,1],det,out=np.zeros_like(det),where=valid)
    hit=valid&(u>=-1e-6)&(v>=-1e-6)&(u+v<=1.000001)
    assert hit.any(),(x,y)
    return np.max(triangles[hit,0,2]+u[hit]*a[hit,2]+v[hit]*b[hit,2])

for name,reverse in [('cup-main-shallow-left',False),('cup-main-shallow-right',True)]:
    mesh=meshes[name]
    for y in [37,64,91,118]:
        x=140 if reverse else 57
        assert abs(mesh.bounds[1,2]-floor_z(mesh,x-14,y-22)-38.1)<.01,(name,'shallow depth')
    for x in [119.25,160.75]:
        for y in [50.5,104.5]:
            actual_x=197-x if reverse else x
            assert abs(mesh.bounds[1,2]-floor_z(mesh,actual_x-14,y-22)-85)<.01,(name,'deep depth')
    for x,y in [(57,50.5),(57,77.5),(57,104.5),(98.5,37),(140,50.5),(119.25,77.5)]:
        actual_x=197-x if reverse else x
        assert abs(floor_z(mesh,actual_x-14,y-22)-88)<.01,(name,'divider')
tower=meshes['cup-tower']
for x in [217,250]:
    for y in [69,118]:
        assert abs(tower.bounds[1,2]-floor_z(tower,x-199,y-43)-97)<.06,'tower cells'
evidence.append('PASS: 3.00 mm base underside recess; inset base 272.8 x 148.4 x 6 mm')
evidence.append('PASS: both main-cup variants: four 38.10 mm shallow cells and four 85 mm deep cells; tower four 97 mm cells')
evidence.append('LED layout: 7 panels per side; 14 total; 840 LEDs; bank=148.485 mm; retainer=160.485 mm')
evidence.append('Envelope: nominal 279.4 x 155 x 165 mm; display bay depth=36.9 mm (2+9.5+25.4)')
probe_path = TMP / 'clearance-probe.stl'
scad(probe_path, 'check-clearances', ['--export-format', 'binstl'])
probe = trimesh.load(probe_path, force='mesh')
assert np.allclose(probe.bounds,[[-20,-20,-20],[-19,-19,-19]],atol=1e-5), 'Mechanical clearance failed'
assert abs(probe.volume-1) < 1e-5, 'Mechanical interference detected'
evidence.append('PASS: rear PCB insertion, cup removal, compartment voids/dividers, inset plate fit, screw-head clearance, display bay and LCD pilots')
print(evidence[-1],flush=True)

# Standard 3MF material parts preserve the common origin of gray and white.
NS = 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
ET.register_namespace('', NS)
def tag(n): return f'{{{NS}}}{n}'
model = ET.Element(tag('model'), {'unit':'millimeter', 'xml:lang':'en-US'})
resources = ET.SubElement(model, tag('resources'))
mats = ET.SubElement(resources, tag('basematerials'), {'id':'1'})
for name, color in [('Gray','#686E75FF'),('White','#FAFAF5FF')]:
    ET.SubElement(mats, tag('base'), {'name':name, 'displaycolor':color})
def add_mesh(objid, name, material=0):
    obj = ET.SubElement(resources, tag('object'), {'id':str(objid),'type':'model','name':name,'pid':'1','pindex':str(material)})
    body = ET.SubElement(obj,tag('mesh'))
    verts = ET.SubElement(body,tag('vertices'))
    for v in meshes[name].vertices:
        ET.SubElement(verts,tag('vertex'),dict(zip(['x','y','z'],[f'{a:.6f}' for a in v])))
    faces = ET.SubElement(body,tag('triangles'))
    for face in meshes[name].faces:
        ET.SubElement(faces,tag('triangle'),dict(zip(['v1','v2','v3'],[str(a) for a in face])))
for objid, name, material in [(2,'gray-shell',0),(3,'white-text',1)]:
    add_mesh(objid,name,material)
assembly = ET.SubElement(resources,tag('object'),{'id':'4','type':'model','name':'WOPR one-piece shell - assign gray and white'})
components = ET.SubElement(assembly,tag('components'))
for n in [2,3]: ET.SubElement(components,tag('component'),{'objectid':str(n)})
ET.SubElement(ET.SubElement(model,tag('build')),tag('item'),{'objectid':'4'})
mf = KIT / 'shell-two-color.3mf'
with zipfile.ZipFile(mf,'w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))
with zipfile.ZipFile(mf) as z:
    assert z.testzip() is None
    check = ET.fromstring(z.read('3D/3dmodel.model'))
    assert len(check.findall('.//'+tag('component'))) == 2
    assert len(check.findall('.//'+tag('base'))) == 2
evidence.append('3MF: two material parts, one build object, valid ZIP/XML')

# Bambu's GUI rejects a single import batch that mixes .3mf and .stl suffixes.
# Deliver one geometry-only 3MF, with separate objects and the shell's material parts.
for objid,name in [(5,'base'),(6,'cup-main-shallow-left'),(7,'cup-tower'),(8,'led-retainer'),(9,'fit-coupon'),(10,'cup-main-shallow-right')]:
    add_mesh(objid,name)
build=model.find(tag('build'))
build[0].set('transform','1 0 0 0 1 0 0 0 1 10 10 0')
for objid,x,y in [(5,310,10),(6,10,190),(7,190,190),(8,310,190),(8,310,230),(9,500,190),(10,10,320)]:
    ET.SubElement(build,tag('item'),{'objectid':str(objid),'transform':f'1 0 0 0 1 0 0 0 1 {x} {y} 0'})
parts_project=KIT/'wopr-parts.3mf'
with zipfile.ZipFile(mf) as original, zipfile.ZipFile(parts_project,'w',zipfile.ZIP_DEFLATED) as z:
    for name in original.namelist():
        z.writestr(name,ET.tostring(model,encoding='utf-8',xml_declaration=True) if name=='3D/3dmodel.model' else original.read(name))
with zipfile.ZipFile(parts_project) as z:
    assert z.testzip() is None
    parts_xml=ET.fromstring(z.read('3D/3dmodel.model'))
    assert len(parts_xml.findall('./'+tag('build')+'/'+tag('item')))==8
    assert 'Metadata/project_settings.config' not in z.namelist()
evidence.append('Bambu handoff: one wopr-parts.3mf, eight spaced build items including both alternative main cups, no printer presets')

views = {
    'hero': ('430,-450,310,139,70,80','assembly',True),
    'rear': ('-280,510,300,139,70,80','assembly',True),
    'empty': ('430,-450,310,139,70,80','assembly',False),
    'front': ('139.7,-550,82.5,139.7,77.5,82.5','assembly',True),
    'back': ('139.7,700,82.5,139.7,77.5,82.5','assembly',True),
    'left': ('-600,77.5,82.5,139.7,77.5,82.5','assembly',True),
    'right': ('750,77.5,82.5,139.7,77.5,82.5','assembly',True),
    'top': ('139.7,77.5,800,139.7,77.5,0','plan-section',False),
    'bottom': ('139.7,77.5,-800,139.7,77.5,0','assembly',False),
    'section': ('-500,77.5,82.5,236,77.5,82.5','section',True),
    'coupon': ('330,-150,220,236,15,124','fit-coupon',False),
    'rear-mounts': ('330,-400,-290,139,70,80','rear-mounts',True),
    'cup-left-top': ('98.5,77.5,550,98.5,77.5,0','cup-plan-left',False),
    'cup-right-top': ('98.5,77.5,550,98.5,77.5,0','cup-plan-right',False),
    'cup-main-section': ('98.5,-250,84,98.5,60,84','cup-main-section',False),
    'cup-tower-detail': ('360,-160,280,233.5,93.5,115','cup-tower',False),
    'base-section': ('-120,16,13,12,16,13','base-section',False),
}
for name, (camera, part, electronic) in views.items():
    path = VIEWS / f'{name}.png'
    scad(path, part, ['--imgsize','1800,1200','--camera',camera,'--viewall','--autocenter',
         '--projection','o','--colorscheme','Tomorrow','--render=true','-D',f'electronics={str(electronic).lower()}'])
    im = Image.open(path).convert('RGB')
    background = Image.new('RGB', im.size, im.getpixel((0,0)))
    box = ImageChops.difference(im,background).getbbox()
    assert box, name
    im.crop(box).save(path)
    print('view:',name,flush=True)

PAGE_W, PAGE_H = 792,612
PDF = OUT / 'pdf/wopr-first-draft.pdf'
c = canvas.Canvas(str(PDF),pagesize=(PAGE_W,PAGE_H))
c.setTitle('W.O.P.R. | 11-inch first-draft print model')
c.setAuthor('Jeremy Proffitt - WOPR project')
NAVY=HexColor('#172535'); GRAY=HexColor('#475569'); ACCENT=HexColor('#AD481F')
page=0
def text(x,y,s,size=10,color=NAVY,font='Helvetica'):
    c.setFillColor(color); c.setFont(font,size); c.drawString(x,y,s)
def lines(x,y,rows,size=10,leading=15):
    for row in rows: text(x,y,row,size); y-=leading
def start(kicker,title,subtitle):
    global page
    page+=1
    c.setFillColor(white); c.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0)
    text(36,579,kicker.upper(),9,ACCENT,'Helvetica-Bold')
    text(36,548,title,25,NAVY,'Helvetica-Bold')
    text(36,527,subtitle,10,GRAY)
    c.setStrokeColor(HexColor('#CBD5E1')); c.line(36,39,756,39)
    text(36,24,'W.O.P.R. / DRAFT 07 / 2026-09-27 / dimensions in mm / not to print scale',8,GRAY)
    text(714,24,f'{page:02d} / 08',8,GRAY)
def pic(name,x,y,w,h):
    im=Image.open(VIEWS/f'{name}.png'); iw,ih=im.size
    scale=min(w/iw,h/ih); rw,rh=iw*scale,ih*scale
    px=x+(w-rw)/2; py=y+(h-rh)/2
    c.drawImage(str(VIEWS/f'{name}.png'),px,py,rw,rh)
    return px,py,rw,rh
def dim_h(x,y,w,label):
    c.setStrokeColor(GRAY); c.setLineWidth(.6); c.line(x,y,x+w,y)
    for a in [x,x+w]: c.line(a,y-4,a,y+6); c.line(a-2,y-2,a+2,y+2)
    c.setFont('Helvetica',9); c.setFillColor(GRAY); c.drawCentredString(x+w/2,y+5,label)
def dim_v(x,y,h,label):
    c.setStrokeColor(GRAY); c.setFillColor(GRAY); c.line(x,y,x,y+h)
    for a in [y,y+h]: c.line(x-4,a,x+5,a)
    c.saveState(); c.translate(x-6,y+h/2); c.rotate(90); c.setFont('Helvetica',9); c.drawCentredString(0,0,label); c.restoreState()
def end(): c.showPage()

start('Design review','W.O.P.R. / divided storage and inset base','Seven RGB panels per side. Two main-cup layouts. Recessed screw heads. Gray and flush white text.')
pic('hero',34,116,724,395)
lines(40,91,['279.4 x 155 x 165 mm  |  11.00 x 6.10 x 6.50 in  |  3 mm nominal shell',
             'OpenSCAD model render. Colored LEDs and display are hardware previews, not printed material.'],10,17)
end()
start('Mockups','Seven-panel banks, the same case','Fourteen boards total: seven adjacent boards behind one continuous window on each side.')
pic('rear',40,251,410,254); pic('empty',455,279,295,209)
text(460,264,'CASE WITHOUT ELECTRONICS',9,ACCENT,'Helvetica-Bold')
lines(40,222,['The tower cup has crossed dividers, making four deep compartments.',
              'Both long sides carry white W.O.P.R. / War Operation Plan Response lettering.',
              'The main touchscreen is on one side, directly above its logo.',
              'Main cup: four shallow compartments in one half, four deep compartments in the other.',
              'The inset base has 3 mm of screw-head space above the lower body edge.'],11,23)
text(40,73,'Remove the pen cups and base for rear access. Fit the electronics first, then lower the cups into place.',9,GRAY)
end()
start('Orthographic drawings','Overall envelope and panel placement','All views below come from the same SCAD geometry. Dimensions are nominal, not a film-prop measurement.')
fx,fy,fw,fh=pic('front',64,240,410,242)
text(64,495,'PRIMARY LONG SIDE',9,ACCENT,'Helvetica-Bold')
dim_h(fx,fy-20,fw,'279.4 / 11.00 in'); dim_v(fx-18,fy,fh,'165 / 6.50 in')
sx,sy,sw,sh=pic('right',526,240,220,242)
text(526,495,'TOWER END',9,ACCENT,'Helvetica-Bold'); dim_h(sx,sy-20,sw,'155 / 6.10 in')
lines(64,182,['LED centers: X = 31.235 + i x 21.255; i = 0 through 6.',
              'TFT center: X = 236; Z = 124. Lower case top: Z = 128.',
              'Spine top: Z = 137. Tower top: Z = 165.',
              'Shell: 279.4 mm long. Inset base: 272.8 x 148.4 mm.'],10,21)
lines(526,182,['Rear TFT pocket: 65.6 x 53.6.', 'Front TFT window: 50.1 x 39.6.', 'Rear LED bank pocket:', '149.085 wide x 18.38 high.'],10,21)
end()
start('Orthographic drawings','Top, rear and service access','Common axes: X along the 11-inch length, Y front to rear, Z up from the base.')
tx,ty,tw,th=pic('top',47,284,342,201)
text(47,500,'PLAN SECTION / Z = 127',9,ACCENT,'Helvetica-Bold'); dim_h(tx,ty-18,tw,'279.4'); dim_v(tx-12,ty,th,'155')
pic('back',420,275,331,207); text(420,500,'OPPOSITE LONG SIDE',9,ACCENT,'Helvetica-Bold')
pic('bottom',49,70,330,170); text(420,239,'BOTTOM / ONE REMOVABLE BASE',9,ACCENT,'Helvetica-Bold')
lines(420,218,['Main cup: 38.1 mm shallow / 85 mm deep.',
               'Tower cup: crossed dividers, four deep cells.',
               'Both cups have 3 mm walls, floors and dividers.',
               'Lift the cups out to reach the rear fasteners.',
               'Eight M3 base screws; 3.3 clearance / 2.5 pilots.',
               'Cup-to-case clearance: 0.30 mm per side.'],10,22)
end()
start('Cup drawings','Both main-cup versions are included','Print either main-cup STL. Left/right is defined when looking at the W.O.P.R. logo side.')
pic('cup-left-top',40,290,330,205); pic('cup-right-top',422,290,330,205)
text(40,500,'SHALLOW LEFT / FOUR SHALLOW + FOUR DEEP',8,ACCENT,'Helvetica-Bold')
text(422,500,'SHALLOW RIGHT / MIRRORED LAYOUT',8,ACCENT,'Helvetica-Bold')
pic('cup-main-section',42,75,405,170)
text(42,257,'MAIN CUP SECTION / LEVEL RIM AT Z = 128',9,ACCENT,'Helvetica-Bold')
pic('cup-tower-detail',530,76,200,176)
text(520,257,'TOWER / FOUR COMPARTMENTS',9,ACCENT,'Helvetica-Bold')
lines(47,63,['Shallow: 38.1 mm (1.50 in). Deep: 85 mm. Main-cup dividers: 3 mm thick.'],9,14)
end()
start('Base drawing','The base sits inside the body','Exactly 3 mm from the underside of the plate to the bottom edge of the body.')
pic('base-section',50,193,325,295)
text(48,173,'SECTION THROUGH A FRONT BASE SCREW',9,ACCENT,'Helvetica-Bold')
# Dimensioned section keyed to the real SCAD Z planes: 0, 3 and 9 mm.
bx=465; by=192; s=12
c.setFillColor(HexColor('#475569')); c.rect(bx-18,by,18,20*s,fill=1,stroke=0)
c.setFillColor(HexColor('#E9EEF3')); c.rect(bx,by,205,3*s,fill=1,stroke=0)
c.setFillColor(HexColor('#94A3B8')); c.rect(bx,by+3*s,205,6*s,fill=1,stroke=0)
c.setFillColor(HexColor('#475569')); c.rect(bx,by+9*s,100,10*s,fill=1,stroke=0)
text(bx+15,by+12,'SCREW-HEAD SPACE',9,GRAY)
text(bx+18,by+67,'6 mm BASE PLATE',11,NAVY,'Helvetica-Bold')
text(bx+8,by+157,'SCREW BOSS',9,white)
dim_v(bx+220,by,3*s,'3.0 mm')
dim_v(bx+246,by+3*s,6*s,'6.0 mm')
text(bx-20,by-20,'BODY BOTTOM / Z = 0',9,ACCENT,'Helvetica-Bold')
lines(48,137,['Base footprint: 272.8 x 148.4 mm, inside the 279.4 x 155 mm body.',
              '3.3 mm inset per side = 3 mm shell wall + 0.3 mm assembly clearance.',
              'Plate underside Z = 3. Plate top and screw-boss seats Z = 9.',
              'Use M3 heads no taller than 3 mm; the old counterbores have been removed.'],10,20)
end()
start('Mount drawing','A full inch behind the display','Section through X = 236. The bay is open at the rear for wires and installation from below.')
sx,sy,sw,sh=pic('section',44,183,330,306)
text(44,163,'SCAD SECTION / LOOKING ALONG X',9,ACCENT,'Helvetica-Bold')
# Explicit dimension chain, keyed to modeled Y coordinates.
x0=439; yy=316; factor=7.5
text(420,489,'DEPTH CHAIN / DETAIL',10,ACCENT,'Helvetica-Bold')
for a,b,col in [(0,2,'#CBD5E1'),(2,11.5,'#475569'),(11.5,36.9,'#E8EEF3')]:
    c.setFillColor(HexColor(col)); c.rect(x0+a*factor,yy,(b-a)*factor,104,fill=1,stroke=0)
dim_h(x0,yy+129,2*factor,'2.0')
dim_h(x0+2*factor,yy-22,9.5*factor,'9.5 hardware')
dim_h(x0+11.5*factor,yy+129,25.4*factor,'25.4 / 1.00 in clear')
text(425,yy+47,'OUTSIDE',8,GRAY); text(x0+16*factor,yy+47,'CLEAR REAR BAY',9,GRAY)
dim_h(x0,yy-54,36.9*factor,'36.9 from exterior face to bay rear')
lines(420,231,['Rear-loading pocket: 65.6 x 53.6; front bezel hides PCB.',
               'Front opening: 50.1 x 39.6; left +4.5, right -1, top -2.',
               'Four hidden blind pilots: diameter 1.8 for M2 screws.',
               'V2 hole pitch: 59.690 x 47.498 (landscape).',
               'Front glass is nominally 2 mm below the case face.',
               'Tower cup starts at Y = 43, beyond the 36.9 mm bay.',
               'The 25.4 mm bay excludes the 9.5 mm hardware depth.'],9,20)
text(44,93,'Mount positions follow manufacturer CAD; assembly thickness and tolerances still need a physical check.',10,GRAY)
end()
start('Print kit and evidence','Install from the inside','Rear access shown with the base and removable pen cups removed. Physical fit remains untested.')
pic('rear-mounts',45,283,235,209)
text(47,269,'UNDERSIDE / REAR MOUNTING ACCESS',8,ACCENT,'Helvetica-Bold')
lines(310,488,['PRINT FILES',
              'OPEN wopr-parts.3mf alone in Bambu Studio.',
              'gray-shell.stl: one continuous structural case.',
              'white-text.stl: aligned lettering; import with gray-shell.',
              'base.stl: one continuous removable underside.',
              'cup-main-shallow-left / shallow-right: choose ONE.',
              'cup-tower.stl: four compartments with crossed dividers.',
              'led-retainer.stl: print two; screws enter from inside.',
              '3 mm walls/dividers. White text: 0.8 mm deep, flush.',
              'No splice strips. Test fit-coupon.stl before the case.',
              'Shell and base need a 280 x 155 mm area, plus brim.',
              'Assign the two filament colors explicitly in the slicer.'],10,20)
lines(44,222,['CHECKED: Eight STL exports are watertight; each structural part is a single solid.',
              'CHECKED: 3 mm base recess, 38.1 mm shallow cells, dividers and mounting clearances.',
              'NOT CHECKED: Actual print, hardware fit, touch access, electrical power or operating temperature.',
              'Proportions are adapted from visual references. This is a review draft, not a measured replica.'],10,19)
text(44,143,'SOURCES / MANUFACTURER DATA AND VISUAL REFERENCE',8,ACCENT,'Helvetica-Bold')
sources=[('Seeed product + board CAD','https://wiki.seeedstudio.com/rgb_matrix_for_xiao/'),
         ('Adafruit #3315 / 65 x 53 x 9.5 mm','https://www.adafruit.com/product/3315'),
         ('Adafruit V2 mounting geometry','https://github.com/adafruit/Adafruit-2.4-TFT-FeatherWing-PCB'),
         ('Miniatua / visual proportions only','https://www.miniatua.com/work/wopr/')]
for j,(label,url) in enumerate(sources):
    y=126-j*16; text(44,y,label,8,GRAY); text(238,y,url,8,GRAY)
    c.linkURL(url,(238,y-2,750,y+10),relative=0)
end(); c.save()
doc=fitz.open(PDF)
assert len(doc)==8
for i,p in enumerate(doc):
    assert len(p.get_text())>200
    p.get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).save(TMP/f'page-{i+1}.png')
evidence.append('PDF: 8 pages; text and raster renders verified by builder; visual review required')
(OUT/'verification.txt').write_text('\n'.join(evidence)+'\n')
with zipfile.ZipFile(OUT/'wopr-first-draft-kit.zip','w',zipfile.ZIP_DEFLATED) as z:
    for path in [SCAD,ROOT/'cad/README.md',ROOT/'cad/build.py',OUT/'verification.txt',mf,parts_project,*[KIT/f'{n}.stl' for n in offsets]]:
        z.write(path,path.relative_to(ROOT))
print(f'PDF: {PDF}; pages={len(doc)}',flush=True)
print('PASS: all geometry and document checks',flush=True)
