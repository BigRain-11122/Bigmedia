# -*- coding: utf-8 -*-
# R450: frame-sampling probe for bs-002-v15 (three laws: beat heads,
# loop-boundary crossings at citywatch beats, full-res text frames)
import json, io, os, subprocess

OUT = '.bs002-v15-tmp/probe-r450'
os.makedirs(OUT, exist_ok=True)
MP4 = 'output/renders/bs-002-v15-shipinhao-60s.mp4'
cards = json.load(io.open('data/sources/bs002/cards-v15-matched.json',
                          encoding='utf-8'))['cards']

def grab(t, name):
    p = os.path.join(OUT, name + '.png')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(t),
                    '-i', MP4, '-frames:v', '1', p], check=True)
    return p

# 1) beat heads (12)
heads = []
for i, c in enumerate(cards):
    t = c['start'] + 0.15
    grab(t, 'b%02d-head' % i)
    heads.append(t)

# 2) loop crossings: citywatch beats b0/b8/b10, source len 4.066s (R197)
cross = {}
for i in (0, 8, 10):
    x = cards[i]['start'] + 4.066
    for tag, dt in (('pre', -0.1), ('x', 0.0), ('post', 0.1)):
        grab(x + dt, 'b%02d-x-%s' % (i, tag))
    cross[i] = round(x, 2)

# 3) full-res text frames (2)
grab(12.0, 'full-t12')
grab(50.0, 'full-t50')

# tiles via PIL (heads 12 -> 4x3; crossings 9 -> 3x3)
from PIL import Image
def tile(names, cols, path, w=270):
    imgs = [Image.open(os.path.join(OUT, n + '.png')) for n in names]
    h = int(w * imgs[0].height / imgs[0].width)
    rows = (len(imgs) + cols - 1) // cols
    T = Image.new('RGB', (w * cols, h * rows), 'black')
    for k, im in enumerate(imgs):
        T.paste(im.resize((w, h)), ((k % cols) * w, (k // cols) * h))
    T.save(path, quality=88)
    return path

tile(['b%02d-head' % i for i in range(12)], 4,
     os.path.join(OUT, 'tile-heads.png'))
tile(['b%02d-x-%s' % (i, t) for i in (0, 8, 10) for t in ('pre', 'x', 'post')], 3,
     os.path.join(OUT, 'tile-cross.png'))

print('heads:', [round(t, 2) for t in heads])
print('crossings:', cross)
print('done ->', OUT)
