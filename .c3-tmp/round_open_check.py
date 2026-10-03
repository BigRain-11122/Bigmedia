import json, os, re, subprocess, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP   = r"C:\Users\sjs20\Desktop\FluxGroup"
OUT   = os.path.join(ROOT, ".c3-tmp", "round_open_report.txt")
L = []
def p(s=""): L.append(str(s))

state = json.load(open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
p("== STATE ==")
p("tick=%s" % state.get("tick"))
p("ts=%s" % state.get("ts"))
p("task=%s" % state.get("task"))
p("production=%s" % state.get("production"))
wm = state.get("decisions_watermark") or {}
p("decisions_watermark=%s" % json.dumps(wm, ensure_ascii=False))
log = state.get("log") or []
p("log_count=%d" % len(log))
for e in log[-3:]:
    p("--- LOG ---")
    p(e)

p("== ORDERS DIR (top5 mtime) ==")
od = os.path.join(ROOT, "orders")
for f in sorted(os.listdir(od), key=lambda x: os.path.getmtime(os.path.join(od, x)), reverse=True)[:5]:
    fp = os.path.join(od, f)
    p("%s | %s" % (f, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(fp)))))

p("== GIT ==")
r = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
p(r.stdout.strip() or "(clean)")
p("index_lock=%s" % os.path.exists(os.path.join(ROOT, ".git", "index.lock")))
r = subprocess.run(["git", "log", "-5", "--oneline"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
p(r.stdout)

p("== GROUP DECISIONS ==")
dec_path = os.path.join(GRP, "docs", "decisions.md")
dec = open(dec_path, encoding="utf-8").read()
nums = sorted(set(re.findall(r"[DC]-\d{8}-\d{2}", dec)))
p("dnums_count=%d" % len(nums))
p(",".join(nums))
p("-- head 45 lines --")
for i, l in enumerate(dec.splitlines()[:45], 1):
    p("L%02d| %s" % (i, l))

p("== GROUP ORDERS head 25 ==")
go = os.path.join(GRP, "docs", "orders.md")
if os.path.exists(go):
    for i, l in enumerate(open(go, encoding="utf-8").read().splitlines()[:25], 1):
        p("L%02d| %s" % (i, l))

p("== LEDGER @BigStream ==")
led = open(os.path.join(GRP, "cph4", "evolution-ledger.md"), encoding="utf-8").read().splitlines()
hits = [(i, l) for i, l in enumerate(led, 1) if "@BigStream" in l]
p("hit_count=%d" % len(hits))
for i, l in hits[-4:]:
    p("L%d| %s" % (i, l[:300]))
for tag in ("@七线", "@全司", "@六司", "@八线"):
    t = [(i, l) for i, l in enumerate(led, 1) if tag in l]
    p("tag %s count=%d" % (tag, len(t)))
    for i, l in t[-2:]:
        p("  L%d| %s" % (i, l[:200]))

p("== ROUTINE ==")
p("daily_20261003=%s" % os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-10-03.md")))
ad = os.path.join(ROOT, "docs", "audits")
if os.path.exists(ad):
    for f in sorted(os.listdir(ad)):
        p("audit_file: %s" % f)
gb = os.path.join(ROOT, "docs", "global-benchmarks.md")
if os.path.exists(gb):
    txt = open(gb, encoding="utf-8").read().splitlines()
    p("global_benchmarks first 8 lines:")
    for l in txt[:8]:
        p("  %s" % l)

p("== FINISHED TAIL ==")
fin = open(os.path.join(ROOT, "output", "finished.md"), encoding="utf-8").read().splitlines()
for l in fin[-12:]:
    p("  %s" % l)

open(OUT, "w", encoding="utf-8").write("\n".join(L))
print("report written: %s (%d lines)" % (OUT, len(L)))
