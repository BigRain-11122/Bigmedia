# -*- coding: utf-8 -*-
# R1393 verify: state.json integrity after update (GBK console display is display-only; io channel is truth)
import json, io

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = io.open(repo + r"\.c3-tmp\r1393_verify.txt", "w", encoding="utf-8")
w = out.write

st = json.load(io.open(repo + r"\src\os\state.json", encoding="utf-8"))
w("tick=%s\n" % st.get("tick"))
w("ts=%s\n" % st.get("ts"))
w("production=%s\n" % st.get("production"))
w("log_count=%s\n" % len(st.get("log", [])))
tail = st["log"][-1]
w("log_tail_head_ok=%s\n" % tail.startswith("2026-10-05 18:5"))
w("log_tail_len=%s\n" % len(tail))
w("log_tail_head_120=%s\n" % tail[:120])
w("task_len=%s task_head_60=%s\n" % (len(st.get("task", "")), st.get("task", "")[:60]))
w("focus_head_150=%s\n" % (st.get("focus", "") or "")[:150])
# JSON re-load clean check
w("json_reload_ok=%s\n" % isinstance(json.loads(io.open(repo + r"\src\os\state.json", encoding="utf-8").read()), dict))
out.close()
print("verify done")
