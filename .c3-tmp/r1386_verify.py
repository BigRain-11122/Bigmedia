# -*- coding: utf-8 -*-
import json, io
repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
st = json.load(io.open(repo + r"\src\os\state.json", encoding="utf-8"))
out = io.open(repo + r"\.c3-tmp\r1386_verify.txt", "w", encoding="utf-8")
out.write("tick=%s ts=%s\n" % (st["tick"], st["ts"]))
out.write("task=%s\n" % st["task"])
out.write("log_len=%d\n" % len(st["log"]))
out.write("log_tail=%s\n" % st["log"][-1][:200])
out.close()
print("ok")
