# -*- coding: utf-8 -*-
"""R1023 DAILY v53 night-bucket scan (fresh, fleet now includes v52). Rotation:
post-v52 counts qiuxin 9 / yanhuo 9 / xiaqi 9 -> three-way tie at 8 (huaijiu / zhixu /
xiaoyao) -> redemption target = huaijiu (v45, 7-piece gap, longest; night face
machine-proven zero clean rows in R1022 r1022_pool.txt - re-verify fresh) -> cascade
zhixu (v47, 5-piece gap; R1022 backup note: zhixu/night line7 zero-hit = v53 first
redemption candidate) -> xiaoyao (v48, 4-piece gap) -> sprite/night line8 (R1022
second backup). Same probe standard as r1019/r1020/r1022. Output:
.c3-tmp/r1023_pool.txt (UTF-8).
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
        spirit_hit = sh in spirit
        if not where and not spirit_hit:
            continue
        hits[sh] = (u','.join(where) if where else u'city-spirit')
    kept = []
    for sh in sorted(hits, key=len, reverse=True):
        if any(sh != k and sh in k for k in [x[0] for x in kept]):
            continue
        kept.append((sh, hits[sh]))
    return kept

out = io.StringIO()
def w(s):
    out.write(s)
    out.write(u'\n')

w(u'R1023 DAILY v53 night-face pre-scan (fresh; fleet includes DAILY-v52 xiaqi/night/4 consumed)')
w(u'Day-context: 2026-10-02 National Day holiday day 2 NIGHT, production ~22:1x literal night (night bucket 3rd piece, v51/v52 precedent chain)')
w(u'Rotation: post-v52 qiuxin 9/yanhuo 9/xiaqi 9 -> three-way tie at 8 -> target huaijiu (v45 gap 7) -> cascade zhixu (v47 gap 5) -> xiaoyao (v48 gap 4)')
w(u'=' * 70)

AXES = [
    (u'\u6000\u65e7', u'huaijiu', u'[H]'),
    (u'\u79e9\u5e8f', u'zhixu', u'[Z]'),
    (u'\u900d\u9065', u'xiaoyao', u'[Y]'),
]
for ax, name, tag in AXES:
    nb = pool['axes'][ax][u'night']
    w(u'%s %s/night %d rows' % (tag, name, len(nb)))
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

# v52 consumed row USED re-check (R978 lesson)
xn = pool['axes'][u'\u4fa0\u6c14'][u'night']
v52_face = faces.get(u'MC-20261002-DAILY-v52', u'')
w(u'[check] xiaqi/night/4 (v52) USED re-verification: line in v52 card face -> %s' % (xn[4] in v52_face))
w(u'[check] zhixu/night line7 candidate: %s' % pool['axes'][u'\u79e9\u5e8f'][u'night'][7])
w(u'[check] sprite/night line8 backup: %s' % pool['sprite'][u'night'][8])
w(u'[rotation note] cascade order post-huaijiu-block: zhixu (v47 gap 5) > xiaoyao (v48 gap 4) > sprite/night line8; night bucket prior consumption = v51 yanhuo/13 + v52 xiaqi/4 only')

io.open(os.path.join(ROOT, '.c3-tmp', 'r1023_pool.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('r1023 night pre-scan done')
