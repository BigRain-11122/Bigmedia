import json, re, datetime

BM = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = BM + r"\src\os\state.json"

src = open(SP, encoding="utf-8").read()
data = json.loads(src)
line = data["log"][-1]
assert line.startswith("2026-10-03 16:1x R1114"), "last log line mismatch"

t = re.sub(r"^\d{4}-\d{2}-\d{2} \d{2}:[0-9x]{1,2} ", "", line)
t = re.sub(r"^R\d+: ", "", t)
task = t[:60]
assert task.startswith("declared-idle"), "prefix strip failed: %r" % task[:30]

i_tk = src.rfind('"task": "')
j_tk = src.find('"', i_tk + 9)
src = src[:i_tk] + '"task": ' + json.dumps(task, ensure_ascii=False) + src[j_tk + 1:]

data2 = json.loads(src)
assert data2["task"] == task
assert data2["tick"] == 1114
open(SP, "w", encoding="utf-8").write(src)
print("OK task_fixed_len=%d" % len(task))
print("task_ascii:", task.encode("ascii", "replace").decode())
