import json, os, re, subprocess, io, sys

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP  = r"C:\Users\sjs20\Desktop\FluxGroup"
OUT  = os.path.join(ROOT, ".c3-tmp", "r1035_scan.txt")

buf = io.StringIO()
def p(*a): print(*a, file=buf, flush=True)

with open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
p("== state ==")
p("tick:", st.get("tick"), "| ts:", st.get("ts"))
p("task:", str(st.get("task"))[:150])
p("production:", st.get("production"))
wm = st.get("decisions_watermark") or {}
dnums = wm.get("dnums", []) if isinstance(wm, dict) else []
p("watermark dnums:", len(dnums))
for line in st.get("log", [])[-3:]:
    p("LOG:", line[:560])

od = os.path.join(ROOT, "orders")
fs = sorted(os.listdir(od), key=lambda x: os.path.getmtime(os.path.join(od, x)))
p("== orders latest 3 ==")
for f in fs[-3:]:
    p("  ", f)

with open(os.path.join(GRP, "cph4", "evolution-ledger.md"), encoding="utf-8", errors="replace") as f:
    led = f.read()
pat = re.compile(r"@BigStream|@七线全司|@全司|@六司|@八线")
hl = [l.strip() for l in led.splitlines() if pat.search(l)]
p("== ledger @hits:", len(hl))
for l in hl[-3:]:
    p("  LED:", l[:170])

with open(os.path.join(GRP, "docs", "decisions.md"), encoding="utf-8", errors="replace") as f:
    dec = f.read()
ids = set(re.findall(r"\b[DC]-\d{8}-\d+\b", dec))
new = sorted(ids - set(dnums))
p("== decisions ids:", len(ids), "| new vs watermark:", new[:25])
lines = dec.splitlines()
bs_lines = [(i, l.strip()) for i, l in enumerate(lines) if "BigStream" in l]
p("== decisions BigStream mentions:", len(bs_lines))
for i, l in bs_lines[-6:]:
    p("  DEC L%d:" % (i + 1), l[:170])
# top dispatch board block
p("== decisions.md head 12 lines ==")
for i, l in enumerate(lines[:12]):
    p("  H%d:" % (i + 1), l[:120])

r = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
p("== git status ==")
p(r.stdout.strip()[:800] or "(clean)")
p("index.lock:", os.path.exists(os.path.join(ROOT, ".git", "index.lock")))

aud = os.path.join(ROOT, "docs", "audits")
p("== audits:", sorted(os.listdir(aud))[-8:] if os.path.isdir(aud) else "N/A")
db = os.path.join(ROOT, "data", "intel", "daily")
p("== daily briefs:", sorted(os.listdir(db))[-4:] if os.path.isdir(db) else "N/A")
gbp = os.path.join(ROOT, "docs", "global-benchmarks.md")
if os.path.exists(gbp):
    gbt = open(gbp, encoding="utf-8", errors="replace").read()
    ds = re.findall(r"2026-\d{2}-\d{2}", gbt)
    p("== global-benchmarks dates(head12):", ds[:12])
rd = os.path.join(ROOT, "docs", "research")
p("== research files:", len(os.listdir(rd)))
p("== monthly-stat notes:", [f for f in os.listdir(rd) if "月度统计" in f])
qp = os.path.join(ROOT, "docs", "self-improvement-queue.md")
p("== queue exists:", os.path.exists(qp))
se = os.path.join(ROOT, "docs", "status-export.json")
if os.path.exists(se):
    sej = json.load(open(se, encoding="utf-8"))
    p("== export_ts:", sej.get("export_ts"))
    p("== export keys:", list(sej.keys()))

with open(OUT, "w", encoding="utf-8") as f:
    f.write(buf.getvalue())
print("written", OUT)
