import io, json, re

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = io.open(repo + r"\.c3-tmp\r1362_probe3.txt", "w", encoding="utf-8")
w = out.write

# full B5 row + surrounding lines in queue
q = io.open(repo + r"\docs\self-improvement-queue.md", encoding="utf-8").read().split("\n")
w("== queue lines containing B5 / slice / C-face ==\n")
for i, l in enumerate(q):
    if ("B5" in l and "段子" in l) or "slice2" in l or "C-face" in l or "C 面" in l or "C面" in l:
        w("Q%d| %s\n\n" % (i, l[:1500]))

# full R1358 log line
st = json.load(io.open(repo + r"\src\os\state.json", encoding="utf-8"))
log = st["log"]
for line in log:
    if "R1358" in line[:20]:
        w("== R1358 FULL ==\n%s\n" % line)

# queue tail (E pool recent entries + burn notes)
w("\n== queue tail 30 (of %d) ==\n" % len(q))
for l in q[-30:]:
    w("QT| " + l[:400] + "\n")

# user-research s9.1 presence
ur = glob = None
import os
for cand in [r"\research\user-research-v1.md", r"\research\user-research.md"]:
    p = repo + cand
    if os.path.exists(p):
        ur = p
        break
if ur:
    txt = io.open(ur, encoding="utf-8").read()
    w("\nuser-research file=%s len=%d\n" % (ur, len(txt)))
    idx = txt.find("9.1")
    if idx >= 0:
        w("== s9.1 excerpt ==\n%s\n" % txt[idx:idx+2200])

out.close()
print("ok")
