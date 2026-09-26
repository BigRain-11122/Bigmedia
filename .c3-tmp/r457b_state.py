import json, io
from datetime import datetime
ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TS = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def read_utf8(p):
    with io.open(p, "r", encoding="utf-8") as f:
        return f.read().strip()
logline = read_utf8(ROOT + r"\.c3-tmp\r457b_log.txt")
p = ROOT + r"\src\os\state.json"
with io.open(p, "r", encoding="utf-8") as f:
    d = json.load(f)
assert d["tick"] == 457, "unexpected tick: %s" % d["tick"]
assert d["log"][-1].startswith("2026-09-27 03:07 R457"), "unexpected last log entry"
d["log"].append(logline)
d["ts"] = TS
with io.open(p, "w", encoding="utf-8", newline="\n") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("OK log=%d ts=%s" % (len(d["log"]), d["ts"]))