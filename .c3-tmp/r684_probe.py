# -*- coding: utf-8 -*-
# R684 quick five checks (anchors: orders O-20260928-1910 / ledger 37 / decisions 74) + three probes
import subprocess, os, re, io, json, glob, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".c3-tmp")
def p(rel): return os.path.join(ROOT, rel)

report = []
report.append("now=%s" % time.strftime("%Y-%m-%d %H:%M:%S"))

# 1. orders top + count (anchor O-20260928-1910, 42 files)
orders = sorted(glob.glob(p("orders/*")), key=os.path.getmtime)
top_order = os.path.basename(orders[-1]) if orders else "NONE"
report.append("orders_top=%s count=%d mtime=%s" % (top_order, len(orders),
    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(orders[-1]))) if orders else "-"))

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

# 4. index.lock + state production/tick
report.append("index_lock=%s" % os.path.exists(p(".git/index.lock")))
try:
    st = json.load(io.open(p("src/os/state.json"), "r", encoding="utf-8"))
    report.append("production=%s tick=%d logN=%d" % (st.get("production"), st.get("tick"), len(st.get("log", []))))
except Exception as e:
    report.append("state_err=%s" % e)

# 5. bm-a codex batch mtimes (#86 c+d unlock criterion)
for f in ["data/storylines/codex/README.md", "data/storylines/codex/city-humanities.md"]:
    fp = p(f)
    report.append("codex_%s mtime=%s" % (os.path.basename(f),
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(fp))) if os.path.exists(fp) else "GONE"))

# 6. render-leg supply precheck: F-032 source card PNG + .lc003-tmp inventory + .lc002-tmp reference build files
card_hits = []
for pat in ["output/cards/*census*v13*", "output/cards/*CENSUS*v13*", "output/renders/*", "data/storylines/**/*census*v13*"]:
    card_hits += glob.glob(p(pat), recursive=True)
report.append("v13_card_candidates=%d" % len(set(card_hits)))
with io.open(os.path.join(TMP, "r684_cards.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(set(card_hits))))
lc003 = sorted(os.listdir(p(".lc003-tmp"))) if os.path.isdir(p(".lc003-tmp")) else []
report.append("lc003_tmp_files=%s" % ",".join(lc003[:20]))
lc002 = sorted(os.listdir(p(".lc002-tmp"))) if os.path.isdir(p(".lc002-tmp")) else []
with io.open(os.path.join(TMP, "r684_lc002.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lc002))
report.append("lc002_tmp_files=%d" % len(lc002))

# 7. finished.md tail for F-055 row + F-032 pointer
try:
    with io.open(p("output/finished.md"), "r", encoding="utf-8") as f:
        fin = f.read()
    idx = fin.find("F-055")
    with io.open(os.path.join(TMP, "r684_fin_tail.txt"), "w", encoding="utf-8") as f:
        f.write(fin[max(0, idx-200):idx+1500] if idx >= 0 else fin[-2000:])
    report.append("finished_F055_found=%s len=%d" % (idx >= 0, len(fin)))
except Exception as e:
    report.append("finished_err=%s" % e)

# 8. three probes
PROBES = [
    ("board", ["python", "src/board_check.py"], "r684_board.txt"),
    ("readiness", ["python", "src/readiness.py"], "r684_readiness.txt"),
    ("loop_health", ["python", "src/os/loop_health.py"], "r684_health.txt"),
]
for name, cmd, out in PROBES:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, timeout=300)
    txt = (r.stdout.decode("utf-8", errors="replace") + "\n[stderr]\n" + r.stderr.decode("utf-8", errors="replace"))
    with io.open(os.path.join(TMP, out), "w", encoding="utf-8") as f:
        f.write(txt)
    report.append("%s: exit=%d" % (name, r.returncode))

with io.open(os.path.join(TMP, "r684_probe.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report))
print("OK")
