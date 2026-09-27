import json, os, re, io

root = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = []

# S1: ledger L140 full row (P-2026-09-27-02)
with open(r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md", encoding="utf-8") as f:
    led = f.read().splitlines()
for i, l in enumerate(led):
    if "P-2026-09-27-02" in l:
        out.append(f"=== LEDGER L{i+1} (P-02) ===")
        out.append(l)
# also P-2026-09-27-07 full row for context
for i, l in enumerate(led):
    if "P-2026-09-27-07" in l:
        out.append(f"=== LEDGER L{i+1} (P-07) ===")
        out.append(l[:600])

# S2: decisions C-20260927-01 full row
with open(r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md", encoding="utf-8") as f:
    dec = f.read().splitlines()
for i, l in enumerate(dec):
    if "C-20260927-01" in l:
        out.append(f"=== DECISIONS L{i+1} (C-01) ===")
        out.append(l)

# S3: group master doc - 19 paypoints + 4-layer pricing (first 120 lines)
with open(r"C:\Users\sjs20\Desktop\FluxGroup\cph4\research\R-20260927-commercial-paypoints.md", encoding="utf-8") as f:
    master = f.read()
out.append(f"=== MASTER DOC len={len(master)} ===")
out.append(master[:6000])

# S4: our narrative mapping doc (R487) - key numbers section
p4 = os.path.join(root, "docs", "research", "R-20260927-bigstream-02-paypoint-narrative-mapping.md")
if os.path.exists(p4):
    with open(p4, encoding="utf-8") as f:
        nm = f.read()
    out.append(f"=== NARRATIVE MAPPING len={len(nm)} ===")
    out.append(nm[:4000])

# S5: HQ-FEEDBACK F-20260927-04 line
with open(os.path.join(root, "HQ-FEEDBACK.md"), encoding="utf-8") as f:
    hq = f.read().splitlines()
for i, l in enumerate(hq):
    if "F-20260927-04" in l:
        out.append(f"=== HQ-FEEDBACK L{i+1} ===")
        out.append(l[:500])

# S6: cards dir listing + find v6 build script & cards.json
cdir = os.path.join(root, "data", "storylines", "cards")
out.append("=== CARDS DIR ===")
out.append(" | ".join(sorted(os.listdir(cdir))[-20:]))
# find build scripts
for d, sub in [(root, None)]:
    for f2 in os.listdir(root):
        if f2.startswith("."):
            p = os.path.join(root, f2)
            if os.path.isdir(p):
                bs = [x for x in os.listdir(p) if x.startswith("build")]
                if bs:
                    out.append(f"BUILD in {f2}: {bs}")

with open(os.path.join(root, ".c3-tmp", "v7_sources.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("OK")
