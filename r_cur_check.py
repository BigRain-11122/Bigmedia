# -*- coding: utf-8 -*-
"""Fast-path round check: state fields, daily brief, orders, group ledger scan, decisions watermark diff."""
import json, os, re, glob, io

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP = r"C:\Users\sjs20\Desktop\FluxGroup"
out = io.StringIO()

# 1) state.json fields
with open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
out.write("== state.json ==\n")
for k in ("tick", "ts", "task", "production"):
    out.write(f"{k}: {st.get(k)}\n")
wm = st.get("decisions_watermark", {})
out.write(f"watermark dnums count: {len(wm.get('dnums', [])) if isinstance(wm, dict) else 'n/a'}\n")
if isinstance(wm, dict):
    out.write(f"watermark last: {sorted(wm.get('dnums', []))[-5:]}\n")
logs = st.get("log", [])
out.write(f"log entries: {len(logs)}\n")
for line in logs[-5:]:
    out.write("LOG>> " + line[:400] + "\n")

# 2) daily brief today
today_md = os.path.join(ROOT, "data", "intel", "daily", "2026-10-05.md")
out.write(f"\ndaily 2026-10-05 exists: {os.path.exists(today_md)}\n")

# 3) orders latest
od = os.path.join(ROOT, "orders")
files = sorted(glob.glob(os.path.join(od, "*")), key=os.path.getmtime, reverse=True)
out.write("\norders latest 3:\n")
for p in files[:3]:
    out.write(f"  {os.path.basename(p)}  mtime={os.path.getmtime(p)}\n")

# 4) evolution-ledger @BigStream scan (strict @-prefix)
led = os.path.join(GRP, "cph4", "evolution-ledger.md")
pat = re.compile(r"@(BigStream|七线全司|全司|六司|八线全量)")
hits = []
if os.path.exists(led):
    with open(led, encoding="utf-8", errors="replace") as f:
        for i, ln in enumerate(f, 1):
            if pat.search(ln):
                hits.append((i, ln.rstrip()[:160]))
out.write(f"\nledger @-hits: {len(hits)}\n")
for i, ln in hits[-6:]:
    out.write(f"  L{i}: {ln}\n")

# 5) decisions.md D/C number set diff vs watermark
dec = os.path.join(GRP, "docs", "decisions.md")
cur = set()
if os.path.exists(dec):
    with open(dec, encoding="utf-8", errors="replace") as f:
        txt = f.read()
    cur = set(re.findall(r"[DC]-\d{8}-\d{2}", txt))
old = set(wm.get("dnums", [])) if isinstance(wm, dict) else set()
new = sorted(cur - old)
out.write(f"\ndecisions total {len(cur)} / watermark {len(old)} / NEW: {new}\n")

# 6) orders.md CEO physical-item area quick peek (top of board section)
orders_md = os.path.join(GRP, "docs", "orders.md")
if os.path.exists(orders_md):
    with open(orders_md, encoding="utf-8", errors="replace") as f:
        head = f.read(1500)
    out.write("\norders.md head 400 chars:\n" + head[:400] + "\n")

with open(os.path.join(ROOT, "r_cur_check.txt"), "w", encoding="utf-8") as f:
    f.write(out.getvalue())
print("written")
