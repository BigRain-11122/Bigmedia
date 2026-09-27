import json, os, re
root = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = []
with open(os.path.join(root, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
log = st.get("log", [])
hits = [(i, l) for i, l in enumerate(log) if "#77" in l]
out.append(f"LOG_77_HITS={len(hits)}")
for i, l in hits:
    out.append(f"--- log[{i}] {l[:300]}")

# production-chain M4 row current state (check for 办法/GB 45438)
with open(os.path.join(root, "docs", "production-chain.md"), encoding="utf-8") as f:
    pc = f.read().splitlines()
for i, l in enumerate(pc):
    if "人工智能生成合成内容标识办法" in l or "GB 45438" in l:
        out.append(f"PC L{i+1}: {l[:500]}")

# finished.md F-item count
with open(os.path.join(root, "output", "finished.md"), encoding="utf-8") as f:
    fin = f.read()
fids = re.findall(r"F-0\d\d", fin)
out.append(f"FINISHED_F_IDS={sorted(set(fids))}")
out.append(f"FINISHED_COUNT={len(set(fids))}")

with open(os.path.join(root, ".c3-tmp", "r517_check.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("OK")
