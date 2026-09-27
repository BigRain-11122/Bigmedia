# r514 fast-path anchor checks (ASCII output only)
import os, json, glob, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
STATE = os.path.join(ROOT, "src", "os", "state.json")

# 1. orders anchor: 35 files (excl README.md), top mtime
orders_dir = os.path.join(ROOT, "orders")
mds = [f for f in glob.glob(os.path.join(orders_dir, "*.md"))
       if os.path.basename(f).lower() != "readme.md"]
stat = sorted(((os.path.getmtime(f), os.path.basename(f)) for f in mds), reverse=True)
import datetime
print("orders_count_excl_readme:", len(mds))
for mt, name in stat[:3]:
    print("order:", name, datetime.datetime.fromtimestamp(mt).strftime("%m-%d %H:%M:%S"))

# 2. evolution-ledger five-mode line count (case-sensitive strict patterns)
ledger = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
pat = re.compile(r"@(BigStream|七线全司|全司|六司|八线全量)")
n_lines = 0
hits = []
with open(ledger, encoding="utf-8", errors="replace") as fh:
    for i, line in enumerate(fh, 1):
        if pat.search(line):
            n_lines += 1
            hits.append((i, line.strip()[:80]))
print("ledger_five_mode_lines:", n_lines)
for i, h in hits[-3:]:
    print("ledger_last:", i, h)

# 3. decisions.md non-empty line count
dec = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
with open(dec, encoding="utf-8", errors="replace") as fh:
    nonempty = sum(1 for l in fh if l.strip())
print("decisions_nonempty_lines:", nonempty)

# 4. state fields + production self-heal check
with open(STATE, encoding="utf-8") as fh:
    st = json.load(fh)
print("production:", st.get("production"))
print("tick:", st.get("tick"), "ts:", st.get("ts"))

# 5. index.lock
lock = os.path.join(ROOT, ".git", "index.lock")
print("index_lock:", os.path.exists(lock))

# 6. window items: BigLife anchors C-00030/31, interchat, footage freshness
for cid in ("C-00030", "C-00031"):
    p = rf"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\{cid}.md"
    print("anchor", cid, os.path.exists(p))
ic = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\interchat-ledger.jsonl"
print("interchat:", os.path.exists(ic))
foot = os.path.join(ROOT, "data", "sources", "footage")
if os.path.isdir(foot):
    fs = sorted(((os.path.getmtime(os.path.join(foot, f)), f) for f in os.listdir(foot)), reverse=True)
    for mt, f in fs[:4]:
        print("footage:", f, datetime.datetime.fromtimestamp(mt).strftime("%m-%d %H:%M"))

# 7. bs006 workdir + sources listing
for d in (os.path.join(ROOT, ".bs006-tmp"), os.path.join(ROOT, "data", "sources", "bs006")):
    print("dir:", d)
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            fp = os.path.join(d, f)
            print("  ", f, os.path.getsize(fp) if os.path.isfile(fp) else "<dir>")

# 8. daily brief + W40 audit presence
db = os.path.join(ROOT, "data", "intel", "daily", "2026-09-27.md")
print("daily_0927:", os.path.exists(db))
db28 = os.path.join(ROOT, "data", "intel", "daily", "2026-09-28.md")
print("daily_0928:", os.path.exists(db28))
w40 = os.path.join(ROOT, "docs", "audits", "2026-W40-self-audit.md")
print("w40_audit:", os.path.exists(w40))
