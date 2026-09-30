# -*- coding: utf-8 -*-
# R735 closeout: state.json tick+1/log/ts/task + status-export refresh.
# ASCII source; Chinese payload lives in r735_closespec.json (encoding law).
import io
import json
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
spec = json.load(io.open(REPO / ".c3-tmp" / "r735_closespec.json",
                         encoding="utf-8"))
now = time.strftime("%Y-%m-%d %H:%M:%S")
hm = now[11:16]
log_line = "%s %s" % (now[:10], hm) + " " + spec["log_body"]

sp = REPO / "src" / "os" / "state.json"
st = json.load(io.open(sp, encoding="utf-8"))
st["tick"] = int(st.get("tick", 734)) + 1
st.setdefault("log", []).append(log_line)
st["ts"] = now
st["task"] = spec["log_body"][:60]
io.open(sp, "w", encoding="utf-8").write(
    json.dumps(st, ensure_ascii=False, indent=1))

ep = REPO / "docs" / "status-export.json"
ex = json.load(io.open(ep, encoding="utf-8"))
ex["export_ts"] = now
ex["outs"][0][1] = spec["os_row"]
ex["results"].insert(0, [str(st["tick"]), log_line])
if len(ex["results"]) > 20:
    ex["results"] = ex["results"][:20]
ex["live"] = spec["live_rows"]
io.open(ep, "w", encoding="utf-8").write(
    json.dumps(ex, ensure_ascii=False, indent=1))

print("CLOSE_OK tick=%d ts=%s" % (st["tick"], now))
print("TASK=%s" % st["task"].encode("unicode_escape")[:120])
