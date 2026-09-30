# -*- coding: utf-8 -*-
# Check watermark drift: current decisions dnum set vs stored baseline; fix export text count.
import io, json, re
from datetime import datetime

dtext = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md', encoding='utf-8').read()
dnow = sorted(set(re.findall(r'[DC]-20\d{6}-\d{2}', dtext)))
st = json.load(io.open('src/os/state.json', encoding='utf-8'))
wm = st['decisions_watermark']['dnums']
new = [d for d in dnow if d not in wm]
gone = [d for d in wm if d not in dnow]
out = ['dnow=%d wm=%d new_since_baseline=%s gone=%s' % (len(dnow), len(wm), new, gone)]
# state R749 log: what DN number did close2 record?
m = re.search(r'基线落位（(\d+) 项', st['log'][-1])
out.append('state_log_says=%s' % (m.group(1) if m else 'NOTFOUND'))

# fix export text: replace hardcoded 93 with len(wm)
E = json.load(io.open('docs/status-export.json', encoding='utf-8'))
fixed = 0
for i, row in enumerate(E['outs']):
    for j in range(len(row)):
        if isinstance(row[j], str) and '93 项基线' in row[j]:
            row[j] = row[j].replace('93 项基线', str(len(wm)) + ' 项基线')
            E['outs'][i][j] = row[j]
            fixed += 1
if fixed:
    E['export_ts'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for k, row in enumerate(E['live']):
        if isinstance(row, list) and row and '93 项基线' in row[0]:
            row[0] = row[0].replace('93 项基线', str(len(wm)) + ' 项基线')
            E['live'][k] = row
    io.open('docs/status-export.json', 'w', encoding='utf-8').write(json.dumps(E, ensure_ascii=False, indent=1) + '\n')
    out.append('export_fixed=%d' % fixed)
else:
    out.append('export_no_93_found (check manually)')
io.open('.c3-tmp/r749_wmcheck.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('OK')
