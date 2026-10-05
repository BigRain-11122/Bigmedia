# -*- coding: utf-8 -*-
# R1401 probe clone+run (python io channel per R1244/R1288 encoding law; ASCII-safe)
import io, subprocess, sys

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"

hdr_old1 = "# R1400 five-check fresh probe (declared-idle window 6/6 batch close R1395~R1400; OSS w4 gate 21:40 not yet open at 20:0x; ASCII-safe per encoding law)"
hdr_old2 = "# lineage: r1399_check.py pattern (batch-close window 6/6) (python io channel clone per R1244/R1288)"
hdr_new1 = "# R1401 five-check fresh probe (declared-idle new window 1/6 after R1400 batch close; OSS w4 gate 21:40 not yet open at 20:1x; ASCII-safe per encoding law)"
hdr_new2 = "# lineage: r1400_check.py pattern (new window first round) (python io channel clone per R1244/R1288)"

src = io.open(repo + r"\.c3-tmp\r1400_check.py", encoding="utf-8").read()
src = src.replace(hdr_old1, hdr_new1).replace(hdr_old2, hdr_new2).replace("r1400_check.txt", "r1401_check.txt")
io.open(repo + r"\.c3-tmp\r1401_check.py", "w", encoding="utf-8").write(src)

prb = io.open(repo + r"\.c3-tmp\r1400_probes.py", encoding="utf-8").read()
prb = prb.replace("r1400_probes.txt", "r1401_probes.txt")
io.open(repo + r"\.c3-tmp\r1401_probes.py", "w", encoding="utf-8").write(prb)

for f in [r"\.c3-tmp\r1401_check.py", r"\.c3-tmp\r1401_probes.py"]:
    p = subprocess.run([sys.executable, f], cwd=repo, capture_output=True, timeout=420)
    print(f, "rc=", p.returncode)
    err = (p.stderr or b"").decode("utf-8", "replace").strip()
    if err:
        print("[stderr]", err[-500:])
print("done")
