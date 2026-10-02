# -*- coding: utf-8 -*-
"""R1022 DAILY v52 night-bucket scan (fresh, fleet now includes v51). Rotation:
post-v51 counts qiuxin 9 / yanhuo 9 / huaijiu 8 / xiaqi 8 / zhixu 8 / xiaoyao 8 ->
four-way tie at 8 -> redemption target = huaijiu (v45, 6-piece gap, longest) ->
cascade xiaqi (v46, 5) -> zhixu (v47, 4) -> xiaoyao (v48, 3). This scan covers the
huaijiu + xiaqi night faces first (rotation order); expected outcome per
r1020_night_pool.txt evidence: huaijiu/night zero clean rows (all 18 carry
content-layer collisions), xiaqi/night line4 = sole clean row (content shingles
chuanlaoda/heshang/yexing/zuishichangkuai ALL ZERO; only construct-layer function
hits). v51 consumed yanhuo/night/13 (re-checked USED). Same probe standard as
r1019/r1020. Output: .c3-tmp/r1022_pool.txt (UTF-8).
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

w(u'R1022 DAILY v52 night-face pre-scan (fresh; fleet includes DAILY-v51 yanhuo/night/13 consumed)')
w(u'Day-context: 2026-10-02 National Day holiday day 2 NIGHT, production ~22:0x literal night (night bucket 2nd piece, v51 first-piece precedent)')
w(u'Rotation: post-v51 qiuxin 9/yanhuo 9, four-way tie at 8 -> target huaijiu (v45 gap 6) -> cascade xiaqi (v46 gap 5) -> zhixu (4) -> xiaoyao (3)')
w(u'=' * 70)

AXES = [
    (u'\u6000\u65e7', u'huaijiu', u'[H]'),
    (u'\u4fa0\u6c14', u'xiaqi', u'[I]'),
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

# yanhuo/night/13 consumed-by-v51 re-check (R978 lesson: USED-row re-verification)
yn = pool['axes'][u'\u70df\u706b'][u'night']
v51_face = faces.get(u'MC-20261002-DAILY-v51', u'')
w(u'[check] yanhuo/night/13 (v51) USED re-verification: line in v51 card face -> %s' % (yn[13] in v51_face))
w(u'[check] xiaqi/night/4 candidate: %s' % pool['axes'][u'\u4fa0\u6c14'][u'night'][4])
w(u'[rotation note] zhixu/night line7 (zero-hit clean row) + sprite/night line8 (zero-hit clean row) = next-face backup candidates for v53 zhixu redemption (gap 4 after this piece)')

io.open(os.path.join(ROOT, '.c3-tmp', 'r1022_pool.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('r1022 night pre-scan done')
