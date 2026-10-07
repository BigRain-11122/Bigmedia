# R1669 five-check probe (ASCII output): group trio + backlog #99 + export ts
import json, re, os, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
LEDGER = os.path.join(ROOT, "cph4", "evolution-ledger.md")
DEC = os.path.join(ROOT, "docs", "decisions.md")
ORDERS_HQ = os.path.join(ROOT, "docs", "orders.md")

def mt(p):
    try:
        return datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return "ERR " + str(e)

print("== mtimes ==")
for p in (LEDGER, DEC, ORDERS_HQ):
    print(os.path.basename(p), mt(p))

# 1) ledger @BigStream strict-prefix scan
hits = []
try:
    with open(LEDGER, encoding="utf-8") as f:
        for i, ln in enumerate(f, 1):
            if re.match(r"^\s*[^@]*@BigStream(?![A-Za-z])", ln) and ("@" in ln):
                hits.append((i, ln.strip()[:120]))
except Exception as e:
    print("ledger read err", e)
print("== ledger @BigStream lines ==", len(hits))
for i, t in hits[-5:]:
    print("L%d %s" % (i, t))

# 2) decisions dnum set diff
dn = set()
try:
    with open(DEC, encoding="utf-8") as f:
        txt = f.read()
    dn = set(re.findall(r"\b[DC]-\d{8}-\d{2}\b", txt))
except Exception as e:
    print("dec read err", e)
with open("src/os/state.json", encoding="utf-8") as f:
    st = json.load(f)
wm = set(st.get("decisions_watermark", {}).get("dnums", []))
new = sorted(dn - wm)
print("== decisions dnums: file=%d wm=%d NEW=%d ==" % (len(dn), len(wm), len(new)))
print("NEW:", new if len(new) <= 20 else new[:20])

# 3) export freshness
try:
    with open("docs/status-export.json", encoding="utf-8") as f:
        ex = json.load(f)
    print("== export export_ts =", ex.get("export_ts"), "now=", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
except Exception as e:
    print("export read err", e)

# 4) backlog top open items + #99
try:
    with open("src/os/backlog.md", encoding="utf-8") as f:
        bl = f.read()
    m = re.findall(r"(?m)^(\d+)\. (?!\[done)", bl)
    print("== backlog open-numbered items (first 10):", m[:10])
    i = bl.find("99.")
    print("== #99 excerpt ==")
    print(bl[i:i+600] if i >= 0 else "not found")
except Exception as e:
    print("backlog err", e)
