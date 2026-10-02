# -*- coding: utf-8 -*-
# R1033 round-start five-check (fast path): orders latest, ledger @rows, decisions watermark diff, daily brief
import os, re, json, glob, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = os.path.join(ROOT, "media", "BigStream")

def mtime(p):
    try:
        return datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "N/A"

print("=== 1. orders/ latest files (BigStream) ===")
od = os.path.join(BS, "orders")
files = [(f, os.path.getmtime(os.path.join(od, f))) for f in os.listdir(od) if os.path.isfile(os.path.join(od, f))]
files.sort(key=lambda x: -x[1])
for f, m in files[:4]:
    print(mtime(os.path.join(od, f)), f)
print("orders file count:", len(files))

print("=== 2. evolution-ledger @rows scan (group repo, read-only) ===")
led = os.path.join(ROOT, "cph4", "evolution-ledger.md")
print("ledger mtime:", mtime(led))
pats = ["@BigStream", "@七线全司", "@全司", "@六司", "@八线全量"]
rows = []
with open(led, encoding="utf-8") as fh:
    for i, line in enumerate(fh, 1):
        if any(p in line for p in pats):
            rows.append((i, line.strip()))
print("total @rows (loose contains):", len(rows))
strict = [(i, l) for (i, l) in rows if re.search(r"@BigStream|@七线全司|@全司|@六司|@八线全量", l)]
print("total @rows (strict prefix-set):", len(strict))
print("--- last 6 strict rows ---")
for i, l in strict[-6:]:
    print(i, l[:200])

print("=== 3. decisions.md dnum watermark diff ===")
dec = os.path.join(ROOT, "docs", "decisions.md")
print("decisions mtime:", mtime(dec))
with open(dec, encoding="utf-8") as fh:
    text = fh.read()
dn = set(re.findall(r"D-\d{8}-\d{2}", text))
cn = set(re.findall(r"C-\d{8}-\d{2}", text))
newset = dn | cn
with open(os.path.join(BS, "src", "os", "state.json"), encoding="utf-8") as fh:
    st = json.load(fh)
wm = set(st.get("decisions_watermark", {}).get("dnums", []))
print("file dnums:", len(newset), "| watermark:", len(wm))
print("NEW (in file, not in watermark):", sorted(newset - wm))
print("GONE (in watermark, not in file):", sorted(wm - newset))

print("=== 4. daily brief today (2026-10-03) ===")
db = os.path.join(BS, "data", "intel", "daily", "2026-10-03.md")
print("2026-10-03 brief:", os.path.exists(db), mtime(db) if os.path.exists(db) else "")

print("=== 5. group orders.md mtime (CEO physical-items area) ===")
go = os.path.join(ROOT, "docs", "orders.md")
print("group orders.md mtime:", mtime(go))

print("=== 6. dispatch board top (decisions.md top 60 lines) ===")
with open(dec, encoding="utf-8") as fh:
    for i, line in enumerate(fh, 1):
        if i > 60: break
        if line.strip():
            print(i, line.strip()[:160])
