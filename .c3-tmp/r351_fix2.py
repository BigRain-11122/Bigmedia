# R351 fix2: strip duplicated date prefix in postscript entry + amend its text honestly (in-flight round entry)
import json, os
from datetime import datetime

R = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(R, ".."))
SP = os.path.join(ROOT, "src", "os", "state.json")
now = datetime.now()
ts_full = now.strftime("%Y-%m-%d %H:%M:%S")

with open(SP, encoding="utf-8") as f:
    st = json.load(f)
assert st["tick"] == 351, "tick anchor mismatch"
assert st["log"][-1].startswith("2026-09-26 2026-09-26 07:53 R351 轮末补记"), "postscript anchor mismatch"
st["log"][-1] = st["log"][-1][len("2026-09-26 "):]
assert st["log"][-1].startswith("2026-09-26 07:53 R351 轮末补记"), "fix2 assert failed"
old = "本坑为脚本内拼接笔误）"
assert old in st["log"][-1], "amend anchor mismatch"
st["log"][-1] = st["log"][-1].replace(old, "本坑为脚本内拼接笔误·补记行自身同型即现即修=同笔误两案一并定谳）")
st["ts"] = ts_full

tmp = SP + ".tmp"
with open(tmp, "w", encoding="utf-8", newline="\n") as f:
    json.dump(st, f, ensure_ascii=False, indent=1)
with open(tmp, encoding="utf-8") as f:
    json.load(f)
os.replace(tmp, SP)
with open(SP, encoding="utf-8") as f:
    json.load(f)
print("OK fix2 done, log entries =", len(st["log"]))
