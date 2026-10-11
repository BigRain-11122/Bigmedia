# -*- coding: utf-8 -*-
"""R2015 closing step (canonical single-writer path, tech#76):
finalize_state + run_close_commit (self-included per tech#81 autodetect
law). Export intentionally NOT refreshed this round: internal tool
delivery with no CEO-visible product change (R1997/R2004 precedent),
last export_ts < 24h and live three lines still accurate."""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "os"))
import close_commit as cc  # noqa: E402

LOG = (
 "2026-10-12 03:4x R2015: 生产轮·P2 队头消费=tech#119 直呼 A/B 留痕面交付（O-20261009-1246 取活·fire 卡 no-fire 等待窗照取·两段制收账=交付段先行）——"
 "①轮首五查全静=own orders 顶 O-20260908-1105 mtime 12:08:14==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）+group_scan 四面全静"
 "（decisions truly_new=0 水位 150 维持+ledger @BigStream 5 行==值守锚零新转办+ORDERS 行水位 quiet rows=270 tail_key='10-11 13:4x'==R1979 基线〔tech#103 连窗过〕"
 "+HQ orders 14:00:46==R1978 消费锚零新行）+无 index.lock+树态=MV sprint 会话域在飞件零接触（R1745 承继）；"
 "②tech#106 消费律=comfy_activity 03:13 quiet rc0（queue 0/0+cpu delta 0.0ms·PID 58200）→fire_window_card 03:14 no-fire"
 "（gate 双闸败 free_min 460<2048+util_max 99>80·probe face=busy-contended·R1987 定谳维持：ComfyUI 空闲驻留+util 源=桌面 GUI 群）"
 "→F-180 SC-005-07（flight-3 挂 fire_consume 重发通道）+F-181 REACT-v15 评审腿（发射器 tech#113 出件在位）维持 fire-ready 结转；"
 "③tech#119 交付=候选①+②合体（③判负不成立：根因位差值带三窗实锚）：新模块 src/os/ollama_ab_ledger.py（append_ab_row best-effort JSONL·tech#52 工艺"
 "=父目录自建+UTF-8+写失败 WARN 永不 raise+n/note 可选列省略）+C-33 ab 消费面（tokens_local_meter 增 parse_ab_ledger〔whisper 解析器容错形复用〕"
 "+meter ab_rows 参〔rc=0 产出入 tokens_local 总计/非 0 尝试无产出单列·窗口过滤〕+build_readout ab_path 参+human 行 ab 双计数）+口径注记=docstring 边界条收窄"
 "（「Not auto-countable」段更新：直呼热身仍手记·A/B 直呼经 append_ab_row 可见·tech#24 手记单一真相口径不变=本面机器可读补充）——R2011 缺口锚收口"
 "（直呼带 10-02 +59/09-25 +34/10-11 +6 自此入探针射程）；9 新测（TestAppendAbRow 4：行形精确+n/note 可选+父目录自建+best-effort 拒 raise／"
 "TestAbFace 5：解析容错委托+窗口过滤分类+attempted 不入总计+缺席面零读+注入 ab_path 端到端）+test_build_readout_via_files 补注入 ab_path（R1865 隔离族）"
 "·**1132 全回归绿 138.7s SUITE_RC=0**（1123+9·run_suite 正法）·live dogfood=真仓缺席面读零无崩；判据「下次 A/B 探针后手记 vs 探针差值收敛可读」"
 "兑现窗=tech#92 阈值分层腿若触发=首件消费者（hermetic 面已锁·真窗读数后置）·capabilities v1.103；"
 "④三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）0 发现"
 "/loop_health 2F+263W 皆在案史实带内（两 outage 09-26/09-28 已裁定不重触发·drift 18≤21 裁定基线·dense fold 带内）·证据 .c3-tmp/r2015_probes.txt；"
 "⑤例行件=10-12 日报在案不重跑（R2008 一份为真相）·W42 周审第 4 期在案（R2008）·GB §④ v1.3 下期 10-15 ≤7d 跳过"
 "·tech#92 雷达标定权威窗 10-12 08:00 届日即领不预扫（zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补）"
 "·meme V1 成片查看位双路径递归零 mp4（R1899 锚维持·装配腿 bm-a 会话域在飞零接触）·MD-0002 T2I gated CEO 点头维持"
 "·export_ts R2014 刷 <24h 零 CEO 可见成品态变化节流不刷（live 三行 F-180 flight-3 态仍准·R1997/R2004 内部工具件先例）"
 "·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·tokens:local=0（纯 CPU 工程+探针只读+套件跑零本地模型产出调用·P-54⑤ 计量律）；"
 "⑥队列补货步=真无独立新种子如实注记零膨胀（tech#119=R2011 既有种子兑现非新种子·禁凑数律）·临时件清理钩=r2015_probes.txt+close 脚本经 tech#81 自含律收口——"
 "下轮=R2016 快速路径首查（fire 卡复查〔comfy_activity 消费律先行〕→fire=flight-3 派发〔--wedge-probe 就位·楔死窗 rc6 快败/健康窗判词 ≥9=TTS light 续链 F-180 登记〕"
 "/no-fire=等待窗照取）+tech#92 08:00 权威窗届日即领。收账显式列文件 commit+push。"
)

FOCUS = (
 "生产轮·P2 队头消费=tech#119 直呼 A/B 留痕面交付（O-20261009-1246 取活·fire 卡 no-f"
)

# --- canonical state accounting (tech#76 single writer) ---
cc.finalize_state(LOG, focus=FOCUS)
print("finalize_state done")

# --- close commit (tech#81 autodetect self-include) ---
rc, lines = cc.run_close_commit(
    files=["src/os/state.json"],
    message=("R2015 close: tech#119 A/B direct-call ledger delivered "
             "(ollama_ab_ledger.py + meter ab face); 1132 suite green; "
             "tick 2015; export throttled (no CEO-visible change) "
             "[via bm-a]"))
print("\n".join(lines))
print("CLOSE_RC=%d" % rc)
