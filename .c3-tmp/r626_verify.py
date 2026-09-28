# r626_verify.py -- post-close verification for R626 idle-fast batch-commit round evidence (ASCII output only)
# generation law per R615 addendum + R618 digit-expectation list: filename replace +
# enumerated 7-item number-expectation (uppercase R and bare digits replaced item by item)
import io, json, os, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = os.path.join(ROOT, "src", "os", "state.json")
XP = os.path.join(ROOT, "docs", "status-export.json")

st = json.load(io.open(SP, encoding="utf-8"))
xp = json.load(io.open(XP, encoding="utf-8"))

checks = []
# (1) tick == 626
checks.append(("TICK_626", st.get("tick") == 626))
ts = st.get("ts", "")
checks.append(("TS_ASCII_SECMARK", bool(re.match(r"^2026-09-28 \d{2}:\d{2}:\d{2}$", ts))))
# (2) task round header R626:
task = st.get("task", "")
checks.append(("TASK_STARTS_R626", task.startswith("R626:")))
checks.append(("TASK_LEN_60", len(task) <= 60))
# (3) log tail is R626 line with window count 6/6 + batch commit wording
log = st.get("log", [])
tail_last = log[-1] if log else ""
checks.append(("LOG_TAIL_IS_R626", " R626: " in tail_last and u"新窗 6/6 满=R621-R626" in tail_last and u"batch commit 收账+push" in tail_last))
# (6) log count >= 651 (pre-close 650 + R626 line)
checks.append(("LOG_COUNT_INCREASED", len(log) >= 651))
# (4) focus points to next round R627 + baseline r626_lednew5 + new window 1/6
focus = st.get("focus", "")
checks.append(("FOCUS_STARTS_R627", focus.startswith("R627:")))
checks.append(("FOCUS_BASELINE_R626", "r626_lednew5.txt" in focus))
checks.append(("FOCUS_WINDOW_1_OF_6", "R627-R632" in focus and u"1/6" in focus and u"满 6=R632" in focus))
# export freshness + OS row
checks.append(("EXPORT_TS_FRESH", bool(re.match(r"^2026-09-28T\d{2}:\d{2}:\d{2}\+08:00$", xp.get("export_ts", "")))))
osrow = None
for row in xp.get("outs", []):
    if row and row[0] == u"OS 循环":
        osrow = row[1]
# (5) OS row: tick 626 + R626 + 6/6
checks.append(("EXPORT_OS_ROW_TICK626", osrow is not None and u"tick 626" in osrow and u"R626" in osrow and u"6/6" in osrow))
checks.append(("PRODUCTION_OPEN", st.get("production") == "open"))

# (7) header line VERIFY_R626 + summary
lines = ["VERIFY_R626 state=%s ts=%s task_head=%r" % (st.get("tick"), ts, task[:20])]
ok = True
for name, val in checks:
    lines.append("%s=%s" % (name, "PASS" if val else "FAIL"))
    ok = ok and val
lines.append("VERIFY_RESULT=" + ("ALL_PASS" if ok else "HAS_FAIL"))
out = "\n".join(lines)
with io.open(os.path.join(ROOT, ".c3-tmp", "r626_verify.txt"), "w", encoding="utf-8") as fh:
    fh.write(out + "\n")
print(out)
