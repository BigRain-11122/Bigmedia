# -*- coding: utf-8 -*-
"""One-shot state.json log correction: probe numbers to true final readings + PS pitfall note."""
import io

P = "src/os/state.json"
OLD = ("⑨三探针=board 0 FAIL/readiness 3 阻塞皆外部 CEO 项/loop_health 0 FAIL 6 WARN "
       "皆在案史实（tick172=done172 对账平）；例行件：")
NEW = ("⑨三探针=board 0 FAIL（5 题 10 稿·exit 0）/readiness 3 阻塞皆外部 CEO 项+1 发现"
       "（render-unannot bs-002=在链件诚实预期红：非「测试件·非成品」亦未到「成品·批次」态"
       "·E8/M4/F-002 登记落成品标即清·下轮范围）/loop_health 0 FAIL 7 WARN（6 在案史实"
       "+account-ahead tick173>done172=轮内瞬态·beat 落地自平）；"
       "**收账踩坑实录（PS5.1 新坑入账）**：Add-Content 双引号串反引号=转义符"
       "（`b=退格注入 0x08+`v=竖tab 拆行+反引号吞字符）→renders note/station-reviews 行腐蚀"
       "·readiness 揭假名捕获 s-002-…（render-stale）——修复法=弃 shell 传中文内容"
       "·write_file 落字面 python 修复脚本（.bs002-tmp/fix_ledgers.py）重写两行"
       "·复跑 readiness=stale 清零（余 1 发现=在链预期红如实留）；例行件：")

t = io.open(P, encoding="utf-8").read()
assert t.count(OLD) == 1
io.open(P, "w", encoding="utf-8", newline="\n").write(t.replace(OLD, NEW))
import json
d = json.load(io.open(P, encoding="utf-8"))
print("state.json valid JSON, tick", d["tick"], "log", len(d["log"]))
