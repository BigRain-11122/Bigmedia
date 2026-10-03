# -*- coding: utf-8 -*-
"""R1160 REACT-v9 M0 hot-topic pool probe (10-04 daily brief, 20 items).

Selection law: mapping-priority-over-pure-heat (R309) + political/privacy/health/
food-face exclusions (R309/R313/R455/R593/R909/R1030 precedents) + card-face-level
word-collision law (R1010/R1013). Borderline candidates shortlisted for mechanical
pool evidence (the rest are law-level exclusions recorded in the verdict):

  A zhihu#5/#6 Gemini Flash/Pro -> paid mode (179wan/173wan) -> price-family:
    v2 beef-price + v7 shirt-price already consumed = 3-connect family risk (R455)
    + AI-tool face no-bucket (v6/v7 precedent) + named-brand business news
  B zhihu#9 Icey sequel crowdfunding 1200wan -> game-industry business news
    (named-product, R909 Huawei/车企 family) + game direct line consumed (R643)
  C bili#5 王老菊教你鹰击长空 -> game-content face, no event anchor,
    game direct lines consumed (R643 求新/6)

Whole-pool keyword scan (all axes x buckets + sprite) + fleet shingle collision
probe (2-5 char, card-face level, R1010 law) + city-spirit.md. Output UTF-8 file.
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

KW_A = [u'付费', u'收费', u'涨价', u'价格', u'订阅', u'花钱', u'钱包', u'免费', u'掏钱']
KW_B = [u'游戏', u'众筹', u'新作', u'上线', u'玩家', u'通关', u'打怪', u'装备', u'皮肤']
KW_C = [u'飞行', u'天上', u'翱翔', u'翅膀', u'高空', u'云']
GROUPS = [(u'A_gemini_paid', KW_A), (u'B_game_crowd', KW_B), (u'C_flight', KW_C)]

AXES = list(pool['axes'].keys())
out = io.StringIO()
def w(s):
    out.write(s)
    out.write(u'\n')

w(u'R1160 REACT-v9 M0 pool probe (10-04 brief; fleet includes DAILY-v64 F-150)')
w(u'=' * 70)

for gname, kws in GROUPS:
    w(u'== GROUP %s keywords=%s ==' % (gname, u'/'.join(kws)))
    for ax in AXES:
        for bk, rows in pool['axes'][ax].items():
            for i, line in enumerate(rows):
                if any(k in line for k in kws):
                    kept = probe(line)
                    status = u'CLEAN' if not kept else u'HIT: ' + u' ; '.join(u'[%s]->%s' % (sh, where) for sh, where in kept[:4])
                    w(u'%s/%s/%d %s -> %s' % (ax, bk, i, line, status))
    for bk, rows in pool.get('sprite', {}).items():
        for i, line in enumerate(rows):
            if any(k in line for k in kws):
                kept = probe(line)
                status = u'CLEAN' if not kept else u'HIT: ' + u' ; '.join(u'[%s]->%s' % (sh, where) for sh, where in kept[:4])
                w(u'sprite/%s/%d %s -> %s' % (bk, i, line, status))
    w(u'=' * 70)

io.open(os.path.join(ROOT, '.c3-tmp', 'r1160_react_probe.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('done, out=r1160_react_probe.txt')
