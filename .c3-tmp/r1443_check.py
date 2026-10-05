import json, re, io, os
from datetime import datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
G = r"C:\Users\sjs20\Desktop\FluxGroup"
OUTP = os.path.join(ROOT, ".c3-tmp", "r1443_check_out.txt")

out = io.open(OUTP, "w", encoding="utf-8")
def w(s):
    try:
        out.write(s + "\n")
    except Exception:
        out.write(repr(s) + "\n")

w("now=%s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# 1) state.json summary
st = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
w("== state.json ==")
w("tick=%s" % st.get("tick"))
w("ts=%s" % st.get("ts"))
w("task=%s" % st.get("task"))
w("production=%s" % st.get("production"))
wm = st.get("decisions_watermark", {})
if isinstance(wm, dict):
    dnums = set(wm.get("dnums", []))
else:
    dnums = set(wm if isinstance(wm, list) else [])
w("watermark dnums count=%d" % len(dnums))
log = st.get("log", [])
w("log count=%d" % len(log))
for entry in log[-3:]:
    w(("LOG| " + (str(entry) if not isinstance(entry, dict) else json.dumps(entry, ensure_ascii=False)))[:280])

# 2) group decisions.md scan (content addressing, canonical \d{2})
dec = io.open(os.path.join(G, "docs", "decisions.md"), encoding="utf-8").read()
ds = set(re.findall(r"[DC]-\d{8}-\d{2}", dec))
new = sorted(ds - dnums)
gone = sorted(dnums - ds)
w("== decisions.md ==")
w("decisions mtime=%s" % datetime.fromtimestamp(os.path.getmtime(os.path.join(G, "docs", "decisions.md"))).strftime("%Y-%m-%d %H:%M:%S"))
w("total D/C tokens=%d new_vs_watermark=%d gone=%d" % (len(ds), len(new), len(gone)))
w("new_tokens=%s" % ",".join(new))

# 3) evolution-ledger @BigStream-family scan (five modes) + mtime adjudication
ledp = os.path.join(G, "cph4", "evolution-ledger.md")
led = io.open(ledp, encoding="utf-8").read()
llines = led.splitlines()
pat = re.compile(r"@BigStream|@七线全司|@全司|@六司|@八线全量")
hits2 = [(i + 1, l) for i, l in enumerate(llines) if pat.search(l)]
w("== evolution-ledger ==")
w("ledger mtime=%s total_lines=%d" % (datetime.fromtimestamp(os.path.getmtime(ledp)).strftime("%Y-%m-%d %H:%M:%S"), len(llines)))
w("at-family lines total=%d last_at_line=%s" % (len(hits2), hits2[-1][0] if hits2 else "none"))
w("-- tail rows after last @-family line (adjudication: zero BS-actionable) --")
if hits2:
    for i, l in enumerate(llines[hits2[-1][0]:], start=hits2[-1][0] + 1):
        if l.strip():
            w("LED-TAIL L%d| %s" % (i, l[:170]))

# 4) local orders dir freshness (latest file + mtime)
odir = os.path.join(ROOT, "orders")
ents = []
for f in os.listdir(odir):
    p = os.path.join(odir, f)
    ents.append((os.path.getmtime(p), f))
ents.sort(reverse=True)
w("== local orders latest3 ==")
for mt, f in ents[:3]:
    w("ORD-LOCAL %s mtime=%s" % (f, datetime.fromtimestamp(mt).strftime("%Y-%m-%d %H:%M")))

# 5) supply gates quick fresh checks
anc = os.path.join(G, "life", "BigLife", "census", "anchors", "C-00030.md")
w("== supply ==")
w("C-00030 anchor exists=%s" % os.path.exists(anc))
anc31 = os.path.join(G, "life", "BigLife", "census", "anchors", "C-00031.md")
w("C-00031 anchor exists=%s" % os.path.exists(anc31))
oh5 = os.path.join(G, "cph4", "oss-harvest", "OH-20261008-bigstream.md")
w("OH-20261008 (OSS w5) exists=%s" % os.path.exists(oh5))
daily = os.path.join(ROOT, "data", "intel", "daily", "2026-10-06.md")
w("daily1006 exists=%s" % os.path.exists(daily))
daily7 = os.path.join(ROOT, "data", "intel", "daily", "2026-10-07.md")
w("daily1007 exists=%s" % os.path.exists(daily7))
pools = os.path.join(G, "life", "BigLife", "cognition", "pools.json")
if os.path.exists(pools):
    try:
        pj = json.load(io.open(pools, encoding="utf-8"))
        def cnt(x):
            if isinstance(x, dict):
                return sum(cnt(v) for v in x.values())
            if isinstance(x, list):
                return len(x)
            return 0
        w("pools TOTAL_LINES=%d" % cnt(pj))
    except Exception as e:
        w("pools parse EXC %s" % str(e)[:120])

# 6) export freshness
exp = os.path.join(ROOT, "docs", "status-export.json")
if os.path.exists(exp):
    ej = json.load(io.open(exp, encoding="utf-8"))
    w("== export ==")
    w("export_ts=%s" % ej.get("export_ts"))
else:
    w("== export MISSING ==")

out.close()
print("done -> " + OUTP)
