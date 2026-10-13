# -*- coding: utf-8 -*-
"""R2217 waiting-state close (night window 00:00-08:00, MV V3 lane yield).

Mandate law: state accounting MUST go through finalize_state (tech#149,
R2136) - no hand-written log.append + json.dump. Export refresh skipped
(fresh from R2214, no live-facts change, <=24h law).
"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'src', 'os'))
import close_commit as cc  # noqa: E402

log_line = (
    "2026-10-14 04:4x R2217: 等待态一行声明收轮（夜窗 00:00-08:00·MV V3 成片冲刺 CEO 优先线让路窗）——"
    "五查全静（own orders 锚 O-20261008-1105 维持+origin_gap_check QUIET ahead0 behind0·R1500 前置位+"
    "group_scan fresh 04:36 全静：DECISIONS 水位 155 维持零新行/LEDGER @BigStream 值锚零新转办/"
    "ORDERS rows=382 tail '10-13 23:5x'==stored 零新令/ORDERS-ORIGIN-DELTA delta=0/DIGEST-SUPPLY quiet）+"
    "三探针=board 0 FAIL/readiness 阻塞皆外部 CEO 面/loop_health 3 FAIL 皆在案史实（09-26/09-28/10-12 停跳族+"
    "account-drift adjudicated WARN 维持）零新发现；fire_consume 单命令直发 F-180 SC-005-07 flight-4="
    "no-fire rc1（gate-static-no-go·worst-case free 824MB<2048·load-class-starved=tech#135 吞吐预探+"
    "tech#141 载类饥饿面在册）→F-180~184 让位结转维持（tech#105 序律不变）；main#32 ① V3 成片落位核对面="
    "negative（release/ 仅 10-08 样片 v1/v2 旧档·kf-demo 正典根最新 mp4 10-13 03:21·成片未呈·MV 会话域零接触）；"
    "main#21 AIHOT resume 夜窗腿=前置「MV 静默或显式收口」不中（VRAM 824MB 饿态）→让路维持·撤旗+worker-restart+"
    "tech#126 冒烟=08:00 晨窗判读位；main#32 ② tech#92/#126 权威窗+③晨窗回滚序=08:00 到点轮领；"
    "P2/P3 队头盘点=GPU-gated/到点件族（tech#1/#3/#9 独占窗·explore#14=10-17 W42 期·explore#22 ≥10-17 窗）"
    "真无可执行 CPU 面件；三队补货=真无新种子如实注记零膨胀（no-fire 门族读数已尽在册 tech#135/#141）。"
    "waiting: MV V3 成片冲刺让路（夜窗）ETA 2026-10-14 08:00 晨窗判读。"
)

res = cc.finalize_state(log_line, tick=2217)
print("finalize:", res)

files = [
    "data/pipeline/fire-consume-ledger.jsonl",
    "src/os/state.json",
]
msg = (
    "R2217 waiting-state night window: MV V3 lane yield maintained "
    "(fire F-180~184 no-fire, VRAM 824MB starved + load-class-starved); "
    "five checks quiet; probes green (3 hist outage FAIL); V3 final cut "
    "not yet delivered; AIHOT resume deferred to 08:00 window; queue "
    "triage all gated, no new seeds honestly noted. [via bm-a]"
)
r = cc.run_close_commit(files=files, message=msg, root=ROOT, push=True,
                        expect_tick=2217)
print("close:", r)
