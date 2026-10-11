# R2010 tech#117 part4: v13/v15 card-only vs with-m1 reconciliation
import json, io, sys, os, re, glob
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

for vn in ('MC-20261010-REACT-v13', 'MC-20261012-REACT-v15'):
    cdir = os.path.join(CARD_ROOT, vn)
    cj = json.load(open(os.path.join(cdir, 'cards.json'), encoding='utf-8'))
    base = norm(' '.join(it(cj)) + ' ' + open(os.path.join(cdir, 'subs.srt'), encoding='utf-8-sig').read())
    extra = ''
    for m in glob.glob(os.path.join(cdir, 'm1-assert-*.txt')):
        extra += open(m, encoding='utf-8', errors='replace').read()
    withm1 = norm(base + ' ' + extra)
    print('===', vn, '===')
    for tag, blob in (('card-only', base), ('with-m1', withm1)):
        hits = [k for k in pool_index if k and k in blob]
        print(tag, len(hits))
        if tag == 'with-m1':
            only = [k for k in hits if not (k and k in base)]
            for k in only:
                for (kind, ax, b, i) in pool_index[k]:
                    raw = axes[ax][b][i-1] if kind == 'axis' else sprite[b][i-1]
                    print('   M1-ONLY:', kind, ax, b, i, raw)
