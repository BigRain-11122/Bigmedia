r"""Find R746-R755 logs + LC-019 closeout + E20/xugenfu status. ASCII code; UTF-8 data out."""
import os, json, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r1194_r746_752.txt")
out = []

with open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
log = st.get("log", [])

pat = re.compile(r"\bR7(4[6-9]|5[0-5]):")
for i, e in enumerate(log):
    m = re.match(r"2026-\d\d-\d\d [\d:.x]+ R(\d+):", e)
    if m and 746 <= int(m.group(1)) <= 755:
        out.append("IDX%04d %s" % (i, e[:1400]))
        out.append("")

with open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("WROTE %d" % (len(out)//2))
