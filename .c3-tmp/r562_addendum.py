# -*- coding: utf-8 -*-
# R562 addendum: record in-round operational red honestly (PS > redirect UTF-16 evidence file, R532/R536/R539/R541 in-case same type; fixed in-round via read-only re-verify UTF-8 overwrite)
import json, io, datetime

NOW = datetime.datetime.now()
LINE = (
    "2026-09-27 " + NOW.strftime('%H:%M') + " R562 轮末补记（操作红如实入账·R532/R536/R539/R541 在案同型再犯）："
    "close 件首跑输出走 PS `>` 重定向落 UTF-16 证据件（.c3-tmp/r562_verify.txt 首版）"
    "——零数据件副作用（state.json/status-export.json 由 close 件内 python json.dump 直写=UTF-8 正确·收账本体不受影响）"
    "→正法修复=r562_verify_fix.py 只读复核覆盖为 UTF-8（close 件不重跑防 log 双记·LASTLOG_COUNT_R562=1 实证单条）"
    "+防再犯注=close/verify 输出捕获一律 python 件内 io.open 写 UTF-8·PS 管道重定向对证据件永不用〔R541 正法重申〕"
)

STATE = 'src/os/state.json'
s = json.load(io.open(STATE, encoding='utf-8'))
assert s['log'][-1].startswith('2026-09-27 21:53 R562'), 'unexpected last log line'
s['log'].append(LINE)
s['ts'] = NOW.strftime('%Y-%m-%d %H:%M:%S')
json.dump(s, io.open(STATE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

s2 = json.load(io.open(STATE, encoding='utf-8'))
print('ADDENDUM_OK tick=%s log_n=%d last_head=%s' % (s2['tick'], len(s2['log']), s2['log'][-1][:44]))
print('COUNT_R562_MAIN=%d COUNT_ADDENDUM=%d' % (
    sum(1 for l in s2['log'] if l.startswith('2026-09-27 21:53 R562: ')),
    sum(1 for l in s2['log'] if 'R562 轮末补记' in l)))
print('TS=%s TASK=%s' % (s2['ts'], s2['task'][:30]))
