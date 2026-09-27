# R508 quick-path anchor check (canon: r501_check lineage, OUTP to new file)
import io, os, re, glob, datetime

OUTP = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r508_check.txt"
lines = []

# 1. orders: O- prefixed files count + latest name + mtime
od = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\orders"
ofiles = [f for f in os.listdir(od) if f.startswith("O-")]
lines.append("orders_count %d" % len(ofiles))
lates = sorted(ofiles)[-1]
lines.append("orders_latest %s mtime %s" % (lates, datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(od, lates))).strftime("%H:%M:%S")))
# any order file edited after R507 anchor close 11:38:36?
edited = []
for f in ofiles:
    p = os.path.join(od, f)
    mt = os.path.getmtime(p)
    if datetime.datetime.fromtimestamp(mt) > datetime.datetime(2026, 9, 27, 11, 38, 36):
        edited.append(f)
lines.append("orders_edited_since_anchor %s" % (edited if edited else "NONE"))

# 2. ledger five-mode row count (canon: @BigStream/@七线全司/@全司/@六司/@八线全量)
lp = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
pat = re.compile(r"@BigStream|@\u4e03\u7ebf\u5168\u53f8|@\u5168\u53f8|@\u516d\u53f8|@\u516b\u7ebf\u5168\u91cf")
cnt = 0
new_rows = []
with io.open(lp, encoding="utf-8") as fh:
    for l in fh:
        if pat.search(l):
            cnt += 1
            if "P-2026-09-2" in l and "09-27" in l:
                new_rows.append(l.strip()[:80])
lines.append("ledger_fivemode_rows %d (anchor 30)" % cnt)
lines.append("ledger_recent_rows %s" % (" | ".join(new_rows[-3:]) if new_rows else "NONE"))

# 3. decisions non-blank count (anchor 45)
dp = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
nb = 0
with io.open(dp, encoding="utf-8") as fh:
    for l in fh:
        if l.strip():
            nb += 1
lines.append("decisions_nonblank %d (anchor 45)" % nb)

# 4. index.lock + production
lock = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.git\index.lock"
lines.append("index_lock %s" % os.path.exists(lock))
sp = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
with io.open(sp, encoding="utf-8") as fh:
    st = fh.read()
lines.append("production_open %s" % ('"production": "open"' in st))

# 5. storylines three subdomains newest writes (bm-a activity probe)
for sub in ("novel", "audio", "comic"):
    d = os.path.join(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines", sub)
    if not os.path.isdir(d):
        lines.append("storyline_%s MISSING" % sub)
        continue
    fs = [x for x in glob.glob(os.path.join(d, "**", "*"), recursive=True) if os.path.isfile(x)]
    if not fs:
        lines.append("storyline_%s EMPTY" % sub)
        continue
    newest = max(fs, key=os.path.getmtime)
    lines.append("storyline_%s newest %s %s" % (sub, os.path.basename(newest), datetime.datetime.fromtimestamp(os.path.getmtime(newest)).strftime("%m-%d %H:%M")))

# 6. BigLife interchat ledger probe (#72 window <=09-28 12:00)
hit = []
for root, dirs, files in os.walk(r"C:\Users\sjs20\Desktop\FluxGroup"):
    for f in files:
        if ("\u4e92\u804a" in f) and ("BigLife" in root or "biglife" in root.lower()):
            hit.append(os.path.join(root, f))
    if len(hit) > 5:
        break
lines.append("biglife_interchat_hits %s" % (len(hit)))

with io.open(OUTP, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")
print("OK")
