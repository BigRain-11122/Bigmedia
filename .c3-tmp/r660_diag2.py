# -*- coding: utf-8 -*-
import json, io, os

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
d = io.open(os.path.join(ROOT, '.c3-tmp', 'r660_diag2.txt'), 'w', encoding='utf-8')

for name in ['src/os/state.json', 'docs/status-export.json']:
    p = os.path.join(ROOT, name)
    raw = io.open(p, encoding='utf-8').read()
    lines = raw.split('\n')
    d.write(f"=== {name}: chars={len(raw)} lines={len(lines)}\n")
    try:
        obj = json.loads(raw)
        d.write("  JSON OK\n")
    except json.JSONDecodeError as e:
        d.write(f"  JSON ERROR: {e}\n")
        # show context around error
        ln = e.lineno
        for i in range(max(0, ln - 6), min(len(lines), ln + 2)):
            tag = '>>' if (i + 1) == ln else '  '
            d.write(f"  {tag}L{i+1}: {lines[i][:120]}\n")
    d.write("  [tail 14 lines]\n")
    for i, l in enumerate(lines[-14:]):
        d.write(f"  T{i}: {l[:120]}\n")
d.close()
print('done')
