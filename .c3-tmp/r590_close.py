# -*- coding: utf-8 -*-
# R590 close-out (idle-fast, window 6/6 full = R585-R590): tick 589->590, append R590 log line
# (five checks quiet + probes in-case green), refresh ts/task/focus; refresh status-export.json
# (P-61 light: export_ts + OS row). Batch commit R585-R590 + push after close (os-protocol sec.6, P-62(3)).
import io, json, os, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = os.path.join(ROOT, "src", "os", "state.json")
XP = os.path.join(ROOT, "docs", "status-export.json")

now = time.strftime("%Y-%m-%d %H:%M:%S")
now_hm = time.strftime("%H:%M")

state = json.load(io.open(SP, encoding="utf-8"))
assert state["tick"] == 589, "expected tick 589, got %s" % state["tick"]

log_r590 = (
    u"2026-09-28 " + now_hm + u" R590: idle-fast（快速路径·五静+探针定谳绿·不进开轮四步·**新窗 6/6 满=R585-R590 本轮 "
    u"batch commit 收账+push**〔os-protocol §6 并窗律 P-62 ③·commit 注区间·窗重置 1/6〕）——①无新令（orders 35 O-件零新增"
    u"零编辑=r590_all·锚=O-20260927-1050 mtime 13:53:11 未动·edited 检测行=锚件自身小数秒伪差〔R534 在案口径〕）+无新集团"
    u"转办（ledger 五模式正法复计 31=锚零新行〔mtime 00:43:06 未动〕+行级 diff vs r589_lednew5.txt 基线 NEW=0 GONE=0=零新 "
    u"CEO 令级事件〔#67 触发律不解锁〕）+无新决策行（decisions UTF8 非空行 63=锚零新·mtime 00:10:41 未动）+production=open "
    u"自愈核在位零翻正（r590_all·STATE_PRODUCTION=open TICK=589→收账 tick590）；②backlog 顶行不可认领（头部 done 项维持·"
    u"首开门控项=#70 OH 下窗 09-29 21:40 后开〔首窗三切片 R432/R458/R459 齐=窗面满〕/#67 史源耗尽待新 CEO 令级事件〔反膨"
    u"胀律照守·本轮行级 diff 零新〕/#66 blocked-on-CEO 物理件/#63 图鉴 C-00030/C-00031 锚正典位直查双 False〔r590_all "
    u"ANCHORS_COUNT=20 尾=C-00029〕supply-gated 照守/#59 REACT 09-29 热点窗届日即领〔日报 09-28 在案·DAILY_0929=False 未"
    u"届〕/#31 有声线 ch.5 v3 稿未落 supply-gated 照守〔novel 尾 09-25 17:58 零新写盘〕/#78 SC-003-01 渲染腿素材面前置维持 "
    u"blocked〔footage 顶=census-card-v7-vertical 09-27 12:32=R511 自产源件非 FluxVerse 实录·r590 到位核验零新实录=呈报状"
    u"态行在案不催办〕/#57 替代率首报 10-07 挂账/长期挂账面维持〔#4 量产注记/#15 口吻批/#17 needs-CEO/#27 发布锁内〕/"
    u"W40 周审+月度统计注记已毕〔R575/R576〕/#80 global-benchmarks 10-01 并窗/自进池仅 B5 开项 gated〔零造活〕）；③树态="
    u"仅自产预期态（无 index.lock False 实证·M state.json+M status-export.json=R585-R589 idle-fast 自记账并窗预期态非 "
    u"bm-a 迹象〔os-protocol §6〕+untracked 94〔r590 探针时点计数〕列面全属 .c3-tmp 49/.sc003-tmp 41/.sc003-v3-tmp 1/"
    u"MC-DIGEST-v8-tmp 3 四族零外族路径〔R589 85→本轮 94 差 9=r589 close+verify 三件+r590 探针族增量生命周期非他人写盘〕"
    u"·HEAD=3679fcb R579-R584 窗 batch commit 未变 git log 零插队=无 bm-a 活跃写盘迹象〔backlog 00:35=R577/"
    u"HQ-FEEDBACK 00:28=R576/station-reviews 00:45=R578/finished+cards README 00:45=R578/status-export 02:33=R589/"
    u"renders README 09-27 13:53/video README 09-27 11:38/storylines 四线尾=09-25~09-27 已知足迹全未动〕）；④例行件：日报 "
    u"09-28 在案不重跑（R575 补产·DAILY_0928=True）·W40 周审在案（R576 交付）·global-benchmarks day0 ≤7 跳过（下期 10-01="
    u"#80 并窗）·T1 催办=已裁项停用口径·当日无集团层新 open 问题=HQ-FEEDBACK 不写〔零膨胀〕·tokens:local=0〔五查+三探针"
    u"纯脚本零本地模型调用·P-54⑤ 计量律如实记〕·发布锁=M5 账号物理件不变（未上线未测量）；⑤三探针定谳=board 0 FAIL rc 0"
    u"（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现 rc 1〔账号批次①+6/10 GATE+#17〕=阻塞"
    u"≠失败口径〔48 renders 全注账〕/loop_health 2 FAIL+25 WARN 全定谳在案类零新增（FAIL① heartbeat-outage 49min 09-26 "
    u"20:24→21:13=R425/R426 同事件足迹裁定不重复触发·FAIL② account-lag done590>tick589=轮内瞬态 tick590 收账自平 "
    u"R173/R577/R579-R588 先例·25 WARN 皆在案史实类）——**窗满触发=batch commit R585-R590（本窗六轮五查全静·commit 注区间）"
    u"·窗重置 1/6**。下轮 R591 快速路径首查（锚=orders 35〔13:53:11〕/ledger 五模式 31〔00:43:06·行级基线=.c3-tmp/"
    u"r590_lednew5.txt〕/decisions 63〔00:10:41〕），全静即 idle-fast（新窗 R591-R596·满 6 或跨日 09-29 00:00 先到即收）。"
)

state["tick"] = 590
state["log"].append(log_r590)
state["ts"] = now
state["task"] = log_r590.split(" ", 2)[2][:60]
state["focus"] = (
    u"R591: 快速路径五查首行——锚=orders 35〔13:53:11〕·ledger 五模式 31〔00:43:06·行级基线=.c3-tmp/r590_lednew5.txt〕"
    u"·decisions 63〔00:10:41〕——无在飞件·#63 C-00030/31 双 False 照守（R590 核）——可认领活优先序=①#67 DIGEST 触发律"
    u"（ledger/decisions 新 CEO 令级事件落账才解·锚动即核）②#59 REACT 09-29 日窗（届日=daily_brief 09-29 铁律先补产后"
    u"日报 top 择优）③#70 OH 下窗 09-29 21:40 后开④C-01/C-02 记票随 HQ 决策轮（本司意见已出零动作）——五查静且无可领="
    u"idle-fast 一行收账·新窗 1/6=R591-R596（满 6 或跨日 09-29 00:00 先到即收=batch commit 收账+push）；任一破静"
    u"（新令/锚动/可领活/探针新红/树异常）=照实活轮收账即 commit"
)

json.dump(state, io.open(SP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# --- status-export refresh (P-61, light per idle-fast precedent: export_ts + OS row derived from this round)
xp = json.load(io.open(XP, encoding="utf-8"))
xp["export_ts"] = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
for row in xp["outs"]:
    if row[0] == u"OS 循环":
        row[1] = (
            u"tick 590：R590（idle-fast 快速路径·五静+探针定谳绿——orders 35/ledger 五模式 31 行级 diff 零新/decisions 63 "
            u"三锚全未动·#63 C-00030/31 双 False 照守·#78 素材面前置 blocked 维持·探针 board 0F/readiness 3 外部 0F/"
            u"loop 2F 在案类+25W 在案类）——R585-R590 窗 6/6 满 batch commit 收账（本 commit 注区间）·窗重置 R591-R596 1/6"
        )
json.dump(xp, io.open(XP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("CLOSE OK: state tick=%d ts=%s" % (state["tick"], now))
print("TASK=%s" % state["task"])
print("LOG_TAIL_COUNT=%d" % len(state["log"]))
