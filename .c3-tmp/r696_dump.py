# -*- coding: utf-8 -*-
import io, re, os
ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = []

# backlog head (first 30 lines)
with io.open(os.path.join(ROOT, "src/os/backlog.md"), encoding="utf-8") as f:
    lines = f.readlines()
out.append("=== BACKLOG head (30 lines) ===")
out.extend(lines[:30])
open_ids = []
for i, l in enumerate(lines):
    m = re.match(r"^(\d+)\.", l.strip())
    if m and "[done" not in l[:200]:
        open_ids.append((m.group(1), l[:150].replace("\n", "")))
out.append("=== BACKLOG open items (id + first 150 chars) ===")
for oid, txt in open_ids:
    out.append("#%s %s" % (oid, txt))

# queue file E-pool section
with io.open(os.path.join(ROOT, "docs/self-improvement-queue.md"), encoding="utf-8") as f:
    ql = f.readlines()
out.append("=== QUEUE E-pool matches ===")
for n, l in enumerate(ql):
    if ("E" in l and "池" in l) or "lane" in l or "E3" in l or "E4" in l or "E5" in l or "E6" in l or "E7" in l:
        out.append("L%d: %s" % (n + 1, l.rstrip()[:220]))

with io.open(os.path.join(ROOT, ".c3-tmp/r696_board_queue.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("DUMP_DONE")
