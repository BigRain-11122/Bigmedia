# r579 five-check probe (idle-fast path) - content addressing per R533+ precedent
# anchors per R578 focus: orders 35 [O-20260927-1050 13:53:11] / ledger five-mode 30 [00:10:41] / decisions 63 [00:10:41]
import io, os, json, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r579_check.txt")

def mtime(p):
    try:
        return datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "MISSING"

lines = []

# 1. orders anchor (O-files only; README excluded per R576 known-delta rule)
orders_dir = os.path.join(ROOT, "orders")
ofiles = [f for f in os.listdir(orders_dir) if f.endswith(".md")]
o_files = sorted([f for f in ofiles if f.startswith("O-")], key=lambda f: os.path.getmtime(os.path.join(orders_dir, f)))
lines.append("ORDERS O-files=%d all-md=%d latest=%s mtime=%s (anchor 35 / O-20260927-1050-HQ-C 13:53:11)" % (
    len(o_files), len(ofiles), o_files[-1], mtime(os.path.join(orders_dir, o_files[-1]))))

# 2. ledger five-mode raw-line regex count (unicode-escape per R533 law)
LEDGER = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
tags = ["\u0040BigStream", "\u0040\u4e03\u7ebf\u5168\u53f8", "\u0040\u5168\u53f8", "\u0040\u516d\u53f8"]
cnt = 0
with io.open(LEDGER, "r", encoding="utf-8", errors="replace") as f:
    for line in f:
        if any(t in line for t in tags):
            cnt += 1
lines.append("LEDGER five-mode lines=%d mtime=%s (anchor 30 / 00:10:41)" % (cnt, mtime(LEDGER)))

# 3. decisions non-empty UTF8 lines
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
with io.open(DEC, "r", encoding="utf-8", errors="replace") as f:
    dcnt = sum(1 for l in f if l.strip())
lines.append("DECISIONS nonempty=%d mtime=%s (anchor 63 / 00:10:41)" % (dcnt, mtime(DEC)))

# 4. state production + tick
with io.open(os.path.join(ROOT, "src", "os", "state.json"), "r", encoding="utf-8") as f:
    st = json.load(f)
lines.append("STATE production=%s tick=%d" % (st.get("production"), st.get("tick")))

# 5. locks
lines.append("INDEX_LOCK exists=%s" % os.path.exists(os.path.join(ROOT, ".git", "index.lock")))

# 6. due-day artifacts
lines.append("DAILY_0928=%s mtime=%s" % (os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-09-28.md")), mtime(os.path.join(ROOT, "data", "intel", "daily", "2026-09-28.md"))))
aud_w40 = os.path.join(ROOT, "docs", "audits", "2026-W40-self-audit.md")
lines.append("AUDIT_W40=%s mtime=%s" % (os.path.exists(aud_w40), mtime(aud_w40)))

# 7. key footprints (bm-a activity signals)
for rel in ["src/os/backlog.md", "HQ-FEEDBACK.md", "docs/reviews/station-reviews.md", "output/renders/README.md", "output/finished.md", "output/cards/README.md", "docs/status-export.json", "data/storylines/novel", "data/storylines/audio", "data/storylines/comic"]:
    p = os.path.join(ROOT, rel)
    if os.path.isdir(p):
        fl = os.listdir(p)
        latest = max(fl, key=lambda f: os.path.getmtime(os.path.join(p, f))) if fl else "-"
        lines.append("FP-DIR %s latest=%s mtime=%s" % (rel, latest, mtime(os.path.join(p, latest)) if fl else "-"))
    else:
        lines.append("FP %s mtime=%s" % (rel, mtime(p)))

# 8. backlog top line
with io.open(os.path.join(ROOT, "src", "os", "backlog.md"), "r", encoding="utf-8") as f:
    bl = [l.rstrip("\n") for l in f]
nonempty = [l for l in bl if l.strip()]
lines.append("BACKLOG top5:")
for l in nonempty[:5]:
    lines.append("  " + l[:160])

with io.open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("OK")
