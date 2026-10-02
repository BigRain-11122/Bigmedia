# -*- coding: utf-8 -*-
"""R1019 pool scan: DAILY v50 axis pick = yanhuo redemption (5-piece gap, tied-8 five axes).
R1018 pre-registered structural note: six-axis festival resident-bucket FREE-face all-weak ->
sprite festival 12 lines = next-supply candidate. This scan machine-probes BOTH faces:
(A) yanhuo/festival FREE rows (used={1,2,3,4,5,7,10,12,13}; law-excluded seasonal rows flagged)
(B) sprite top-level festival bucket rows (zero consumption so far per R1018 note)
Probe standard (R1013/R1018 series law): shingle hits vs fleet card faces (lines+source_quote)
+ city-spirit.md. Zero-direct-collision row wins (v44/v47/v48/v49 precedent); >=3-char content
shingle hit OR distinctive 2-char noun repeat = direct collision flag; construct-layer 2-char
(function/opener/sigh words) = honest adjacency note; nian-wei/seasonal wording = R972 law exclusion.
Output: .c3-tmp/r1019_pool.txt (UTF-8).
"""
import io, json, os, re

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
BASE = os.path.join(ROOT, 'data', 'storylines', 'cards')

pool = json.load(io.open(os.path.join(ROOT, '..', '..', 'life', 'BigLife', 'cognition', 'pools.json'), encoding='utf-8'))
spirit = io.open(os.path.join(ROOT, 'data', 'storylines', 'codex', 'city-spirit.md'), encoding='utf-8').read()

# fleet card faces (R1010 law: lines + source_quote, card-face level)
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

FUNCTION_WORDS = set([u'的了呢啊吧是在也得还又都就才要把被和与跟', u'节日', u'灯笼', u'热闹', u'好个', u'看看', u'看这', u'咱们', u'咱这', u'真好好', u'一个', u'一些', u'这个', u'那'])
SEASONAL = [u'年味', u'过年', u'春联', u'春雨', u'除夕', u'拜年', u'红包', u'元宵', u'汤圆', u'年年有余']

def probe(text):
    hits = {}
    for sh in sorted(shingles(text), key=len, reverse=True):
        if len(sh) < 2:
            continue
        # skip shingles fully inside a longer reported hit for readability
        where = sorted(d for d, f in faces.items() if sh in f)
        if not where and sh not in spirit:
            continue
        spirit_hit = sh in spirit
        if where or spirit_hit:
            key = (sh, u','.join(where) if where else u'city-spirit')
            hits[sh] = key
    # compress: keep only maximal (non-subsumed) hit shingles
    kept = []
    for sh in sorted(hits, key=len, reverse=True):
        if any(sh != k and sh in k for k in [x[0] for x in kept]):
            continue
        kept.append((sh, hits[sh][1]))
    return kept

out = io.StringIO()
def w(s):
    out.write(s if isinstance(s, str) else s.encode('utf-8').decode('utf-8'))
    out.write(u'\n')

w(u'R1019 DAILY v50 pool scan (yanhuo redemption + sprite face, R1018 pre-registration)')
w(u'=' * 70)

# (A) yanhuo/festival face
fest = pool['axes'][u'\u70df\u706b'][u'festival']  # yanhuo
used_y = {1, 2, 3, 4, 5, 7, 10, 12, 13}
w(u'[A] yanhuo/festival 18 rows; used=%s' % sorted(used_y))
for i, line in enumerate(fest):
    mark = u'USED' if i in used_y else u'FREE'
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
# (B) sprite festival face
sprite = pool.get('sprite')
w(u'[B] sprite top-level keys: %s' % (sorted(sprite.keys()) if isinstance(sprite, dict) else type(sprite).__name__))
sf = sprite.get(u'festival') if isinstance(sprite, dict) else None
if sf:
    w(u'sprite/festival %d rows (R1018 note: 12 lines unconsumed)' % len(sf))
    for i, line in enumerate(sf):
        seas = u' | SEASONAL(R972)' if any(s in line for s in SEASONAL) else u''
        w(u'FREE line%-2d %s%s' % (i, line, seas))
        if not seas:
            kept = probe(line)
            if not kept:
                w(u'    -> ZERO direct shingle hits (clean row)')
            else:
                for sh, where in kept:
                    w(u'    HIT [%s] -> %s' % (sh, where))

io.open(os.path.join(ROOT, '.c3-tmp', 'r1019_pool.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('scan done')
