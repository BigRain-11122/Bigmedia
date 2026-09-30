# -*- coding: utf-8 -*-
# R682 quick five checks (anchors: ledger 37 / decisions 70 per R681 baseline)
import os, re, io, json, glob, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.dirname(os.path.abspath(__file__))
def p(rel): return os.path.join(ROOT, rel)

report = []

# 0. now
report.append("now=%s" % time.strftime("%Y-%m-%d %H:%M:%S"))

# 1. orders top file + count
orders = sorted(glob.glob(p("orders/*")), key=os.path.getmtime)
top_order = os.path.basename(orders[-1]) if orders else "NONE"
report.append("orders_top=%s mtime=%s count=%d" % (top_order, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(orders[-1]))) if orders else "-", len(orders)))

# 2. ledger six-mode CaseSensitive count
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

# 3. decisions UTF8 non-empty count
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
try:
    with io.open(DEC, "r", encoding="utf-8") as f:
        lines = [l for l in f if l.strip()]
    report.append("decisions_nonempty=%d (anchor 70)" % len(lines))
except Exception as e:
    report.append("decisions_err=%s" % e)

# 4. index.lock
report.append("index_lock=%s" % os.path.exists(p(".git/index.lock")))

# 5. state production/tick + R681 entry tail (from 4th marker)
try:
    st = json.load(io.open(p("src/os/state.json"), "r", encoding="utf-8"))
    report.append("production=%s tick=%d logN=%d" % (st.get("production"), st.get("tick"), len(st.get("log", []))))
    last = st["log"][-1]
    idx = last.find("\u2463")
    tail = last[idx:] if idx >= 0 else last[-1500:]
    with io.open(os.path.join(TMP, "r682_r681tail.txt"), "w", encoding="utf-8") as f:
        f.write(tail)
    report.append("r681_tail_written=%d chars" % len(tail))
except Exception as e:
    report.append("state_err=%s" % e)

# 6. backlog numbered rows (first 10)
try:
    with io.open(p("src/os/backlog.md"), "r", encoding="utf-8") as f:
        bl = f.read()
    rows = [l[:160] for l in bl.splitlines() if re.match(r"^\*\*\d+\.|^?\d+\.\s", l)]
    with io.open(os.path.join(TMP, "r682_bktop.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rows[:12]))
    report.append("backlog_rowN=%d" % len(rows))
except Exception as e:
    report.append("backlog_err=%s" % e)

# 7. bm-a codex batch mtimes
for f in ["data/storylines/codex/README.md", "data/storylines/codex/city-humanities.md"]:
    fp = p(f)
    report.append("codex_%s mtime=%s" % (os.path.basename(f), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(fp))) if os.path.exists(fp) else "GONE"))

# 8. HEAD
try:
    head = os.popen("git rev-parse --short HEAD").read().strip()
    report.append("HEAD=%s" % head)
except Exception as e:
    report.append("git_err=%s" % e)

with io.open(os.path.join(TMP, "r682_probe.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report))
print("\n".join(report))
