import json, os, glob, io, re
from datetime import datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP  = r"C:\Users\sjs20\Desktop\FluxGroup"
out = io.StringIO()
def w(s=""): out.write(str(s) + "\n")

now = datetime.now()
w("now: " + now.strftime("%Y-%m-%d %H:%M:%S") + "  ISOweek: " + str(now.isocalendar()))

sp = os.path.join(ROOT, "src/os/state.json")
st = json.load(open(sp, encoding="utf-8"))
w("")
w("== state.json keys: " + ", ".join(st.keys()))
for k in ("tick","ts","task","production","mode","window_rounds","claimed"):
    if k in st: w(f"{k} = {json.dumps(st[k], ensure_ascii=False)[:300]}")
wm = st.get("decisions_watermark")
w("decisions_watermark = " + json.dumps(wm, ensure_ascii=False)[:1600])
log = st.get("log", [])
w(f"log_len = {len(log)}")
w("")
for i, e in enumerate(log[-5:]):
    e = str(e)
    w(f"--- log[-{5-i}] len={len(e)}")
    w("HEAD: " + e[:330])
    w("TAIL: " + e[-430:])
    w("")

w("== daily briefs (last 6) ==")
dd = os.path.join(ROOT, "data/intel/daily")
if os.path.isdir(dd):
    w(", ".join(sorted(os.listdir(dd))[-6:]))
else:
    w("no daily dir")

w("")
w("== docs/audits (last 12 by mtime) ==")
ad = os.path.join(ROOT, "docs/audits")
for p in sorted(glob.glob(os.path.join(ad, "*")), key=os.path.getmtime)[-12:]:
    w(os.path.basename(p))

w("")
cands = [p for p in glob.glob(os.path.join(ROOT, "**/finished.md"), recursive=True) if ".git" not in p]
for fm in cands:
    lines = open(fm, encoding="utf-8").read().splitlines()
    w(f"== {os.path.relpath(fm, ROOT)} ({len(lines)} lines) last 14:")
    for ln in lines[-14:]:
        w(ln[:200])

w("")
w("== cph4/oss-harvest (last 10 by mtime) ==")
oh = os.path.join(GRP, "cph4/oss-harvest")
for p in sorted(glob.glob(os.path.join(oh, "*")), key=os.path.getmtime)[-10:]:
    w(os.path.basename(p) + "  mtime=" + datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M"))

w("")
w("== orders files (by date in name, top 8) ==")
ofs = []
for p in glob.glob(os.path.join(ROOT, "orders", "*")):
    m = re.search(r"(\d{8})", os.path.basename(p))
    ofs.append((m.group(1) if m else "00000000", os.path.basename(p)))
for d, n in sorted(ofs, reverse=True)[:8]:
    w(d + "  " + n)

w("")
w("== ledger @BigStream/@全司 rows (last 6) ==")
lp = os.path.join(GRP, "cph4/evolution-ledger.md")
pat = re.compile(r"@BigStream|@七线全司|@全司|@六司")
hits = []
with open(lp, encoding="utf-8") as f:
    for i, ln in enumerate(f, 1):
        if pat.search(ln):
            hits.append((i, ln.rstrip()))
w(f"total @hits = {len(hits)}")
for i, ln in hits[-6:]:
    w(f"L{i}: " + ln[:280])

open(os.path.join(ROOT, ".c3-tmp/r1371_probe.txt"), "w", encoding="utf-8").write(out.getvalue())
print("OK")
