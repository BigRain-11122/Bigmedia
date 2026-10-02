# -*- coding: utf-8 -*-
"""R1027 pool scan: DAILY v57 pick. Rotation post-v56 (R1026 machine-pointer chain):
qiuxin 9 / huaijiu 9 / xiaqi 9 / yanhuo 9 / zhixu 9 / xiaoyao 9 = SIX AXES ALL-TIED (4th
all-tie state after v36/v42/v48-era states; precedent R1006/R1012/R1018 = all-tie ->
longest-gap redemption). qiuxin last consumed v49 (festival/9), gap = v50..v56 seven
pieces all other axes = LONGEST redemption distance -> redemption target = qiuxin.
Per R1026 next-pointer: v57 = qiuxin axis full fresh supply-face scan (ALL 12 buckets x
18 rows = 216 rows) against CURRENT fleet (includes DAILY-v56 xiaoyao/dusk/6 consumed).
Day-context: 2026-10-02 National Day holiday day 2 DEEP NIGHT, production ~23:2x ->
night bucket = literal time-point direct match (strongest), festival = holiday direct.
Probe standard (R1013/R1018/R1023-R1026 series law): shingle hits vs fleet card faces
(lines+source_quote) + city-spirit.md. Zero-direct-collision row wins; >=3-char content
shingle hit OR distinctive 2-char noun repeat = direct collision flag; construct-layer
2-char (function/opener/punctuation) = honest adjacency note.
Output: .c3-tmp/r1027_pool.txt (UTF-8). Console = clean-row registry only.
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

w(u'R1027 DAILY v57 qiuxin-redemption FULL fresh scan (fleet includes DAILY-v56 xiaoyao/dusk/6 consumed)')
w(u'Day-context: 2026-10-02 National Day holiday day 2 DEEP NIGHT, production ~23:2x -> night bucket = literal time-point direct match; festival = holiday direct match')
w(u'Rotation post-v56 (R1026 machine-pointer chain): qiuxin 9 / huaijiu 9 / xiaqi 9 / yanhuo 9 / zhixu 9 / xiaoyao 9 = SIX AXES ALL-TIED (4th all-tie; R1006/R1012/R1018 precedent = longest-gap redemption)')
w(u'qiuxin last consumed v49 (festival/9), gap 7 (v50..v56 all other axes) = LONGEST -> redemption target = qiuxin')
w(u'SUPPLY FACES = ALL 12 buckets full scan per R1026 pointer (fresh, not ordinal blind-pick)')
w(u'=' * 70)

axes = pool['axes']
# scan order: literal/holiday-context faces first, then adjacency, then weather/context faces
BUCKET_ORDER = [u'night', u'festival', u'dusk', u'market_close', u'morning', u'weekend',
                u'market_open', u'rain', u'typhoon', u'heatwave', u'coldsnap', u'ceo_order']

clean_registry = []
for bucket in BUCKET_ORDER:
    rows = axes[u'求新'][bucket]
    tag = u'[LITERAL-NIGHT]' if bucket == u'night' else (u'[HOLIDAY]' if bucket == u'festival' else u'')
    w(u'[PRIMARY] %s/%s %d rows %s' % (u'求新', bucket, len(rows), tag))
    for i, line in enumerate(rows):
        kept = probe(line)
        if not kept:
            w(u'    FREE line%-2d %s' % (i, line))
            w(u'        -> ZERO direct shingle hits (clean row)')
            clean_registry.append((u'求新', bucket, i, line))
        else:
            w(u'    line%-2d %s' % (i, line))
            for sh, where in kept[:6]:
                w(u'        HIT [%s] -> %s' % (sh, where))
            if len(kept) > 6:
                w(u'        ... +%d more hits' % (len(kept) - 6))
    w(u'=' * 70)

w(u'CLEAN ROW REGISTRY (zero direct shingle hits):')
for axis, bucket, i, line in clean_registry:
    w(u'  %s/%s line%d %s' % (axis, bucket, i, line))
w(u'=' * 70)
w(u'[rotation note] post-v57 pick decision: quality selection among clean rows with day-context priority (night literal > festival holiday > dusk/market_close adjacency > others), NOT ordinal blind-pick; construct-layer adjacency honest notes recorded in build script probe; post-v57 rotation pointer = re-count machine chain (post-v57 counts: qiuxin 10, all others 9 -> next minimum by gap) - carried in build meta + queue row.')

io.open(os.path.join(ROOT, '.c3-tmp', 'r1027_pool.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('scan done; clean rows:', len(clean_registry))
for a, b, i, l in clean_registry:
    print(a, b, i, l)
