# r614_verify.py -- post-close verification for R614 batch commit evidence (ASCII output only)
import io, json, os, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = os.path.join(ROOT, "src", "os", "state.json")
XP = os.path.join(ROOT, "docs", "status-export.json")

st = json.load(io.open(SP, encoding="utf-8"))
xp = json.load(io.open(XP, encoding="utf-8"))

checks = []
checks.append(("TICK_614", st.get("tick") == 614))
ts = st.get("ts", "")
checks.append(("TS_ASCII_SECMARK", bool(re.match(r"^2026-09-28 \d{2}:\d{2}:\d{2}$", ts))))
task = st.get("task", "")
checks.append(("TASK_STARTS_R614", task.startswith("R614:")))
checks.append(("TASK_LEN_60", len(task) <= 60))
log = st.get("log", [])
checks.append(("LOG_TAIL_IS_R614", bool(log) and " R614: " in log[-1] and "batch commit" in log[-1]))
checks.append(("LOG_COUNT_INCREASED", len(log) >= 637))
focus = st.get("focus", "")
checks.append(("FOCUS_STARTS_R615", focus.startswith("R615:")))
checks.append(("FOCUS_BASELINE_R614", "r614_lednew5.txt" in focus))
checks.append(("FOCUS_WINDOW_1_6", "R615-R620" in focus))
checks.append(("EXPORT_TS_FRESH", bool(re.match(r"^2026-09-28T\d{2}:\d{2}:\d{2}\+08:00$", xp.get("export_ts", "")))))
osrow = None
for row in xp.get("outs", []):
    if row and row[0] == u"OS 循环":
        osrow = row[1]
checks.append(("EXPORT_OS_ROW_TICK614", osrow is not None and u"tick 614" in osrow and u"R609-R614" in osrow))
checks.append(("PRODUCTION_OPEN", st.get("production") == "open"))

lines = ["VERIFY_R614 state=%s ts=%s task_head=%r" % (st.get("tick"), ts, task[:20])]
ok = True
for name, val in checks:
    lines.append("%s=%s" % (name, "PASS" if val else "FAIL"))
    ok = ok and val
lines.append("VERIFY_RESULT=" + ("ALL_PASS" if ok else "HAS_FAIL"))
out = "\n".join(lines)
with io.open(os.path.join(ROOT, ".c3-tmp", "r614_verify.txt"), "w", encoding="utf-8") as fh:
    fh.write(out + "\n")
print(out)
