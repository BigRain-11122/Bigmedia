# -*- coding: utf-8 -*-
# R1390 clone-and-run: python io channel per encoding law (R1244/R1288), independent OUT (R1311)
import io, subprocess, sys

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
tmp = repo + r"\.c3-tmp"

for src, dst, marker in [
    (tmp + r"\r1389_check.py",  tmp + r"\r1390_check.py",  "r1389_check"),
    (tmp + r"\r1389_probes.py", tmp + r"\r1390_probes.py", "r1389_probes"),
]:
    body = io.open(src, encoding="utf-8").read()
    io.open(dst, "w", encoding="utf-8").write(body.replace(marker, marker.replace("1389", "1390")))

for script in [tmp + r"\r1390_check.py", tmp + r"\r1390_probes.py"]:
    p = subprocess.run([sys.executable, script], cwd=repo, capture_output=True, timeout=600)
    print(script, "rc=", p.returncode)
    err = (p.stderr or b"").decode("utf-8", "replace").strip()
    if err:
        print("stderr:", err[-400:])
