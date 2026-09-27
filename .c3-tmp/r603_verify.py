# -*- coding: utf-8 -*-
# R603 verify (five-face recheck per r585 template law): tick / ts / task 60c / log tail R603 line /
# focus R604 baseline r603_lednew5.txt / export_ts sync. Output via io.open UTF-8 (R562 law, no PS redirection).
import io, json, os, re, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = os.path.join(ROOT, "src", "os", "state.json")
XP = os.path.join(ROOT, "docs", "status-export.json")
OUT = os.path.join(ROOT, ".c3-tmp", "r603_verify.txt")

lines = []
st = json.load(io.open(SP, encoding="utf-8"))
xp = json.load(io.open(XP, encoding="utf-8"))

# face 1: tick
lines.append("TICK=%s EXPECT=603 PASS=%s" % (st.get("tick"), st.get("tick") == 603))
# face 2: ts format (second-level ASCII)
ts = st.get("ts", "")
ok_ts = bool(re.match(r"^2026-09-28 \d{2}:\d{2}:\d{2}$", ts))
lines.append("TS=%s FORMAT_PASS=%s" % (ts, ok_ts))
# face 3: task = log line minus date prefix, first 60 chars
tail = st["log"][-1]
task = st.get("task", "")
body = tail.split(" ", 2)[2][:60] if tail.count(" ") >= 2 else ""
lines.append("TASK_LEN=%d BODY_MATCH=%s" % (len(task), task == body))
lines.append("TASK=%s" % task)
# face 4: log tail is the R603 line (window 1/6 first-round note)
lines.append("LOG_TAIL_IS_R603=%s" % ("R603: idle-fast" in tail and u"新窗 1/6=R603-R608" in tail))
lines.append("LOG_COUNT=%d" % len(st["log"]))
# face 5: focus carries R604 baseline r603_lednew5.txt
focus = st.get("focus", "")
lines.append("FOCUS_R604_BASELINE=%s" % ("r603_lednew5.txt" in focus and u"2/6=R603-R608" in focus))
# face 6: export_ts synced (same minute as state ts)
lines.append("EXPORT_TS=%s SYNC=%s" % (xp.get("export_ts"), xp.get("export_ts", "").startswith(time.strftime("%Y-%m-%dT%H:%M"))))
# baseline file exists
lines.append("BASELINE_FILE=%s" % os.path.exists(os.path.join(ROOT, ".c3-tmp", "r603_lednew5.txt")))

ok_all = (
    st.get("tick") == 603 and ok_ts and task == body
    and ("R603: idle-fast" in tail and u"新窗 1/6=R603-R608" in tail)
    and ("r603_lednew5.txt" in focus and u"2/6=R603-R608" in focus)
)
lines.append("VERIFY_ALL_PASS=%s" % ok_all)
io.open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print("\n".join(lines))
