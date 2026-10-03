# r1189 fast-path five-check (ASCII only)
import os, re, io, json, glob, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP  = r"C:\Users\sjs20\Desktop\FluxGroup"
now = datetime.datetime.now()
lines = []
def p(s): lines.append(s)

# 1) orders latest
orders = sorted(glob.glob(os.path.join(ROOT, "orders", "*")))
latest_order = orders[-1] if orders else "NONE"
p("orders_latest=%s mtime=%s" % (os.path.basename(latest_order),
   datetime.datetime.fromtimestamp(os.path.getmtime(latest_order)).strftime("%m-%d %H:%M") if orders else "-"))

# 2) evolution-ledger @BigStream / @七线全司 / @全司 / @六司 rows
led = os.path.join(GRP, "cph4", "evolution-ledger.md")
txt = io.open(led, encoding="utf-8", errors="replace").read()
hits = [l for l in txt.splitlines() if re.search(r"@BigStream|@七线全司|@全司|@六司", l)]
p("ledger_target_rows=%d mtime=%s" % (len(hits),
   datetime.datetime.fromtimestamp(os.path.getmtime(led)).strftime("%m-%d %H:%M")))
for h in hits[-3:]: p("  LED_TAIL: " + h[:160])

# 3) decisions.md dnums set diff vs state watermark
dtxt = io.open(os.path.join(GRP, "docs", "decisions.md"), encoding="utf-8", errors="replace").read()
dset = set(re.findall(r"[DC]-\d{8}-\d{2}", dtxt))
st = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
wm = set(st["decisions_watermark"]["dnums"])
new = sorted(dset - wm)
p("decisions_dnums_file=%d wm=%d NEW=%s mtime=%s" % (len(dset), len(wm), new,
   datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(GRP, "docs", "decisions.md"))).strftime("%m-%d %H:%M")))

# 4) backlog top unfinished line
bg = io.open(os.path.join(ROOT, "src", "os", "backlog.md"), encoding="utf-8").read().splitlines()
tops = [l for l in bg if l.strip() and not l.strip().startswith("#")][:4]
for t in tops: p("  BG_TOP: " + t[:150])

# 5) production / lock / export age / daily brief today / audits week
p("production=%s" % st.get("production"))
p("index_lock=%s" % os.path.exists(os.path.join(ROOT, ".git", "index.lock")))
ex = json.load(io.open(os.path.join(ROOT, "docs", "status-export.json"), encoding="utf-8"))
ex_ts = ex.get("export_ts", "?")
p("export_ts=%s" % ex_ts)
db = os.path.join(ROOT, "data", "intel", "daily", "2026-10-04.md")
p("daily_brief_1004=%s" % os.path.exists(db))
iso = now.isocalendar()
p("today=%s ISOweek=%d-W%d" % (now.strftime("%m-%d %H:%M"), iso[0], iso[1]))
p("audit_w%d=%s" % (iso[1], os.path.exists(os.path.join(ROOT, "docs", "audits", "%d-W%d-self-audit.md" % (iso[0], iso[1])))))

out = os.path.join(ROOT, ".c3-tmp", "r1189_check.txt")
io.open(out, "w", encoding="utf-8").write("\n".join(lines))
print("WROTE", out, "lines=%d" % len(lines))
