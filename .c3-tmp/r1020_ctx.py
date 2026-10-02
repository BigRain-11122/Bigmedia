import io, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
st = __import__('json').load(io.open(ROOT + r"\src\os\state.json", encoding="utf-8"))
log = st["log"]
out = io.StringIO()
out.write(u"=== LAST LOG LINE (R1019) FULL ===\n")
out.write(log[-1] + u"\n")
out.write(u"\n=== SECOND LAST (R1018) tail 600 chars ===\n")
out.write(log[-2][-600:] + u"\n")

q = io.open(ROOT + r"\docs\self-improvement-queue.md", encoding="utf-8").read().splitlines()
idx = None
for i, l in enumerate(q):
    if "E30" in l:
        idx = i
        break
out.write(u"\n=== QUEUE E30 section (line %s) ===\n" % idx)
if idx is not None:
    for l in q[max(0, idx-6):idx+18]:
        out.write(l + u"\n")

io.open(ROOT + r"\.c3-tmp\r1020_ctx.txt", "w", encoding="utf-8").write(out.getvalue())
print("ok")
