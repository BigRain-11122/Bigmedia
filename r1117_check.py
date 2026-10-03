import json, re, os, io, datetime

OUT = []
root = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
hq = r"C:\Users\sjs20\Desktop\FluxGroup"

def rd(p):
    with io.open(p, encoding="utf-8", errors="replace") as f:
        return f.read()

# 1) state.json key fields + log tail
st = json.loads(rd(os.path.join(root, "src", "os", "state.json")))
OUT.append("== state ==")
for k in ("tick", "ts", "task", "production"):
    OUT.append("%s: %s" % (k, st.get(k)))
wm = st.get("decisions_watermark") or {}
dn = wm.get("dnums") if isinstance(wm, dict) else None
if dn is None:
    dn = wm.get("known") or []
OUT.append("watermark dnums: %d tail=%s" % (len(dn), list(dn)[-6:]))
logs = st.get("log") or []
OUT.append("log entries: %d (order probe first/last heads):" % len(logs))
OUT.append("  first: " % () + (logs[0][:80] if logs else ""))
OUT.append("  last : " % () + (logs[-1][:80] if logs else ""))
for e in logs[-3:]:
    s = e if isinstance(e, str) else json.dumps(e, ensure_ascii=False)
    OUT.append("LOGTAIL>> " + s[:500])
    OUT.append("")

# 2) orders latest files
odir = os.path.join(root, "orders")
files = sorted((os.path.getmtime(os.path.join(odir, f)), f) for f in os.listdir(odir) if not f.startswith("."))
OUT.append("== orders latest 3 ==")
for mt, f in files[-3:]:
    OUT.append("%s  %s" % (datetime.datetime.fromtimestamp(mt).strftime("%m-%d %H:%M"), f))

# 3) group evolution-ledger scan for company tags
lp = os.path.join(hq, "cph4", "evolution-ledger.md")
OUT.append("== ledger tagged lines (last 6) ==")
if os.path.exists(lp):
    lines = rd(lp).split("\n")
    hits = []
    for i, ln in enumerate(lines, 1):
        if re.search(r"@(BigStream|Biggame|BigMoney|BigLife|BigDomain|BigCompute|FluxVerse|CPH4|七线全司|全司|六司|八线全量)", ln):
            hits.append((i, ln.strip()))
    OUT.append("tagged hit count: %d" % len(hits))
    for i, ln in hits[-6:]:
        OUT.append("L%d: %s" % (i, ln[:260]))
else:
    OUT.append("ledger missing")

# 4) group decisions dnum diff vs watermark
dp = os.path.join(hq, "docs", "decisions.md")
OUT.append("== decisions dnum diff ==")
if os.path.exists(dp):
    dc = rd(dp)
    fileset = set(re.findall(r"[DC]-\d{8}-\d{2}", dc))
    known = set(dn or [])
    OUT.append("file dnums: %d watermark: %d" % (len(fileset), len(known)))
    OUT.append("NEW vs watermark: %s" % sorted(fileset - known))
    OUT.append("in-watermark-gone: %s" % sorted(known - fileset)[:8])
    # dispatch board head (first 8 non-empty lines)
    head = [l for l in dc.split("\n") if l.strip()][:8]
    for l in head:
        OUT.append("HEAD| " + l[:180])
else:
    OUT.append("decisions.md missing")

# 5) routine file checks
OUT.append("== routine ==")
d10 = os.path.join(root, "data", "intel", "daily", "2026-10-03.md")
OUT.append("daily 10-03 exists: %s" % os.path.exists(d10))
for wk in ("2026-W40-self-audit.md", "2026-W39-self-audit.md"):
    OUT.append("%s exists: %s" % (wk, os.path.exists(os.path.join(root, "docs", "audits", wk))))
gb = os.path.join(root, "docs", "global-benchmarks.md")
if os.path.exists(gb):
    g1 = [l for l in rd(gb).split("\n")[:40] if "2026-" in l][:2]
    OUT.append("benchmarks head lines: %s" % [x[:80] for x in g1])
# CENSUS anchor C-00030 check
a30 = os.path.join(hq, "life", "BigLife", "census", "anchors", "C-00030.md")
OUT.append("anchor C-00030 exists: %s" % os.path.exists(a30))
an = os.path.join(hq, "life", "BigLife", "census", "anchors")
if os.path.isdir(an):
    last = sorted(os.listdir(an))[-3:]
    OUT.append("anchors tail: %s" % last)

with io.open(os.path.join(root, "r1098_check.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("done")
