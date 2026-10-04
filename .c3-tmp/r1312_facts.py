# r1312 targeted facts: mid-window rounds / dig15 E4 status / open items 78+86 / export freshness
import json, os, re, glob, time

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
L = []
add = L.append

state = json.load(open(os.path.join(repo, "src", "os", "state.json"), encoding="utf-8"))
log = state.get("log", [])

add("== log heads R1303..R1308 ==")
for line in log:
    m = re.search(r"R(13(0[3-8]))\b", line[:30])
    if m:
        add(line[:700])
        add("")

# dig15 E4 result files anywhere (mtime 10-04 18:00 .. now)
add("== e4/dig15 result files ==")
now = time.time()
for root, dirs, files in os.walk(repo):
    if ".git" in root or "node_modules" in root:
        continue
    for f in files:
        p = os.path.join(root, f)
        try:
            mt = os.path.getmtime(p)
        except OSError:
            continue
        if ("e4" in f.lower() or "dig" in f.lower() or "v15" in f.lower()) and (now - mt) < 30 * 3600:
            add(time.strftime("%m-%d %H:%M", time.localtime(mt)) + "  " + os.path.relpath(p, repo))
add("")

# backlog items 78 and 86 full text
bl = open(os.path.join(repo, "src", "os", "backlog.md"), encoding="utf-8").read().splitlines()
add("== backlog L325-L372 (items 78/86 region) ==")
for i in range(324, min(372, len(bl))):
    add(f"L{i+1}| {bl[i][:400]}")
add("")

# status-export freshness
se = os.path.join(repo, "docs", "status-export.json")
mt = os.path.getmtime(se)
add(f"status-export mtime={time.strftime('%m-%d %H:%M', time.localtime(mt))}")
try:
    ex = json.load(open(se, encoding="utf-8"))
    add("export_ts=" + str(ex.get("export_ts", "")))
    add("keys=" + ",".join(list(ex.keys())[:12]))
except Exception as e:
    add("export parse err " + str(e))

out = os.path.join(repo, ".c3-tmp", "r1312_facts.txt")
open(out, "w", encoding="utf-8").write("\n".join(L))
print("done", len(L))
