# -*- coding: utf-8 -*-
"""BigStream weekly self-audit data pack (O-20260924-1057 periodic self-review).

The periodic self-review law (os-protocol S7): once per ISO week the
company audits itself - team / flow / resource health, mechanism drift,
ledger hygiene, efficiency-balance metrics (dept-review S5 B5), last
week's remediation follow-ups. This script builds the ZERO-TOKEN data
pack first, so the judging layer (a loop round) only reads one file and
writes the verdict:

    python src/os/self_audit.py            # pack to docs/audits/packs/
    python src/os/self_audit.py --week 2026-W39

Read-only by design; probes run as subprocesses. Exit 0 unless a hard
collection error occurs. ASCII rule: source pure ASCII; Chinese only in
the markdown data pack it writes.

Collected (each = one line in the pack):
  probes      board_check / readiness / loop_health exit codes + key line
  loop        state.json tick + last log line timestamp
  backlog     done vs open counts (pure regex on backlog.md)
  orders      order files / claimed / receipted counts (grep markers)
  gates       station-reviews + expert-calls ledger row counts
  renders     ledger rows vs mp4 files on disk
  tests       full unittest discovery pass/fail tail
  git         commits in the last 7 days
"""
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PACK_DIR = REPO / "docs" / "audits" / "packs"
STATE = REPO / "src" / "os" / "state.json"
BACKLOG = REPO / "src" / "os" / "backlog.md"
ORDERS_DIR = REPO / "orders"
STATION = REPO / "docs" / "reviews" / "station-reviews.md"
CALLS = REPO / "docs" / "reviews" / "expert-calls.md"
RENDERS_LEDGER = REPO / "output" / "renders" / "README.md"


def iso_week_of(d):
    y, w, _ = d.isocalendar()
    return "%d-W%02d" % (y, w)


def run(cmd, timeout=600):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           cwd=str(REPO), timeout=timeout, encoding="utf-8",
                           errors="replace")
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as e:
        return 99, "%s: %s" % (type(e).__name__, e)


def probe_lines():
    """Three probes -> [(name, exit, key_line)] (pure collection)."""
    out = []
    for name, cmd in (
        ("board_check", [sys.executable, "src/board_check.py"]),
        ("readiness", [sys.executable, "src/readiness.py"]),
        ("loop_health", [sys.executable, "src/os/loop_health.py"]),
    ):
        code, text = run(cmd)
        key = [ln for ln in text.splitlines()
               if ("fail" in ln.lower() or "blocker" in ln.lower()
                   or "not ready" in ln.lower() or "->" in ln)]
        out.append((name, code, key[-1] if key else text.splitlines()[-1] if text.strip() else "-"))
    return out


def collect_pack(week):
    """All collection logic -> dict (pure-ish; subprocesses read-only)."""
    import json
    pack = {"week": week, "collected": datetime.now().strftime("%Y-%m-%d %H:%M")}
    pack["probes"] = probe_lines()
    try:
        s = json.loads(STATE.read_text(encoding="utf-8"))
        pack["loop"] = {"tick": s.get("tick"),
                        "last_log_head": (s.get("log") or ["-"])[-1][:100]}
    except Exception as e:
        pack["loop"] = {"error": str(e)[:80]}
    text = BACKLOG.read_text(encoding="utf-8") if BACKLOG.exists() else ""
    done = len(re.findall(r"^\d+\. \[done", text, re.M))
    open_ = len(re.findall(r"^\d+\. (?!\[done)", text, re.M))
    pack["backlog"] = {"done": done, "open": open_}
    o_files = sorted(ORDERS_DIR.glob("O-*.md")) if ORDERS_DIR.exists() else []
    claimed = sum(1 for f in o_files if "执行认领" in f.read_text(encoding="utf-8", errors="replace"))
    receipted = sum(1 for f in o_files if "执行回执" in f.read_text(encoding="utf-8", errors="replace"))
    pack["orders"] = {"files": len(o_files), "claimed": claimed, "receipted": receipted}
    def rows(p):
        try:
            return len([ln for ln in p.read_text(encoding="utf-8").splitlines()
                        if ln.startswith("| 2")])
        except OSError:
            return 0
    pack["gates"] = {"station_reviews": rows(STATION), "expert_calls": rows(CALLS)}
    mp4 = list((REPO / "output" / "renders").glob("*.mp4"))
    ledger_rows = 0
    if RENDERS_LEDGER.exists():
        ledger_rows = len([ln for ln in RENDERS_LEDGER.read_text(encoding="utf-8").splitlines()
                           if ln.startswith("| bs-")])
    pack["renders"] = {"mp4_on_disk": len(mp4), "ledger_rows": ledger_rows}
    code, text = run([sys.executable, "-m", "unittest", "discover", "-s", "tests",
                      "-p", "test_*.py", "-v"], timeout=900)
    tail = [ln for ln in text.splitlines() if ln.startswith(("OK", "FAILED"))]
    pack["tests"] = {"tail": tail[0] if tail else "no-summary(code %d)" % code}
    code, text = run(["git", "log", "--oneline", "--since=7 days ago"])
    pack["git"] = {"commits_7d": len(text.strip().splitlines()) if code == 0 else -1}
    return pack


def render_pack(p):
    """Pack dict -> markdown (data file; Chinese fine here)."""
    lines = []
    lines.append("# 周自审数据包 %s（自动采集·零 token）" % p["week"])
    lines.append("")
    lines.append("> 生成器=`src/os/self_audit.py`（O-20260924-1057 周期自审令）·"
                 "采集时间=%s·判读层=OS 循环轮（周自审报告=`docs/audits/%s-self-audit.md`）。"
                 % (p["collected"], p["week"]))
    lines.append("")
    lines.append("## 机检探针")
    for name, code, key in p["probes"]:
        lines.append("- %s: exit=%d | %s" % (name, code, key[:120]))
    lines.append("")
    lines.append("## 循环与台账")
    loop = p.get("loop", {})
    lines.append("- state.json: tick=%s | 尾行=%s" % (
        loop.get("tick"), loop.get("last_log_head", loop.get("error", "-"))))
    b = p["backlog"]
    lines.append("- backlog: done=%d open=%d" % (b["done"], b["open"]))
    o = p["orders"]
    lines.append("- orders: 落册=%d 已认领=%d 已回执=%d" % (o["files"], o["claimed"], o["receipted"]))
    g = p["gates"]
    lines.append("- 环节台账: station-reviews=%d 行 · expert-calls=%d 行" % (
        g["station_reviews"], g["expert_calls"]))
    r = p["renders"]
    lines.append("- renders: 盘上 mp4=%d · 台账行=%d" % (r["mp4_on_disk"], r["ledger_rows"]))
    lines.append("- tests: %s" % p["tests"]["tail"])
    lines.append("- git: 7 日 commits=%d" % p["git"]["commits_7d"])
    lines.append("")
    lines.append("## 判读层清单（循环轮填写）")
    lines.append("1. 三维健康（团队/流程/资源·对照 `docs/audits/2026-09-24-company-audit.md` 框架）")
    lines.append("2. 机制漂移（文档 vs 实况·可调 loop-engineer 专家）")
    lines.append("3. 效率平衡度量（dept-review §5 B5：评审轮次/件+催办行数）")
    lines.append("4. 上周整改项复查（闭环验证）")
    lines.append("5. 假设校准状态（未上线=未测量·只登记）")
    lines.append("")
    return "\n".join(lines) + "\n"


def main(argv):
    week = None
    i = 1
    while i < len(argv):
        if argv[i] == "--week":
            i += 1
            week = argv[i]
        i += 1
    if not week:
        week = iso_week_of(date.today())
    pack = collect_pack(week)
    PACK_DIR.mkdir(parents=True, exist_ok=True)
    out = PACK_DIR / ("%s-pack.md" % week)
    out.write_text(render_pack(pack), encoding="utf-8")
    print("OK pack %s probes=%s tests=%s git7d=%d out=%s"
          % (week,
             ",".join("%s:%d" % (n, c) for n, c, _ in pack["probes"]),
             pack["tests"]["tail"], pack["git"]["commits_7d"], out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
