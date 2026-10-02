# -*- coding: utf-8 -*-
"""R1035: pools.json expansion delta analysis - find NEW lines vs R1032-era baseline.
R1032 scan (00:52) read pool at 1440-line era; mtime now 10-03 01:06 phys 1625 lines.
We reconstruct new-line candidates: R1032 pool.txt recorded clean-row inventory at 1440 era,
but not all rows. Instead: pool.json likely has structure with version markers; check first.
"""
import io, os, json, re

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
POOL = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json'
out = io.open(os.path.join(ROOT, '.c3-tmp', 'r1035_pool_delta.txt'), 'w', encoding='utf-8')
def w(s): out.write(str(s) + '\n')

pool = json.load(io.open(POOL, encoding='utf-8'))
w('top-level keys: %s' % sorted(pool.keys()))
for k, v in sorted(pool.items()):
    if isinstance(v, dict):
        w('  %s -> sub keys: %s' % (k, sorted(v.keys())[:20]))
    elif isinstance(v, list):
        w('  %s -> list len=%d first=%r' % (k, len(v), v[0][:60] if v else None))
    else:
        w('  %s -> %r' % (k, str(v)[:100]))

AXES = [u'求新', u'怀旧', u'侠气', u'烟火', u'秩序', u'逍遥']
total = 0
counts = {}
for face in AXES + [u'sprite']:
    if face in pool.get('axes', {}):
        rows_by_bucket = pool['axes'][face]
    elif face == 'sprite' and 'sprite' in pool:
        rows_by_bucket = pool['sprite']
    else:
        w('MISSING face %s' % face); continue
    c = {bk: len(rows) for bk, rows in rows_by_bucket.items()}
    counts[face] = c
    total += sum(c.values())
    w('%s bucket counts: %s (sum=%d)' % (face, c, sum(c.values())))
w('TOTAL=%d (R1032-era baseline=1440, phys file lines=1625)' % total)
out.close()
print('ok total=%d' % total)
