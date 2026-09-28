# r630_verify.py -- post-close verification for R630 REAL round (P-2026-09-28-02 order received/acked/adapted)
# digit-expectation list per R618 law: uppercase R and bare digits replaced item by item from r629 template
import io, json, os, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = os.path.join(ROOT, "src", "os", "state.json")
XP = os.path.join(ROOT, "docs", "status-export.json")

st = json.load(io.open(SP, encoding="utf-8"))
xp = json.load(io.open(XP, encoding="utf-8"))

checks = []
# (1) tick == 630
checks.append(("TICK_630", st.get("tick") == 630))
ts = st.get("ts", "")
checks.append(("TS_ASCII_SECMARK", bool(re.match(r"^2026-09-28 \d{2}:\d{2}:\d{2}$", ts))))
# (2) task round header R630:
task = st.get("task", "")
checks.append(("TASK_STARTS_R630", task.startswith("R630:")))
checks.append(("TASK_LEN_60", len(task) <= 60))
# (3) log tail is R630 real-round line with order id
log = st.get("log", [])
tail_last = log[-1] if log else ""
checks.append(("LOG_TAIL_IS_R630", " R630: " in tail_last and "P-2026-09-28-02" in tail_last and u"实活轮" in tail_last))
# (6) log count >= 655 (pre-close 654 + R630 line)
checks.append(("LOG_COUNT_INCREASED", len(log) >= 655))
# (4) focus points to next round R631 + baseline r630_lednew5 + DIGEST-v9 production
focus = st.get("focus", "")
checks.append(("FOCUS_STARTS_R631", focus.startswith("R631:")))
checks.append(("FOCUS_BASELINE_R630", "r630_lednew5.txt" in focus))
checks.append(("FOCUS_DIGEST_V9", "DIGEST-v9" in focus and "F-053" in focus))
# export freshness + OS row
checks.append(("EXPORT_TS_FRESH", bool(re.match(r"^2026-09-28T\d{2}:\d{2}:\d{2}\+08:00$", xp.get("export_ts", "")))))
osrow = None
for row in xp.get("outs", []):
    if row and row[0] == u"OS 循环":
        osrow = row[1]
# (5) OS row: tick 630 + R630
checks.append(("EXPORT_OS_ROW_TICK630", osrow is not None and u"tick 630" in osrow and u"R630" in osrow))
checks.append(("PRODUCTION_OPEN", st.get("production") == "open"))

# (7) header line VERIFY_R630 + summary
lines = ["VERIFY_R630 state=%s ts=%s task_head=%r" % (st.get("tick"), ts, task[:16])]
ok = True
for name, val in checks:
    lines.append("%s=%s" % (name, "PASS" if val else "FAIL"))
    ok = ok and val
lines.append("VERIFY_RESULT=" + ("ALL_PASS" if ok else "HAS_FAIL"))
out = "\n".join(lines)
with io.open(os.path.join(ROOT, ".c3-tmp", "r630_verify.txt"), "w", encoding="utf-8") as fh:
    fh.write(out + "\n")
print(out)
