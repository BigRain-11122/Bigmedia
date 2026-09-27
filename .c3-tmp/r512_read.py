# r512_read.py - dump ledger slices needed for LC-001 closeout
import os, io, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = os.path.join(ROOT, ".c3-tmp", "r512-read.md")
lines = []
def w(s=""):
    lines.append(str(s))

def dump_tail(path, n, label):
    w("## %s" % label)
    if not os.path.exists(path):
        w("  NOT FOUND: %s" % path)
        return
    with io.open(path, "r", encoding="utf-8", errors="replace") as fh:
        all_l = fh.read().splitlines()
    w("(total %d lines)" % len(all_l))
    for s in all_l[-n:]:
        w(s[:260])

def main():
    # 1. finished.md tail (F-047 block format)
    dump_tail(os.path.join(ROOT, "output", "finished.md"), 55, "finished_tail55")

    # 2. release-schedule D15 region
    w("## release_schedule_D15_region")
    rs = os.path.join(ROOT, "docs", "release-schedule-v1.md")
    with io.open(rs, "r", encoding="utf-8", errors="replace") as fh:
        rl = fh.read().splitlines()
    for i, s in enumerate(rl, 1):
        if ("D15" in s) or ("D18" in s and i < 200) or ("五-1" in s) or ("§五" in s):
            w("L%d: %s" % (i, s[:260]))

    # 3. station-reviews tail
    dump_tail(os.path.join(ROOT, "docs", "reviews", "station-reviews.md"), 18, "station_reviews_tail18")

    # 4. renders README L84-92 (lc-001 rows)
    w("## renders_readme_L84_96")
    with io.open(os.path.join(ROOT, "output", "renders", "README.md"), "r", encoding="utf-8", errors="replace") as fh:
        rr = fh.read().splitlines()
    for i in range(83, min(97, len(rr))):
        w("L%d: %s" % (i + 1, rr[i][:300]))

    # 5. lc001 README
    dump_tail(os.path.join(ROOT, "data", "sources", "lc001", "README.md"), 40, "lc001_readme_tail40")

    # 6. .lc001-tmp listing
    w("## lc001_tmp_listing")
    lt = os.path.join(ROOT, ".lc001-tmp")
    for f in sorted(os.listdir(lt)):
        p = os.path.join(lt, f)
        w("  %s %d bytes" % (f, os.path.getsize(p)))

    # 7. plan.json visual rows (source refs)
    w("## lc001_plan_sources")
    pj = os.path.join(ROOT, "output", "renders", "lc-001-v1-shipinhao-60s.mp4.plan.json")
    if not os.path.exists(pj):
        pj = os.path.join(lt, "lc-001-v1-shipinhao-60s.plan.json")
    if os.path.exists(pj):
        w("plan at %s" % pj)
        with io.open(pj, "r", encoding="utf-8", errors="replace") as fh:
            plan = fh.read()
    else:
        plan = ""
        w("plan.json NOT FOUND in renders or tmp")
        # list plan files in renders
        for f in sorted(os.listdir(os.path.join(ROOT, "output", "renders"))):
            if "plan" in f and "lc-001" in f:
                w("  found: %s" % f)
    for m in re.finditer(r'"src[^"]*"\s*:\s*"([^"]+)"', plan):
        w("  src: %s" % m.group(1)[:160])
    # any mention of census-card
    for m in re.finditer(r'[^"]*census[^"]*', plan):
        w("  census-ref: %s" % m.group(0)[:200])

    # 8. latest review cards list
    w("## reviews_dir_latest")
    rd = os.path.join(ROOT, "docs", "reviews")
    revs = sorted([f for f in os.listdir(rd) if f.startswith("review-")])
    for f in revs[-8:]:
        w("  %s" % f)

    # 9. backlog #77/#78/#79 rows
    w("## backlog_77_78_79")
    with io.open(os.path.join(ROOT, "src", "os", "backlog.md"), "r", encoding="utf-8", errors="replace") as fh:
        bl = fh.read().splitlines()
    for i, s in enumerate(bl, 1):
        if re.match(r"^(77|78|79)\.", s.strip()):
            # print this row + following 6 lines
            for j in range(i - 1, min(i + 5, len(bl))):
                w("L%d: %s" % (j + 1, bl[j][:280]))
            w("  ---")

    with io.open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("OK")

if __name__ == "__main__":
    main()
