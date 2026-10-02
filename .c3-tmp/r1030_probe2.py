# -*- coding: utf-8 -*-
"""R1030 REACT-v9 probe round 2: second-tier candidate faces + global clean-row census.

Round-1 result: A(AI-drama)/B(cola-fake)/C(returns)/D(LoL-game) all blocked at
card-face level or zero pool lines. Second-tier candidates from 10-03 brief:

  E zhihu#9 Tsinghua-PKU gold-content vs gaokao involution (106wan) ->
    education face: study/exam/skill/lesson/rank
  F zhihu#10 China stations called zhan vs Japan/Korea chao called yi (103wan) ->
    station/post/courier face: station/post-station/ferry/pier/crossroads

Plus: global clean-row census across ALL axes x buckets + sprite (fleet includes
DAILY-v59) to ground the honest-mapping decision on remaining material.
Output: r1030_probe2.txt
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

out = io.StringIO()
def w(s):
    out.write(s)
    out.write(u'\n')

w(u'R1030 REACT-v9 probe round 2 (fleet includes DAILY-v59 F-144)')
w(u'=' * 70)

# --- E education / F station keyword groups ---
KW_E = [u'\u529f\u8bfe', u'\u8003\u8bd5', u'\u672c\u4e8b', u'\u72b9\u592a', u'\u8bfb\u4e66', u'\u4e0a\u8bfe', u'\u5b66\u5f92', u'\u540d\u6b21']
KW_F = [u'\u9a7f\u7ad9', u'\u8f66\u7ad9', u'\u7ad9\u53f0', u'\u6e21\u53e3', u'\u7801\u5934', u'\u8857\u53e3', u'\u62d7\u70b9']
GROUPS = [(u'E_education', KW_E), (u'F_station', KW_F)]

AXES = list(pool['axes'].keys())
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

# --- global clean-row census (all axes x buckets + sprite) ---
w(u'== GLOBAL CLEAN-ROW CENSUS (zero direct shingle hits vs fleet + spirit) ==')
SEASONAL = [u'年味', u'过年', u'春联', u'春雨', u'除夕', u'拜年', u'红包', u'元宵', u'汤圆', u'年年有余']
total_clean = 0
for ax in AXES:
    for bk, rows in pool['axes'][ax].items():
        for i, line in enumerate(rows):
            if any(s in line for s in SEASONAL):
                continue
            if not probe(line):
                w(u'CLEAN %s/%s/%d %s' % (ax, bk, i, line))
                total_clean += 1
for bk, rows in pool.get('sprite', {}).items():
    for i, line in enumerate(rows):
        if any(s in line for s in SEASONAL):
            continue
        if not probe(line):
            w(u'CLEAN sprite/%s/%d %s' % (bk, i, line))
            total_clean += 1
w(u'== total clean rows (seasonal-excluded): %d ==' % total_clean)
w(u'=' * 70)

io.open(os.path.join(ROOT, '.c3-tmp', 'r1030_probe2.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('done, clean total:', total_clean)
