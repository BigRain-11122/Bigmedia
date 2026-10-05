# -*- coding: utf-8 -*-
"""R1450 fast-path five-check probe -> r1450_check_out.txt (clone of R1448 caliber)."""
import io, json, os, re, subprocess, glob

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
HQ = r"C:\Users\sjs20\Desktop\FluxGroup"
OUT = os.path.join(ROOT, ".c3-tmp", "r1450_check_out.txt")
lines = []
def w(s):
    lines.append(s)

# 1) state.json top fields + log tail
with io.open(os.path.join(ROOT, "src", "os", "state.json"), "r", encoding="utf-8") as f:
    st = json.load(f)
w("=== state.json top ===")
for k in ("tick", "ts", "task", "production"):
    if k in st:
        w("%s: %s" % (k, st[k]))
wm = st.get("decisions_watermark", {})
dnums = wm.get("dnums", []) if isinstance(wm, dict) else []
w("watermark dnums count: %d | ts: %s" % (len(dnums), wm.get("ts", "?")))
log = st.get("log", [])
w("log count: %d" % len(log))
w("=== log tail 2 ===")
for entry in log[-2:]:
    w(entry[:300])
    w("---")

# 2) group decisions.md D/C numbers (content-addressed, canonical \d{2})
dec_path = os.path.join(HQ, "docs", "decisions.md")
with io.open(dec_path, "r", encoding="utf-8") as f:
    dec_txt = f.read()
dnums_file = set(re.findall(r"D-\d{8}-\d{2}", dec_txt))
cnums_file = set(re.findall(r"C-\d{8}-\d{2}", dec_txt))
wset = set(dnums) if dnums else set()
new_d = dnums_file - wset
new_c = cnums_file - wset
gone = wset - dnums_file - cnums_file
w("=== group decisions.md ===")
w("mtime: %s" % __import__("datetime").datetime.fromtimestamp(os.path.getmtime(dec_path)).strftime("%Y-%m-%d %H:%M:%S"))
w("D set: %d | C set: %d" % (len(dnums_file), len(cnums_file)))
w("new D vs watermark: %s" % (sorted(new_d) if new_d else "NONE"))
w("new C vs watermark: %s" % (sorted(new_c) if new_c else "NONE"))
w("gone from watermark: %s" % (sorted(gone) if gone else "NONE"))

# 2b) dispatch board (派工通告板 block) BigStream rows
board_rows = []
m = re.search(r"派工通告板(.*?)(?:\n# |\Z)", dec_txt, re.S)
if m:
    for ln in m.group(1).splitlines():
        if "BigStream" in ln and ln.strip():
            board_rows.append(ln.strip()[:200])
w("dispatch board rows total: %d" % len(board_rows))
for r in board_rows[-3:]:
    w("BS row: %s" % r)

# 3) evolution-ledger @BigStream scan (strict @ prefix, five modes, case-insensitive)
led_path = os.path.join(HQ, "cph4", "evolution-ledger.md")
with io.open(led_path, "r", encoding="utf-8") as f:
    led_txt = f.read()
pat = re.compile(r"@[Bb]ig[Ss]tream|@七线全司|@全司|@六司|@八线全量")
hits = []
for i, ln in enumerate(led_txt.splitlines(), 1):
    if pat.search(ln):
        hits.append((i, ln.strip()))
w("=== evolution-ledger scan ===")
w("total @lines: %d | mtime: %s" % (len(hits), __import__("datetime").datetime.fromtimestamp(os.path.getmtime(led_path)).strftime("%Y-%m-%d %H:%M:%S")))
for i, ln in hits[-4:]:
    w("L%d: %s" % (i, ln[:260]))

# 4) gates: daily brief today/tomorrow, orders latest, GB gate, OH w5, supply gates, export freshness
today = "2026-10-06"
w("=== gates ===")
w("daily brief %s exists: %s" % (today, os.path.exists(os.path.join(ROOT, "data", "intel", "daily", today + ".md"))))
w("daily brief 2026-10-07 exists: %s" % os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-10-07.md")))
orders = sorted(glob.glob(os.path.join(ROOT, "orders", "*.md")), key=os.path.getmtime)
w("orders latest: %s" % [os.path.basename(p) for p in orders[-2:]])
gb = os.path.join(ROOT, "docs", "global-benchmarks.md")
with io.open(gb, "r", encoding="utf-8") as f:
    gb_txt = f.read()
m = re.search(r"(\d{4}-\d{2}-\d{2})", gb_txt[:2000])
w("global-benchmarks first date: %s (gate <=7d, next ~10-08)" % (m.group(1) if m else "?"))
w("OH-20261008 built: %s (OSS w5 opens 10-08 21:40)" % os.path.exists(os.path.join(HQ, "cph4", "oss-harvest", "OH-20261008-bigstream.md")))
# CENSUS anchors supply gate (cross-repo read-only)
census = os.path.join(HQ, "life", "BigLife", "census", "anchors")
if os.path.isdir(census):
    anchors = sorted(f for f in os.listdir(census) if f.endswith(".md"))
    w("census anchors tail: %s (C-00030/31 absent = gate closed)" % anchors[-3:])
    w("C-00030 present: %s | C-00031 present: %s" % ("C-00030.md" in anchors, "C-00031.md" in anchors))
else:
    w("census anchors dir missing: %s" % census)
# pools line count (content-addressed, BigLife cognition, read-only)
pools = os.path.join(HQ, "life", "BigLife", "cognition", "pools.json")
with io.open(pools, "r", encoding="utf-8") as f:
    pj = json.load(f)
total = 0
for v in (pj.get("axes") or {}).values():
    if isinstance(v, list):
        total += len(v)
    elif isinstance(v, dict):
        total += sum(len(vv) for vv in v.values() if isinstance(vv, list))
sp = pj.get("sprite", [])
if isinstance(sp, list):
    total += len(sp)
elif isinstance(sp, dict):
    total += sum(len(vv) for vv in sp.values() if isinstance(vv, list))
w("pools TOTAL_LINES: %d (baseline 1440; axes 1296 + sprite dict 144)" % total)
# export freshness
exp_path = os.path.join(ROOT, "docs", "status-export.json")
with io.open(exp_path, "r", encoding="utf-8") as f:
    ex = json.load(f)
w("export_ts: %s (fresh <=24h)" % ex.get("export_ts", "?"))

# 5) git status + lock + HEAD
p = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True)
w("=== git ===")
w(p.stdout.strip()[:600] if p.stdout.strip() else "(clean)")
lock = os.path.join(ROOT, ".git", "index.lock")
w("index.lock exists: %s" % os.path.exists(lock))
p2 = subprocess.run(["git", "log", "--oneline", "-2"], cwd=ROOT, capture_output=True, text=True)
w("HEAD 2: %s" % p2.stdout.strip().replace("\n", " | "))

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("OK %d lines -> %s" % (len(lines), OUT))
