import json, re, datetime, shutil, os

BM = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = BM + r"\src\os\state.json"
LP = BM + r"\.c3-tmp\r1115_logline.txt"

line = open(LP, encoding="utf-8").read().strip()
src = open(SP, encoding="utf-8").read()

# sanity: current tick
m = re.search(r'"tick":\s*(\d+)', src)
tick = int(m.group(1))
assert tick == 1114, "unexpected tick %d" % tick

# 1) bump tick
src = src.replace('"tick": %d,' % tick, '"tick": %d,' % (tick + 1), 1)

# 2) append log line before the closing "]," of the log array (last occurrence)
i = src.rfind("\n ],")
assert i > 0, "log array close not found"
prev_end = src.rfind('"', 0, i)
assert prev_end > 0
src = src[:prev_end + 1] + ",\n  " + json.dumps(line, ensure_ascii=False) + src[i:]

# 3) heartbeat ts + task (LAST fields; keep original closing quotes via splice)
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
t = re.sub(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}x ", "", line)
t = re.sub(r"^R\d+: ", "", t)
task = t[:60]

i_ts = src.rfind('"ts": "')
assert i_ts > 0
j_ts = src.find('"', i_ts + 7)
assert j_ts > i_ts
src = src[:i_ts] + '"ts": ' + json.dumps(now, ensure_ascii=False) + src[j_ts + 1:]

i_tk = src.rfind('"task": "')
assert i_tk > i_ts
j_tk = src.find('"', i_tk + 9)
assert j_tk > i_tk
src = src[:i_tk] + '"task": ' + json.dumps(task, ensure_ascii=False) + src[j_tk + 1:]

# validate
data = json.loads(src)
assert data["tick"] == 1115
assert data["log"][-1].startswith("2026-10-03 16:1x R1115")
assert data["task"] == task
assert data["ts"] == now
assert len(data["log"]) >= 1115

shutil.copyfile(SP, SP + ".bak_r1115")
open(SP, "w", encoding="utf-8").write(src)
os.remove(SP + ".bak_r1115")
print("OK tick=1115 ts=%s log_lines=%d" % (now, len(data["log"])))
print("task_ascii:", task.encode("ascii", "replace").decode())
