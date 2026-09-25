import os, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
FG = r"C:\Users\sjs20\Desktop\FluxGroup"

def say(k):
    print(k, flush=True)

# 5. ledger four-mode count
led = os.path.join(FG, "cph4", "evolution-ledger.md")
with open(led, encoding="utf-8", errors="replace") as f:
    llines = f.readlines()
tok = ("@BigStream", "@\u4e03\u7ebf\u5168\u53f8", "@\u5168\u53f8", "@\u516d\u53f8")
cnt = sum(1 for l in llines if any(t in l for t in tok))
say("LEDGER_4MODE_LINES: %d (anchor=21)" % cnt)

# 6. decisions non-empty count
dec = os.path.join(FG, "docs", "decisions.md")
with open(dec, encoding="utf-8") as f:
    dlines = f.readlines()
say("DECISIONS_NONEMPTY: %d (anchor=33)" % sum(1 for l in dlines if l.strip()))

# 7. index.lock
say("INDEX_LOCK: %s" % os.path.exists(os.path.join(ROOT, ".git", "index.lock")))

# 8. daily today
say("DAILY_0926: %s" % os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-09-26.md")))

# 9. recent writes under docs/data/src (bm-a sign check)
cand = []
for sub in ("docs", "data", "src"):
    for dp, dn, fn in os.walk(os.path.join(ROOT, sub)):
        dn[:] = [x for x in dn if x != "__pycache__"]
        for f in fn:
            p = os.path.join(dp, f)
            cand.append((os.path.getmtime(p), p))
cand.sort(reverse=True)
for mt, p in cand[:6]:
    say("RECENT_WRITE: %s %s" % (datetime.datetime.fromtimestamp(mt).strftime("%m-%d %H:%M:%S"), p.replace(ROOT, "")[:100]))
