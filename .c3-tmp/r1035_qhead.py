import os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = os.path.join(ROOT, "r1035_qhead.txt")
L = []

q = os.path.join(ROOT, "docs", "self-improvement-queue.md")
with open(q, encoding="utf-8") as f:
    lines = f.read().splitlines()
L.append("== queue head 130 ==")
L.extend(lines[:130])

b = os.path.join(ROOT, "src", "os", "backlog.md")
with open(b, encoding="utf-8") as f:
    blines = f.read().splitlines()
L.append("")
L.append("== backlog lines 234-431 (new items) ==")
L.extend(blines[233:])

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L))
print("OK q=%d b=%d" % (len(lines), len(blines)))
