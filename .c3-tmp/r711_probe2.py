import json, io, re, os, glob, time
root = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = io.open(os.path.join(root, ".c3-tmp/r711_probe2.txt"), "w", encoding="utf-8")
W = out.write

def tail(path, n=40, cut=240):
    p = os.path.join(root, path)
    if not os.path.exists(p):
        W("[MISSING] %s\n" % path)
        return
    lines = io.open(p, encoding="utf-8", errors="ignore").read().splitlines()
    W("== %s (total %d lines) ==\n" % (path, len(lines)))
    for l in lines[-n:]:
        W((l[:cut] + ("\n" if len(l) > cut else "\n")))

def grep(path, pat, n=20, cut=300):
    p = os.path.join(root, path)
    if not os.path.exists(p):
        W("[MISSING] %s\n" % path)
        return
    hits = [l for l in io.open(p, encoding="utf-8", errors="ignore").read().splitlines() if re.search(pat, l)]
    W("== %s grep %s (%d hits) ==\n" % (path, pat, len(hits)))
    for l in hits[-n:]:
        W(l[:cut] + "\n")

# 1. full R710 state log entry
d = json.load(io.open(os.path.join(root, "src/os/state.json"), encoding="utf-8"))
W("== R710 LOG FULL ==\n")
W(d["log"][-1] + "\n\n")

# 2. tmp dirs listing
for td in [".lc011-tmp", ".lc010-tmp"]:
    p = os.path.join(root, td)
    W("== %s ==\n" % td)
    if os.path.isdir(p):
        for f in sorted(os.listdir(p)):
            fp = os.path.join(p, f)
            W("  %-32s %8d  %s\n" % (f, os.path.getsize(fp), time.strftime("%m-%d %H:%M", time.localtime(os.path.getmtime(fp)))))
    else:
        W("  [missing]\n")

# 3. LC readme locations
W("== glob lc01* README ==\n")
for g in glob.glob(os.path.join(root, "**", "*lc01*"), recursive=True):
    if os.path.isfile(g) and ("README" in g or g.endswith(".md")):
        W(g.replace(root, "") + "\n")

# 4. LC-010 E8 review precedent
tail("docs/reviews/review-20260929-lc010-v1.md", n=80, cut=400)

# 5. finished.md tail
tail("output/finished.md", n=45, cut=280)

# 6. renders README LC rows
grep("output/renders/README.md", r"lc-0|LC-0", n=14, cut=320)

# 7. queue E section
tail("docs/self-improvement-queue.md", n=50, cut=240)

# 8. release-schedule
tail("docs/release-schedule.md", n=50, cut=240)

# 9. station-reviews tail
tail("docs/reviews/station-reviews.md", n=10, cut=380)

# 10. cards README tail (DIGEST-v10 / REACT-v5 E4 backfill status)
tail("data/storylines/cards/README.md", n=26, cut=300)

# 11. E4 backfill check in review files
grep("docs/reviews/review-20260929-mcdigest-v10.md", r"E4|回填|参考仪", n=10, cut=300)
grep("docs/reviews/review-20260929-mcreact-v5.md", r"E4|回填|参考仪", n=10, cut=300)
out.close()
print("written")
