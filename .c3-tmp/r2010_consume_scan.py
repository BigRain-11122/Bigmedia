# R2010 tech#117: full consumption scan - all 1440 pool lines x 15 REACT cards verbatim match
import json, io, sys, os, glob, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
POOL = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json'
CARD_ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines\cards'
BUCKETS = ['morning','dusk','night','weekend','rain','typhoon','heatwave','coldsnap','market_open','market_close','ceo_order','festival']

d = json.load(open(POOL, encoding='utf-8'))
axes, sprite = d['axes'], d['sprite']

# flatten pool: key = normalized line, value = list of (axis, bucket, idx)
def norm(s):
    return re.sub(r'[\s，。、；：？！「」『』（）——…·,.!?;:\'"~]', '', s)

pool_index = {}  # norm -> [(kind, axis, bucket, idx_1based)]
for ax, bv in axes.items():
    for b, lines in bv.items():
        for i, ln in enumerate(lines, 1):
            pool_index.setdefault(norm(ln), []).append(('axis', ax, b, i))
for b, lines in sprite.items():
    for i, ln in enumerate(lines, 1):
        pool_index.setdefault(norm(ln), []).append(('sprite', '-', b, i))
total_lines = sum(len(v) for v in pool_index.values())
print('pool unique normalized lines:', len(pool_index), 'total entries:', total_lines)

# collect all strings from each card (cards.json full + m1-assert + subs.srt)
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
consumed = {}  # (kind, axis, bucket, idx) -> set of card names
norm_pool_keys = set(pool_index.keys())
for cpath in cards:
    cname = os.path.basename(os.path.dirname(cpath))
    cdir = os.path.dirname(cpath)
    texts = []
    cj = json.load(open(cpath, encoding='utf-8'))
    texts.extend(iter_strings(cj))
    for extra in ('subs.srt',):
        p = os.path.join(cdir, extra)
        if os.path.exists(p):
            texts.append(open(p, encoding='utf-8-sig').read())
    m1 = os.path.join(cdir, 'm1-assert-*.txt')
    for m in glob.glob(m1):
        texts.append(open(m, encoding='utf-8', errors='replace').read())
    blob = norm(' '.join(texts))
    # sliding window match: for each pool line, check normalized containment
    used = 0
    for k in norm_pool_keys:
        if k and k in blob:
            for ent in pool_index[k]:
                consumed.setdefault(ent, set()).add(cname)
            used += 1
    print('%s: matched %d pool lines' % (cname, used))

# matrix: per (axis,bucket) consumed count of 18; per bucket sprite consumed of 12
print()
print('=== consumption matrix (axis x bucket: consumed/18) ===')
hdr = '%-6s ' % 'axis' + ' '.join('%13s' % b[:7] for b in BUCKETS)
print(hdr)
agg_bucket = {b: [0, 0] for b in BUCKETS}  # [axis_consumed, sprite_consumed]
for ax in axes.keys():
    row = []
    for b in BUCKETS:
        n = sum(1 for i in range(1, 19) if ('axis', ax, b, i) in consumed)
        row.append(n)
        agg_bucket[b][0] += n
    print('%-6s ' % ax + ' '.join('%13d' % n for n in row))
print()
print('=== per-bucket totals: axis-consumed/108, sprite-consumed/12 ===')
for b in BUCKETS:
    sp = sum(1 for i in range(1, 13) if ('sprite', '-', b, i) in consumed)
    print('%-13s axis %3d/108  sprite %2d/12  cards=%s' % (b, agg_bucket[b][0], sp, sorted(set(os.path.basename(os.path.dirname(c)) for ent in consumed for os_ in [1] if ent[2]==b and any(ent in consumed)))))
total_consumed = len(consumed)
print()
print('total consumed lines (unique entries):', total_consumed, '/', 1440)
# remaining per position
print()
print('=== per-position remaining <20% (consumed >=15/18) tri-state ===')
warn = 0
for (kind, ax, b, i), cards_used in sorted(consumed.items()):
    cap = 18 if kind == 'axis' else 12
    # individual position consumption is 1 max per line; tri-state is at position level
# position-level: consumed count per (axis,bucket)
for ax in axes.keys():
    for b in BUCKETS:
        n = sum(1 for i in range(1, 19) if ('axis', ax, b, i) in consumed)
        if n > 0:
            print('axis %s x %s: %d/18 consumed, remaining %d (%.0f%%)' % (ax, b, n, 18-n, (18-n)/18*100))
for b in BUCKETS:
    n = sum(1 for i in range(1, 13) if ('sprite', '-', b, i) in consumed)
    if n > 0:
        print('sprite x %s: %d/12 consumed, remaining %d (%.0f%%)' % (b, n, 12-n, (12-n)/12*100))
