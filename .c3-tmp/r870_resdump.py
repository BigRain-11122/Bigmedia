# -*- coding: utf-8 -*-
import json, io
d = json.load(io.open('docs/status-export.json', encoding='utf-8'))
res = d.get('results', [])
out = []
out.append('results count=%d' % len(res))
for r in res:
    head = r[1][:26] if isinstance(r, list) and len(r) > 1 else str(r)[:30]
    out.append('  %s | %s' % (r[0], head))
io.open('.c3-tmp/r870_results.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('OK count=%d' % len(res))
