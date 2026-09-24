# R202 driver for F-006 douyin piece (BS-001 v14b-series, D-BS-06 order 3):
# 1) S2 three-gate enforcement (ai_feel + layer1.8 douyin + spec douyin window)
# 2) loop-crossing frame probe (footage-matching-spec v1.1: citywatch beats,
#    beat-relative src_len=4.066s +/- 0.1s, pre/x/post)
# 3) beat-head frames (semantic + AIGC readability + H1/H2 backing check)
# Results -> UTF-8 .bs001-dy-tmp/s2-results-r202.md (PS5.1 GBK console bypass)
# ASCII source (encoding law; platform name via \u escape, r199 pattern).
import io
import json
import os
import subprocess
import sys

os.chdir(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream')

video = r'output\renders\bs-001-v14b-douyin-9x16.mp4'
plan = video + '.plan.json'
beats = r'data\sources\bs001\voiceover-v11-trim.beats.txt'
srt = r'output\renders\.v11-trim\subs.srt'
cards_path = r'data\sources\bs001\cards-v12-matched.json'
SRC_LEN_S = 4.066
PROBE = r'.bs001-dy-tmp\probe-r202'
os.makedirs(PROBE, exist_ok=True)

out = io.open(r'.bs001-dy-tmp\s2-results-r202.md', 'w', encoding='utf-8')
checks = [
    ('ai_feel', [sys.executable, 'src\\ai_feel_check.py', '--beats', beats, '--srt', srt]),
    ('edit_craft_l18', [sys.executable, 'src\\edit_craft_check.py', '--plan', plan, '--srt', srt, '--profile', 'douyin']),
    ('platform_spec', [sys.executable, 'src\\platform_spec_check.py', '--video', video, '--platform', '\u6296\u97f3']),
]
for name, cmd in checks:
    r = subprocess.run(cmd, capture_output=True)
    out.write('## BS-001 v14b-douyin | %s | rc=%d\n' % (name, r.returncode))
    out.write(r.stdout.decode('utf-8', 'replace'))
    if r.stderr.strip():
        out.write('[STDERR] ' + r.stderr.decode('utf-8', 'replace')[-400:] + '\n')
    out.write('\n')
d = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                    '-show_entries', 'stream=width,height',
                    '-show_entries', 'format=duration', '-of', 'csv=p=0',
                    video], capture_output=True)
out.write('## BS-001 v14b-douyin | ffprobe: %s\n' % d.stdout.decode('utf-8', 'replace').strip().replace('\n', ' | '))
out.close()
print('s2 leg done')

# --- loop-crossing probe + beat heads ---
from PIL import Image, ImageDraw

cards = json.load(io.open(cards_path, encoding='utf-8'))['cards']
shots = []
for i, c in enumerate(cards):
    vis = c.get('visual') or {}
    src = vis.get('source') or ''
    if 'citywatch' in src:
        s = float(c['start'])
        x = s + SRC_LEN_S
        shots.append(('b%d-pre' % i, x - 0.1))
        shots.append(('b%d-x' % i, x))
        shots.append(('b%d-post' % i, x + 0.1))
# beat heads: hook + each visual-source beat (semantic + AIGC readability)
for i, c in enumerate(cards):
    shots.append(('head-b%d' % i, float(c['start']) + 0.15))

cells = []
log = io.open(r'.bs001-dy-tmp\probe-r202.md', 'w', encoding='utf-8')
for label, t in shots:
    png = os.path.join(PROBE, '%s.png' % label.replace('-', '_'))
    r = subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', '%.3f' % t,
                        '-i', video, '-frames:v', '1', '-vf', 'scale=360:640', png],
                       capture_output=True)
    if r.returncode == 0 and os.path.exists(png):
        img = Image.open(png).convert('RGB')
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, 359, 30], fill=(0, 0, 0))
        d.text((8, 8), label + ' @%.2fs' % t, fill=(255, 255, 0))
        cells.append(img)
        log.write('%s @%.3fs\n' % (label, t))
cols = 4
rows = (len(cells) + cols - 1) // cols
tile = Image.new('RGB', (cols * 360, rows * 640), (20, 20, 20))
for idx, img in enumerate(cells):
    tile.paste(img, ((idx % cols) * 360, (idx // cols) * 640))
tile.save(os.path.join(PROBE, 'tile-r202.png'))
log.write('total probe frames: %d\n' % len(cells))
log.close()
print('probe leg done: %d frames' % len(cells))
