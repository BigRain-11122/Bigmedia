r"""Verify r1194 state close wrote clean UTF-8 (console display is GBK-lossy; file is truth)."""
import json, io

P = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json'
d = json.load(io.open(P, encoding='utf-8'))
out = []
out.append('tick=%s' % d['tick'])
out.append('ts=%s' % d['ts'])
out.append('task=%s' % d['task'])
out.append('production=%s' % d.get('production'))
last = d['log'][-1]
out.append('LASTLOG_LEN=%d' % len(last))
out.append('LASTLOG_HEAD=%s' % last[:80])
out.append('LASTLOG_TAIL=%s' % last[-160:])
out.append('LOG_LEN=%d' % len(d['log']))
io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1194_verify.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('ok')
