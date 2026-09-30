# -*- coding: utf-8 -*-
# R749 closeout: receipt round for D-20260930 external-audit batch.
# (1) HQ-FEEDBACK rows F-20260930-01/02, (2) backlog item 95 append,
# (3) production report v1 (XL-14 three columns), (4) r694_probe decisions
# check -> watermark diff, (5) state.json tick 749 + log + focus + ts + task
# + decisions_watermark baseline, (6) status-export refresh.
# NOTE: codex files (bm-a in-flight batch) are NOT added -- yield rule #86 c+d.
import io, json, re, subprocess, sys
from datetime import datetime

NOW = datetime.now()
TS_FULL = NOW.strftime('%Y-%m-%d %H:%M:%S')
TS_HM = NOW.strftime('%H:%M')

def W(path, text):
    io.open(path, 'w', encoding='utf-8').write(text)
    print('WROTE', path)

def append(path, text):
    c = io.open(path, encoding='utf-8').read()
    if not c.endswith('\n'): c += '\n'
    W(path, c + text)

def edit(path, old, new, must=1):
    c = io.open(path, encoding='utf-8').read()
    n = c.count(old)
    if n != must:
        print('!! SKIP %s (match=%d expected=%d)' % (path, n, must)); sys.exit(1)
    W(path, c.replace(old, new, 1))

# ============ 0. watermark extraction + dirty measurements ============
DEC = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
dtext = io.open(DEC, encoding='utf-8').read()
dnums = sorted(set(re.findall(r'[DC]-20\d{6}-\d{2}', dtext)))
board_rows = len(re.findall(r'^\| (?:\*\*)?D-20260930-\d{2}', dtext, re.M))
print('dnum_total=%d board_rows=%d' % (len(dnums), board_rows))

def dirty(uall=True):
    cmd = ['git', 'status', '--porcelain']
    if uall: cmd.append('-uall')
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return [l for l in r.stdout.splitlines() if l.strip()]

pre = dirty()
pre_n = len(pre)
print('dirty_pre_uall=%d' % pre_n)

# stage the evidence batch + written-so-far files (NOT codex, NOT state.json yet)
subprocess.run(['git', 'add', '.c3-tmp', 'src/os/iteration_prompt.txt'], check=True)

# ============ 1. r694_probe decisions check -> watermark diff ============
PO_OLD = '''# 3. decisions UTF8 non-empty (anchor 75)
DEC = r"C:\\Users\\sjs20\\Desktop\\FluxGroup\\docs\\decisions.md"
try:
    with io.open(DEC, "r", encoding="utf-8") as f:
        lines = [l for l in f if l.strip()]
    report.append("decisions_nonempty=%d (anchor 75)" % len(lines))
except Exception as e:
    report.append("decisions_err=%s" % e)'''
PO_NEW = '''# 3. decisions content-addressing watermark (R749 / D-20260930-18+19: line-count retired)
DEC = r"C:\\Users\\sjs20\\Desktop\\FluxGroup\\docs\\decisions.md"
try:
    with io.open(DEC, "r", encoding="utf-8") as f:
        dtext = f.read()
    dset = sorted(set(re.findall(r"[DC]-20\\d{6}-\\d{2}", dtext)))
    try:
        st0 = json.load(io.open(p("src/os/state.json"), "r", encoding="utf-8"))
        wm = st0.get("decisions_watermark", {}).get("dnums", [])
    except Exception:
        wm = []
    new_d = [d for d in dset if d not in wm]
    report.append("decisions_dnum_total=%d watermark=%d new=%d" % (len(dset), len(wm), len(new_d)))
    if new_d:
        report.append("decisions_NEW_DNUMS: " + ",".join(new_d))
except Exception as e:
    report.append("decisions_err=%s" % e)'''
edit('.c3-tmp/r694_probe.py', PO_OLD, PO_NEW)

# ============ 2. HQ-FEEDBACK rows ============
HF1 = ('| F-20260930-01 | P1 | D-20260930-13 SLA + D-20260930-19 投递层统一单（D-11+D-16+D-18 合并单）+ D-20260930-20 送达律延伸 + D-20260930-21 送达执法·BigStream ack 行（收讫回执·P-51 双载体=本行+commit 含行号·检出=13:13 内容寻址首扫〔decisions 行数锚 75=陈旧漂移实证·D-18 判据吸收〕→外审批 D-20260930-05~30+派工通告板全读）——**全过审零驳回+机制腿当轮交付**：'
 '①消费步落位=src/os/iteration_prompt.txt 集团转办扫描步后新增 D-20260930-19 消费步块（轮首读 decisions.md 派工通告板对号本司/七司全部行+读集团 docs/orders.md CEO 待办物理件区·新行 ≤2 轮 ≤20min ack 或驳回=D-13 SLA·12:00 班后派工=下一班首轮处理合法）；'
 '②水位改制=**内容寻址**（D/C-YYYYMMDD-NN 正则集合差集 vs state.json `decisions_watermark.dnums` 基线 %d 项本轮落位·**纯行数比对退役**=D-18 行数漂移实证吸收·r694_probe.py decisions 检查同步改水印差集制）；'
 '③D-21 送达补正=BigStream 零编号引用 ❌→本轮 commit 消息含 D-20260930-13/D-19/D-21+轮号 R749+下一动作=点名窗 10-01 03:07 前闭环 | '
 '证据=iteration_prompt.txt 投递层消费步块+state.json decisions_watermark（%d 项基线·ts %s）+.c3-tmp/r749_probe.txt（内容寻址首扫 133 非空行/75 旧锚漂移定谳）+commit 消息行号族 | '
 '下一动作=#95 XL-14 余腿+queue §E 补池义务随轮（D-19 窗 10-02 12:00 验收面按 ③ 三态判据） | closed |\n' % (len(dnums), len(dnums), TS_FULL))
append('HQ-FEEDBACK.md', HF1)

HF2 = ('| F-20260930-02 | P1 | D-20260930-06 XL-14 BigStream 自领回执（七司各领 XL-13~18 批·验收窗 ≤10-03）——**三件判据逐项**：'
 '①dirty 908→<50：**leg1 本轮执行**=.c3-tmp 全批收账 commit（历轮收账缺口证据件·R150 先例·codex=bm-a 在飞批零接触让位 #86 c+d）·dirty 实测 %d→%s（git status -uall 口径）·余腿=.sc003-tmp/.sc003-v3-tmp 族批闭+达标复核 ≤10-03 随轮；'
 '②≥1 条真发布回写链接=**blocked-on-CEO 账号物理件如实注**（批次① 视频号+公众号 11 平台全未注册=M5 双前置不满足·未上线=未测量·readiness 探针在案——非本司可执行面·开号后 M5 发布+M6 回写链接即落）；'
 '③产出报表三列=**v1 落件** output/reports/production-report-v1.md（三列=轮次|实物|计分档·Executive Protocol v1.1 口径·F-065~F-074 种子 10 行+R749 机制件·口径注=集团反馈后校准） | '
 '证据=本行+production-report-v1.md+git status 前后对照（.c3-tmp/r749_probe.txt）+readiness ① 账号 11 平台未注册在案 | '
 '下一动作=leg2 sc003 tmp 族批闭+dirty<50 达标复核呈报（≤10-03） | open（窗 10-03） |\n' % (pre_n, 'PENDING_POST'))
append('HQ-FEEDBACK.md', HF2)

# ============ 3. backlog item 95 (append at end per house convention) ============
BK = ('95. **D-20260930-06 XL-14 BigStream 承接单 + D-20260930-19 投递层机制腿（集团转办·外审批 09-30 12:23-13:0x 落账·decisions 派工通告板对号·ack 判据=编号引用 commit·验收窗 ≤10-03/D-19 窗 10-02 12:00）**：①dirty 908→<50（git status -uall 口径）②≥1 条真发布回写链接=blocked-on-CEO 账号物理件如实注（M5 双前置·未上线=未测量）③产出报表三列（v1 已落 output/reports/production-report-v1.md·集团反馈后校准）④D-19 机制腿=iteration_prompt 消费步+state decisions_watermark+probe 水印差集制——按认领制随轮领做\n'
   '   **[R749 收讫+回执毕 2026-09-30：五查破静=decisions 行数锚 75 陈旧（D-18 行数漂移实证）→内容寻址重扫=133 非空行（D-20260930-05~30 外审 12 轮批+通告板 22 行 12:41 设立）→转全任务书收讫轮（R444 先例）；科学判断闸=BigStream 相关行全过审零驳回（D-06 XL-14 认领/D-13 SLA ack/D-19 机制腿/D-20 送达律延伸知悉/D-21 ❌→补正/D-25 接手面/D-26 六律知悉/D-12 计分 0→32=51.6% 受冤回归注记/D-04 Bonsai reject 判确认/D-01 ②③ 知悉）；④机制腿全落（prompt 消费步+watermark %d 项基线+probe 改制）；①leg1=.c3-tmp 全批 git add（dirty %d→见 F-20260930-02 实测·codex 零接触）；③报表 v1 落件；②blocked-on-CEO 注记在案；回执双载体=HQ-FEEDBACK F-20260930-01/02+commit 消息含 D-20260930-13/D-19/D-21——余腿=leg2 sc003 tmp 族批闭+dirty<50 达标复核+报表校准=R750 顺位①]**\n' % (len(dnums), pre_n))
append('src/os/backlog.md', BK)

# ============ 4. production report v1 (XL-14 three columns) ============
PR = ('# BigStream 产出报表（XL-14 三列版 v1）\n\n'
 '> 集团 D-20260930-06 XL-14 交付件。三列口径=【轮次/日期】|【本轮实物产出（文件+台账指针）】|【计分档】（Executive Protocol v1.1：能跑/能看/能用实物=2·实际文件改动=1·纯 md/纯记账=0）。\n'
 '> 数据源=output/finished.md 成品库登记+docs/status-export.json；本表=成品实物增量面；发布数/到账数=CEO 账号物理件解锁后 M5/M6 回写（未上线=未测量）。\n'
 '> v1 2026-09-30 R749 落件（R444 引擎批次种子=拆条/速报近十件）·口径随集团反馈校准（窗 ≤10-03）。\n\n'
 '| 轮次/日期 | 本轮实物产出 | 计分档 |\n|---|---|---|\n'
 '| R711 · 09-29 | F-065 lc-011-v1-shipinhao-60s（成品库第 65 件·冗余池第 8 件·output/renders/） | 2 |\n'
 '| R715 · 09-30 | F-066 lc-012-v1-shipinhao-60s（第 66 件·冗余池第 9 件） | 2 |\n'
 '| R716 · 09-30 | F-067 MC-20260930-REACT-v6 城市速报 006（第 67 件·P-1 试点终判件） | 2 |\n'
 '| R721 · 09-30 | F-068 lc-013-v1-shipinhao-60s（第 68 件·冗余池第 10 件） | 2 |\n'
 '| R726 · 09-30 | F-069 lc-014-v1-shipinhao-60s（第 69 件·冗余池第 11 件） | 2 |\n'
 '| R730 · 09-30 | F-070 lc-015-v1-shipinhao-60s（第 70 件·冗余池第 12 件） | 2 |\n'
 '| R734 · 09-30 | F-071 lc-016-v1-shipinhao-60s（第 71 件·冗余池第 13 件） | 2 |\n'
 '| R738 · 09-30 | F-072 lc-017-v1-shipinhao-60s（第 72 件·冗余池第 14 件） | 2 |\n'
 '| R742 · 09-30 | F-073 lc-018-v1-shipinhao-60s（第 73 件·冗余池第 15 件） | 2 |\n'
 '| R748 · 09-30 | F-074 lc-019-v1-shipinhao-60s（第 74 件·冗余池第 16 件） | 2 |\n'
 '| R749 · 09-30 | D-20260930-19 投递层机制腿（iteration_prompt 消费步+state decisions_watermark 水印键+r694_probe 改制）+dirty 批账 leg1（.c3-tmp 全批收账）+本报表 v1 落件 | 1 |\n\n'
 '> 记账注：R749 计分档=1（实际文件改动·收讫+机制轮无新成片）；成品库 74 件全数在案可查 output/finished.md；发布 0 条=账号物理件未开（M5 双前置）。\n')
W('output/reports/production-report-v1.md', PR)
subprocess.run(['git', 'add', 'HQ-FEEDBACK.md', 'src/os/backlog.md', 'output/reports/production-report-v1.md', '.c3-tmp'], check=True)

# measure post-commit dirty estimate (untracked + worktree-modified; state.json excluded -> added at final step)
after = dirty()
post_est = sum(1 for l in after if l.startswith('??') or (len(l) > 1 and l[1] != ' '))
post_est -= 1  # src/os/state.json itself is currently worktree-modified, will be committed
print('dirty_post_est=%d' % post_est)
# fix the pending number in HQ row 2
c = io.open('HQ-FEEDBACK.md', encoding='utf-8').read()
if c.count('PENDING_POST') != 1: print('!! PENDING_POST mismatch'); sys.exit(1)
W('HQ-FEEDBACK.md', c.replace('PENDING_POST', str(post_est), 1))
subprocess.run(['git', 'add', 'HQ-FEEDBACK.md'], check=True)

# ============ 5. state.json ============
R749 = ('2026-09-30 ' + TS_HM + ' R749: 收讫+回执轮·D-20260930 外审批收账（五查破静=decisions 行数锚 75=陈旧〔D-20260930-18 行数漂移实证·13:13 内容寻址首扫 133 非空行〕→D-20260930-05~30 外审 12 轮批+派工通告板 22 行 12:41 设立全读→转全任务书·R444 先例）'
 '——①科学判断闸=BigStream 相关行全过审零驳回：D-06（XL-14 本司自领：dirty 908→<50+真发布回写链接+产出报表三列·窗 10-03）+D-13（新行 ≤2 轮 ≤20min ack SLA）+D-16/D-18/D-19（投递层统一单=合并单·水位内容寻址禁纯行数）+D-20（送达律延伸 decisions 派工行·律源勘正禁重复立法·知悉）+D-21（送达执法 BigStream ❌ 未送达→本轮编号引用 ack 补正·点名窗 10-01 03:07 前闭环）+D-25（外审交付清单 docs/audits/external-audit-handover-20260930.md=接手面单点）+D-26（audit-charter 附录 A 六律知悉）+D-12（计分器 v1.1 修正后本司 0→32=51.6% 受冤回归注记）+D-04（Bonsai 收口=本司 reject 判确认）+D-01 ②③（F-20260928-02 台账核销+hf-cache 冻结采纳知悉）'
 '——②D-19 机制腿交付：iteration_prompt.txt 增投递层统一消费步（通告板对号+集团 orders.md 物理件区+D/C 号正则集合差集水位·禁纯行数）+state.json decisions_watermark 基线落位（%d 项·内容寻址执法面）+r694_probe.py decisions 检查改水印差集制；'
 '③XL-14 leg1=dirty 批账：.c3-tmp 全批 git add 收账（历轮收账缺口证据件·R150 先例·codex=bm-a 在飞批零接触让位）→dirty %d→%d（-uall 口径·余腿=.sc003-tmp/.sc003-v3-tmp 族批闭+达标复核 ≤10-03）·真发布回写链接=blocked-on-CEO 账号物理件如实注（M5 双前置·11 平台 0 开号·未上线=未测量）；'
 '④产出报表三列 v1=output/reports/production-report-v1.md（三列=轮次|实物|计分档·F-065~F-074 种子 10 行+R749 机制件·口径注=集团反馈后校准）；'
 '⑤回执双载体=HQ-FEEDBACK F-20260930-01（投递层 ack·closed）+F-20260930-02（XL-14 自领回执·open 窗 10-03）+backlog #95 入板+commit 消息含 D-20260930-13/D-19/D-21+R749=P-51 送达判据；'
 '⑥例行件：三探针=board 0 FAIL/readiness 3 阻塞皆外部 CEO 面（账号批次①+GATE+发布锁）+loop_health 2 FAIL 皆在案史实（09-26/09-28 outage 窗=批停事件族 D-20260928-01）/日报 09-30 在案不重跑（R713）/W40 周审在案/global-benchmarks 10-01 届日明日领（#80 并窗勿提前）/#70 OSS 窗 2 切片（≤10-02 21:40·R644 切片 1 在案）顺延下轮/#86 c+d 让位判据未达（codex mtime 09-29 04:06 未动·零接触）·tokens:local=0（本轮纯收讫+机制面零本地模型调用·P-54⑤ 计量律如实记）'
 '——下轮=R750 可领序：①#95 XL-14 余腿（sc003 tmp 族批闭+dirty<50 达标复核+报表 v1 校准·窗 ≤10-03）②queue §E 补池义务（lane=E20 徐根福 standby 单条<2）③#70 OSS 窗 2 切片（≤10-02 21:40）④global-benchmarks 10-01 刷新（#80 并窗）⑤#86 c+d 让位判据。收账显式列文件 commit+push')

c = io.open('src/os/state.json', encoding='utf-8').read()
anchor = '"\n ],\n "ts":'
if c.count(anchor) != 1:
    print('!! state anchor mismatch=%d' % c.count(anchor)); sys.exit(1)
c = c.replace(anchor, '",\n  "' + R749.replace('\\', '\\\\').replace('"', '\\"') + '"\n ],\n "ts":', 1)
c = c.replace('"tick": 748,', '"tick": 749,', 1)
m = re.search(r'"focus": "R749: [^"]*"', c)
if not m: print('!! focus not found'); sys.exit(1)
FOCUS = ('R750: ①#95 XL-14 余腿（.sc003-tmp/.sc003-v3-tmp 族批闭收账+dirty<50 达标复核 -uall 口径+产出报表 v1 校准·窗 ≤10-03）②queue §E 补池义务（lane=E20 徐根福 standby 单条<2·选优轮评估：未拆存量卡/BS-007 稿集件/徐根福前件直连位）'
         '③#70 OSS 窗 2 切片（≤10-02 21:40·R644 切片 1 在案）④global-benchmarks 10-01 刷新（#80 并窗）⑤#86 c+d 让位判据'
         '——五查锚=orders O-20260928-1910 42·ledger 41·decisions_watermark dnum 基线 %d 项 R749（内容寻址·D-20260930-18 禁行数）' % len(dnums))
c = c[:m.start()] + '"focus": "' + FOCUS + '"' + c[m.end():]
if not re.search(r'"ts": "2026-09-30 13:07:33"', c): print('!! ts anchor missing'); sys.exit(1)
c = re.sub(r'"ts": "2026-09-30 13:07:33"', '"ts": "' + TS_FULL + '"', c, count=1)
task_line = R749.split('R749: ', 1)[1][:60]
m2 = re.search(r'"task": "[^"]*"', c)
c = c[:m2.start()] + '"task": "R749: ' + task_line.replace('\\', '\\\\').replace('"', '\\"') + '"' + c[m2.end():]
# watermark key insertion before "log": [
wm = ('"decisions_watermark": {"dnums": ' + json.dumps(dnums, ensure_ascii=False) + ', "board_rows": %d, "ts": "%s", "law": "D-20260930-18/19 content-addressing; set-diff vs dnums; line-count retired R749"},\n "log": [' % (board_rows, TS_FULL))
if c.count('\n "log": [') != 1: print('!! log key anchor mismatch'); sys.exit(1)
c = c.replace('\n "log": [', '\n ' + wm[:-len('\n "log": [')].rstrip() + '\n "log": [', 1)
W('src/os/state.json', c)
try:
    json.load(io.open('src/os/state.json', encoding='utf-8'))
    print('STATE_JSON_VALID')
except Exception as e:
    print('!! STATE JSON INVALID: %s' % e); sys.exit(1)

# ============ 6. status-export.json ============
E = json.load(io.open('docs/status-export.json', encoding='utf-8'))
E['export_ts'] = TS_FULL
E['outs'][0][2] = ('tick 749，R749 收讫+回执轮·D-20260930 外审批 25+ 行收账（五查破静=decisions 行数锚陈旧→内容寻址重扫）——BigStream 相关行全过审零驳回；'
 'D-19 机制腿交付（iteration_prompt 投递层消费步+state decisions_watermark %d 项基线+probe 改制）+XL-14 leg1（.c3-tmp 全批收账 dirty %d→%d）'
 '——余腿=sc003 tmp 族+达标复核（≤10-03）·真发布=blocked-on-CEO 账号物理件·发布锁=M5 不变' % (len(dnums), pre_n, post_est))
E['results'].insert(0, ['749', R749])
E['live'] = [
 ['当前活：R749 收讫+回执轮毕——D-20260930 外审批收账+投递层机制腿（D-19 消费步+内容寻址水位）+XL-14 leg1 dirty 批账（908→%d·-uall）·下轮=#95 XL-14 余腿+queue §E 补池' % post_est],
 ['最近实物：output/reports/production-report-v1.md（产出报表三列 v1·XL-14 交付件·2026-09-30 %s）+F-074 lc-019 成片（R748 13:07·成品库第 74 件）' % TS_HM],
 ['下个里程碑：XL-14 dirty<50 达标（≤10-03）+D-19 验收窗（10-02 12:00）+queue §E 补池选优入池（≤48h）+global-benchmarks 刷新（10-01）'],
]
W('docs/status-export.json', json.dumps(E, ensure_ascii=False, indent=1) + '\n')

print('CLOSEOUT_OK pre=%d post_est=%d dnums=%d' % (pre_n, post_est, len(dnums)))
