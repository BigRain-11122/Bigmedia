# -*- coding: utf-8 -*-
# R2149 close: orders 351-355 consumption + main#27 close-out judgment + tech#141 done
# Uses finalize_state born gate (tech#149) + canonical export writer (tech#148/70).
import sys
import os.path as _osp
sys.path.insert(0, _osp.join(_osp.dirname(_osp.abspath(__file__)), '..', 'src', 'os'))

from close_commit import finalize_state, run_close_commit
from group_scan import current_orders_watermark

LOG = (
    "2026-10-13 12:4x R2149: 生产轮·集团 ORDERS 五新行消费+main#27 死线窗收口判读+tech#141 判读收口"
    "（MV 域查看位零接触 R1745 承继）——"
    "①轮首五查破静=group_scan ORDERS rows 350→355（tail '10-13 12:3x'→'13:1x'·D-13 SLA 带内）+"
    "DECISIONS truly_new=0+LEDGER @BigStream 5 行=锚+origin_gap QUIET（ahead0 behind0）——"
    "五新行全 MV 域导演席簇：row 351=O-20261013-1255 导演席对标深造令（R-20261013-director-canon 派出）+"
    "row 352 调研组归笼第二波（分镜/调色/QC/一致性 5/9）+"
    "row 353=O-20261013-1300 每块全球一流律·产线母法（BigStream 长期最高质量门·已入 PRODUCTION-SYSTEM-v1 母法位——"
    "本司全产线知悉入账：闸>死线·产出不达基准禁出厂·S2 三门/E8/M4 既有闸面维持·MV sprint 会话域执行正身）+"
    "row 354 调研组归笼第三波（表演/字幕/端到端 8/9）+row 355 调研组终报 9/9 全部收口（导演对标组归笼）——"
    "执行面=MV sprint 会话域行内自述同窗收口·本循环查看位零接触维持；"
    "②main#27 死线窗收口判读：成片呈报毕定谳（orders 10-13 11:3x 行=CEO 复评 60 分→V3 整改令簇=成片已到 CEO 眼）+"
    "②③腿（撤旗/worker-restart/F 接力）维持 gated 至 10-14 夜窗 00:00 起（R2128 注承继）——"
    "tech#141 判读收口=fire 接力首试读数入账（fire-consume-ledger 10-13 11:33/12:04/12:13/12:24 四行 no-fire "
    "reason=bm-a-workday-hours-zero-dispatch=O-1505③ 铁律面首闸+载类面 R2097 tech#140 load-class 实锚 free 3040<8704）"
    "→双结构堵维持=F 族（F-180~183）候位顺延自然窗+pause 旗基重锚（data/pipeline/aihot-watchdog-state.json "
    "reason=CEO workday at-machine yield〔夜窗 KF 基已过期·comfy DOWN GPU 闲 4%·VRAM 余 6.1G<14b 8704M=worker restart "
    "必挤 CEO 前台群〕·resume_step=10-14 夜窗 main#21 三连·tech#92 重判窗=resume 后首个 08:00 compose=10-14 08:00 "
    "R2125 承继）+陈 ceo-off-work-flag 移除（10-12 20:50 残旗跨日失效态·CEO 已回机 13:1x 在发令·生命周期闭口·独立提交）；"
    "③机面读数=GPU 4%/6117MiB（CEO 前台群）+comfy DOWN（KF 批毕）+ollama DOWN+AIHOT api {ok,db:ok}（worker 缺席=skip-pause 预期态）；"
    "④三队步=tech#141 done 标回写+main#28 史源扩容（10-13 簇并入 DIGEST-v20 候选池=当日扫描信息入队正身·"
    "DIGEST-SUPPLY advisory 10-13 row-date 承接）+tech#126/142 维持 gated 夜窗；"
    "⑤三探针=board 0 FAIL/readiness 3 阻塞皆外部 CEO 面+1 发现（render-unannot react-v16=在链预期红 F-183 登记即清 R2118 裁定）/"
    "loop_health 3 FAIL 皆在案史实（heartbeat-outage 09-26/09-28/10-12）+account-drift-adjudicated 18 beats 在案；"
    "例行件：日报 2026-10-13 在案不重跑+global-benchmarks 10-08 ≤7 天跳过（下期 10-15）+"
    "HQ-FEEDBACK 不写（无集团层新 open 问题）+tokens:local=0（本轮零本地模型调用·纯脚本机检·P-54⑤ 计量律如实记）；"
    "下轮=夜窗恢复序（CEO 下班旗窗或 10-14 00:00：撤 pause 旗→worker-restart→tech#126 校准冒烟→F-180 族 fire 接力→DIGEST-v20 产窗）。"
)

finalize_state(
    log_line=LOG,
    focus="night-window resume sequence (main#21 unpause+worker-restart, F-180 fire relay, DIGEST-v20 production)",
    tick=2149,
    watermark_add=[],
    orders_watermark=current_orders_watermark(),
)

FILES = [
    'src/os/state.json',
    'data/pipeline/aihot-watchdog-state.json',
    'state/queue/tech.md',
    'state/queue/main.md',
    '.c3-tmp/r2149_orders_tail.txt',
    '.c3-tmp/r2149_tech_head.txt',
    '.c3-tmp/r2149_tech_tail.txt',
]

MESSAGE = (
    "R2149: consume HQ orders rows 351-355 (MV director-research cluster + global-top production law ack, "
    "view-position zero-touch); main#27 close-out: film delivered to CEO (60pt re-review in orders), legs deferred "
    "to 10-14 night window; tech#141 done: fire relay readings 4x no-fire workday-block + load-class 3040<8704, "
    "F family deferred to natural window; AIHOT pause flag re-anchored to CEO workday yield; tech#126/142 stay "
    "gated night window; DIGEST-v20 10-13 cluster queued (main#28). Next: night-window resume sequence. [via bm-a]"
)

EXPORT_PATCH = {
    "do": "MV V3 整改调研九组 9/9 归档毕（集团令 351-355 消费）；本司产线候夜窗恢复：AI 日报 Worker+180 号有声节目，白天让路 CEO。",
    "live": [
        "当前活：白天让路 CEO 用机；夜窗恢复 AI 日报算力线。",
        "最近实物：集团调研九组报告 9/9 归档（10-13）；本司最新成品=城市盘点 019（10-12）。",
        "下个里程碑：10-14 夜窗撤让路旗恢复 AI 日报 Worker，08:00 出新版日报；有声节目 180 号过审后登记。",
    ],
    "results": [
        ["orders 351-355 消费", "r2149"],
        ["fire no-fire workday x4", "f180"],
        ["pause 旗重锚夜窗序", "aihot"],
        ["DIGEST-v20 候选入队", "v20"],
    ],
}

run_close_commit(
    files=FILES,
    message=MESSAGE,
    push=True,
    export_patch=EXPORT_PATCH,
)
print("R2149-CLOSE-DONE")
