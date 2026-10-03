r"""Extract open (non-done) items from self-improvement-queue tables. ASCII code; UTF-8 data out."""
import os, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r1194_queue_open.txt")
out = []
with open(os.path.join(ROOT, "docs", "self-improvement-queue.md"), encoding="utf-8") as f:
    lines = f.read().splitlines()

cur_section = ""
for i, l in enumerate(lines):
    if l.startswith("## ") or l.startswith("# "):
        cur_section = l.strip()
    if l.strip().startswith("|") and not set(l.strip()) <= {"|", "-", " ", ":"}:
        # table row
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        joined = " | ".join(cells)
        if "done" not in joined and "已完成" not in joined:
            out.append("L%04d [%s] %s" % (i + 1, cur_section[:40], joined[:260]))
    elif re.match(r"^\s*[-*]\s+\*\*[A-Z]?\d+", l) or ("pending" in l.lower() and l.strip().startswith(("-", "*"))):
        if "done" not in l:
            out.append("L%04d [%s] %s" % (i + 1, cur_section[:40], l.strip()[:260]))

with open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("WROTE %d open rows" % len(out))
