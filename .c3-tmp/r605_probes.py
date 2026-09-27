# -*- coding: utf-8 -*-
# R605 probes runner: board / readiness / loop_health (R562 law: outputs written UTF-8 via io.open in-file)
import io, os, re, subprocess, sys

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".c3-tmp")

def run(tag, script):
    r = subprocess.run([sys.executable, script], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "") + (r.stderr or "")
    io.open(os.path.join(TMP, "r605_%s.txt" % tag), "w", encoding="utf-8").write(out)
    m = re.findall(r"(\d+)\s*FAIL\s*[^\n]*?(\d+)\s*WARN", out)
    fails = sum(int(a) for a, b in m)
    warns = sum(int(b) for a, b in m)
    print("%s: exit=%d FAIL=%d WARN=%d" % (tag, r.returncode, fails, warns))
    for l in [l for l in out.splitlines() if l.strip()][-2:]:
        print("   |", l.encode("ascii", "replace").decode("ascii")[:150])

run("board", os.path.join("src", "board_check.py"))
run("readiness", os.path.join("src", "readiness.py"))
run("loop", os.path.join("src", "os", "loop_health.py"))
