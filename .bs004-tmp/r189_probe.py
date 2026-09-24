# R189 mid/end-frame probe (new gate face per #23-4):
# for every citywatch beat of the four v14-batch renders, extract
# start/mid/end frames; plus one hook frame per piece for
# AIGC-notice + H1/H2 dark-box readability. Tiles per piece.
import io
import json
import os
import subprocess

os.chdir(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream')
PIECES = [
    ('bs-001-v14-shipinhao-60s.mp4', r'data\sources\bs001\cards-v12-matched.json'),
    ('bs-002-v2-shipinhao-60s.mp4', r'data\sources\bs002\cards-v1-matched.json'),
    ('bs-003-v2-shipinhao-60s.mp4', r'data\sources\bs003\cards-v1-matched.json'),
    ('bs-004-v2-shipinhao-60s.mp4', r'data\sources\bs004\cards-v1-matched.json'),
]
PROBE = r'.bs004-tmp\probe-r189'
os.makedirs(PROBE, exist_ok=True)
from PIL import Image, ImageDraw

for mp4, cards_path in PIECES:
    video = r'output\renders' + '\\' + mp4
    cards = json.load(io.open(cards_path, encoding='utf-8'))['cards']
    shots = []  # (label, t)
    for i, c in enumerate(cards):
        vis = c.get('visual') or {}
        src = vis.get('source') or ''
        if 'citywatch' in src:
            s, e = float(c['start']), float(c['end'])
            shots.append(('b%d-start' % i, s + 0.15))
            shots.append(('b%d-mid' % i, (s + e) / 2.0))
            shots.append(('b%d-end' % i, max(s + 0.15, e - 0.15)))
    shots.append(('hook-aigc', 0.80))
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
    if cells:
        cols = 4
        rows = (len(cells) + cols - 1) // cols
        tile = Image.new('RGB', (cols * 360, rows * 640), (20, 20, 20))
        for idx, img in enumerate(cells):
            tile.paste(img, ((idx % cols) * 360, (idx // cols) * 640))
        outp = os.path.join(PROBE, mp4.split('-60s')[0] + '-tile.png')
        tile.save(outp)
        print(mp4, '->', os.path.basename(outp), 'cells=%d' % len(cells))
print('probe done')
