# R352 idle-fast fast-path check: five-quiet + anchors + storylines + group anchors
# ASCII-only stdout per encoding law (console GBK garbling)
import os, re, io
from datetime import datetime

GR = r"C:\Users\sjs20\Desktop\FluxGroup"
BR = os.path.join(GR, "media", "BigStream")

print("now", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# 1. git index.lock
print("index_lock", os.path.exists(os.path.join(BR, ".git", "index.lock")))

# 2. group ledger @-four-mode token count (anchor 21)
led = os.path.join(GR, "cph4", "evolution-ledger.md")
pat = re.compile("@BigStream|@七线全司|@全司|@六司")
with io.open(led, encoding="utf-8") as f:
    hits = [l for l in f.read().splitlines() if pat.search(l)]
print("ledger_hits", len(hits))

# 3. group decisions non-empty lines (anchor 33, tail D-20260926-04)
dec = os.path.join(GR, "docs", "decisions.md")
with io.open(dec, encoding="utf-8") as f:
    dl = [l for l in f.read().splitlines() if l.strip()]
ids = [m for l in dl for m in re.findall(r"D-20260\d{3}-\d+", l)]
print("decisions_lines", len(dl), "last_decision", ids[-1] if ids else "none")

# 4. BigLife census anchors supply gate (canonical position only)
anch = os.path.join(GR, "life", "BigLife", "census", "anchors")
print("anchor_C00030", os.path.exists(os.path.join(anch, "C-00030.md")))
print("anchor_C00031", os.path.exists(os.path.join(anch, "C-00031.md")))
try:
    names = sorted(os.listdir(anch))
    print("anchors_count", len(names), "tail", names[-2:])
except Exception as e:
    print("anchors_err", type(e).__name__)

# 5. storylines novel/audio/comic new files since 09-26 00:00 local (ch.5 v3 signal, bm-a domain)
thr = datetime(2026, 9, 26, 0, 0, 0).timestamp()
sl = os.path.join(BR, "data", "storylines")
newf = []
for sub in ("novel", "audio", "comic"):
    p = os.path.join(sl, sub)
    if not os.path.isdir(p):
        print("storylines_missing", sub)
        continue
    for root, dirs, files in os.walk(p):
        for fn in files:
            fp = os.path.join(root, fn)
            try:
                mt = os.path.getmtime(fp)
            except OSError:
                continue
            if mt >= thr:
                newf.append("%s/%s|%s" % (sub, fn, datetime.fromtimestamp(mt).strftime("%H:%M")))
print("storylines_new_since_0926", len(newf))
for x in newf[:10]:
    print("  new", x.encode("unicode_escape").decode("ascii", "backslashreplace"))

# 6. daily report (one-per-day truth) + W39 audit + benchmarks freshness
dr = os.path.join(BR, "data", "intel", "daily", "2026-09-26.md")
print("daily_20260926", os.path.exists(dr),
      datetime.fromtimestamp(os.path.getmtime(dr)).strftime("%m-%d %H:%M") if os.path.exists(dr) else "-")
print("audit_W39", os.path.exists(os.path.join(BR, "docs", "audits", "2026-W39-self-audit.md")))
gb = os.path.join(BR, "docs", "global-benchmarks.md")
with io.open(gb, encoding="utf-8") as f:
    gtxt = f.read()
i = gtxt.find("更新记录")
seg = gtxt[i:i + 400] if i >= 0 else ""
ds = re.findall(r"2026-\d{2}-\d{2}", seg)
if ds:
    d0 = datetime.strptime(ds[0], "%Y-%m-%d")
    print("benchmarks_last_update", ds[0], "age_days", (datetime.now() - d0).days)
else:
    print("benchmarks_last_update", "none")
