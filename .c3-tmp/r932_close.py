# r932_close.py - waiting-round account close for R932 (ASCII-only per encoding law)
import json, re, io, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
STATE = ROOT + r"\src\os\state.json"
PAYLOAD = ROOT + r"\.c3-tmp\r932_payload.json"

with io.open(PAYLOAD, encoding="utf-8") as f:
    p = json.load(f)

with io.open(STATE, encoding="utf-8") as f:
    s = json.load(f)

assert s["production"] == "open", "production gate flipped"
assert s["tick"] == 931, "tick anchor drifted: %s" % s["tick"]

now = datetime.datetime.now()
ts = now.strftime("%Y-%m-%d %H:%M:%S")

log_line = p["log_line"]
# normalize the approximate minute prefix to actual close minute
line_prefix_re = re.compile(r"^2026-10-02 04:\d\d")
fixed_prefix = now.strftime("%Y-%m-%d %H:%M")
log_line = line_prefix_re.sub(fixed_prefix, log_line, count=1)
assert log_line.startswith("2026-10-02 "), "log line prefix format broken"

s["tick"] = 932
s["log"].append(log_line)
s["focus"] = p["focus"]
s["ts"] = ts
s["task"] = log_line.split(" ", 2)[2][:60]

with io.open(STATE, "w", encoding="utf-8", newline="\n") as f:
    json.dump(s, f, ensure_ascii=False, indent=1)
    f.write("\n")

# post-write verification (R899 close-family format-bug clause)
with io.open(STATE, encoding="utf-8") as f:
    check = json.load(f)
assert check["tick"] == 932
assert check["log"][-1].startswith(fixed_prefix[:16]), "last log ts prefix mismatch"
assert check["task"][:5] == "R932:"
assert check["ts"] == ts
print("R932 close OK tick=%d ts=%s" % (check["tick"], check["ts"]))
