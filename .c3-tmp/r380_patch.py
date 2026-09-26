# -*- coding: utf-8 -*-
# R380 log-line honesty patch: probe count at close time (20 warn incl. transient account-ahead)
# + in-round self-check note (double date prefix bug caught by loop_health, fixed same round).
import io, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sp = os.path.join(ROOT, "src", "os", "state.json")
st = json.load(io.open(sp, encoding="utf-8"))
old = (u"④三探针全绿（board 0 FAIL 5 题 10 稿 5 in production/readiness 3 阻塞皆外部 CEO 面 0 发现〔renders 台账零扰动〕"
       u"/loop_health 0 FAIL 19 WARN 皆在案史实）；")
new = (u"④三探针全绿（board 0 FAIL 5 题 10 稿 5 in production/readiness 3 阻塞皆外部 CEO 面 0 发现〔renders 台账零扰动〕"
       u"/loop_health 0 FAIL 20 WARN〔19 在案史实+1 account-ahead tick380>beats379=轮内瞬态·beat 落地自平 R173/R180 先例〕"
       u"·收账脚本日期前缀双写笔误=loop_health 当场咬住即修=轮内自检闭环·操作红如实入账）；")
assert old in st["log"][-1], "anchor not found"
st["log"][-1] = st["log"][-1].replace(old, new)
json.dump(st, io.open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("patched OK")
