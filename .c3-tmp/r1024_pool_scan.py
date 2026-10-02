# -*- coding: utf-8 -*-
"""R1024 pool scan: DAILY v54 pick. Rotation post-v53 counts: qiuxin 9 / huaijiu 8 /
xiaqi 9 / yanhuo 9 / zhixu 9 / xiaoyao 8 (sprite tracked separately: v50 festival/0).
Tie at 8: huaijiu (v45, gap 8) / xiaoyao (v48, gap 5) - BOTH blocked on night face fresh
per r1023_pool.txt (huaijiu/night 18 rows all carry content collisions; xiaoyao/night 18
rows all carry hits). -> cascade to pre-registered second backup = sprite/night line8
(R1022 pre-registered, "fresh re-probe needed" note). This scan = that fresh re-probe
against the CURRENT fleet (which now includes v53 zhixu/night/7 face). Probe standard
(R1013/R1018/R1019/R1023 series law): shingle hits vs fleet card faces
(lines+source_quote) + city-spirit.md. Zero-direct-collision row wins; >=3-char content
shingle hit OR distinctive 2-char noun repeat = direct collision flag; construct-layer
2-char (function/opener/punctuation) = honest adjacency note. Output: .c3-tmp/r1024_pool.txt
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

w(u'R1024 DAILY v54 sprite/night pre-scan (fresh; fleet includes DAILY-v53 zhixu/night/7 consumed)')
w(u'Day-context: 2026-10-02 National Day holiday day 2 NIGHT, production ~22:2x literal night (night bucket 4th piece, v51/v52/v53 precedent chain)')
w(u'Rotation post-v53: qiuxin 9 / huaijiu 8 / xiaqi 9 / yanhuo 9 / zhixu 9 / xiaoyao 8 | sprite 1 (v50 festival/0)')
w(u'Tie at 8: huaijiu (v45, gap 8) + xiaoyao (v48, gap 5) - both night faces machine-proven zero clean rows (r1023_pool.txt fresh) -> cascade to sprite/night line8 = R1022 pre-registered second backup (fresh re-probe = this scan)')
w(u'=' * 70)

sprite = pool['sprite']
nb = sprite[u'night']
w(u'[S] sprite/night %d rows (sprite voice 2nd piece candidate; night-bucket prior consumption = v51 yanhuo/13 + v52 xiaqi/4 + v53 zhixu/7)' % len(nb))
for i, line in enumerate(nb):
    w(u'FREE line%-2d %s' % (i, line))
    kept = probe(line)
    if not kept:
        w(u'    -> ZERO direct shingle hits (clean row)')
    else:
        for sh, where in kept:
            w(u'    HIT [%s] -> %s' % (sh, where))
w(u'=' * 70)
w(u'[check] v53 zhixu/night/7 USED re-verification: line in v53 card face -> %s')
w(u'[check] sprite/night line8 candidate: %s' % nb[8])
w(u'[rotation note] post-v54 (if line8 consumed): sprite night face = line8 consumed; night bucket = 4th piece; next backups TBD by fresh scan next round; supply-face switch (dusk bucket / market_close bucket = evening-adjacent faces) = structural candidates for v55 if night face exhausts clean rows')

io.open(os.path.join(ROOT, '.c3-tmp', 'r1024_pool.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('scan done')
