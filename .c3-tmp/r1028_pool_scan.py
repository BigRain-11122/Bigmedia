# -*- coding: utf-8 -*-
"""R1028 DAILY v58 yanhuo-axis FULL fresh supply-face scan (fleet includes DAILY-v57).
Rotation post-v57: qiuxin 10 / huaijiu 9 / xiaqi 9 / yanhuo 9 / zhixu 9 / xiaoyao 9 ->
five axes tied at 9 -> redemption target = yanhuo (last v51 night/13, gap v52..v57 = 6
pieces = LONGEST; R1027 next-pointer redemption). Per R1027 pointer: yanhuo supply faces
fresh full scan - night face consumed v51/13 only (17 candidate rows remain), festival
face consumed 8 rows (v4/4+v11/13+v19/3+v24/2+v27/7+v32/10+v38/5+v44/1), other 10 buckets
untouched (180 rows). Production ~23:4x deep night -> night bucket = literal time-exact
first-priority face (v51 precedent). Same probe standard as r1023/r1026/r1027: 2-5 char
shingles (punctuation-inclusive) vs fleet card faces (lines + source_quote, R1010
card-face-level law) + city-spirit.md. Output: .c3-tmp/r1028_pool.txt (UTF-8).
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

AXIS = u'\u70df\u706b'  # yanhuo
BUCKETS = [u'night', u'festival', u'dusk', u'market_close', u'morning', u'weekend',
           u'rain', u'typhoon', u'heatwave', u'coldsnap', u'market_open', u'ceo_order']

out = io.StringIO()
def w(s):
    out.write(s)
    out.write(u'\n')

w(u'R1028 DAILY v58 yanhuo-axis FULL fresh supply-face scan (fleet includes DAILY-v57 qiuxin/market_close/1)')
w(u'Day-context: 2026-10-02 National Day holiday day 2 DEEP NIGHT, production ~23:4x literal night (night bucket 4th piece candidate, v51 yanhuo + v52 xiaqi + v53 zhixu + v54 sprite precedents)')
w(u'Rotation: post-v57 qiuxin 10 / huaijiu 9 / xiaqi 9 / yanhuo 9 / zhixu 9 / xiaoyao 9 -> five tied at 9 -> target yanhuo (v51 night/13, gap 6 LONGEST = R1027 pointer redemption)')
w(u'Priority order: night (literal time-exact) > festival (day-2 window) > dusk > market_close (evening-adjacent) > remaining 8 buckets (season/context honest notes)')
w(u'=' * 70)

clean_count = {}
for bk in BUCKETS:
    rows = pool['axes'][AXIS][bk]
    w(u'== yanhuo/%s %d rows ==' % (bk, len(rows)))
    clean = 0
    for i, line in enumerate(rows):
        seas = u' | SEASONAL(R972)' if any(s in line for s in SEASONAL) else u''
        w(u'FREE line%-2d %s%s' % (i, line, seas))
        if not seas:
            kept = probe(line)
            if not kept:
                w(u'    -> ZERO direct shingle hits (CLEAN ROW)')
                clean += 1
            else:
                for sh, where in kept:
                    w(u'    HIT [%s] -> %s' % (sh, where))
    clean_count[bk] = clean
    w(u'== bucket %s clean rows: %d ==' % (bk, clean))
    w(u'=' * 70)

# v51 consumed row USED re-check (R978 lesson)
yn = pool['axes'][AXIS][u'night']
v51_face = faces.get(u'MC-20261002-DAILY-v51', u'')
w(u'[check] yanhuo/night/13 (v51) USED re-verification: line in v51 card face -> %s' % (yn[13] in v51_face))
w(u'[check] v57 consumed row re-verification: qiuxin/market_close/1 in v57 card face -> %s' % (pool['axes'][u'\u6c42\u65b0'][u'market_close'][1] in faces.get(u'MC-20261002-DAILY-v57', u'')))
w(u'[rotation note] post-v58 registration: yanhuo becomes 10 -> counts 10/9/9/10/9/9 -> next minimum three-way tie (huaijiu last v55 gap 2 / xiaqi last v52 gap 5 / zhixu last v53 gap 4 / xiaoyao last v56 gap 1) -> next target = xiaqi (longest gap) with night/festival face re-scan; 10-03 day-boundary round = E31 REACT-v9 first claim (daily brief 10-03 missing = produce first)')

io.open(os.path.join(ROOT, '.c3-tmp', 'r1028_pool.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('r1028 yanhuo full scan done, clean counts:', json.dumps(clean_count, ensure_ascii=True))
