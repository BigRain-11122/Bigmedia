# -*- coding: utf-8 -*-
# Fast-path five-check scratch (round opener): state tail / watermark / ledger / decisions / orders / backlog top
import json, re, os, io, glob, datetime

BASE = r"C:\Users\sjs20\Desktop\FluxGroup"
BM = os.path.join(BASE, "media", "BigStream")
OUT = []

def w(s):
    OUT.append(str(s))

# 1) state.json
with open(os.path.join(BM, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
w("== STATE ==")
w("tick=%s | ts=%s" % (st.get("tick"), st.get("ts")))
w("task=%s" % st.get("task"))
w("production=%s" % st.get("production"))
wm = st.get("decisions_watermark") or {}
w("watermark=%s" % json.dumps(wm, ensure_ascii=False)[:400])
log = st.get("log") or []
w("log_len=%d" % len(log))
for line in log[-3:]:
    w("LOGTAIL>> " + line[:900])

# 2) group decisions.md
dec_path = os.path.join(BASE, "docs", "decisions.md")
dec = open(dec_path, encoding="utf-8").read()
dnums = sorted(set(re.findall(r"D-\d{8}-\d+", dec)))
cnums = sorted(set(re.findall(r"C-\d{8}-\d+", dec)))
known = set(wm.get("dnums") or []) | set(wm.get("cnums") or [])
new_rows = [d for d in dnums if d not in known] + [c for c in cnums if c not in known]
w("== DECISIONS ==")
w("total_d=%d total_c=%d new_vs_watermark=%s" % (len(dnums), len(cnums), new_rows))
m = re.search(r"派工通告板(.*?)(?=\n#+ |\Z)", dec, re.S)
if m:
    rows = [r.strip() for r in m.group(1).splitlines() if r.strip()]
    w("dispatch_rows=%d (tail 6):" % len(rows))
    for r in rows[-6:]:
        w("DISPATCH>> " + r[:260])
else:
    w("dispatch_board=NOT FOUND")

# 3) evolution-ledger @ rows
led_path = os.path.join(BASE, "cph4", "evolution-ledger.md")
led = open(led_path, encoding="utf-8").read()
pat = re.compile(r"@(BigStream|七线全司|全司|六司|八线)")
hits = [l for l in led.splitlines() if pat.search(l)]
w("== LEDGER ==")
w("at_rows=%d (tail 4):" % len(hits))
for l in hits[-4:]:
    w("LEDGER>> " + l[:300])

# 4) group orders.md CEO physical-item zone (status rows only)
try:
    go = open(os.path.join(BASE, "docs", "orders.md"), encoding="utf-8").read()
    lines = [l.strip() for l in go.splitlines() if ("物理件" in l or "账号" in l or "商户" in l or "服务器" in l)]
    w("== GROUP ORDERS physical ==")
    for l in lines[-6:]:
        w("GORDER>> " + l[:200])
except Exception as e:
    w("group orders read err: %s" % e)

# 5) own orders dir tail by mtime
odir = os.path.join(BM, "orders")
files = sorted(glob.glob(os.path.join(odir, "*")), key=os.path.getmtime)
w("== OWN ORDERS tail ==")
for f in files[-4:]:
    w("ORDER>> %s (%s)" % (os.path.basename(f), datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime("%m-%d %H:%M")))

# 6) backlog top items status
bl = open(os.path.join(BM, "src", "os", "backlog.md"), encoding="utf-8").read().splitlines()
w("== BACKLOG items ==")
count = 0
for l in bl:
    if re.match(r"^\d+\.", l):
        num = l.split(".")[0]
        done = "[done" in l
        w("ITEM %s done=%s :: %s" % (num, done, l[:150]))
        count += 1
        if count >= 14:
            break
w("backlog_total_lines=%d" % len(bl))

# 7) routine checks
w("== ROUTINE ==")
w("intel_today=%s" % os.path.exists(os.path.join(BM, "data", "intel", "daily", "2026-10-01.md")))
w("audit_W40=%s" % os.path.exists(os.path.join(BM, "docs", "audits", "2026-W40-self-audit.md")))
try:
    gb = open(os.path.join(BM, "docs", "global-benchmarks.md"), encoding="utf-8").read()
    idx = gb.find("更新记录")
    dates = re.findall(r"2026-\d{2}-\d{2}", gb[idx:]) if idx >= 0 else []
    w("gb_last_update=%s" % (dates[0] if dates else "NONE"))
except Exception as e:
    w("gb err %s" % e)
w("lock_exists=%s" % os.path.exists(os.path.join(BM, ".git", "index.lock")))
# probe scripts present
for name in ["board", "readiness", "loop_health"]:
    cands = glob.glob(os.path.join(BM, "src", "**", "*%s*.py" % name), recursive=True)
    w("probe[%s]=%s" % (name, [os.path.relpath(c, BM) for c in cands][:3]))

with open(os.path.join(BM, ".c3-tmp", "round_check_out.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("OK lines=%d" % len(OUT))
