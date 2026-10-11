# R2010 tech#117: inspect BigLife pools.json structure (read-only, cross-repo)
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json'
d = json.load(open(p, encoding='utf-8'))
axes = d['axes']
sprite = d['sprite']
print('axes keys:', list(axes.keys()))
print('sprite buckets:', list(sprite.keys()))
# inspect one axis value and one sprite bucket value
k0 = list(axes.keys())[0]
v0 = axes[k0]
print('axes[%r] type:' % k0, type(v0).__name__)
if isinstance(v0, dict):
    print('  sub keys:', list(v0.keys())[:20])
    sk0 = list(v0.keys())[0]
    sv = v0[sk0]
    print('  axes[%r][%r] type:' % (k0, sk0), type(sv).__name__, 'len:', len(sv) if hasattr(sv, '__len__') else '-')
    if isinstance(sv, list) and sv:
        print('  sample line:', repr(sv[0])[:120])
elif isinstance(v0, list):
    print('  len:', len(v0), 'sample:', repr(v0[0])[:120] if v0 else '')
b0 = list(sprite.keys())[0]
v1 = sprite[b0]
print('sprite[%r] type:' % b0, type(v1).__name__)
if isinstance(v1, dict):
    print('  sub keys:', list(v1.keys())[:20])
    for sk in list(v1.keys())[:2]:
        sv = v1[sk]
        print('  sprite[%r][%r] type:' % (b0, sk), type(sv).__name__, 'len:', len(sv) if hasattr(sv, '__len__') else '-')
        if isinstance(sv, list) and sv:
            print('    sample:', repr(sv[0])[:120])
        elif isinstance(sv, dict):
            print('    subsub:', list(sv.keys())[:10])
elif isinstance(v1, list):
    print('  len:', len(v1), 'sample:', repr(v1[0])[:120] if v1 else '')
# full count matrix
print('=== size matrix ===')
total = 0
if isinstance(sprite, dict):
    for b, bv in sprite.items():
        if isinstance(bv, dict):
            row = {}
            for ax, lv in bv.items():
                n = len(lv) if isinstance(lv, list) else (len(lv) if hasattr(lv, '__len__') else 0)
                row[ax] = n
                total += n
            print(b, row)
        elif isinstance(bv, list):
            total += len(bv)
            print(b, 'list len', len(bv))
print('sprite total lines:', total)
if isinstance(axes, dict):
    at = 0
    for a, av in axes.items():
        n = len(av) if isinstance(av, (list, dict)) else 0
        at += n
        print('axis', repr(a), n)
    print('axes total:', at)
