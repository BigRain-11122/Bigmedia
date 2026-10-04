# -*- coding: utf-8 -*-
"""Local substitution rate report aggregator (L2/(L2+L3)) — P-2026-09-25-07 §五 / backlog #57.

Zero-token routine for the 2026-10-07 governance-day first report:
parses src/os/state.json log for per-round ``tokens:local=N`` metering lines
and data/pipeline/p4-ledger.md for P4 local digest runs, aggregates by ISO
week, and renders the substitution-rate data pack. Cloud face (L3) is parsed
from ``tokens:cloud=`` entries when present (0 today under the established
BigStream accounting: production inference plane fully local). Honest
boundary notes are rendered verbatim so the report cannot read as a fake
green light.

Run:
    python src/os/local_rate_report.py [--out <evidence.txt>] [--json]
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
from datetime import datetime

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from self_audit import iso_week_of  # single source for ISO week math  # noqa: E402

STATE_PATH = os.path.join(REPO, "src", "os", "state.json")
P4_LEDGER_PATH = os.path.join(REPO, "data", "pipeline", "p4-ledger.md")
DEFAULT_OUT = os.path.join(REPO, "r_local_rate_report.txt")

LOCAL_RE = re.compile(r"tokens:local=(\d+)")
CLOUD_RE = re.compile(r"tokens:cloud=(\d+)")
ROUND_RE = re.compile(r"\bR(\d{3,4})\b")
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")

# Honest boundary notes carried verbatim into every report (no fake green light).
BOUNDARY_NOTES = [
    u"①主开发脑/正式美术/Gate3 终审=L3 保留面（集团纲领 §六诚实边界）——bm-a 会话面云用量=会话面注记不转移本司生产计量（任务书 Token 面纪律既定口径）。",
    u"②TTS=edge-tts=零 API 计费网络端点（D-BS-02 既定产线默认·零 token 计费面）；ASR=faster-whisper 本地；评审席=Ollama 本地；渲染=FFmpeg 本地（L1 确定律面不计 L2）。",
    u"③tokens:local 计量=每次本地模型调用记 1（S1 门/E4 参考仪/E8 评审席/专家席/ASR 终轨·P-54⑤ 计量律·逐轮行 2026-09-24 起在账）。",
    u"④P4 台账行（data/pipeline/p4-ledger.md）=调研读取替代独立面，与 tokens:local 逐轮行分列呈报防双计。",
]


def parse_rounds(log_lines):
    """Extract (date, week, round, local_n, cloud_n) per log line.

    First tokens:local/cloud match per line = that round's own metering entry;
    later mentions inside recaps are ignored (single-truth reading).
    """
    rounds = []
    for line in log_lines:
        dm = DATE_RE.match(line)
        lm = LOCAL_RE.search(line)
        cm = CLOUD_RE.search(line)
        if not dm or not lm:
            continue
        rm = ROUND_RE.search(line)
        d = datetime.strptime(dm.group(1), "%Y-%m-%d").date()
        rounds.append({
            "date": dm.group(1),
            "week": iso_week_of(d),
            "round": "R" + rm.group(1) if rm else "?",
            "local": int(lm.group(1)),
            "cloud": int(cm.group(1)) if cm else 0,
        })
    return rounds


def aggregate_weeks(rounds):
    """Per ISO week: rounds metered, rounds with local calls, L2/L3 sums."""
    weeks = {}
    for r in rounds:
        w = weeks.setdefault(r["week"], {
            "rounds": 0, "active_rounds": 0, "l2": 0, "l3": 0,
            "first_date": r["date"], "last_date": r["date"],
        })
        w["rounds"] += 1
        if r["local"] > 0:
            w["active_rounds"] += 1
        w["l2"] += r["local"]
        w["l3"] += r["cloud"]
        w["last_date"] = r["date"]
    for w in weeks.values():
        denom = w["l2"] + w["l3"]
        w["rate"] = (float(w["l2"]) / denom) if denom else None
    return weeks


def parse_p4_ledger(text):
    """Parse p4-ledger.md table rows: | time | input | model | digest | lines | refs | trunc | secs | verdict |."""
    rows = []
    for line in text.splitlines():
        if not line.startswith("|") or "时间" in line or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 9 or not re.match(r"\d{4}-", cells[0]):
            continue
        rows.append({
            "time": cells[0], "input": cells[1], "model": cells[2],
            "digest": cells[3], "lines": cells[4], "refs": cells[5],
            "truncated": cells[6], "secs": cells[7], "verdict": cells[8],
        })
    return rows


def render_report(rounds, weeks, p4_rows):
    """Render the UTF-8 data pack (Chinese content lives here, not in prints)."""
    total_l2 = sum(r["local"] for r in rounds)
    total_l3 = sum(r["cloud"] for r in rounds)
    denom = total_l2 + total_l3
    overall = (float(total_l2) / denom) if denom else None
    first = rounds[0]["date"] if rounds else "-"
    last = rounds[-1]["date"] if rounds else "-"

    out = io.StringIO()
    out.write(u"# 本地替代率数据包（L2/(L2+L3)·替代率首报数据面）\n\n")
    out.write(u"口径=P-2026-09-25-07 §五（backlog #57）：周轮汇 L2/(L2+L3)；数据面=state.json tokens:local 逐轮行 + data/pipeline/p4-ledger.md。\n")
    out.write(u"数据窗=%s → %s（prep 时点·终报=2026-10-07 治理日复跑刷新）。\n\n" % (first, last))

    out.write(u"## 周轮汇表\n\n")
    out.write(u"| ISO 周 | 计量轮数 | 有本地调用轮 | 本地调用 L2 | 云端调用 L3 | L2/(L2+L3) |\n")
    out.write(u"|---|---|---|---|---|---|\n")
    for wk in sorted(weeks):
        w = weeks[wk]
        rate = (u"%.4f" % w["rate"]) if w["rate"] is not None else u"N/A"
        out.write(u"| %s | %d | %d | %d | %d | %s |\n" % (
            wk, w["rounds"], w["active_rounds"], w["l2"], w["l3"], rate))
    rate_s = (u"%.4f" % overall) if overall is not None else u"N/A"
    out.write(u"| **合计** | **%d** | **%d** | **%d** | **%d** | **%s** |\n\n" % (
        len(rounds), sum(1 for r in rounds if r["local"] > 0), total_l2, total_l3, rate_s))

    out.write(u"## 首报口径读数（「本地处理 N 件·云端省减 M 读取轮次」）\n\n")
    out.write(u"- 本地处理 %d 件（生产推理面本地模型调用 L2：S1 门/E4 参考仪/E8 评审席/专家席/ASR 终轨）。\n" % total_l2)
    out.write(u"- 云端省减 %d 读取轮次（L2 同位：每次本地调用=一次潜在云端读取/推理轮的替代；生产推理面 L3=%d）。\n" % (total_l2, total_l3))
    out.write(u"- P4 调研摘要台账独立面：%d 行（%s）——调研读取替代分列呈报防双计。\n\n" % (
        len(p4_rows), u"、".join(sorted(set(r["model"] for r in p4_rows))) or u"-"))

    out.write(u"## 诚实边界注（防假绿灯·逐字呈报）\n\n")
    for n in BOUNDARY_NOTES:
        out.write(u"- %s\n" % n)
    out.write(u"\n## 刷新指令（2026-10-07 治理日终报）\n\n")
    out.write(u"python src/os/local_rate_report.py --out rNNNN_local_rate.txt（零 token·一命令复跑·数据窗自动延至 10-07）。\n")
    return out.getvalue()


def build_pack(state_path=STATE_PATH, p4_path=P4_LEDGER_PATH):
    state = json.load(io.open(state_path, encoding="utf-8"))
    rounds = parse_rounds(state.get("log", []))
    weeks = aggregate_weeks(rounds)
    p4_text = io.open(p4_path, encoding="utf-8").read()
    p4_rows = parse_p4_ledger(p4_text)
    return rounds, weeks, p4_rows


def main(argv=None):
    ap = argparse.ArgumentParser(description="local substitution rate report packer")
    ap.add_argument("--out", default=DEFAULT_OUT, help="UTF-8 evidence file path")
    ap.add_argument("--json", action="store_true", help="also dump machine-readable pack")
    args = ap.parse_args(argv)

    rounds, weeks, p4_rows = build_pack()
    text = render_report(rounds, weeks, p4_rows)
    io.open(args.out, "w", encoding="utf-8").write(text)

    # console face = ASCII only (encoding law: CJK never relies on console)
    total_l2 = sum(r["local"] for r in rounds)
    total_l3 = sum(r["cloud"] for r in rounds)
    print("rounds metered=%d  L2 local calls=%d  L3 cloud calls=%d  weeks=%d  p4_rows=%d" % (
        len(rounds), total_l2, total_l3, len(weeks), len(p4_rows)))
    print("report written: %s" % args.out)
    if args.json:
        jpath = os.path.splitext(args.out)[0] + ".json"
        io.open(jpath, "w", encoding="utf-8").write(json.dumps({
            "weeks": weeks, "total_l2": total_l2, "total_l3": total_l3,
            "p4_rows": p4_rows, "boundary_notes": BOUNDARY_NOTES,
        }, ensure_ascii=False, indent=1))
        print("json written: %s" % jpath)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
