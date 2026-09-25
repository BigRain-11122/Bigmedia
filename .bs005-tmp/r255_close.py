# -*- coding: utf-8 -*-
# R255 idle-fast close: append log line, refresh ts/task (PT-20260925-02).
# ASCII-only script; Chinese content lives in r255-logline.txt (UTF-8 data).
import io
import json
import time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
STATE = ROOT + r"\src\os\state.json"
LINE = ROOT + r"\.bs005-tmp\r255-logline.txt"

content = io.open(LINE, encoding="utf-8").read().strip()
stamp = time.strftime("%Y-%m-%d %H:%M")
entry = stamp + " " + content

raw = io.open(STATE, encoding="utf-8", newline="").read()
lines = raw.split("\r\n")

close_idx = None
for i, l in enumerate(lines):
    if l.strip() == "],":
        close_idx = i
        break
if close_idx is None:
    raise SystemExit("FAIL log-array close not found")

new_entry = "  " + json.dumps(entry, ensure_ascii=False) + ","
lines.insert(close_idx, new_entry)

ts_val = time.strftime("%Y-%m-%d %H:%M:%S")
task_val = content[:60]

out = []
for l in lines:
    s = l.strip()
    if s.startswith('"ts":'):
        l = ' "ts": ' + json.dumps(ts_val, ensure_ascii=False) + ","
    elif s.startswith('"task":'):
        l = ' "task": ' + json.dumps(task_val, ensure_ascii=False)
    out.append(l)

io.open(STATE, "w", encoding="utf-8", newline="").write("\r\n".join(out))

check = json.load(io.open(STATE, encoding="utf-8"))
print("OK tick=%s log_len=%d ts=%s task_len=%d"
      % (check["tick"], len(check["log"]), check["ts"], len(check["task"])))
