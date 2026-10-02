import io, json

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
st = json.load(io.open(ROOT + r"\src\os\state.json", encoding="utf-8"))
l = st["log"][-1]
io.open(ROOT + r"\.c3-tmp\r1020_r1019tail.txt", "w", encoding="utf-8").write(l[-2600:])
print("ok len=%d" % len(l))
