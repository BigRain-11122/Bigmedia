# -*- coding: utf-8 -*-
"""R2024 close: F-180 flight-3 dispatch round accounting.

- state.json: tick 2023->2024, R2024 log, ts+task refresh (PT-20260925-02)
- status-export.json: export_ts + do line (real-world derived, F3 law)
- tech.md: tech#122 seed (VRAM squeeze mitigation evaluation, gated on
  flight-3 outcome)  [queue restock step]
- explicit-file pathspec commit + push (close_commit helper, shared-tree safe)
"""
import io
import json
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "os"))
from close_commit import run_close_commit  # noqa: E402

NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
NOW_HM = datetime.now().strftime("%H:%M")

LOG = (
    "2026-10-12 05:" + NOW_HM + " R2024: fire 真窗首开+F-180 flight-3 原子派发——①五查全静"
    "（own orders 顶=O-20260908-1105 mtime 12:08:14==R1733 锚静+origin_gap_check QUIET ahead0 behind0=R1500 前置位"
    "+group_scan 全静：decisions truly_new=0 水位 150 维持+ledger @BigStream 5 行==盘锚零新转办"
    "+ORDERS 水位 quiet rows=270 tail_key='10-11 13:4x'==R1979 锚静+HQ orders 14:00:46==R1978 锚静）"
    "+树净零 index.lock（脏面=MV sprint 会话件预期态 R1745 承继）；②三探针=board 0 FAIL"
    "/readiness 3 阻塞皆外部 CEO 面 0 发现/loop_health 2 FAIL 皆在案史实（09-26/09-28 outage）+263 WARN 折叠面；"
    "③**tech#121 消费序律首次完整兑现=五查/探针毕后下一命令即 fire_consume 单命令直发"
    "→card=fire reason=fire-fresh 05:05:46 dispatch pid 79492**（ledger 第 12 行 GO·no-fire 序列 R2020-R2023 "
    "probe-face-cold-reload×1+util-face 97/96 双点后真窗开=读卡 verdict 序列捕获率 100% 判据兑现读数）；"
    "④守窗 14 分钟读数=wedge-probe 已过（无 rc6=tech#120 生成面应答首战 PASS）+ollama 83616 生成在飞"
    "（CPU 418→422s+GPU 95-98 高位）·VRAM 挤态诊断=llama-server keep-warm 5GB+GUI 群 30+ 上下文挤 12GB 卡"
    "→14b 慢生成（R2012 GEN-OK 108.9s 同根因面）·1500s 帽至 05:30:22 收账时点未落=判词异步落地下轮首读"
    "（R176→R177 先例）·三连烧穿=flight-4 前置 VRAM 缓释位评估（tech#122 落种·跨道动作先判 MV 需求）；"
    "⑤收账=main#19 flight-3 派发实录行+tech#122 种子+state/export/ledger commit+push"
    "——下轮=首读 flight-3 判词（PASS≥9→TTS light 续链→F-180 登记·F-181 后段位）+tech#92 雷达标定权威窗 08:00 并读"
)

TASK = LOG.split("R2024:", 1)[1].strip()[:60]

# --- state.json ---
sp = ROOT / "src" / "os" / "state.json"
d = json.loads(io.open(sp, encoding="utf-8").read())
d["tick"] = 2024
d["ts"] = NOW
d["task"] = TASK
d["log"].append(LOG)
io.open(sp, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))

# --- status-export.json ---
ep = ROOT / "docs" / "status-export.json"
e = json.loads(io.open(ep, encoding="utf-8").read())
e["export_ts"] = NOW
e["do"] = (
    "F-180 口述史二季首件 S1 门 flight-3 已派发（05:05 真窗 fire-fresh·wedge-probe 过·"
    "ollama 14b 挤态生成中·判词异步落地）→判词落地即续 TTS→S2→E8 链至 F-180 登记；"
    "F-181 REACT-v15 排后段位；10-12 08:00 雷达标定判读窗在队"
)
io.open(ep, "w", encoding="utf-8").write(json.dumps(e, ensure_ascii=False, indent=1))

# --- tech.md restock: tech#122 seed ---
tp = ROOT / "state" / "queue" / "tech.md"
t = io.open(tp, encoding="utf-8").read()
if "tech#122" not in t:
    seed = (
        "\n122. [R2024 补货·flight-3 挤态诊断真发现] S1/E4/E8 判词通道 VRAM 挤态缓释位评估"
        "（缺口锚=R2012/R2013 双 1500s 烧穿+R2024 flight-3 挤态生成读数：llama-server keep-warm ~5GB"
        "+GUI 群 30+ 上下文挤 12GB 卡→ollama 14b 慢生成·GEN-OK 14b 108.9s 冷载同根因面；"
        "缓释候选在册正法=MiniGameOllamaServe/KeepWarm 任务 disable+Stop-Process llama-server"
        "〔腾显存 8.3GB→1.8GB 实测在册·生产后按序恢复〕）——**gated=flight-3 判词读数**："
        "落地判词=缓释不触发（慢生成可容忍窗内完成）；三连 1500s 烧穿=flight-4 前置评估腿"
        "（先判 CEO 优先线 MV sprint VRAM 需求面+恢复序完备性·跨道动作如实呈报后执行）\n"
    )
    io.open(tp, "a", encoding="utf-8").write(seed)

# --- explicit-file commit + push ---
files = [
    "src/os/state.json",
    "state/queue/main.md",
    "state/queue/tech.md",
    "docs/status-export.json",
    "data/pipeline/fire-consume-ledger.jsonl",
]
msg = (
    "R2024 close: F-180 flight-3 dispatched via fire_consume single-command law "
    "(first true fire window 05:05:46 fire-fresh pid 79492; tech#121 sequence 100% captured "
    "in ledger; wedge-probe passed, ollama 14b generating in squeezed VRAM; verdict async -> "
    "next round first-read; tech#122 VRAM-relief seed gated on flight outcome; "
    "tech#92 radar authoritative window 08:00 pending; tick 2024) [via bm-a]"
)
rc, lines = run_close_commit(files, msg)
for line in lines:
    print(line)
print("CLOSE-RC", rc)
