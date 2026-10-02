import json, re, os, subprocess

base = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
grp = r"C:\Users\sjs20\Desktop\FluxGroup"
out = []
W = out.append

def rd(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()

W("== STATE ==")
st = json.loads(rd(os.path.join(base, "src/os/state.json")))
W("tick=%s ts=%s" % (st.get("tick"), st.get("ts")))
W("task=%r" % str(st.get("task"))[:110])
W("production=%r" % st.get("production"))
wm = st.get("decisions_watermark", {})
dnums_known = set()
if isinstance(wm, dict):
    dnums_known = set(wm.get("dnums", []) or [])
    W("wm_keys=%s wm_count=%d" % (list(wm.keys()), len(dnums_known)))
log = st.get("log", [])
W("log_count=%d" % len(log))
for s in log[-3:]:
    W("LOG| " + str(s)[:240])

W("== GIT ==")
r = subprocess.run(["git","-C",base,"status","--short"], capture_output=True, text=True, encoding="utf-8", errors="replace")
W(r.stdout.strip() or "(clean)")
r = subprocess.run(["git","-C",base,"log","-3","--oneline"], capture_output=True, text=True, encoding="utf-8", errors="replace")
W(r.stdout.strip())

W("== ORDERS DIR TAIL ==")
od = os.path.join(base, "orders")
try:
    for f in sorted(os.listdir(od))[-5:]:
        W(f)
except Exception as e:
    W("err %r" % e)

W("== DECISIONS DIFF ==")
dec = rd(os.path.join(grp, "docs", "decisions.md"))
dn = set(re.findall(r"[DC]-\d{8}-\d{2}", dec))
new = sorted(dn - dnums_known)
W("dec_total=%d known=%d NEW=%s" % (len(dn), len(dnums_known), new))
idx = dec.find("pai-gong")
idx2 = dec.find(u"派工通告板")
if idx2 >= 0:
    seg = dec[idx2: idx2+2600]
    for l in seg.splitlines()[:26]:
        if l.strip():
            W("PB| " + l.strip()[:150])
else:
    W("(no dispatch board header)")

W("== LEDGER @SCAN ==")
led = rd(os.path.join(grp, "cph4", "evolution-ledger.md"))
pat = re.compile(r"@(?:BigStream|七线全司|全司|六司|八线全量)")
hits = []
for i, l in enumerate(led.splitlines(), 1):
    if pat.search(l):
        hits.append((i, l.strip()))
W("hits=%d" % len(hits))
for n, l in hits[-8:]:
    W("L%d| %s" % (n, l[:160]))

W("== ROUTINE ==")
W("daily 10-02 exists: %s" % os.path.exists(os.path.join(base, "data", "intel", "daily", "2026-10-02.md")))
try:
    afs = sorted(os.listdir(os.path.join(base, "docs", "audits")))
    W("audits tail: %s" % afs[-5:])
except Exception as e:
    W("audits err %r" % e)
gb = rd(os.path.join(base, "docs", "global-benchmarks.md"))
i4 = gb.find(u"更新记录")
dates = re.findall(r"2026-\d{2}-\d{2}", gb[i4:i4+400]) if i4 >= 0 else []
W("gb update-rec dates head: %s" % dates[:3])

W("== QUEUE TOP ==")
q = rd(os.path.join(base, "docs", "self-improvement-queue.md"))
ql = [l.strip() for l in q.splitlines() if l.strip()]
for l in ql[:42]:
    W("Q| " + l[:160])

with open(os.path.join(base, ".c3-tmp", "scan_out.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("OK lines=%d" % len(out))
