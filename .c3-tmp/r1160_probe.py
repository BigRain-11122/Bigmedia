# -*- coding: utf-8 -*-
# R1160 probes + queue E31 + REACT probe pattern locate. Output: r1160_probe.txt
import subprocess, os, re, datetime, io, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.dirname(os.path.abspath(__file__))
lines = []
def add(s): lines.append(str(s))
def run(label, args):
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (p.stdout or "") + (p.stderr or "")
    add("=== %s (rc=%d) ===" % (label, p.returncode))
    add(out.strip()[-1800:])
    add("")

add("now=%s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
run("BOARD", ["python", "src/board_check.py"])
run("READINESS", ["python", "src/readiness.py"])
run("LOOP_HEALTH", ["python", "src/os/loop_health.py"])

# queue §E E31 entry
q = os.path.join(ROOT, "docs", "self-improvement-queue.md")
if os.path.exists(q):
    qt = io.open(q, encoding="utf-8").read()
    i = qt.find("E31")
    add("=== QUEUE E31 ===")
    add(qt[max(0,i-200):i+900] if i>=0 else "E31 NOT FOUND")
add("")

# r1030 probe scripts on disk
add("=== r1030 files ===")
for f in sorted(glob.glob(os.path.join(TMP, "r1030*"))):
    add(os.path.basename(f))
add("")

# r1030_react_probe.txt head (pattern for M0 selection probe)
p = os.path.join(TMP, "r1030_react_probe.txt")
if os.path.exists(p):
    add("=== r1030_react_probe.txt head ===")
    add(io.open(p, encoding="utf-8", errors="replace").read()[:2500])

io.open(os.path.join(TMP, "r1160_probe.txt"), "w", encoding="utf-8").write("\n".join(lines))
print("ok", len(lines))
