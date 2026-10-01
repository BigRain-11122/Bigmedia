# r932_fix.py - fix literal minute placeholder in last log line (close-family format bug type 6)
import json, re, io, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
STATE = ROOT + r"\src\os\state.json"

with io.open(STATE, encoding="utf-8") as f:
    s = json.load(f)

assert s["tick"] == 932, "unexpected tick %s" % s["tick"]
last = s["log"][-1]
assert last.startswith("2026-10-02 04:0x "), "unexpected prefix: %r" % last[:20]

now = datetime.datetime.now()
fixed_prefix = now.strftime("%Y-%m-%d %H:%M")
last = last.replace("2026-10-02 04:0x", fixed_prefix, 1)
s["log"][-1] = last
s["ts"] = now.strftime("%Y-%m-%d %H:%M:%S")
s["task"] = last.split(" ", 2)[2][:60]

with io.open(STATE, "w", encoding="utf-8", newline="\n") as f:
    json.dump(s, f, ensure_ascii=False, indent=1)
    f.write("\n")

# post-write verification (R899 clause): timestamp must be real digits
with io.open(STATE, encoding="utf-8") as f:
    check = json.load(f)
cl = check["log"][-1]
m = re.match(r"^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})", cl)
assert m, "last log line still lacks real timestamp: %r" % cl[:20]
assert cl.startswith(m.group(1) + " " + m.group(2) + " ")
assert "x" not in cl[:16], "literal placeholder residue in ts prefix"
assert check["task"].startswith("R932:")
print("R932 fix OK: prefix=%s ts=%s" % (m.group(0), check["ts"]))
