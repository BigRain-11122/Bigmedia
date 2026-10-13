# -*- coding: utf-8 -*-
"""R2218 accounting close (tech#149 finalize_state + tech#148 export writer + tech#155 expect_tick)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "src", "os"))
from close_commit import finalize_state, run_close_commit

LOG_LINE = (
    "2026-10-14 04:5x R2218: 等待窗内 P2 可领腿执行轮（夜窗 00:00-08:00·CPU 面·tech#126 夜窗读数面=队列紧凑读数器 head 位）"
    "——①五查全静=own orders 锚 O-20261008-1105 mtime 10-08 12:08 维持+origin_gap_check QUIET ahead0 behind0（R1500 前置位）"
    "+group_scan fresh 04:36 全静承读（R2217 锚 6min 龄·DECISIONS truly_new=0 水位 155+LEDGER @BigStream 零新转办"
    "+ORDERS rows=382 tail '10-13 23:5x'==stored+DIGEST-SUPPLY quiet+ORDERS-ORIGIN-DELTA delta=0）"
    "+树态=MV-lane 预期脏面零锁（R1745 零接触承继）；"
    "②三探针带内=board 0 FAIL/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）"
    "+2 发现 react-v16/digest-v20 unannot=F-183/184 fire 窗登记即清预期态维持/loop_health 3F+299W 皆在案史实（adjudicated 族）；"
    "③**本轮交付=tech#126 窗中读数**（tech#92 10-14 08:00 权威窗前置证据面）——管道健康三证"
    "（api 200 {ok,db:ok}+watchdog pause 22:34 已撤态〔main#21 夜窗〕+score 流 fresh 04:51:54"
    "+content.analyze completed 8942 笔 since 22:35=重排池在磨零 wedge）"
    "+**判据窗预读（窗 10-13 08:00→05:0x）**=json-zhihu-hot 31 scored/max48/ge60=0"
    "（PASS 臂〔头部 ≥3 ≥60〕趋向 FAIL）+全源带 max 48-56（knowledge 51/tech 52/popular 35/英文 RSS decoder 56"
    "·窗内唯一 ≥60=nvidia-blog 73×1）+nonbf_ge60 累计 14→**fallback 臂 T1 60→55 亦有不足风险**"
    "（带顶 ≤56 下 55 阈值 ≈1 件/窗·城市校准版疑似压全源带非仅城市源）——08:00 compose 窗=判读正身（本读=证据输入非预判）；"
    "④fire 面=F-180 正身直发 no-fire rc1 reason=probe-face-service-anomaly;load-class-starved"
    "（04:46 收据·VRAM 11482/12282 free ~800MB+util 55%=MV V3 渲染窗持续占卡·ollama 服务自身健康 HTTP 200×10 模型"
    "=吞吐探针饿面非服务坏）→F-180~184 五件 fire-ready carried 维持；"
    "⑤main#32 V3 成片仍未落位（kf-demo 最新件 23:57 r977 fix3 波维持·GPU 占用 55%=其窗在跑·查看位零接触）；"
    "⑥队列补货步=tech#156 真种子入队（T1 60→55 fallback 不足风险面·评分带全局压缩归因腿·gated 08:00 判读窗读数驱动触发）"
    "·tech#126 注记固化为 08:00 窗读数底座；临时件清理=r2218 探针/锚件 7 件删净（evidence 件 r2218_t126_midwindow.json 入账）；"
    "例行件=HQ-FEEDBACK 不写（零集团层新 open 问题）+T1 催办剔除维持（账号物理件=呈现状行不催办）"
    "+tokens:local=0（psql 直读/探针=零本地模型产出调用·P-54⑤ 计量律）"
    "——下轮=08:00 tech#92/#126 权威窗读数（PASS/ fallback T1 60→55 判读+tech#156 归因腿触发判定）"
    "+晨窗回滚序（re-enable MiniGameOllama 双任务+LEG-3 未毕收 app 窗口位）+VRAM 门开即 fire 接力 F-180→184"
)
summary = finalize_state(
    LOG_LINE,
    focus=("08:00 tech#92/#126 authority window reads (PASS or T1 60->55 fallback + tech#156 attribution-leg trigger) "
           "+ morning rollback re-enable MiniGameOllama dual tasks + F-180 relay on util/VRAM gate open + main#32 V3 film watch (R2218)"),
)
print(summary)

EXPORT_PATCH = {
    "live": [
        "当前活：夜窗值守+tech#126 窗中读数已落（管道健康零 wedge；判据窗预读 zhihu max48/ge60=0→08:00 权威窗判读）。",
        "最近实物：AIHOT 判据窗预读证据件（管道健康三证+全源评分带读数+fallback 55 不足风险发现），2026-10-14 04:5x。",
        "下个里程碑：08:00 tech#92/#126 权威窗执行（PASS 或 T1 60→55 fallback+归因腿）；fire 五件候 VRAM 开窗发射；V3 成片 main#32 跟进。",
    ],
}
EXPORT_DO = ("R2218 夜窗 P2 腿执行轮：tech#126 窗中读数交付（AIHOT 管道健康三证+判据窗预读 zhihu 31/max48/ge60=0"
             "→PASS 臂趋向 FAIL+fallback T1 55 不足风险新发现=tech#156 种子）；fire 门 VRAM 800MB 饿空维持 F-180~184 carried；"
             "main#32 V3 成片未落维持；五查全静。")

rc, lines = run_close_commit(
    files=["src/os/state.json",
           "state/queue/tech.md",
           ".c3-tmp/r2218_t126_midwindow.json",
           ".c3-tmp/r2218_close.py"],
    message=(
        "R2218: waiting-window P2 leg executed - tech#126 mid-window readout "
        "delivered (AIHOT pipeline health 3-evidence: api ok + score flow "
        "fresh 04:51 + 8942 analyze completed since 22:35 revive, zero "
        "wedge; tech#92 criterion-window pre-read: zhihu-hot 31 scored "
        "max48 ge60=0 -> PASS branch trending FAIL, whole-band ceiling "
        "48-56 -> T1 60->55 fallback insufficiency risk seeded as "
        "tech#156 attribution leg, decision stays at 08:00 window); fire "
        "no-fire rc1 (VRAM ~800MB starved by MV V3 render, ollama itself "
        "healthy) F-180..184 carried; main#32 film not landed; five faces "
        "quiet; next=08:00 authority window [via bm-a]"
    ),
    export_patch=EXPORT_PATCH,
    export_do=EXPORT_DO,
    expect_tick=2218,
)
for line in lines:
    print(line)
print("RC=%d" % rc)
sys.exit(rc)
