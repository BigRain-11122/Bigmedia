import os, json, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = os.path.join(ROOT, "media", "BigStream")
OUT = []
def w(s): OUT.append(s)

# orders count + latest mtimes
od = os.path.join(BS, "orders")
ofs = [(f, os.path.getmtime(os.path.join(od, f))) for f in os.listdir(od) if f.endswith(".md")]
ofs.sort(key=lambda x: -x[1])
w("ORDERS_N=%d" % len(ofs))
for f, m in ofs[:3]:
    w("ORD|%s|%s" % (f, time.strftime("%m-%d %H:%M:%S", time.localtime(m))))

# ledger five-pattern LINE count (case-sensitive canon)
pats = ["@BigStream", "@七线全司", "@全司", "@六司", "@八线全量"]
led = os.path.join(ROOT, "cph4", "evolution-ledger.md")
cnt = 0
with open(led, encoding="utf-8") as f:
    for ln in f:
        if any(p in ln for p in pats):
            cnt += 1
w("LEDGER_LINES=%d" % cnt)

# decisions non-empty lines
dec = os.path.join(ROOT, "docs", "decisions.md")
nn = []
with open(dec, encoding="utf-8") as f:
    for ln in f:
        if ln.strip():
            nn.append(ln.strip())
w("DECISIONS=%d" % len(nn))

# state fields
st = json.load(open(os.path.join(BS, "src", "os", "state.json"), encoding="utf-8"))
w("PROD=%s|TICK=%s|TS=%s" % (st.get("production"), st.get("tick"), st.get("ts")))
w("LOGN=%d" % len(st.get("log", [])))

# anchors C-00030/31 + tail
ad = os.path.join(ROOT, "life", "BigLife", "census", "anchors")
w("C30=%s|C31=%s" % (os.path.exists(os.path.join(ad, "C-00030.md")), os.path.exists(os.path.join(ad, "C-00031.md"))))
try:
    tail = sorted([f for f in os.listdir(ad) if f.endswith(".md")])[-3:]
    w("ANCHOR_TAIL=%s" % ",".join(tail))
except Exception as e:
    w("ANCHOR_ERR=%s" % e)

# interchat ledger (#72) + footage tail (#78 FluxVerse 实录到位核验)
w("INTERCHAT=%s" % os.path.exists(os.path.join(ROOT, "life", "BigLife", "cognition", "interchat-ledger.jsonl")))
ft = os.path.join(BS, "data", "sources", "footage")
if os.path.isdir(ft):
    fs = [(f, os.path.getmtime(os.path.join(ft, f))) for f in os.listdir(ft)]
    fs.sort(key=lambda x: -x[1])
    w("FOOTAGE_TAIL=%s|%s" % (fs[0][0], time.strftime("%m-%d %H:%M", time.localtime(fs[0][1]))))

# window items
w("W40=%s" % os.path.exists(os.path.join(BS, "docs", "audits", "2026-W40-self-audit.md")))
w("INTEL28=%s" % os.path.exists(os.path.join(BS, "data", "intel", "daily", "2026-09-28.md")))

# tmp inventories
bt = os.path.join(BS, ".bs006-tmp")
if os.path.isdir(bt):
    w("BS006_TMP=%s" % ",".join(sorted(os.listdir(bt))))
lc = os.path.join(BS, ".lc001-tmp")
if os.path.isdir(lc):
    w("LC001_TMP=%s" % ",".join(sorted(os.listdir(lc))))

outp = os.path.join(BS, ".c3-tmp", "r515_check_out.txt")
with open(outp, "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("OK %d lines" % len(OUT))
