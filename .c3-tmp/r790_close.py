# -*- coding: utf-8 -*-
# R790 waiting-state declaration close: tick+1, focus R791, log append, ts+task refresh
import io, json, sys

P = 'src/os/state.json'
s = io.open(P, 'r', encoding='utf-8', newline='').read()
has_bom = s.startswith(u'\ufeff')
if has_bom:
    s = s.lstrip(u'\ufeff')

LOG = (u'2026-09-30 23:08 R790: 等待态声明收轮·声明轮并窗第 3 轮（五查全静=r771_scan.py 内容寻址复跑 23:05：orders 42=锚零新令〔顶=O-20260928-1910·41 O-件+README 口径〕'
u'/ledger 六模式 41=锚带内〔last_p=P-20260925-09 值守行位移非事件·R763/R771/R789 同判〕'
u'/decisions dnum 差集 0 新行=102 基线〔D-20260930-19 水位差集制·通告板对号零新行·D-13 SLA 无触发〕'
u'/production=open 自愈核在位 tick789/无 index.lock 实核·树态三成员维持=M CODELY.md〔18:55:34 平台记忆压缩波·R767 定谳·零接触不提交不回退〕'
u'+codex 两文件〔README/city-humanities mtime 09-29 04:06:16/04:06:09 零接触未动=#86 c+d 让位判据未达·bm-a 让位〕'
u'+M state.json=声明轮并窗自账预期态+?? .c3-tmp 声明窗证据件七枚在盘〔r788/r789 批自产·窗满 batch commit 卷入=R150/R781 先例〕〕'
u'+三探针=board 0 FAIL（5 ideas 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面 0 发现（阻塞≠失败口径·68 renders 全注账）'
u'/loop_health 2 FAIL+93 WARN 皆在案史实类（09-26/09-28 outage 窗已裁定不重复触发'
u'+account-ahead tick789 vs beats786=声明轮无 beats 合法瞬态·tick790 收账自平）'
u'——可领序四项全时闸维持=GB 10-01 届日勿提前〔7 日闸防误重置·§④ 首行 2026-09-24=day6 实证·本轮 23:05 仍 09-30 无跨日〕'
u'/REACT 10-01 日报窗未落〔data/intel/daily/2026-10-01.md Test-Path False 23:03 实核·09-30 件在案〕'
u'/#70 窗 3=10-02 21:40 后开/queue §E supply-gated 豁免面维持〔新锚卡 C-00030+ 零落位+零新令级事件·R757/R763 供给实核在案禁重扫〕'
u'+W40 提案窗配额已足（P-1 pilot-closed 终判毕）+novel ch3 v4 未落盘实核（SC-001-03 止 v3·TOP1 leg① 非触发·bm-a 面）'
u'——例行件：export 18:22:40 在 24h 窗内不刷〔产品优先律 2·实况零变化〕·日报 09-30 在案不重跑〔R713〕/W40 周审在案〔R576〕'
u'/月末账 R763 收盘在案〔R-20260928-03 v1.1〕/T1 催办=已裁项停用口径/HQ-FEEDBACK 不写〔无集团层新 open 问题·dnum 差集 0 零膨胀〕'
u'·tokens:local=0（纯探针零模型调用·P-54⑤ 计量律如实记）'
u'——waiting: supply-gated lane held（卡点=新锚卡 C-00030+/新令级事件/bm-a codex 批未闭/10-01 GB+REACT 届日）ETA 2026-10-01。'
u'下轮=R791 可领序：①GB 10-01 刷新（届日领·跨日边界即收窗·#80 并窗·AIGC 标识双锚）'
u'②REACT 10-01 热点窗（10-01 日报缺=先补产 daily_brief 再领·当日一份为真相）③#86 c+d 让位判据④#70 窗 3（10-02 21:40 后开）'
u'〔并窗 4/6·窗满 6/6=R793 batch commit 区间 R788-R793·跨日先到以跨日为准〕')

prefix = u'2026-09-30 23:08 R790: '
TASK = LOG[len(prefix):][:60]

def rep(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('ANCHOR-FAIL %s count=%d' % (label, n)); sys.exit(1)
    s = s.replace(old, new, 1)
    print('OK %s' % label)

# 0. read old task from JSON for exact replacement
j0 = json.loads(s)
old_task = j0[u'task']

# 1. tick
rep(u'"tick": 789,', u'"tick": 790,', 'tick')
# 2. focus round pointer
rep(u'"focus": "R790: ', u'"focus": "R791: ', 'focus')
# 3. log append (anchor includes array close to stay unique)
anchor = u'\u3014\u5e76\u7a97 3/6\u3015"\r\n  ],'
newtail = u'\u3014\u5e76\u7a97 3/6\u3015",\r\n    "' + LOG + u'"\r\n  ],'
rep(anchor, newtail, 'log-append')
# 4. ts
rep(u'"ts": "2026-09-30 22:55:00"', u'"ts": "2026-09-30 23:08:00"', 'ts')
# 5. task
rep(u'"task": "' + old_task + u'"', u'"task": "' + TASK + u'"', 'task')

# validate JSON before write
j = json.loads(s)
assert j[u'tick'] == 790, 'tick assert fail'
assert j[u'log'][-1].startswith(u'2026-09-30 23:08 R790:'), 'log tail assert fail'
assert j[u'ts'] == u'2026-09-30 23:08:00', 'ts assert fail'
print('json-valid tick=790 log_len=%d ts=%s' % (len(j[u'log']), j[u'ts']))
print('task=%s' % j[u'task'])

out = (u'\ufeff' if has_bom else u'') + s
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('WROTE %s bytes=%d' % (P, len(out.encode('utf-8'))))
