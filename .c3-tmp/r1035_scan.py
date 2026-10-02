import json, os, re, subprocess

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP  = r"C:\Users\sjs20\Desktop\FluxGroup"
OUT = os.path.join(ROOT, "r1035_scan.txt")
L = []
def w(s=""): L.append(str(s))

# 1) state.json top fields + log tail
with open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
w("== state ==")
w("tick=%s ts=%s" % (st.get("tick"), st.get("ts")))
w("task=%s" % st.get("task"))
w("production=%s" % st.get("production"))
log = st.get("log", [])
w("log_len=%d" % len(log))
w("== log tail 3 ==")
for r in log[-3:]:
    w(r[:700]); w("---")

wm = st.get("decisions_watermark")
w("watermark_type=%s" % type(wm).__name__)
if isinstance(wm, dict):
    for k, v in wm.items():
        if isinstance(v, list):
            w("wm %s=list len %d last8=%s" % (k, len(v), v[-8:]))
        else:
            w("wm %s=%s" % (k, v))
else:
    w("watermark=%s" % wm)

# 2) orders dir latest
od = os.path.join(ROOT, "orders")
fs = sorted(x for x in os.listdir(od) if not x.startswith("."))
w("== orders latest 6 ==")
for x in fs[-6:]:
    w(x)

# 3) git status
r = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
w("== git status ==")
w((r.stdout.strip() or "(clean)")[:1500])
w("stderr=%s" % r.stderr.strip()[:300])

# 4) evolution-ledger strict @BigStream scan
lgr = os.path.join(GRP, "cph4", "evolution-ledger.md")
cnt = 0; tail = []
with open(lgr, encoding="utf-8") as f:
    for line in f:
        if "@BigStream" in line:
            cnt += 1
            tail.append(line.strip()[:200])
w("ledger @BigStream rows=%d" % cnt)
w("== ledger last 2 @BigStream rows ==")
for t in tail[-2:]:
    w(t)

# 5) decisions.md dnum set diff vs watermark
dec = os.path.join(GRP, "docs", "decisions.md")
with open(dec, encoding="utf-8") as f:
    dtext = f.read()
dnums = set(re.findall(r"[DC]-\d{8}-\d{2}", dtext))
cur = set()
if isinstance(wm, dict):
    cur = set(wm.get("dnums", []) or [])
missing = sorted(dnums - cur)
w("decisions unique dnums=%d watermark=%d" % (len(dnums), len(cur)))
w("missing_vs_watermark=%s" % (missing if missing else "NONE"))

# 6) dispatch board head (top 40 lines of decisions.md)
w("== decisions.md head 40 ==")
for line in dtext.splitlines()[:40]:
    w(line[:160])

# 7) routine items
w("== routine ==")
p_daily = os.path.join(ROOT, "data", "intel", "daily", "2026-10-03.md")
w("daily 2026-10-03 exists=%s" % os.path.exists(p_daily))
ad = os.path.join(ROOT, "docs", "audits")
au = sorted(x for x in os.listdir(ad)) if os.path.isdir(ad) else []
w("audits last 5=%s" % au[-5:])
gb = os.path.join(ROOT, "docs", "global-benchmarks.md")
if os.path.exists(gb):
    with open(gb, encoding="utf-8") as f:
        gt = f.read()
    m = re.search(r"## .{0,3}4", gt)
    seg = gt[m.start():m.start()+1200] if m else ""
    dates = re.findall(r"2026-\d{2}-\d{2}", seg)
    w("global-benchmarks sec4 first dates=%s" % dates[:3])
else:
    w("global-benchmarks missing")

# 8) index.lock check
w("index.lock exists=%s" % os.path.exists(os.path.join(ROOT, ".git", "index.lock")))

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L))
print("SCAN OK rows=%d" % len(L))
