# -*- coding: utf-8 -*-
import io, os, re
ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = []

# 1. finished.md CENSUS + LC rows
with io.open(os.path.join(ROOT, "output/finished.md"), encoding="utf-8") as f:
    fin = f.readlines()
out.append("=== finished.md CENSUS/LC rows (F-num | title line) ===")
for l in fin:
    if "CENSUS" in l or ("LC" in l and ("lc-0" in l or "LC-0" in l)):
        out.append(l.rstrip()[:260])

# 2. cards README census section tail
with io.open(os.path.join(ROOT, "data/storylines/cards/README.md"), encoding="utf-8") as f:
    cr = f.readlines()
out.append("=== cards README head 12 lines ===")
out.extend([l.rstrip()[:200] for l in cr[:12]])
out.append("=== cards README census-ish rows (last 60) ===")
census_rows = [l for l in cr if "CENSUS" in l or "图鉴" in l]
out.extend([l.rstrip()[:230] for l in census_rows[-60:]])

# 3. release-schedule (pool state)
with io.open(os.path.join(ROOT, "docs/release-schedule-v1.md"), encoding="utf-8") as f:
    rs = f.readlines()
out.append("=== release-schedule (last 45 lines) ===")
out.extend([l.rstrip()[:230] for l in rs[-45:]])

# 4. BS-007 references
out.append("=== BS-007 references in repo (grep docs+data+src) ===")
for base in ["docs", "data", "src", "output"]:
    for dirpath, dirs, files in os.walk(os.path.join(ROOT, base)):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("__pycache__",)]
        for fn in files:
            if fn.endswith((".md", ".json", ".txt", ".py")):
                fp = os.path.join(dirpath, fn)
                try:
                    with io.open(fp, encoding="utf-8", errors="replace") as f:
                        for n, l in enumerate(f, 1):
                            if "BS-007" in l:
                                out.append("%s:%d %s" % (fp.replace(ROOT + os.sep, ""), n, l.strip()[:200]))
                                break
                except Exception:
                    pass

with io.open(os.path.join(ROOT, ".c3-tmp/r696_select.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("DUMP_DONE lines=%d" % len(out))
