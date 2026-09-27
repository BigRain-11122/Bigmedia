# -*- coding: utf-8 -*-
# R585 addendum: record op-red (PS `>` redirection mojibake evidence file, R562 same-type recurrence)
# log-line only per R562 precedent; tick/ts/task stay as close values (heartbeat face unchanged).
import io, json, os, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = os.path.join(ROOT, "src", "os", "state.json")

now_hm = time.strftime("%H:%M")
state = json.load(io.open(SP, encoding="utf-8"))
assert state["tick"] == 585, "expected tick 585, got %s" % state["tick"]

addendum = (
    u"2026-09-28 " + now_hm + u" R585 轮末补记（操作红如实入账·R562 在案同型再犯）：verify 首跑输出走 PS `>` 重定向"
    u"落乱码证据件（.c3-tmp/r585_verify_gen.txt·UTF-16/GBK 混读态·shell 显示层 Binary 拒显）——零数据件副作用"
    u"（state.json/status-export.json 由 close 件内 python json.dump 直写=UTF-8 正确·收账本体不受影响·log 尾 607 条"
    u"单增实证）→正法即走=r585_verify.py 件内 io.open 写 UTF-8（r585_verify.txt 复核五面全过：tick 585/ts 01:53:21/"
    u"task 60 字/log 尾 R585 行/focus R586 基线 r585_lednew5.txt/export_ts 同步）·乱码件留档为 op-red 证据不删"
    u"·防再犯注第三次重申=R562 律「close/verify 输出捕获一律 python 件内 io.open 写 UTF-8·PS 管道重定向对证据件永不用」"
    u"〔R541/R562 本件三犯·下轮起 verify 步直接套用 r585_verify.py 模板零新写〕"
)

state["log"].append(addendum)
json.dump(state, io.open(SP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ADDENDUM OK: log_count=%d" % len(state["log"]))
