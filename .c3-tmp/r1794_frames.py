# -*- coding: utf-8 -*-
"""MD-0001 frame-sampling verification (R1794): shot heads + mid/tail + boundaries."""
import subprocess, sys, io
from pathlib import Path
from PIL import Image, ImageDraw

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
REPO = Path('.').resolve()
OUT = REPO / 'output/renders/md-0001-v1-bilibili-16x9.mp4'
TMP = REPO / '.c3-tmp/asm-r1794'
TMP.mkdir(parents=True, exist_ok=True)

heads = [0.3, 6.3, 11.3, 15.3, 22.3, 28.3, 36.3, 42.3, 47.3, 54.3, 59.3, 65.3, 69.3]
mids = [3.0, 32.0, 62.0]
tails = [21.5, 53.5, 68.5, 75.3]
bounds = [5.95, 6.05, 27.90, 28.10, 64.90, 65.10, 68.90, 69.10]


def grab(t, name):
    p = TMP / name
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                    '-ss', '%.2f' % t, '-i', str(OUT),
                    '-frames:v', '1', str(p)], check=True)
    return p


def tile(paths, cols, out_name, cell_w=608):
    rows = (len(paths) + cols - 1) // cols
    im0 = Image.open(paths[0])
    cell_h = int(cell_w * im0.height / im0.width)
    canvas = Image.new('RGB', (cols * cell_w, rows * (cell_h + 18)), (20, 20, 20))
    d = ImageDraw.Draw(canvas)
    for i, p in enumerate(paths):
        im = Image.open(p).resize((cell_w, cell_h))
        x = (i % cols) * cell_w
        y = (i // cols) * (cell_h + 18)
        canvas.paste(im, (x, y + 18))
        d.text((x + 4, y + 3), '#%d' % i, fill=(255, 255, 0))
    out = TMP / out_name
    canvas.save(out, quality=88)
    print('TILE', out, canvas.size)


hp = [grab(t, 'head%02d.png' % i) for i, t in enumerate(heads)]
tile(hp, 4, 'verify-heads-r1794.png')
ep = [grab(t, 'ev%02d.png' % i) for i, t in enumerate(mids + tails + bounds)]
tile(ep, 4, 'verify-mid-tail-bound-r1794.png')
print('OK')
