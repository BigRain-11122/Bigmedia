import json, os, glob

out = []
p = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
with open(p, encoding="utf-8") as f:
    d = json.load(f)

# weekend bucket across all axes + sprite
for axe in d["axes"]:
    b = d["axes"][axe].get("weekend")
    if b:
        out.append("AXE_" + axe + "_weekend: " + " | ".join(b if isinstance(b, list) else json.dumps(b, ensure_ascii=False)))
sp = d["sprite"].get("weekend")
out.append("SPRITE_weekend: " + " | ".join(sp if isinstance(sp, list) else json.dumps(sp, ensure_ascii=False)))

# anchor cards creed fields
adir = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors"
for fp in sorted(glob.glob(os.path.join(adir, "C-*.md"))):
    with open(fp, encoding="utf-8") as f:
        txt = f.read()
    lines = txt.splitlines()
    cid = os.path.basename(fp).replace(".md", "")
    name = ""
    creed = ""
    job = ""
    for i, ln in enumerate(lines):
        if ln.startswith("# "):
            name = ln[2:].strip()[:20]
        if "\u4fe1\u6761" in ln and creed == "":
            creed = ln.strip()[:70]
        if ln.startswith("- ") and ("\u804c\u4e1a" in ln or "\u5c97\u4f4d" in ln) and job == "":
            job = ln.strip()[:60]
    out.append("CARD " + cid + " " + name + " || job=" + job + " || " + creed)

with open(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r575_weekprobe.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print("OK " + str(len(out)))
