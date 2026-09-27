import json, os

p = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
with open(p, encoding="utf-8") as f:
    d = json.load(f)

out = []
out.append("TYPE " + str(type(d).__name__))
if isinstance(d, dict):
    out.append("TOPKEYS " + str(len(d)))
    for k, v in d.items():
        out.append("KEY " + repr(k) + " " + str(type(v).__name__) + " " + (str(len(v)) if hasattr(v, "__len__") else ""))
elif isinstance(d, list):
    out.append("LEN " + str(len(d)))
    out.append("SAMPLE " + json.dumps(d[0], ensure_ascii=False)[:400] if d else "EMPTY")

with open(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r575_poolprobe.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out[:80]) + "\n")
print("OK")
