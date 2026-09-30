# -*- coding: utf-8 -*-
# R684 fix: renders README source-name extension trap (R21/R147/R512 precedent: no-extension form on stale-scan surface)
import io, os, subprocess

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".c3-tmp")
p = os.path.join(ROOT, "output", "renders", "README.md")
rr = io.open(p, encoding="utf-8").read()
OLD = u"data/sources/footage/census-card-v13-vertical.mp4`（R684·F-032 成品卡 PNG 派生"
NEW = u"data/sources/footage/census-card-v13-vertical`（R684·F-032 成品卡 PNG 派生"
assert OLD in rr, "target not found"
rr = rr.replace(OLD, NEW, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(rr)

# re-run readiness to confirm single expected finding
env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"
r = subprocess.run(["python", "src/readiness.py"], cwd=ROOT, env=env, capture_output=True)
txt = r.stdout.decode("utf-8", "replace")
io.open(os.path.join(TMP, "r684_readiness3.txt"), "w", encoding="utf-8").write(txt)
last = [l for l in txt.splitlines() if l.strip()][-1]
io.open(os.path.join(TMP, "r684_findings2.txt"), "w", encoding="utf-8").write(
    "\n".join(l for l in txt.splitlines() if "render-" in l or "readiness:" in l))
print("fixed; readiness exit=%d last=%s" % (r.returncode, last))
