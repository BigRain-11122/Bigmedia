# -*- coding: utf-8 -*-
# R962 format fix: restore canonical indent=1 + CRLF (text-mode default) format, add focus field.
import json, datetime

SP = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"

sj = json.load(open(SP, encoding="utf-8"))
assert int(sj["tick"]) == 962, "tick drift: %s" % sj["tick"]
assert len(sj["log"]) == 990, "log count drift: %d" % len(sj["log"])
assert sj["log"][-1].startswith("2026-10-02 09:05:1"), "R962 tail mismatch"
assert "2/6" in sj["log"][-1] and "waiting: supply-gated lane held" in sj["log"][-1]
assert "r962_check.py" in sj["log"][-1] and "r962_probes.py" in sj["log"][-1]
assert "done964>tick961" in sj["log"][-1]

sj["focus"] = ("R962: 声明窗新窗 2/6（实况变化即转全任务书）："
               "①OSS w3 切片 10-02 21:40 届窗即领（≥1 切片 ≤3 刀）"
               "②10-03 00:00 跨日先到=日界批收+10-03 日报补产+REACT 10-03 领件"
               "③#94 ① 10-04 记忆 ≤10KB 梳理窗④W41 周轮件=10-05（周报+自驱提案窗+CLOUD_LINE 首测）")

json.dump(sj, open(SP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# reload verification (r899 lesson: post-write json.load + assertions)
sj2 = json.load(open(SP, encoding="utf-8"))
assert sj2["log"][-1] == sj["log"][-1], "appended line mismatch after reload"
assert int(sj2["tick"]) == 962 and len(sj2["log"]) == 990
assert sj2["ts"] == sj["ts"] and sj2["task"].startswith("R962:")
assert sj2["production"] == "open"
assert sj2["focus"].startswith("R962:")

data = open(SP, "rb").read()
print("CLOSE-OK tick=%s ts=%s log_entries=%d crlf=%d lf=%d size=%d" % (
    sj2["tick"], sj2["ts"], len(sj2["log"]), data.count(b"\r\n"), data.count(b"\n"), len(data)))
