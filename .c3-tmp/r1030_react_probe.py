# -*- coding: utf-8 -*-
"""R1030 REACT-v9 M0 hot-topic pool probe (10-03 daily brief, 20 items).

Selection law: mapping-priority-over-pure-heat (R309) + political/privacy/health/
food-face exclusions (R309/R313/R455/R593/R909 precedent) + card-face-level
word-collision law (R1010/R1013). Candidates shortlisted from 10-03 brief:

  A zhihu#2 AI short-drama boom China-vs-abroad (365wan) -> MEDIA-city on-brand
  B zhihu#5 why so little cola counterfeiting (166wan) -> fake/goods/trust face
  C zhihu#6 anti-unseal-tape vs malicious returns (116wan) -> theme-family repeat
    risk with REACT-v6 (refund abuse) per R455 law - probe anyway
  D zhihu#7 LoL hero passive double-price-double-stat (111wan) -> GAME-city face

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

KW_A = [u'\u5267', u'\u5c4f\u5e55', u'\u89c6\u9891', u'\u76f4\u64ad', u'\u5185\u5bb9', u'\u65b0\u82b1\u6837']
KW_B = [u'\u5047', u'\u771f\u8d27', u'\u724c\u5b50', u'\u653e\u5fc3', u'\u63ba', u'\u5192\u724c', u'\u6b63\u5b97']
KW_C = [u'\u9000\u8d27', u'\u9000\u6b3e', u'\u4fe1\u4efb', u'\u7f51\u8d2d', u'\u5feb\u9012', u'\u53d1\u8d27']
KW_D = [u'\u6e38\u620f', u'\u76ae\u80a4', u'\u5347\u7ea7', u'\u88c5\u5907', u'\u6253\u602a', u'\u901a\u5173']
GROUPS = [(u'A_ai_drama', KW_A), (u'B_fake_goods', KW_B), (u'C_returns_trust', KW_C), (u'D_game', KW_D)]

AXES = list(pool['axes'].keys())
out = io.StringIO()
def w(s):
    out.write(s)
    out.write(u'\n')

w(u'R1030 REACT-v9 M0 pool probe (10-03 brief; fleet includes DAILY-v59 F-144)')
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

io.open(os.path.join(ROOT, '.c3-tmp', 'r1030_react_probe.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('done, out=r1030_react_probe.txt')
