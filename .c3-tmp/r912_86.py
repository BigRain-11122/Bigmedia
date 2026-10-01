import io, os, re, json

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP = r"C:\Users\sjs20\Desktop\FluxGroup"
OUT = []

# 1. backlog #86 full text
bl = io.open(os.path.join(ROOT, "src", "os", "backlog.md"), "r", encoding="utf-8").read().splitlines()
start = None
for i, l in enumerate(bl):
    if re.match(r"^86\.", l):
        start = i
        break
if start is not None:
    OUT.append("--- backlog #86 full ---")
    for l in bl[start:start + 40]:
        OUT.append("86: " + l[:400])
        if re.match(r"^\d+\.", l) and not re.match(r"^86\.", l):
            break

# 2. codex dir listing
cd = os.path.join(ROOT, "data", "storylines", "codex")
OUT.append("--- codex dir ---")
for f in sorted(os.listdir(cd)):
    p = os.path.join(cd, f)
    sz = os.path.getsize(p)
    import datetime
    mt = datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M")
    OUT.append("CX: %s  %dB  %s" % (f, sz, mt))

# 3. README tail (ledger)
rd = io.open(os.path.join(cd, "README.md"), "r", encoding="utf-8").read().splitlines()
OUT.append("--- codex README lines=%d tail 30 ---" % len(rd))
for l in rd[-30:]:
    OUT.append("RD: " + l[:240])

# 4. three zhi counts + last 3 entries each
for name in ["city-spirit.md", "city-humanities.md", "residents.md", "city-culture.md"]:
    p = os.path.join(cd, name)
    if not os.path.exists(p):
        OUT.append("(%s ABSENT)" % name)
        continue
    t = io.open(p, "r", encoding="utf-8").read()
    lines = t.splitlines()
    nums = re.findall(r"^#\s*(\d+)", t, re.M)
    OUT.append("--- %s: lines=%d ---" % (name, len(lines)))
    OUT.append("HEAD: " + t[:400].replace("\n", " / "))
    for l in lines[-12:]:
        OUT.append("  Z: " + l[:200])

# 5. pools.json (BigLife cognition)
for cand in [os.path.join(GRP, "life", "BigLife", "cognition", "pools.json"),
             os.path.join(GRP, "life", "BigLife", "data", "cognition", "pools.json")]:
    if os.path.exists(cand):
        OUT.append("pools.json at: " + cand)
        j = json.load(io.open(cand, "r", encoding="utf-8"))
        if isinstance(j, dict):
            OUT.append("pools keys: " + str(list(j.keys()))[:300])
            tot = 0
            for k, v in j.items():
                if isinstance(v, list):
                    OUT.append("  %s: %d items" % (k, len(v)))
                    tot += len(v)
            OUT.append("total list items: %d" % tot)
        break
else:
    OUT.append("pools.json not found in candidates")

with open(os.path.join(ROOT, ".c3-tmp", "r912_86.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("lines:", len(OUT))
