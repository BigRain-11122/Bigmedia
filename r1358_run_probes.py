# -*- coding: utf-8 -*-
# Run the three standard probes with UTF-8 capture (python io channel per encoding law)
import os, subprocess

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"
PY = "python"
jobs = [
    ("board", ["src/board_check.py"], "r1358_probe_board.txt"),
    ("readiness", ["src/readiness.py"], "r1358_probe_readiness.txt"),
    ("loop", ["src/os/loop_health.py"], "r1358_probe_loop.txt"),
]
for name, args, out in jobs:
    r = subprocess.run([PY] + args, cwd=ROOT, capture_output=True, env=env)
    with open(os.path.join(ROOT, out), "wb") as f:
        f.write(r.stdout)
        if r.stderr:
            f.write(b"\n[stderr]\n")
            f.write(r.stderr)
    print("%s rc=%d bytes_out=%d" % (name, r.returncode, len(r.stdout)))
print("RUN_OK")
