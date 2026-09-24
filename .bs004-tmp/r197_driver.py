# R197 driver for #26 re-render batch (3 pieces):
# 1) S2 three-gate re-run (ai_feel + layer1.8 + spec) - readings must match R189
# 2) loop-crossing frame probe (new sampling face per footage-matching-spec v1.1):
#    for every citywatch beat, sample at beat-relative (src_len - src_off) +/- 0.1s
#    (src_len=4.066s post-R196 recut; all src_off=0 in the v14 plans)
# Results -> UTF-8 .bs004-tmp/s2-results-r197.md (PS5.1 console GBK bypass)
import io
import json
import os
import subprocess
import sys

os.chdir(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream')
PIECES = [
    ('bs-001-v14b-shipinhao-60s.mp4', r'data\sources\bs001\voiceover-v11-trim.beats.txt', r'output\renders\.v11-trim\subs.srt', r'data\sources\bs001\cards-v12-matched.json'),
    ('bs-002-v2b-shipinhao-60s.mp4', r'data\sources\bs002\voiceover-v5.beats.txt', r'.bs002-tmp\subs.srt', r'data\sources\bs002\cards-v1-matched.json'),
    ('bs-003-v2b-shipinhao-60s.mp4', r'data\sources\bs003\voiceover-v5.beats.txt', r'.bs003-tmp\subs.srt', r'data\sources\bs003\cards-v1-matched.json'),
]
SRC_LEN_S = 4.066
PROBE = r'.bs004-tmp\probe-r197'
os.makedirs(PROBE, exist_ok=True)

out = io.open(r'.bs004-tmp\s2-results-r197.md', 'w', encoding='utf-8')
for mp4, beats, srt, cards_path in PIECES:
    video = r'output\renders' + '\\' + mp4
    plan = video + '.plan.json'
    checks = [
        ('ai_feel', [sys.executable, 'src\\ai_feel_check.py', '--beats', beats, '--srt', srt]),
        ('edit_craft_l18', [sys.executable, 'src\\edit_craft_check.py', '--plan', plan, '--srt', srt, '--profile', 'shipinhao']),
        ('platform_spec', [sys.executable, 'src\\platform_spec_check.py', '--video', video, '--platform', '微信视频号']),
    ]
    for name, cmd in checks:
        r = subprocess.run(cmd, capture_output=True)
        out.write('## %s | %s | rc=%d\n' % (mp4, name, r.returncode))
        out.write(r.stdout.decode('utf-8', 'replace'))
        if r.stderr.strip():
            out.write('[STDERR] ' + r.stderr.decode('utf-8', 'replace')[-400:] + '\n')
        out.write('\n')
    # duration evidence
    d = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                        '-of', 'csv=p=0', video], capture_output=True)
    out.write('## %s | ffprobe duration: %s\n\n' % (mp4, d.stdout.decode('utf-8', 'replace').strip()))
out.close()
print('s2 leg done')

# --- loop-crossing probe ---
from PIL import Image, ImageDraw

probe_log = io.open(r'.bs004-tmp\probe-r197-crossings.md', 'w', encoding='utf-8')
for mp4, beats, srt, cards_path in PIECES:
    video = r'output\renders' + '\\' + mp4
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
    cells = []
    for label, t in shots:
        png = os.path.join(PROBE, '%s_%s.png' % (mp4.split('-60s')[0], label))
        r = subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', '%.3f' % t,
                            '-i', video, '-frames:v', '1', '-vf', 'scale=360:640', png],
                           capture_output=True)
        if r.returncode == 0 and os.path.exists(png):
            img = Image.open(png).convert('RGB')
            d = ImageDraw.Draw(img)
            d.rectangle([0, 0, 359, 30], fill=(0, 0, 0))
            d.text((8, 8), label + ' @%.2fs' % t, fill=(255, 255, 0))
            cells.append(img)
            probe_log.write('%s %s @%.3fs\n' % (mp4, label, t))
    if cells:
        cols = 3  # pre/x/post triplets per beat
        rows = (len(cells) + cols - 1) // cols
        tile = Image.new('RGB', (cols * 360, rows * 640), (20, 20, 20))
        for idx, img in enumerate(cells):
            tile.paste(img, ((idx % cols) * 360, (idx // cols) * 640))
        tile.save(os.path.join(PROBE, mp4.split('-60s')[0] + '-crossing-tile.png'))
    probe_log.write('%s -> %d crossing frames\n' % (mp4, len(cells)))
probe_log.close()
print('probe leg done')
