# -*- coding: utf-8 -*-
"""R1014 pool pre-scan: huaijiu/festival FREE rows + card-face-level fleet dedup (R1010 law)."""
import json, io, os, sys

OUT = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1014_pool.txt', 'w', encoding='utf-8')
def P(s):
    OUT.write(s + u'\n')

BASE = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines\cards'
pool = json.load(io.open(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json', encoding='utf-8'))
fest = pool['axes'][u'怀旧'][u'festival']
used = {0: 'v2', 3: 'v10', 1: 'v16', 12: 'v22', 17: 'v25', 4: 'v33', 5: 'v39'}
for i, l in enumerate(fest):
    mark = 'USED ' + used[i] if i in used else 'FREE'
    P(u'%d %s %s' % (i, mark, l))

P(u'---card-face-level fleet dedup (lines+source_quote scan, R1010 law)---')
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, 'cards.json')
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding='utf-8'))
        face = u'\n'.join(u'\n'.join(c.get('lines', [])) for c in cfg.get('cards', []))
        sq = cfg.get('meta', {}).get('source_quote', u'')
        faces[d] = (face, sq)

free_rows = [(i, l) for i, l in enumerate(fest) if i not in used]
clean = []
for i, l in free_rows:
    hits = [d for d, (f, sq) in faces.items() if l in f or l in sq]
    P((u'FACEHIT %s' % hits) if hits else u'CLEAN  idx=%d %s' % (i, l))
    if not hits:
        clean.append((i, l))
P(u'---FREE clean count: %d' % len(clean))
P(u'---quote-face word probe for clean rows (wordface vs fleet source_quote faces)---')
for i, l in clean:
    words = [w for w in [u'灯笼', u'灯串', u'热闹', u'喜庆', u'年味', u'过年', u'春联', u'春雨', u'伞', u'手艺', u'心里', u'暖和', u'日子', u'踏实', u'回到从前', u'档案', u'灯火', u'灯'] if w in l]
    flags = sorted(set(w for w in words if any(w in sq for _, (f, sq) in faces.items())))
    P(u'idx=%d words=%s flags=%s | %s' % (i, u','.join(words) or u'-', u','.join(flags) or u'NONE', l))
OUT.close()
print('written r1014_pool.txt')
