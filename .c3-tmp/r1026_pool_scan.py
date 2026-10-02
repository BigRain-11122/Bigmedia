# -*- coding: utf-8 -*-
"""R1026 pool scan: DAILY v56 pick. Rotation post-v55 counts (machine-pointer chain R1025):
qiuxin 9 / huaijiu 9 / xiaqi 9 / yanhuo 9 / zhixu 9 / xiaoyao 8 (sprite tracked separately:
v50 festival/0 + v54 night/8). XIAOYAO unique minimum (last piece v48, gap 7 = LONGEST) ->
redemption target = xiaoyao. xiaoyao/night face = machine-proven zero clean rows (r1023_pool.txt
fresh, re-confirmed r1024; fleet additions only add collisions, blocked status stable).
Per R1025 rotation note + pre-registration: xiaoyao x {festival, dusk, market_close} fresh
re-probe against CURRENT fleet (now includes DAILY-v55 huaijiu/market_close/1). Expected
pre-registered backup: xiaoyao/dusk line6. Probe standard (R1013/R1018/R1023-R1025 series law):
shingle hits vs fleet card faces (lines+source_quote) + city-spirit.md. Zero-direct-collision
row wins; >=3-char content shingle hit OR distinctive 2-char noun repeat = direct collision
flag; construct-layer 2-char (function/opener/punctuation) = honest adjacency note.
Output: .c3-tmp/r1026_pool.txt (UTF-8).
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

w(u'R1026 DAILY v56 xiaoyao-redemption fresh re-probe (fleet includes DAILY-v55 huaijiu/market_close/1 consumed)')
w(u'Day-context: 2026-10-02 National Day holiday day 2 DEEP NIGHT, production ~23:0x literal night (night face for target axis = machine-proven blocked)')
w(u'Rotation post-v55 (R1025 machine-pointer chain): qiuxin 9 / huaijiu 9 / xiaqi 9 / yanhuo 9 / zhixu 9 / xiaoyao 8 | sprite 2 (v50 festival/0 + v54 night/8)')
w(u'XIAOYAO unique minimum (v48, gap 7 = LONGEST) -> redemption target = xiaoyao')
w(u'xiaoyao/night face machine-proven zero clean rows (r1023_pool.txt fresh, re-confirmed r1024 cascade; fleet additions only ADD collisions -> blocked status stable, NOT re-scanned)')
w(u'SUPPLY FACES for xiaoyao = {festival, dusk, market_close} fresh re-probe (R1025 pre-registered backup: xiaoyao/dusk line6; quality selection among clean rows, NOT ordinal blind-pick)')
w(u'=' * 70)

axes = pool['axes']
FACES_TO_SCAN = [(u'逍遥', b) for b in (u'festival', u'dusk', u'market_close')]

clean_registry = []
for axis, bucket in FACES_TO_SCAN:
    rows = axes[axis][bucket]
    w(u'[PRIMARY] %s/%s %d rows' % (axis, bucket, len(rows)))
    for i, line in enumerate(rows):
        kept = probe(line)
        if not kept:
            w(u'    FREE line%-2d %s' % (i, line))
            w(u'        -> ZERO direct shingle hits (clean row)')
            clean_registry.append((axis, bucket, i, line))
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
w(u'[rotation note] post-v56 pick decision: xiaoyao/dusk line6 = R1025 pre-registered backup redeemed (3rd backup-promotion after v53/v54); honest notes for construct-layer adjacency recorded in build script probe; post-v56 rotation pointer = re-count machine chain (all axes 9 except whichever axis was NOT touched -> next minimum axis by gap) - carried in build meta + queue row.')

io.open(os.path.join(ROOT, '.c3-tmp', 'r1026_pool.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('scan done; clean rows:', len(clean_registry))
for a, b, i, l in clean_registry:
    print(a, b, i, l)
