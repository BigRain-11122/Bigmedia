# R921 close helper step 2: remove illegal trailing comma on last log element.
# ASCII-only per encoding law (CJK via unicode escapes).
import json

p = r"src/os/state.json"
s = open(p, encoding="utf-8", newline="").read()

# end of R921 log line: "...W41 10-05\uff09ETA 2026-10-02 21:40",  -> drop comma
tail_bad = "\uff09" + 'ETA 2026-10-02 21:40",'
tail_ok = "\uff09" + 'ETA 2026-10-02 21:40"'
n = s.count(tail_bad)
assert n == 1, "expect 1 occurrence, got %d" % n
s = s.replace(tail_bad, tail_ok)
open(p, "w", encoding="utf-8", newline="").write(s)

d = json.loads(open(p, encoding="utf-8").read())
print("JSON OK, tick=%s ts=%s log_lines=%d" % (d["tick"], d["ts"], len(d["log"])))
print("last_log_prefix=%s" % d["log"][-1][:30])
print("task=%s" % d["task"][:40])
