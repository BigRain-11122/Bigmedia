# -*- coding: utf-8 -*-
"""Fast-path five-check probe for round start. Writes UTF-8 report."""
import json, os, re, glob, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP = r"C:\Users\sjs20\Desktop\FluxGroup"
out = []
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
out.append("NOW: " + now)

st_path = os.path.join(ROOT, "src", "os", "state.json")
with open(st_path, encoding="utf-8") as f:
    st = json.load(f)

out.append("TICK: %s" % st.get("tick"))
out.append("TS: %s" % st.get("ts"))
out.append("TASK: %s" % st.get("task"))
prod = st.get("production")
out.append("PRODUCTION: %s" % prod)
if prod != "open":
    out.append("!! production != open -> self-heal needed (D-BS-06)")

wm = st.get("decisions_watermark", {})
dnums = wm.get("dnums", []) if isinstance(wm, dict) else []
out.append("WM dnums count: %d" % len(dnums))
out.append("WM dnums tail: %s" % (dnums[-15:] if dnums else []))

log = st.get("log", [])
out.append("LOG total: %d" % len(log))
out.append("=== LOG TAIL 4 ===")
for line in log[-4:]:
    out.append(line)
    out.append("---")

# orders latest files
orders_dir = os.path.join(ROOT, "orders")
files = glob.glob(os.path.join(orders_dir, "*"))
files = [p for p in files if os.path.isfile(p)]
files.sort(key=os.path.getmtime, reverse=True)
out.append("=== ORDERS latest 5 (mtime) ===")
for p in files[:5]:
    out.append("%s | %s" % (os.path.basename(p), datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M:%S")))

# group evolution-ledger @BigStream scan
led = os.path.join(GRP, "cph4", "evolution-ledger.md")
hits = []
if os.path.exists(led):
    with open(led, encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            if re.search(r"@BigStream|@七线全司|@全司|@六司|@八线全量", line):
                hits.append((i, line.rstrip()))
out.append("=== LEDGER @-lines total: %d ===" % len(hits))
for i, line in hits[-6:]:
    out.append("L%d: %s" % (i, line[:260]))

# group decisions.md D/C number set diff
dec = os.path.join(GRP, "docs", "decisions.md")
new_nums = []
if os.path.exists(dec):
    with open(dec, encoding="utf-8", errors="replace") as f:
        content = f.read()
    nums = set(re.findall(r"\b([DC]-\d{8}-\d{2})\b", content))
    wmset = set(dnums) if dnums else set()
    new_nums = sorted(nums - wmset)
out.append("=== DECISIONS new D/C (vs watermark): %d ===" % len(new_nums))
out.append("NEW: %s" % new_nums)

# dispatch board top block (派工通告板) - first 40 lines of decisions.md
if os.path.exists(dec):
    with open(dec, encoding="utf-8", errors="replace") as f:
        dl = f.read().splitlines()
    out.append("=== decisions.md HEAD 25 lines ===")
    for line in dl[:25]:
        out.append(line[:200])

# orders.md CEO physical-items zone: just check file exists & mtime
om = os.path.join(GRP, "docs", "orders.md")
if os.path.exists(om):
    out.append("GRP orders.md mtime: %s" % datetime.datetime.fromtimestamp(os.path.getmtime(om)).strftime("%Y-%m-%d %H:%M:%S"))

rep = os.path.join(ROOT, ".r_fastcheck_report.txt")
with open(rep, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("OK report written, lines=%d" % len(out))
