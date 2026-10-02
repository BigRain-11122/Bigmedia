import json, re, os

base = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
grp = r"C:\Users\sjs20\Desktop\FluxGroup"
out = []
W = out.append

def rd(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()

st = json.loads(rd(os.path.join(base, "src/os/state.json")))
log = st.get("log", [])

W("== RECENT ROUND TITLES (R900+) ==")
for s in log:
    m = re.match(r"(\d{4}-\d{2}-\d{2} \S+ R(\d+):)(.{0,130})", str(s))
    if m and int(m.group(2)) >= 900:
        W("R%s| %s" % (m.group(2), m.group(3)))

W("== XL MENTIONS IN LOG ==")
cnt = 0
for s in log:
    if "XL-" in str(s):
        cnt += 1
for s in [x for x in log if "XL-" in str(x)][-6:]:
    W("XL| " + str(s)[:230])
W("XL hit rounds=%d" % cnt)

W("== OSS MENTIONS (recent) ==")
oss_hits = [x for x in log if re.search(r"OSS|oss-harvest|OH-2026", str(x))]
W("oss hit count=%d" % len(oss_hits))
for s in oss_hits[-5:]:
    W("OSS| " + str(s)[:200])

W("== OSS-HARVEST DIR ==")
oh = os.path.join(grp, "cph4", "oss-harvest")
try:
    for f in sorted(os.listdir(oh)):
        W(f)
except Exception as e:
    W("err %r" % e)

W("== HQ-FEEDBACK TAIL ==")
hq = rd(os.path.join(base, "HQ-FEEDBACK.md"))
lines = [l for l in hq.splitlines() if l.strip()]
for l in lines[-12:]:
    W("HQ| " + l.strip()[:170])

with open(os.path.join(base, ".c3-tmp", "scan2_out.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("OK %d" % len(out))
