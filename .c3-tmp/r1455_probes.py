# -*- coding: utf-8 -*-
"""R1455 three-probe runner (board/readiness/loop_health) -> UTF-8 files (R1454 caliber clone)."""
import os, subprocess, io, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".c3-tmp")
env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"

probes = [
    ("board", ["python", "src\\board_check.py"]),
    ("readiness", ["python", "src\\readiness.py"]),
    ("loop", ["python", "src\\os\\loop_health.py"]),
]
summary = []
for name, cmd in probes:
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    out = (p.stdout or "") + (p.stderr or "")
    with open(os.path.join(TMP, "r1455_%s.txt" % name), "w", encoding="utf-8") as f:
        f.write(out)
    summary.append("%s rc=%d lines=%d" % (name, p.returncode, len(out.splitlines())))

facts = []
for name in ("board", "readiness", "loop"):
    path = os.path.join(TMP, "r1455_%s.txt" % name)
    with io.open(path, "r", encoding="utf-8") as f:
        txt = f.read()
    fails = [ln for ln in txt.splitlines() if re.search(r"FAIL|BLOCKER", ln)]
    facts.append("=== %s (key lines) ===" % name)
    facts.extend(fails[:15] if fails else ["(no FAIL/blocker lines)"])
    facts.append("")
with io.open(os.path.join(TMP, "r1455_probe_facts.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(facts))
print("; ".join(summary))
