# r488_verify.py - post-accounting JSON validation gate + final state readout (new file, OUTP new, utf-8)
import io, os, json, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r488_verify.txt")
L = []
def w(s):
    L.append(str(s))

# 1) state.json validation + key fields
sp = os.path.join(ROOT, "src", "os", "state.json")
with io.open(sp, "r", encoding="utf-8") as f:
    st = json.load(f)
w("state_json=OK tick=%d production=%s" % (st["tick"], st["production"]))
w("state_ts=%s" % st["ts"])
w("state_task_head=%s" % st["task"][:40])
w("log_tail2:")
for ln in st["log"][-2:]:
    w("  " + ln[:80])
w("focus_head=%s" % st["focus"][:30])
w("focus_tail=%s" % st["focus"][-60:])

# 2) status-export.json validation + tick faces + mojibake gone
pp = os.path.join(ROOT, "docs", "status-export.json")
with io.open(pp, "r", encoding="utf-8") as f:
    raw = f.read()
se = json.loads(raw)
w("export_json=OK export_ts=%s" % se["export_ts"])
w("outs0_e1_head=%s" % se["outs"][0][1][:60])
w("outs0_e2_head=%s" % se["outs"][0][2][:60])
w("results0=%s | %s" % (se["results"][0][0], se["results"][0][1][:80]))
bad = [ch for ch in ("收謦", "收讳", "收记", "回扯", "定谴") if ch in raw]
w("mojibake_left=%s" % (bad or "NONE"))

with io.open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("\n".join(L))
