import json, re, io, os
from datetime import datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
G = r"C:\Users\sjs20\Desktop\FluxGroup"
OUTP = os.path.join(ROOT, ".c3-tmp", "r1430_check_out.txt")

out = io.open(OUTP, "w", encoding="utf-8")
def w(s):
    try:
        out.write(s + "\n")
    except Exception:
        out.write(repr(s) + "\n")

w("now=%s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# 1) state.json summary
st = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
w("== state.json ==")
w("tick=%s" % st.get("tick"))
w("ts=%s" % st.get("ts"))
w("task=%s" % st.get("task"))
w("production=%s" % st.get("production"))
wm = st.get("decisions_watermark", {})
if isinstance(wm, dict):
    dnums = set(wm.get("dnums", []))
else:
    dnums = set(wm if isinstance(wm, list) else [])
w("watermark dnums count=%d" % len(dnums))
log = st.get("log", [])
w("log count=%d" % len(log))
for entry in log[-4:]:
    w("LOG| " + (str(entry) if not isinstance(entry, dict) else json.dumps(entry, ensure_ascii=False))[:300])

# 2) group decisions.md scan (content addressing)
dec = io.open(os.path.join(G, "docs", "decisions.md"), encoding="utf-8").read()
ds = set(re.findall(r"[DC]-\d{8}-\d{2}", dec))
new = sorted(ds - dnums)
w("== decisions.md ==")
w("total D/C tokens=%d new_vs_watermark=%d" % (len(ds), len(new)))
w("new_tokens=%s" % ",".join(new))
lines = dec.splitlines()
# dispatch board block (派工通告板)
board_start = None
for i, l in enumerate(lines):
    if "派工通告板" in l:
        board_start = i
        break
if board_start is not None:
    block = lines[board_start:board_start + 40]
    w("-- dispatch board head rows --")
    for l in block[:40]:
        if l.strip():
            w("BOARD| " + l[:200])
hits = [(i + 1, l) for i, l in enumerate(lines) if ("BigStream" in l or "七司" in l or "全司" in l)]
w("bigstream/7si lines total=%d last8:" % len(hits))
for i, l in hits[-8:]:
    w("DEC L%d| %s" % (i, l[:200]))

# 3) evolution-ledger @BigStream-family scan
led = io.open(os.path.join(G, "cph4", "evolution-ledger.md"), encoding="utf-8").read()
llines = led.splitlines()
pat = re.compile(r"@BigStream|@七线全司|@全司|@六司|@八线全量")
hits2 = [(i + 1, l) for i, l in enumerate(llines) if pat.search(l)]
w("== evolution-ledger ==")
w("at-family lines total=%d last6:" % len(hits2))
for i, l in hits2[-6:]:
    w("LED L%d| %s" % (i, l[:220]))
pnums = set(re.findall(r"P-\d{4}-\d{2}-\d{2}-\d{2}", led))
w("ledger P-tokens count=%d last6=%s" % (len(pnums), ",".join(sorted(pnums)[-6:])))

# 4) group orders.md physical-件 region (present-status only, no chasing)
o = io.open(os.path.join(G, "docs", "orders.md"), encoding="utf-8").read()
olines = o.splitlines()
w("== orders.md chars=%d ==" % len(o))
acct = [(i + 1, l) for i, l in enumerate(olines) if ("物理件" in l or ("账号" in l and i < 60))]
w("physical-lines last4:")
for i, l in acct[-4:]:
    w("ORD L%d| %s" % (i, l[:160]))

# 5) local orders dir freshness (latest file + mtime)
odir = os.path.join(ROOT, "orders")
ents = []
for f in os.listdir(odir):
    p = os.path.join(odir, f)
    ents.append((os.path.getmtime(p), f))
ents.sort(reverse=True)
w("== local orders latest3 ==")
for mt, f in ents[:3]:
    w("ORD-LOCAL %s mtime=%s" % (f, datetime.fromtimestamp(mt).strftime("%Y-%m-%d %H:%M")))

# 6) backlog open items (topmost unfinished)
bl = io.open(os.path.join(ROOT, "src", "os", "backlog.md"), encoding="utf-8").read().splitlines()
open_items = []
for idx, l in enumerate(bl):
    m = re.match(r"^(\d+)\.\s", l)
    if m and "[done" not in l:
        open_items.append((int(m.group(1)), idx + 1, l))
w("== backlog ==")
w("open item count=%d (file order, first 12):" % len(open_items))
for num, ln, l in open_items[:12]:
    w("OPEN #%d L%d| %s" % (num, ln, l[:170]))

# 7) self-improvement-queue top (open items)
q = os.path.join(ROOT, "docs", "self-improvement-queue.md")
if os.path.exists(q):
    ql = io.open(q, encoding="utf-8").read().splitlines()
    w("== self-improvement-queue (first 30 lines) ==")
    for l in ql[:30]:
        if l.strip():
            w("Q| " + l[:180])
else:
    w("== self-improvement-queue MISSING ==")

# 8) global benchmarks freshness (§④ first update-record date)
gb = os.path.join(ROOT, "docs", "global-benchmarks.md")
if os.path.exists(gb):
    gl = io.open(gb, encoding="utf-8").read().splitlines()
    rec = [l for l in gl if "更新记录" in l or re.match(r"^\|?\s*20\d\d-\d\d-\d\d", l.strip())]
    w("== global-benchmarks ==")
    for l in rec[:4]:
        w("GB| " + l[:160])
else:
    w("== global-benchmarks MISSING ==")

out.close()
print("done -> " + OUTP)
