# R351 fix: strip duplicated date prefix in log[-1] + append honest postscript entry
import json, os
from datetime import datetime

R = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(R, ".."))
SP = os.path.join(ROOT, "src", "os", "state.json")
now = datetime.now()
stamp = now.strftime("%Y-%m-%d %H:%M")
ts_full = now.strftime("%Y-%m-%d %H:%M:%S")

with open(SP, encoding="utf-8") as f:
    st = json.load(f)
assert st["tick"] == 351, "tick anchor mismatch"
assert st["log"][-1].startswith("2026-09-26 2026-09-26 07:53 R351:"), "bad-prefix anchor mismatch"
st["log"][-1] = st["log"][-1][len("2026-09-26 "):]  # strip duplicated date prefix
assert st["log"][-1].startswith("2026-09-26 07:53 R351:"), "fix assert failed"

post = (
    "2026-09-26 %s R351 轮末补记（收账写入坑如实入账·自检闭环）：r351_close.py 模板串日期双写"
    "（'2026-09-26 %%s' 误叠 stamp 已含日期）致 R351 log 行首双日期·loop_health 即时亮 log-ts FAIL 1——"
    "一次性 python 修复（strip 首段重复日期 11 字符+断言+json.loads 校验）·"
    "坑沉淀=close 脚本行首时间戳单源自 stamp 一处拼接（与 R322 replace 多行锚坑同面=state.json 收账一律 python 单次脚本律已遵守·本坑为脚本内拼接笔误）"
) % stamp
st["log"].append(post)
st["ts"] = ts_full
st["task"] = st["log"][-2].split("R351: ", 1)[1][:60]

tmp = SP + ".tmp"
with open(tmp, "w", encoding="utf-8", newline="\n") as f:
    json.dump(st, f, ensure_ascii=False, indent=1)
with open(tmp, encoding="utf-8") as f:
    json.load(f)
os.replace(tmp, SP)
with open(SP, encoding="utf-8") as f:
    json.load(f)
print("OK fixed, log entries =", len(st["log"]))
