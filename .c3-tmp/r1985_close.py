# -*- coding: utf-8 -*-
"""R1985 round close: production round (DIGEST v18 CPU pre-stage).

Two-stage commit law (tech#27 / os-protocol 6 v1.12): stage A commits the
deliverables (cards + backlog/queue ledgers + probes evidence + refreshed
export), then finalize_state + stage B commits state.json with the
close script self-included (tech#81).
Fire card 16:14:52 = no-fire (gate double-fail free 481MB util 100; mv
file-face quiet 133.6min x hardware busy = ComfyUI full-MV i2v wave in
flight, CEO priority lane defer correct side). Waiting-window take =
#67 trigger-law new CEO-order cluster -> DIGEST v18 (R1871 precedent).
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(_HERE, "..", "src", "os")))

from close_commit import finalize_state, run_close_commit  # noqa: E402

LOG_LINE = u"2026-10-11 16:2x R1985: 生产轮·#67 触发律直领新令级事件簇——DIGEST v18《城市盘点 018·全曲冲刺日数字盘点》CPU 预置腿当轮交付（等待窗取活=fire 卡 no-fire 窗内 CPU 面·R1871 范式·实活轮）——①轮首五查全静=own orders 顶 O-20260908-1105 mtime 12:08:14==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）+group_scan 四面全静=decisions truly_new=0 水位 141 维持+ledger @BigStream 5 行==值守锚零新转办+ORDERS 行水位第六窗读数=quiet（rows=270 tail_key='10-11 13:4x'==R1979 落库基线·tech#103 判据连续第六窗过）+HQ orders mtime 14:00:46==R1978 消费锚零新行+无 index.lock+树态=MV sprint 会话域在飞件零接触（R1745 承继）+例行件预检=10-11 日报在案/W41 周审在案/GB §④ v1.3 下期 10-15 ≤7d 跳过/export_ts 14:20 <24h；②fire_window_card 16:14:52 复查=no-fire（gate 双闸败 free_min 481MB<2048+util_max 100>80·band 6 稳态·**mv quiet 133.6min=文件面静×硬件忙**〔ComfyUI 全曲 i2v 波在渲=CEO 优先线让路正确侧〕·probe not-resident 反事实 fly evictable 9799·readings-age gate 54s tech#90 在役）→SC-005-04/05/06 三件 fire-ready 维持结转（F-176/177/178·main#16·S1+E4 双材料 turnkey·**断轮承记**=同轮号先行体 15:52-16:02 SC-005-04 S1 三尝试〔300s timeout→ollama exit 3→GPU-guard DEFER util 93 占用窗〕死于收账前零 state 落账=与 16:14:52 no-fire 读数同向互证·三件 fire-ready 判定不变〔无 mp3/srt 产出〕·其 tmp 脚本 asr_diff/same_text_r1985.py 留盘不收账=fire 窗消费轮接手）；③等待窗照取可执行项（O-20261009-1246 项 c）=三队 fresh 复读（main 全 gated·#4 MD-0002 T2I gated CEO 点头/#12 gate 关 R1946/#13/#14-16 SC-005 系·tech 全 done 或 gated〔#92 10-12 08:00 权威窗/#93/#101/#102/#98/#100/#14/#15/#17/#63〕·explore 全 done 或到点 10-13+〔#22/#14 ≥10-17·#18 10-16·#26 回访 10-13/15〕）+**#67 触发律命中=10-11 全曲冲刺日 CEO 令簇七行**（11:3x 全曲整改冲刺令六项整改+剧本四律/12:1x 追补令⑦-⑩/12:5x 全机队完整版冲刺令最高优先/13:0x 导演席审查硬门+tw-mv-director skill 立档/13:2x 女主每曲独立选角律/13:2x 执行落地机制令/13:4x MV 评审分层机制定谳令）=F-170 v17〔10-08/09 双日〕后新落令级事件簇零消费→**DIGEST v18 CPU 预置腿交付**：M1 机核 18 断言全绿（r1985_build_digest18.py 四族=A1 七令标签在册+10-11 行计数 13·A2 六 CEO verbatim 引文〔13:4x 评审分层主引文「mv的评审要分层级，导演是总控，专家是群审，我只是最后决定上线与否的。」连续子句拆两行+11:3x 剧本四律尾链「一定要把故事写好！！！！！！逻辑通顺！！！！自然！！！立意高！！！！」+12:5x「不要制作30秒的了！要给我弄完整版！能直接发布的！」+13:2x 选角律/元批评两引+13:0x 导演审引〕·A3 skill/CASTING-LAW/EXECUTION-FIX-LEDGER/CEO-FEEDBACK 四正典件在位·A4 D-20261011-06 在 decisions+F-170..175 六件登记·A5 em 全行 ≤28.75〔引文行 26.00em 驱动=h2_size 32 档 v10/v16 长引文先例带·首轮 40 档 26.00>23.0 FAIL 轮内改档复跑全绿〕）+M2 poster 真渲 exit 0（1080×1080·cover t=0.150s·副产 mp4 105KB 入 -tmp）+验图五检 5/5 一次过（多模态十行转写全对位·引语跨两行=设计排版 v5/v12/v14/v15/v16/v17 先例同型·零重叠零越界零截断·AIGC 角标清晰·来源行「基于硅基城市真实事件（全曲冲刺日令批台账档案）」闭合·层级留白明确）+M3「城市盘点 018」四禁零中+M4 四检过（红线五条/三重标注图内双落/来源双落/编辑价值=1 句「我只是最后决定上线与否的」放权定谳 vs 单日 7 令 6 成品全速反差链·F-042 对照结构同源第十七证·十八连母题续·脱敏律核=全部数字台账读数〔令行数/成品登记数/整改项/剧本律/秒数/曲数/机制数/回访日期〕·P1 边界=他司执行面不入卡面）；④台账=backlog #67 R1985 注（预置腿全档）+main 队新行 17（DIGEST v18 GPU 尾=gated fire 窗 M4.5 七席+E4+F-179 登记·**fire 窗消费序定谳=SC-005-04→05→06 三连先发〔F-176/177/178〕→v18 F-179 后段位**·e4-material 件=fire 窗前 CPU 顺手步预载 R1875 范式）+tech 队补货 #105（fire 窗多件消费序律=本轮真发现种子·四件竞争同窗首次·SOP 先行腿随 main#17 落·工具面候选倾向判负·观察位随下个 fire 窗消费轮并读）+export_refresh live 三行刷（tech#70 writer 正法·live-clock export_ts·大白话律 tech#74）；⑤三探针=probe_capture 紧凑面 r1985_probes.txt（board rc0 0 FAIL〔5 题 10 稿 5 in production〕/readiness rc1 3 阻塞皆外部 CEO 面〔账号批次①+M4 GATE 6/10+#17 needs-CEO〕0 发现〔78 renders unannot=0〕/loop_health rc1 2F+247W 皆在案史实〔两 outage=09-26/09-28 已裁定不重触发·drift 17==基线带内·新 WARN state-ts-stale 44min=本轮收账 ts 刷新即清〕）；⑥例行件=10-11 日报在案不重跑（R1927 一份为真相）+W42 周审 10-12 届日即领+GB §④ 下期 10-15 跳过+meme V1 成片查看位双路径零件维持（shortvideo-dept+meme-daily-v1 双路径零 mp4=bm-a 会话域在飞零接触·R1899 锚维持）+HQ-FEEDBACK 不写（无集团层新 open 问题·零膨胀）+tokens:local=0（本轮零本地模型调用=纯机检+FFmpeg 渲染+多模态验图·P-54⑤ 计量律如实记）。下轮=R1986 快速路径首查=fire 窗首查（GO 即 SC-005-04 S1 连发→05→06 三连 F-176/177/178 后段 v18 F-179）+10-12 08:00 tech#92 雷达标定权威窗（zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补）+W42 周审 10-12。收账两段制=交付件先行 commit+state 记账后段 commit（tech#27/os-protocol §6 v1.12）。"

FOCUS = u"R1986 快速路径首查（fire 卡复查〔GO 即发 SC-005-04 S1 连发→05→06 三连 F-176/177/178·后段 DIGEST v18 M4.5+E4+F-179·e4-material 预载顺手步〕+10-12 08:00 tech#92 雷达标定判据窗届日即领〔zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补〕+W42 周审 10-12+meme V1 成片查看位+MD-0002 T2I gated CEO 点头维持）"

DELIVERABLES = [
    "data/storylines/cards/MC-20261011-DIGEST-v18/cards.json",
    "data/storylines/cards/MC-20261011-DIGEST-v18/subs.srt",
    "data/storylines/cards/MC-20261011-DIGEST-v18/MC-20261011-DIGEST-v18.png",
    "src/os/backlog.md",
    "state/queue/main.md",
    "state/queue/tech.md",
    "docs/status-export.json",
    ".c3-tmp/r1985_build_digest18.py",
    ".c3-tmp/r1985_checks.py",
    ".c3-tmp/r1985_orders_rows.py",
    ".c3-tmp/r1985_probes.txt",
    ".c3-tmp/r1985_export_patch.json",
]


def main():
    # stage A: deliverables first (two-stage law)
    rc_a, lines_a = run_close_commit(
        files=DELIVERABLES,
        message=("R1985 deliverables: DIGEST v18 (full-sprint-day digest) CPU "
                 "pre-stage M0-M4 - 18 assertions green (7 MV-domain order "
                 "labels 10-11, 6 CEO verbatim quotes, 4 canonical artifacts, "
                 "D-20261011-06, F-170..175 six registrations, em band 32 "
                 "quote-line driver), poster render + frame-verify 5/5, "
                 "M3/M4 pass; backlog #67 note; main queue row 17 (GPU tail "
                 "F-179 gated fire window, consumption order SC-005 x3 "
                 "first); tech seed #105 fire-window multi-piece order law; "
                 "export live refreshed [via bm-a]"),
    )
    for ln in lines_a:
        print(ln.encode("ascii", "replace").decode("ascii"))
    print("stage A rc=%s" % rc_a)
    if rc_a != 0:
        return rc_a
    # stage B: state accounting (self-include law commits this script too)
    summary = finalize_state(log_line=LOG_LINE, focus=FOCUS)
    print("finalize tick=%s ts=%s wm_added=%s orders_wm_rows=%s log_len=%s"
          % (summary["tick"], summary["ts"], summary["wm_added"],
             summary["orders_wm_rows"], summary["log_len"]))
    rc_b, lines_b = run_close_commit(
        files=["src/os/state.json"],
        message=("R1985 loop close: production round - DIGEST v18 CPU "
                 "pre-stage delivered in waiting window (fire card "
                 "no-fire 16:14:52 gate double-fail free 481MB util 100; "
                 "mv file-face quiet 133.6min x hardware busy = ComfyUI "
                 "full-MV i2v wave in flight, CEO priority lane defer "
                 "correct side); SC-005-04/05/06 fire-ready carried "
                 "F-176/177/178; v18 GPU tail queued row 17 with "
                 "consumption order (SC-005 x3 first, F-179 after); ORDERS "
                 "row-watermark quiet 6th window tech#103; probes "
                 "in-band board rc0 [via bm-a]"),
    )
    for ln in lines_b:
        print(ln.encode("ascii", "replace").decode("ascii"))
    print("stage B rc=%s" % rc_b)
    return rc_b


if __name__ == "__main__":
    sys.exit(main())
