import io, os, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = []

OUT.append("--- src/*.py ---")
for f in sorted(os.listdir(os.path.join(ROOT, "src"))):
    if f.endswith(".py"):
        OUT.append("S: " + f)

OUT.append("--- backlog item headers ---")
bl = io.open(os.path.join(ROOT, "src", "os", "backlog.md"), "r", encoding="utf-8").read().splitlines()
for l in bl:
    m = re.match(r"^(\d+)\.\s*(.*)", l)
    if m:
        done = "[done" in l or "[R" in l
        OUT.append("#%s done=%s | %s" % (m.group(1), ("done-mark" if "[done" in l else "open"), l[:110]))

OUT.append("--- backlog #86 + #97..#99 grep ---")
for l in bl:
    if re.match(r"^(86|87|88|89|9[0-9])\.", l):
        OUT.append("NUM: " + l[:400])

OUT.append("--- queue head 75 ---")
q = io.open(os.path.join(ROOT, "docs", "self-improvement-queue.md"), "r", encoding="utf-8").read().splitlines()
for l in q[:75]:
    OUT.append("Q: " + l[:170])

OUT.append("--- DD/bilibili conclusion in state log ---")
import json
st = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), "r", encoding="utf-8-sig"))
log = st["log"]
hits = [l for l in log if "bs001-dd" in l or ("B站深纵" in l and "登记" in l)]
OUT.append("dd hits=%d" % len(hits))
for l in hits[-4:]:
    OUT.append("DD: " + l[:300])
fin = io.open(os.path.join(ROOT, "output", "finished.md"), "r", encoding="utf-8").read()
m = [l for l in fin.splitlines() if "DD" in l or "bilibili" in l or "深纵" in l]
OUT.append("fin dd lines=%d" % len(m))
for l in m[-5:]:
    OUT.append("FD: " + l[:250])

with open(os.path.join(ROOT, ".c3-tmp", "r912_open.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("lines:", len(OUT))
