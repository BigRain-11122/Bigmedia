# R459 status-export refresh (P-61): export_ts + engineering dept + OS-loop outs + results tick row
import io, json, sys
from datetime import datetime, timezone, timedelta

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
SE = ROOT + r'\docs\status-export.json'
D_DEPT = ROOT + r'\.c3-tmp\r459_export_dept.txt'
D_OUT = ROOT + r'\.c3-tmp\r459_export_out.txt'

def rd(p):
    with io.open(p, encoding='utf-8-sig') as f:
        return f.read().strip('\n')

with io.open(SE, encoding='utf-8') as f:
    se = json.load(f)

now = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%dT%H:%M:%S+08:00')
se['export_ts'] = now

new_dept = rd(D_DEPT)
for d in se['depts']:
    if d.get('n') == '\u5de5\u7a0b\u6280\u672f\u90e8':
        d['t'] = new_dept
        d['s'] = 'R459: #74 watch-round name-off receipt (P-2026-09-25-06 dual-notation) + #70 OSS window slice 3 delivered = first window full (3 slices R432/R458/R459; libass parked, reopen pair mapped; next window after 09-29 21:40); round recovered from mid-flight interruption (R155 precedent), three knife claims re-verified'

new_out = rd(D_OUT)
os_row = se['outs'][0]
se['outs'][0] = [os_row[0], new_out, os_row[1]]

se['results'][0] = ['459',
    'R459 \u751f\u4ea7\u8f6e\uff1a\u53cc\u6d3b\u4ef6\u4ea4\u4ed8\uff08#74 \u503c\u5b88\u8f6e\u70b9\u540d\u6838\u9500\u56de\u6267=P-2026-09-25-06 \u53cc\u8bb0\u6cd5\u5e76\u5199+\u6839\u56e0\u5b9a\u8c03\u4e3a\u8ba1\u6570\u9762\u5f31\u5339\u914d\u975e\u4ea4\u4ed8\u8fdd\u7ea6+#70 OH \u9996\u7a97\u5207\u7247 3 \u4ea4\u4ed8\u6bd5=\u9996\u7a97\u4e09\u5207\u7247\u9f50\u7a97\u9762\u6ee1\uff09\u00b7\u65ad\u6d1e\u6062\u590d\u8f6e\uff08\u524d\u6267\u884c\u4f53\u4e2d\u65ad\u4e8e\u6536\u8d26\u524d\u00b7\u672c\u6267\u884c\u4f53\u4e09\u5200\u8bc1\u636e\u9010\u9879\u590d\u6838\u540e\u63a5\u624b\u8865\u9f50\uff09']

with io.open(SE, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(se, f, ensure_ascii=False, indent=1)
    f.write('\n')

with io.open(SE, encoding='utf-8') as f:
    chk = json.load(f)
print('export_ts', chk['export_ts'])
print('outs_os_len', len(chk['outs'][0]), 'ticks', [e[:8] for e in chk['outs'][0][1:]])
print('results_head', chk['results'][0][0])
print('dept_hit', any(d.get('n') == '\u5de5\u7a0b\u6280\u672f\u90e8' and 'R459' in d['t'] for d in chk['depts']))
