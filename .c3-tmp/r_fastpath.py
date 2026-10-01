import json, re, os, subprocess, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = os.path.join(ROOT, "media", "BigStream")
OUT = []

def sec(t):
    OUT.append("")
    OUT.append("==== " + t + " ====")

sec("clock")
OUT.append("now: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

sec("state.json")
with open(os.path.join(BS, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
for k in ["tick", "ts", "task", "production"]:
    OUT.append(k + ": " + str(st.get(k))[:260])
wm = st.get("decisions_watermark", {})
if isinstance(wm, dict):
    dnums = wm.get("dnums", [])
    OUT.append("wm keys: " + str(list(wm.keys())))
    OUT.append("dnums count: %d last5: %s" % (len(dnums), dnums[-5:]))
log = st.get("log", [])
OUT.append("log count: %d" % len(log))
for line in log[-3:]:
    OUT.append("LOGTAIL: " + line[:700])

sec("git status")
r = subprocess.run(["git", "status", "--short"], cwd=BS, capture_output=True, text=True)
OUT.append(r.stdout.strip()[:800] or "(clean)")
lock = os.path.join(BS, ".git", "index.lock")
OUT.append("index.lock exists: " + str(os.path.exists(lock)))

sec("orders dir latest")
od = os.path.join(BS, "orders")
files = sorted(os.listdir(od))
OUT.extend(files[-8:])

sec("backlog top + R9xx/claims")
with open(os.path.join(BS, "src", "os", "backlog.md"), encoding="utf-8") as f:
    bl = f.read().splitlines()
for l in bl[:14]:
    OUT.append("BL: " + l[:220])
r9 = [l for l in bl if re.search(r"R9[0-1]\d", l)]
OUT.append("--- R9xx mention lines: %d ---" % len(r9))
for l in r9[-20:]:
    OUT.append("R9: " + l[:260])

sec("daily brief / weekly audit / benchmarks")
for p in [os.path.join(BS, "data", "intel", "daily", "2026-10-02.md"),
          os.path.join(BS, "docs", "audits", "2026-W40-self-audit.md"),
          os.path.join(BS, "docs", "global-benchmarks.md")]:
    OUT.append(p.split("\\BigStream\\")[-1] + " exists: " + str(os.path.exists(p)))

sec("group evolution-ledger @rows")
p = os.path.join(ROOT, "cph4", "evolution-ledger.md")
try:
    glines = open(p, encoding="utf-8", errors="replace").read().splitlines()
except Exception as e:
    glines = []
    OUT.append("ERR " + str(e))
at = [(i + 1, l.strip()) for i, l in enumerate(glines) if re.search(r"@BigStream|@七线全司|@全司|@六司|@八线", l)]
OUT.append("at rows: %d" % len(at))
for i, l in at[-6:]:
    OUT.append("L%d: %s" % (i, l[:220]))

sec("group decisions.md")
p2 = os.path.join(ROOT, "docs", "decisions.md")
try:
    txt2 = open(p2, encoding="utf-8", errors="replace").read()
except Exception as e:
    txt2 = ""
    OUT.append("ERR " + str(e))
dn = set(re.findall(r"D-20\d{6}-\d+", txt2))
cn = set(re.findall(r"C-20\d{6}-\d+", txt2))
OUT.append("D count %d latest8: %s" % (len(dn), ", ".join(sorted(dn)[-8:])))
OUT.append("C count %d latest6: %s" % (len(cn), ", ".join(sorted(cn)[-6:])))
OUT.append("--- decisions.md head 55 nonblank lines ---")
cnt = 0
for l in txt2.splitlines():
    if l.strip():
        OUT.append("HEAD: " + l.strip()[:200])
        cnt += 1
        if cnt >= 55:
            break

sec("group orders.md physical items")
try:
    txt3 = open(os.path.join(ROOT, "docs", "orders.md"), encoding="utf-8", errors="replace").read()
    m = re.search(r"物理件", txt3)
    if m:
        OUT.append(txt3[max(0, m.start() - 300): m.start() + 900][:1100])
    else:
        OUT.append("(no marker)")
except Exception as e:
    OUT.append("ERR " + str(e))

with open(os.path.join(BS, ".c3-tmp", "r_fastpath_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("written lines:", len(OUT))
