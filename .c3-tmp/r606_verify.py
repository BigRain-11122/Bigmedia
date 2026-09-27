# -*- coding: utf-8 -*-
# R606 verify: state.json + status-export.json post-close readback (UTF-8 per R562 law; r605_verify.py template)
import io, json

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
st = json.load(io.open(ROOT + r"\src\os\state.json", encoding="utf-8"))
xp = json.load(io.open(ROOT + r"\docs\status-export.json", encoding="utf-8"))

lines = []
lines.append("tick=%s" % st["tick"])
lines.append("ts=%s" % st["ts"])
lines.append("task=%s" % st["task"])
lines.append("task_len=%d" % len(st["task"]))
lines.append("log_count=%d" % len(st["log"]))
lines.append("log_tail_head=%s" % st["log"][-1][:100])
lines.append("focus_head=%s" % st["focus"][:100])
lines.append("export_ts=%s" % xp["export_ts"])
os_row = [r[1] for r in xp["outs"] if r[0] == u"OS 循环"]
lines.append("os_row_head=%s" % (os_row[0][:80] if os_row else "NA"))
out = "\n".join(lines)
io.open(ROOT + r"\.c3-tmp\r606_verify.txt", "w", encoding="utf-8").write(out)
print("VERIFY_WRITTEN (UTF-8 in-file per R562; console shows ascii only)")
print("tick=%s ts=%s log_count=%d task_len=%d" % (st["tick"], st["ts"], len(st["log"]), len(st["task"])))
