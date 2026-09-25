# R316 driver for C1 leg-3/4 pilot: bs-001 douyin v15 speed-ramp re-render.
# 1) S2 three-gate enforcement (ai_feel + layer1.8 douyin + spec douyin window)
# 2) ramp window continuity probe: frames around every internal micro-block
#    boundary of each ramped punch beat (pre/x/post at +/-1 frame)
# 3) per-segment ramp algebra report (sum(out_frames) vs span frames)
# Results -> UTF-8 .bs001-dy-tmp/s2-results-r316.md (PS5.1 GBK console bypass)
# ASCII source (encoding law; platform name via \u escape, r202 pattern).
import io
import json
import os
import subprocess
import sys

os.chdir(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream')

video = r'output\renders\bs-001-v15-douyin-9x16.mp4'
plan = video + '.plan.json'
beats = r'data\sources\bs001\voiceover-v11-trim.beats.txt'
srt = r'output\renders\.v11-trim\subs.srt'
PROBE = r'.bs001-dy-tmp\probe-r316'
os.makedirs(PROBE, exist_ok=True)

out = io.open(r'.bs001-dy-tmp\s2-results-r316.md', 'w', encoding='utf-8')
checks = [
    ('ai_feel', [sys.executable, 'src\\ai_feel_check.py', '--beats', beats, '--srt', srt]),
    ('edit_craft_l18', [sys.executable, 'src\\edit_craft_check.py', '--plan', plan, '--srt', srt, '--profile', 'douyin']),
    ('platform_spec', [sys.executable, 'src\\platform_spec_check.py', '--video', video, '--platform', '\u6296\u97f3']),
]
for name, cmd in checks:
    r = subprocess.run(cmd, capture_output=True)
    out.write('## BS-001 v15-douyin | %s | rc=%d\n' % (name, r.returncode))
    out.write(r.stdout.decode('utf-8', 'replace'))
    if r.stderr.strip():
        out.write('[STDERR] ' + r.stderr.decode('utf-8', 'replace')[-400:] + '\n')
    out.write('\n')
d = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                    '-show_entries', 'stream=width,height,nb_frames',
                    '-show_entries', 'format=duration', '-of', 'csv=p=0',
                    video], capture_output=True)
out.write('## BS-001 v15-douyin | ffprobe: %s\n' % d.stdout.decode('utf-8', 'replace').strip().replace('\n', ' | '))

# --- ramp algebra report ---
pj = json.load(io.open(plan, encoding='utf-8'))
out.write('\n## ramp algebra report\n')
out.write('ramp_beats: %s\n' % pj.get('ramp_beats'))
for s in pj['segments']:
    blocks = s.get('ramp')
    if not blocks:
        continue
    fps = 30.0
    span_frames = int(round(s['dur_s'] * fps)) + 1  # plain-path zoompan safety frame
    out.write('seg %d dur %.3fs span_frames+1=%d blocks=%d sum_out=%d speeds=%s\n' % (
        s['idx'], s['dur_s'], span_frames, len(blocks),
        sum(b['out_frames'] for b in blocks),
        ','.join('%.4f' % b['speed'] for b in blocks)))

# --- ramp window continuity probe (pre/x/post around internal boundaries) ---
from PIL import Image, ImageDraw

bounds = {b['k']: b['time_s'] for b in pj['boundaries']}
shots = []
for s in pj['segments']:
    blocks = s.get('ramp')
    if not blocks:
        continue
    seg_start = 0.0 if s['idx'] == 0 else bounds.get(s['idx'], 0.0)
    cum = 0
    for b in blocks[:-1]:
        cum += b['out_frames']
        t = seg_start + cum / 30.0
        tag = 'b%d-o%d' % (s['idx'], cum)
        shots.append((tag + '-pre', t - 1 / 30.0))
        shots.append((tag + '-x', t))
        shots.append((tag + '-post', t + 1 / 30.0))

cells = []
log = io.open(r'.bs001-dy-tmp\probe-r316.md', 'w', encoding='utf-8')
for label, t in shots:
    png = os.path.join(PROBE, '%s.png' % label.replace('-', '_'))
    r = subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', '%.3f' % t,
                        '-i', video, '-frames:v', '1', '-vf', 'scale=360:640', png],
                       capture_output=True)
    if r.returncode == 0 and os.path.exists(png):
        img = Image.open(png).convert('RGB')
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, 359, 30], fill=(0, 0, 0))
        d.text((8, 8), label + ' @%.3fs' % t, fill=(255, 255, 0))
        cells.append(img)
        log.write('%s @%.3fs\n' % (label, t))
    else:
        log.write('%s @%.3fs EXTRACT-FAIL\n' % (label, t))
cols = 6
rows = (len(cells) + cols - 1) // cols
tile = Image.new('RGB', (cols * 360, rows * 640), (20, 20, 20))
for idx, img in enumerate(cells):
    tile.paste(img, ((idx % cols) * 360, (idx // cols) * 640))
tile.save(os.path.join(PROBE, 'tile-r316.png'))
log.write('total probe frames: %d\n' % len(cells))
log.close()
out.write('\n## ramp continuity probe: %d frames -> %s\\tile-r316.png\n' % (len(cells), PROBE))
out.close()
print('driver done: %d probe frames' % len(cells))
