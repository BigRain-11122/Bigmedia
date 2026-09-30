# -*- coding: utf-8 -*-
# R660 fix: restore the 659 entry's array close lost in the suffix surgery
import json, io, os

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
EP = os.path.join(ROOT, 'docs', 'status-export.json')
D = os.path.join(ROOT, '.c3-tmp', 'r660_fix_verify.txt')

raw = io.open(EP, encoding='utf-8').read()
bad = '触发律",\n  [\n   "660",'
good = '触发律"\n  ],\n  [\n   "660",'
cnt = raw.count(bad)
assert cnt == 1, f'bad pattern count={cnt}'
fixed = raw.replace(bad, good)

obj = json.loads(fixed)  # must parse
res = obj['results']
outs0 = obj['outs'][0]
d = io.open(D, 'w', encoding='utf-8')
d.write(f"results_len={len(res)}\n")
d.write(f"last={res[-1][0]} elems={len(res[-1])}\n")
d.write(f"prev={res[-2][0]} elems={len(res[-2])}\n")
d.write(f"os_head={outs0[1][:80]}\n")
d.write(f"export_ts={obj['export_ts']}\n")
io.open(EP, 'w', encoding='utf-8', newline='').write(fixed)

# re-verify from disk
obj2 = json.loads(io.open(EP, encoding='utf-8').read())
d.write(f"reparse_ok results_len={len(obj2['results'])} last={obj2['results'][-1][0]}\n")
d.write(f"prev_elems={len(obj2['results'][-2])} (must be 2)\n")
d.close()
print('done')
