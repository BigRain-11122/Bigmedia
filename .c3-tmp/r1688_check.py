# -*- coding: utf-8 -*-
"""R1688 five-check probe (fresh body, independent rerun)."""
import os, re, subprocess, datetime

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = lambda *p: os.path.join(root, *p)
def mt(p):
    try: return datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M:%S")
    except OSError: return "ABSENT"

print("=== own orders top ===")
od = F("orders")
for n in sorted(os.listdir(od), reverse=True)[:3]:
    print(n, mt(os.path.join(od, n)))

print("=== decisions/ledger/group-orders/fleet mtimes ===")
g = lambda *p: F("..", "..", "docs", *p) if False else os.path.join(root, "..", "..", *p)
grp = os.path.abspath(os.path.join(root, "..", ".."))
for p in ["docs\\decisions.md", "cph4\\evolution-ledger.md", "docs\\orders.md",
          "cph4\\fleet\\backlog.md"]:
    print(p, mt(os.path.join(grp, p)))

print("=== decisions dnum set diff vs watermark ===")
try:
    import json
    st = json.load(open(F("src", "os", "state.json"), encoding="utf-8"))
    wm = set(st["decisions_watermark"]["dnums"])
    print("watermark size", len(wm))
    txt = open(os.path.join(grp, "docs", "decisions.md"), encoding="utf-8", errors="ignore").read()
    cur = set(re.findall(r"[DC]-\d{8}-\d{1,3}", txt))
    trul = cur - wm
    print("current size", len(cur), "TRULY_NEW:", sorted(trul) if trul else "[]")
except Exception as e:
    print("ERR", e)

print("=== ledger @BigStream lines ===")
led = os.path.join(grp, "cph4", "evolution-ledger.md")
txt = open(led, encoding="utf-8", errors="ignore").read()
hits = [l.strip()[:120] for l in txt.splitlines() if "@BigStream" in l]
print("count", len(hits))
for h in hits[-4:]:
    print(h)

print("=== index.lock / state ts / daily ===")
print("index.lock", os.path.exists(os.path.join(root, ".git", "index.lock")))
print("daily1008", mt(F("data", "intel", "daily", "2026-10-08.md")))
print("daily1007", mt(F("data", "intel", "daily", "2026-10-07.md")))
print("W42 audit", mt(F("docs", "audits", "2026-W42-self-audit.md")))
print("now", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
