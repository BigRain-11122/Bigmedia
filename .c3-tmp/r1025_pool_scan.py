# -*- coding: utf-8 -*-
"""R1025 pool scan: DAILY v55 pick. Rotation post-v54 counts: qiuxin 9 / huaijiu 8 /
xiaqi 9 / yanhuo 9 / zhixu 9 / xiaoyao 8 (sprite tracked separately: v50 festival/0 +
v54 night/8). Tie at 8: huaijiu (v45, gap 9 = LONGEST) / xiaoyao (v48, gap 6).
Redemption target = huaijiu. huaijiu/night face = machine-proven zero clean rows
(r1023_pool.txt fresh, both huaijiu 18 rows all content collisions and xiaoyao/night
18 rows all carry hits). Per R1024 rotation note + focus pre-registration:
SUPPLY-FACE SWITCH for v55 = festival return OR dusk/market_close evening-adjacent
buckets, fresh scan. This scan = that fresh pre-probe against CURRENT fleet (now
includes DAILY-v54 sprite/night/8). Probe standard (R1013/R1018/R1023/R1024 series
law): shingle hits vs fleet card faces (lines+source_quote) + city-spirit.md.
Zero-direct-collision row wins; >=3-char content shingle hit OR distinctive 2-char
noun repeat = direct collision flag; construct-layer 2-char (function/opener/
punctuation) = honest adjacency note. Backup faces (xiaoyao festival/dusk/
market_close) scanned same run for pre-registration. Output: .c3-tmp/r1025_pool.txt
(UTF-8).
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

w(u'R1025 DAILY v55 supply-face-switch fresh pre-scan (fleet includes DAILY-v54 sprite/night/8 consumed)')
w(u'Day-context: 2026-10-02 National Day holiday day 2 NIGHT, production ~22:3x literal night (night face for target axis = blocked)')
w(u'Rotation post-v54: qiuxin 9 / huaijiu 8 / xiaqi 9 / yanhuo 9 / zhixu 9 / xiaoyao 8 | sprite 2 (v50 festival/0 + v54 night/8)')
w(u'Tie at 8: huaijiu (v45, gap 9 = LONGEST) + xiaoyao (v48, gap 6) -> redemption target = huaijiu')
w(u'huaijiu/night + xiaoyao/night faces machine-proven zero clean rows (r1023_pool.txt fresh, re-confirmed in r1024 cascade) -> zero-collision standard NOT relaxed (v1-v54 fifty-four-link zero-collision chain)')
w(u'SUPPLY-FACE SWITCH (R1024 rotation note + focus pre-registration): huaijiu x {festival return, dusk, market_close evening-adjacent} primary + xiaoyao x same three faces backup (pre-registration)')
w(u'=' * 70)

axes = pool['axes']
PRIMARY = [(u'怀旧', b) for b in (u'festival', u'dusk', u'market_close')]
BACKUP = [(u'逍遥', b) for b in (u'festival', u'dusk', u'market_close')]

clean_registry = []
for axis, bucket in PRIMARY + BACKUP:
    rows = axes[axis][bucket]
    tag = u'PRIMARY' if axis == u'怀旧' else u'BACKUP'
    w(u'[%s] %s/%s %d rows' % (tag, axis, bucket, len(rows)))
    for i, line in enumerate(rows):
        kept = probe(line)
        if not kept:
            w(u'    FREE line%-2d %s' % (i, line))
            w(u'        -> ZERO direct shingle hits (clean row)')
            clean_registry.append((axis, bucket, i, line))
        else:
            # compress: only report rows that are NEAR-clean (1-2 construct-layer hits) or fully dirty summary
            content_hits = [x for x in kept]
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
w(u'[rotation note] post-v55 pick decision: quality selection among clean rows (NOT ordinal blind-pick); day-context priority = dusk/market_close (evening-adjacent to 22:3x production moment) > festival (holiday return); axis priority = huaijiu (gap 9 longest) > xiaoyao (gap 6). If huaijiu clean rows exist on evening-adjacent faces -> take best huaijiu row; honest notes for construct-layer adjacency recorded in build script probe.')

io.open(os.path.join(ROOT, '.c3-tmp', 'r1025_pool.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('scan done')
