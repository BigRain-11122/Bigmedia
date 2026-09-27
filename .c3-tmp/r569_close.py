# -*- coding: utf-8 -*-
# R569 idle-fast close-out: state.json log/tick/ts/task/focus + status-export export_ts/dept-t (window round 5/6 of R565-R570 -> NO commit this round; R570 window full or day-boundary 09-28 00:00 fires first)
import json, io, datetime, sys
try:
    sys.stdout.reconfigure(errors='replace')
except Exception:
    pass

NOW = datetime.datetime.now()
HHX = '%s:%sx' % (NOW.strftime('%H'), NOW.strftime('%M')[0])  # e.g. 23:0x
LINE = (
    "2026-09-27 " + NOW.strftime('%H:%M') + " R569: idle-fast（快速路径·五静+探针定谳绿·不进开轮四步·新窗 5/6=R565-R570·本窗不 commit〔满 6 或跨日 09-28 00:00 先到即收〕）——"
    "①无新令（orders 35 件零新增零编辑=r569_check·锚=O-20260927-1050-HQ-C mtime 13:53:11 未动·edited 检测行=锚件自身小数秒伪差〔R534 在案口径〕）"
    "+无新集团转办（ledger 五模式 raw-line 正则复计 31=锚零新行·mtime 15:15:21 未动·diff 腿 31-new=r533 基线行号漂移伪差已知〔主判据=计数+mtime 双证〕）"
    "+无新决策行（decisions UTF8 非空行 56=锚零新·mtime 15:14:19 未动）"
    "+production=open 自愈核在位零翻正（r569_check·STATE_PRODUCTION=open TICK=568）；"
    "②backlog 顶行不可认领（#75/#74/#71/#73/#79/#77/#64 done 维持·#78 SC-003-01 渲染腿素材面前置维持 blocked〔footage 顶=census-card-v7-vertical 09-27 12:32=R511 自产源件非 FluxVerse 实录·r569 到位核验零新实录=呈报状态行在案不催办〕"
    "/#59 REACT 09-28 热点窗届日即领〔daily_brief 09-28 缺=明届日随窗补产·DAILY_0928 预检 False 在案·今日 09-27 " + HHX + " 未届〕"
    "/#63 图鉴 C-00030/C-00031 锚正典位直查双 False〔20 锚尾三止 C-00029〕supply-gated 照守"
    "/#70 OH 下窗 09-29 21:40 后开〔首窗三切片 R432/R458/R459 齐=窗面满〕"
    "/#31 有声线 ch.5 v3 稿未落=会话创作腿 supply-gated 照守〔novel 尾 09-25 17:58 零新写盘〕"
    "/#57 替代率首报 10-07 挂账/W40 周自审 09-28 开周+月度统计注记首件 ≤09-30 随 W40 周审轮"
    "/#67 DIGEST 史源耗尽待 ledger 新 CEO 令级事件〔反膨胀律照守〕/#80 global-benchmarks 10-01 并窗"
    "/自进池 open 项全门控〔B5 账号期站内采样/B3 周更 W40/C4 首进链件触发位〕）；"
    "③树态=仅自产预期态（无 index.lock False 实证·M state.json+M status-export.json=R568 idle-fast 自记账并窗预期态非 bm-a 迹象〔os-protocol §6〕"
    "+untracked 73〔r569 探针时点计数〕列面全属 .c3-tmp/.sc003 两族零外族路径〔R568 65 vs 本轮 73 差 8=r568 收账四证据件+close.py+r569_mk/all/lednew 探针族生命周期非他人写盘〕"
    "·HEAD=3dcb2a3 R559-R564 窗 batch commit 未变 git log 零插队=无 bm-a 活跃写盘迹象〔backlog 14:35=R517/HQ-FEEDBACK 12:26=R511/station-reviews 14:35=R517/renders README 13:53=R515/finished 14:35=R517/cards README 14:35=R517/video README 11:38/storylines 四线尾=09-25~09-27 已知足迹全未动〕）；"
    "④例行件：日报 09-27 在案不重跑〔09-28 件=明届日随窗补产·DAILY_0928 预检 False 在案〕·W39 周审在案〔W40 明日 09-28 开周+月度统计注记首件 ≤09-30〕"
    "·global-benchmarks day3 ≤7 跳过〔下期 10-01=#80 并窗〕·T1 催办=已裁项停用口径"
    "·当日无集团层新 open 问题=HQ-FEEDBACK 不写〔零膨胀〕·tokens:local=0〔五查+三探针纯脚本零本地模型调用·P-54⑤ 计量律如实记〕"
    "·发布锁=M5 账号物理件不变（未上线未测量）；"
    "⑤三探针定谳=board 0 FAIL（5 题 10 稿·5 in production·rc 0）"
    "/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现 rc 1〔账号批次①+6/10 GATE+#17〕=阻塞≠失败口径〔48 renders 全注账〕"
    "/loop_health 2 FAIL+24 WARN 全定谳在案类零新增（FAIL① heartbeat-outage 49min 09-26 20:24→21:13=R425 调度器漏触发同事件足迹 R426 已裁定不重复触发"
    "·FAIL② account-lag done569>tick568=本轮在飞 done-beat 先行于收账 tick 瞬态 +1〔R527-R568 同型基线·新断洞判据 lag ≥2 未破线·本轮收账 tick569 即平〕"
    "·24 WARN=13 log-order+11 heartbeat-gap 全 ≤09-27 13:55 史实零新增·backlog 80 项 66 done 82% 燃尽）；"
    "——操作红如实入账=轮首 r569 探针复制通道首试 PS 内联 python -c '&&' 连接=ParserError（R539 ① 同型再犯·零盘面副作用）→正法即改=r569_mk.py 脚本件复制通道（write_file+python 执行·零 PS 管道）=R541 正法〔PS 内联复合命令一律 python 件承载〕延伸执法；"
    "——探针复制律第七十七证（r569_all.py=r568_all.py 经 r569_mk.py 复制+改指+stdout errors=replace 前置=R565 操作红②处方持续生效·本轮 stdout 零崩溃 exit 0=修红生效实证·零 PS 往返零历史件覆写=R462 防再犯律+R466 预核律双守）"
    "——一行收账即出（idle-fast 新窗 5/6 不 commit〔os-protocol §6 并窗律〕·ts+task 照刷+P-61 导出步照走 status-export 刷 export_ts+工程技术部 t 行）"
    "·下轮=R570 窗满 6/6=本窗 batch commit R565-R570 注区间（或跨日 09-28 00:00 先到即收"
    "·跨日收账触发=届日件三面随窗领：日报 09-28 缺则先补产+REACT 09-28 热点窗领+W40 周自审开周+月度统计注记首件 ≤09-30）"
)

STATE = 'src/os/state.json'
s = json.load(io.open(STATE, encoding='utf-8'))
assert 'R568' in s['log'][-1], 'unexpected last log line: ' + s['log'][-1][:40]
s['tick'] = 569
s['ts'] = NOW.strftime('%Y-%m-%d %H:%M:%S')
content = LINE.split('R569: ', 1)[1]
s['task'] = content[:60]
s['focus'] = (
    "R570: 窗满 6/6=本窗 batch commit R565-R570 注区间（或跨日 09-28 00:00 先到即收·届日件三面：日报 09-28 缺则先补产+REACT 09-28 热点窗领+W40 周自审开周+月度统计注记首件 ≤09-30"
    "——锚=orders 35〔mtime 13:53:11〕·ledger 五模式 31〔mtime 15:15:21·raw-line 正则脚本单一通道〕·decisions 56〔mtime 15:14:19〕"
    "——全静即 idle-fast 窗满收账 batch commit 注区间〔R565-R570〕+收 .c3-tmp r565-r570 探针证据件"
    "·任一异常/可认领活=转全任务书实活轮照走〔实活窗收账 commit 注区间〕"
)
s['log'].append(LINE)
json.dump(s, io.open(STATE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

EXP = 'docs/status-export.json'
e = json.load(io.open(EXP, encoding='utf-8'))
e['export_ts'] = NOW.strftime('%Y-%m-%dT%H:%M:%S+08:00')
DEPT_T = (
    "R569: idle-fast (fast path, five checks quiet + probes adjudicated green, no four-step entry) - "
    "window round 5/6 of R565-R570, NO commit this round (window full at R570 = batch commit R565-R570, or day-boundary 09-28 00:00 fires first, whichever earlier); "
    "orders 35 anchor O-20260927-1050 mtime 13:53:11 unchanged (edited-detection self-hit = known sub-second artifact, R534 canon); "
    "ledger five-mode raw-line regex recount 31 = anchor (mtime 15:15:21 unchanged; diff-leg 31-new = r533 baseline line-number drift artifact, primary = count+mtime); "
    "decisions 56 = anchor (mtime 15:14:19 unchanged); production=open intact (tick 568->569); "
    "backlog top gated (#75/#74/#71/#73/#79/#77/#64 done kept; #78 SC-003 footage top census-card-v7-vertical 09-27 12:32 = R511 self-produced, FluxVerse capture not arrived, stays blocked status-line; "
    "#59 REACT due 09-28 with daily_brief 09-28 produce-on-window-day (DAILY_0928 pre-check False on file); #63 C-00030/31 supply-gated (20 anchors tail C-00029); "
    "#70 OSS next window 09-29 21:40; #31 ch.5 v3 pending session leg; #57 10-07; W40 weekly-audit opens 09-28 + monthly-stats note first piece <=09-30; #67 anti-bloat; #80 benchmarks 10-01); "
    "tree = expected self state (no index.lock; M state.json+M status-export.json = R568 idle-fast self-accounting, os-protocol sec6; untracked 73 all .c3-tmp/.sc003 families, zero external-family paths, delta 8 vs R568 = r568 close evidence files + r569 probe lifecycle; HEAD=3dcb2a3 batch unchanged, zero bm-a activity); "
    "probes: board 0 FAIL exit 0 (5 ideas 10 drafts 5 in production), readiness 3 external blockers 0 findings exit 1 (48 renders annotated), "
    "loop 2F+24W all in-case (outage 49min 09-26 historical R425/R426 adjudicated not re-triggered; account-lag done569>tick568 = in-flight done-beat transient +1 constant baseline, lag>=2 not broken, closing tick569 balances; "
    "24 WARN = 13 log-order + 11 heartbeat-gap all <=09-27 13:55 historical, zero new; backlog 80 items 66 done 82% burn); "
    "op-red honestly logged: first PS inline python -c with '&&' = ParserError (R539 type-1 recurrence, zero disk impact) -> fixed in-round via r569_mk.py script-file copy channel (R541 canon extension: PS inline compound commands always via python file); "
    "probe-copy law 77th proof (r569_all.py copied from r568_all.py via r569_mk.py with renames + stdout errors=replace per R565 op-red prescription, zero console crash exit 0 = fix verified effective); "
    "next round R570 window full 6/6 = batch commit R565-R570 with range annotation (or day-boundary 09-28 00:00 first; due-day items on crossing: daily 09-28 produce + REACT + W40 audit + monthly stats note)"
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
print('LASTLOG_HAS_R569=%s' % ('R569' in lastline))
print('FOCUS_HAS_R570=%s' % ('R570' in s2['focus']))
