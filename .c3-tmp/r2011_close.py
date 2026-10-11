#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R2011 close: state tick/log/focus via finalize_state (single-writer law tech#76),
export refresh via tech#70 writer, close commit via run_close_commit (tech#65/81)."""
import datetime
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src", "os"))

from close_commit import finalize_state, run_close_commit  # noqa: E402
from export_refresh import refresh_export  # noqa: E402

LOG_BODY = (
    "生产轮·P2 队头消费=tech#24 local_rate_report 源面切换评估交付（等待窗照取可执行项·W42 周报窗 gate 开=R2008 周审落位·实活轮·计分=实际文件改动 1 分）——"
    "①轮首五查全静=own orders 顶 O-20260908-1105 mtime==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）"
    "+group_scan 固定探针四面全静（decisions truly_new=0 水位 150 维持+ledger @BigStream 5 行==值守锚零新转办"
    "+ORDERS 行水位 quiet rows=270 tail_key='10-11 13:4x'==基线+HQ orders 14:00:46==R1978 消费锚）+无 index.lock"
    "+树态=MV sprint 会话域在飞件零接触（mv001/mv0001/drama_takt/comfy-activity-ledger 批件零碰·R1745 承继）；"
    "②火窗判读=fire_window_card 01:15 no-fire（util-face worst-case 98>80=GUI 群满载带〔gate-credit vram 面过 free 4997/effective 9889 而 util 单闸败〕"
    "·MV sprint quiet 674.7min·probe not-resident）→F-180 SC-005-07/F-181 REACT-v15 评审腿维持 fire-ready gated"
    "+tech#92 权威窗 08:00 未到届日不预扫→P2 队头可即领项=tech#24 领做（tech#1/3/9/18 GPU gated·#14/15/17/38/39 各 gated"
    "·#93 gated MD-0002·#111 低优先续采批触发窗未到·#115/116 观察位不占产线·#118 gated v20）；"
    "③tech#24 交付双落=**切换判据 FAIL 判负留痕**（预注册判据=手记 vs 探针差值连续 2 窗 ≤1 才切："
    "逐日有界窗对比 19 窗全读 09-24→10-12〔v1 教训=meter() 开放式窗逐日须自建 [D,D+1) 行级过滤〕·"
    "**末 2 窗 10-11 diff=+6（手记 28 vs 探针 22）/10-12 diff=+1=判据 FAIL**·历史仅 10-06/10-07+10-07/10-08 两对过线·远窗大差带 10-02 +59/09-25 +34"
    "→手记行维持单一真相〔tech#10 口径承继〕）+差值结构成因双面定谳（探针盲区=direct ollama run 直呼 A/B/暖机无台账行〔R1956 十次 A/B 直呼=10-11 +6 主量正身·probe docstring 既有边界〕"
    "+**跨 lane 污染新发现**=expert-calls/whisper-ledger 行含他窗会话调用〔10-10 wh_ex_p=3 vs 本循环手记 1=并发 whisper v3/MV sprint 会话留行〕"
    "·探针=仓级口径手记=轮级口径=结构性不同源）+**W42 周报首读落位**（local_rate_report 复跑数据包：L2=326〔W39 106/W40 154/W41 65/W42 开窗 1〕×L3=0=替代率 1.0000"
    "+P4 台账 4 行分列防双计·首读行入 2026-W42-self-audit 效率度量节+变更记录行·证据 .c3-tmp/r2011_t24_diff.txt+r2011_local_rate_w42 双件）"
    "+W43 复读条件预注册（r2011_t24_compare.py committed 证据件零新工具）；"
    "④三探针=board 0 FAIL〔5 题 10 稿·5 in production〕/readiness 3 阻塞皆外部 CEO 面〔账号批次①+M4 GATE 6/10+#17 needs-CEO〕0 发现"
    "/loop_health 2F+260W 皆在案史实带内〔两 outage 09-26/09-28 已裁定不重触发·WARN 260 vs R2009 基线 259 +1=本轮近邻轮间隙 heartbeat-gap 顾问级带内〕"
    "（证据 .c3-tmp/r2011_groupscan.txt+r1932_group_scan.txt 刷新件+r2011_fire_card.txt）+queue-glue/dup 守卫例行消费零发现；"
    "⑤例行件=10-12 日报在案不重跑（R2008 补产一份为真相）·W42 周审第 4 期在案（R2008·本轮 tech#24 首读行按任务书 '+W42 周报首读' 条款补入=audit 件增行非重跑）"
    "·GB §④ v1.3 下期 10-15 ≤7d 跳过·meme V1 成片查看位零新到件·krea2 查看位 R1978 锚后零新到件（双查看位禁重扫）"
    "·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·tokens:local=0（纯 CPU 判据执行+探针只读零本地模型调用·P-54⑤ 计量律·A/B 探针重跑零飞）；"
    "⑥队列补货步=tech#119（ad-hoc ollama 直呼 A/B 探针留痕面评估=tech#24 差值构成真发现根因位承接·低优先如实注·非凑数）"
    "+临时件=r2011 证据件七件已随交付 commit bf08601d 入账（tech#81 自含律·本 close 脚本经 autodetect 自含）"
    "——下轮=R2012 快速路径首查（10-12 08:00 tech#92 雷达标定权威窗届日即领〔锚例版上线后首生产窗 zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补"
    "·R1956 v3 读数 caveat=生产分数部分基于损坏替换文本注记承继〕+fire 窗 F-180 SC-005-07〔fire_consume --launch 单命令〕→F-181 REACT-v15 评审腿连发判断〔main#19→#20 序律〕）"
)

import datetime
now = datetime.datetime.now()
ts = now.strftime("%Y-%m-%d %H:%M:%S")
ts_prefix = now.strftime("%Y-%m-%d %H:%M")[:-1] + "x"
log_line = "%s R2011: %s" % (ts_prefix, LOG_BODY)

FOCUS = (
    "R2012 10-12 08:00 权威窗届日即领（tech#92 雷达标定判读〔锚例版上线后首生产窗·zhihu-hot 头部 ≥3 件 ≥60=selection-score 文本腿收口"
    "·FAIL=阈值分层腿递补·R1956 v3 读数 caveat=生产分数部分基于损坏替换文本注记承继〕）"
    "→F-180 SC-005-07 沈佩兰 fire 窗消费（三件套+发射器 turnkey·fire_consume --launch 单命令·材料轴检验位 E4 判据）"
    "→F-181 REACT-v15 评审腿（main#20·M4.5 七席+E4·tech#116 随件并读）；"
    "GPU 队列=MD-0002 T2I gated CEO 点头；tech#119 低优先在册"
)

summary = finalize_state(log_line=log_line, tick=2011, focus=FOCUS)
print("finalize_state:", {k: summary[k] for k in ("tick", "ts", "task")})

LIVE = [
    "本地替代率周报首读落档：生产推理百分百走本地模型（累计 326 次调用），云端零调用；自动换源判据未过，手记为准。",
    "最近实物：W42 本地替代率首读数据包 .c3-tmp/r2011_local_rate_w42.txt（2026-10-12 01:4x）",
    "下个里程碑：早上八点做雷达评分校准判读；显卡一有空窗就连出两件成品——口述史沈阿姨篇、热点卡收尾（48 小时内）。",
]
try:
    _rc, _lines, _viol = refresh_export(
        os.path.join("docs", "status-export.json"),
        patch={"live": LIVE, "do": "tech#24 本地替代率 W42 首读+换源判据判负毕（手记维持单一真相·W43 复读在册）；下步=08:00 雷达标定判读→fire 窗 F-180/F-181 连发判断"},
    )
    if _rc != 0:
        print("export refresh refused:", _viol)
    else:
        print("export refreshed ok")
except Exception as e:  # refresh failure is advisory, never fail close
    print("export refresh warn:", e)

FILES = [
    "src/os/state.json",
    "docs/status-export.json",
]
rc = run_close_commit(files=FILES, message=(
    "R2011 loop close: tech#24 consumed (source-switch criterion FAIL verbatim, hand-note stays single truth; "
    "W42 first reading L2=326/L3=0 rate 1.0000 into self-audit; cross-lane + direct-call mismatch documented); "
    "state tick 2011; export refresh [via bm-a]"
), root=ROOT)
print("run_close_commit rc:", rc)
