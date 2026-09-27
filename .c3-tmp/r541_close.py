# R541 idle-fast close-out: state.json log/tick/ts/task/focus + status-export export_ts/dept-t + tmp cleanup
import json, io, os, datetime

NOW = datetime.datetime.now()
LOG_TS = NOW.strftime('%Y-%m-%d %H:%M')
LINE = (
    "2026-09-27 " + NOW.strftime('%H:%M') + " R541: idle-fast 空转快速路径轮（五静+三探针定谳绿·不进开轮四步）——"
    "①无新令（orders 35 件零新增零编辑·锚=O-20260927-1050-HQ-C mtime 13:53:11 未动）"
    "+无新集团转办（ledger 五模式 31=锚零新行·mtime 15:15:21 未动）"
    "+无新决策行（decisions 非空行 56=锚·尾注=bm-c 窗补登注记非本司动作面）"
    "+production=open 自愈核在位；"
    "②backlog 顶行不可认领（#78 素材实录到位核验=footage 顶 census-card-v7-vertical 09-27 12:32=R511 自产源件非 FluxVerse 实录·零新实录维持 blocked〔呈报状态行在案不催办〕"
    "/#59 REACT 09-28 届日即领〔09-27 件 R456 已产·daily_brief 09-28 明届日随窗补产〕"
    "/#63 C-00030/C-00031 锚双 False supply-gated〔anchors 尾 C-00029·共 20〕"
    "/#70 OH 首窗三切片齐下窗 09-29 21:40 后开"
    "/#31 ch.5 v3 稿未落 supply-gated"
    "/#57 替代率 10-07"
    "/#67 史源耗尽待 ledger 新 CEO 令级事件〔反膨胀律〕"
    "/#80 benchmarks 10-01 并窗"
    "/W40 周自审+月度统计注记首件 09-28 开周）；"
    "③树态=仅自产预期态（无 index.lock·untracked .sc003 两 tmp=SC-003 批次未闭预期态"
    "+.c3-tmp r541 探针证据件随下窗 batch commit·HEAD=4d8d3df=R540 窗批 commit 未变=无 bm-a 活跃写盘迹象）；"
    "④三探针定谳绿=board 0 FAIL（5 题 10 稿·5 in production·rc 0）"
    "/readiness 3 阻塞皆外部 CEO 物理件+0 发现 rc 1〔阻塞≠失败口径·48 renders 全注账〕"
    "/loop_health 2 FAIL+24 WARN 零新增〔FAIL① heartbeat-outage 49min 09-26 史实在案类"
    "·FAIL② account-lag beats541>tick540=在飞 done-beat 瞬态收账即平·R459 先例〕；"
    "⑤例行件：日报 09-27 在案不重跑〔09-28 明届日随窗补产〕/W39 周审在案·W40 明开周"
    "/global-benchmarks day3 ≤7 跳过〔下期 10-01〕/T1 催办已裁项停用"
    "/当日无集团层新 open 问题 HQ-FEEDBACK 不写〔零膨胀〕"
    "/tokens:local=0〔五查+三探针纯脚本·P-54⑤ 计量律〕/发布锁=M5 账号物理件不变（未上线=未测量）；"
    "⑥操作红如实入账=三探针首跑 PS > 重定向落 UTF-16 件〔R532/R536/R539 在案同型重犯·探针跑两遍读数同·零盘面副作用〕"
    "→python subprocess capture 正法复跑覆盖=UTF-8 证据件在位（r541_board/readiness/loophealth.txt+r541_probes.json）"
    "+r541_probesum.txt 冗余件即删+r519_probe.json 更名 r541_probe.json；"
    "idle-fast 并窗轮 1/6 不 commit〔新窗 R541-R546·满 6 收账 R546 batch commit·跨日 09-28 00:00 先到即收〕"
)

STATE = 'src/os/state.json'
s = json.load(io.open(STATE, encoding='utf-8'))
s['tick'] = 541
s['ts'] = NOW.strftime('%Y-%m-%d %H:%M:%S')
content = LINE.split('R541: ', 1)[1]
s['task'] = content[:60]
s['focus'] = (
    "R542: 快速路径首查（#78 素材实录到位核验/REACT 09-28 热点窗届日领〔daily_brief 09-28 缺则先补产→REACT 轴位映射律〕"
    "/W40 周自审开周+月度统计注记首件 ≤09-30/OH 切片 4 09-29 21:40 后开/#80 benchmarks 10-01 并窗/新令/集团转办"
    "——锚=orders 35〔mtime 13:53:11〕·ledger 五模式 31〔mtime 15:15:21·unicode-escape 正法〕·decisions 56"
    "——全静即 idle-fast 并窗轮 2/6〔窗 R541-R546·满 6 R546 batch commit·跨日 09-28 00:00 先到即收〕"
)
assert s['log'][-1].startswith('2026-09-27 18:15 R540'), 'unexpected last log line'
s['log'].append(LINE)
json.dump(s, io.open(STATE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

EXP = 'docs/status-export.json'
e = json.load(io.open(EXP, encoding='utf-8'))
e['export_ts'] = NOW.strftime('%Y-%m-%dT%H:%M:%S+08:00')
DEPT_T = (
    "R541: idle-fast (fast path, five checks quiet + probes adjudicated green, no four-step entry) - "
    "window round 1/6 no commit (new window R541-R546; full-6 batch at R546; day boundary 09-28 00:00 collects first); "
    "orders 35 anchor mtime 13:53:11 unchanged; ledger five-mode 31 = anchor (mtime 15:15:21 unchanged); "
    "decisions 56 = anchor; production=open intact (tick 540->541); "
    "backlog top gated (#78 SC-003 footage top census-card-v7-vertical 09-27 12:32 = R511 self-produced, FluxVerse capture not arrived, stays blocked status-line; "
    "#59 REACT due 09-28 with daily_brief 09-28 to be produced on window day; #63 C-00030/31 supply-gated; "
    "#70 OSS next window 09-29 21:40; #31 ch.5 v3 pending session leg; #57 10-07; W40 weekly audit + monthly stats note open 09-28; #67 anti-bloat; #80 benchmarks 10-01); "
    "tree = expected self state only (no index.lock; untracked .sc003 tmp = SC-003 batch-unclosed expected; "
    ".c3-tmp r541 evidence to next batch commit; HEAD=4d8d3df unchanged = no bm-a activity); "
    "probes: board 0 FAIL exit 0 (5 ideas 10 drafts 5 in production), readiness 3 external blockers 0 findings exit 1, "
    "loop 2F+24W all in-case (outage 49min 09-26 historical; account-lag beats541>tick540 = in-flight done-beat transient, closing tick541 balances); "
    "op-red logged honestly: probe first run PS > redirect wrote UTF-16 display files (R532/R536/R539 in-case repeat; probes ran twice same readings; zero disk side-effect) "
    "-> python subprocess capture rerun overwrote UTF-8 evidence in place; redundant r541_probesum.txt deleted; r519_probe.json renamed r541_probe.json"
)
found = False
for d in e['depts']:
    if d.get('n') == '工程技术部':
        d['t'] = DEPT_T
        found = True
assert found, 'eng dept row missing'
json.dump(e, io.open(EXP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# cleanup + rename (evidence hygiene)
if os.path.exists('.c3-tmp/r541_probesum.txt'):
    os.remove('.c3-tmp/r541_probesum.txt')
if os.path.exists('.c3-tmp/r519_probe.json'):
    os.replace('.c3-tmp/r519_probe.json', '.c3-tmp/r541_probe.json')

# round-trip verify
s2 = json.load(io.open(STATE, encoding='utf-8'))
e2 = json.load(io.open(EXP, encoding='utf-8'))
print('STATE_OK tick=%s ts=%s log_n=%d' % (s2['tick'], s2['ts'], len(s2['log'])))
print('EXPORT_OK ts=%s dept_t_head=%s' % (e2['export_ts'], e2['depts'][7]['t'][:24]))
print('TASK=%s' % s2['task'][:60])
