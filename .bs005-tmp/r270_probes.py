# -*- coding: utf-8 -*-
# R270: three probes runner (board / readiness / loop_health) with
# python-internal UTF-8 file redirect (PS `>` pipeline = PS5.1 UTF-16
# re-encode trap, R269 lesson). Also routine file checks: daily brief,
# weekly audit, global-benchmarks date, self-improvement queue mtime.
import io
import os
import subprocess
import sys
import time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".bs005-tmp")


def run(name, script, out):
    r = subprocess.run([sys.executable, "-X", "utf8", script],
                       cwd=ROOT, capture_output=True)
    text = r.stdout.decode("utf-8", errors="replace")
    if r.stderr.strip():
        text += "\n[stderr]\n" + r.stderr.decode("utf-8", errors="replace")
    io.open(os.path.join(TMP, out), "w", encoding="utf-8").write(text)
    fails = text.count("FAIL")
    warns = text.count("WARN")
    print("%s rc=%d FAIL=%d WARN=%d" % (name, r.returncode, fails, warns))
    shown = 0
    for line in text.splitlines():
        if ("FAIL" in line or "WARN" in line) and shown < 8:
            print("  |%s" % line.strip()[:170])
            shown += 1
    return r.returncode


run("board", "src/board_check.py", "board-r270.txt")
run("readiness", "src/readiness.py", "readiness-r270.txt")
run("loop_health", "src/os/loop_health.py", "loop-health-r270.txt")

daily = os.path.join(ROOT, "data", "intel", "daily", "2026-09-25.md")
print("daily-brief-2026-09-25 exists=%s" % os.path.exists(daily))
aud = os.path.join(ROOT, "docs", "audits")
w39 = [f for f in os.listdir(aud) if "W39" in f] if os.path.isdir(aud) else []
print("weekly-audit W39 files=%s" % (sorted(w39) if w39 else "NONE"))

siq = os.path.join(ROOT, "docs", "self-improvement-queue.md")
if os.path.exists(siq):
    print("self-improvement-queue mtime=%s"
          % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(siq))))
gb = os.path.join(ROOT, "docs", "global-benchmarks.md")
if os.path.exists(gb):
    with io.open(gb, "r", encoding="utf-8") as f:
        for line in f:
            if "2026-" in line:
                print("global-benchmarks first-date-line=%s" % line.strip()[:120])
                break
