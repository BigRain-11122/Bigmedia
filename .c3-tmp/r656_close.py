# -*- coding: utf-8 -*-
"""R656+R657 close verify rig (replicates r655_verify2 length-alignment law). ASCII-safe output."""
import io, os, json, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = []
def p(k, v):
    OUT.append(k + ": " + str(v))
def chk(name, cond):
    p("CHECK_" + name, "PASS" if cond else "FAIL")

st = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
ex = json.load(io.open(os.path.join(ROOT, "docs", "status-export.json"), encoding="utf-8"))

p("NOW", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
p("TICK", st.get("tick"))
p("TS", st.get("ts"))
p("TASK_HEAD", st.get("task", "")[:30])
p("FOCUS_HEAD", st.get("focus", "")[:12])
log = st.get("log", [])
p("LOG_N", len(log))
tail = log[-1] if log else ""
p("LOG_TAIL_HEAD", tail[:60])
p("LOG_TAIL_LEN", len(tail))

chk("tick_657", st.get("tick") == 657)
chk("ts_fresh_0529", str(st.get("ts", "")).startswith("2026-09-29 05:29"))
chk("task_prefix", st.get("task", "").startswith(u"断洞双记+declared-idle"))
chk("focus_r658", st.get("focus", "").startswith("R658: "))
chk("log_tail_is_new", "R656+R657" in tail[:40])
chk("log_tail_has_absorb", "双记 tick655" in tail)
chk("log_tail_has_idle4", "declared-idle 空轮判定第四连" in tail)
chk("log_tail_has_window", "R654-R657 窗提前闭" in tail)
chk("log_tail_has_next", "R658 可领序" in tail)
chk("prev_tail_r655_addendum", any("R655 轮末补记" in l for l in log[-4:-1]))
chk("production_open", st.get("production") == "open")

p("EXPORT_TS", ex.get("export_ts"))
chk("export_ts_fresh", str(ex.get("export_ts", "")).startswith("2026-09-29T05:29"))
outs0 = ex.get("outs", [])[0]
p("OUTS0_HEAD", outs0[1][:13])
chk("outs0_tick657", outs0[1].startswith("tick 657"))
res = ex.get("results", [])
p("RESULTS_COUNT", len(res))
p("RES0_KEY", res[0][0] if res else "NONE")
chk("res0_657", res and res[0][0] == "657")
chk("res0_has_dual", res and "断洞双记" in res[0][1])
chk("res1_655", len(res) > 1 and res[1][0] == "655")

fails = [o for o in OUT if o.startswith("CHECK_") and o.endswith("FAIL")]
p("ALL_PASS", "YES" if not fails else "NO(" + str(len(fails)) + ")")
io.open(os.path.join(ROOT, ".c3-tmp", "r656_close.txt"), "w", encoding="utf-8").write("\n".join(OUT))
print("RIG_DONE lines=" + str(len(OUT)) + " fails=" + str(len(fails)))
