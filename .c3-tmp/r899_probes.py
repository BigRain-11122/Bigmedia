# -*- coding: utf-8 -*-
"""R899 probe driver: run content-address scan + three probes, save evidence files."""
import subprocess, io, sys

CMDS = [
    (r".c3-tmp\r807_scan.py", r".c3-tmp\r899_scan.txt"),
    (r"src\board_check.py", r".c3-tmp\r899_board.txt"),
    (r"src\readiness.py", r".c3-tmp\r899_rd.txt"),
    (r"src\os\loop_health.py", r".c3-tmp\r899_loop.txt"),
]

for script, out in CMDS:
    p = subprocess.run([sys.executable, script], capture_output=True)
    io.open(out, "wb").write(p.stdout + p.stderr)
    print("ran", script, "rc", p.returncode, "->", out)
print("ALL DONE")
