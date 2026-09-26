# -*- coding: utf-8 -*-
# R452: frame-sampling probe for bs-003-v15 (three laws: beat heads,
# loop-boundary crossings computed per beat/source, full-res text frames)
import json, io, os, subprocess

OUT = '.bs003-v15-tmp/probe-r452'
os.makedirs(OUT, exist_ok=True)
MP4 = 'output/renders/bs-003-v15-shipinhao-60s.mp4'
SRCLEN = {'looplog-vertical.mp4': 12.000, 'reviewsdoc-vertical.mp4': 10.000,
          'citywatch-vertical.mp4': 4.066}
cards = json.load(io.open('data/sources/bs003/cards-v15-matched.json',
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
    heads.append(round(t, 2))

# 2) loop crossings: any beat whose source repeats inside the beat
cross = {}
for i, c in enumerate(cards):
    src = (c.get('visual') or {}).get('source')
    if not src:
        continue
    slen = SRCLEN.get(os.path.basename(src))
    if slen is None:
        continue
    k = 1
    while c['start'] + slen * k < c['end'] - 0.05:
        x = c['start'] + slen * k
        for tag, dt in (('pre', -0.1), ('x', 0.0), ('post', 0.1)):
            grab(x + dt, 'b%02d-x%d-%s' % (i, k, tag))
        cross['b%02d#%d' % (i, k)] = round(x, 2)
        k += 1

# 3) full-res text frames (2)
grab(12.0, 'full-t12')
grab(50.0, 'full-t50')

# tiles via PIL (heads 12 -> 4x3; crossings -> 3xN)
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
if cross:
    names = ['b%02d-x%d-%s' % (int(k[1:3]), int(k.split('#')[1]), t)
             for k in cross for t in ('pre', 'x', 'post')]
    tile(names, 3, os.path.join(OUT, 'tile-cross.png'))

print('heads:', heads)
print('crossings:', cross)
print('done ->', OUT)
