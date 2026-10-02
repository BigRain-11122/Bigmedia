import json, os, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP  = r"C:\Users\sjs20\Desktop\FluxGroup"
OUT = os.path.join(ROOT, "r1035_probe2.txt")
L = []
def w(s=""): L.append(str(s))

with open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
log = st.get("log", [])
w("== log rows R1030..now (first 260 chars each) ==")
for r in log:
    m = re.search(r"R(10[3-9][0-9]):", r)
    if m and int(m.group(1)) >= 1030:
        w("[%s]" % m.group(1))
        w(r[:300])
        w("...tail:" + r[-260:])
        w("======")

q = os.path.join(ROOT, "docs", "self-improvement-queue.md")
with open(q, encoding="utf-8") as f:
    qt = f.read()
w("== queue total lines=%d ==" % len(qt.splitlines()))
w("== queue tail 70 ==")
w("\n".join(qt.splitlines()[-70:]))

anch = os.path.join(GRP, "media", "BigLife", "census", "anchors")
if os.path.isdir(anch):
    names = sorted(os.listdir(anch))
    w("== BigLife anchors count=%d top5=%s ==" % (len(names), names[-5:]))
else:
    w("anchors dir missing at %s" % anch)

nov = os.path.join(ROOT, "data", "storylines", "novel")
if os.path.isdir(nov):
    w("== novel files ==")
    w(", ".join(sorted(os.listdir(nov))))

fin = os.path.join(ROOT, "output", "finished.md")
with open(fin, encoding="utf-8") as f:
    ft = f.read()
w("== finished tail 12 lines ==")
w("\n".join(ft.splitlines()[-12:]))

cards = os.path.join(ROOT, "data", "storylines", "cards", "README.md")
if os.path.exists(cards):
    with open(cards, encoding="utf-8") as f:
        ct = f.read()
    w("== cards README tail 8 ==")
    w("\n".join(ct.splitlines()[-8:]))

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L))
print("PROBE2 OK rows=%d" % len(L))
