# -*- coding: utf-8 -*-
# R681 quick five checks (six-mode CaseSensitive per R677+ anchor discipline)
import os, re, io, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def p(rel): return os.path.join(ROOT, rel)

report = []

# 1. orders top file
orders = sorted(glob.glob(p("orders/*")), key=os.path.getmtime)
top_order = os.path.basename(orders[-1]) if orders else "NONE"
report.append("orders_top=%s mtime=%s" % (top_order, os.path.getmtime(orders[-1]) if orders else "-"))

# 2. ledger six-mode CaseSensitive count (strict @ prefix, CaseSensitive)
LED = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
count = 0
try:
    with io.open(LED, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if re.search(r"@BigStream|@七线全司|@全司|@六司|@八线|@全公司|@all-companies", line):
                count += 1
    report.append("ledger_sixmode_count=%d (anchor 35)" % count)
except Exception as e:
    report.append("ledger_err=%s" % e)

# 3. decisions UTF8 non-empty count
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
try:
    with io.open(DEC, "r", encoding="utf-8") as f:
        lines = [l for l in f if l.strip()]
    report.append("decisions_nonempty=%d (anchor 69)" % len(lines))
except Exception as e:
    report.append("decisions_err=%s" % e)

# 4. index.lock
report.append("index_lock=%s" % os.path.exists(p(".git/index.lock")))

# 5. state production
try:
    st = json.load(io.open(p("src/os/state.json"), "r", encoding="utf-8"))
    report.append("production=%s tick=%d" % (st.get("production"), st.get("tick")))
except Exception as e:
    report.append("state_err=%s" % e)

# 6. daily brief 09-29 present
report.append("daily_0929=%s" % os.path.exists(p("data/intel/daily/2026-09-29.md")))

# 7. W40 audit present
w40 = glob.glob(p("docs/audits/*W40*"))
report.append("w40_audit=%s" % (os.path.basename(w40[-1]) if w40 else "NONE"))

# 8. backlog top rows
try:
    with io.open(p("src/os/backlog.md"), "r", encoding="utf-8") as f:
        bl = f.read()
    rows = [l for l in bl.splitlines() if l.strip().startswith("#")]
    report.append("backlog_top3=%s" % json.dumps(rows[:3], ensure_ascii=False))
except Exception as e:
    report.append("backlog_err=%s" % e)

# 9. LC-002 files present
lc = ".lc002-tmp"
for fn in ["audio.mp3", "subs.srt", "s2-results.md"]:
    report.append("lc002_%s=%s" % (fn, os.path.exists(p(os.path.join(lc, fn)))))
mp4 = p("output/renders/lc-002-v1-shipinhao-60s.mp4")
report.append("lc002_mp4=%s" % os.path.exists(mp4))
plan = p("output/renders/lc-002-v1-shipinhao-60s.mp4.plan.json")
report.append("lc002_plan=%s" % os.path.exists(plan))

# 10. finished.md LC registry (LC-001 precedent)
try:
    fin = io.open(p("output/finished.md"), "r", encoding="utf-8").read()
    report.append("finished_LC-001=%s" % ("LC-001" in fin))
    report.append("finished_LC-002=%s" % ("LC-002" in fin))
except Exception as e:
    report.append("finished_err=%s" % e)

# 11. bm-a codex batch still uncommitted? mtimes
for f in ["data/storylines/codex/README.md", "data/storylines/codex/city-humanities.md"]:
    fp = p(f)
    report.append("codex_%s mtime=%s" % (os.path.basename(f), os.path.getmtime(fp) if os.path.exists(fp) else "GONE"))

with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "r681_probe.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report))
print("\n".join(report))
