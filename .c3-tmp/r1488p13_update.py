import json, re, io
from datetime import datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
STATE = ROOT + r"\src\os\state.json"
LOGLINE = ROOT + r"\.c3-tmp\r1488p13_logline.txt"

with io.open(STATE, encoding="utf-8-sig") as f:
    data = json.load(f)
with io.open(LOGLINE, encoding="utf-8-sig") as f:
    line = f.read().rstrip("\n").rstrip("\r")

assert line not in data["log"], "duplicate log line"
assert data["tick"] == 1487, "unexpected tick: %s" % data["tick"]

data["log"].append(line)
data["tick"] = 1488
data["ts"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
task = re.sub(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}\S*\s+", "", line)
data["task"] = task[:60]

with io.open(STATE, "w", encoding="utf-8", newline="\n") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("OK tick=%s ts=%s" % (data["tick"], data["ts"]))
print("task=%s" % data["task"])
