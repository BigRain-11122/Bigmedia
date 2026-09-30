# -*- coding: utf-8 -*-
# R743 export fix: r743_close.py crashed after state write (live rows are
# 1-element arrays -> index [0] not [1]). This script touches ONLY the
# export, reusing state's ts and last log entry (no double accounting).
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
payload = json.loads(
    (ROOT / ".c3-tmp" / "r743_payload.json").read_text(encoding="utf-8"))

sp = ROOT / "src" / "os" / "state.json"
state = json.loads(sp.read_text(encoding="utf-8"))
stamp = state["ts"]
entry = state["log"][-1]
assert "R743" in entry[:40], "last state log entry is not R743"
assert int(state["tick"]) == 743, "tick not 743"

ep = ROOT / "docs" / "status-export.json"
ex = json.loads(ep.read_text(encoding="utf-8"))
ex["export_ts"] = stamp
ex["outs"][0][1] = payload["os_row"]
ex["live"][0][0] = payload["live1"]
ex["live"][1][0] = payload["live2"]
ex["live"][2][0] = payload["live3"]
ex["results"].insert(0, ["743", entry])
ep.write_text(json.dumps(ex, ensure_ascii=False, indent=1),
              encoding="utf-8")
print("EXPORT_FIXED tick=%s ts=%s live0=%s..." % (
    state["tick"], stamp, payload["live1"][:24]))
