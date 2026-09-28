# r640 pool probe: bucket structure + cat/game/play keyword lines (UTF-8 out)
import io, json, re, collections

P = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
R = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
d = json.load(io.open(P, encoding="utf-8"))
out = []
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
out.append("total_leaf_lines=%d" % len(acc))
buckets = collections.Counter()
for p, _ in acc:
    parts = p.strip("/").split("/")
    if len(parts) >= 3:
        buckets["/".join(parts[:3])] += 1
out.append("=== buckets (top3 path levels) ===")
for k, v in sorted(buckets.items()):
    out.append("%s (%d)" % (k, v))
kw = re.compile("\u55b5|\u732b|\u72d7|\u73a9|\u6e38\u620f|\u6ed1\u677f|\u98de|\u53ef\u7231|\u840c|\u54c8\u57fa\u7c73")
# kw chars: miao cat dog play game slideboard fly cute meng miao "ha-ji-mi"
out.append("=== kw hits ===")
n = 0
for p, s in acc:
    if kw.search(s):
        out.append("%s :: %s" % (p, s))
        n += 1
out.append("kw_hit_count=%d" % n)
io.open(R + r"\.c3-tmp\r640_pool.txt", "w", encoding="utf-8").write("\n".join(out))
print("POOL_OK leaves=%d kw=%d" % (len(acc), n))
