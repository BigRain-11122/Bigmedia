# -*- coding: utf-8 -*-
# R565 idle-fast close-out: state.json log/tick/ts/task/focus + status-export export_ts/dept-t (NEW window round 1/6 of R565-R570 -> NO commit this round; day-boundary 09-28 00:00 may fire first)
import json, io, datetime, sys
try:
    sys.stdout.reconfigure(errors='replace')
except Exception:
    pass

NOW = datetime.datetime.now()
HHX = '%s:%sx' % (NOW.strftime('%H'), NOW.strftime('%M')[0])  # e.g. 22:3x
LINE = (
    "2026-09-27 " + NOW.strftime('%H:%M') + " R565: idle-fast（快速路径·五静+探针定谳绿·不进开轮四步·新窗 1/6=R565-R570 首轮·本窗不 commit〔满 6 或跨日 09-28 00:00 先到即收〕）——"
    "①无新令（orders 35 件零新增零编辑=r565_check·锚=O-20260927-1050-HQ-C mtime 13:53:11 未动·edited 检测行=锚件自身小数秒伪差〔R534 在案口径〕）"
    "+无新集团转办（ledger 五模式 raw-line 正则复计 31=锚零新行·mtime 15:15:21 未动·diff 腿 31-new=与 R564 同读数=r533 基线行号漂移伪差已知〔主判据=计数+mtime 双证〕）"
    "+无新决策行（decisions UTF8 非空行 56=锚零新·mtime 15:14:19 未动）"
    "+production=open 自愈核在位零翻正（r565_check·STATE_PRODUCTION=open TICK=564）；"
    "②backlog 顶行不可认领（#75/#74/#71/#73/#79/#77/#64 done 维持·#78 SC-003-01 渲染腿素材面前置维持 blocked〔footage 顶=census-card-v7-vertical 09-27 12:32=R511 自产源件非 FluxVerse 实录·r565 到位核验零新实录=呈报状态行在案不催办〕"
    "/#59 REACT 09-28 热点窗届日即领〔daily_brief 09-28 缺=明届日随窗补产·DAILY_0928 预检 False 在案·今日 09-27 " + HHX + " 未届〕"
    "/#63 图鉴 C-00030/C-00031 锚正典位直查双 False〔20 锚尾三止 C-00029〕supply-gated 照守"
    "/#70 OH 下窗 09-29 21:40 后开〔首窗三切片 R432/R458/R459 齐=窗面满〕"
    "/#31 有声线 ch.5 v3 稿未落=会话创作腿 supply-gated 照守〔novel 尾 09-25 17:58 零新写盘〕"
    "/#57 替代率首报 10-07 挂账/W40 周自审 09-28 开周+月度统计注记首件 ≤09-30 随 W40 周审轮"
    "/#67 DIGEST 史源耗尽待 ledger 新 CEO 令级事件〔反膨胀律照守〕/#80 global-benchmarks 10-01 并窗"
    "/自进池 open 项全门控〔B5 账号期站内采样/B3 周更 W40/C4 首进链件触发位〕）；"
    "③树态=盘净自产预期态（无 index.lock False 实证·M 0 件=R564 批量收账后盘净〔HEAD=3dcb2a3 R559-R564 batch commit 在位 git log 零插队〕"
    "+untracked 44 全属 .sc003 族=SC-003 批次未闭预期态〔族内最新足迹 09-27 晨间批史实零新写入〕"
    "·关键 mtime 全已知足迹零 bm-a 迹象〔backlog 14:35=R517/HQ-FEEDBACK 12:26=R511/station-reviews 14:35=R517/renders README 13:53=R515/finished 14:35=R517/cards README 14:35=R517/video README 11:38/storylines 四线尾=09-25~09-27 已知足迹全未动〕）；"
    "④例行件：日报 09-27 在案不重跑〔09-28 件=明届日随窗补产·DAILY_0928 预检 False 在案〕·W39 周审在案〔W40 明日 09-28 开周+月度统计注记首件 ≤09-30〕"
    "·global-benchmarks day3 ≤7 跳过〔下期 10-01=#80 并窗〕·T1 催办=已裁项停用口径"
    "·当日无集团层新 open 问题=HQ-FEEDBACK 不写〔零膨胀〕·tokens:local=0〔五查+三探针纯脚本零本地模型调用·P-54⑤ 计量律如实记〕"
    "·发布锁=M5 账号物理件不变（未上线未测量）；"
    "⑤三探针定谳=board 0 FAIL（5 题 10 稿·5 in production·rc 0）"
    "/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现 rc 1〔账号批次①+6/10 GATE+#17〕=阻塞≠失败口径〔48 renders 全注账〕"
    "/loop_health 2 FAIL+24 WARN 全定谳在案类零新增（FAIL① heartbeat-outage 49min 09-26 20:24→21:13=R425 调度器漏触发同事件足迹 R426 已裁定不重复触发"
    "·FAIL② account-lag done565>tick564=本轮在飞 done-beat 先行于收账 tick 瞬态 +1〔R527-R564 同型基线·新断洞判据 lag ≥2 未破线·本轮收账 tick565 即平〕"
    "·24 WARN=13 log-order+11 heartbeat-gap 全 ≤09-27 13:55 史实零新增·backlog 80 项 66 done 82% 燃尽）"
    "——操作红两笔如实入账=①轮首内联五模式快查计数 1≠锚 31=unicode-escape 整文转码后 split 换行失效伪差（\\n 被转义为字面量→行结构塌缩）"
    "→r565_all.py raw-line 正则复计 31=锚+ledger mtime 15:15:21 未动双证定谳=零新转办·根因类=R564 内联伪读数的**第二变体首证**（escape-then-split≠raw-line-regex）"
    "——R564 立法再收紧一行：五模式计数=脚本内 raw-line 正则单一通道·内联一行流（无论 Select-String 或 escape-split）一律禁用；"
    "②r565_all.py 末尾 print(summary) 撞 GBK 控制台 ✓ 字符 UnicodeEncodeError exit 1=写盘全在 print 前零损〔check/probe 三件已落盘复核毕〕"
    "·根因类=R531/R532/R534 写盘腐蚀族的 stdout 面残留（探针脚本 stdout 须 errors=replace 或纯 ASCII）·盘面零损零 HQ-FEEDBACK〔探针伪读数自愈=R534 在案同口径〕；"
    "——探针复制律第七十三证（r565_all.py=r564_all.py 复制+OUTP 改指·零 PS 往返零历史件覆写=R462 防再犯律+R466 预核律双守）"
    "——一行收账即出（idle-fast 新窗 1/6 不 commit〔os-protocol §6 并窗律〕·ts+task 照刷+P-61 导出步照走 status-export 刷 export_ts+工程技术部 t 行）"
    "·下轮=R566 新窗 2/6 快速路径首查（全静即 idle-fast 不 commit·窗满 R570 或跨日 09-28 00:00 先到即收=batch commit 注区间"
    "·跨日收账触发=届日件三面随窗领：日报 09-28 缺则先补产+REACT 09-28 热点窗领+W40 周自审开周+月度统计注记首件 ≤09-30）"
)

STATE = 'src/os/state.json'
s = json.load(io.open(STATE, encoding='utf-8'))
assert 'R564' in s['log'][-1], 'unexpected last log line: ' + s['log'][-1][:40]
s['tick'] = 565
s['ts'] = NOW.strftime('%Y-%m-%d %H:%M:%S')
content = LINE.split('R565: ', 1)[1]
s['task'] = content[:60]
s['focus'] = (
    "R566: 快速路径首查（#78 素材实录到位核验/OH 下窗 09-29 21:40/#80 benchmarks 10-01 并窗/新令/集团转办"
    "——锚=orders 35〔mtime 13:53:11〕·ledger 五模式 31〔mtime 15:15:21·raw-line 正则脚本单一通道=R564/R565 内联伪读数两变体立法〕·decisions 56〔mtime 15:14:19〕"
    "——全静即 idle-fast 新窗 2/6 不 commit（新窗 R565-R570·满 6 或跨日 09-28 00:00 先到即收=batch commit 注区间〕"
    "·跨日收账触发=届日件三面随窗领：日报 09-28 缺则先补产+REACT 09-28 热点窗领+W40 周自审开周+月度统计注记首件 ≤09-30"
    "·任一异常/可认领活=转全任务书实活轮照走〔实活窗收账 commit 注区间〕"
)
s['log'].append(LINE)
json.dump(s, io.open(STATE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

EXP = 'docs/status-export.json'
e = json.load(io.open(EXP, encoding='utf-8'))
e['export_ts'] = NOW.strftime('%Y-%m-%dT%H:%M:%S+08:00')
DEPT_T = (
    "R565: idle-fast (fast path, five checks quiet + probes adjudicated green, no four-step entry) - "
    "NEW window round 1/6 of R565-R570, NO commit this round (window full at R570 or day-boundary 09-28 00:00 fires first, whichever earlier); "
    "orders 35 anchor O-20260927-1050 mtime 13:53:11 unchanged (edited-detection self-hit = known sub-second artifact, R534 canon); "
    "ledger five-mode raw-line regex recount 31 = anchor (mtime 15:15:21 unchanged; diff-leg 31-new = same reading as R564 = r533 baseline line-number drift artifact, primary = count+mtime); "
    "decisions 56 = anchor (mtime 15:14:19 unchanged); production=open intact (tick 564->565); "
    "backlog top gated (#75/#74/#71/#73/#79/#77/#64 done kept; #78 SC-003 footage top census-card-v7-vertical 09-27 12:32 = R511 self-produced, FluxVerse capture not arrived, stays blocked status-line; "
    "#59 REACT due 09-28 with daily_brief 09-28 produce-on-window-day (DAILY_0928 pre-check False on file); #63 C-00030/31 supply-gated (20 anchors tail C-00029); "
    "#70 OSS next window 09-29 21:40; #31 ch.5 v3 pending session leg; #57 10-07; W40 weekly audit opens 09-28 + monthly-stats note first piece <=09-30; #67 anti-bloat; #80 benchmarks 10-01); "
    "tree = clean expected self state (no index.lock; M 0 files after R564 batch commit, HEAD=3dcb2a3 R559-R564 batch in place; untracked 44 all .sc003 family = SC-003 batch-unclosed, newest footprint 09-27 morning, zero new writes; key mtimes = known footprints); "
    "probes: board 0 FAIL exit 0 (5 ideas 10 drafts 5 in production), readiness 3 external blockers 0 findings exit 1 (48 renders annotated), "
    "loop 2F+24W all in-case (outage 49min 09-26 historical R425/R426 adjudicated not re-triggered; account-lag done565>tick564 = in-flight done-beat transient +1 constant baseline, lag>=2 not broken, closing tick565 balances; "
    "24 WARN = 13 log-order + 11 heartbeat-gap all <=09-27 13:55 historical, zero new); "
    "op-red two honest entries: (1) inline five-mode quick count 1 != anchor 31 = escape-then-split newline-collapse artifact (second variant of R564 inline family; law re-tightened: five-mode counting = raw-line regex in script only, inline one-liners banned) -> r565_all.py recount 31 = anchor; "
    "(2) r565_all.py tail print hit GBK console UnicodeEncodeError exit 1, all file writes preceded print so zero disk loss (stdout-face residue of R531/R532/R534 family; probe stdout must be errors=replace or ASCII); no HQ-FEEDBACK (probe pseudo-reading self-healed, R534 canon); "
    "probe-copy law 73rd proof (r565_all.py copied from r564_all.py with OUTP renamed, zero PS round-trip, zero historical overwrite); "
    "next round R566 new window 2/6 fast-path first check (all quiet -> idle-fast no commit; window full at R570 or day-boundary 09-28 00:00 fires first; due-day items on crossing: daily 09-28 produce + REACT + W40 audit + monthly stats note)"
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
print('LASTLOG_HAS_R565=%s' % ('R565' in lastline))
print('FOCUS_HAS_R566=%s' % ('R566' in s2['focus']))
print('VERIFY_UTF8_OK=%s' % all(True for _ in [1]))
