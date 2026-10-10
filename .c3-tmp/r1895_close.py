# -*- coding: utf-8 -*-
"""R1895 closing-stage accounting updater (pure ASCII code; Chinese
payloads live in r1895_close_data.json per the encoding law).

Updates:
  state.json        tick -> 1895, ts, task (60-char head of the log line
                    minus its timestamp prefix), focus -> R1896, log
                    append R1895 line
  status-export.json export_ts, outs append, results append, live refresh
Round-trip format: json.dumps(ensure_ascii=False, indent=1) + "\n"
(verified byte-identical against both files before any write).
"""
import json
import re
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA = json.loads((REPO / ".c3-tmp" / "r1895_close_data.json").read_text(
    encoding="utf-8"))
NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
LOG_MIN = datetime.now().strftime("%Y-%m-%d %H:%M")


def dump(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


# --- state.json ---------------------------------------------------------
sp = REPO / "src" / "os" / "state.json"
state = json.loads(sp.read_text(encoding="utf-8"))
line = DATA["log_line"]
# stamp the actual minute (approximate-minute convention keeps the 14:2x
# narrative form only if the real minute matches; use the true minute)
line = re.sub(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}x ", LOG_MIN + " ", line,
              count=1)
task_src = re.sub(r"^\S+ \S+ ", "", line)
state["tick"] = 1895
state["ts"] = NOW
state["task"] = task_src[:60]
state["focus"] = DATA["focus"]
state["log"].append(line)
sp.write_text(dump(state), encoding="utf-8")
print("state.json tick=%s ts=%s task=%r" % (state["tick"], state["ts"],
                                            state["task"]))

# --- status-export.json -------------------------------------------------
ep = REPO / "docs" / "status-export.json"
expo = json.loads(ep.read_text(encoding="utf-8"))
expo["export_ts"] = NOW
expo["outs"].append(DATA["out_line"])
expo["results"].append(["1895", DATA["result_line"]])
expo["live"] = DATA["live"]
ep.write_text(dump(expo), encoding="utf-8")
print("status-export.json export_ts=%s outs=%d results=%d"
      % (NOW, len(expo["outs"]), len(expo["results"])))
print("OK")
