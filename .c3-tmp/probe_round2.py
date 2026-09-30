import json, os, re, glob, subprocess, datetime

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = []
A = out.append

with open(os.path.join(repo, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
logs = st.get("log", [])
for e in logs:
    if "R684:" in e[:26] or "R685:" in e[:26] or "R686:" in e[:26]:
        A("===== " + e[:20] + " =====")
        A(e)

# tmp dirs
for d in sorted(glob.glob(os.path.join(repo, ".lc*-tmp"))):
    A(f"DIR {os.path.basename(d)}:")
    for p in sorted(os.listdir(d)):
        sz = os.path.getsize(os.path.join(d, p))
        A(f"  {p} ({sz})")

# source dirs for lc
for d in sorted(glob.glob(os.path.join(repo, "data", "sources", "*"))):
    b = os.path.basename(d).lower()
    if "lc" in b:
        A(f"SRC {d.replace(repo, '.')}:")
        for p in sorted(os.listdir(d)):
            A("  " + p)

# census card footage sources
ft = os.path.join(repo, "data", "sources", "footage")
A("=== footage census-card files ===")
for p in sorted(os.listdir(ft)):
    if "census" in p.lower():
        A("  " + p + " | " + datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(ft, p))).strftime("%m-%d %H:%M"))

# release schedule section
rs = os.path.join(repo, "docs", "release-schedule.md")
if os.path.exists(rs):
    with open(rs, encoding="utf-8") as f:
        t = f.read()
    A(f"=== release-schedule len {len(t)} ===")
    m = re.search(r"五[-—]1|[§#]+.*五.*", t)
    i = t.find("D25")
    A("D25_ctx: " + (t[max(0, i - 200): i + 700].replace("\n", " || ") if i >= 0 else "(D25 not found)"))
    j = t.find("LC-00")
    A("LC_ctx: " + (t[max(0, j - 300): j + 500].replace("\n", " || ") if j >= 0 else "(LC- not found)"))

# recent commits
r = subprocess.run(["git", "-C", repo, "log", "-6", "--oneline", "--stat=72"], capture_output=True, text=True, encoding="utf-8")
A("=== git log -6 ===")
A(r.stdout[:3000])

# cards finished tail (F-057 block)
fin = os.path.join(repo, "output", "finished.md")
with open(fin, encoding="utf-8") as f:
    ft2 = f.read()
i = ft2.find("F-057")
A("=== F-057 block ===")
A(ft2[max(0, i - 100): i + 1500] if i >= 0 else "F-057 not found")

with open(os.path.join(repo, ".c3-tmp", "probe-round2.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("WROTE", len(out), "lines")
