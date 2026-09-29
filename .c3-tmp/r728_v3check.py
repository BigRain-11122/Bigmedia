# -*- coding: utf-8 -*-
# R728 v3 checks: M1 plain-language + col2 verbatim zero-change vs v1 + spoken delta
import io, subprocess, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def cols(p):
    rows = [l.rstrip("\n") for l in io.open(p, encoding="utf-8") if l.strip()]
    return [tuple(c.strip() for c in r.split(" | ")) for r in rows]

v1 = cols(os.path.join(ROOT, "data/sources/lc015/voiceover-v1.beats.txt"))
v3 = cols(os.path.join(ROOT, "data/sources/lc015/voiceover-v3.beats.txt"))
same = all(a[0] == b[0] and a[1] == b[1] for a, b in zip(v1, v3))
delta = sum(len(b[2]) - len(a[2]) for a, b in zip(v1, v3))
print("rows", len(v1), len(v3), "ALL_COL2_VERBATIM=", same, "spoken_delta_v1_to_v3=", delta)

r = subprocess.run([sys.executable, "-X", "utf8", "src/plain_language_check.py",
                   "--beats", "data/sources/lc015/voiceover-v3.beats.txt"],
                  cwd=ROOT, capture_output=True, timeout=120)
txt = r.stdout.decode("utf-8", errors="replace")
print("M1_v3_exit=", r.returncode)
print(txt[:300])
with io.open(os.path.join(ROOT, ".c3-tmp/r728_m1_v3.txt"), "w", encoding="utf-8") as f:
    f.write("exit=%d\n%s" % (r.returncode, txt))
