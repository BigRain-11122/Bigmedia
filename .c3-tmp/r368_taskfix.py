# -*- coding: utf-8 -*-
"""Fix R368 task field to match precedent: strip 'R368: ' prefix too."""
import json, io, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "src", "os", "state.json")
with io.open(STATE, "r", encoding="utf-8") as f:
    state = json.load(f)
tail = state["log"][-1]
assert " R368: " in tail, "unexpected tail"
body = tail.split(" R368: ", 1)[1]
state["task"] = body[:60]
with io.open(STATE, "w", encoding="utf-8", newline="\n") as f:
    json.dump(state, f, ensure_ascii=False, indent=1)
with io.open(STATE, "r", encoding="utf-8") as f:
    chk = json.load(f)
assert chk["log"][-1] == tail, "log corrupted"
assert chk["task"] == body[:60] and chk["tick"] == 368, "task/tick check failed"
# echo ascii-safe
print("task_fix ok: len=%d startswith_idle=%s" % (len(chk["task"]), chk["task"].startswith("idle-fast")))
