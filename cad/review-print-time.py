"""Compare current four-wheel support strategies using the native Bambu slicer.

Run after build-reinforced.py and build-eight-wheel-projects.py, on WoprBuildPrivate.
Keeps structural settings and compares grid versus snug automatic supports.
"""
from pathlib import Path
import json, math, re, subprocess, zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / 'tmp/clearance'
OUT = ROOT / 'output/reinforced/bambu-projects'
PRESETS = ROOT / 'tmp/unified-bambu'
BAMBU = 'C:/Program Files/Bambu Studio/bambu-studio.exe'
TMP.mkdir(parents=True, exist_ok=True)

def slice_file(source, label, process=None):
    target = TMP / (label + '.3mf')
    command = [BAMBU, '--datadir', str(TMP/'cli-data')]
    if process:
        command += ['--load-settings', str(PRESETS/'machine.json')+';'+str(process),
                    '--load-filaments', str(PRESETS/'filament.json')]
    command += ['--arrange', '1' if process else '0', '--orient', '0',
                '--slice', '0', '--mstpp', '120', '--export-3mf', str(target), str(source)]
    with (TMP/(label+'.log')).open('w') as log:
        result = subprocess.run(command, cwd=TMP, stdout=log, stderr=log,
                                timeout=180, creationflags=subprocess.CREATE_NO_WINDOW)
    assert result.returncode == 0, (label, result.returncode)
    return target

def statistics(path):
    plates = []
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None
        info = ET.fromstring(archive.read('Metadata/slice_info.config'))
        support_length = 0
        for name in archive.namelist():
            if not name.endswith('.gcode'):
                continue
            feature = ''; relative = True; previous_e = 0
            for line in archive.read(name).decode().splitlines():
                if line.startswith('; FEATURE:'):
                    feature = line.split(':', 1)[1].strip()
                command = line.split(';')[0].strip()
                if command == 'M83': relative = True
                if command == 'M82': relative = False
                match = re.search(r'(?:^| )E(-?[0-9.]+)', command)
                if not match: continue
                value = float(match.group(1))
                if command.startswith('G92'):
                    previous_e = value; continue
                if not command.startswith(('G0 ', 'G1 ')): continue
                delta = value if relative else value-previous_e
                previous_e = value
                # E-only recovery moves do not deposit support on the object.
                if delta > 0 and 'support' in feature.lower() and re.search(r'(?:^| )[XY]', command):
                    support_length += delta
        for plate in info.findall('plate'):
            values = {m.get('key'): m.get('value') for m in plate.findall('metadata')}
            assert values['outside'] == 'false', (path, values)
            plates.append({'index': int(values['index']), 'seconds': int(values['prediction']),
                           'grams': float(values['weight']), 'support_used': values['support_used']=='true'})
    return {'file': path.name, 'plates': plates, 'seconds': sum(p['seconds'] for p in plates),
            'grams': round(sum(p['grams'] for p in plates), 2),
            'support_toolpath_grams': round(support_length*math.pi*(1.75/2)**2*1.27/1000, 2)}

baseline = []
for part in ['r-frame-zip', 'r-shell']:
    path = TMP / ('baseline-'+part+'.3mf')
    if path.exists(): baseline.append(statistics(path))

candidates = {}
process = json.loads((PRESETS/'process.json').read_text())
for style in ['grid', 'snug']:
    settings = {**process, 'support_type': 'normal(auto)', 'support_style': style}
    preset = TMP / ('review-'+style+'.json')
    preset.write_text(json.dumps(settings))
    candidates[style] = []
    for part in ['r-frame-zip', 'r-shell']:
        path = slice_file(ROOT/'output/reinforced/four'/(part+'.stl'), 'revised-'+style+'-'+part, preset)
        row = statistics(path); candidates[style].append(row)
        print(style, part, json.dumps(row), flush=True)

selected = min(candidates, key=lambda k: sum(p['seconds'] for p in candidates[k]))
report = {'printer': 'Bambu Lab H2D 0.4 nozzle', 'filament': 'Generic PETG',
          'bed': 'Textured PEI Plate', 'baseline_ref': 'a1b386f',
          'baseline_process': '0.20mm Standard, 35% gyroid, normal automatic support',
          'revised_process': '0.24mm Standard, 35% rectilinear, short bridges without support',
          'baseline_single_color_parts': baseline, 'revised_single_color_parts': candidates,
          'selected_support': selected,
          'rejected_support': 'Tree support failed H2D G-code validation with both '
                              'automatic and explicit nozzle configuration. Not used.',
          'limits': 'Estimates only. Support grams derived from XY extrusion toolpaths. '
                    'No physical print or strength test. Fastest of the two valid tested support strategies.'}
(OUT/'print-review.json').write_text(json.dumps(report, indent=2)+'\n')
print('PASS: Bambu print comparison; selected '+selected+' automatic support', flush=True)
