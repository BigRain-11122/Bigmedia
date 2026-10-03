# -*- coding: utf-8 -*-
# R1159 probes + group orders scan + export freshness. Output: r1159_all.txt
import subprocess, os, re, datetime, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
TMP = os.path.dirname(os.path.abspath(__file__))
GROUP = os.path.normpath(os.path.join(ROOT, "..", ".."))
lines = []
def add(s): lines.append(s)

def run(label, args):
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (p.stdout or "") + (p.stderr or "")
    add("=== %s (rc=%d) ===" % (label, p.returncode))
    add(out.strip()[-2200:])
    add("")

add("now=%s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# three probes
run("BOARD", ["python", "src/board_check.py"])
run("READINESS", ["python", "src/readiness.py"])
run("LOOP_HEALTH", ["python", "src/os/loop_health.py"])

# group orders.md: rows mentioning BigStream (last 3) + rows dated 10-02/10-03
add("=== GROUP orders.md BigStream/dates scan ===")
go = os.path.join(GROUP, "docs", "orders.md")
if os.path.exists(go):
    txt = open(go, encoding="utf-8", errors="replace").read().splitlines()
    hits = [(i, l.strip()) for i, l in enumerate(txt, 1) if "@BigStream" in l or "BigStream" in l]
    add("bigstream_rows=%d" % len(hits))
    for i, h in hits[-3:]:
        add("L%d: %s" % (i, h[:200]))
    dhits = [(i, l.strip()) for i, l in enumerate(txt, 1) if re.search(r"2026-10-0[23]", l)]
    add("dated_1002_1003_rows=%d" % len(dhits))
    for i, h in dhits[-5:]:
        add("L%d: %s" % (i, h[:200]))
add("")

# export freshness
add("=== status-export.json ===")
se = os.path.join(ROOT, "docs", "status-export.json")
if os.path.exists(se):
    d = json.load(open(se, encoding="utf-8"))
    add("export_ts=%s" % d.get("export_ts"))
    for k in ("active", "current", "latest_artifact", "next_milestone", "milestone"):
        if k in d: add("%s=%s" % (k, str(d[k])[:200]))
    # dump top-level keys to find the three CEO-facing rows
    add("top_keys=%s" % list(d.keys())[:20])

with open(os.path.join(TMP, "r1159_all.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("ok %d lines" % len(lines))
