# -*- coding: utf-8 -*-
# R1404 close verify: state.json tail fields (tick/ts/task/log tail) UTF-8 read-back
import json, io
repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
st = json.load(io.open(repo + r"\src\os\state.json", encoding="utf-8"))
out = io.open(repo + r"\.c3-tmp\r1404_verify.txt", "w", encoding="utf-8")
w = out.write
w("tick=%s\nts=%s\n" % (st.get("tick"), st.get("ts")))
w("task=%s\n" % st.get("task"))
w("log_len=%s\n" % len(st.get("log", [])))
w("== log tail 1 ==\n")
for line in st.get("log", [])[-1:]:
    w(line[:400] + "\n")
w("== focus head ==\n")
w((st.get("focus") or "")[:200] + "\n")
out.close()
print("verify ok")
