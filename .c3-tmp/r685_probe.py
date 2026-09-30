# -*- coding: utf-8 -*-
# R685 five-check probe (anchors: orders O-20260928-1910 / ledger 37 / decisions 74)
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

# 2. ledger six-mode CaseSensitive count (anchor 37)
LED = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
count = 0
try:
    with io.open(LED, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if re.search(r"@BigStream|@七线全司|@全司|@六司|@八线|@全公司|@all-companies", line):
                count += 1
    report.append("ledger_sixmode_count=%d (anchor 37)" % count)
except Exception as e:
    report.append("ledger_err=%s" % e)

# 3. decisions UTF8 non-empty (anchor 74)
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
try:
    with io.open(DEC, "r", encoding="utf-8") as f:
        lines = [l for l in f if l.strip()]
    report.append("decisions_nonempty=%d (anchor 74)" % len(lines))
except Exception as e:
    report.append("decisions_err=%s" % e)

# 4. index.lock + state production/tick + round.lock
report.append("index_lock=%s" % os.path.exists(p(".git/index.lock")))
try:
    st = json.load(io.open(p("src/os/state.json"), "r", encoding="utf-8"))
    report.append("production=%s tick=%d" % (st.get("production"), st.get("tick")))
except Exception as e:
    report.append("state_err=%s" % e)

# 5. bm-a codex batch mtimes (#86 c+d unlock criterion)
for f in ["data/storylines/codex/README.md", "data/storylines/codex/city-humanities.md"]:
    fp = p(f)
    report.append("codex_%s mtime=%s" % (os.path.basename(f),
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(fp))) if os.path.exists(fp) else "GONE"))

# 6. lc002 asr/e4 wrapper inventory (reuse for LC-003 closure)
lc002 = sorted(os.listdir(p(".lc002-tmp"))) if os.path.isdir(p(".lc002-tmp")) else []
asr_e4 = [x for x in lc002 if ("asr" in x.lower() or "e4" in x.lower())]
report.append("lc002_asr_e4_files=%s" % ",".join(asr_e4))

# 7. three probes
PROBES = [
    ("board", ["python", "src/board_check.py"], "r685_board.txt"),
    ("readiness", ["python", "src/readiness.py"], "r685_readiness.txt"),
    ("loop_health", ["python", "src/os/loop_health.py"], "r685_health.txt"),
]
for name, cmd, out in PROBES:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, timeout=300)
    txt = (r.stdout.decode("utf-8", errors="replace") + "\n[stderr]\n" + r.stderr.decode("utf-8", errors="replace"))
    with io.open(os.path.join(TMP, out), "w", encoding="utf-8") as f:
        f.write(txt)
    report.append("%s: exit=%d" % (name, r.returncode))

with io.open(os.path.join(TMP, "r685_probe.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report))
print("PROBE_DONE")
