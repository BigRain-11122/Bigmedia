r"""Check LC-019 completion status in ledgers and on disk. ASCII code; UTF-8 data out."""
import os, re, glob, json

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r1194_lc019_status.txt")
out = []

# 1. lc019 source dir
d = os.path.join(ROOT, "data", "sources", "lc019")
if os.path.isdir(d):
    out.append("lc019_dir files: " + ", ".join(sorted(os.listdir(d))))
else:
    out.append("lc019_dir MISSING")

# 2. tmp dir
for t in [".lc019-tmp"]:
    p = os.path.join(ROOT, t)
    out.append("%s exists=%s" % (t, os.path.isdir(p)))
    if os.path.isdir(p):
        out.append("  files: " + ", ".join(sorted(os.listdir(p))[:20]))

# 3. renders output for lc-019
for pat in ["output/renders/*lc-019*", "output/renders/*lc019*"]:
    hits = glob.glob(os.path.join(ROOT, pat.replace("/", os.sep)))
    out.append("renders glob %s -> %s" % (pat, [os.path.basename(h) for h in hits]))

# 4. finished.md tail (last 60 lines) + LC-019 mentions
with open(os.path.join(ROOT, "output", "finished.md"), encoding="utf-8") as f:
    fm = f.read()
out.append("finished.md LC-019 mentions: %d" % len(re.findall(r"LC-019|lc-019", fm)))
m = re.findall(r"F-0\d\d[^\n]{0,80}", fm)
out.append("finished last F-numbers: " + " | ".join(x[:60] for x in m[-12:]))

# 5. queue burn record tail
with open(os.path.join(ROOT, "docs", "self-improvement-queue.md"), encoding="utf-8") as f:
    q = f.read()
idx = q.find("## burn")
burn = q[idx:idx+4000] if idx >= 0 else ""
out.append("---- burn head ----")
out.append(burn[:3500])

with open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("OK")
