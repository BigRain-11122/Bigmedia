# -*- coding: utf-8 -*-
# r1147 batch-close round: state.json update via RAW targeted string replacement
# (keeps on-disk quirks, e.g. the 2-space watermark ts indent; no full re-dump)
# + status-export.json refresh (export_ts / outs[0] / results append / live[0]).
# Chinese payload from r1147_payload.txt; script body ASCII per encoding law.
import io, json, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
ST = ROOT + r"\src\os\state.json"
EX = ROOT + r"\docs\status-export.json"
PAY = ROOT + r"\.c3-tmp\r1147_payload.txt"

raw = io.open(ST, encoding="utf-8").read()
st = json.loads(raw)
pl = [l for l in io.open(PAY, encoding="utf-8").read().split("\n") if l.strip()]
body = pl[0].strip()     # log line body, starts with "R1147:"
focus = pl[1].strip()    # new focus value
res_text = pl[2].strip() # results entry text (after timestamp prefix)
outs_text = pl[3].strip() # new outs[0] text

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
full_log = now[:16] + " " + body

assert st["tick"] == 1146, "tick drift"
assert st["log"][-1].startswith("2026-10-03 21:23 R1146"), "log tail drift"
assert st["ts"] == "2026-10-03 21:23:32", "ts drift"
assert '"' not in body and "\\" not in body, "log body needs json escaping"

# 1. tick
a = '"tick": 1146,'
assert raw.count(a) == 1, "tick anchor not unique"
raw = raw.replace(a, '"tick": 1147,', 1)

# 2. log append + top-level ts (single structural anchor; last log entry has NO trailing comma)
anchor = '"\n  ],\n  "ts": "2026-10-03 21:23:32",'
assert raw.count(anchor) == 1, "log-close anchor not unique: %d" % raw.count(anchor)
raw = raw.replace(anchor, '",\n    "' + full_log + '"\n  ],\n  "ts": "' + now + '",', 1)

# 3. watermark ts (quirk-preserving 2-space indent line, followed by "law")
wa = '\n  "ts": "2026-10-03 21:23:32",\n    "law":'
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

# verify + write state
chk = json.loads(raw)
assert chk["tick"] == 1147 and chk["ts"] == now
assert len(chk["log"]) == len(st["log"]) + 1 and chk["log"][-1] == full_log
assert chk["task"] == body[:60] and chk["focus"] == focus
assert chk["decisions_watermark"]["ts"] == now
assert chk["decisions_watermark"]["dnums"] == st["decisions_watermark"]["dnums"]
io.open(ST, "w", encoding="utf-8", newline="").write(raw)

# --- export refresh ---
eraw = io.open(EX, encoding="utf-8").read()
ex = json.loads(eraw)
assert ex["outs"][0][0] == "OS 循环", "outs[0] anchor drift"
had_nl = eraw.endswith("\n")
ex["export_ts"] = now
ex["outs"][0][1] = outs_text
ex["results"].append(["1147", now[:16] + " " + res_text])
ex["live"][0] = ["当前活：R1147 声明窗 6/6 batch close R1142-R1147 一盘 commit（并窗重置 0/6·waiting 10-04 日界三件）（" + now[11:16] + "）"]
out = json.dumps(ex, ensure_ascii=False, indent=1)
if had_nl:
    out += "\n"
io.open(EX, "w", encoding="utf-8", newline="").write(out)

print("OK tick=%s ts=%s log_len=%d" % (chk["tick"], chk["ts"], len(chk["log"])))
print("task=%s" % chk["task"])
print("log_tail_prefix=%s" % chk["log"][-1][:90])
print("export_ts=%s results_len=%d live0=%s" % (ex["export_ts"], len(ex["results"]), ex["live"][0][0][:60]))
