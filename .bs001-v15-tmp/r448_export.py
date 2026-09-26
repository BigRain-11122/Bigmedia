# -*- coding: utf-8 -*-
# R448 export: refresh status-export.json (P-61 step, live-derived fields)
import json
import datetime
from pathlib import Path

R = Path(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream')
now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '+08:00'
ep = R / 'docs' / 'status-export.json'
ex = json.loads(ep.read_text(encoding='utf-8'))
ex['export_ts'] = now

os_line = ('tick 448，R448 生产轮：#71 重制批 F-001 v15 件全链走门收官'
           '（S2 席 ASR 终轨=数字面值 100% 存活+自动醒释义位净读+字位 9.1% 系列带'
           '·E8 评审单七席 ≥9·M4 完成态·F-001 SUPERSEDED 更账 v14b→v15·'
           'E4 参考仪在飞回填=下轮·F-002~F-004 逐件随轮继）')
for row in ex.get('outs', []):
    if isinstance(row, list) and row and 'OS' in str(row[0]):
        row[1] = os_line
for row in ex.get('results', []):
    if isinstance(row, list) and row and str(row[0]) == '447':
        row[0] = '448'
        row[1] = ('R448 实活轮：#71 F-001 v15 终审链（ASR 终轨+E8 七席+M4+SUPERSEDED 更账毕）')
for d in ex.get('depts', []):
    if isinstance(d, dict) and 'OS' in str(d.get('n', '')):
        d['s'] = ('R448: #71 F-001 v15 piece closed (ASR final-track 9.0, '
                  'E8 seven seats >=9, M4 done, SUPERSEDED v14b->v15)')
    if isinstance(d, dict) and '工程技术部' in str(d.get('n', '')):
        d['s'] = ('R448: ASR final-track QC (medium-int8 beam5 noctx) + diff '
                  'quantifier; readiness v15 row label aligned to batch mark '
                  '(0 findings); three probes run')

ep.write_text(json.dumps(ex, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('export_ts=%s' % ex['export_ts'])
print('results_head=%s' % str(ex['results'][0])[:90])
