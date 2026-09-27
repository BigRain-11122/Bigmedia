# r576 five-check probe (idle-fast path) - content addressing per R533+ precedent
import io, os, re, json, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r576_check.txt")

def mtime(p):
    try:
        return datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "MISSING"

lines = []

# 1. orders anchor
orders_dir = os.path.join(ROOT, "orders")
ofiles = [f for f in os.listdir(orders_dir) if f.endswith(".md")]
ofiles.sort(key=lambda f: os.path.getmtime(os.path.join(orders_dir, f)))
lines.append("ORDERS count=%d latest=%s mtime=%s" % (len(ofiles), ofiles[-1], mtime(os.path.join(orders_dir, ofiles[-1]))))

# 2. ledger five-mode raw-line regex count (unicode-escape per R533 law)
LEDGER = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
tags = ["\u0040BigStream", "\u0040\u4e03\u7ebf\u5168\u53f8", "\u0040\u5168\u53f8", "\u0040\u516d\u53f8"]
cnt = 0
with io.open(LEDGER, "r", encoding="utf-8", errors="replace") as f:
    for line in f:
        if any(t in line for t in tags):
            cnt += 1
lines.append("LEDGER five-mode lines=%d mtime=%s (anchor 31 / 15:15:21)" % (cnt, mtime(LEDGER)))

# 3. decisions non-empty UTF8 lines
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
with io.open(DEC, "r", encoding="utf-8", errors="replace") as f:
    dcnt = sum(1 for l in f if l.strip())
lines.append("DECISIONS nonempty=%d mtime=%s (anchor 56 / 15:14:19)" % (dcnt, mtime(DEC)))

# 4. state production + tick
with io.open(os.path.join(ROOT, "src", "os", "state.json"), "r", encoding="utf-8") as f:
    st = json.load(f)
lines.append("STATE production=%s tick=%d" % (st.get("production"), st.get("tick")))

# 5. locks + tree signals
lines.append("INDEX_LOCK exists=%s" % os.path.exists(os.path.join(ROOT, ".git", "index.lock")))

# 6. due-day artifacts
lines.append("DAILY_0928=%s mtime=%s" % (os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-09-28.md")), mtime(os.path.join(ROOT, "data", "intel", "daily", "2026-09-28.md"))))
aud_w40 = os.path.join(ROOT, "docs", "audits", "2026-W40-self-audit.md")
lines.append("AUDIT_W40=%s mtime=%s" % (os.path.exists(aud_w40), mtime(aud_w40)))
# any audit files
auds = os.listdir(os.path.join(ROOT, "docs", "audits"))
lines.append("AUDIT dir files=%s" % sorted(auds))
# self_audit data pack dir?
for cand in ["output", "docs"]:
    pass
# key footprints
for rel in ["src/os/backlog.md", "HQ-FEEDBACK.md", "docs/reviews/station-reviews.md", "output/renders/README.md", "output/finished.md", "output/cards/README.md", "docs/status-export.json"]:
    lines.append("FP %s mtime=%s" % (rel, mtime(os.path.join(ROOT, rel))))

# storylines footprints
for sub in ["video", "novel", "audio", "comic"]:
    d = os.path.join(ROOT, "data", "storylines", sub)
    if os.path.isdir(d):
        fl = sorted(os.listdir(d))
        latest = max(fl, key=lambda f: os.path.getmtime(os.path.join(d, f))) if fl else "-"
        lines.append("STORY %s latest=%s mtime=%s" % (sub, latest, mtime(os.path.join(d, latest)) if fl else "-"))

with io.open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("OK")
