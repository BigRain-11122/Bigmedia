# -*- coding: utf-8 -*-
# r615_addendum.py -- end-of-round op-red note (R585 precedent): verify template generation law
import io, json, time

SP = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
st = json.load(io.open(SP, encoding="utf-8"))
assert st["tick"] == 615 and " R615: " in st["log"][-1], "state not in R615 post-close state"

now_hm = time.strftime("%H:%M")
st["log"].append(
    u"2026-09-28 " + now_hm + u" R615 轮末补记（操作红如实入账·R585 在案同型）：verify 首跑=r614_verify 模板仅文件名"
    u"替换（r614→r615）·数字预期面全数陈旧（TICK_614/task R614/log tail R614/OS row tick 614 等六项伪 FAIL）——"
    u"数据面零损伤（state.json/status-export.json 由 close 件 json.dump 直写 UTF-8 正确·五面实读复核即证）·"
    u"重写 r615_verify.py 数字预期后 12/12 ALL_PASS；**R616 起 verify 生成律=文件名替换+数字预期同步改**"
    u"（tick 值/task 轮号/log tail 轮号/focus 次轮号+baseline 名/OS row tick 口径/LOG_COUNT 下限——单纯 rN 字符串"
    u"替换不触数字检查面·R612 生成序律同族坑）+focus 区间名补正一起（窗 2/6=R615-R620·close 件漏写区间名"
    u"verify 咬住=检查面有效实证）"
)
json.dump(st, io.open(SP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ADDENDUM OK: log_count=%d" % len(st["log"]))
