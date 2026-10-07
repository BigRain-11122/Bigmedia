# -*- coding: utf-8 -*-
"""R1689 fast-path five-check probe (one-off, ASCII output only)."""
import json, re, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = os.path.join(ROOT, "media", "BigStream")

def mtime(p):
    try:
        import datetime
        return datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return "ERR " + str(e)

# 1. decisions.md dnum content-addressing diff vs state watermark
state = json.load(open(os.path.join(BS, "src", "os", "state.json"), encoding="utf-8"))
wm = set(state["decisions_watermark"]["dnums"])
dec_path = os.path.join(ROOT, "docs", "decisions.md")
dec_txt = open(dec_path, encoding="utf-8").read()
file_dnums = set(re.findall(r"[DC]-\d{8}-\d{2}", dec_txt))
PSEUDO = {"D-20260930-008", "D-20260930-1"}
new = sorted((file_dnums - wm) - PSEUDO)
gone = len(wm - file_dnums)
print("decisions mtime:", mtime(dec_path), "file_dnums:", len(file_dnums), "wm:", len(wm))
print("TRULY_NEW:", new if new else "[]")
print("GONE_from_file:", gone)

# 2. ledger @BigStream four-mode strict-prefix scan
led_path = os.path.join(ROOT, "cph4", "evolution-ledger.md")
led_txt = open(led_path, encoding="utf-8").read()
lines = led_txt.splitlines()
hits = []
for i, ln in enumerate(lines, 1):
    if re.search(r"@(BigStream|七线全司|全司|六司)", ln):
        hits.append((i, ln.strip()[:120]))
print("ledger mtime:", mtime(led_path), "four-mode hit lines:", len(hits))
for i, ln in hits[-6:]:
    print("  L%d: %s" % (i, ln))

# 3. group orders mtime + CEO todo-area BS rows
gorders = os.path.join(ROOT, "docs", "orders.md")
print("group orders mtime:", mtime(gorders))
go_txt = open(gorders, encoding="utf-8").read()
bs_rows = [ln.strip()[:100] for ln in go_txt.splitlines() if "BigStream" in ln]
print("group orders BigStream rows:", len(bs_rows))
for r in bs_rows[-3:]:
    print("  ", r)

# 4. daily1008 + weekly audit presence
p = os.path.join(BS, "data", "intel", "daily", "2026-10-08.md")
print("daily1008 exists:", os.path.exists(p), mtime(p) if os.path.exists(p) else "")

# 5. production flag + index.lock
print("production:", state.get("production"), "| index.lock:", os.path.exists(os.path.join(BS, ".git", "index.lock")))
print("tick:", state.get("tick"), "| ts:", state.get("ts"))
