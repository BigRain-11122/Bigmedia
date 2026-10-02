# -*- coding: utf-8 -*-
"""R1015 pool pre-scan: xiaqi/festival FREE rows + card-face-level fleet dedup (R1010 law)."""
import json, io, os

OUT = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1015_pool.txt', 'w', encoding='utf-8')
def P(s):
    OUT.write(s + u'\n')

BASE = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines\cards'
pool = json.load(io.open(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json', encoding='utf-8'))
fest = pool['axes'][u'侠气'][u'festival']
used = {5: 'v3', 13: 'v8', 2: 'v13', 1: 'v20', 10: 'v26', 9: 'v34', 11: 'v40', 0: 'city-spirit-v1.2'}
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
P(u'---quote-face word probe for clean rows (wordface vs fleet faces+source_quote, R1010 law)---')
for i, l in clean:
    words = [w for w in [u'灯笼', u'灯', u'年味', u'喜庆', u'热闹', u'星星', u'船长', u'船上', u'江湖', u'义气',
                         u'走动', u'串门', u'节日氛围', u'节日气氛', u'欢聚', u'号子', u'飘香', u'心情', u'灯饰',
                         u'大伙儿', u'乐呵', u'一年到头', u'累不坏'] if w in l]
    flags = sorted(set(w for w in words if any((w in f or w in sq) for _, (f, sq) in faces.items())))
    P(u'idx=%d words=%s flags=%s | %s' % (i, u','.join(words) or u'-', u','.join(flags) or u'NONE', l))
OUT.close()
print('written r1015_pool.txt')
