# -*- coding: utf-8 -*-
"""R2066 accounting: tick 2065->2066, ts/task refresh, log append. Surgical text edit + JSON validate + atomic write."""
import io
import json
import re
import datetime

SRC = 'src/os/state.json'
c = io.open(SRC, encoding='utf-8').read()
orig_len = len(c)

now = datetime.datetime.now()
ts_full = now.strftime('%Y-%m-%d %H:%M:%S')

ENTRY = (
    '2026-10-12 18:5x R2066: 等待轮声明轮第二窗（CEO pause+workday-block 双执法窗·R2065 同型续·18:53 开轮=工作日时段非夜窗 00:00-08:00）——'
    '①轮首五查全静：own orders 顶 O-20261008-1105 mtime==R1733 锚零新令+origin_gap_check QUIET（ahead0 behind0=R2064 push 收口后净）'
    '+group_scan 六面 fresh 18:55（decisions quiet wm152 truly_new=0+ledger @BigStream 5 行==值守锚零新转办+ORDERS rows=312 tail 10-12 18:0x==水位'
    '+DIGEST-SUPPLY quiet〔v19 staged 卡覆盖〕+ORIGIN-DELTA WARN delta1 续〔15:2x 行 origin-only ~3.6h·tech#134 观察位判据 24h 窗至 10-13 18:00 维持'
    '·愈合归 FleetLink owner 域·行内容已消费零信息损失〕+MTIME 静）'
    '+树态=MV 域他窗在飞件（data/storylines/drama/mv0001 与 data/sources/mv001 族+src/os/fire_consume.py mtime 16:13=他窗 fire_consume 族·零接触 R2064 承继）'
    '+无 index.lock；'
    '②三探针带内：board 0 FAIL（5 题 10 稿 5 in production）+readiness 3 阻塞皆外部 CEO 面 0 发现（78 renders 全注账）'
    '+loop_health 3 FAIL 皆在案史实零新增面（10-12 09:59→10:57 57min 晨间窗史实已在 R2065 读数内·09-26/09-28 两旧例）+278 WARN 折叠带内；'
    '③三队盘点注记（O-20261009-1246 项 c 纯声明违例防）：P1 全 gated——main#19/20/24 三件 fire-ready〔F-180 SC-005-07 flight-4/F-181 REACT-v15/F-182 DIGEST-v19〕'
    '结转夜窗 00:00 yield-predicate-first+main#21 gated resume 令+main#22 核读毕下读 10-13 00:00 常务轮窗后+main#23 gated Phase1 窗 10-13/15；'
    'P2 tech 队全量核读=真无可执行项（本轮勘正注=首读 tech#129 行 400 字截断漏看尾注·全行复读证实 done R2051=DIGEST-SUPPLY 面交付在册·'
    '同法核 106/113/114/119 尾注证实已交付·115 观察位随 cards 收官轮并读·124 第三副本触发窗未到禁凑数律·126 gated 夜窗校准冒烟·'
    '128 观察位=main#21 承载·全队可即领标记皆挂 done 项=零可领）；'
    'P3 explore 开项全为到点执行窗（W3/W42 周扫 10-16/10-17 族+radar weekly/monthly gated+正片定版 gated+观察期 10-13/15）——真无可执行项=一行声明收轮合法；'
    '④三队补货步：真无新种子=零膨胀如实注记（五查/探针/队列全量核读零新发现·tech#134/115 在册观察位不重复立项·禁凑数律照守）；'
    '⑤export 节流=18:36:14 锚 <24h 且本轮无实况变化跳过刷新；'
    '⑥操作红 1 如实入账：probe_capture 无 --loop 参（--loop=loop_health 个件面参数·wrapper 默认紧凑面无该 flag）首调 rc2 usage·正法=默认紧凑面单命令；'
    '⑦收账步：ts+task 照刷（ts=18:58 秒级 ASCII）。'
    '下轮=夜窗 00:00 fire_consume 单命令直发 F-180（tech#121 消费序 yield-predicate-first）→F-181→F-182·main#22 复读 10-13 00:00 常务轮窗后·tech#92 判据窗 10-13 08:00（resume 时点分叉照 R2047 行）。收账显式列文件 commit+push。'
)

# task = first 60 chars of log line minus timestamp prefix
prefix_len = len('2026-10-12 18:5x R2066: ')
task_new = ENTRY[prefix_len:prefix_len + 60]

# --- 1. tick ---
assert c.count('"tick": 2065') == 1, 'tick anchor not unique'
c = c.replace('"tick": 2065', '"tick": 2066')

# --- 2. ts (top-level = the match AFTER the log array start pos 4320, i.e. near file end; watermark ts sits inside 1030..4320) ---
LOG_START = c.find('"log": [')
ts_matches = [(m.start(), m.group(1)) for m in re.finditer(r'"ts": "([^"]*)"', c)]
print('ts matches:', ts_matches)
top_ts = [(p, v) for p, v in ts_matches if p > LOG_START]
assert len(top_ts) == 1, 'top-level ts not unique: %r' % (top_ts,)
pos, old_ts = top_ts[0]
print('top-level ts: %r -> %r' % (old_ts, ts_full))
c = c[:pos] + '"ts": "%s"' % ts_full + c[pos + len('"ts": "%s"' % old_ts):]

# --- 3. task (top-level, same rule: after log array start) ---
task_matches = [(m.start(), m.group(1)) for m in re.finditer(r'"task": "([^"]*)"', c)]
print('task matches:', [(p, v[:40]) for p, v in task_matches])
top_task = [(p, v) for p, v in task_matches if p > LOG_START]
assert len(top_task) == 1, 'top-level task not unique: %r' % (top_task[:2],)
pos, old_task = top_task[0]
print('top-level task: %r... -> %r...' % (old_task[:30], task_new[:30]))
c = c[:pos] + '"task": "%s"' % task_new + c[pos + len('"task": "%s"' % old_task):]

# --- 4. log append after R2065 entry ---
anchor = '"2026-10-12 18:4x R2065: '
assert c.count(anchor) == 1, 'R2065 entry anchor not unique (%d)' % c.count(anchor)
i = c.find(anchor)
j = i + len(anchor)
while True:
    j = c.find('"', j)
    assert j != -1, 'no closing quote for R2065 entry'
    if c[j - 1] != '\\':
        break
    j += 1
insert_at = j + 1
print('log insert at %d, following context: %r' % (insert_at, c[insert_at:insert_at + 30]))
c = c[:insert_at] + ',\n  "' + ENTRY + '"' + c[insert_at:]

# --- 5. validate ---
json.loads(c)
print('JSON valid. len %d -> %d (+%d)' % (orig_len, len(c), len(c) - orig_len))

# --- 6. atomic write ---
tmp = SRC + '.r2066.tmp'
io.open(tmp, 'w', encoding='utf-8', newline='').write(c)
import os
os.replace(tmp, SRC)
print('written:', SRC)
print('TASK_FIELD:', task_new)
