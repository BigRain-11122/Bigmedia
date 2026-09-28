# r640 weekend bucket full dump v2 (structure-agnostic walk)
import io, json

P = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
R = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
d = json.load(io.open(P, encoding="utf-8"))
acc = []

def walk(node, path):
    if isinstance(node, dict):
        for k, v in node.items():
            walk(v, path + "/" + str(k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            if isinstance(v, (dict, list)):
                walk(v, path + "/" + str(i))
            else:
                acc.append((path + "/" + str(i), str(v)))
    else:
        acc.append((path, str(node)))

walk(d, "")
out = []
for p, s in acc:
    if "/weekend" in p:
        out.append("%s :: %s" % (p, s))
io.open(R + r"\.c3-tmp\r640_weekend.txt", "w", encoding="utf-8").write("\n".join(out))
print("WEEKEND_OK lines=%d" % len(out))
