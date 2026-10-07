# R1675 quick-path five-checks probe (fresh independent re-run, this body)
# Output kept compact/ASCII-safe for PS 5.1 console.
import os, re, json, datetime

R = r"C:\Users\sjs20\Desktop\FluxGroup"
B = os.path.join(R, "media", "BigStream")

def mt(p):
    try:
        return datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return "ABSENT(%s)" % type(e).__name__

def rd(p, enc="utf-8"):
    try:
        with open(p, "r", encoding=enc, errors="replace") as f:
            return f.read()
    except Exception as e:
        return ""

print("=== R1675 five-checks @", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "===")

# 1) own orders top (latest file by mtime)
od = os.path.join(B, "orders")
files = [(f, os.path.getmtime(os.path.join(od, f))) for f in os.listdir(od) if os.path.isfile(os.path.join(od, f))]
files.sort(key=lambda x: -x[1])
print("own_orders_top:", files[0][0], "| mtime:", datetime.datetime.fromtimestamp(files[0][1]).strftime("%Y-%m-%d %H:%M:%S"))

# 2) group trio mtimes
dec = os.path.join(R, "docs", "decisions.md")
led = os.path.join(R, "cph4", "evolution-ledger.md")
god = os.path.join(R, "docs", "orders.md")
flb = os.path.join(R, "quant", "bigmoney", "fleet", "backlog.md")
print("decisions_mtime:", mt(dec), "(anchor 2026-10-07 12:07:04)")
print("ledger_mtime:", mt(led), "(anchor 2026-10-07 15:12:28)")
print("grp_orders_mtime:", mt(god), "(anchor 2026-10-07 15:13:06)")
print("fleet_backlog_mtime:", mt(flb), "(anchor 2026-10-07 22:33:42)")

# 3) dnum content-addressing diff (decisions vs state watermark)
dtext = rd(dec)
file_dnums = set(re.findall(r"[DC]-\d{8}-\d+", dtext))
st = json.load(open(os.path.join(B, "src", "os", "state.json"), encoding="utf-8"))
wm = set(st.get("decisions_watermark", {}).get("dnums", []))
new = sorted(file_dnums - wm)
pseudo = {"D-20260930-008", "D-20260930-1"}
truly = [d for d in new if d not in pseudo]
print("dnum_file_count:", len(file_dnums), "wm_count:", len(wm))
print("dnum_NEW:", new, "TRULY_NEW:", truly)

# 4) dispatch board (派工通告板) BS/七司 rows
m = re.search(r"派工通告板(.*?)(?=\n## |\n---|\Z)", dtext, re.S)
board_rows = []
if m:
    for ln in m.group(1).splitlines():
        if re.search(r"BigStream|七司|全司", ln) and re.search(r"[DC]-\d{8}", ln):
            board_rows.append(ln.strip()[:60])
print("board_bs_rows:", len(board_rows))

# 5) ledger @BigStream lines (substring scan; anchor L91/L92)
ltext = rd(led)
hits = [(i + 1, ln.strip()[:50]) for i, ln in enumerate(ltext.splitlines()) if "@BigStream" in ln]
print("ledger_atBigStream:", len(hits), [h[0] for h in hits])

# 6) fleet BS row
ftext = rd(flb)
bs = [ln.strip()[:100] for ln in ftext.splitlines() if "bigstream" in ln.lower() or "BigStream" in ln]
print("fleet_BS_row:", bs[:2])

# 7) backlog + queue anchors
bl = os.path.join(B, "src", "os", "backlog.md")
qu = os.path.join(B, "docs", "self-improvement-queue.md")
print("backlog_mtime:", mt(bl), "(anchor 2026-10-07 01:01:13)")
print("queue_mtime:", mt(qu), "(anchor 2026-10-07 00:48:40)")

# 8) daily1007 in case / daily1008 absent
d7 = os.path.join(B, "data", "intel", "daily", "2026-10-07.md")
d8 = os.path.join(B, "data", "intel", "daily", "2026-10-08.md")
print("daily1007:", "IN_CASE" if os.path.exists(d7) else "ABSENT", "| daily1008:", "IN_CASE" if os.path.exists(d8) else "ABSENT")

# 9) GB mtime + day age
gb = os.path.join(B, "docs", "global-benchmarks.md")
gmt = mt(gb)
gbdate = re.search(r"2026-\d{2}-\d{2}", rd(gb)[:4000])
print("gb_mtime:", gmt, "(due 2026-10-08 01:02)")

# 10) pools E30 three buckets
pl = os.path.join(R, "life", "BigLife", "cognition", "pools.json")
ptext = rd(pl)
print("pools_mtime:", mt(pl), "| weekend:", ptext.count("weekend"), "market_open:", ptext.count("market_open"), "market_close:", ptext.count("market_close"))

# 11) production flag + index.lock + export ts
print("production:", st.get("production"))
lock = os.path.join(B, ".git", "index.lock")
print("index_lock:", os.path.exists(lock))
try:
    ex = json.load(open(os.path.join(B, "docs", "status-export.json"), encoding="utf-8"))
    print("export_ts:", ex.get("export_ts", "?"))
except Exception as e:
    print("export_ts: READ_FAIL", type(e).__name__)

# 12) backlog first non-done items (top claimable check)
btext = rd(bl)
open_items = []
for ln in btext.splitlines():
    mm = re.match(r"^(\d+)\.\s", ln)
    if mm and "[done" not in ln:
        open_items.append(int(mm.group(1)))
    if len(open_items) >= 6:
        break
print("backlog_open_top:", open_items)
print("=== end probe ===")
