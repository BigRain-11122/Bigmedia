# -*- coding: utf-8 -*-
"""r1153 window 6/6 batch close accounting (declared-idle waiting state).
Updates state.json: tick 1152->1153, ts, task (first 60 chars of log line minus ts prefix),
focus, log append, watermark ts refresh (dnums/board_rows unchanged, NEW=[])."""
import json, io, datetime

ST = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json'
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

log_line = (
    now + ' R1153: declared-idle 一行声明收轮·并窗 6/6 批收 R1148-R1153（等待态：五查静 fresh 实证 r1153_all.py 22:33'
    '——orders 顶=O-20260928-1910 未变/ledger @target 41==41 零新行/decisions dnums 131==131 NEW=[]/无 index.lock/production=open'
    '——三探针持平：board 0 FAIL/readiness 3 外部 CEO 件·0 发现/loop 3 FAIL+128 WARN 既判史实·account-lag beats1156>tick1152=+4 动态史实 R981/R1054 定谳不再重复'
    '——无可领活=全 lane 时序闸：#86 三腿 supply-gated fresh 实证 pools 1440/interchat 22/CENSUS C-00030 absent'
    '·REACT v9=10-04 窗·DIGEST 10-03 已产·#94=10-04 窗·#70 OSS=10-05 21:40·#57=10-07·GB 闸=10-08·DAILY 10-03 在案·W41 提案窗=10-05 起'
    '——窗满即收：tick=1153·export 不刷（21:34 已刷 <24h·实况持平 F3 律）·commit 注区间 R1148-R1153·root 残件随窗卷入（R1119 先例）'
    '·waiting: 10-04 day-boundary trio（日清简报+REACT v9 F-151+#94 记忆窗）ETA 2026-10-04 00:0x·tokens:local=0·云计费=0'
)
focus_line = (
    'R1153: declared-idle 6/6 窗满批收 R1148-R1153（五静 fresh 实证 r1153_check.txt 22:33·三探针持平·全 lane 时序闸 10-04 日界'
    '·waiting: 10-04 day-boundary trio ETA 2026-10-04）'
)
task_line = log_line.split(' ', 2)[2][:60]

s = json.load(io.open(ST, encoding='utf-8'))
old_wm_ts = s['decisions_watermark'].get('ts')
s['tick'] = 1153
s['ts'] = now
s['task'] = task_line
s['focus'] = focus_line
s['decisions_watermark']['ts'] = now
s['log'].append(log_line)
io.open(ST, 'w', encoding='utf-8', newline='\n').write(json.dumps(s, ensure_ascii=False, indent=2) + '\n')
print('OK tick=%s ts=%s' % (s['tick'], s['ts']))
print('task=%r' % task_line)
print('wm ts: %s -> %s (dnums %d, board_rows %s)' % (old_wm_ts, now, len(s['decisions_watermark']['dnums']), s['decisions_watermark'].get('board_rows')))
print('log len=%d last=%s' % (len(s['log']), s['log'][-1][:60]))
