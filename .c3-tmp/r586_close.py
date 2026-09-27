# -*- coding: utf-8 -*-
# R586 close-out (idle-fast): tick 585->586, append R586 log line (five checks quiet + probes
# in-case green), refresh ts/task/focus; refresh status-export.json (P-61 light: export_ts + OS row).
# Window round 2/6 of R585-R590 => NO commit this round (os-protocol sec.6, P-62(3)).
import io, json, os, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = os.path.join(ROOT, "src", "os", "state.json")
XP = os.path.join(ROOT, "docs", "status-export.json")

now = time.strftime("%Y-%m-%d %H:%M:%S")
now_hm = time.strftime("%H:%M")

state = json.load(io.open(SP, encoding="utf-8"))
assert state["tick"] == 585, "expected tick 585, got %s" % state["tick"]

log_r586 = (
    u"2026-09-28 " + now_hm + u" R586: idle-fast（快速路径·五静+探针定谳绿·不进开轮四步·新窗 2/6=R585-R590·本轮不 "
    u"commit〔满 6 或跨日 09-29 00:00 先到即收〕）——①无新令（orders 35 O-件零新增零编辑=r586_all·锚=O-20260927-1050 "
    u"mtime 13:53:11 未动·edited 检测行=锚件自身小数秒伪差〔R534 在案口径〕）+无新集团转办（ledger 五模式正法复计 31=锚"
    u"零新行〔mtime 00:43:06 未动〕+行级 diff vs r585_lednew5.txt 基线 NEW=0 GONE=0=零新 CEO 令级事件〔#67 触发律不"
    u"解锁〕）+无新决策行（decisions UTF8 非空行 63=锚零新·mtime 00:10:41 未动）+production=open 自愈核在位零翻正"
    u"（r586_all·STATE_PRODUCTION=open TICK=585→收账 tick586）；②backlog 顶行不可认领（头部 done 项维持·首开门控项="
    u"#70 OH 下窗 09-29 21:40 后开〔首窗三切片 R432/R458/R459 齐=窗面满〕/#67 史源耗尽待新 CEO 令级事件〔反膨胀律照"
    u"守·本轮行级 diff 零新〕/#66 blocked-on-CEO 物理件/#63 图鉴 C-00030/C-00031 锚正典位直查双 False〔r586_all "
    u"ANCHORS_COUNT=20 尾=C-00029〕supply-gated 照守/#59 REACT 09-29 热点窗届日即领〔日报 09-28 在案·DAILY_0929="
    u"False 未届〕/#31 有声线 ch.5 v3 稿未落 supply-gated 照守〔novel 尾 09-25 17:58 零新写盘〕/#78 SC-003-01 渲染腿"
    u"素材面前置维持 blocked〔footage 顶=census-card-v7-vertical 09-27 12:32=R511 自产源件非 FluxVerse 实录·r586 "
    u"到位核验零新实录=呈报状态行在案不催办〕/#57 替代率首报 10-07 挂账/长期挂账面维持〔#4 量产注记/#15 口吻批/#17 "
    u"needs-CEO/#27 发布锁内〕/W40 周审+月度统计注记已毕〔R575/R576〕/#80 global-benchmarks 10-01 并窗/自进池仅 B5 "
    u"开项 gated〔零造活〕）；③树态=仅自产预期态（无 index.lock False 实证·M state.json+M status-export.json=R585 "
    u"idle-fast 自记账并窗预期态非 bm-a 迹象〔os-protocol §6〕+untracked 58〔r586 探针时点计数〕列面全属 .c3-tmp/."
    u"sc003 两族+MC-DIGEST-v8-tmp 三件+本轮 r586 探针族零外族路径·HEAD=3679fcb R579-R584 窗 batch commit 未变 git "
    u"log 零插队=无 bm-a 活跃写盘迹象〔backlog 00:35=R577/HQ-FEEDBACK 00:28=R576/station-reviews 00:45=R578/"
    u"finished+cards README 00:45=R578/status-export 01:53=R585/renders README 09-27 13:53/video README 09-27 "
    u"11:38/storylines 四线尾=09-25~09-27 已知足迹全未动〕）；④例行件：日报 09-28 在案不重跑（R575 补产）·W40 周审"
    u"在案（R576 交付）·global-benchmarks day0 ≤7 跳过（下期 10-01=#80 并窗）·T1 催办=已裁项停用口径·当日无集团层新 "
    u"open 问题=HQ-FEEDBACK 不写〔零膨胀〕·tokens:local=0〔五查+三探针纯脚本零本地模型调用·P-54⑤ 计量律如实记〕·发"
    u"布锁=M5 账号物理件不变（未上线=未测量）；⑤三探针定谳=board 0 FAIL rc 0（5 题 10 稿·5 in production）/"
    u"readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现 rc 1〔账号批次①+6/10 GATE+#17〕=阻塞≠失败口径〔48 renders 全注"
    u"账〕/loop_health 2 FAIL+25 WARN 全定谳在案类零新增（FAIL① heartbeat-outage 49min 09-26 20:24→21:13=R425/"
    u"R426 同事件足迹裁定不重复触发·FAIL② account-lag done586>tick585=轮内瞬态 tick586 收账自平 R173/R577/R579-"
    u"R585 先例·25 WARN 皆在案史实类〔13 log-order+12 heartbeat-gap〕）——一行收账即出（本轮不 commit·P-61 导出步照"
    u"刷 export_ts）。下轮 R587 快速路径首查（锚=orders 35〔13:53:11〕/ledger 五模式 31〔00:43:06·行级基线=.c3-tmp/"
    u"r586_lednew5.txt〕/decisions 63〔00:10:41〕），全静即 idle-fast（新窗 3/6）。"
)

state["tick"] = 586
state["log"].append(log_r586)
state["ts"] = now
state["task"] = log_r586.split(" ", 2)[2][:60]
state["focus"] = (
    u"R587: 快速路径五查首行——锚=orders 35〔13:53:11〕·ledger 五模式 31〔00:43:06·行级基线=.c3-tmp/r586_lednew5.txt〕"
    u"·decisions 63〔00:10:41〕——无在飞件·#63 C-00030/31 双 False 照守（R586 核）——可认领活优先序=①#67 DIGEST 触发律"
    u"（ledger/decisions 新 CEO 令级事件落账才解·锚动即核）②#59 REACT 09-29 日窗（届日=daily_brief 09-29 铁律先补产后"
    u"日报 top 择优）③#70 OH 下窗 09-29 21:40 后开④C-01/C-02 记票随 HQ 决策轮（本司意见已出零动作）——五查静且无可领="
    u"idle-fast 一行收账·新窗 3/6=R585-R590（本轮不 commit〔满 6 或跨日 09-29 00:00 先到即收〕）；任一破静（新令/锚动/"
    u"可领活/探针新红/树异常）=照实活轮收账即 commit"
)

json.dump(state, io.open(SP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# --- status-export refresh (P-61, light per idle-fast precedent: export_ts + OS row derived from this round)
xp = json.load(io.open(XP, encoding="utf-8"))
xp["export_ts"] = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
for row in xp["outs"]:
    if row[0] == u"OS 循环":
        row[1] = (
            u"tick 586：R586（idle-fast 快速路径·五静+探针定谳绿——orders 35/ledger 五模式 31 行级 diff 零新/decisions 63 "
            u"三锚全未动·#63 C-00030/31 双 False 照守·#78 素材面前置 blocked 维持·探针 board 0F/readiness 3 外部 0F/"
            u"loop 2F 在案类+25W 在案类）——新窗 R585-R590 进行中（本轮 2/6 不 commit·满 6 或跨日 09-29 00:00 先到即收）"
        )
json.dump(xp, io.open(XP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("CLOSE OK: state tick=%d ts=%s" % (state["tick"], now))
print("TASK=%s" % state["task"])
print("LOG_TAIL_COUNT=%d" % len(state["log"]))
