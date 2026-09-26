# -*- coding: utf-8 -*-
# R356 idle-fast five-check script (ASCII source; CJK tokens via \u escapes)
import os, re, time

def p(x):
    print(x)

p("now=" + time.strftime("%Y-%m-%d %H:%M:%S"))

# 1 orders latest filename (recorded anchor: O-20260925-1931-HQ-C)
fs = sorted(os.listdir("orders"))
p("orders_latest=" + (fs[-1] if fs else "NONE"))

# 2 group ledger four-mode line count (anchor 21)
ledger = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
toks = ["@BigStream", "@\u4e03\u7ebf\u5168\u53f8", "@\u5168\u53f8", "@\u516d\u53f8"]
n = 0
if os.path.exists(ledger):
    with open(ledger, encoding="utf-8", errors="replace") as f:
        for line in f:
            if any(t in line for t in toks):
                n += 1
p("ledger_four_mode_lines=" + str(n))

# 3 group decisions non-empty count + tail D-id (anchor 33 / D-20260926-04)
dec = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
c = 0
tail = ""
with open(dec, encoding="utf-8", errors="replace") as f:
    for line in f:
        if line.strip():
            c += 1
            m = re.findall(r"D-\d{8}-\d+", line)
            if m:
                tail = m[-1]
p("dec_nonempty=" + str(c))
p("dec_tail=" + tail)

# 4 storylines new writes since 2026-09-26 00:00 +08 (epoch thr 1790352000)
thr = 1790352000
for sub in ("novel", "audio", "comic"):
    base = os.path.join("data", "storylines", sub)
    k = 0
    lp = ""
    lt = 0.0
    if os.path.isdir(base):
        for root, dirs, files in os.walk(base):
            for fn in files:
                fp = os.path.join(root, fn)
                try:
                    mt = os.path.getmtime(fp)
                except OSError:
                    continue
                if mt >= thr:
                    k += 1
                if mt > lt:
                    lt = mt
                    lp = fp
    tag = time.strftime("%m-%d %H:%M", time.localtime(lt)) if lp else "-"
    p("story_%s new=%d latest=%s@%s" % (sub, k, lp, tag))

# 5 census anchors canonical position: C-00030 / C-00031
adirs = []
for base in ("data", "research"):
    for root, dirs, files in os.walk(base):
        for d in list(dirs):
            if d == "anchors":
                adirs.append(os.path.join(root, d))
f30 = []
f31 = []
tailnames = []
for d in adirs:
    for fn in sorted(os.listdir(d)):
        full = os.path.join(d, fn)
        if os.path.isfile(full):
            tailnames.append(fn)
            if "C-00030" in fn:
                f30.append(fn)
            if "C-00031" in fn:
                f31.append(fn)
p("anchor_dirs=" + (str(len(adirs)) + " " + "|".join(adirs) if adirs else "NONE"))
p("anchor_tail=" + (",".join(tailnames[-3:]) if tailnames else "empty"))
p("C-00030=" + ("FOUND " + ",".join(f30) if f30 else "absent"))
p("C-00031=" + ("FOUND" if f31 else "absent"))

# 6 daily report 2026-09-26
p("daily_0926=" + ("in-place" if os.path.exists(os.path.join("data", "intel", "daily", "2026-09-26.md")) else "MISSING"))

# 7 index.lock
p("index_lock=" + ("yes" if os.path.exists(os.path.join(".git", "index.lock")) else "no"))

# 8 W39 self-audit
p("w39_audit=" + ("in-place" if os.path.exists(os.path.join("docs", "audits", "2026-W39-self-audit.md")) else "MISSING"))
