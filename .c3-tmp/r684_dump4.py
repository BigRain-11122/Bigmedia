# -*- coding: utf-8 -*-
# R684: dump queue section E rows
import io, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".c3-tmp")
q = os.path.join(ROOT, "docs", "self-improvement-queue.md")
lines = io.open(q, encoding="utf-8").read().splitlines()
out = []
inE = False
for i, l in enumerate(lines):
    if "E1" in l and ("LC-003" in l or "何雨欣" in l or "C-00022" in l):
        out.append("L%d: %s" % (i + 1, l))
io.open(os.path.join(TMP, "r684_queue_e1.txt"), "w", encoding="utf-8").write("\n\n".join(out))
print("hits=%d" % len(out))
