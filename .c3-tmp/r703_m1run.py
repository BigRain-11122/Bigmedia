# -*- coding: utf-8 -*-
# R703 LC-009 M1 check (plain_language_check --beats, r696_m1run.py channel)
import io, os, subprocess, sys
ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = []
r = subprocess.run([sys.executable, "src/plain_language_check.py", "--beats",
                   r"data\sources\lc009\voiceover-v1.beats.txt"],
                  cwd=ROOT, capture_output=True, timeout=120)
txt = r.stdout.decode("utf-8", errors="replace")
out.append("exit=%d" % r.returncode)
out.append(txt[-2000:])
out.append("[stderr]")
out.append(r.stderr.decode("utf-8", errors="replace")[-500:])
with io.open(os.path.join(ROOT, ".c3-tmp/r703_m1.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("M1_DONE exit=%d" % r.returncode)
