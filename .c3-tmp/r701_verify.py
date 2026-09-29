# -*- coding: utf-8 -*-
# R701 authoritative verify (R669/R670 law: run verify right after close, read it back)
import io, json, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
res = []

st = json.load(io.open(ROOT + r"\src\os\state.json", encoding="utf-8"))
res.append("tick=%s (expect 701)" % st.get("tick"))
res.append("ts=%s (fresh=%s)" % (st.get("ts"), st.get("ts","").startswith("2026-09-29 20:0")))
res.append("task_len=%d (expect <=60)" % len(st.get("task","")))
res.append("task=%s" % st.get("task","")[:60])
res.append("production=%s" % st.get("production"))
res.append("log_tail=%s" % st["log"][-1][:80])
res.append("log_count=%d" % len(st["log"]))

ex = json.load(io.open(ROOT + r"\docs\status-export.json", encoding="utf-8"))
res.append("export_ts=%s" % ex.get("export_ts"))
res.append("results_tail_tick=%s (expect 701)" % ex["results"][-1][0])
os_row = [r for r in ex.get("outs", []) if r and r[0] == "OS 循环"]
res.append("os_row_head=%s" % (os_row[0][1][:40] if os_row else "MISSING"))
res.append("live_rows=%d (expect 3)" % len(ex.get("live", [])))
res.append("live_recent=%s" % ex["live"][1][0][:100])

t = io.open(ROOT + r"\output\finished.md", encoding="utf-8").read()
res.append("finished_F062=%s" % ("F-062 登记（R701）" in t))
t2 = io.open(ROOT + r"\output\renders\README.md", encoding="utf-8").read()
res.append("renders_lc008_done=%s" % ("F-062·冗余池第五件视频" in t2))
res.append("renders_unannot_still=%s" % ("待收官腿 E8+ASR+E4+M4→F-062" in t2))  # expect False
t3 = io.open(ROOT + r"\docs\reviews\review-20260929-lc008-v1.md", encoding="utf-8").read()
res.append("review_exists=%s len=%d" % (len(t3) > 5000, len(t3)))
t4 = io.open(ROOT + r"\docs\release-schedule-v1.md", encoding="utf-8").read()
res.append("sched_v20=%s" % ("v2.0 2026-09-29 R701" in t4))
res.append("sched_ammo5=%s" % ("视频号冗余弹药 5 件" in t4))
t5 = io.open(ROOT + r"\docs\reviews\station-reviews.md", encoding="utf-8").read()
res.append("station_R701=%s" % ("R701 收官腿" in t5))
t6 = io.open(ROOT + r"\docs\reviews\expert-calls.md", encoding="utf-8").read()
res.append("ec_R701_row=%s" % ("20260929195424-E4-audience" in t6))
t7 = io.open(ROOT + r"\docs\self-improvement-queue.md", encoding="utf-8").read()
res.append("queue_R701_out=%s" % ("R701 收官腿毕" in t7))
t8 = io.open(ROOT + r"\data\sources\lc008\README.md", encoding="utf-8").read()
res.append("lc008_close=%s" % ("收官毕（R701）" in t8))
t9 = io.open(ROOT + r"\docs\reviews\expert-verdicts\20260929195424-E4-audience.md", encoding="utf-8").read()
res.append("e4_verdict=%s" % (len(t9) > 500))

out = "\n".join(res)
io.open(ROOT + r"\.c3-tmp\r701_verify.txt", "w", encoding="utf-8").write(out)
print(out)
