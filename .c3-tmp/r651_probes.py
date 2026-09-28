# -*- coding: utf-8 -*-
"""R651 three-probe runner (UTF-8 file evidence, avoid GBK console)."""
import io, os, subprocess

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
probes = [
    ("board", ["python", "src/board_check.py"]),
    ("readiness", ["python", "src/readiness.py"]),
    ("loop_health", ["python", "src/os/loop_health.py"]),
]
out = []
for name, cmd in probes:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True)
    txt = (r.stdout + b"\n" + r.stderr).decode("utf-8", errors="replace")
    out.append("=== %s rc=%d ===\n%s" % (name, r.returncode, txt[-3000:]))
with io.open(os.path.join(ROOT, ".c3-tmp", "r651_probes.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("WROTE r651_probes.txt")
