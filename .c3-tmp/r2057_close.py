# -*- coding: utf-8 -*-
"""R2057 round-close: git autonomy enforcement close (CEO 2026-10-12 15:0x
ruling narrows the nod-rule to metis-only; FluxGroup repos self-managed ->
R2052-R2056 batch landed as 80ca7600, this close lands R2057 accounting).

Consumed this round:
- D-20261012-03 (BigDomain receipt-cleanup decision; BigStream non-exec face
  -> acknowledged, zero action) -> decisions watermark 151->152
- HQ ORDERS rows 297->300 (O-20261012-1340/1400/1420/1510 MV sprint orders;
  bm-a MV sprint session domain, zero touch) -> orders_row_watermark stored
- fire_consume verbatim round-start command: no-fire rc1 (CEO pause window
  expected), F-180/F-181/F-182 stay fire-ready
Queue restock: main#25 night-window MV i2v watch position.
"""

import io
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src", "os"))

import close_commit  # noqa: E402
import group_scan  # noqa: E402

LOG = (
    "2026-10-12 15:3x R2057: git 收口实活轮（CEO 10-12 15:0x 勘正执法：git 点头制收窄至 "
    "metis 团队工程·FluxGroup 全仓全自主 → R2052-R2056 积压账面 17 件外科 pathspec 收口 "
    "commit 80ca7600·loop_health account-uncommitted+round-debris 双 WARN 就此自清）——"
    "①轮首五查=origin_gap_check QUIET ahead0 behind0+group_scan 两新面：D-20261012-03"
    "（BigDomain 回执清账+任务板补货·执行司=BigDomain·本司非执行面=知悉零动作·本 commit "
    "含行号=送达回执·watermark 151→152 收讫）+ORDERS rows 297→300 三新行"
    "（O-20261012-1340/1400/1420/1510=MV 产线冲刺令簇·SHOTLIST-FULL-v2 定稿+夜窗双机 i2v "
    "并行+10-14 呈片时钟=bm-a MV sprint 会话域在执·OS 循环零接触·orders_row_watermark "
    "300 收讫）·ledger @BigStream 5 行=值判锚静·@六司 1 行=P-2026-10-09-01 历史件已收讫·"
    "DIGEST-SUPPLY quiet（v19 staged 卡覆盖）；②fire_consume verbatim 轮首命令=no-fire rc1"
    "（cold-skip-no-admissible-credit·CEO pause 窗预期态·F-180 flight-4+F-181 REACT-v15+"
    "F-182 DIGEST-v19 三件 fire-ready 结转维持）；③三探针=board 0 FAIL（5 题 10 稿 "
    "5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17）0 发现 "
    "78 renders unannot=0/loop_health 3 FAIL 皆在案史实带（09-26 49min+09-28 609min+10-12 "
    "57min outage 史实非新事件）·board --quiet 传参笔误=R72/R98 同型操作红直跑即净；"
    "④队列补货 1 条真种子=main#25 夜窗 MV i2v 双机并行开工位守望（O-20261012-1420/1510 "
    "冲刺时钟锚·10-13 晨收片核对面·查看位零接触）；⑤例行件=10-12 日报在案不重跑"
    "（R2008 一份为真相）·W42 周审在案·GB §④ v1.3 10-08=4d ≤7d 跳过下期 ~10-15·"
    "export_ts 15:10:58 ≤24h 新鲜·live 三行仍准（最近实物=aihot_watchdog v1.109+8 测）"
    "不刷=产品优先律 §2 节流·T1 催办无超线项（账号物理件=呈现状行不催办）·HQ-FEEDBACK "
    "不写（无集团层新 open 问题零膨胀）·tokens:local=0（纯 git/账面零本地模型调用·"
    "P-54⑤ 计量律）；下轮=fire 真开即 F-180 flight-4 单命令先发（F-181/F-182 接力·"
    "tech#105 序律）+tech#92 权威窗 10-13 08:00 判读+main#22 下读 10-13 00:00 常务轮窗后+"
    "main#25 夜窗守望 10-13 晨位"
)

FOCUS = (
    "fire 窗项轮首命令 verbatim 正身照发：python src/os/fire_consume.py --launch "
    "data/storylines/audio/sc005-07-v1-tmp/s1_call.py --ledger（GO=fire→F-180 flight-4 派发"
    "〔preflight 三件首战〕→S1 判词 ≥9=TTS light 续链→F-180 登记·F-181 评审腿后段位；"
    "no-fire rc1=三件维持结转）+tech#92 判据窗 10-13 08:00 重判读数按 resume 分叉"
    "（requeued 池冻结态读数随窗并读）+main#22 下读=10-13 00:00 常务轮窗后"
    "（bill §七 落=标 done·未落+当班空窗=HQ-FEEDBACK 一行呈报位·禁逐轮重扫）+main#25 "
    "夜窗 MV i2v 双机并行开工位守望（10-13 晨收片核对面·查看位零接触）+pause 窗 CPU "
    "职守维持（watchdog PT5M 自巡零干预预期）"
)

QUEUE_ITEM = (
    "25. [R2057 补货] 夜窗 MV i2v 双机并行开工位守望（O-20261012-1420 时钟压缩令+"
    "O-20261012-1510 冲刺确认令锚：今晚 00:00-08:00 bm-a 夜窗〔O-20261012-1505 铁律内〕"
    "+bm-c 各 32 条 i2v 并行→明晨全齐→10-14 呈片时钟——OS 循环守望面=10-13 晨收片核对面"
    "〔i2v 产出件数+夜窗开工回执轻扫·查看位零接触·MV sprint 会话域在飞件禁碰〕）"
    "——10-13 晨窗到点执行"
)

MSG = (
    "R2057 round close: git autonomy enforcement (R2052-R2056 batch 80ca7600 "
    "landed per CEO 10-12 15:0x metis-only nod-rule), D-20261012-03 consumed "
    "to watermark (BigDomain-targeted, non-exec face), ORDERS rows 297->300 "
    "consumed (MV sprint orders ack, zero touch), queue restock main#25 "
    "night-window i2v watch, fire-ready F-180/181/182 deferred (CEO pause "
    "window no-fire rc1); next: F-180 flight-4 on first real fire window, "
    "tech#92 window 10-13 08:00 [via bm-a]"
)


def main():
    # --- queue restock: append main#25 (idempotent) ---
    qpath = os.path.join(ROOT, "state", "queue", "main.md")
    with io.open(qpath, encoding="utf-8", newline="") as f:
        q = f.read()
    if "main#25" in q or "[R2057" in q:
        print("QUEUE-RESTORE-SKIP (marker present)")
    else:
        if q and not q.endswith("\n"):
            q += "\n"
        q += QUEUE_ITEM + "\n"
        with io.open(qpath, "w", encoding="utf-8", newline="") as f:
            f.write(q)
        print("QUEUE-RESTOCK-OK main#25 appended")

    # --- orders watermark: turnkey from group_scan ---
    try:
        owm = group_scan.current_orders_watermark()
    except Exception as exc:  # loud fallback keeps the close alive
        print("WARN orders watermark autodetect failed: %r" % (exc,))
        owm = {"rows": 300, "tail_key": "10-12 15:1x"}
    print("ORDERS-WM %r" % (owm,))

    # --- single-writer state accounting ---
    summary = close_commit.finalize_state(
        log_line=LOG,
        focus=FOCUS,
        tick=2057,
        watermark_add=["D-20261012-03"],
        orders_watermark=owm,
    )
    print("STATE %r" % (summary,))

    # --- pathspec accounting commit + push (self-includes this script) ---
    rc, lines = close_commit.run_close_commit(
        files=["src/os/state.json", "state/queue/main.md"],
        message=MSG,
    )
    for ln in lines:
        print(ln)
    return rc


if __name__ == "__main__":
    sys.exit(main())
