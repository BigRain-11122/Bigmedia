# -*- coding: utf-8 -*-
# R683 probe runner: board_check / readiness / loop_health -> UTF-8 files
import subprocess, time, re, io, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
PROBES = [
    ("board", ["python", "src/board_check.py"], "r683_board.txt"),
    ("readiness", ["python", "src/readiness.py"], "r683_readiness.txt"),
    ("loop_health", ["python", "src/os/loop_health.py"], "r683_health.txt"),
]
summary = []
for name, cmd, out in PROBES:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, timeout=300)
    txt = (r.stdout.decode("utf-8", errors="replace") + "\n[stderr]\n" +
           r.stderr.decode("utf-8", errors="replace"))
    with io.open(os.path.join(ROOT, ".c3-tmp", out), "w", encoding="utf-8") as f:
        f.write(txt)
    summary.append("%s: exit=%d" % (name, r.returncode))

# global-benchmarks section-4 first dated line (7-day gate check)
gb = os.path.join(ROOT, "docs", "global-benchmarks.md")
with io.open(gb, encoding="utf-8") as f:
    lines = f.read().splitlines()
idx = next((i for i, x in enumerate(lines) if "更新记录" in x), None)
first_date = None
if idx is not None:
    for x in lines[idx:idx + 12]:
        m = re.search(r"2026-\d\d-\d\d", x)
        if m:
            first_date = m.group(0)
            break
summary.append("GB sec4 first date: %s" % first_date)

with io.open(os.path.join(ROOT, ".c3-tmp", "r683_probes_sum.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(summary))
print("OK")
