# -*- coding: utf-8 -*-
import json, os, re, io
ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
st = json.load(open(ROOT + r'\src\os\state.json', encoding='utf-8'))
log = st.get('log', [])
o = io.open(ROOT + r'\.c3-tmp\r1418_rlogs.txt', 'w', encoding='utf-8')
for rn in ['R1298','R1299','R1300','R1301','R1302','R1304','R1306','R1307','R1308','R1309','R1310','R1311']:
    hits = [l for l in log if re.search(r'\b' + rn + r': ', l)]
    for h in hits[-1:]:
        o.write(rn + ' >> ' + h[:340] + '\n')
o.write('---QUEUE-TAIL---\n')
q = open(ROOT + r'\docs\self-improvement-queue.md', encoding='utf-8').read()
o.write('queue_len=%d chars\n' % len(q))
lines = [l for l in q.splitlines() if l.strip()]
for l in lines[-48:]:
    o.write('Q| ' + l[:200] + '\n')
o.close()
print('ok')
