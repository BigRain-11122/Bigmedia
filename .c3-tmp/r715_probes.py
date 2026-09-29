# -*- coding: utf-8 -*-
# R715: three probes (board/readiness/loop_health) -> UTF-8 file
import io, os, subprocess, sys

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"
out = io.open(os.path.join(ROOT, ".c3-tmp", "r715_probes.txt"), "w", encoding="utf-8")
for name, cmd in [
    ("board_check", [sys.executable, "src" + os.sep + "board_check.py"]),
    ("readiness", [sys.executable, "src" + os.sep + "readiness.py"]),
    ("loop_health", [sys.executable, "src" + os.sep + "os" + os.sep + "loop_health.py"]),
]:
    p = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True)
    txt = p.stdout.decode("utf-8", "replace")
    out.write("=== %s exit=%d ===\n%s\n" % (name, p.returncode, txt))
    err = p.stderr.decode("utf-8", "replace").strip()
    if err:
        out.write("[stderr] " + err[-500:] + "\n")
out.close()
print("probes done")
