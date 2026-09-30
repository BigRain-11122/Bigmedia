# -*- coding: utf-8 -*-
# R696 five-check probe (anchors: orders O-20260928-1910 / ledger 38 / decisions 75)
import subprocess, os, re, io, json, glob, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".c3-tmp")
def p(rel): return os.path.join(ROOT, rel)

report = []
report.append("now=%s" % time.strftime("%Y-%m-%d %H:%M:%S"))

# 1. orders top + count (anchor O-20260928-1910, 42 files)
orders = sorted(glob.glob(p("orders/*")), key=os.path.getmtime)
top_order = os.path.basename(orders[-1]) if orders else "NONE"
report.append("orders_top=%s count=%d" % (top_order, len(orders)))

# 2. ledger six-mode CaseSensitive count (anchor 38)
LED = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
count = 0
new_rows = []
try:
    with io.open(LED, "r", encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            if re.search(r"@BigStream|@七线全司|@全司|@六司|@八线|@全公司|@all-companies", line):
                count += 1
                new_rows.append("L%d %s" % (i, line[:120].replace("\n", "")))
    report.append("ledger_sixmode_count=%d (anchor 38)" % count)
    if count > 38:
        report.append("ledger_NEW_ROWS_BELOW_38:")
        report.extend(new_rows[38:])
except Exception as e:
    report.append("ledger_err=%s" % e)

# 3. decisions UTF8 non-empty (anchor 75)
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
try:
    with io.open(DEC, "r", encoding="utf-8") as f:
        lines = [l for l in f if l.strip()]
    report.append("decisions_nonempty=%d (anchor 75)" % len(lines))
except Exception as e:
    report.append("decisions_err=%s" % e)

# 4. index.lock + state production/tick
report.append("index_lock=%s" % os.path.exists(p(".git/index.lock")))
try:
    st = json.load(io.open(p("src/os/state.json"), "r", encoding="utf-8"))
    report.append("production=%s tick=%d" % (st.get("production"), st.get("tick")))
except Exception as e:
    report.append("state_err=%s" % e)

# 5. bm-a codex batch mtimes (#86 c+d unlock criterion, anchor mtime 04:06)
for f in ["data/storylines/codex/README.md", "data/storylines/codex/city-humanities.md"]:
    fp = p(f)
    report.append("codex_%s mtime=%s" % (os.path.basename(f),
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(fp))) if os.path.exists(fp) else "GONE"))

# 6. round.lock
rl = p("logs/iteration-loop/round.lock")
report.append("round_lock=%s" % (os.path.exists(rl)))

# 7. daily brief 09-29 / 09-30 presence (REACT v6 window precondition)
for d in ["2026-09-29", "2026-09-30"]:
    db = p("data/intel/daily/%s.md" % d)
    report.append("daily_%s=%s" % (d, os.path.exists(db)))

# 8. three probes
PROBES = [
    ("board", ["python", "src/board_check.py"], "r696_board.txt"),
    ("readiness", ["python", "src/readiness.py"], "r696_readiness.txt"),
    ("loop_health", ["python", "src/os/loop_health.py"], "r696_health.txt"),
]
for name, cmd, out in PROBES:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, timeout=300)
    txt = (r.stdout.decode("utf-8", errors="replace") + "\n[stderr]\n" + r.stderr.decode("utf-8", errors="replace"))
    with io.open(os.path.join(TMP, out), "w", encoding="utf-8") as f:
        f.write(txt)
    report.append("%s: exit=%d" % (name, r.returncode))

with io.open(os.path.join(TMP, "r696_probe.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report))
print("PROBE_DONE")
