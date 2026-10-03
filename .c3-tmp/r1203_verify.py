# -*- coding: utf-8 -*-
# r1203 verify: read state.json tail with explicit UTF-8, write verify output as UTF-8 file (PS5.1 console redirect GBK trap avoidance).
import json, io

P = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json'
d = json.load(io.open(P, encoding='utf-8'))

out = []
out.append('tick=%s ts=%s' % (d.get('tick'), d.get('ts')))
out.append('task=%s' % d.get('task'))
last = d.get('log', [])[-1]
out.append('log[-1] len=%d' % len(last))
out.append('log[-1][:200]=%s' % last[:200])
out.append('log[-1][-200:]=%s' % last[-200:])
out.append('log_lines=%d' % len(d.get('log', [])))
out.append('production=%s' % d.get('production'))
out.append('decisions_watermark dnums=%d' % len(d.get('decisions_watermark', {}).get('dnums', [])))
out.append('focus=%s' % d.get('focus', '')[:120])

io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1203_verify2.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('ok')
