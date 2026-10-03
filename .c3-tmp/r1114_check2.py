import re, os, glob

base = r"C:\Users\sjs20\Desktop\FluxGroup"
bm = base + r"\media\BigStream"

# 1) strict @-mention scan on group ledger (baseline = 41 rows frozen)
led = open(base + r"\cph4\evolution-ledger.md", encoding="utf-8").read().splitlines()
strict_terms = ["@BigStream", "@七线全司", "@全司", "@六司", "@八线全量", "@八线"]
rows = []
for i, ln in enumerate(led, 1):
    if any(t in ln for t in strict_terms):
        rows.append(i)
print("ledger_strict_rows", len(rows), "last_row_lines", rows[-3:] if rows else [])
# show the last 2 strict rows briefly (ascii-safe)
for i in rows[-2:]:
    print("  L%d:" % i, led[i-1][:120].encode("ascii", "replace").decode())

# 2) orders dir top file
od = sorted(glob.glob(bm + r"\orders\*.md"), key=os.path.getmtime)
print("orders_latest", [os.path.basename(f) for f in od[-3:]])

# 3) group orders.md CEO pending-physical section quick check (top 12 lines of file)
gp = base + r"\docs\orders.md"
if os.path.exists(gp):
    g = open(gp, encoding="utf-8").read()
    print("group_orders_size", len(g))
    # only count new P- lines vs state anchor O-20260928-1910 not needed; just show newest P numbers
    pn = re.findall(r"P-\d{8}-\d{2}", g)
    print("group_P_numbers_last5", pn[-5:] if pn else [])
else:
    print("group_orders_missing")
