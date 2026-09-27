# -*- coding: utf-8 -*-
# R570 idle-fast close-out: window 6/6 FULL (R565-R570) -> this round fires the window batch commit R565-R570 + push
# state.json log/tick/ts/task/focus + status-export export_ts/dept-t, then caller runs git add/commit/push
import json, io, datetime, sys
try:
    sys.stdout.reconfigure(errors='replace')
except Exception:
    pass

NOW = datetime.datetime.now()
HHX = '%s:%sx' % (NOW.strftime('%H'), NOW.strftime('%M')[0])  # e.g. 23:1x
LINE = (
    "2026-09-27 " + NOW.strftime('%H:%M') + " R570: idle-fast（快速路径·五静+探针定谳绿·不进开轮四步·**新窗 6/6 满=R565-R570 本轮 batch commit 收账+push**〔os-protocol §6 并窗律 P-62 ③·commit 注区间〕）——"
    "①无新令（orders 35 件零新增·锚=O-20260927-1050-HQ-C mtime 13:53:11 未动·edited 检测行=锚件自身小数秒伪差〔R534 在案口径〕）"
    "+无新集团转办（ledger 五模式 raw-line 正则复计 31=锚零新行·mtime 15:15:21 未动·diff 腿 31-new=r533 基线行号漂移伪差已知〔主判据=计数+mtime 双证〕）"
    "+无新决策行（decisions UTF8 非空行 56=锚零新·mtime 15:14:19 未动）"
    "+production=open 自愈核在位零翻正（r570_check·STATE_PRODUCTION=open TICK=569→收账 tick570）；"
    "②backlog 顶行不可认领（#75/#74/#71/#73/#79/#77/#64 done 维持·#78 SC-003-01 渲染腿素材面前置维持 blocked〔footage 顶=census-card-v7-vertical 09-27 12:32=R511 自产源件非 FluxVerse 实录·r570 到位核验零新实录=呈报状态行在案不催办〕"
    "/#59 REACT 09-28 热点窗届日即领〔daily_brief 09-28 缺=明届日随窗补产·DAILY_0928 预检 False 在案·今日 09-27 " + HHX + " 未届〕"
    "/#63 图鉴 C-00030/C-00031 锚正典位直查双 False〔20 锚尾三止 C-00029〕supply-gated 照守"
    "/#70 OH 下窗 09-29 21:40 后开〔首窗三切片 R432/R458/R459 齐=窗面满〕"
    "/#31 有声线 ch.5 v3 稿未落=会话创作腿 supply-gated 照守〔novel 尾 09-25 17:58 零新写盘〕"
    "/#57 替代率首报 10-07 挂账/W40 周自审 09-28 开周+月度统计注记首件 ≤09-30 随 W40 周审轮"
    "/#67 DIGEST 史源耗尽待 ledger 新 CEO 令级事件〔反膨胀律照守〕/#80 global-benchmarks 10-01 并窗"
    "/自进池 open 项全门控〔B5 账号期站内采样/B3 周更 W40/C4 首进链件触发位〕）；"
    "③树态=仅自产预期态（无 index.lock False 实证·M state.json+M status-export.json=R569 idle-fast 自记账并窗预期态非 bm-a 迹象〔os-protocol §6〕"
    "+untracked 80〔r570 探针时点计数〕列面全属 .c3-tmp/.sc003 两族零外族路径〔vs R569 73 差 7=r570 探针族生命周期自产件〔all/board/check/lednew/loop/readiness 六件〕非他人写盘〕"
    "·HEAD=3dcb2a3 R559-R564 窗 batch commit 未变 git log 零插队=无 bm-a 活跃写盘迹象〔backlog 14:35=R517/HQ-FEEDBACK 12:26=R511/station-reviews 14:35=R517/renders README 13:53=R515/finished 14:35=R517/cards README 14:35=R517/video README 11:38/storylines 四线尾=09-25~09-27 已知足迹全未动〕）；"
    "④例行件：日报 09-27 在案不重跑〔09-28 件=明届日随窗补产·DAILY_0928 预检 False 在案〕·W39 周审在案〔W40 明日 09-28 开周+月度统计注记首件 ≤09-30〕"
    "·global-benchmarks day3 ≤7 跳过〔下期 10-01=#80 并窗〕·T1 催办=已裁项停用口径"
    "·当日无集团层新 open 问题=HQ-FEEDBACK 不写〔零膨胀〕·tokens:local=0〔五查+三探针纯脚本零本地模型调用·P-54⑤ 计量律如实记〕"
    "·发布锁=M5 账号物理件不变（未上线未测量）；"
    "⑤三探针定谳=board 0 FAIL（5 题 10 稿·5 in production·rc 0）"
    "/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现 rc 1〔账号批次①+6/10 GATE+#17〕=阻塞≠失败口径〔48 renders 全注账〕"
    "/loop_health 2 FAIL+24 WARN 全定谳在案类零新增（FAIL① heartbeat-outage 49min 09-26 20:24→21:13=R425 调度器漏触发同事件足迹 R426 已裁定不重复触发"
    "·FAIL② account-lag done570>tick569=本轮在飞 done-beat 先行于收账 tick 瞬态 +1〔R527-R569 同型基线·新断洞判据 lag ≥2 未破线·本轮收账 tick570 即平〕"
    "·24 WARN=13 log-order+11 heartbeat-gap 全 ≤09-27 13:55 史实零新增·backlog 80 项 66 done 82% 燃尽）；"
    "——操作红如实入账=轮首 git status --short && git log 复合命令=PS5.1 && 不支持 ParserError（R539 ① 同型第三次·零盘面副作用）→正法即改=; 分隔符轮内咬住（R564 已将 R534 律扩至内联命令·本犯=扩律后再犯·机制位=启动器模板句首 git 双查固定 && 写法=下轮呈 bm-a 面任务书微修候选非循环自改）；"
    "——探针复制律第七十八证（r570_all.py=r569_all.py 经 python -c 单命令复制+改指+stdout errors=replace 前置=R565 操作红②处方持续生效·本轮 stdout 零崩溃 exit 0=修红生效实证·零 PS 往返零历史件覆写=R462 防再犯律+R466 预核律双守·单命令非复合=R541 律面内）；"
    "——窗满收账：batch commit R565-R570 注区间+push·收 .c3-tmp r565-r570 探针证据件+state.json+status-export.json 三族〔.sc003 两族=SC-003-01 在途批 #78 blocked 中间件维持 untracked 留档·R547-R564 三窗先例同判·批闭〔素材到位渲染走链〕时随批收账〕"
    "·下轮=R571 新窗 1/6（R571-R576）·跨日 09-28 00:00 届日件三面随窗领：日报 09-28 缺则先补产+REACT 09-28 热点窗领+W40 周自审开周+月度统计注记首件 ≤09-30"
)

STATE = 'src/os/state.json'
s = json.load(io.open(STATE, encoding='utf-8'))
assert 'R569' in s['log'][-1], 'unexpected last log line: ' + s['log'][-1][:40]
s['tick'] = 570
s['ts'] = NOW.strftime('%Y-%m-%d %H:%M:%S')
content = LINE.split('R570: ', 1)[1]
s['task'] = content[:60]
s['focus'] = (
    "R571: 新窗 1/6（R571-R576·满 6 或跨日 09-28 00:00 先到即收）·跨日届日件三面随窗领：日报 09-28 缺则先补产（python src/intel/daily_brief.py）+REACT 09-28 热点窗领（#59）+W40 周自审开周（self_audit.py 出数据包）+月度统计注记首件 ≤09-30"
    "——锚=orders 35〔mtime 13:53:11〕·ledger 五模式 31〔mtime 15:15:21·raw-line 正则脚本单一通道〕·decisions 56〔mtime 15:14:19〕"
    "——全静即 idle-fast 一行收账（新窗计 1/6 不 commit）·任一异常/可认领活=转全任务书实活轮照走"
)
s['log'].append(LINE)
json.dump(s, io.open(STATE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

EXP = 'docs/status-export.json'
e = json.load(io.open(EXP, encoding='utf-8'))
e['export_ts'] = NOW.strftime('%Y-%m-%dT%H:%M:%S+08:00')
DEPT_T = (
    "R570: idle-fast (fast path, five checks quiet + probes adjudicated green) - window round 6/6 of R565-R570 FULL -> this round fires window batch commit R565-R570 with range annotation + push (os-protocol sec6 window law); "
    "orders 35 anchor O-20260927-1050 mtime 13:53:11 unchanged (edited-detection self-hit = known sub-second artifact, R534 canon); "
    "ledger five-mode raw-line regex recount 31 = anchor (mtime 15:15:21 unchanged; diff-leg 31-new = r533 baseline line-number drift artifact, primary = count+mtime); "
    "decisions 56 = anchor (mtime 15:14:19 unchanged); production=open intact (tick 569->570); "
    "backlog top gated (#75/#74/#71/#73/#79/#77/#64 done kept; #78 SC-003 footage top census-card-v7-vertical 09-27 12:32 = R511 self-produced, FluxVerse capture not arrived, stays blocked status-line; "
    "#59 REACT due 09-28 with daily_brief 09-28 produce-on-window-day (DAILY_0928 pre-check False on file); #63 C-00030/31 supply-gated (20 anchors tail C-00029); "
    "#70 OSS next window 09-29 21:40; #31 ch.5 v3 pending session leg; #57 10-07; W40 weekly-audit opens 09-28 + monthly-stats note first piece <=09-30; #67 anti-bloat; #80 benchmarks 10-01); "
    "tree = expected self state (no index.lock; M state.json+M status-export.json = R569 idle-fast self-accounting, os-protocol sec6; untracked 80 all .c3-tmp/.sc003 families, zero external-family paths, delta 7 vs R569 = r570 probe lifecycle; HEAD=3dcb2a3 batch unchanged, zero bm-a activity); "
    "probes: board 0 FAIL exit 0 (5 ideas 10 drafts 5 in production), readiness 3 external blockers 0 findings exit 1 (48 renders annotated), "
    "loop 2F+24W all in-case (outage 49min 09-26 historical R425/R426 adjudicated not re-triggered; account-lag done570>tick569 = in-flight done-beat transient +1 constant baseline, lag>=2 not broken, closing tick570 balances; "
    "24 WARN = 13 log-order + 11 heartbeat-gap all <=09-27 13:55 historical, zero new; backlog 80 items 66 done 82% burn); "
    "op-red honestly logged: round-start PS inline git '&&' compound = ParserError (R539 type-1 third recurrence despite R564 law extension, zero disk impact) -> semicolon separator fixed in-round; mechanism note = launcher template first git double-check uses '&&', candidate for bm-a taskbook micro-fix, not self-edited by loop; "
    "probe-copy law 78th proof (r570_all.py copied from r569_all.py via single non-compound python -c with renames + stdout errors=replace per R565 op-red prescription, zero console crash exit 0 = fix verified effective); "
    "window batch commit collects .c3-tmp r565-r570 probe evidence + state.json + status-export.json; .sc003 families stay untracked (SC-003-01 in-flight batch #78 blocked, R547-R564 three-window precedent, collected at batch close when footage arrives); "
    "next round R571 = new window 1/6 (R571-R576); due-day items on 09-28 crossing: daily 09-28 produce + REACT hot window + W40 weekly-audit open + monthly stats note first piece <=09-30"
)
found = False
for d in e['depts']:
    if d.get('n') == '工程技术部':
        d['t'] = DEPT_T
        d['s'] = 1
        found = True
assert found, 'eng dept row missing'
json.dump(e, io.open(EXP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# round-trip verify (ASCII slice patterns only, per R539 addendum law)
s2 = json.load(io.open(STATE, encoding='utf-8'))
e2 = json.load(io.open(EXP, encoding='utf-8'))
lastline = s2['log'][-1]
eng = [d for d in e2['depts'] if d.get('n') == '工程技术部'][0]
print('STATE_OK tick=%s ts=%s log_n=%d' % (s2['tick'], s2['ts'], len(s2['log'])))
print('EXPORT_OK ts=%s eng_s=%s eng_s_type=%s' % (e2['export_ts'], eng['s'], type(eng['s']).__name__))
print('TASK_HEAD=%r' % s2['task'][:40].encode('unicode-escape')[:80])
print('LASTLOG_HAS_R570=%s' % ('R570' in lastline))
print('FOCUS_HAS_R571=%s' % ('R571' in s2['focus']))
