# -*- coding: utf-8 -*-
# r802: extract R801 log line tail (next-round pointer) + tick/ts fields
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
st = json.loads(io.open(os.path.join(ROOT, 'src', 'os', 'state.json'), 'r', encoding='utf-8-sig').read())
logs = st['log']
last = logs[-1] if logs else ''
# find the last log entry mentioning R801
r801 = [x for x in logs if x.startswith('2026-10-01 02') and 'R801' in x[:60]]
line = r801[-1] if r801 else last
out = [u'tick=%s ts=%s task=%s' % (st.get('tick'), st.get('ts'), st.get('task', '')),
       u'--- R801 full line (%d chars) ---' % len(line),
       line]
io.open(os.path.join(HERE, 'r802_r801tail.txt'), 'w', encoding='utf-8').write(u'\n'.join(out) + u'\n')
print('TAIL-OK len=%d tick=%s' % (len(line), st.get('tick')))
