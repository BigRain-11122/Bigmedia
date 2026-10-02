# -*- coding: utf-8 -*-
"""R1020 pool scan: DAILY v51 axis pick. Rotation post-v50 counts: qiuxin 9 / huaijiu 8 /
xiaqi 8 / yanhuo 8 / zhixu 8 / xiaoyao 8 (sprite tracked separately, 1 piece v50).
Redemption target by longest gap = yanhuo (v44, 6-piece gap) - R1019 suspended verdict
re-verification (FREE face all-weak, stable). Cascade order by gap among tied-8 axes:
huaijiu (v45, gap 5) -> xiaqi (v46, gap 4) -> zhixu (v47, gap 3) -> xiaoyao (v48, gap 2).
Sprite festival face re-probe post-v50: line6/line10 previously clean now carry ding-ding
2-char adjacency hit vs v50 face (ding-ding family consumed by v50) -> expect ZERO clean rows.
Probe standard (R1013/R1018/R1019 series law): shingle hits vs fleet card faces
(lines+source_quote) + city-spirit.md. Zero-direct-collision row wins; >=3-char content
shingle hit OR distinctive 2-char noun repeat = direct collision flag; construct-layer
2-char (function/opener/punctuation) = honest adjacency note; nian-wei/seasonal = R972
law exclusion. Output: .c3-tmp/r1020_pool.txt (UTF-8).
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

w(u'R1020 DAILY v51 pool scan (yanhuo re-verify + tied-8 cascade huaijiu/xiaqi/zhixu/xiaoyao + sprite post-v50)')
w(u'Rotation post-v50: qiuxin 9 / huaijiu 8 / xiaqi 8 / yanhuo 8 / zhixu 8 / xiaoyao 8 | sprite 1 (v50 line0)')
w(u'Redemption target = yanhuo (v44 gap 6, R1019 suspended) -> cascade by gap: huaijiu (v45, 5) -> xiaqi (v46, 4) -> zhixu (v47, 3) -> xiaoyao (v48, 2)')
w(u'=' * 70)

AXES = [
    (u'\u70df\u706b', u'yanhuo', u'A', {1, 2, 3, 4, 5, 7, 10, 12, 13}, u'[A] rotation target, R1019 suspended - re-verify'),
    (u'\u6000\u65e7', u'huaijiu', u'B', {0, 1, 3, 4, 5, 12, 16, 17}, u'[B] cascade rank 1 (v45, gap 5)'),
    (u'\u4fa0\u6c14', u'xiaqi', u'C', {0, 1, 2, 5, 7, 9, 10, 13}, u'[C] cascade rank 2 (v46, gap 4)'),
    (u'\u79e9\u5e8f', u'zhixu', u'D', {2, 4, 6, 9, 11, 12, 14, 15, 16, 17}, u'[D] cascade rank 3 (v47, gap 3)'),
    (u'\u900d\u9065', u'xiaoyao', u'E', {0, 1, 2, 3, 4, 5, 13, 15, 16, 17}, u'[E] cascade rank 4 (v48, gap 2)'),
]

for ax, name, tag, used, note in AXES:
    fest = pool['axes'][ax][u'festival']
    w(u'%s %s/festival 18 rows; used=%s | %s' % (tag, name, sorted(used), note))
    for i, line in enumerate(fest):
        mark = u'USED' if i in used else u'FREE'
        seas = u' | SEASONAL(R972)' if any(s in line for s in SEASONAL) else u''
        w(u'%s line%-2d %s%s' % (mark, i, line, seas))
        if mark == u'FREE' and not seas:
            kept = probe(line)
            if not kept:
                w(u'    -> ZERO direct shingle hits (clean row)')
            else:
                for sh, where in kept:
                    w(u'    HIT [%s] -> %s' % (sh, where))
    w(u'=' * 70)

sprite = pool.get('sprite')
sf = sprite.get(u'festival') if isinstance(sprite, dict) else None
w(u'[F] sprite/festival %d rows re-probe post-v50 (used={0}; line6/line10 ding-ding adjacency expectation)' % len(sf))
for i, line in enumerate(sf):
    seas = u' | SEASONAL(R972)' if any(s in line for s in SEASONAL) else u''
    mark = u'USED' if i == 0 else u'FREE'
    w(u'%s line%-2d %s%s' % (mark, i, line, seas))
    if mark == u'FREE' and not seas:
        kept = probe(line)
        if not kept:
            w(u'    -> ZERO direct shingle hits (clean row)')
        else:
            for sh, where in kept:
                w(u'    HIT [%s] -> %s' % (sh, where))

io.open(os.path.join(ROOT, '.c3-tmp', 'r1020_pool.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('scan done')
