# -*- coding: utf-8 -*-
"""R2223 waiting-state close (night window 00:00-08:00) via finalize_state canon path."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, r"src\os")
import close_commit

log_line = (
    "2026-10-14 05:4x R2223: 等待态一行收账（夜窗 00:00-08:00）：R2222 后 ~6min 状态零漂移，五查全静="
    "own orders 锚 O-20260908-1105 mtime 10-08 12:08 维持+origin_gap_check QUIET ahead0 behind0（R1500 前置位）+"
    "group_scan 六面 fresh 05:43 全静（DECISIONS truly_new=0 水位 155 维持+LEDGER @BigStream 5 行值守锚零新转办+"
    "ORDERS rows=382 tail '10-13 23:5x'==stored 零新行+DIGEST-SUPPLY quiet〔v20 卡覆盖 10-14〕+ORDERS-ORIGIN-DELTA delta=0）+"
    "树=MV-lane 预期脏面零锁（mv0001/mv001 域 MV sprint 会话件+tests/test_drama_takt.py+tools/drama_takt_probe.py 他窗在飞件·"
    "R1745 零接触承继）零 bm-a 新写盘迹象；三探针带内=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面"
    "（账号批次①+M4 GATE 6/10+#17 needs-CEO）+2 发现 react-v16/digest-v20 unannot=F-183/184 fire 窗登记即清预期态"
    "（R2118 裁定维持）/loop_health 3F+299W 皆在案史实（三 outage 窗=pause-让路窗族+drift 21=adjudicated 基线带内）；"
    "fire 面=fire_consume --ledger 正身直发=no-fire rc1 reason=card-no-fire: gate-static-no-go;vram-face worst-case free 743MB"
    "<guard 2048MB;load-class-starved（05:43 收据·ledger 行随本 commit 入账）→F-180 SC-005-07 flight-4+F-181 REACT-v15+"
    "F-182 DIGEST-v19+F-183 REACT-v16+F-184 DIGEST-v20 五件 fire-ready carried（真窗=util/VRAM 门开·fire_window_card 唯一仲裁面）；"
    "main#32 三联守望=V3 成片仍未落位（fire 卡 mv probe 静默面维持+release/ 目录未现+kf-demo 顶件 23:57 r977 fix3 已消费·查看位零接触）；"
    "队列盘点=queue_status fresh 05:43 实读零漂移（backlog 114 项 claimable 8 皆他窗 lane/gated〔head #110 Toonflow LEG-3=VRAM 门控位〕+"
    "main claimable 3 皆 MV 域零接触查看位/守望位+tech claimable 2 皆 08:00 权威窗 gated〔#92/#126·R2218 窗中读数已作证据底座·"
    "tech#156 归因腿同窗触发判定〕+explore 0）→真无可执行项=一行声明收轮合法（waiting: fire VRAM 门闭+权威窗 08:00 未到·"
    "ETA 10-14 08:00 tech#92/#126 权威窗读数〔PASS 或 fallback T1 60→55 判读+tech#156 归因腿触发判定〕+晨窗回滚序"
    "〔re-enable MiniGameOllama 双任务+LEG-3 未毕收 app 窗口位〕+VRAM 门开即 fire 接力 F-180→184·保护态豁免面=GPU 占用让路"
    "〔CEO 用机让路律族·夜窗 MV 优先线〕）；例行件=10-14 日报在案不重跑（R2205 补产·一份为真相）·W42 周审在案（R2011）·"
    "W42 自驱提案 P-7 已交·GB §④ 下期 10-15 ≤7d 跳过+export=skip <24h（R2222 commit 后 <1h 龄·实况零变化·tech#148 强制律下 "
    "skip=零写入安全态·live 三行核读仍准）·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·T1 催办无超线项"
    "（账号物理件=呈现状行不催办）·tokens:local=0（探针/直读/fire 卡读=档案读写零本地模型产出调用·P-54⑤ 计量律）；"
    "队列补货步=真无新种子如实注记零膨胀（六面静+探针带内+fire 门读数=既有结构面〔tech#135/#141 在册〕·禁凑数律）·"
    "临时件清理钩=本轮读数会话内直读零落盘·close 脚本照 tech#81 自含律入账——"
    "下轮=等待态续（等待对象同上不重扫）·08:00 权威窗届即转读数链（tech#92/#126 判读+tech#156 触发判定+晨窗回滚序）。"
)

res = close_commit.finalize_state(
    log_line,
    focus="08:00 tech#92/#126 authority window reads (PASS or T1 60->55 fallback + tech#156 attribution-leg trigger) + morning rollback re-enable MiniGameOllama dual tasks + F-180 relay on util/VRAM gate open + main#32 V3 film watch (R2223)",
)
print("finalize_state ->", res)

rc, lines = close_commit.run_close_commit(
    files=[r"src\os\state.json", r"data\pipeline\fire-consume-ledger.jsonl"],
    message=(
        "R2223 waiting-state night window: five checks quiet, probes in-band; fire no-fire rc1 "
        "(gate-static-no-go, worst-case free 743MB < 2048 guard, load-class-starved - MV V3/CEO lane yield) "
        "F-180..184 carried; main#32 V3 final cut not landed (no release dir, top file still r977 fix3); "
        "queue triage all gated (tech#92/#126 at 08:00 authority window, tech#156 rides same readout), "
        "zero drift from R2222; no new seeds honestly noted. Next=08:00 authority window reads + morning "
        "rollback + fire relay on VRAM gate open. [via bm-a]"
    ),
    push=True,
    expect_tick=2223,
)
print("run_close_commit rc=", rc)
for ln in lines:
    print("  ", ln)
