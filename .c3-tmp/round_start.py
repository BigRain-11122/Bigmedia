import json, re, os, io, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .c3-tmp -> repo root
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "round_start_check.txt")
GRP = r"C:\Users\sjs20\Desktop\FluxGroup"

lines = []
def w(s): lines.append(str(s))

# 1. state.json fields
sp = os.path.join(ROOT, "src", "os", "state.json")
d = json.load(open(sp, encoding="utf-8"))
w("== state.json ==")
w("ts=%s" % d.get("ts"))
w("task=%s" % d.get("task"))
w("tick=%s" % d.get("tick"))
w("production=%s" % d.get("production"))
wm = d.get("decisions_watermark", {})
w("watermark.dnums_count=%s" % len(wm.get("dnums", [])) if isinstance(wm, dict) else "watermark=%s" % wm)
if isinstance(wm, dict):
    w("watermark.dnums_tail=%s" % ",".join(wm.get("dnums", [])[-8:]))
    w("watermark keys=%s" % list(wm.keys()))
log = d.get("log", [])
w("log_count=%s" % len(log))
w("== log tail 3 ==")
for x in log[-3:]:
    w(x[:600])

# 2. orders latest
w("== orders latest ==")
od = os.path.join(ROOT, "orders")
fs = sorted(glob.glob(os.path.join(od, "*")), key=os.path.getmtime, reverse=True)
for f in fs[:4]:
    w("%s mtime=%s" % (os.path.basename(f), datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime("%m-%d %H:%M")))

# 3. group transfer scan: evolution-ledger @BigStream lines
w("== evolution-ledger scan ==")
led = os.path.join(GRP, "cph4", "evolution-ledger.md")
if os.path.exists(led):
    txt = open(led, encoding="utf-8", errors="replace").read().splitlines()
    pats = re.compile(r"@BigStream|@七线全司|@全司|@六司|@八线全量")
    hits = [(i+1, l[:160]) for i, l in enumerate(txt) if pats.search(l)]
    w("total_hit_lines=%s" % len(hits))
    for i, l in hits[-6:]:
        w("L%s: %s" % (i, l))
else:
    w("ledger MISSING")

# 4. decisions.md D/C set diff vs watermark
w("== decisions.md content-address diff ==")
dec = os.path.join(GRP, "docs", "decisions.md")
if os.path.exists(dec):
    dtxt = open(dec, encoding="utf-8", errors="replace").read()
    cur = set(re.findall(r"[DC]-20\d{6}-\d{2}", dtxt))
    wnums = set(wm.get("dnums", [])) if isinstance(wm, dict) else set()
    new = sorted(cur - wnums)
    w("cur_count=%s known_count=%s new=%s" % (len(cur), len(wnums), new if new else "NONE"))
else:
    w("decisions MISSING")

# 5. index.lock / daily brief / weekly audit
w("== misc ==")
w("index_lock=%s" % os.path.exists(os.path.join(ROOT, ".git", "index.lock")))
db = os.path.join(ROOT, "data", "intel", "daily", "2026-10-04.md")
w("daily_1004=%s" % os.path.exists(db))
wk = glob.glob(os.path.join(ROOT, "docs", "audits", "*self-audit*"))
w("self_audits=%s" % [os.path.basename(x) for x in wk])
# group orders.md CEO physical items note (top lines)
go = os.path.join(GRP, "docs", "orders.md")
if os.path.exists(go):
    mt = os.path.getmtime(go)
    w("group_orders_mtime=%s" % datetime.datetime.fromtimestamp(mt).strftime("%m-%d %H:%M"))
# dispatch board top block
try:
    g2 = open(dec, encoding="utf-8", errors="replace").read().splitlines()
    for i, l in enumerate(g2[:40]):
        if "派工通告" in l:
            w("dispatch_board_at_L%s" % (i+1))
            for j in range(i, min(i+15, len(g2))):
                w("  %s" % g2[j][:150])
            break
except Exception as e:
    w("dispatch_err=%s" % e)

open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print("OK %s lines" % len(lines))
