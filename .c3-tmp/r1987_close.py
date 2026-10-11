# -*- coding: utf-8 -*-
"""R1987 round close: production round - tech#106 delivery (comfy_activity
probe, C-43 v1.95) + R1986 carryover S1 verdict consumed (timeout, zero
false-green, chain stays at gate) + live divergence adjudication (idle
server holds VRAM, util from desktop GUI fleet).
Two-stage commit law: stage A deliverables, then finalize_state + stage B
state.json with close script self-included (tech#81).
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(_HERE, "..", "src", "os")))

from close_commit import finalize_state, run_close_commit  # noqa: E402

LOG_LINE = u"2026-10-11 17:4x R1987: 生产轮·tech#106 交付=ComfyUI 侧活度探针 comfy_activity（C-43 v1.95·R1986 窗中翻脸消费律正身工具化）——①轮首五查全静=own orders 顶 O-20260908-1105 mtime==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）+group_scan 四面静（decisions truly_new=0 水位 141 维持+ledger @BigStream 5 行==值守锚+ORDERS 行水位第八窗 quiet rows=270=='10-11 13:4x'==R1979 基线）+HQ orders 14:00:46==R1978 消费锚零新行+无 index.lock+树态=MV sprint 会话域在飞件零接触（R1745 承继）；②R1986 结转首查=S1 后台判词收消费=超时遗憾定谳（expert-verdicts 16:40 后零新档+expert-calls 零新行=R1986 四发全烧零判词·S1 未过门零假绿灯·SC-005-04 链停门位）+fire_window_card 17:24:47 no-fire（gate 双闸败 free_min 455<2048+util_max 100>80·probe busy-contended·mv quiet 202.9min）→SC-005-04/05/06 三件 fire-ready 维持结转（F-176/177/178）；③tech#106 交付=src/os/comfy_activity.py 双面只读探针（queue GET /queue 计数+cpu ComfyUI python 进程 CPU 增量双采样·PS Name LIKE python%+CommandLine match 'comfyui'〔便携路径携 token live 验真 PID 58200〕·Name 过滤防探针自匹配=本轮首查 live 实锚〔无过滤时探针自身 powershell 命令行亦命中 PID 6524 实证〕·verdict 三态〔active 单一可读正面即证/quiet=cpu empty 或小 delta+queue 0/0〔lane 态非 VRAM 态〕/error fail-closed 缺读数永不读作 quiet〕+stale-render wedged 候选注记〔R1876 族·advisory 零闸〕+--ledger JSONL 七字段 fire 消费前读数证据链·rc 0/1/2 族契约）·41 新测+1053 全回归绿 103.8s SUITE_RC=0（1012+41·run_suite 正法）；④**live dogfood 首读=R1987 分叉读数正身裁决：quiet rc0（queue 0/0+cpu delta 0.0ms/4s+PID 58200）×nvidia-smi util 100%/free 171MB=R1936/R1937 起「文件静×硬件忙=长渲染在飞」归因本窗证伪——ComfyUI 空闲持 11.8GB VRAM·util 源=桌面 GUI 群（compute-apps 31 GUI 进程在列）·评审腿阻塞真面=VRAM 驻留非渲染波（让路判定不变·归因诚实面收口）+R1986 消费律正身就位（fire GO 消费前单命令跑本器）**；⑤三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）0 发现/loop_health 2F+246W 皆在案史实（两 outage 09-26/09-28 已裁定不重触发）·证据 .c3-tmp/r1987_probes.txt；⑥例行件=10-11 日报在案不重跑（R1927 一份为真相）·W42 周审 10-12 届日即领·GB §④ v1.3 下期 10-15 跳过·tech#92 雷达标定权威窗 10-12 08:00 届日即领不预扫·meme V1 成片查看位零新到件（R1899 锚维持）·MD-0002 T2I gated CEO 点头维持·export_ts 16:24:39 <24h 零 CEO 可见成品态变化节流不刷（live 三行核读=盘点 018+SC-005 二批等 GPU 窗态仍准）·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·tokens:local=0（探针+PS 查询+套件跑零本地模型调用·P-54⑤ 计量律）；⑦队列补货步=真无独立新种子如实注记零膨胀（live 分叉读数发现已消费进 tech#106 done 注记=禁凑数律）·临时件=r1987 证据件两枚入账收口（tech#81 自含律）——下轮=R1988 快速路径首查（fire 卡复查〔tech#106 活度读数先行=GO 消费前单命令跑 comfy_activity〕→GO 即重发 SC-005-04 S1 1500s 标准窗→PASS 续链 TTS light→同文本核验→S2【ai_feel+ASR 终轨】→E8+E4→M4→F-176 登记→05→06 连发·窗关如实结轮；no-fire=等待窗取 P2/P3；10-12 08:00 tech#92 雷达标定窗届日即领+W42 周审+REACT-v15 10-12 窗）"

FOCUS = u"R1988 快速路径首查（fire 卡复查〔tech#106 活度读数先行：GO 消费前单命令跑 comfy_activity〕→GO 即重发 SC-005-04 S1 1500s 标准窗→PASS 续链 TTS light→同文本核验→S2【ai_feel+ASR 终轨】→E8+E4→M4→F-176 登记→05→06 连发·窗关如实结轮；no-fire=等待窗取 P2/P3；10-12 08:00 tech#92 雷达标定窗届日即领+W42 周审+REACT-v15 10-12 窗）"

DELIVERABLES = [
    "src/os/comfy_activity.py",
    "tests/test_comfy_activity.py",
    "docs/capabilities.md",
    "state/queue/tech.md",
    "data/pipeline/comfy-activity-ledger.jsonl",
    ".c3-tmp/r1987_probes.txt",
    ".c3-tmp/r1987_comfy_dogfood.txt",
]


def main():
    # stage A: deliverables first (two-stage law)
    rc_a, lines_a = run_close_commit(
        files=DELIVERABLES,
        message=("R1987 deliverables: comfy_activity probe (tech#106) - "
                 "ComfyUI-side liveness tool for the R1986 fire-GO "
                 "consumption law: /queue counts + python process CPU-time "
                 "delta, quiet/active/error verdict fail-closed, "
                 "stale-render advisory, --ledger evidence chain; 41 new "
                 "tests, 1053 suite green; live dogfood: quiet x util100 "
                 "divergence resolved (idle server holds VRAM, util from "
                 "desktop GUI fleet) [via bm-a]"),
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
             summary.get("orders_wm_rows"), summary["log_len"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
