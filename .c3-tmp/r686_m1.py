# -*- coding: utf-8 -*-
# R686 M1 plain-language check on LC-004 beats (spoken-column scan)
import subprocess, io, os, sys

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
ver = sys.argv[1] if len(sys.argv) > 1 else "v1"
r = subprocess.run(["python", "src/plain_language_check.py", "--beats",
                    "data/sources/lc004/voiceover-%s.beats.txt" % ver],
                   cwd=ROOT, capture_output=True, timeout=120)
with io.open(os.path.join(ROOT, ".c3-tmp", "r686_m1_%s.txt" % ver), "w", encoding="utf-8") as f:
    f.write(r.stdout.decode("utf-8", errors="replace") + "\n[stderr]\n" +
            r.stderr.decode("utf-8", errors="replace"))
print("m1 %s exit=%d" % (ver, r.returncode))
