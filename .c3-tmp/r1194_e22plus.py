r"""Check E22-E33 queue entries + LC-021 closeout. ASCII code; UTF-8 data out."""
import os, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r1194_e22plus.txt")
out = []

with open(os.path.join(ROOT, "docs", "self-improvement-queue.md"), encoding="utf-8") as f:
    q = f.read()

for tag in ["E22", "E23", "E24", "E25", "E26", "E27", "E28", "E29", "E32", "E33", "E34"]:
    for m in re.finditer(r"[-*]\s+\*\*%s\b[^\n]{0,240}" % tag, q):
        out.append("HIT %s: %s" % (tag, m.group(0)[:260]))
    for m in re.finditer(r"^.*%s[^\n]{0,160}" % tag, q.split("## burn", 1)[-1], re.M):
        s = m.group(0).strip()
        if "**" in s and not s.startswith("HIT"):
            out.append("BURN %s: %s" % (tag, s[:260]))

with open(os.path.join(ROOT, "output", "finished.md"), encoding="utf-8") as f:
    fm = f.read()
for m in re.finditer(r"F-07[45][^\n]{0,110}", fm):
    out.append("FIN: " + m.group(0)[:130])
out.append("LC-021 in finished: %d hits" % len(re.findall(r"LC-021|lc-021", fm)))

with open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("WROTE %d" % len(out))
