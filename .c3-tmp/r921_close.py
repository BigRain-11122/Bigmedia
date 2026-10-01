# R921 close helper: insert missing comma before R921 log entry, validate JSON.
# ASCII-only per encoding law.
import json

p = r"src/os/state.json"
s = open(p, encoding="utf-8", newline="").read()
marker = '  "2026-10-02 02:13 R921'
if marker in s and s.index(marker) > 0:
    i = s.index(marker)
    j = i - 1
    while s[j] in "\r\n":
        j -= 1
    assert s[j] == '"', repr(s[j])
    if s[j + 1 : j + 2] != ",":
        s = s[: j + 1] + "," + s[j + 1 :]
        open(p, "w", encoding="utf-8", newline="").write(s)
        print("comma inserted")
    else:
        print("comma already present")
else:
    print("marker not found - no action")

d = json.loads(open(p, encoding="utf-8").read())
print("JSON OK, tick=%s ts=%s log_lines=%d" % (d["tick"], d["ts"], len(d["log"])))
print("last_log_prefix=%s" % d["log"][-1][:30])
print("task=%s" % d["task"][:40])
