# -*- coding: utf-8 -*-
# R683 M1 plain-language check on LC-003 v1 beats (spoken-column scan)
import subprocess, io, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
r = subprocess.run(["python", "src/plain_language_check.py", "--beats",
                    "data/sources/lc003/voiceover-v1.beats.txt"],
                   cwd=ROOT, capture_output=True, timeout=120)
with io.open(os.path.join(ROOT, ".c3-tmp", "r683_m1.txt"), "w", encoding="utf-8") as f:
    f.write(r.stdout.decode("utf-8", errors="replace") + "\n[stderr]\n" +
            r.stderr.decode("utf-8", errors="replace"))
print("m1 exit=%d" % r.returncode)
