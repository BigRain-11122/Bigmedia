# R2010 tech#117: full 72-position line-count matrix + locate REACT consumption records
import json, io, sys, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json'
d = json.load(open(p, encoding='utf-8'))
axes = d['axes']
print('=== 72-position matrix (axis x bucket -> line count) ===')
buckets = ['morning','dusk','night','weekend','rain','typhoon','heatwave','coldsnap','market_open','market_close','ceo_order','festival']
print('axis      ' + ' '.join('%13s' % b for b in buckets))
total = 0
counts = {}
for ax, bv in axes.items():
    row = []
    for b in buckets:
        n = len(bv.get(b, []))
        counts[(ax, b)] = n
        total += n
        row.append(n)
    print('%-8s ' % ax + ' '.join('%13d' % n for n in row))
print('TOTAL lines in 72 positions:', total)
print('positions with 0 lines:', sum(1 for v in counts.values() if v == 0))
print('min/max per position:', min(counts.values()), max(counts.values()))

# REACT card dirs in BigStream
root = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
card_root = os.path.join(root, 'data', 'storylines', 'cards')
react_dirs = sorted(glob.glob(os.path.join(card_root, 'MC-*REACT*')))
print()
print('=== REACT card dirs (%d) ===' % len(react_dirs))
for rd in react_dirs:
    print(os.path.basename(rd))
    for f in sorted(os.listdir(rd)):
        print('   ', f)
