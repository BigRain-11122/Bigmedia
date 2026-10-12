# -*- coding: utf-8 -*-
# r2039_close.py -- R2039 production close: tech#92 re-judge-window precheck done.
# R2038 next-step pointer fulfilled: score/structure receipt re-verify.
# Reading (r2039_t92_readout.json): worker 4576 confirmed live (receipts max
# 08:30:54 fresh, api /api/health ok, fetch 73 runs since 06:00 -> supply
# fresh); analyze queue moving (completed 6529->6577, active 6, created 1103);
# BUT score/structure completion flow = 0 since restart -- all 44 receipts
# qwen2.5:14b-8k/unknown = 120s-cap contention family (MV sprint GPU ~98%
# = CEO priority side, correct yield). So calibration-effect verification and
# window accumulation both depend on night-window scoring quiet periods.
# stale_active_pre_restart=6 unchanged (maintenance reclaim pending).
# Accumulation: nonbf scored total 1486 / ge60=11 cumulative (82/75/75/66 old
# anchors); city ceiling band unchanged (bili-tech 60 / knowledge 59 /
# zhihu-hot 59). failed pool 676->803 contention growth (no re-requeue per
# R1800); new pool 494->1118 (interval 15/21/15/33 non-persisted regression
# face still open). Re-judge window 10-13 08:00 per pre-registered judgment.
# Night-window seed #126 added to tech queue. fire no-fire rc1 mv-active #15.
import io, json, datetime, sys, os, subprocess

P = 'src/os/state.json'
raw = io.open(P, 'rb').read()
has_bom = raw.startswith(b'\xef\xbb\xbf')
txt = raw.decode('utf-8-sig')
nl = '\r\n' if '\r\n' in txt else '\n'
lines = txt.split(nl)

idx_close = idx_ts = idx_task = None
for i in range(len(lines) - 1, max(len(lines) - 40, 0), -1):
    st = lines[i].strip()
    if st == '],':
        idx_close = i
    elif st.startswith('"ts":') and idx_ts is None:
        idx_ts = i
    elif st.startswith('"task":') and idx_task is None:
        idx_task = i
assert idx_close is not None and idx_ts == idx_close + 1 and idx_task == idx_close + 2, \
    (idx_close, idx_ts, idx_task)
assert lines[idx_ts].strip() == '"ts": "2026-10-12 08:25:22",', lines[idx_ts]

LOG = (
    '  "2026-10-12 08:4x R2039: 生产轮·tech#92 重判窗前置位复验毕（R2038 下步指针兑现·score/structure 回执面定谳）'
    '——①轮首五查全静（own orders 顶 O-20260908-1105 mtime==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0〔R1500 前置位〕'
    '+group_scan 四面全静〔decisions truly_new=0 水位 150 维持·D-20261012-01/02 属水位内默认·ledger @BigStream 5 行==值锚静默转辙'
    '·ORDERS quiet rows=270 tail_key=\'10-11 13:4x\'==R1979 基线〕+树态=MV sprint 会话域在飞采集件〔R1745 承继·mv0001/mv001 前缀族〕+零 index.lock；'
    '②三探针=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面 0 发现（78 renders unannot=0）'
    '/loop_health 2F+267W 皆在案史实带内（两 outage 已裁定不重触发·drift 18≤基线 21）；'
    '③tech#92 重判窗前置位复验（本轮主活·.c3-tmp/r2039_t92_prewindow.py psql 通道=r2039_t92_readout.json）'
    '=worker 4576 激活确认（receipts max 08:30:54 分钟级真负载+api /api/health {ok,db:ok,ms:1}'
    '+fetch 73 笔/06:00 起活到 08:32:38=供给面新鲜）+队列复动续证（content.analyze completed 6529→6577·active 6·created 1103）'
    '——**真发现=score/structure 完成流=0**：重启后 44 笔 receipts 全=qwen2.5:14b-8k/unknown'
    '（120s 帽争抢族·MV sprint GPU 满载=CEO 优先侧正确让路）→零 completed 评分回执'
    '=校准生效验证与 10-13 08:00 窗内积累双依赖夜窗评分静默期；stale active pre-restart=6 维持（maintenance 回收待）；'
    '积累面=nonbf scored 总 1486/ge60=11（累计口径·含 82/75/75/66 旧锚）·城市源天花板带维持'
    '（bilibili-tech 60/knowledge 59/zhihu-hot 59）→重判窗照预注册判据读数'
    '（zhihu-hot 头部 ≥3 篇 ≥60=文本腿收口 tech#92/FAIL=阈值分层 fallback 腿 T1 60→55）；'
    'failed 池 676→803（争抢族增长·不 re-requeue 维持 R1800 先例）+new 池 494→1118'
    '（interval 15/21/15/33 未持久化回归面维持开放）；'
    '④fire 消费序律=fire_consume verbatim 直发=no-fire rc1（reason=card-no-fire: mv-active=MV sprint 会话活跃让路正确侧'
    '·no-fire 序列第 15 数据点·ledger 行落账）；'
    '⑤队列补货步=真种子一条入 tech 队（#126 夜窗校准冒烟+城市源 failed 池夜窗重排=重判窗前置证据面·本轮争抢族实锚承接）；'
    '⑥例行件=日报 10-12 在案不重跑（Test-Path 实证）+W42 周审在案+global-benchmarks 下期 10-15≤7d 跳过'
    '+T1 催办线无超 48h 新项+HQ-FEEDBACK 不写（无集团层新 open 问题·零膨胀）'
    '+tokens:local=0（纯进程/DB 读数探针零本地模型调用·P-54⑤ 计量律如实记）；'
    '临时件清理钩=r2039 探针三件入账收口（readout 证据件 tech#92/backlog 引用·盘上留档）'
    '——下轮=R2040 轮首 fire_consume 直发维持（GO=F-180 flight-4 派发→S1 判词→F-180 登记·F-181 后段位）'
    '+tech#126 夜窗腿（夜窗实测前置）+tech#92 判据窗 10-13 08:00 重判读数。收账显式列文件 commit+push。"'
)

prev = lines[idx_close - 1]
assert prev.strip().startswith('"2026-10-12 08:3x R2038:'), prev[:60]
if not prev.rstrip().endswith(','):
    lines[idx_close - 1] = prev + ','
assert not LOG.rstrip().endswith(','), 'LOG must be last element without trailing comma'

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
TASK = (' "task": "生产轮·tech#92 重判窗前置位复验毕（score/structure 完成流=0 争抢族·校准验证依赖夜窗）'
        '+夜窗冒烟种子入队",')

lines.insert(idx_close, LOG)
lines[idx_ts + 1] = ' "ts": "%s",' % now
lines[idx_task + 1] = TASK

out = nl.join(lines)
assert out.count('"tick": 2038,') == 1
out = out.replace('"tick": 2038,', '"tick": 2039,')

old_focus_tail = ('+\u8bc4\u6bb5\u6062\u590d\u590d\u9a8c\uff08score/structure \u56de\u6267\u9762+6 \u65e7 stale active \u56de\u6536\u6001\uff09'
                  '+tech#92 \u5224\u636e\u7a97 10-13 08:00 \u91cd\u5224\uff08zhihu-hot \u5934\u90e8 \u22653 \u4ef6 \u226560='
                  '\u6587\u672c\u817f\u6536\u53e3\u00b7FAIL=\u9608\u503c\u5206\u5c42\u817f\u9012\u8865\uff09')
new_focus_tail = ('+tech#126 \u591c\u7a97\u6821\u51c6\u5192\u70df\u817f\uff08\u57ce\u5e02\u6e90 failed \u6c60\u591c\u7a97\u91cd\u6392'
                  '\u00b7\u91cd\u5224\u7a97\u524d\u7f6e\u8bc1\u636e\u9762\u00b7\u591c\u7a97\u5b9e\u6d4b\u524d\u7f6e\uff09'
                  '+tech#92 \u5224\u636e\u7a97 10-13 08:00 \u91cd\u5224\u8bfb\u6570\uff08zhihu-hot \u5934\u90e8 \u22653 \u4ef6 \u226560='
                  '\u6587\u672c\u817f\u6536\u53e3\u00b7FAIL=\u9608\u503c\u5206\u5c42\u817f\u9012\u8865\uff09')
cnt = out.count(old_focus_tail)
assert cnt == 2, 'focus tail count=%d (expect focus field + R2038 log history)' % cnt
out = out.replace(old_focus_tail, new_focus_tail, 1)  # first occurrence only = focus field

json.loads(out)  # validity gate

data = out.encode('utf-8')
if has_bom:
    data = b'\xef\xbb\xbf' + data
io.open(P, 'wb').write(data)
print('r2039 state OK: tick=2039 ts=%s bom=%s nl=%r json=valid' % (now, has_bom, nl))

# --- tech.md: tech#92 R2039 precheck note (inline append after R2038 note tail anchor) ---
tp = 'state/queue/tech.md'
t = io.open(tp, encoding='utf-8').read()
anchor = '\u56de\u6267\u590d\u9a8c=\u4e0b\u8f6e\u4f4d\uff08\u91cd\u5224\u7a97\u524d\u7f6e\uff09'  # 回执复验=下轮位（重判窗前置）
assert t.count(anchor) == 1, 'tech#92 R2038 note-tail anchor count=%d' % t.count(anchor)
note = (
    ' **[R2039 \u524d\u7f6e\u4f4d\u590d\u9a8c\u6bd5 2026-10-12]**\uff08\u8bc1\u636e .c3-tmp/r2039_t92_readout.json\uff09'
    '\uff1a\u2460worker 4576 \u6fc0\u6d3b\u786e\u8ba4\uff08receipts max 08:30:54 \u5206\u949f\u7ea7\u771f\u8d1f\u8f7d'
    '+api health ok+fetch \u4f9b\u7ed9\u9762\u65b0\u9c9c\uff09\uff1b\u2461**\u771f\u53d1\u73b0=score/structure \u5b8c\u6210\u6d41=0**'
    '\uff1a\u91cd\u542f\u540e 44 \u7b14 receipts \u5168=qwen2.5:14b-8k/unknown\uff08120s \u5e3d\u4e89\u62a2\u65cf\u00b7MV sprint GPU \u6ee1\u8f7d'
    '=CEO \u4f18\u5148\u4fa7\u8ba9\u8def\uff09\u2192\u96f6 completed \u8bc4\u5206\u56de\u6267=\u6821\u51c6\u751f\u6548\u9a8c\u8bc1\u4e0e\u7a97\u5185\u79ef\u7d2f'
    '\u53cc\u4f9d\u8d56\u591c\u7a97\u8bc4\u5206\u9759\u9ed8\u671f\uff1b\u2462\u961f\u5217\u590d\u52a8\u7eed\u8bc1\uff08analyze completed 6529\u21926577'
    '\u00b7active 6\u00b7created 1103\uff09+stale active=6 \u7ef4\u6301\uff1b\u2463\u79ef\u7d2f\u9762=nonbf \u603b 1486/ge60=11\uff08\u7d2f\u8ba1\u53e3\u5f84\uff09'
    '\u00b7\u57ce\u5e02\u6e90\u5929\u82b1\u677f\u5e26\u7ef4\u6301\uff08tech 60/knowledge 59/zhihu-hot 59\uff09'
    '\uff1b\u2464failed \u6c60 676\u2192803\uff08\u4e89\u62a2\u65cf\u589e\u957f\u00b7\u4e0d re-requeue \u7ef4\u6301 R1800\uff09'
    '\u2014\u2014**\u591c\u7a97\u817f\u7701 #126 \u5165\u961f\uff08\u91cd\u5224\u7a97\u524d\u7f6e\u8bc1\u636e\u9762\u627f\u63a5\uff09**'
)
t = t.replace(anchor, anchor + note)

# --- tech.md: append seed #126 ---
assert t.rstrip().endswith('\u3002') or True
seed = (
    '\n126. [R2039 \u65b0\u79cd\u5b50\u00b7tech#92 \u91cd\u5224\u7a97\u524d\u7f6e\u771f\u53d1\u73b0\u627f\u63a5] '
    '**\u591c\u7a97\u6821\u51c6\u5192\u70df+\u57ce\u5e02\u6e90 failed \u6c60\u591c\u7a97\u91cd\u6392**'
    '\uff08\u5224\u636e\u7a97 10-13 08:00 \u524d\u7f6e\u8bc1\u636e\u9762\uff09\u2014\u2014'
    'R2039 \u590d\u9a8c\u5b9a\u8c2d\uff1aworker 4576 \u6fc0\u6d3b\u786e\u8ba4\u4f46\u91cd\u542f\u540e 44 \u7b14 receipts '
    '\u5168=qwen2.5:14b-8k/unknown\uff08120s \u5e3d\u4e89\u62a2\u65cf\u00b7MV sprint GPU \u6ee1\u8f7d CEO \u4f18\u5148\u4fa7\u8ba9\u8def\uff09'
    '\u2192score/structure \u5b8c\u6210\u6d41=0=\u6821\u51c6\u751f\u6548\u9a8c\u8bc1\u4e0e\u7a97\u5185\u79ef\u7d2f\u53cc\u4f9d\u8d56'
    '\u591c\u7a97\u8bc4\u5206\u9759\u9ed8\u671f\uff1b\u672c\u9879=\u591c\u7a97\uff08fire \u5361 GO \u6216 util<60 \u5b9e\u6d4b\u524d\u7f6e\uff09'
    '\u6267\u884c admin requeueFailed\uff08\u9650\u57ce\u5e02\u6e90\u4e09\u6e90 failed \u6c60\u00b7R1876 admin API \u6b63\u6cd5\u590d\u7528\uff09'
    '+\u6b21\u65e5\u7a97\u524d\u62bd\u8bfb selection-score completed \u56de\u6267 \u22653 \u7b14\u4e0e\u57ce\u5e02\u6e90\u65b0\u8bc4\u5206 '
    '\u226560 \u51fa\u73b0\u7387\uff08\u951a\u4f8b\u6ce8\u5165\u751f\u6548\u5192\u70df\u8bc1\u636e\u9762\uff09\uff1b\u7a97\u8bfb\u6570\u7167'
    '\u9884\u6ce8\u518c\u5224\u636e\uff08zhihu-hot \u5934\u90e8 \u22653 \u7bc7 \u226560=PASS \u6587\u672c\u817f\u6536\u53e3 tech#92'
    '/\u5426\u5219\u9608\u503c\u5206\u5c42 fallback \u817f T1 60\u219255\uff09\uff1b\u5224\u8d1f\u7559\u75d5\u5408\u6cd5='
    '\u591c\u7a97\u91cd\u6392\u540e\u4ecd 0 \u5b8c\u6210=\u4e89\u62a2\u65cf\u786e\u5b9a\u6027\u5224\u5b9a\u7ef4\u6301\uff08R1800 \u5148\u4f8b\uff09'
    '\u2014\u2014\u6309\u8ba4\u9886\u5236\u968f\u8f6e\u9886\u505a'
)
t = t.rstrip() + '\n' + seed.strip() + '\n'
io.open(tp, 'w', encoding='utf-8', newline='').write(t)
print('tech.md tech#92 R2039 note + seed #126 appended')

# --- backlog #112 R2039 note ---
bp = 'src/os/backlog.md'
b = io.open(bp, encoding='utf-8').read()
b_anchor = '\u2014\u2014\u76d8\u9762 15:07 \u590d\u6d4b\u8bfb\u7ef4\u6301\u3002'  # ——盘面 15:07 复测读维持。
assert b.count(b_anchor) == 1, 'backlog #112 R2038 tail anchor count=%d' % b.count(b_anchor)
b_note = (
    '\n   **[R2039 \u524d\u7f6e\u590d\u9a8c 2026-10-12]**\uff1atech#92 \u91cd\u5224\u7a97\u524d\u7f6e\u590d\u9a8c\u6bd5'
    '\uff08R2038 \u4e0b\u6b65\u6307\u9488\u5151\u73b0\u00b7\u8bc1\u636e .c3-tmp/r2039_t92_readout.json\uff09'
    '\u2014\u2014\u2460worker 4576 \u6fc0\u6d3b\u786e\u8ba4\uff08receipts max 08:30:54 \u5206\u949f\u7ea7\u771f\u8d1f\u8f7d'
    '+api /api/health {ok,db:ok,ms:1}+fetch 73 \u7b14/06:00 \u8d77\u6d3b\u5230 08:32:38=\u4f9b\u7ed9\u9762\u65b0\u9c9c\uff09'
    '+\u961f\u5217\u590d\u52a8\u7eed\u8bc1\uff08content.analyze completed 6529\u21926577\u00b7active 6\u00b7created 1103\uff09\uff1b'
    '\u2461**\u771f\u53d1\u73b0=score/structure \u5b8c\u6210\u6d41=0**\uff1a\u91cd\u542f\u540e 44 \u7b14 receipts '
    '\u5168=qwen2.5:14b-8k/unknown\uff08120s \u5e3d\u4e89\u62a2\u65cf\u00b7MV sprint GPU \u6ee1\u8f7d=CEO \u4f18\u5148\u4fa7'
    '\u6b63\u786e\u8ba9\u8def\uff09\u2192\u96f6 completed \u8bc4\u5206\u56de\u6267=\u6821\u51c6\u751f\u6548\u9a8c\u8bc1\u4e0e'
    ' 10-13 08:00 \u7a97\u5185\u79ef\u7d2f\u53cc\u4f9d\u8d56\u591c\u7a97\u8bc4\u5206\u9759\u9ed8\u671f\uff1b'
    '\u2462stale active pre-restart=6 \u7ef4\u6301\uff08maintenance \u56de\u6536\u5f85\uff09\uff1b\u79ef\u7d2f\u9762='
    'nonbf scored \u603b 1486/ge60=11\uff08\u7d2f\u8ba1\u53e3\u5f84\u00b7\u542b 82/75/75/66 \u65e7\u951a\uff09'
    '\u00b7\u57ce\u5e02\u6e90\u5929\u82b1\u677f\u5e26\u7ef4\u6301\uff08bilibili-tech 60/knowledge 59/zhihu-hot 59\uff09'
    '\u2192\u91cd\u5224\u7a97\u7167\u9884\u6ce8\u518c\u5224\u636e\u8bfb\u6570\uff1b\u2463failed \u6c60 676\u2192803'
    '\uff08\u4e89\u62a2\u65cf\u589e\u957f\u00b7\u4e0d re-requeue \u7ef4\u6301 R1800 \u5148\u4f8b\uff09+new \u6c60 494\u21921118'
    '\uff08interval \u672a\u6301\u4e45\u5316\u56de\u5f52\u9762\u7ef4\u6301\u5f00\u653e\uff09\u2014\u2014'
    '**\u591c\u7a97\u817f #126 \u5165 tech \u961f\uff08\u591c\u7a97\u91cd\u6392+\u6821\u51c6\u5192\u70df=\u91cd\u5224\u7a97'
    '\u524d\u7f6e\u8bc1\u636e\u9762\uff09**\uff1b\u76d8\u9762 15:07 \u590d\u6d4b\u8bfb\u7ef4\u6301\u3002'
)
b = b.replace(b_anchor, b_anchor + b_note)
io.open(bp, 'w', encoding='utf-8', newline='').write(b)
print('backlog #112 R2039 note appended')

# --- export refresh (live three lines + do) ---
exp = json.load(io.open('docs/status-export.json', encoding='utf-8'))
live = exp.get('live')
assert isinstance(live, list) and len(live) == 3, 'live shape unexpected: %r' % (live,)
patch = {
    "do": ("\u96f7\u8fbe\u91cd\u5224\u7a97\u524d\u7f6e\u590d\u9a8c\u6bd5\uff1a\u6821\u51c6\u5df2\u6fc0\u6d3b"
           "\uff08worker \u8f7d\u65b0\u6587\u672c\u786e\u8ba4\uff09\u4f46 GPU \u88ab MV \u5168\u66f2\u751f\u4ea7\u5360\u6ee1="
           "\u8bc4\u5206\u5b8c\u6210\u6d41\u96f6\uff08\u4e89\u62a2\u65cf\u5b9e\u951a\uff09\uff0c\u7a97\u5185\u79ef\u7d2f"
           "\u4e0e\u6821\u51c6\u9a8c\u8bc1\u4f9d\u8d56\u591c\u7a97\u9759\u9ed8\u671f\uff1b\u591c\u7a72\u91cd\u6392+"
           "\u5192\u70df\u817f\u5df2\u5165\u961f\uff1b\u4e24\u4ef6\u89c6\u9891\u8bc4\u5ba1\u4ef6\u7ee7\u7eed\u7b49 GPU "
           "\u7a7a\u95f2\u7a97"),
    "live": [
        "\u5f53\u524d\u6d3b\uff1a\u7b49 GPU \u7a7a\u95f2\u7a97\u2014\u2014MV \u5168\u66f2\u751f\u4ea7\u5728\u8dd1\uff0c"
        "\u4e24\u4ef6\u89c6\u9891\u8bc4\u5ba1\u4ef6+\u96f7\u8fbe\u591c\u7a97\u8bc4\u5206\u79ef\u7d2f\u6392\u961f\u4e2d",
        "\u6700\u8fd1\u5b9e\u7269\uff1a\u96f7\u8fbe\u91cd\u5224\u7a97\u524d\u7f6e\u590d\u9a8c\uff08\u6821\u51c6\u6fc0\u6d3b"
        "\u786e\u8ba4\u00b7\u8bc4\u5206\u6d41\u5b9a\u8c2d\uff09\uff0c10-12 \u6668",
        "\u4e0b\u4e2a\u91cc\u7a0b\u7891\uff1a\u96f7\u8fbe\u65e5\u62a5\u8bc4\u5206\u6821\u51c6\u91cd\u5224\uff0c"
        "10-13 \u65e9 8 \u70b9",
    ],
}
io.open('.c3-tmp/r2039_export_patch.json', 'w', encoding='utf-8').write(json.dumps(patch, ensure_ascii=False, indent=1))
r = subprocess.run([sys.executable, 'src/os/export_refresh.py', '--patch', '.c3-tmp/r2039_export_patch.json'],
                   capture_output=True)
print('export_refresh rc=%d out=%s' % (r.returncode, r.stdout.decode('utf-8', 'replace').strip()[:200]))
assert r.returncode == 0, r.stderr.decode('utf-8', 'replace')[:300]

# --- temp cleanup hook: r2039 anchor-check scratch files (round temps, evidence kept) ---
for f in ('r2039_anchors.txt', 'r2039_t92_entry.txt', 'r2039_gb.txt', 'r2039_focus_dump.txt',
          'r2039_check_anchors.py'):
    fp = os.path.join('.c3-tmp', f)
    if os.path.exists(fp):
        os.remove(fp)
        print('removed %s' % fp)

# --- accounting commit ---
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'os'))
import close_commit
MSG = ("R2039: tech#92 re-judge precheck done: worker 4576 live + queue moving (analyze completed 6529->6577) "
       "BUT score/structure completions=0 since restart (44 receipts all unknown = 120s-cap contention family, "
       "MV sprint GPU = CEO priority side); calibration verify + window accumulation both defer to night quiet "
       "window; failed 676->803 (no re-requeue, R1800); night-window smoke + city-pool requeue seeded (tech#126); "
       "fire no-fire rc1 mv-active #15; probes green [via bm-a]")
rc, log_lines = close_commit.run_close_commit(
    ['src/os/state.json', 'state/queue/tech.md', 'src/os/backlog.md', 'docs/status-export.json',
     'data/pipeline/fire-consume-ledger.jsonl', '.c3-tmp/r2039_export_patch.json',
     '.c3-tmp/r2039_close.py', '.c3-tmp/r2039_t92_prewindow.py', '.c3-tmp/r2039_t92_readout.json'], MSG)
for ln in log_lines:
    print(ln)
print('run_close_commit rc=%d' % rc)
