# R342 fast-path five checks (read-only, ASCII output)
import os, datetime

BS = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
ANCH = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors"
LEDGER = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"

# 1. CENSUS supply gate: anchors canonical position only (R316 discipline)
for cid in ("C-00030", "C-00031"):
    p = os.path.join(ANCH, cid + ".md")
    print("anchor %s exists=%s" % (cid, os.path.exists(p)))
anch_files = sorted(f for f in os.listdir(ANCH) if f.endswith(".md")) if os.path.isdir(ANCH) else []
print("anchors count=%d tail=%s" % (len(anch_files), anch_files[-2:] if len(anch_files) >= 2 else anch_files))

# 2. Group ledger four-mode line count (anchor 21)
modes = ("@BigStream", "@\u4e03\u7ebf\u5168\u53f8", "@\u5168\u53f8", "@\u516d\u53f8")
with open(LEDGER, encoding="utf-8", errors="replace") as f:
    lines = f.read().splitlines()
hits = [ln for ln in lines if any(m in ln for m in modes)]
print("ledger four-mode lines=%d (anchor 21)" % len(hits))

# 3. decisions.md non-empty line count (python non-empty, anchor 33)
with open(DEC, encoding="utf-8", errors="replace") as f:
    dl = [ln for ln in f.read().splitlines() if ln.strip()]
print("decisions non-empty=%d (anchor 33)" % len(dl))
print("decisions tail=%s" % dl[-1][:60] if dl else "decisions EMPTY")

# 4. daily report 2026-09-26 in place (no rerun if present)
print("daily 09-26 exists=%s" % os.path.exists(os.path.join(BS, "data", "intel", "daily", "2026-09-26.md")))

# 5. index.lock
print("index.lock exists=%s" % os.path.exists(os.path.join(BS, ".git", "index.lock")))

# 6. bm-a storyline landing probe: any file in storylines written since 09-26 00:00
cut = datetime.datetime(2026, 9, 26, 0, 0, 0)
fresh = []
for sub in ("novel", "audio", "comic"):
    d = os.path.join(BS, "data", "storylines", sub)
    if not os.path.isdir(d):
        continue
    for root, _dirs, files in os.walk(d):
        for fn in files:
            p = os.path.join(root, fn)
            try:
                mt = datetime.datetime.fromtimestamp(os.path.getmtime(p))
            except OSError:
                continue
            if mt >= cut:
                fresh.append("%s\\%s %s" % (sub, fn, mt.strftime("%m-%d %H:%M")))
print("storylines files written since 09-26 00:00 = %d" % len(fresh))
for s in fresh[:10]:
    print("  FRESH: " + s)

# 7. ch.5 v3 landing check (SC-001-05-v3 / ch.6)
for sub in ("novel", "audio", "comic"):
    d = os.path.join(BS, "data", "storylines", sub)
    names = sorted(os.listdir(d)) if os.path.isdir(d) else []
    print("%s dir tail=%s" % (sub, names[-3:] if len(names) >= 3 else names))

# 8. W39 audit + global-benchmarks freshness (skip conditions)
print("W39 audit exists=%s" % os.path.exists(os.path.join(BS, "docs", "audits", "2026-W39-self-audit.md")))
with open(os.path.join(BS, "docs", "global-benchmarks.md"), encoding="utf-8", errors="replace") as f:
    gb = f.read()
print("global-benchmarks has 2026-09-24=%s (day2 <=7 skip)" % ("2026-09-24" in gb))

print("CHECK-DONE")
