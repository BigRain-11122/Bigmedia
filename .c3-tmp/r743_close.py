# -*- coding: utf-8 -*-
# R743 close: state.json (tick/log/ts/task/focus) + status-export refresh.
# Chinese payload read from r743_payload.json (encoding law: script=ASCII).
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
payload = json.loads(
    (ROOT / ".c3-tmp" / "r743_payload.json").read_text(encoding="utf-8"))

sp = ROOT / "src" / "os" / "state.json"
state = json.loads(sp.read_text(encoding="utf-8"))
now = datetime.now()
stamp = now.strftime("%Y-%m-%d %H:%M:%S")
entry = now.strftime("%Y-%m-%d %H:%M") + " " + payload["log"]
state["tick"] = int(state.get("tick", 0)) + 1
state["log"].append(entry)
state["ts"] = stamp
state["task"] = payload["log"][:60]
state["focus"] = payload["focus"]
sp.write_text(json.dumps(state, ensure_ascii=False, indent=1),
              encoding="utf-8")

ep = ROOT / "docs" / "status-export.json"
ex = json.loads(ep.read_text(encoding="utf-8"))
ex["export_ts"] = stamp
ex["outs"][0][1] = payload["os_row"]
ex["live"][0][1] = payload["live1"]
ex["live"][1][1] = payload["live2"]
ex["live"][2][1] = payload["live3"]
ex["results"].insert(0, ["743", entry])
ep.write_text(json.dumps(ex, ensure_ascii=False, indent=1),
              encoding="utf-8")
print("CLOSED tick=%s ts=%s task=%s" % (state["tick"], stamp,
                                        state["task"][:40]))
