# R351 quick-path five-check probe (ASCII output only)
import os, glob, time

R = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(R, ".."))

def p(rel):
    return os.path.join(ROOT, rel)

res = {}

# 2) backlog-top supply gate: CENSUS anchors canonical slot C-00030/C-00031
ANCHORS = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors"
res["anchors_exists_dir"] = os.path.isdir(ANCHORS)
a30 = os.path.join(ANCHORS, "C-00030.md")
a31 = os.path.join(ANCHORS, "C-00031.md")
res["C-00030"] = os.path.exists(a30)
res["C-00031"] = os.path.exists(a31)
try:
    names = sorted(os.listdir(ANCHORS))
    res["anchors_count"] = len(names)
    res["anchors_tail2"] = ",".join(names[-2:])
except Exception as e:
    res["anchors_err"] = str(e)

# 3) index.lock
res["index_lock"] = os.path.exists(p(".git\\index.lock"))

# HEAD
try:
    ref = open(p(".git\\HEAD"), encoding="utf-8").read().strip()
    if ref.startswith("ref:"):
        hp = p(".git\\" + ref[4:].strip().replace("/", "\\"))
        head = open(hp, encoding="utf-8").read().strip()
    else:
        head = ref
    res["HEAD"] = head[:7]
except Exception as e:
    res["HEAD_err"] = str(e)

# 5) group anchors: ledger lines containing four-mode tokens; decisions non-empty lines
LED = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
try:
    tok = ["@BigStream", "@\u4e03\u7ebf\u5168\u53f8", "@\u5168\u53f8", "@\u516d\u53f8"]
    n = 0
    with open(LED, encoding="utf-8", errors="replace") as f:
        for line in f:
            if any(t in line for t in tok):
                n += 1
    res["ledger_lines"] = n  # anchor 21
    res["ledger_mtime"] = time.strftime("%m-%d %H:%M", time.localtime(os.path.getmtime(LED)))
except Exception as e:
    res["ledger_err"] = str(e)
try:
    with open(DEC, encoding="utf-8", errors="replace") as f:
        lines = [l for l in f if l.strip()]
    res["decisions_nonempty"] = len(lines)  # anchor 33
    res["decisions_mtime"] = time.strftime("%m-%d %H:%M", time.localtime(os.path.getmtime(DEC)))
except Exception as e:
    res["decisions_err"] = str(e)

# 4) bm-a face: storylines novel/audio/comic new writes on 09-26 (threshold 2026-09-26 00:00 +08)
TH = 1790352000
SL = p("data\\storylines")
new_writes = []
if os.path.isdir(SL):
    for sub in ["novel", "audio", "comic"]:
        d = os.path.join(SL, sub)
        if not os.path.isdir(d):
            continue
        for dirpath, dirnames, filenames in os.walk(d):
            for fn in filenames:
                fp = os.path.join(dirpath, fn)
                try:
                    if os.path.getmtime(fp) >= TH:
                        new_writes.append(os.path.relpath(fp, ROOT))
                except OSError:
                    pass
res["storylines_new_0926"] = len(new_writes)
if new_writes:
    res["storylines_new_sample"] = ";".join(new_writes[:5])

# daily brief 09-26
res["daily_0926"] = os.path.exists(p("data\\intel\\daily\\2026-09-26.md"))

# orders latest by mtime
try:
    od = p("orders")
    latest = max(glob.glob(os.path.join(od, "*.md")), key=os.path.getmtime)
    res["orders_latest"] = os.path.basename(latest)
except Exception as e:
    res["orders_err"] = str(e)

# W39 self-audit present
res["w39_audit"] = os.path.exists(p("docs\\audits\\2026-W39-self-audit.md"))

for k, v in res.items():
    print(k, "=", v)
