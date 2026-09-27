# r618_verify.py -- post-close verification for R618 idle-fast round evidence (ASCII output only)
# generation law per R615 addendum + R618 third-offense hardening: filename replace +
# enumerated number-expectation list (uppercase R and bare digits must be replaced item by item)
import io, json, os, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = os.path.join(ROOT, "src", "os", "state.json")
XP = os.path.join(ROOT, "docs", "status-export.json")

st = json.load(io.open(SP, encoding="utf-8"))
xp = json.load(io.open(XP, encoding="utf-8"))

checks = []
checks.append(("TICK_618", st.get("tick") == 618))
ts = st.get("ts", "")
checks.append(("TS_ASCII_SECMARK", bool(re.match(r"^2026-09-28 \d{2}:\d{2}:\d{2}$", ts))))
task = st.get("task", "")
checks.append(("TASK_STARTS_R618", task.startswith("R618:")))
checks.append(("TASK_LEN_60", len(task) <= 60))
log = st.get("log", [])
tail_main = log[-2] if len(log) >= 2 else ""
tail_add = log[-1] if log else ""
checks.append(("LOG_TAIL_IS_R618", " R618: " in tail_main and u"本窗不 commit" in tail_main and u"新窗 4/6=R615-R620" in tail_main))
checks.append(("LOG_TAIL_ADDENDUM_R618", u"R618 轮末补记" in tail_add))
checks.append(("LOG_COUNT_INCREASED", len(log) >= 642))
focus = st.get("focus", "")
checks.append(("FOCUS_STARTS_R619", focus.startswith("R619:")))
checks.append(("FOCUS_BASELINE_R618", "r618_lednew5.txt" in focus))
checks.append(("FOCUS_WINDOW_5_6", "R615-R620" in focus and u"窗 5/6" in focus))
checks.append(("EXPORT_TS_FRESH", bool(re.match(r"^2026-09-28T\d{2}:\d{2}:\d{2}\+08:00$", xp.get("export_ts", "")))))
osrow = None
for row in xp.get("outs", []):
    if row and row[0] == u"OS 循环":
        osrow = row[1]
checks.append(("EXPORT_OS_ROW_TICK618", osrow is not None and u"tick 618" in osrow and u"R618" in osrow and u"4/6" in osrow))
checks.append(("PRODUCTION_OPEN", st.get("production") == "open"))

lines = ["VERIFY_R618 state=%s ts=%s task_head=%r" % (st.get("tick"), ts, task[:20])]
ok = True
for name, val in checks:
    lines.append("%s=%s" % (name, "PASS" if val else "FAIL"))
    ok = ok and val
lines.append("VERIFY_RESULT=" + ("ALL_PASS" if ok else "HAS_FAIL"))
out = "\n".join(lines)
with io.open(os.path.join(ROOT, ".c3-tmp", "r618_verify.txt"), "w", encoding="utf-8") as fh:
    fh.write(out + "\n")
print(out)
