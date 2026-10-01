# -*- coding: utf-8 -*-
# r850 three probes (board_check / readiness / loop_health). R847 lineage rerun.
import subprocess, io, os, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".c3-tmp")
probes = [
    ("board", [os.path.join("src", "board_check.py")], "r850_board.txt"),
    ("readiness", [os.path.join("src", "readiness.py")], "r850_readiness.txt"),
    ("loop_health", [os.path.join("src", "os", "loop_health.py")], "r850_loop.txt"),
]
summary = []
for name, cmd, out in probes:
    p = subprocess.run(["python"] + cmd, cwd=ROOT, capture_output=True)
    text = (p.stdout or b"").decode("utf-8", errors="replace")
    if not text.strip():
        text = (p.stderr or b"").decode("utf-8", errors="replace")
    io.open(os.path.join(TMP, out), "w", encoding="utf-8").write(text)
    summary.append("== %s rc=%d evidence=%s lines=%d" % (name, p.returncode, out, len(text.splitlines())))
    key = [l for l in text.splitlines()
           if re.search(r"FAIL|WARN|PASS|OK|blocker|blockers|findings", l, re.I)]
    for l in key[:10]:
        summary.append("  " + l.strip()[:260])
    tail = [l for l in text.splitlines() if l.strip()][-3:]
    summary.append("  --tail--")
    for l in tail:
        summary.append("  " + l.strip()[:260])
io.open(os.path.join(TMP, "r850_probe_summary.txt"), "w", encoding="utf-8").write("\n".join(summary))
print("probes done, summary written")

