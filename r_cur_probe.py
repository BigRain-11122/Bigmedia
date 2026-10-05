# -*- coding: utf-8 -*-
# Quick-judgment probe (zero-token): state tail + group scans + hygiene checks
import json, os, re, glob, io, datetime, subprocess

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GROUP = r"C:\Users\sjs20\Desktop\FluxGroup"
TODAY = "2026-10-05"
out = []
def w(s):
    try:
        out.append(str(s))
    except Exception:
        out.append(repr(s))

def readf(p):
    try:
        return open(p, encoding="utf-8").read()
    except Exception as e:
        return "READ_FAIL: %r" % e

# 1. state.json
w("== state.json ==")
try:
    st = json.load(open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
    w("top-level keys: %s" % sorted(st.keys()))
    for k in ("tick", "ts", "task", "production", "mode"):
        v = st.get(k, "<absent>")
        w("%s: %s" % (k, json.dumps(v, ensure_ascii=False)[:300] if not isinstance(v, str) else v))
    log = st.get("log", [])
    if isinstance(log, list):
        w("log len: %d, tail 3:" % len(log))
        for line in log[-3:]:
            w("  | " + (line if isinstance(line, str) else json.dumps(line, ensure_ascii=False))[:400])
    else:
        w("log (non-list): %s" % json.dumps(log, ensure_ascii=False)[-1500:])
    wm = st.get("decisions_watermark", {})
    w("decisions_watermark: %s" % json.dumps(wm, ensure_ascii=False)[:600])
    wmdnums = set(wm.get("dnums", [])) if isinstance(wm, dict) else set()
except Exception as e:
    w("STATE_FAIL: %r" % e)
    wmdnums = set()

# 2. group decisions.md (content-addressed diff)
dp = os.path.join(GROUP, "docs", "decisions.md")
dec = readf(dp)
nums = set(re.findall(r"[DC]-\d{8}-\d+", dec))
new_nums = sorted(nums - wmdnums)
w("== group decisions.md ==")
w("total D/C: %d | NEW vs watermark: %s" % (len(nums), new_nums if new_nums else "NONE"))
dl = dec.splitlines()
w("-- first 12 lines:")
for l in dl[:12]:
    w("  | " + l[:220])
idx = None
for i, l in enumerate(dl):
    if "派工通告板" in l:
        idx = i
        break
if idx is not None:
    w("-- 派工通告板 block (30 lines from L%d):" % (idx + 1))
    for l in dl[idx:idx + 30]:
        w("  | " + l[:220])
else:
    w("-- 派工通告板 marker NOT FOUND")

# 3. evolution-ledger @scan
ep = os.path.join(GROUP, "cph4", "evolution-ledger.md")
ev = readf(ep)
evl = ev.splitlines()
pat = re.compile(r"@BigStream|@七线全司|@全司|@六司")
hits = [(i + 1, l) for i, l in enumerate(evl) if pat.search(l)]
w("== evolution-ledger @hits: %d, last 12:" % len(hits))
for n, l in hits[-12:]:
    w("  L%d: %s" % (n, l[:220]))

# 4. group orders.md (CEO physical items + BigStream lines)
op = os.path.join(GROUP, "docs", "orders.md")
ot = readf(op)
ol = ot.splitlines()
w("== group orders.md: first 10 lines:")
for l in ol[:10]:
    w("  | " + l[:220])
bm_hits = [(i + 1, l) for i, l in enumerate(ol) if "BigStream" in l or "账号" in l or "商户" in l]
w("-- BigStream/physical lines: %d, last 8:" % len(bm_hits))
for n, l in bm_hits[-8:]:
    w("  L%d: %s" % (n, l[:220]))

# 5. local orders/ newest
orders = [p for p in glob.glob(os.path.join(ROOT, "orders", "*")) if os.path.isfile(p)]
orders.sort(key=os.path.getmtime, reverse=True)
w("== local orders/ newest 5:")
for p in orders[:5]:
    w("  %s  %s" % (datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M"), os.path.basename(p)))

# 6. git status + lock
g = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True)
w("== git status --short ==")
w(g.stdout.strip() if g.stdout.strip() else "(clean)")
w("index.lock: %s" % os.path.exists(os.path.join(ROOT, ".git", "index.lock")))

# 7. loop dir heartbeat
ld = os.path.join(ROOT, "logs", "iteration-loop")
if os.path.isdir(ld):
    fs = sorted(glob.glob(os.path.join(ld, "*")), key=os.path.getmtime, reverse=True)
    w("== logs/iteration-loop newest 6:")
    for p in fs[:6]:
        w("  %s  %s" % (datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M"), os.path.basename(p)))

# 8. hygiene: intel daily / weekly audit / benchmarks
w("== hygiene ==")
w("intel daily %s: %s" % (TODAY, os.path.exists(os.path.join(ROOT, "data", "intel", "daily", TODAY + ".md"))))
iso = datetime.date(2026, 10, 5).isocalendar()
wk = "%d-W%02d" % (iso[0], iso[1])
w("ISO week: %s | audit file exists: %s" % (wk, os.path.exists(os.path.join(ROOT, "docs", "audits", wk + "-self-audit.md"))))
gb = readf(os.path.join(ROOT, "docs", "global-benchmarks.md"))
m = re.search(r"更新记录", gb)
if m:
    seg = gb[m.end():m.end() + 400]
    d = re.search(r"2026-\d{2}-\d{2}", seg)
    w("global-benchmarks §4 last-update date: %s" % (d.group(0) if d else "NOT FOUND"))
else:
    w("global-benchmarks 更新记录 marker: NOT FOUND")

# 9. backlog + self-improvement queue tops
for name, rel in (("backlog", os.path.join("src", "os", "backlog.md")),
                  ("self-improvement-queue", os.path.join("docs", "self-improvement-queue.md"))):
    t = readf(os.path.join(ROOT, rel))
    w("== %s top 14 lines ==" % name)
    for l in t.splitlines()[:14]:
        w("  | " + l[:220])

open(os.path.join(ROOT, "r_cur_probe_out.txt"), "w", encoding="utf-8").write("\n".join(out))
print("PROBE_OK")
