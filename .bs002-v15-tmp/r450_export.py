# -*- coding: utf-8 -*-
# R450 export: refresh status-export.json (P-61 step, live-derived fields)
import json
import datetime
from pathlib import Path

R = Path(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream')
now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '+08:00'
ep = R / 'docs' / 'status-export.json'
ex = json.loads(ep.read_text(encoding='utf-8'))
ex['export_ts'] = now

os_line = ('tick 450，R450 生产轮：#71 重制批 F-002 v15 件全链走门收官'
           '（cards-v15-matched 对位表 line_diffs=0 卡锚零动·R-E shipinhao 渲染'
           ' bs-002-v15-shipinhao 57.24s 2.8s 余量=批次① 重制带最宽·角标'
           ' BS-002 EP.02+§4.5 三开关·S2 三门全绿〔ai_feel 0/0+层 1.8 六面'
           '+spec 双 PASS〕·帧验三律 12/12+9/9+双全分辨率帧全过·ASR 终轨'
           ' 数字面值 100% 存活+真同音 7.3% 带内·E8 七席全 9.0〔S1 10/10 '
           '满分件〕·E4 参考仪 8.0 同轮回填·M4 完成态·F-002 SUPERSEDED 更账'
           '〔v2b 标历史档〕·R449 起件→R450 收官两轮链=工艺复用提速实证；'
           '余=F-003/F-004 逐件随轮继）')
for row in ex.get('outs', []):
    if isinstance(row, list) and row and 'OS' in str(row[0]):
        row[1] = os_line
for row in ex.get('results', []):
    if isinstance(row, list) and row and str(row[0]) == '449':
        row[0] = '450'
        row[1] = ('R450 实活轮：#71 F-002 v15 件全链收官（渲染腿+S2 三门+'
                  '帧验三律+ASR 终轨+E8 七席+E4 8.0 同轮回填+M4+SUPERSEDED 更账）')
    if isinstance(row, list) and row and str(row[0]) == '24':
        row[0] = '26'
        row[1] = row[1].replace('24 行', '26 行')
for d in ex.get('depts', []):
    if isinstance(d, dict) and '工程技术部' in str(d.get('n', '')):
        d['s'] = ('R450: #71 F-002 v15 full-chain close (matched cards '
                  'line_diffs=0, R-E render 57.24s 2.8s margin, S2 gates '
                  'green, frame laws pass, ASR digits 100% alive, E8 seven '
                  'seats >=9, E4 8.0 in-round backfill, M4 done, F-002 '
                  'SUPERSEDED ledgered)')

ep.write_text(json.dumps(ex, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('export_ts=%s' % ex['export_ts'])
print('results_head=%s' % str(ex['results'][0])[:90])
