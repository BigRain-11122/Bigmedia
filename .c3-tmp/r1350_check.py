import json, re, io, sys, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GROUP = r"C:\Users\sjs20\Desktop\FluxGroup"
out = io.StringIO()

def w(s=""):
    out.write(str(s) + "\n")

# 1) state.json essentials
with open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
w("== state.json ==")
w("tick=%s" % st.get("tick"))
w("ts=%s" % st.get("ts"))
w("task=%s" % st.get("task"))
w("production=%s" % st.get("production"))
wm = st.get("decisions_watermark") or {}
w("watermark.dnums=%s" % json.dumps(wm.get("dnums", wm), ensure_ascii=True))
log = st.get("log", [])
w("log_len=%d" % len(log))
for e in log[-5:]:
    w("LOG| " + json.dumps(e, ensure_ascii=True))

# 2) group decisions.md content-addressed scan
try:
    with open(os.path.join(GROUP, "docs", "decisions.md"), encoding="utf-8") as f:
        dtext = f.read()
    dnums = sorted(set(re.findall(r"[DC]-\d{8}-\d{2}", dtext)))
    w("== decisions.md ==")
    w("dnum_count=%d" % len(dnums))
    w("dnums=%s" % ",".join(dnums))
    w("-- head 22 lines --")
    for i, ln in enumerate(dtext.splitlines()[:22]):
        w("D%02d| %s" % (i, ln))
except Exception as ex:
    w("decisions.md ERROR %r" % ex)

# 3) evolution-ledger @BigStream scan
try:
    lp = os.path.join(GROUP, "cph4", "evolution-ledger.md")
    with open(lp, encoding="utf-8") as f:
        llines = f.readlines()
    w("== evolution-ledger ==")
    w("total_lines=%d" % len(llines))
    hits = [(i + 1, ln.rstrip()) for i, ln in enumerate(llines)
            if re.search(r"@BigStream|@Bigstream|@七线全司|@全司|@六司", ln)]
    w("hit_count=%d" % len(hits))
    for i, ln in hits[-10:]:
        w("L%d| %s" % (i, ln))
except Exception as ex:
    w("ledger ERROR %r" % ex)

# 4) group orders.md CEO physical items
try:
    with open(os.path.join(GROUP, "docs", "orders.md"), encoding="utf-8") as f:
        otext = f.read()
    w("== orders.md phys ==")
    olines = otext.splitlines()
    w("total_lines=%d" % len(olines))
    for i, ln in enumerate(olines):
        if re.search(r"账号|商户|服务器|物理件", ln):
            w("O%03d| %s" % (i, ln.strip()[:160]))
except Exception as ex:
    w("orders.md ERROR %r" % ex)

with open(os.path.join(ROOT, ".c3-tmp", "r1350_check.txt"), "w", encoding="utf-8") as f:
    f.write(out.getvalue())
print("written r1350_check.txt")
