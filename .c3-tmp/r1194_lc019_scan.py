r"""Find LC-019 completion status and LC lane stop decision. ASCII code; UTF-8 data out."""
import os, json, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r1194_lc019.txt")
out = []

with open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
log = st.get("log", [])

pat = re.compile(r"LC-019|lc019|lc-019|E20|拆条|E16")
seen = 0
for i, e in enumerate(log):
    if pat.search(e):
        out.append("IDX%04d %s" % (i, e[:900]))
        seen += 1
    if seen > 40:
        break

with open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n\n".join(out))
print("MATCHED %d entries" % seen)
