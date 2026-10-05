# -*- coding: utf-8 -*-
# R1386 driver: clone R1385 check/probes scripts via python io channel (encoding law
# R1244/R1288/R1368 - never PS Copy-Item for .py with Chinese regex), then run both.
import io, subprocess, sys

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"

for src, dst in [(r"\.c3-tmp\r1385_check.py", r"\.c3-tmp\r1386_check.py"),
                 (r"\.c3-tmp\r1385_probes.py", r"\.c3-tmp\r1386_probes.py")]:
    txt = io.open(repo + src, encoding="utf-8").read()
    txt = txt.replace("r1385", "r1386").replace("R1385", "R1386")
    io.open(repo + dst, "w", encoding="utf-8").write(txt)

for script in [r"\.c3-tmp\r1386_check.py", r"\.c3-tmp\r1386_probes.py"]:
    p = subprocess.run([sys.executable, repo + script], cwd=repo, capture_output=True, timeout=600)
    print(script, "rc=", p.returncode)
    err = (p.stderr or b"").decode("utf-8", "replace").strip()
    if err:
        print("[stderr]", err[-500:])
print("driver done")
