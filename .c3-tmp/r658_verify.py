# -*- coding: utf-8 -*-
# R658 close verify rig (length-alignment law: substrings, no full-tail equality)
import io, json, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = []
def chk(name, cond):
    OUT.append("CHECK_" + name + ": " + ("PASS" if cond else "FAIL"))

st = json.load(io.open(ROOT + r"\src\os\state.json", encoding="utf-8"))
ex = json.load(io.open(ROOT + r"\docs\status-export.json", encoding="utf-8"))
OUT.append("NOW: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
OUT.append("TICK: " + str(st.get("tick")))
OUT.append("TS: " + str(st.get("ts")))
OUT.append("TASK: " + st.get("task", "")[:60])
OUT.append("LOG_N: " + str(len(st.get("log", []))))
tail = st.get("log", [])[-1] if st.get("log") else ""
OUT.append("LOG_TAIL_HEAD: " + tail[:60])

chk("tick_658", st.get("tick") == 658)
chk("ts_today", str(st.get("ts", "")).startswith("2026-09-29 05:5"))
chk("task_prefix", st.get("task", "").startswith("R658: "))
chk("task_len_60", len(st.get("task", "")) == 60)
chk("log_tail_r658", tail.startswith("2026-09-29 ") and "R658: " in tail[:30])
chk("tail_has_82", "#82" in tail[:200])
chk("tail_has_probes", "loop_health 3 FAIL" in tail)
chk("tail_has_next", "R659" in tail[-200:])
chk("focus_r659", st.get("focus", "").startswith("R659: "))
chk("production_open", st.get("production") == "open")
chk("export_ts_fresh", str(ex.get("export_ts", "")).startswith("2026-09-29T05:55"))
outs0 = ex.get("outs", [])[0]
chk("outs0_tick658", outs0[1].startswith("tick 658"))
res = ex.get("results", [])
chk("res0_658", res and res[0][0] == "658")
chk("res0_has_fix", res and "标题位律" in res[0][1])
chk("res1_657", len(res) > 1 and res[1][0] == "657")
dfix = any(d.get("n") == "数据分析部" and "自驱面计量行 live" in d.get("t", "")
           for d in ex.get("depts", []))
chk("dept_data_fixed", dfix)

fails = [o for o in OUT if o.startswith("CHECK_") and o.endswith("FAIL")]
OUT.append("ALL_PASS: " + ("YES" if not fails else "NO(" + str(len(fails)) + ")"))
io.open(ROOT + r"\.c3-tmp\r658_verify.txt", "w", encoding="utf-8").write("\n".join(OUT))
print("RIG_DONE lines=" + str(len(OUT)) + " fails=" + str(len(fails)))
