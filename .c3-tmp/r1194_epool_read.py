r"""Extract queue E-pool section + burn records + selected state log entries. ASCII code; UTF-8 data out."""
import os, json, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r1194_epool.txt")
out = []

with open(os.path.join(ROOT, "docs", "self-improvement-queue.md"), encoding="utf-8") as f:
    qlines = f.read().splitlines()

# E-pool section: from '## E' heading to '## burn' heading (or end), print all lines
in_e = False
for i, l in enumerate(qlines):
    if l.startswith("## E"):
        in_e = True
    elif l.startswith("## ") and in_e:
        out.append("---- SECTION END at L%04d: %s" % (i + 1, l[:60]))
        break
    if in_e and l.strip():
        out.append("L%04d %s" % (i + 1, l[:300]))

with open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
log = st.get("log", [])
out.append("")
out.append("==== STATE LOG SELECTED ====")
want = ["R1095", "R1160", "R1179", "R1180", "R1178", "R1177", "R1176", "R1175", "R1174", "R1173", "R1172", "R1171", "R1170", "R1169", "R1168", "R1167", "R1166", "R1165", "R1164", "R1163", "R1162", "R1161"]
for e in log:
    for w in want:
        if w + ":" in e[:20] or re.search(r"\b" + w + r"\b", e[:30]):
            out.append(">>> " + e[:1200])
            break

with open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("WROTE %d lines" % len(out))
