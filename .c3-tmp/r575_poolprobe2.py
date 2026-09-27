import json

p = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
with open(p, encoding="utf-8") as f:
    d = json.load(f)

out = []
sp = d["sprite"]
for k, v in sp.items():
    n = len(v) if hasattr(v, "__len__") else 0
    sample = ""
    if isinstance(v, list) and v:
        sample = json.dumps(v[0], ensure_ascii=False)[:150]
    elif isinstance(v, dict):
        sample = json.dumps(v, ensure_ascii=False)[:150]
    out.append("SPRITE_BUCKET " + k + " n=" + str(n) + " " + sample)

ax = d["axes"]
for k, v in ax.items():
    out.append("AXE " + k + " " + str(type(v).__name__) + " " + (str(len(v)) if hasattr(v, "__len__") else ""))

with open(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r575_poolprobe2.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print("OK " + str(len(out)))
