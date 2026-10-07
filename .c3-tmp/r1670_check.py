# R1670 five-check probe (ASCII output): group trio + own orders + dailies + anchors
import json, re, os, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
LEDGER = os.path.join(ROOT, "cph4", "evolution-ledger.md")
DEC = os.path.join(ROOT, "docs", "decisions.md")
ORDERS_HQ = os.path.join(ROOT, "docs", "orders.md")
FLEET_BL = os.path.join(ROOT, "quant", "bigmoney", "fleet", "backlog.md")
OWN_ORDERS = "orders"
DAILY = "data/intel/daily"
GB = "docs/global-benchmarks.md"
W41 = "docs/audits/2026-W41-self-audit.md"

def mt(p):
    try:
        return datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return "ERR " + str(e)

print("== mtimes ==")
for p in (LEDGER, DEC, ORDERS_HQ, FLEET_BL, GB):
    print(os.path.basename(p), mt(p))
print("backlog.md", mt("src/os/backlog.md"))
print("queue", mt("docs/self-improvement-queue.md"))

# own orders top file
try:
    fs = [(mt(os.path.join(OWN_ORDERS, n)), n) for n in os.listdir(OWN_ORDERS) if n.endswith(".md")]
    fs.sort(reverse=True)
    print("== own orders top3 ==")
    for t, n in fs[:3]:
        print(t, n)
except Exception as e:
    print("own orders err", e)

# dailies
print("== dailies ==")
for d in ("2026-10-07.md", "2026-10-08.md"):
    print(d, os.path.exists(os.path.join(DAILY, d)))
print("W41 audit exists:", os.path.exists(W41))

# 1) ledger @BigStream strict-prefix scan
hits = []
try:
    with open(LEDGER, encoding="utf-8") as f:
        for i, ln in enumerate(f, 1):
            if re.match(r"^\s*[^@]*@BigStream(?![A-Za-z])", ln) and ("@" in ln):
                hits.append((i, ln.strip()[:110]))
except Exception as e:
    print("ledger read err", e)
print("== ledger @BigStream lines ==", len(hits))
for i, t in hits[-3:]:
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
gone = len(wm - dn)
print("== decisions dnums: file=%d wm=%d GONE=%d NEW=%d ==" % (len(dn), len(wm), gone, len(new)))
print("NEW:", new)

# 3) fleet backlog BS rows (waiting object, mtime + line count only)
try:
    with open(FLEET_BL, encoding="utf-8") as f:
        fl = f.read()
    rows = [ln.strip()[:110] for ln in fl.splitlines() if "bigstream" in ln.lower()]
    print("== fleet backlog BS rows ==", len(rows))
    for r in rows[:3]:
        print(r)
except Exception as e:
    print("fleet backlog err", e)

# 4) export freshness
try:
    with open("docs/status-export.json", encoding="utf-8") as f:
        ex = json.load(f)
    print("== export export_ts =", ex.get("export_ts"), "now=", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
except Exception as e:
    print("export read err", e)

# 5) backlog top open items
try:
    with open("src/os/backlog.md", encoding="utf-8") as f:
        bl = f.read()
    m = re.findall(r"(?m)^(\d+)\. (?!\[done)", bl)
    print("== backlog open-numbered items (first 8):", m[:8])
except Exception as e:
    print("backlog err", e)

# production state recheck
print("production:", st.get("production"))
