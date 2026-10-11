# R2010 tech#117 part2: per-bucket totals, sprite consumption, v10 match verification
import json, io, sys, os, glob, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
POOL = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json'
CARD_ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines\cards'
BUCKETS = ['morning','dusk','night','weekend','rain','typhoon','heatwave','coldsnap','market_open','market_close','ceo_order','festival']

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

def iter_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from iter_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from iter_strings(v)

cards = sorted(glob.glob(os.path.join(CARD_ROOT, 'MC-*REACT-v[0-9]*', 'cards.json')))
consumed = {}
for cpath in cards:
    cname = os.path.basename(os.path.dirname(cpath))
    cdir = os.path.dirname(cpath)
    texts = []
    cj = json.load(open(cpath, encoding='utf-8'))
    texts.extend(iter_strings(cj))
    p = os.path.join(cdir, 'subs.srt')
    if os.path.exists(p):
        texts.append(open(p, encoding='utf-8-sig').read())
    blob = norm(' '.join(texts))
    for k in pool_index:
        if k and k in blob:
            for ent in pool_index[k]:
                consumed.setdefault(ent, set()).add(cname)

# per-bucket totals + which cards used that bucket
print('=== per-bucket totals: axis-consumed/108 (6 pos x 18), sprite-consumed/12 ===')
grand_axis = 0
grand_sprite = 0
bucket_state = {}
for b in BUCKETS:
    ax_n = sum(1 for (k, a2, b2, i) in consumed if k == 'axis' and b2 == b)
    sp_n = sum(1 for (k, a2, b2, i) in consumed if k == 'sprite' and b2 == b)
    cards_b = sorted(set(c for (k, a2, b2, i), cs in consumed.items() if b2 == b for c in cs))
    grand_axis += ax_n
    grand_sprite += sp_n
    # remaining ratio over the bucket's 108 axis lines
    rem_pct = (108 - ax_n) / 108 * 100
    bucket_state[b] = (ax_n, sp_n, rem_pct, cards_b)
    print('%-13s axis %3d/108 (rem %5.1f%%)  sprite %2d/12  cards(%d)=%s' % (b, ax_n, rem_pct, sp_n, len(cards_b), [c[-3:] for c in cards_b]))
print('grand: axis %d/1296  sprite %d/144  total %d/1440' % (grand_axis, grand_sprite, grand_axis + grand_sprite))

# tri-state: per position (axis,bucket) remaining<20% => red; bucket remaining<20% => amber watch; else green
print()
print('=== tri-state warning face (position 18/18 & bucket 108/108 & sprite 12/12, <20% remaining) ===')
red = amber = 0
for b in BUCKETS:
    ax_n, sp_n, rem_pct, _ = bucket_state[b]
    bucket_level = 'RED' if rem_pct < 20 else ('AMBER' if rem_pct < 40 else 'GREEN')
    if bucket_level == 'RED': red += 1
    if bucket_level == 'AMBER': amber += 1
    print('%-13s bucket %s (axis rem %.1f%%, sprite rem %.1f%%)' % (b, bucket_level, rem_pct, (12 - sp_n) / 12 * 100))
print('RED buckets:', red, ' AMBER buckets:', amber, ' (GREEN = 12 - red - amber)')

# position-level detail (consumed>=2 positions listed)
print()
print('=== positions consumed >=2 lines (top consumers) ===')
for ax in axes.keys():
    for b in BUCKETS:
        n = sum(1 for i in range(1, 19) if ('axis', ax, b, i) in consumed)
        if n >= 2:
            cards_used = sorted(set(c for i in range(1, 19) if ('axis', ax, b, i) in consumed for c in consumed[('axis', ax, b, i)]))
            print('axis %s x %s: %d/18 consumed, rem %.0f%%, cards=%s' % (ax, b, n, (18-n)/18*100, [c[-3:] for c in cards_used]))

# v10 verification: which lines matched in v10 (7 matched - verify not false positive)
print()
print('=== v10 match verification (7 lines) ===')
cdir = os.path.join(CARD_ROOT, 'MC-20261007-REACT-v10')
texts = []
cj = json.load(open(os.path.join(cdir, 'cards.json'), encoding='utf-8'))
texts.extend(iter_strings(cj))
blob = norm(' '.join(texts))
for k, ents in pool_index.items():
    if k and k in blob:
        for (kind, ax, b, i) in ents:
            raw = ''
            if kind == 'axis':
                raw = axes[ax][b][i-1]
            else:
                raw = sprite[b][i-1]
            print('  %s %s/%s/%d: %s' % (kind, ax, b, i, raw))

# consumed line reuse (any line consumed by >1 card?)
print()
print('=== cross-card line reuse ===')
reuse = {ent: cs for ent, cs in consumed.items() if len(cs) > 1}
for ent, cs in sorted(reuse.items()):
    kind, ax, b, i = ent
    raw = axes[ax][b][i-1] if kind == 'axis' else sprite[b][i-1]
    print('  %s %s/%s/%d (%s): %s' % (kind, ax, b, i, sorted(cs), raw))
if not reuse:
    print('  (none - all consumed lines are single-use)')
