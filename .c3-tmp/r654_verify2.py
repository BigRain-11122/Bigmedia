# -*- coding: utf-8 -*-
"""R654 verify round 2: corrected expectation strings (R618 law - enumerate explicit values).
Data face already verified correct in round 1; this pass fixes 4 check-string authoring errors."""
import json, io, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
STATE = os.path.join(ROOT, "src", "os", "state.json")
EXPORT = os.path.join(ROOT, "docs", "status-export.json")

with io.open(STATE, "r", encoding="utf-8") as fh:
    s2 = json.load(fh)
with io.open(EXPORT, "r", encoding="utf-8") as fh:
    e2 = json.load(fh)

tail = s2["log"][-1]
checks = [
    ("TICK", s2["tick"], 654),
    ("PRODUCTION", s2["production"], "open"),
    ("LOG_COUNT", len(s2["log"]), 676),
    ("LOG_TAIL_R654_LABEL", tail.split(" ")[2], "R654:"),
    ("LOG_TAIL_DECLARED_IDLE", tail.split(" ", 3)[3][:16], "declared-idle（空轮判定·五静+探"),
    ("TS_ASCII", s2["ts"], "2026-09-29 04:59:33"),
    ("TASK_60_HEAD", s2["task"][:13], "declared-idle（"),
    ("TASK_60_LEN", len(s2["task"]), 60),
    ("FOCUS_R655", s2["focus"][:13], "R655: 空轮判定路径"),
    ("FOCUS_WINDOW_NOTE", ("并窗 2/6=R654-R659" in s2["focus"]), True),
    ("EXPORT_TS", e2["export_ts"], "2026-09-29T04:59:33+08:00"),
    ("RESULTS_HEAD_TICK", e2["results"][0][0], "654"),
    ("RESULTS_COUNT", len(e2["results"]), 19),
    ("OUTS_OS_HEAD", e2["outs"][0][-1][:13], "tick 654：R654"),
    ("LOG_TAIL_NEXT_ANCHOR", ("五查锚不变（orders O-1910/ledger 34/decisions 68）" in tail), True),
]
fails = 0
with io.open(os.path.join(ROOT, ".c3-tmp", "r654_verify2.txt"), "w", encoding="utf-8") as fh:
    fh.write("VERIFY_R654_ROUND2 (expectation strings corrected; data face from round 1)\n")
    for name, got, want in checks:
        ok = (got == want)
        if not ok:
            fails += 1
        fh.write(name + ": " + ("PASS" if ok else "FAIL") + " got=" + repr(got)[:90] + " want=" + repr(want)[:90] + "\n")
    fh.write("SUMMARY: " + ("15/15 ALL_PASS" if fails == 0 else str(fails) + " FAIL") + "\n")
print("VERIFY2 fails=" + str(fails))
