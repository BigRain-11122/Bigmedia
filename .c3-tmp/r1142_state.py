# -*- coding: utf-8 -*-
# R1142 declared-idle state update via RAW targeted string replacement
# (keeps on-disk quirks, e.g. the 2-space watermark ts indent; no full re-dump).
# Chinese payload from r1142_payload.txt; script body ASCII per encoding law.
import io, json, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
ST = ROOT + r"\src\os\state.json"
PAY = ROOT + r"\.c3-tmp\r1142_payload.txt"

raw = io.open(ST, encoding="utf-8").read()
st = json.loads(raw)
lines = [l for l in io.open(PAY, encoding="utf-8").read().split("\n") if l.strip()]
body = lines[0].strip()    # log line body, starts with "R1142:"
focus = lines[1].strip()   # new focus value

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
full_log = now[:16] + " " + body

assert st["tick"] == 1141, "tick drift"
assert st["log"][-1].startswith("2026-10-03 20:34 R1141"), "log tail drift"
assert st["ts"] == "2026-10-03 20:34:20", "ts drift"
assert '"' not in body and "\\" not in body, "log body needs json escaping"

# 1. tick
a = '"tick": 1141,'
assert raw.count(a) == 1, "tick anchor not unique"
raw = raw.replace(a, '"tick": 1142,', 1)

# 2. log append + top-level ts (single structural anchor; last log entry has NO trailing comma)
anchor = '"\n  ],\n  "ts": "2026-10-03 20:34:20",'
assert raw.count(anchor) == 1, "log-close anchor not unique: %d" % raw.count(anchor)
raw = raw.replace(anchor, '",\n    "' + full_log + '"\n  ],\n  "ts": "' + now + '",', 1)

# 3. watermark ts (quirk-preserving 2-space indent line, followed by "law")
wa = '\n  "ts": "2026-10-03 20:34:20",\n    "law":'
assert raw.count(wa) == 1, "watermark ts anchor not unique"
raw = raw.replace(wa, '\n  "ts": "' + now + '",\n    "law":', 1)

# 4. task
ta = '"task": ' + json.dumps(st["task"], ensure_ascii=False)
assert raw.count(ta) == 1, "task anchor not unique"
raw = raw.replace(ta, '"task": ' + json.dumps(body[:60], ensure_ascii=False), 1)

# 5. focus
fa = '"focus": ' + json.dumps(st["focus"], ensure_ascii=False)
assert raw.count(fa) == 1, "focus anchor not unique"
raw = raw.replace(fa, '"focus": ' + json.dumps(focus, ensure_ascii=False), 1)

# verify + write
chk = json.loads(raw)
assert chk["tick"] == 1142 and chk["ts"] == now
assert len(chk["log"]) == len(st["log"]) + 1 and chk["log"][-1] == full_log
assert chk["task"] == body[:60] and chk["focus"] == focus
assert chk["decisions_watermark"]["ts"] == now
assert chk["decisions_watermark"]["dnums"] == st["decisions_watermark"]["dnums"]
io.open(ST, "w", encoding="utf-8", newline="").write(raw)
print("OK tick=%s ts=%s log_len=%d" % (chk["tick"], chk["ts"], len(chk["log"])))
print("task=%s" % chk["task"])
print("log_tail_prefix=%s" % chk["log"][-1][:90])
