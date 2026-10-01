# -*- coding: utf-8 -*-
import json, io
d = json.load(io.open('docs/status-export.json', encoding='utf-8'))
out = []
out.append('live: ' + json.dumps(d.get('live'), ensure_ascii=False))
out.append('results: ' + json.dumps(d.get('results'), ensure_ascii=False)[:900])
out.append('depts(list): ' + json.dumps(d.get('depts'), ensure_ascii=False)[:900])
out.append('outs: ' + json.dumps(d.get('outs'), ensure_ascii=False)[:500])
out.append('chips: ' + json.dumps(d.get('chips'), ensure_ascii=False)[:500])
io.open('.c3-tmp/r870_export2.txt', 'w', encoding='utf-8').write('\n\n'.join(out))
print('OK')
