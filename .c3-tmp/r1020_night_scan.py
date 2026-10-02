# -*- coding: utf-8 -*-
"""R1020 night-bucket scan: DAILY v51 supply-face switch (structural). Festival faces
(resident six-axis + sprite) machine-proven ZERO clean rows in r1020_pool.txt ->
per R1019 pointer ("yu 11 tong 1288 rows" supply note) the day-context bucket switches
to NIGHT: same-day time-of-day match (production 21:1x = literal night; v50 ye-mu
same-round timing precedent raised to bucket level; National Day holiday day 2 NIGHT
scene). Rotation law continues inside the night face: post-v50 counts qiuxin 9 /
huaijiu 8 / xiaqi 8 / yanhuo 8 / zhixu 8 / xiaoyao 8 -> redemption target = yanhuo
(v44, gap 6) -> cascade huaijiu (v45,5) -> xiaqi (v46,4) -> zhixu (v47,3) ->
xiaoyao (v48,2). Night bucket = zero prior DAILY consumption expected (probe catches
cross-series REACT/city-spirit faces regardless). Same probe standard as r1019/r1020.
Output: .c3-tmp/r1020_night_pool.txt (UTF-8).
"""
import io, json, os

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
BASE = os.path.join(ROOT, 'data', 'storylines', 'cards')

pool = json.load(io.open(os.path.join(ROOT, '..', '..', 'life', 'BigLife', 'cognition', 'pools.json'), encoding='utf-8'))
spirit = io.open(os.path.join(ROOT, 'data', 'storylines', 'codex', 'city-spirit.md'), encoding='utf-8').read()

faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, 'cards.json')
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding='utf-8'))
        face = u'\n'.join(u'\n'.join(c.get('lines', [])) for c in cfg.get('cards', []))
        sq = cfg.get('meta', {}).get('source_quote', u'')
        faces[d] = face + u'\n' + sq

def shingles(text, lo=2, hi=5):
    s = set()
    n = len(text)
    for L in range(lo, hi + 1):
        for i in range(0, n - L + 1):
            s.add(text[i:i + L])
    return s

SEASONAL = [u'年味', u'过年', u'春联', u'春雨', u'除夕', u'拜年', u'红包', u'元宵', u'汤圆', u'年年有余']

def probe(text):
    hits = {}
    for sh in sorted(shingles(text), key=len, reverse=True):
        if len(sh) < 2:
            continue
        where = sorted(d for d, f in faces.items() if sh in f)
        if not where and sh not in spirit:
            continue
        spirit_hit = sh in spirit
        if where or spirit_hit:
            key = (sh, u','.join(where) if where else u'city-spirit')
            hits[sh] = key
    kept = []
    for sh in sorted(hits, key=len, reverse=True):
        if any(sh != k and sh in k for k in [x[0] for x in kept]):
            continue
        kept.append((sh, hits[sh][1]))
    return kept

out = io.StringIO()
def w(s):
    out.write(s)
    out.write(u'\n')

w(u'R1020 DAILY v51 night-bucket scan (supply-face switch: festival zero-clean exhaustion machine-proven in r1020_pool.txt)')
w(u'Day-context match: 2026-10-02 National Day holiday day 2 NIGHT + production 21:1x literal night (v50 ye-mu same-round timing raised to bucket level)')
w(u'Rotation inside night face: target yanhuo (v44 gap 6) -> huaijiu (5) -> xiaqi (4) -> zhixu (3) -> xiaoyao (2)')
w(u'=' * 70)

AXES = [
    (u'\u70df\u706b', u'yanhuo', u'[G]'),
    (u'\u6000\u65e7', u'huaijiu', u'[H]'),
    (u'\u4fa0\u6c14', u'xiaqi', u'[I]'),
    (u'\u79e9\u5e8f', u'zhixu', u'[J]'),
    (u'\u900d\u9065', u'xiaoyao', u'[K]'),
]

for ax, name, tag in AXES:
    nb = pool['axes'][ax][u'night']
    w(u'%s %s/night %d rows (zero prior DAILY night consumption expected)' % (tag, name, len(nb)))
    for i, line in enumerate(nb):
        seas = u' | SEASONAL(R972)' if any(s in line for s in SEASONAL) else u''
        w(u'FREE line%-2d %s%s' % (i, line, seas))
        if not seas:
            kept = probe(line)
            if not kept:
                w(u'    -> ZERO direct shingle hits (clean row)')
            else:
                for sh, where in kept:
                    w(u'    HIT [%s] -> %s' % (sh, where))
    w(u'=' * 70)

sprite = pool.get('sprite')
sn = sprite.get(u'night') if isinstance(sprite, dict) else None
w(u'[L] sprite/night %d rows' % len(sn))
for i, line in enumerate(sn):
    seas = u' | SEASONAL(R972)' if any(s in line for s in SEASONAL) else u''
    w(u'FREE line%-2d %s%s' % (i, line, seas))
    if not seas:
        kept = probe(line)
        if not kept:
            w(u'    -> ZERO direct shingle hits (clean row)')
        else:
            for sh, where in kept:
                w(u'    HIT [%s] -> %s' % (sh, where))

io.open(os.path.join(ROOT, '.c3-tmp', 'r1020_night_pool.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('night scan done')
