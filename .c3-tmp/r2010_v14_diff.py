# R2010 tech#117 part3: v14 card-only vs with-m1 diff (52 vs 51 reconciliation)
import json, io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
POOL = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json'
CARD_ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines\cards'
d = json.load(open(POOL, encoding='utf-8'))
axes, sprite = d['axes'], d['sprite']

def norm(s):
    return re.sub(r'[\s，。、；：？！「」『』（）——…·,.!?;:\'"~]', '', s)

pool_index = {}
for ax, bv in axes.items():
    for b, lines in bv.items():
        for i, ln in enumerate(lines, 1):
            pool_index.setdefault(norm(ln), []).append(('axis', ax, b, i))
for b, lines in sprite.items():
    for i, ln in enumerate(lines, 1):
        pool_index.setdefault(norm(ln), []).append(('sprite', '-', b, i))

def it(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from it(v)
    elif isinstance(o, list):
        for v in o:
            yield from it(v)

cdir = os.path.join(CARD_ROOT, 'MC-20261011-REACT-v14')
cj = json.load(open(os.path.join(cdir, 'cards.json'), encoding='utf-8'))
base = norm(' '.join(it(cj)) + ' ' + open(os.path.join(cdir, 'subs.srt'), encoding='utf-8-sig').read())
withm1 = norm(base + ' ' + open(os.path.join(cdir, 'm1-assert-r1967.txt'), encoding='utf-8', errors='replace').read())
for tag, blob in (('card-only', base), ('with-m1', withm1)):
    hits = [k for k in pool_index if k and k in blob]
    print(tag, len(hits))
    for k in hits:
        for (kind, ax, b, i) in pool_index[k]:
            raw = axes[ax][b][i-1] if kind == 'axis' else sprite[b][i-1]
            print('   ', kind, ax, b, i, raw)
