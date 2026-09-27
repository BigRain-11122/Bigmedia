import json, os, re

root = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = []

# full last log line
with open(os.path.join(root, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
log = st.get("log", [])
out.append("R516_FULL_LOG:")
out.append(log[-1])
out.append("")

# backlog items 76-80 (first 400 chars of each line)
with open(os.path.join(root, "src", "os", "backlog.md"), encoding="utf-8") as f:
    bl = f.read().splitlines()
out.append(f"backlog_lines={len(bl)}")
for i, l in enumerate(bl):
    if re.match(r"^(7[6-9]|80)\. ", l):
        out.append(f"--- L{i+1}: {l[:600]}")

# decisions canonical count: all non-empty lines
dec = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
with open(dec, encoding="utf-8") as f:
    txt = f.read()
ne = [l for l in txt.splitlines() if l.strip()]
out.append(f"DECISIONS_ALL_NONEMPTY={len(ne)}")
# rows starting with | D- or | C-
rows = [l for l in ne if re.match(r"^\|\s*(D|C)-\d", l)]
out.append(f"DECISION_ROWS={len(rows)}")
for l in rows[-4:]:
    out.append("  R: " + l[:130])

with open(os.path.join(root, ".c3-tmp", "focus_check.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("OK")
