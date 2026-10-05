# -*- coding: utf-8 -*-
import json, io

st = json.load(io.open(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json", encoding="utf-8"))
out = io.StringIO()
out.write("tick=%s\nts=%s\n" % (st["tick"], st["ts"]))
out.write("task=%s\n" % st["task"])
out.write("production=%s\n" % st["production"])
last = str(st["log"][-1])
out.write("log[-1] HEAD: %s\n" % last[:120])
out.write("log[-1] TAIL: %s\n" % last[-200:])
out.write("log_len=%d\n" % len(st["log"]))
io.open(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1371_verify.txt", "w", encoding="utf-8").write(out.getvalue())
print("OK")
