# -*- coding: utf-8 -*-
"""R1029 DAILY v59 xiaqi-axis FULL fresh supply-face scan (fleet includes DAILY-v58).
Rotation post-v58: qiuxin 10 / huaijiu 9 / xiaqi 9 / yanhuo 10 / zhixu 9 / xiaoyao 9 ->
FOUR axes tied at 9 -> redemption target = xiaqi (last v52 night/4, gap v53..v58 = 6
pieces = LONGEST; R1028 next-pointer redemption). xiaqi consumed faces: festival 8 rows
(v3/5 + v8/13 + v13/2 + v20/1 + v26/10 + v34/9 + v46/7 + city-spirit v1.2/0) + night/4
(v52). Production ~23:4x deep night -> night bucket = literal time-exact first-priority
face (v51/v52/v53/v54 precedent). Same probe standard as r1023/r1026/r1027/r1028:
2-5 char shingles (punctuation-inclusive) vs fleet card faces (lines + source_quote,
R1010 card-face-level law) + city-spirit.md. Output: .c3-tmp/r1029_pool.txt (UTF-8).
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

AXIS = u'\u4fa0\u6c14'  # xiaqi
BUCKETS = [u'night', u'festival', u'dusk', u'market_close', u'morning', u'weekend',
           u'rain', u'typhoon', u'heatwave', u'coldsnap', u'market_open', u'ceo_order']

out = io.StringIO()
def w(s):
    out.write(s)
    out.write(u'\n')

w(u'R1029 DAILY v59 xiaqi-axis FULL fresh supply-face scan (fleet includes DAILY-v58 yanhuo/weekend/7)')
w(u'Day-context: 2026-10-02 National Day holiday day 2 DEEP NIGHT, production ~23:4x literal night (night bucket 5th piece candidate, v51 yanhuo + v52 xiaqi + v53 zhixu + v54 sprite precedents)')
w(u'Rotation: post-v58 qiuxin 10 / huaijiu 9 / xiaqi 9 / yanhuo 10 / zhixu 9 / xiaoyao 9 -> FOUR tied at 9 -> target xiaqi (v52 night/4, gap v53..v58 = 6 LONGEST = R1028 pointer redemption)')
w(u'Priority order: night (literal time-exact) > festival (day-2 window, 10 residual rows) > dusk > market_close (evening-adjacent) > remaining 8 buckets (season/context honest notes)')
w(u'=' * 70)

clean_count = {}
for bk in BUCKETS:
    rows = pool['axes'][AXIS][bk]
    w(u'== xiaqi/%s %d rows ==' % (bk, len(rows)))
    clean = 0
    clean_rows = []
    for i, line in enumerate(rows):
        seas = u' | SEASONAL(R972)' if any(s in line for s in SEASONAL) else u''
        w(u'FREE line%-2d %s%s' % (i, line, seas))
        if not seas:
            kept = probe(line)
            if not kept:
                w(u'    -> ZERO direct shingle hits (CLEAN ROW)')
                clean += 1
                clean_rows.append(i)
            else:
                for sh, where in kept:
                    w(u'    HIT [%s] -> %s' % (sh, where))
    clean_count[bk] = clean
    if clean_rows:
        w(u'== bucket %s clean rows: %d -> lines %s ==' % (bk, clean, clean_rows))
    else:
        w(u'== bucket %s clean rows: %d ==' % (bk, clean))
    w(u'=' * 70)

# v52 consumed row USED re-check (R978 lesson)
xq = pool['axes'][AXIS][u'night']
v52_face = faces.get(u'MC-20261002-DAILY-v52', u'')
w(u'[check] xiaqi/night/4 (v52) USED re-verification: line in v52 card face -> %s' % (xq[4] in v52_face))
w(u'[check] v58 consumed row re-verification: yanhuo/weekend/7 in v58 card face -> %s' % (pool['axes'][u'\u70df\u706b'][u'weekend'][7] in faces.get(u'MC-20261002-DAILY-v58', u'')))
w(u'[rotation note] post-v59 registration: xiaqi becomes 10 -> counts 10/9/10/10/9/9 -> next minimum = two-way tie (huaijiu last v55 gap 3 / zhixu last v53 gap 5 / xiaoyao last v56 gap 2)... recompute: qiuxin 10/huaijiu 9/xiaqi 10/yanhuo 10/zhixu 9/xiaoyao 9 -> tied at 9: huaijiu (gap v56..v59=3) / zhixu (gap v54..v59=5) / xiaoyao (gap v57..v59=2) -> next target = zhixu (longest gap 5) with night/festival face re-scan; 10-03 day-boundary round = E31 REACT-v9 first claim (daily brief 10-03 missing = produce first per O-2304 iron rule)')

io.open(os.path.join(ROOT, '.c3-tmp', 'r1029_pool.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('r1029 xiaqi full scan done, clean counts:', json.dumps(clean_count, ensure_ascii=True))
