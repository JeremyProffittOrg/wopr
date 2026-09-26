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
EXE = os.environ.get('OPENSCAD', 'C:/Users/Jeremy/tools/openscad-nightly/openscad.com')
for folder in [KIT, VIEWS, TMP, OUT / 'pdf']:
    folder.mkdir(parents=True, exist_ok=True)

# Supply only font directories; no machine state is included in the kit.
fontconfig = TMP / 'fonts.conf'
fontconfig.write_text('<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig><dir>C:/Windows/Fonts</dir><cachedir>'+str(TMP/'font-cache')+'</cachedir></fontconfig>')
ENV = dict(os.environ, FONTCONFIG_FILE=str(fontconfig))
evidence = []

def scad(path, part='assembly', extra=()):
    args = [EXE, '--backend', 'Manifold', '--hardwarnings', '-o', str(path), '-D', f'part="{part}"', *extra, str(SCAD)]
    result = subprocess.run(args, capture_output=True, text=True, env=ENV, timeout=180)
    if result.returncode or 'ERROR:' in result.stderr or 'WARNING:' in result.stderr:
        raise RuntimeError(f'OpenSCAD {part}: {result.stderr}')
    if not path.exists() or not path.stat().st_size:
        raise RuntimeError(f'No output: {path}')

meshes = {}
offsets = {'gray-left':[0,0,6], 'gray-right':[140,0,6], 'white-right':[140,0,6],
           'base-left':[0,0,0], 'base-right':[140,0,0], 'splice':[0,0,0], 'fit-coupon':[199,0,93]}
for part, offset in offsets.items():
    raw = TMP / f'{part}.stl'
    scad(raw, part, ['--export-format', 'binstl'])
    mesh = trimesh.load(raw, force='mesh')
    assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume > 0, part
    if part != 'white-right':
        assert len(mesh.split()) == 1, f'{part} contains disconnected structure'
    mesh.apply_translation(-np.array(offset))
    mesh.export(KIT / f'{part}.stl')
    meshes[part] = mesh
    line = f'{part}: watertight=True; bounds_mm=' + ' x '.join(f'{n:.3f}' for n in mesh.extents)
    evidence.append(line)
    print(line, flush=True)

body_bounds = np.array([meshes[name].bounds + offsets[name] for name in
                        ['gray-left','gray-right','white-right','base-left','base-right']])
envelope = body_bounds[:,1,:].max(axis=0) - body_bounds[:,0,:].min(axis=0)
assert np.allclose(envelope,[279.4,155,165],atol=.06), envelope
assert np.allclose(meshes['fit-coupon'].extents,[74,36.9,62],atol=.01)
assert all(m.extents[0] <= 165 and m.extents[1] <= 155.01 for m in meshes.values())
evidence.append('Envelope: nominal 279.4 x 155 x 165 mm; display bay depth=36.9 mm (2+9.5+25.4)')

# Standard 3MF material parts preserve the common origin of gray and white.
NS = 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
ET.register_namespace('', NS)
def tag(n): return f'{{{NS}}}{n}'
model = ET.Element(tag('model'), {'unit':'millimeter', 'xml:lang':'en-US'})
resources = ET.SubElement(model, tag('resources'))
mats = ET.SubElement(resources, tag('basematerials'), {'id':'1'})
for name, color in [('Gray','#686E75FF'),('White','#FAFAF5FF')]:
    ET.SubElement(mats, tag('base'), {'name':name, 'displaycolor':color})
for objid, name, material in [(2,'gray-right',0),(3,'white-right',1)]:
    obj = ET.SubElement(resources, tag('object'), {'id':str(objid),'type':'model','name':name,'pid':'1','pindex':str(material)})
    body = ET.SubElement(obj,tag('mesh'))
    verts = ET.SubElement(body,tag('vertices'))
    for v in meshes[name].vertices:
        ET.SubElement(verts,tag('vertex'),dict(zip(['x','y','z'],[f'{a:.6f}' for a in v])))
    faces = ET.SubElement(body,tag('triangles'))
    for face in meshes[name].faces:
        ET.SubElement(faces,tag('triangle'),dict(zip(['v1','v2','v3'],[str(a) for a in face])))
assembly = ET.SubElement(resources,tag('object'),{'id':'4','type':'model','name':'WOPR right shell - assign gray and white'})
components = ET.SubElement(assembly,tag('components'))
for n in [2,3]: ET.SubElement(components,tag('component'),{'objectid':str(n)})
ET.SubElement(ET.SubElement(model,tag('build')),tag('item'),{'objectid':'4'})
mf = KIT / 'right-shell-two-color.3mf'
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

views = {
    'hero': ('430,-450,310,139,70,80','assembly',True),
    'rear': ('-280,510,300,139,70,80','assembly',True),
    'empty': ('430,-450,310,139,70,80','assembly',False),
    'front': ('139.7,-550,82.5,139.7,77.5,82.5','assembly',True),
    'back': ('139.7,700,82.5,139.7,77.5,82.5','assembly',True),
    'left': ('-600,77.5,82.5,139.7,77.5,82.5','assembly',True),
    'right': ('750,77.5,82.5,139.7,77.5,82.5','assembly',True),
    'top': ('139.7,77.5,800,139.7,77.5,0','assembly',False),
    'bottom': ('139.7,77.5,-800,139.7,77.5,0','assembly',False),
    'section': ('-500,77.5,82.5,236,77.5,82.5','section',True),
    'coupon': ('330,-150,220,236,15,124','fit-coupon',False),
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
    text(36,24,'W.O.P.R. / DRAFT 01 / 2026-09-26 / dimensions in mm / not to print scale',8,GRAY)
    text(714,24,f'{page:02d} / 06',8,GRAY)
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
    c.setStrokeColor(GRAY); c.line(x,y,x,y+h)
    for a in [y,y+h]: c.line(x-4,a,x+5,a)
    c.saveState(); c.translate(x-6,y+h/2); c.rotate(90); c.setFont('Helvetica',9); c.drawCentredString(0,0,label); c.restoreState()
def end(): c.showPage()

start('Design review','A small W.O.P.R., built around real boards','Gray case. Flush white lettering. Eight side-light modules. One inset touchscreen.')
pic('hero',34,116,724,395)
lines(40,91,['279.4 x 155 x 165 mm  |  11.00 x 6.10 x 6.50 in  |  3 mm nominal shell',
             'OpenSCAD model render. Colored LEDs and display are hardware previews, not printed material.'],10,17)
end()
start('Mockups','The same design, around the back','Eight boards total: four on each long side. The small LED clusters are shown at their real size.')
pic('rear',40,251,410,254); pic('empty',455,279,295,209)
text(460,264,'CASE WITHOUT ELECTRONICS',9,ACCENT,'Helvetica-Bold')
lines(40,222,['The silhouette follows the low central case, rounded shoulders, raised spine and tall end tower.',
              'Both long sides carry white W.O.P.R. / War Operation Plan Response lettering.',
              'The main touchscreen is on one side, directly above its logo.',
              'Four separate clusters light up on each side; there are 480 LEDs across all eight boards.',
              'The underside opens for installation and support removal. The panel doors are decorative.'],11,23)
text(40,73,'User-confirmed layout: four boards per long side, eight total. Board spacing is a first-draft choice.',9,GRAY)
end()
start('Orthographic drawings','Overall envelope and panel placement','All views below come from the same SCAD geometry. Dimensions are nominal, not a film-prop measurement.')
fx,fy,fw,fh=pic('front',64,240,410,242)
text(64,495,'PRIMARY LONG SIDE',9,ACCENT,'Helvetica-Bold')
dim_h(fx,fy-20,fw,'279.4 / 11.00 in'); dim_v(fx-18,fy,fh,'165 / 6.50 in')
sx,sy,sw,sh=pic('right',526,240,220,242)
text(526,495,'TOWER END',9,ACCENT,'Helvetica-Bold'); dim_h(sx,sy-20,sw,'155 / 6.10 in')
lines(64,182,['Main light centers: X = 37, 79, 121 and 163; Z = 101.',
              'TFT center: X = 236; Z = 124. Lower case top: Z = 128.',
              'Spine top: Z = 137. Tower top: Z = 165.',
              'Case splits at X = 140 for a smaller printer.'],10,21)
lines(526,182,['Front display pocket:', '65.6 wide x 53.6 high', 'Seeed pocket, each:', '21.6 wide x 18.4 high'],10,21)
end()
start('Orthographic drawings','Top, rear and service access','Common axes: X along the 11-inch length, Y front to rear, Z up from the base.')
tx,ty,tw,th=pic('top',47,284,342,201)
text(47,500,'TOP',9,ACCENT,'Helvetica-Bold'); dim_h(tx,ty-18,tw,'279.4'); dim_v(tx-12,ty,th,'155')
pic('back',420,275,331,207); text(420,500,'OPPOSITE LONG SIDE',9,ACCENT,'Helvetica-Bold')
pic('bottom',49,70,330,170); text(420,239,'BOTTOM / TWO REMOVABLE HALVES',9,ACCENT,'Helvetica-Bold')
lines(420,218,['Eight M3 base screw clearances: diameter 3.3.',
               'Shell pilot holes: diameter 2.5; fit-test first.',
               'Bottom vent slots: 3 x 20.',
               'Rear cable opening: 12 x 7.',
               'Shell and base seams are glued using splice strips.',
               'No controller or power supply is specified yet.'],10,22)
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
lines(420,231,['Pocket: 65.6 x 53.6, around a nominal 65 x 53 board.',
               'Four mounting ears: diameter 2.7 clearance.',
               'V2 hole pitch: 59.690 x 47.498 (landscape).',
               'Front glass is nominally 2 mm below the case face.',
               'Fit-test glass-to-PCB stack and connector clearance.',
               'The 25.4 mm bay excludes the 9.5 mm hardware depth.'],9,20)
text(44,93,'Mount positions follow manufacturer CAD; assembly thickness and tolerances still need a physical check.',10,GRAY)
end()
start('Print kit and evidence','Gray + white, in the same print','First-draft geometry verified digitally. Physical fit and slicer toolpaths are not yet verified.')
pic('coupon',45,283,235,209)
text(47,269,'PRINT THE DISPLAY FIT COUPON FIRST',8,ACCENT,'Helvetica-Bold')
lines(310,488,['PRINT FILES',
              'right-shell-two-color.3mf: one object, gray + white parts.',
              'gray-left.stl / gray-right.stl: split structural case.',
              'white-right.stl: aligned lettering; import with gray-right.',
              'base-left.stl / base-right.stl: removable underside.',
              'splice.stl: print four. fit-coupon.stl: test the display mount.',
              'Nominal shell: 3 mm. White text: 0.8 mm deep, flush.',
              'Use internal supports; remove them through the open bottom.',
              'Start at 0.2 mm layers. Use a bed at least 180 x 180 mm.',
              'Assign the two filament colors explicitly in the slicer.'],10,20)
lines(44,238,['CHECKED: Seven STL exports are watertight. Structural parts are connected solids.',
              'CHECKED: 3MF contains two material parts. PDF has six pages with SCAD views.',
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
assert len(doc)==6
for i,p in enumerate(doc):
    assert len(p.get_text())>200
    p.get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).save(TMP/f'page-{i+1}.png')
evidence.append('PDF: 6 pages; text and raster renders verified by builder; visual review required')
(OUT/'verification.txt').write_text('\n'.join(evidence)+'\n')
with zipfile.ZipFile(OUT/'wopr-first-draft-kit.zip','w',zipfile.ZIP_DEFLATED) as z:
    for path in [SCAD,ROOT/'cad/README.md',ROOT/'cad/build.py',OUT/'verification.txt',*KIT.glob('*')]:
        z.write(path,path.relative_to(ROOT))
print(f'PDF: {PDF}; pages={len(doc)}',flush=True)
print('PASS: all geometry and document checks',flush=True)
