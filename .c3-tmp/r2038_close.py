# -*- coding: utf-8 -*-
# r2038_close.py -- R2038 production close: tech#92 activation step executed.
# Single worker 4576 restarted 08:16:37 (after anchored selection-score-city.md
# mtime 10-11 08:23:09 -> anchored rubric now live); 10-13 08:00 re-judge armed.
# R2037 "double-worker" read CORRECTED by hard evidence: 59324 was the API
# (api-r1891.log pid 59324 "Server listening at 3101"), 7660 was the worker
# (worker-r1891.log pid 7660); apps/worker and apps/api share the same relative
# cmdline "node --env-file-if-exists=../../.env src/main.ts" (same-named
# src/main.ts) = process-ID blind spot. Activation kill took API down as
# collateral (3100 proxy 502) -> restored same round: apps/api restart
# (node 73084, 3101 health ok, 3100 proxy 200). Topology end-state:
# proxy 65752 + worker 4576 + api 73084, all single-instance.
# Eval-segment stall (R2037 assigned): score/structure/summarize/story_digest
# receipts all silent since 10-11 21:11-21:13 while prefilter flowed to 08:18;
# root cause = content.analyze 12 active slots hung on old worker (concurrency
# starvation). Post-restart: completed 6529->6535, created 1027->1021, 6 new
# active slots eating; 6 stale actives (heartbeat frozen 08:15, retry 0/4)
# await pgboss maintenance sweep; score/structure receipts re-verify next round.
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
assert lines[idx_ts].strip() == '"ts": "2026-10-12 08:05:33",', lines[idx_ts]

LOG = (
    '  "2026-10-12 08:3x R2038: 生产轮·tech#92 激活步执行毕（单 worker 4576 重启 08:16:37 载锚例版·10-13 08:00 重判窗就位）'
    '+R2037「双 worker」判读勘正（59324 实=API·7660=worker·同形 cmdline 识别盲区实锚）+API 侧车当场修复+评段断流根因定谳（analyze 队列槽饿死）——'
    '①轮首五查全静=own orders 顶 O-20260908-1105 mtime==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）'
    '+group_scan 四面全静（decisions truly_new=0 水位 150 维持+ledger @BigStream 5 行==值守锚零新转办+ORDERS quiet rows=270 tail_key=\'10-11 13:4x\'==R1979 基线）'
    '+无 index.lock+树态=MV sprint 会话域在飞件零接触（R1745 承继）；②三探针绿=board 0 FAIL（5 题 10 稿 5 in production）'
    '/readiness 3 阻塞皆外部 CEO 面 0 发现/loop_health 2F+266W 皆在案史实带内（两 outage 已裁定不重触发·drift 18≤基线 21）；'
    '③tech#121 消费序律=探针毕后下一命令 fire_consume verbatim 直发=no-fire rc1（reason=card-no-fire: mv-active=MV sprint 会话活跃让路正确侧'
    '·no-fire 序列第 14 数据点·ledger 行落盘）→F-180 SC-005-07 flight-4（s1_call preflight 三件+--wedge-probe 就位）+F-181 REACT-v15 评审腿'
    '（tech#113 发射器 staged·tech#123 preflight 正法重生成）双件维持 fire-ready 结转；'
    '④**tech#92 激活步执行毕（本轮主活）**=kill 双 node 59324+7660→worker-restart.bat 单 worker 重启=node PID 4576 起 08:16:37'
    '（晚于锚例 rubric mtime 10-11 08:23:09=industry/prompts/selection-score-city.md 锚例版将在役·117 行注入防护边界验讫）→10-13 08:00 重判窗就位；'
    '⑤**R2037 判读勘正（硬证双 log）**=59324 实=API 进程（api-r1891.log pid 59324 \'Server listening at 3101\'）+7660 实=worker'
    '（worker-r1891.log pid 7660）——apps/worker 与 apps/api 同名 src/main.ts+同形 CWD 相对 cmdline=\'node --env-file-if-exists=../../.env src/main.ts\''
    '=进程识别盲区实锚（非「双 worker 拓扑回归」面）→激活步 kill 连带 API 停摆（3100 proxy 502 api unavailable）当场修复'
    '=apps/api 单实例重启 node 73084 起 08:19:26（3101 health {ok,db:ok,ms:1}+3100 proxy 200 恢复）→拓扑终态=site-proxy 65752+worker 4576+api 73084 '
    '三件套单实例全绿；⑥**评段断流归因定谳（R2037 派件）**=receipts 实测 score_article/structure_article/summarize_article/story_digest 全停 '
    '10-11 21:11-21:13（293/147/93/50 行零新增）而 prefilter_article 活到 08:18（1056 行）→根因面=content.analyze 队列 12 active 槽被旧 worker '
    '挂起任务占满（并发饥饿·prefilter 他队列不受连坐）；重启后=completed 6529→6535/created 1027→1021 队列复动+6 新 active 08:20 在吃'
    '+6 旧 stale active（heartbeat 冻结 08:15·retry_limit 4 retry_count 0）待 pgboss maintenance 回收——score/structure 回执复验归下轮（半愈态如实注）；'
    '⑦例行件=10-12 日报在案不重跑（R2008 一份为真相）·W42 周审第 4 期在案（R2008）·GB §④ v1.3 下期 10-15 ≤7d 跳过·T1 催办无超线项'
    '（账号物理件=呈现状行不催办）·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·tokens:local=0（纯进程/DB 读+探针零本地模型产出调用·P-54⑤ 计量律）；'
    '⑧队列补货步=真种子一条入 tech 队（#125 AIHOT 进程识别盲区+api-restart.bat 配套候选·本轮实锚）'
    '+临时件清理钩=r2038 bat 重定向四小件删净（aihot-poc 域·本会话零 .c3-tmp 新建件）'
    '——下轮=R2039 轮首 fire_consume 直发维持（GO=F-180 flight-4 派发→S1 判词→F-180 登记·F-181 后段位）'
    '+评段恢复复验（score/structure 回执面+6 旧 stale active 回收态）+tech#92 判据窗 10-13 08:00 重判'
    '（zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补）"'
)

prev = lines[idx_close - 1]
assert prev.strip().startswith('"2026-10-12 08:1x R2037:'), prev[:60]
if not prev.rstrip().endswith(','):
    lines[idx_close - 1] = prev + ','
assert not LOG.rstrip().endswith(','), 'LOG must be last element without trailing comma'

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
TASK = ' "task": "生产轮·tech#92 激活步毕（worker 4576 载锚例版·10-13 重判就位）+双 worker 勘正+API 修复+断流定谳",'

lines.insert(idx_close, LOG)
lines[idx_ts + 1] = ' "ts": "%s",' % now
lines[idx_task + 1] = TASK

out = nl.join(lines)
assert out.count('"tick": 2037,') == 1
out = out.replace('"tick": 2037,', '"tick": 2038,')

old_focus_tail = ('+tech#92 雷达标定权威窗 08:00 届日即领（zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补）')
new_focus_tail = ('+评段恢复复验（score/structure 回执面+6 旧 stale active 回收态）'
                  '+tech#92 判据窗 10-13 08:00 重判（zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补）')
assert out.count(old_focus_tail) == 2, 'focus tail count=%d (expect focus field + R2034 log history)' % out.count(old_focus_tail)
out = out.replace(old_focus_tail, new_focus_tail, 1)  # first occurrence only = focus field (pos ~546, before log array)

json.loads(out)  # validity gate

data = out.encode('utf-8')
if has_bom:
    data = b'\xef\xbb\xbf' + data
io.open(P, 'wb').write(data)
print('r2038 state OK: tick=2038 ts=%s bom=%s nl=%r json=valid' % (now, has_bom, nl))

# --- tech.md: tech#92 R2038 activation note (inline append) ---
tp = 'state/queue/tech.md'
t = io.open(tp, encoding='utf-8').read()
anchor = '\u8bc1\u636e .c3-tmp/r2037_t92_readout.json'
assert t.count(anchor) == 1, 'tech#92 R2037 evidence anchor count=%d' % t.count(anchor)
note = (
    ' **[R2038 \u6fc0\u6d3b\u6b65\u6267\u884c\u6bd5 2026-10-12]**\uff1a'
    '\u2460kill \u53cc node 59324+7660\u2192worker-restart.bat \u5355 worker \u91cd\u542f=node PID 4576 \u8d77 08:16:37'
    '\uff08\u665a\u4e8e\u951a\u4f8b rubric mtime 10-11 08:23:09=\u951a\u4f8b\u7248\u5c06\u5728\u5f79\uff09\u2192**10-13 08:00 \u91cd\u5224\u7a97\u5c31\u4f4d**\uff1b'
    '\u2461**R2037\u300c\u53cc worker\u300d\u5224\u8bfb\u52d8\u6b63\uff08\u786c\u8bc1\u53cc log\uff09**=59324 \u5b9e=API \u8fdb\u7a0b'
    '\uff08api-r1891.log pid 59324 \'Server listening at 3101\'\uff09+7660 \u5b9e=worker\uff08worker-r1891.log pid 7660\uff09'
    '\u2014\u2014apps/worker \u4e0e apps/api \u540c\u540d src/main.ts+\u540c\u5f62 CWD \u76f8\u5bf9 cmdline=\u8fdb\u7a0b\u8bc6\u522b\u76f2\u533a\u5b9e\u951a'
    '\uff08\u975e\u62d3\u6251\u56de\u5f52\u9762\uff09\u2192kill \u8fde\u5e26 API \u505c\u6446\u5f53\u573a\u4fee\u590d\uff08apps/api \u91cd\u542f 73084\u00b73101 health ok\u00b73100 proxy 200\uff09'
    '\u2192\u62d3\u6251\u7ec8\u6001=proxy 65752+worker 4576+api 73084 \u4e09\u4ef6\u5957\u5355\u5b9e\u4f8b\u5168\u7eff\uff1b'
    '\u2462\u8bc4\u6bb5\u65ad\u6d41\u5f52\u56e0\u5b9a\u8c2d=content.analyze \u961f\u5217 12 active \u69fd\u88ab\u65e7 worker \u6302\u8d77\u4efb\u52a1\u5360\u6ee1'
    '\uff08score/structure/summarize \u56de\u6267\u5168\u505c 10-11 21:11-21:13 \u800c prefilter \u6d3b\u5230 08:18=\u5e76\u53d1\u9985\u997f\uff09'
    '\u2192\u91cd\u542f\u540e\u961f\u5217\u590d\u52a8\uff08completed 6529\u21926535\u00b7created 1027\u21921021\u00b76 \u65b0\u69fd\u5728\u5403\uff09'
    '+6 \u65e7 stale active \u5f85 maintenance \u56de\u6536\u2014\u2014score/structure \u56de\u6267\u590d\u9a8c=\u4e0b\u8f6e\u4f4d\uff08\u91cd\u5224\u7a97\u524d\u7f6e\uff09'
)
t = t.replace(anchor, anchor + note)

# --- tech.md: new seed #125 (queue restock step) ---
t = t.rstrip('\r\n')
if not t.endswith('\n'):
    t += '\n'
t += '\r\n'
t += (
    '125. [R2038 \u8865\u8d27\u00b7tech#92 \u6fc0\u6d3b\u6b65\u6267\u884c\u9762\u771f\u53d1\u73b0] AIHOT \u8fdb\u7a0b\u8bc6\u522b\u76f2\u533a+API \u91cd\u542f\u914d\u5957\u7f3a\u4f4d'
    '\uff08\u7f3a\u53e3\u951a=R2038 \u5b9e\u951a\uff1aworker\uff08apps/worker\uff09\u4e0e API\uff08apps/api\uff09\u540c\u5f62 cmdline '
    '\'node --env-file-if-exists=../../.env src/main.ts\'\uff08CWD \u76f8\u5bf9\u00b7\u4e24 app \u540c\u540d src/main.ts\uff09'
    '=\u8fdb\u7a0b\u8bc6\u522b\u76f2\u533a\u5b9e\u951a\u2014\u2014R2037\u300c\u53cc worker 59324+7660\u300d\u5224\u8bfb\u52d8\u6b63=59324 \u5b9e=API'
    '\uff08api-r1891.log pid \u5b9e\u8bc1\uff09+7660=worker\uff08worker-r1891.log\uff09\u00b7\u6fc0\u6d3b\u6b65 kill \u8fde\u5e26 API \u505c\u6446 3100 proxy 502 '
    '\u5f53\u573a\u4fee\u590d\uff08apps/api \u91cd\u542f 73084\u00b7health ok\uff09\u2014\u2014\u5019\u9009=\u2460aihot-poc \u6839\u589e api-restart.bat \u914d\u5957\u4ef6'
    '\uff08worker-restart.bat \u59ca\u59b9\u9762\u00b7\u53cc bat=\u62d3\u6251\u5355\u4e00\u771f\u76f8\uff09\u2461\u8fd0\u7ef4\u63a2\u9488\u589e AIHOT \u8fdb\u7a0b\u9762\u5065\u5eb7\u8bfb'
    '\uff08worker+api+proxy \u4e09\u4ef6\u5957\u62d3\u6251\u6821\u9a8c\u00b7\u540c\u5f62 cmdline \u5224 CWD \u5b9e\u8bc1\uff09\u2462\u5224\u8d1f\u7559\u75d5\uff1b'
    '\u5224\u636e=\u4e0b\u8f6e\u8d77 kill/restart AIHOT \u57df\u8fdb\u7a0b\u524d=\u8fdb\u7a0b\u8eab\u4efd CWD \u5b9e\u8bc1+api-restart.bat \u843d\u4f4d\u540e worker \u57df\u64cd\u4f5c\u96f6 API \u4fa7\u8f66\u635f\u4f24'
    '\u2014\u2014\u6309\u8ba4\u9886\u5236\u968f\u8f6e\u9886\u505a\uff08CPU \u9762\u00b7\u8f7b\u91cf\uff09'
)
io.open(tp, 'w', encoding='utf-8', newline='').write(t)
print('tech.md tech#92 R2038 note + seed #125 appended')

# --- backlog #112 R2038 note ---
bp = 'src/os/backlog.md'
b = io.open(bp, encoding='utf-8').read()
b_anchor = '\uff08\u6fc0\u6d3b\u6b65=worker \u91cd\u542f\u5f52\u4e0b\u8f6e\uff09'
assert b.count(b_anchor) == 1, 'backlog #112 R2037 anchor count=%d' % b.count(b_anchor)
b_note = (
    '\r\n   **[R2038 \u8fdb\u5c55 2026-10-12]**\uff1atech#92 \u6fc0\u6d3b\u6b65\u6267\u884c\u6bd5\u2014\u2014\u53cc node 59324+7660 kill\u2192\u5355 worker 4576 \u91cd\u542f 08:16:37'
    '\uff08\u665a\u4e8e\u951a\u4f8b\u7248 mtime=\u65b0\u6821\u51c6\u6587\u672c\u5c06\u5728\u5f79\uff09\u2192**\u91cd\u5224\u7a97 10-13 08:00 \u5c31\u4f4d**\uff1b'
    '**R2037\u300c\u53cc worker\u300d\u52d8\u6b63**=59324 \u5b9e=API\uff08api-r1891.log pid \u5b9e\u8bc1\uff09+7660=worker\uff08worker-r1891.log\uff09'
    '\u2014\u2014\u540c\u5f62 CWD \u76f8\u5bf9 cmdline \u8bc6\u522b\u76f2\u533a\u5b9e\u951a\u00b7kill \u8fde\u5e26 API \u505c\u6446\u5f53\u573a\u4fee\u590d\uff08apps/api \u91cd\u542f 73084'
    '\u00b73101 health {ok,db:ok}\u00b73100 proxy 200\uff09\u2192\u62d3\u6251\u7ec8\u6001=proxy+worker+api \u4e09\u4ef6\u5957\u5355\u5b9e\u4f8b\u5168\u7eff\uff1b'
    '**\u8bc4\u6bb5\u65ad\u6d41\u5f52\u56e0\u5b9a\u8c2d**=content.analyze \u961f\u5217 12 active \u69fd\u88ab\u65e7 worker \u6302\u8d77\u4efb\u52a1\u5360\u6ee1'
    '\uff08score/structure/summarize \u56de\u6267\u5168\u505c 10-11 21:11-21:13 \u800c prefilter \u6d3b\u5230 08:18=\u5e76\u53d1\u9985\u997f\u673a\u5236\uff09'
    '\u2192\u91cd\u542f\u540e\u961f\u5217\u590d\u52a8\uff08completed 6529\u21926535\u00b7created 1027\u21921021\u00b76 \u65b0\u69fd\u5728\u5403\uff09'
    '+6 \u65e7 stale active \u5f85 maintenance \u56de\u6536\u2014\u2014**score/structure \u56de\u6267\u590d\u9a8c=\u4e0b\u8f6e\uff08\u91cd\u5224\u7a97\u524d\u7f6e\u4f4d\uff09**\uff1b'
    'interval 180min \u8282\u6d41\u8986\u5199\u9762\u5f52\u56e0\u4ecd\u5f00\u653e\uff08R2037 \u6ce8\u8bb0\u7ef4\u6301\uff09\u3002'
)
b = b.replace(b_anchor, b_anchor + b_note)
io.open(bp, 'w', encoding='utf-8', newline='').write(b)
print('backlog #112 R2038 note appended')

# --- export refresh (live three lines + do) ---
exp = json.load(io.open('docs/status-export.json', encoding='utf-8'))
live = exp.get('live')
assert isinstance(live, list) and len(live) == 3, 'live shape unexpected: %r' % (live,)
patch = {
    "do": ("\u96f7\u8fbe\u8bc4\u5206\u6821\u51c6\u6fc0\u6d3b\u6b65\u6267\u884c\u6bd5\uff08worker \u91cd\u542f\u8f7d\u65b0\u6821\u51c6\u6587\u672c+API \u4fa7\u8f66\u4fee\u590d\uff09\uff0c"
           "\u91cd\u5224\u7a97 10-13 \u65e9 8 \u70b9\uff1b\u8bc4\u6bb5\u65ad\u6d41\u6839\u56e0\u5df2\u5b9a\u8c2d\uff08\u961f\u5217\u69fd\u9985\u997f\uff09\u00b7\u961f\u5217\u5df2\u590d\u52a8\uff1b"
           "\u4e24\u4ef6\u89c6\u9891\u8bc4\u5ba1\u4ef6\u7ee7\u7eed\u7b49 GPU \u7a7a\u95f2\u7a97"),
    "live": [
        "\u5f53\u524d\u6d3b\uff1a\u7b49 GPU \u7a7a\u95f2\u7a97\u2014\u2014MV \u5168\u66f2\u751f\u4ea7\u5728\u8dd1\uff0c\u4e24\u4ef6\u89c6\u9891\u8bc4\u5ba1\u4ef6\u6392\u961f\u4e2d",
        "\u6700\u8fd1\u5b9e\u7269\uff1a\u96f7\u8fbe\u8bc4\u5206\u6821\u51c6\u6fc0\u6d3b+\u8bc4\u6bb5\u65ad\u6d41\u4fee\u590d\uff0810-12 \u6668\u6267\u884c\u6bd5\uff09",
        "\u4e0b\u4e2a\u91cc\u7a0b\u7891\uff1a\u96f7\u8fbe\u65e5\u62a5\u8bc4\u5206\u6821\u51c6\u91cd\u5224\uff0c10-13 \u65e9 8 \u70b9",
    ],
}
io.open('.c3-tmp/r2038_export_patch.json', 'w', encoding='utf-8').write(json.dumps(patch, ensure_ascii=False, indent=1))
r = subprocess.run([sys.executable, 'src/os/export_refresh.py', '--patch', '.c3-tmp/r2038_export_patch.json'],
                   capture_output=True)
print('export_refresh rc=%d out=%s' % (r.returncode, r.stdout.decode('utf-8', 'replace').strip()[:200]))
assert r.returncode == 0, r.stderr.decode('utf-8', 'replace')[:300]

# --- temp cleanup: r2038 bat redirect files in aihot-poc (session round temps) ---
for f in ('r2038_bat_stdout.txt', 'r2038_bat_stderr.txt',
          'r2038_api_bat_stdout.txt', 'r2038_api_bat_stderr.txt'):
    fp = os.path.join('data/assets/aihot-poc', f)
    if os.path.exists(fp):
        os.remove(fp)
        print('removed %s' % fp)

# --- accounting commit (tech#65 shrink kill window + tech#81 self-include) ---
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'os'))
import close_commit
MSG = ("R2038: tech#92 activation done (single worker 4576 restarted 08:16:37 > anchored rubric mtime; "
       "10-13 08:00 re-judge armed); R2037 double-worker read corrected by hard logs (59324=API, 7660=worker, "
       "identical CWD cmdlines = ID blind spot) -> collateral API kill restored same round (3101 health ok, "
       "proxy 200); eval stall root-caused: analyze 12 active slots hung since 10-11 21:11 starved score stage "
       "while prefilter flowed; queue moving post-restart, 6 stale slots pending sweep, receipts re-verify next "
       "round; fire no-fire mv-active; tech seed #125 [via bm-a]")
rc, log_lines = close_commit.run_close_commit(
    ['src/os/state.json', 'state/queue/tech.md', 'src/os/backlog.md', 'docs/status-export.json',
     'data/pipeline/fire-consume-ledger.jsonl', '.c3-tmp/r2038_export_patch.json', '.c3-tmp/r2038_close.py'], MSG)
for ln in log_lines:
    print(ln)
print('run_close_commit rc=%d' % rc)
