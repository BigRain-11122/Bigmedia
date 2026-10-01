import io, os, re, glob

GRP = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = os.path.join(GRP, "media", "BigStream")
OUT = []

# find fluxverse repo
fv_roots = [d for d in glob.glob(os.path.join(GRP, "*")) if os.path.isdir(d)]
OUT.append("GRP dirs: " + str([os.path.basename(d) for d in fv_roots]))

# locate 空间正典 / city-plan in fluxverse-like dirs
cands = []
for root, dirs, files in os.walk(GRP):
    dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "node_modules", "Library", "Temp", ".codely-cli", ".ollama")]
    for f in files:
        if re.search(r"city-plan|空间正典|space-canon|DESIGN", f, re.I) and f.endswith((".md",)):
            cands.append(os.path.join(root, f))
OUT.append("canon cands:")
for c in cands[:20]:
    OUT.append("  " + c.replace(GRP, "<GRP>"))

# read the most likely one(s) and dump headings + market/district lines
for c in cands:
    base = os.path.basename(c).lower()
    if "city-plan" in base or "空间" in base or "space" in base:
        t = io.open(c, "r", encoding="utf-8", errors="replace").read()
        lines = t.splitlines()
        OUT.append("=== FILE %s lines=%d ===" % (c.replace(GRP, "<GRP>"), len(lines)))
        for l in lines:
            if re.match(r"^#{1,4}\s", l) or re.search(r"市井|街区|商|铺|市集|渔市|门楼|主街|生活感|烟火", l):
                OUT.append("  F: " + l.strip()[:180])

# existing 3 harvested entries in city-humanities (for dedup)
hu = io.open(os.path.join(BS, "data", "storylines", "codex", "city-humanities.md"), "r", encoding="utf-8").read()
OUT.append("--- harvested FluxVerse entries in humanities ---")
for l in hu.splitlines():
    if "FluxVerse" in l or "空间正典" in l:
        OUT.append("H: " + l[:200])

with io.open(os.path.join(BS, ".c3-tmp", "r912_fv.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("lines:", len(OUT))
