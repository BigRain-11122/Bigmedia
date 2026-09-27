# -*- coding: utf-8 -*-
# R560 idle-fast close-out: state.json log/tick/ts/task/focus + status-export export_ts/dept-t (window round 2/6 of window R559-R564 -> NO commit this round)
import json, io, datetime

NOW = datetime.datetime.now()
HHX = '%s:%sx' % (NOW.strftime('%H'), NOW.strftime('%M')[0])  # e.g. 21:3x
LINE = (
    "2026-09-27 " + NOW.strftime('%H:%M') + " R560: idle-fast（快速路径·五静+探针定谳绿·不进开轮四步·并窗轮 2/6 不 commit）——"
    "①无新令（orders 35 件零新增零编辑=r560_check·锚=O-20260927-1050-HQ-C mtime 13:53:11 未动·edited 检测行=锚件自身小数秒伪差〔R534 在案口径〕）"
    "+无新集团转办（ledger 五模式 unicode-escape 正法复计 31=锚零新行·mtime 15:15:21 未动）"
    "+无新决策行（decisions UTF8 非空行 56=锚零新·mtime 15:14:19 未动）"
    "+production=open 自愈核在位零翻正（r560_check·STATE_PRODUCTION=open TICK=559）；"
    "②backlog 顶行不可认领（#75/#74/#71/#73/#79/#77/#64 done 维持·#78 SC-003-01 渲染腿素材面前置维持 blocked〔footage 顶=census-card-v7-vertical 09-27 12:32=R511 自产源件非 FluxVerse 实录·r560 到位核验零新实录=呈报状态行在案不催办〕"
    "/#59 REACT 09-28 热点窗届日即领〔daily_brief 09-28 缺=明届日随窗补产·DAILY_0928 预检 False 在案·今日 09-27 " + HHX + " 未届〕"
    "/#63 图鉴 C-00030/C-00031 锚正典位直查双 False〔20 锚尾三止 C-00029〕supply-gated 照守"
    "/#70 OH 下窗 09-29 21:40 后开〔首窗三切片 R432/R458/R459 齐=窗面满〕"
    "/#31 有声线 ch.5 v3 稿未落=会话创作腿 supply-gated 照守〔novel 尾 09-25 17:58 零新写盘〕"
    "/#57 替代率首报 10-07 挂账/W40 周自审 09-28 开周+月度统计注记首件 ≤09-30 随 W40 周审轮"
    "/#67 DIGEST 史源耗尽待 ledger 新 CEO 令级事件〔反膨胀律照守〕/#80 global-benchmarks 10-01 并窗"
    "/自进池 open 项全门控〔B5 账号期站内采样/B3 周更 W40/C4 首进链件触发位〕）；"
    "③树态=仅自产预期态（无 index.lock False 实证·M state.json+M status-export.json=R559 idle-fast 自记账并窗预期态非 bm-a 迹象〔os-protocol §6〕"
    "+untracked 49〔r560 探针时点计数〕列面全属 .c3-tmp/.sc003 两族零外族路径〔.sc003 族 42 件=SC-003 批次未闭预期态族内最新足迹 11:48 晨间批史实零新写入"
    "·R559 43 vs 本轮 49 差 6=r559_close.py+r560_all.py+r560 四证据件生命周期非他人写盘〕"
    "·HEAD=fb16775 R553-R558 窗 batch commit 未变 git log 零插队=无 bm-a 活跃写盘迹象〔storylines video 尾 12:49=R512 足迹/novel·audio·comic 尾 09-25"
    "·backlog 14:35=R517·HQ-FEEDBACK 12:26=R511·station-reviews 14:35=R517/renders README 13:53=R515·finished 14:35=R517·cards README 14:35=R517 足迹全未动〕）；"
    "④例行件：日报 09-27 在案不重跑〔09-28 件=明届日随窗补产·DAILY_0928 预检 False 在案〕·W39 周审在案〔W40 明日 09-28 开周+月度统计注记首件 ≤09-30〕"
    "·global-benchmarks day3 ≤7 跳过〔下期 10-01=#80 并窗〕·T1 催办=已裁项停用口径"
    "·当日无集团层新 open 问题=HQ-FEEDBACK 不写〔零膨胀〕·tokens:local=0〔五查+三探针纯脚本零本地模型调用·P-54⑤ 计量律如实记〕"
    "·发布锁=M5 账号物理件不变（未上线=未测量）；"
    "⑤三探针定谳=board 0 FAIL（5 题 10 稿·5 in production·rc 0）"
    "/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现 rc 1〔账号批次①+6/10 GATE+#17〕=阻塞≠失败口径〔48 renders 全注账〕"
    "/loop_health 2 FAIL+24 WARN 全定谳在案类零新增（FAIL① heartbeat-outage 49min 09-26 20:24→21:13=R425 调度器漏触发同事件足迹 R426 已裁定不重复触发"
    "·FAIL② account-lag done560>tick559=本轮在飞 done-beat 先行于收账 tick 瞬态 +1〔R527-R559 同型·新断洞判据 lag ≥2 未破线·本轮收账 tick560 即平〕"
    "·24 WARN=13 log-order+11 heartbeat-gap 全 ≤09-27 13:55 史实零新增·backlog 80 项 66 done 82% 燃尽）"
    "——探针复制律第六十八证（r560_all.py=r559_all.py 复制+OUTP 改指·零 PS 往返零历史件覆写=R462 防再犯律+R466 预核律双守）"
    "——一行收账即出（idle-fast 并窗轮 2/6·本轮不 commit·P-61 导出步照刷 export_ts）"
    "·下轮=R561 快速路径首查（全静即 idle-fast 3/6·跨日 09-28 00:00 先到即收=届日件三面随窗领：日报 09-28 缺则先补产+REACT 09-28 热点窗领+W40 周自审开周+月度统计注记首件 ≤09-30）"
)

STATE = 'src/os/state.json'
s = json.load(io.open(STATE, encoding='utf-8'))
s['tick'] = 560
s['ts'] = NOW.strftime('%Y-%m-%d %H:%M:%S')
content = LINE.split('R560: ', 1)[1]
s['task'] = content[:60]
s['focus'] = (
    "R561: 快速路径首查（#78 素材实录到位核验/OH 切片 4 09-29 21:40 后开/#80 benchmarks 10-01 并窗/新令/集团转办"
    "——锚=orders 35〔mtime 13:53:11〕·ledger 五模式 31〔mtime 15:15:21·unicode-escape 正法〕·decisions 56〔mtime 15:14:19〕"
    "——全静即 idle-fast 并窗轮 3/6 不 commit〔窗 R559-R564·满 6/跨日 09-28 00:00/异常/实活 先到即收〕"
    "·跨日 09-28 00:00 收账触发=届日件三面随窗领：日报 09-28 缺则先补产+REACT 09-28 热点窗领+W40 周自审开周+月度统计注记首件 ≤09-30"
    "·任一异常/可认领活=转全任务书实活轮照走〔实活窗收账 commit 注区间〕"
)
assert s['log'][-1].startswith('2026-09-27 21:25 R559'), 'unexpected last log line'
s['log'].append(LINE)
json.dump(s, io.open(STATE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

EXP = 'docs/status-export.json'
e = json.load(io.open(EXP, encoding='utf-8'))
e['export_ts'] = NOW.strftime('%Y-%m-%dT%H:%M:%S+08:00')
DEPT_T = (
    "R560: idle-fast (fast path, five checks quiet + probes adjudicated green, no four-step entry) - "
    "WINDOW ROUND 2/6 of window R559-R564, NO commit this round (window law os-protocol S6); "
    "orders 35 anchor O-20260927-1050 mtime 13:53:11 unchanged (edited-detection self-hit = known sub-second artifact, R534 canon); "
    "ledger five-mode unicode-escape recount 31 = anchor (mtime 15:15:21 unchanged); decisions 56 = anchor (mtime 15:14:19 unchanged); production=open intact (tick 559->560); "
    "backlog top gated (#75/#74/#71/#73/#79/#77/#64 done kept; #78 SC-003 footage top census-card-v7-vertical 09-27 12:32 = R511 self-produced, FluxVerse capture not arrived, stays blocked status-line; "
    "#59 REACT due 09-28 with daily_brief 09-28 produce-on-window-day (DAILY_0928 pre-check False on file); #63 C-00030/31 supply-gated (20 anchors tail C-00029); "
    "#70 OSS next window 09-29 21:40; #31 ch.5 v3 pending session leg; #57 10-07; W40 weekly audit opens 09-28 + monthly-stats note first piece <=09-30; #67 anti-bloat; #80 benchmarks 10-01); "
    "tree = expected self state only (no index.lock; M state.json+M status-export.json = R559 self-accounting window expected state per os-protocol S6, not bm-a sign; "
    "untracked 49 at probe time all in .c3-tmp/.sc003 families, zero foreign paths (.sc003 family 42 files = SC-003 batch-unclosed, newest footprint 11:48 midday = zero new writes; "
    "R559 43 -> 49 delta 6 = r559_close.py + r560_all.py + r560 four evidence files lifecycle, not third-party writes); HEAD=fb16775 unchanged = no bm-a activity; key mtimes = known footprints); "
    "probes: board 0 FAIL exit 0 (5 ideas 10 drafts 5 in production), readiness 3 external blockers 0 findings exit 1 (48 renders annotated), "
    "loop 2F+24W all in-case (outage 49min 09-26 historical R425/R426 adjudicated not re-triggered; account-lag done560>tick559 = in-flight done-beat transient +1 constant baseline, lag>=2 not broken, closing tick560 balances; "
    "24 WARN = 13 log-order + 11 heartbeat-gap all <=09-27 13:55 historical, zero new); "
    "probe-copy law 68th proof (r560_all.py copied from r559_all.py with OUTP renamed, zero PS round-trip, zero historical overwrite); "
    "next round R561 fast-path first check (all quiet -> idle-fast 3/6; day-boundary 09-28 00:00 fires first -> batch commit window + due-day items: daily 09-28 produce + REACT + W40 audit + monthly stats note)"
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
print('TASK=%s' % s2['task'][:60])
print('LASTLOG_HEAD=%s' % lastline[:40])
print('LASTLOG_HAS_R560=%s' % ('R560' in lastline))
print('FOCUS_HEAD=%s' % s2['focus'][:40])
print('FOCUS_HAS_R561=%s' % ('R561' in s2['focus']))
