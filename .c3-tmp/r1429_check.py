import json, re, io, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
G = r"C:\Users\sjs20\Desktop\FluxGroup"
OUTP = os.path.join(ROOT, ".c3-tmp", "r1421_check_out.txt")

out = io.open(OUTP, "w", encoding="utf-8")
def w(s):
    try:
        out.write(s + "\n")
    except Exception:
        out.write(repr(s) + "\n")

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
    w("watermark_note=%s" % wm.get("note", ""))
else:
    dnums = set(wm if isinstance(wm, list) else [])
w("watermark dnums count=%d" % len(dnums))
w("watermark dnums last=%s" % ",".join(sorted(dnums)[-25:]))
log = st.get("log", [])
w("log count=%d" % len(log))
for entry in log[-6:]:
    if isinstance(entry, dict):
        w("LOG| " + json.dumps(entry, ensure_ascii=False)[:260])
    else:
        w("LOG| " + str(entry)[:260])

# 2) group decisions.md scan (content addressing)
dec = io.open(os.path.join(G, "docs", "decisions.md"), encoding="utf-8").read()
ds = set(re.findall(r"[DC]-\d{8}-\d{2}", dec))
new = sorted(ds - dnums)
w("== decisions.md ==")
w("total D/C tokens=%d new_vs_watermark=%d" % (len(ds), len(new)))
w("new_tokens=%s" % ",".join(new))
lines = dec.splitlines()
hits = [(i + 1, l) for i, l in enumerate(lines) if ("BigStream" in l or "七司" in l or "全司" in l)]
w("bigstream/7si lines total=%d last8:" % len(hits))
for i, l in hits[-8:]:
    w("DEC L%d| %s" % (i, l[:200]))

# 3) evolution-ledger @BigStream-family scan
led = io.open(os.path.join(G, "cph4", "evolution-ledger.md"), encoding="utf-8").read()
llines = led.splitlines()
pat = re.compile(r"@BigStream|@七线全司|@全司|@六司|@八线全量")
hits2 = [(i + 1, l) for i, l in enumerate(llines) if pat.search(l)]
w("== evolution-ledger ==")
w("at-family lines total=%d last6:" % len(hits2))
for i, l in hits2[-6:]:
    w("LED L%d| %s" % (i, l[:220]))
pnums = set(re.findall(r"P-\d{4}-\d{2}-\d{2}-\d{2}", led))
w("ledger P-tokens count=%d last6=%s" % (len(pnums), ",".join(sorted(pnums)[-6:])))

# 4) group orders.md physical-件 region
o = io.open(os.path.join(G, "docs", "orders.md"), encoding="utf-8").read()
olines = o.splitlines()
w("== orders.md chars=%d ==" % len(o))
acct = [(i + 1, l) for i, l in enumerate(olines) if ("物理件" in l or ("账号" in l and i < 60))]
w("physical-lines last6:")
for i, l in acct[-6:]:
    w("ORD L%d| %s" % (i, l[:160]))

out.close()
print("done -> " + OUTP)
