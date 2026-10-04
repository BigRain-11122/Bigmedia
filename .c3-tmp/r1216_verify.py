# -*- coding: utf-8 -*-
# r1216 verify: state.json written clean (UTF-8, valid JSON, correct fields).
import json, io, datetime
P = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json'
d = json.load(io.open(P, encoding='utf-8'))
out = []
out.append('now=%s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
out.append('tick=%s' % d['tick'])
out.append('ts=%s' % d['ts'])
out.append('task=%s' % d['task'])
out.append('focus=%s' % d['focus'][:120])
out.append('log_lines=%d' % len(d['log']))
last = d['log'][-1]
out.append('LAST_LOG_HEAD=%s' % last[:100])
out.append('LAST_LOG_LEN=%d' % len(last))
out.append('production=%s' % d.get('production'))
out.append('JSON_VALID=YES')
io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1216_verify.txt','w',encoding='utf-8').write('\n'.join(out))
print('ok')
