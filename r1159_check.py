# -*- coding: utf-8 -*-
# Fast-path five-check dump (round R1159). Output: r1159_check.txt (UTF-8).
import json, os, re, subprocess, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "r1159_check.txt")
GROUP = os.path.normpath(os.path.join(ROOT, "..", ".."))  # FluxGroup
lines = []

def sec(t):
    lines.append("")
    lines.append("=== " + t + " ===")

now = datetime.datetime.now()
sec("TIME / ENV")
lines.append("now=%s" % now.strftime("%Y-%m-%d %H:%M:%S"))

# 1) state.json fields + log tail 3
with open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
sec("STATE top fields")
for k in ("tick", "ts", "task", "focus", "production", "mode"):
    lines.append("%s=%s" % (k, st.get(k)))
wm = st.get("decisions_watermark", {})
dnums = set(wm.get("dnums", []))
sec("STATE log tail 3 (first 600 chars each)")
log = st.get("log", [])
lines.append("log_len=%d" % len(log))
for e in log[-3:]:
    lines.append("--- entry (first 600):")
    lines.append(str(e)[:600])

# 2) git status / HEAD / recent log
def sh(args):
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (p.stdout or "") + (("\n[stderr]" + p.stderr) if p.stderr.strip() else "")
sec("GIT")
g = sh(["git", "status", "--short"])
lines.append("status--short:\n" + (g.strip()[:1500] if g.strip() else "(clean)"))
lines.append("HEAD: " + sh(["git", "log", "-1", "--oneline"]).strip())
lines.append("recent5:\n" + sh(["git", "log", "-5", "--oneline"]).strip())
lock = os.path.join(ROOT, ".git", "index.lock")
lines.append("index.lock exists: %s" % os.path.exists(lock))

# 3) orders/ latest files by mtime
sec("ORDERS dir (latest 8 by mtime)")
od = os.path.join(ROOT, "orders")
files = [(os.path.getmtime(os.path.join(od, n)), n) for n in os.listdir(od) if os.path.isfile(os.path.join(od, n))]
files.sort(reverse=True)
for mt, n in files[:8]:
    lines.append("%s  %s" % (datetime.datetime.fromtimestamp(mt).strftime("%m-%d %H:%M:%S"), n))

# 4) group ledger scan: @BigStream / group-wide mentions (last 5 + count)
sec("GROUP evolution-ledger @BigStream scan")
ledger = os.path.join(GROUP, "cph4", "evolution-ledger.md")
pat = re.compile(r"@BigStream|@涓冪嚎鍏ㄥ徃|@鍏ㄥ徃|@鍏徃|@鍏嚎")
cnt = 0; hits = []
if os.path.exists(ledger):
    with open(ledger, encoding="utf-8", errors="replace") as f:
        for i, ln in enumerate(f, 1):
            if pat.search(ln):
                cnt += 1
                hits.append((i, ln.strip()))
lines.append("hit_count=%d" % cnt)
for i, h in hits[-5:]:
    lines.append("L%d: %s" % (i, h[:220]))

# 5) group decisions.md D/C set diff vs watermark
sec("GROUP decisions.md D/C set diff")
dec = os.path.join(GROUP, "docs", "decisions.md")
dpat = re.compile(r"[DC]-\d{8}-\d{2}")
cur = set()
if os.path.exists(dec):
    with open(dec, encoding="utf-8", errors="replace") as f:
        cur = set(dpat.findall(f.read()))
new = sorted(cur - dnums)
gone = sorted(dnums - cur)
lines.append("current_set=%d watermark=%d new=%d gone=%d" % (len(cur), len(dnums), len(new), len(gone)))
for n_ in new:
    lines.append("NEW: " + n_)
for g_ in gone:
    lines.append("GONE(watermark stale): " + g_)

# 6) group orders.md mtime (CEO pending-physical section anchor)
sec("GROUP orders.md mtime")
gorders = os.path.join(GROUP, "docs", "orders.md")
if os.path.exists(gorders):
    lines.append("mtime=%s" % datetime.datetime.fromtimestamp(os.path.getmtime(gorders)).strftime("%Y-%m-%d %H:%M:%S"))

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("written %s, %d lines" % (OUT, len(lines)))

