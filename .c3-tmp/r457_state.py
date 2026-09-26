import json, io, re
ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TS = "2026-09-27 03:07:18"
def read_utf8(p):
    with io.open(p, "r", encoding="utf-8") as f:
        return f.read().strip()
logline = read_utf8(ROOT + r"\.c3-tmp\r457_log.txt")
focus = read_utf8(ROOT + r"\.c3-tmp\r457_focus.txt")
m = re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2} R\d+: ", logline)
assert m, "log line missing timestamp prefix"
task = logline[m.end():][:60]
p = ROOT + r"\src\os\state.json"
with io.open(p, "r", encoding="utf-8") as f:
    d = json.load(f)
assert d["tick"] == 456, "unexpected tick anchor: %s" % d["tick"]
assert len(d["log"]) > 450, "unexpected log size: %d" % len(d["log"])
assert d["log"][-1].startswith("2026-09-27 02:51 R456") or "R456" in d["log"][-1], "unexpected last log entry"
d["tick"] = 457
d["log"].append(logline)
d["focus"] = focus
d["ts"] = TS
d["task"] = task
with io.open(p, "w", encoding="utf-8", newline="\n") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("OK tick=%d log=%d ts=%s task_len=%d" % (d["tick"], len(d["log"]), d["ts"], len(d["task"])))