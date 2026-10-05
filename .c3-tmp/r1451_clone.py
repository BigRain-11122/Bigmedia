# -*- coding: utf-8 -*-
"""Clone r1450 check/probe scripts -> r1451 and run both (R1449->R1450 chain pattern)."""
import io, subprocess, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".c3-tmp")

for src, dst in [("r1450_check.py", "r1451_check.py"), ("r1450_probes.py", "r1451_probes.py")]:
    t = io.open(os.path.join(TMP, src), encoding="utf-8").read()
    t = t.replace("r1450", "r1451").replace("R1450", "R1451")
    io.open(os.path.join(TMP, dst), "w", encoding="utf-8").write(t)
    print("cloned %s" % dst)

p1 = subprocess.run(["python", os.path.join(".c3-tmp", "r1451_check.py")], cwd=ROOT,
                    capture_output=True, text=True, encoding="utf-8", errors="replace")
print("check rc=%d: %s" % (p1.returncode, (p1.stdout or "").strip()))
if p1.returncode != 0:
    print("check stderr: %s" % (p1.stderr or "")[:500])

p2 = subprocess.run(["python", os.path.join(".c3-tmp", "r1451_probes.py")], cwd=ROOT,
                    capture_output=True, text=True, encoding="utf-8", errors="replace")
print("probes rc=%d: %s" % (p2.returncode, (p2.stdout or "").strip()))
if p2.returncode != 0:
    print("probes stderr: %s" % (p2.stderr or "")[:500])
