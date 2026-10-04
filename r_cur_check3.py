# -*- coding: utf-8 -*-
"""R1305: locate DAILY production tooling + latest state."""
import os, io, glob, re, json

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = io.StringIO()

# 1) latest build scripts / cards files by mtime
for pat in [r"data\storylines\cards\*.py", r"data\storylines\cards\*.json", r"data\storylines\cards\*.md"]:
    fs = glob.glob(os.path.join(ROOT, pat))
    fs.sort(key=os.path.getmtime, reverse=True)
    out.write(f"== {pat} (total {len(fs)}) latest 8 ==\n")
    for p in fs[:8]:
        import datetime
        out.write(f"  {os.path.basename(p)}  {datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%m-%d %H:%M')}\n")

# 2) cards README tail (last 40 lines)
rp = os.path.join(ROOT, "data", "storylines", "cards", "README.md")
if os.path.exists(rp):
    with open(rp, encoding="utf-8") as f:
        lines = f.read().splitlines()
    out.write(f"\ncards/README.md lines={len(lines)} tail 25:\n")
    for ln in lines[-25:]:
        out.write("  " + ln[:200] + "\n")

# 3) finished.md tail 12 lines
fp = os.path.join(ROOT, "output", "finished.md")
if os.path.exists(fp):
    with open(fp, encoding="utf-8") as f:
        lines = f.read().splitlines()
    out.write(f"\nfinished.md lines={len(lines)} tail 12:\n")
    for ln in lines[-12:]:
        out.write("  " + ln[:200] + "\n")

# 4) queue E30/E31/E33 recent mentions (last 3 each)
qp = os.path.join(ROOT, "docs", "self-improvement-queue.md")
with open(qp, encoding="utf-8") as f:
    qlines = f.read().splitlines()
out.write(f"\nqueue lines={len(qlines)}\n")
for tag in ["E30", "E31", "E33", "E34"]:
    hits = [ln for ln in qlines if tag in ln]
    out.write(f"-- {tag}: {len(hits)} hits, last 2 ==\n")
    for ln in hits[-2:]:
        out.write("  " + ln[:260] + "\n")

# 5) board probe script location
cands = []
for pat in [r"src\**\*.py", r"tests\*.py"]:
    for p in glob.glob(os.path.join(ROOT, pat), recursive=True):
        b = os.path.basename(p).lower()
        if "board" in b:
            cands.append(p)
out.write(f"\nboard scripts: {cands}\n")

# 6) latest DAILY version count in cards README
with open(rp, encoding="utf-8") as f:
    txt = f.read()
vs = re.findall(r"DAILY[- ]v(\d+)", txt)
out.write(f"\nDAILY versions mentioned max: {max(map(int, vs)) if vs else 'none'}\n")

# 7) state log tail for DAILY F-number context
with open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
for ln in st["log"][-8:]:
    if "DAILY" in ln or "E30" in ln or "F-15" in ln:
        out.write("STATE>> " + ln[:300] + "\n")

with open(os.path.join(ROOT, "r_cur_check3.txt"), "w", encoding="utf-8") as f:
    f.write(out.getvalue())
print("ok")
