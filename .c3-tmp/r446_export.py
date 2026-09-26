# -*- coding: utf-8 -*-
# R446 export-fix: status-export.json actual structure (lists of lists/dicts n-t-s)
import json
import datetime
from pathlib import Path

R = Path(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream')
now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '+08:00'
ep = R / 'docs' / 'status-export.json'
ex = json.loads(ep.read_text(encoding='utf-8'))
ex['export_ts'] = now

os_line = ('tick 446，R446 生产轮：#71 重制腿③ F-001 首件起件三腿毕'
           '（v15 拍稿重走 M1 全绿 0 FAIL 0 WARN·空气预算 58.66s 入窗 1.3s 余量'
           '·S1 v1.5+L18-L20 门 1500s 脱壳在飞）')
for row in ex.get('outs', []):
    if isinstance(row, list) and row and 'OS' in str(row[0]):
        row[1] = os_line
for row in ex.get('results', []):
    if isinstance(row, list) and row and str(row[0]) == '445':
        row[0] = '446'
        row[1] = ('R446 实活轮：#71 F-001 两律重制起件（拍稿/M1 机检/空气预算/S1 起飞）')
for d in ex.get('depts', []):
    if isinstance(d, dict) and 'OS' in str(d.get('n', '')):
        d['s'] = 'R446: #71 F-001 remake piece started (beats v15 + S1 in flight)'

ep.write_text(json.dumps(ex, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('export_ts=%s' % ex['export_ts'])
print('outs_os=%s' % [r for r in ex['outs'] if isinstance(r, list) and r and 'OS' in str(r[0])][0][1][:60])
print('results_head=%s' % str(ex['results'][0])[:90])
