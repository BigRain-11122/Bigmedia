# -*- coding: utf-8 -*-
# R447 export: refresh status-export.json (P-61 step, live-derived fields)
import json
import datetime
from pathlib import Path

R = Path(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream')
now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '+08:00'
ep = R / 'docs' / 'status-export.json'
ex = json.loads(ep.read_text(encoding='utf-8'))
ex['export_ts'] = now

os_line = ('tick 447，R447 生产轮：#71 重制腿③ F-001 渲染腿毕'
           '（edit_craft 七参接线 291 回归绿·cards-v15-matched 对位·R-E 渲染'
           ' bs-001-v15-shipinhao 58.66s 角标+三开关首用·S2 三门全绿·'
           '帧验三律 12/12+12/12 全净·E8/M4/F-001 更账=R448）')
for row in ex.get('outs', []):
    if isinstance(row, list) and row and 'OS' in str(row[0]):
        row[1] = os_line
for row in ex.get('results', []):
    if isinstance(row, list) and row and str(row[0]) == '446':
        row[0] = '447'
        row[1] = ('R447 实活轮：#71 F-001 渲染腿（R-E 接线+对位+渲染+S2 三门+帧验三律全过）')
for d in ex.get('depts', []):
    if isinstance(d, dict) and 'OS' in str(d.get('n', '')):
        d['s'] = ('R447: #71 F-001 render leg done (S2 three gates green, '
                  'frame verify 24/24, E8/M4 next)')
    if isinstance(d, dict) and '工程技术部' in str(d.get('n', '')):
        d['s'] = ('R447: edit_craft series/cyber 7-flag wiring (291 regression '
                  'green); v15 matched cards; R-E render + S2 gates green')

ep.write_text(json.dumps(ex, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('export_ts=%s' % ex['export_ts'])
print('results_head=%s' % str(ex['results'][0])[:90])
