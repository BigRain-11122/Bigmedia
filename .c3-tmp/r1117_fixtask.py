import json, re, io

BM = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = BM + r"\src\os\state.json"

src = io.open(SP, encoding="utf-8").read()
data = json.loads(src)
last = data["log"][-1]
assert last.startswith("2026-10-03 16:3x R1117"), last[:40]

task = last.split("R1117: ", 1)[1][:60]
assert task.startswith("declared-idle"), task[:20]

i_tk = src.rfind('"task": "')
assert i_tk > 0
j_tk = src.find('"', i_tk + 9)
assert j_tk > i_tk
src = src[:i_tk] + '"task": ' + json.dumps(task, ensure_ascii=False) + src[j_tk + 1:]

data2 = json.loads(src)
assert data2["task"] == task
assert data2["tick"] == 1117
io.open(SP, "w", encoding="utf-8").write(src)
print("task fixed len=%d" % len(task))
