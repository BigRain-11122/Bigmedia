# -*- coding: utf-8 -*-
"""R477 fast-path five-check probe (write_file new file, no PS roundtrip, OUTP fresh)."""
import os, re, glob, time, subprocess

OUTP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "r477_check.txt")
lines = []

def w(s):
    lines.append(s)

w("now " + time.strftime("%Y-%m-%d %H:%M:%S"))

# 1. orders latest (O- prefix) vs anchor O-20260925-1931-HQ-C
od = glob.glob("orders/O-*.md")
od.sort(key=os.path.getmtime)
top = os.path.basename(od[-1]) if od else "NONE"
w("orders_top " + top)
w("orders_top_mtime " + (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(od[-1]))) if od else "-"))
w("orders_O_count " + str(len(od)))

# 2. index.lock
w("index_lock " + str(os.path.exists(".git/index.lock")))

# 3. ledger five-mode rows (strict @ prefix: @BigStream/@七线全司/@全司/@六司/@八线全量)
try:
    ld = open(r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md", encoding="utf-8").read()
    rows = [l for l in ld.splitlines() if re.search(r"@(BigStream|七线全司|全司|六司|八线全量)", l)]
    w("ledger_rows " + str(len(rows)))
    if rows:
        w("ledger_last_row_len " + str(len(rows[-1])))
except Exception as e:
    w("ledger_ERR " + repr(e))

# 4. decisions non-empty count (anchor 45)
try:
    dc = open(r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md", encoding="utf-8").read()
    w("decisions_nonempty " + str(len([l for l in dc.splitlines() if l.strip()])))
except Exception as e:
    w("decisions_ERR " + repr(e))

# 5. daily briefs
w("daily_0927 " + str(os.path.exists("data/intel/daily/2026-09-27.md")))
w("daily_0928 " + str(os.path.exists("data/intel/daily/2026-09-28.md")))

# 6. production state
st = open("src/os/state.json", encoding="utf-8").read()
w("production_open " + str('"production": "open"' in st))

# 7. anchors C-00030/C-00031 supply-gate check (census anchors file)
census_hits = []
for pat in ("data/**/census*.json", "data/**/anchors*.json"):
    for f in glob.glob(pat, recursive=True):
        try:
            c = open(f, encoding="utf-8").read()
            if "C-00030" in c or "C-00031" in c:
                census_hits.append(f)
        except Exception:
            pass
w("anchor_C00030_31 " + (str(census_hits) if census_hits else "False"))

# 8. storylines subdomain fresh writes (bm-a activity sign): newest mtime per dir
base = "data/storylines"
for sub in ("novel", "audio", "comic"):
    d = os.path.join(base, sub)
    if not os.path.isdir(d):
        w("storylines_%s nodir" % sub)
        continue
    newest = 0
    for root, _dirs, files in os.walk(d):
        for f in files:
            newest = max(newest, os.path.getmtime(os.path.join(root, f)))
    w("storylines_%s_newest %s" % (sub, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(newest)) if newest else "none"))

# 9. git status + HEAD
g = subprocess.run(["git", "status", "--short"], capture_output=True, text=True, encoding="utf-8")
w("git_status_begin")
w(g.stdout.strip() if g.stdout.strip() else "(clean)")
w("git_status_end")
h = subprocess.run(["git", "log", "-1", "--oneline"], capture_output=True, text=True, encoding="utf-8")
w("HEAD " + h.stdout.strip())

# 10. state tick/ts tail
m = re.search(r'"tick":\s*(\d+)', st)
w("state_tick " + (m.group(1) if m else "?"))
m2 = re.search(r'"ts":\s*"([^"]+)"', st)
w("state_ts " + (m2.group(1) if m2 else "?"))

with open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("OK r477_check ->", OUTP)
