# -*- coding: utf-8 -*-
"""R1444 verify final state fields -> UTF-8 file (console GBK-safe)."""
import io, json

PATH = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
st = json.loads(io.open(PATH, encoding="utf-8").read())
lines = [
    "tick=%s" % st["tick"],
    "log_count=%d" % len(st["log"]),
    "ts=%s" % st["ts"],
    "task=%s" % st["task"],
    "log_last_head=%s" % st["log"][-1][:100],
    "log_last_len=%d" % len(st["log"][-1]),
    "log_prev_head=%s" % st["log"][-2][:60],
]
io.open(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1444_verify.txt", "w", encoding="utf-8").write("\n".join(lines))
print("VERIFY_WRITTEN")
