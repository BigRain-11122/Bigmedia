import io, json

p = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
L = io.open(p, encoding="utf-8").read().splitlines(True)
i = [k for k, l in enumerate(L) if l.startswith('  "2026-10-03 14:2x R1104:')][0]
ln = L[i]
assert ln.rstrip("\r\n").endswith(','), "line does not end with comma: %r" % ln[-20:]
L[i] = ln.rstrip("\r\n")[:-1] + "\n"
io.open(p, "w", encoding="utf-8", newline="").write("".join(L))
print("trailing comma removed")

s = json.load(io.open(p, encoding="utf-8"))
print("tick=%s" % s["tick"])
print("ts=%s" % s["ts"])
print("task_len=%d" % len(s["task"]))
print("log_tail_60=%s" % s["log"][-1][:60])
print("log_count=%d" % len(s["log"]))
print("focus_prefix=%s" % s["focus"][:40])
print("production=%s" % s["production"])
print("JSON_VALID")
