import json, re, datetime

BM = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = BM + r"\src\os\state.json"

src = open(SP, encoding="utf-8").read()
data = json.loads(src)
line = data["log"][-1]
assert line.startswith("2026-10-03 16:1x R1114")

fixed = line.replace("2026-10-03 16:1x R1114", "2026-10-03 16:0x R1114")
fixed = fixed.replace("三门全跑 16:1x", "三门全跑 16:0x")
assert "16:1x" not in fixed, "stale 16:1x remains"

old_json = json.dumps(line, ensure_ascii=False)
new_json = json.dumps(fixed, ensure_ascii=False)
assert src.count(old_json) == 1
src = src.replace(old_json, new_json, 1)

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
i_ts = src.rfind('"ts": "')
j_ts = src.find('"', i_ts + 7)
src = src[:i_ts] + '"ts": ' + json.dumps(now, ensure_ascii=False) + src[j_ts + 1:]

data2 = json.loads(src)
assert data2["log"][-1].startswith("2026-10-03 16:0x R1114")
assert data2["tick"] == 1114
assert data2["ts"] == now
assert data2["task"].startswith("declared-idle")
open(SP, "w", encoding="utf-8").write(src)
print("OK ts=%s logline_fixed" % now)
