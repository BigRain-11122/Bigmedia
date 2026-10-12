# r2037_close.py -- R2037 production close: tech#92 authoritative-window read
# Verdict: INVALID (activation-missing), not FAIL -- workers (started 10-10 12:34:24,
# double-worker 59324+7660) predate anchored selection-score-city.md mtime (10-11
# 08:23:09); module-cache law (R1887) => anchored rubric never live; window tested
# the OLD city rubric. R1956 "already live in worker" assertion corrected
# (R1886 non-activated swap family, 3rd case). Window re-judge moved to 10-13 08:00;
# activation step (kill double worker -> single restart) = next round.
# Also: 10-12 daily compose 08:00:34 judged0/selected0 (3rd empty window); zhihu-hot
# 62 scored / max 59 / ge60=0 surface; interval 180min throttle regressed (15/21/15/33);
# city failed pool 676 (contention family, no re-requeue per R1800); new pools 494/489;
# score receipts silent since 10-11 21:11 while prefilter alive to 08:03 (half-alive).
import io, json, datetime, sys, os, subprocess

P = 'src/os/state.json'
raw = io.open(P, 'rb').read()
has_bom = raw.startswith(b'\xef\xbb\xbf')
txt = raw.decode('utf-8-sig')
nl = '\r\n' if '\r\n' in txt else '\n'
lines = txt.split(nl)

# --- locate array close + ts + task lines (tail window only) ---
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
assert lines[idx_ts].strip() == '"ts": "2026-10-12 07:40:45",', lines[idx_ts]

LOG = (
    '  "2026-10-12 08:1x R2037: 生产轮·tech#92 雷达标定权威窗判读=无效审（activation-missing·判据窗顺延 10-13）+fire_consume no-fire=mv-active（MV 会话在写=CEO 优先线让路正确侧）——'
    '①轮首五查全静=own orders 顶 O-20260908-1105 mtime 12:08:14==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）+group_scan 四面全静'
    '（decisions truly_new=0 水位 150 维持+ledger @BigStream 5 行==值守锚零新转办+ORDERS 行水位 quiet rows=270 tail_key=\'10-11 13:4x\'==R1979 基线）'
    '+无 index.lock+树态=MV sprint 会话域在飞件零接触（R1745 承继）；②三探针绿=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面 0 发现'
    '/loop_health 2F+265W 皆在案史实带内（两 outage 已裁定不重触发）；③tech#121 消费序律=探针毕后 fire_consume 单命令直发（.c3-tmp/r2037 探针前 --launch 路径勘正一次=单值参）'
    '=no-fire rc1（reason=card-no-fire: mv-active=mv_sprint_probe 文件面新鲜=MV sprint 会话活跃让路正确侧·ledger 行落盘）→F-180 SC-005-07 flight-4'
    '（s1_call preflight 三件+--wedge-probe）+F-181 REACT-v15 评审腿（tech#113 发射器 staged·tech#123 preflight 正法重生成）双件维持 fire-ready 结转；'
    '④tech#92 权威窗判读（08:02 读·等待窗=分段 Start-Sleep 过 08:00 compose 点·browser_wait_for 工具异常如实注记）=.c3-tmp/r2037_t92_probe.py+readout.json：'
    '10-12 日报 08:00:34 compose 毕=judged 0/selected 0/sections 0=空态第三窗+zhihu-hot 全库 62 scored/max 59/ge60=0（窗内 published_at 滤仅 2 件=热榜源 published_at 长尾错位注记）'
    '→表面 FAIL——**但激活前置缺失实锤**=AIHOT worker 进程起时 10-10 12:34:24（**双 worker 59324+7660 同秒起=R1770 单 worker 拓扑回归面**）早于锚例 prompt mtime 10-11 08:23:09'
    '→R1887 模块级缓存定律=锚例版从未在 worker 在役=R1956「锚例版已上线 worker」断言勘正（**R1886 换装未生效同族第三案**）→权威窗测的是旧 city rubric=判据窗判定无效不成立 FAIL'
    '·**判据窗顺延 10-13 08:00+激活步（杀双 worker→单 worker 重启载锚例版=R1887 激活步正法）归下轮**；⑤#112 轻读随件=api ok{ok,db:ok}+fetch cron 新鲜'
    '（last_ok 08:01/07:57/07:58）+**interval 180min 节流未持久化回归**（sources.interval_minutes 现实 15/21/15/33·R1952 UPDATE 被覆写面待归因）'
    '+城市源 failed 池 676（R1800 争抢族 precedent 不 re-requeue 维持）+new 池 494/489 积压注记（**score 回执 10-11 21:11 后零行·prefilter 回执活到 08:03〔648 行 since 21:12〕'
    '=评段上游断流 pipeline 半活态·归因归下轮**）；⑥例行件=10-12 日报在案不重跑（R2008）·W42 周审在案（R2008）·GB §④ v1.3 下期 10-15 ≤7d 跳过·T1 催办无超线项'
    '（账号物理件=呈现状行不催办）·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·tokens:local=0（纯 DB/进程读数零本地模型调用·P-54⑤ 计量律）；'
    '⑦队列补货步=真无独立新种子如实注记零膨胀（tech#92 激活步=既有项下一步非新种子·禁凑数律）·临时件清理钩=r2037 探针三件随 close 自含律入账'
    '——下轮=R2038 轮首 fire_consume 直发维持（GO=F-180 flight-4 派发→S1 判词→F-180 登记·F-181 后段位）+tech#92 激活步（worker 重启）→10-13 08:00 重判"'
)

prev = lines[idx_close - 1]
assert prev.strip().startswith('"2026-10-12 07:4x R2036:'), prev[:60]
if not prev.rstrip().endswith(','):
    lines[idx_close - 1] = prev + ','
assert not LOG.rstrip().endswith(','), 'LOG must be last element without trailing comma'

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
TASK = ' "task": "生产轮·tech#92 权威窗判读=无效审（锚例未激活·worker 重启步归下轮·顺延 10-13）",'

lines.insert(idx_close, LOG)
lines[idx_ts + 1] = ' "ts": "%s",' % now
lines[idx_task + 1] = TASK

out = nl.join(lines)
assert out.count('"tick": 2036,') == 1
out = out.replace('"tick": 2036,', '"tick": 2037,')
json.loads(out)  # validity gate

data = out.encode('utf-8')
if has_bom:
    data = b'\xef\xbb\xbf' + data
io.open(P, 'wb').write(data)
print('r2037 state OK: tick=2037 ts=%s bom=%s nl=%r json=valid' % (now, has_bom, nl))

# --- tech.md tech#92 R2037 note (inline append to entry line) ---
tp = 'state/queue/tech.md'
t = io.open(tp, encoding='utf-8').read()
anchor = 'A-eviction-credit/A-hot-resident/B-eviction-credit \u4e09\u8def\u5f84\u5168\u5b9e\u6218\uff09'
assert t.count(anchor) == 1, 'tech#92 anchor not unique: %d' % t.count(anchor)
note = (
    ' **[R2037 \u6743\u5a01\u7a97\u5224\u8bfb 2026-10-12\uff08\u65e0\u6548\u5ba1\u5b9a\u8c28\u975e FAIL\uff09]**\uff1a'
    '\u246010-12 \u65e5\u62a5 08:00:34 compose \u6bd5=judged 0/selected 0=\u7a7a\u6001\u7b2c\u4e09\u7a97\uff1b'
    '\u2461zhihu-hot \u5168\u5e93 62 scored/max 59/ge60=0\uff08\u7a97\u5185 published_at \u6ee4\u4ec5 2 \u4ef6=\u70ed\u699c\u6e90 published_at \u957f\u5c3e\u9519\u4f4d\u6ce8\u8bb0\uff09'
    '\u2192\u8868\u9762 FAIL\uff1b\u2462**\u4f46\u6fc0\u6d3b\u524d\u7f6e\u7f3a\u5931\u5b9e\u9524**\uff1aworker \u8fdb\u7a0b\u8d77\u65f6 10-10 12:34:24'
    '\uff08\u53cc worker 59324+7660 \u540c\u79d2\u8d77=R1770 \u5355 worker \u62d3\u6251\u56de\u5f52\u9762\uff09\u65e9\u4e8e\u951a\u4f8b prompt mtime 10-11 08:23:09'
    '\u2192R1887 \u6a21\u5757\u7ea7\u7f13\u5b58\u5b9a\u5f8b=\u951a\u4f8b\u7248\u4ece\u672a\u5728\u4f4d\uff1dR1956\u300c\u5df2\u4e0a\u7ebf worker\u300d\u65ad\u8a00\u52d8\u6b63'
    '\uff08R1886 \u6362\u88c5\u672a\u751f\u6548\u540c\u65cf\u7b2c\u4e09\u6848\uff09\u2192\u6743\u5a01\u7a97\u6d4b\u7684\u662f\u65e7 city rubric=\u5224\u5b9a\u65e0\u6548\uff1b'
    '\u2463receipts \u4f50\u8bc1=score \u56de\u6267 10-11 21:11 \u540e\u96f6\u884c\uff08~11h \u8bc4\u5206\u9759\u9ed8\uff09\u800c prefilter \u6d3b\u5230 08:03\uff08648 \u884c since 21:12\uff09'
    '=pipeline \u534a\u6d3b\u6001\u5f52\u56e0\u4e0b\u8f6e\uff08GPU \u4e89\u62a2\u65cf+prefilter block \u65cf\u5f85\u5f52\u56e0\uff09\u2014\u2014'
    '**\u5224\u636e\u7a97\u987a\u5ef6 10-13 08:00+\u6fc0\u6d3b\u6b65\u8865\u505a=\u6740\u53cc worker\u2192\u5355 worker \u91cd\u542f\u8f7d\u951a\u4f8b\u7248\uff08R1887 \u6fc0\u6d3b\u6b65\u6b63\u6cd5\uff09\u2192\u4e0b\u7a97\u91cd\u5224**'
    '\uff08PASS=\u6587\u672c\u817f\u6536\u53e3/FAIL=\u9608\u503c\u5206\u5c42\u817f\u9012\u8865\u7167\u9884\u6ce8\u518c\uff09\uff1b'
    '\u2464\u968f\u4ef6 #112 \u8f7b\u8bfb=interval 180min \u8282\u6d41\u672a\u6301\u4e45\u5316\u56de\u5f52\uff0815/21/15/33 \u5b9e\u8bfb\uff09+\u57ce\u5e02\u6e90 failed \u6c60 676\u4e0d re-requeue\uff08R1800\uff09'
    '+new \u6c60 494/489 \u79ef\u538b\u2014\u2014\u8bc1\u636e .c3-tmp/r2037_t92_readout.json'
)
t = t.replace(anchor, anchor + note)
io.open(tp, 'w', encoding='utf-8', newline='').write(t)
print('tech.md tech#92 R2037 note appended')

# --- backlog #112 light-read note ---
bp = 'src/os/backlog.md'
b = io.open(bp, encoding='utf-8').read()
b_anchor = '\u76d8\u9762\u7167\u5e38\u89c4 15:07 \u590d\u6d4b\u8bfb\uff09\u3002'
assert b.count(b_anchor) == 1, 'backlog #112 anchor not unique: %d' % b.count(b_anchor)
b_note = (
    '\r\n   **[R2037 \u8f7b\u8bfb 2026-10-12]**\uff1atech#92 \u6743\u5a01\u7a97\u5224\u8bfb=\u65e0\u6548\u5ba1\uff08activation-missing\uff1a\u53cc worker \u8d77\u65f6 10-10 12:34 \u65e9\u4e8e\u951a\u4f8b\u7248 mtime 10-11 08:23'
    '=\u951a\u4f8b\u672a\u6fc0\u6d3b\u00b7R1886 \u540c\u65cf\u7b2c\u4e09\u6848\u00b7R1956\u65ad\u8a00\u52d8\u6b63\uff09+\u7a7a\u6001\u7b2c\u4e09\u7a97\uff0810-12 \u65e5\u62a5 judged 0/selected 0\uff09'
    '+interval 180min \u8282\u6d41\u672a\u6301\u4e45\u5316\u56de\u5f52\uff0815/21/15/33 \u5b9e\u8bfb\uff09+failed \u6c60 676 \u4e89\u62a2\u65cf\u4e0d re-requeue \u7ef4\u6301+new \u6c60 494/489 \u79ef\u538b'
    '\uff08score \u56de\u6267 21:11 \u540e\u96f6\u884c\u00b7prefilter \u6d3b\u5230 08:03=\u8bc4\u6bb5\u4e0a\u6e38\u65ad\u6d41\u5f52\u56e0\u4e0b\u8f6e\uff09\u2014\u2014\u6808\u6d3b\u6027 api ok/fetch \u65b0\u9c9c\u7ef4\u6301'
    '\uff1b\u5224\u636e\u7a97\u987a\u5ef6 10-13 08:00\uff08\u6fc0\u6d3b\u6b65=worker \u91cd\u542f\u5f52\u4e0b\u8f6e\uff09\u2014\u2014\u76d8\u9762 15:07 \u590d\u6d4b\u8bfb\u7ef4\u6301\u3002'
)
b = b.replace(b_anchor, b_anchor + b_note)
io.open(bp, 'w', encoding='utf-8', newline='').write(b)
print('backlog #112 R2037 light-read note appended')

# --- export refresh (live three lines + do; export_refresh.py live-clock writer) ---
exp = json.load(io.open('docs/status-export.json', encoding='utf-8'))
live = exp.get('live')
assert isinstance(live, list) and len(live) == 3, 'live shape unexpected: %r' % (live,)
patch = {
    "do": ("\u96f7\u8fbe\u65e5\u62a5\u8bc4\u5206\u6821\u51c6\u7a97\u5224\u8bfb\u5b8c\u6210\uff1a\u65b0\u6821\u51c6\u6587\u672c\u672a\u751f\u6548\uff08\u9700\u91cd\u542f\u670d\u52a1\u6fc0\u6d3b\uff09\uff0c"
           "\u91cd\u5224\u7a97\u987a\u5ef6\u660e\u6668 08:00\uff1b\u4e24\u4ef6\u89c6\u9891\u8bc4\u5ba1\u4ef6\u7ee7\u7eed\u7b49 GPU \u7a7a\u95f2\u7a97"),
    "live": [
        "\u5f53\u524d\u6d3b\uff1a\u7b49 GPU \u7a7a\u95f2\u7a97\u2014\u2014MV \u5168\u66f2\u751f\u4ea7\u5728\u8dd1\uff0c\u4e24\u4ef6\u89c6\u9891\u8bc4\u5ba1\u4ef6\u6392\u961f\u4e2d",
        "\u6700\u8fd1\u5b9e\u7269\uff1a\u57ce\u5e02\u76d8\u70b9 018 \u6570\u5b57\u5361\u7247\uff0810-11 \u6df1\u591c\u5b8c\u6210\uff09",
        "\u4e0b\u4e2a\u91cc\u7a0b\u7891\uff1a\u96f7\u8fbe\u65e5\u62a5\u8bc4\u5206\u6821\u51c6\u6fc0\u6d3b+\u91cd\u5224\uff0c10-13 \u65e9 8 \u70b9",
    ],
}
io.open('.c3-tmp/r2037_export_patch.json', 'w', encoding='utf-8').write(json.dumps(patch, ensure_ascii=False, indent=1))
r = subprocess.run([sys.executable, 'src/os/export_refresh.py', '--patch', '.c3-tmp/r2037_export_patch.json'],
                   capture_output=True)
print('export_refresh rc=%d out=%s' % (r.returncode, r.stdout.decode('utf-8', 'replace').strip()[:200]))
assert r.returncode == 0, r.stderr.decode('utf-8', 'replace')[:300]

# --- accounting commit (tech#65 shrink kill window + tech#81 self-include) ---
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'os'))
import close_commit
MSG = ("R2037 production: tech#92 authoritative window read = INVALID (activation-missing): double-worker started "
       "10-10 12:34 predates anchored selection-score-city.md (10-11 08:23) per module-cache law -> anchored rubric "
       "never live (R1886 family 3rd case, R1956 assertion corrected); window re-judge moved to 10-13 08:00, "
       "activation step (single-worker restart) next round; fire_consume no-fire rc1 reason=mv-active (yield correct); "
       "#112 light-read: 3rd empty daily window, interval 180min throttle regressed (15/21/15/33), failed pool 676 "
       "(no re-requeue per R1800), new pools 494/489, score receipts silent since 10-11 21:11 while prefilter alive; "
       "five-checks quiet, probes in-band, no new seeds [via bm-a]")
rc, log_lines = close_commit.run_close_commit(
    ['src/os/state.json', 'state/queue/tech.md', 'src/os/backlog.md', 'docs/status-export.json',
     'data/pipeline/fire-consume-ledger.jsonl', '.c3-tmp/r2037_t92_probe.py', '.c3-tmp/r2037_t92_readout.json',
     '.c3-tmp/r2037_export_patch.json', '.c3-tmp/r2037_close.py'], MSG)
for ln in log_lines:
    print(ln)
print('run_close_commit rc=%d' % rc)
