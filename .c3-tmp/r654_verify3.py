# -*- coding: utf-8 -*-
"""R654 verify round 3: startswith semantics (root fix for prefix-check char-count trap).
R618 law note: prefix checks must use startswith, never sliced equality."""
import json, io, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
with io.open(os.path.join(ROOT, "src", "os", "state.json"), "r", encoding="utf-8") as fh:
    s2 = json.load(fh)
with io.open(os.path.join(ROOT, "docs", "status-export.json"), "r", encoding="utf-8") as fh:
    e2 = json.load(fh)

tail = s2["log"][-1]
checks = [
    ("TICK", s2["tick"] == 654),
    ("PRODUCTION", s2["production"] == "open"),
    ("LOG_COUNT", len(s2["log"]) == 676),
    ("LOG_TAIL_R654_LABEL", tail.split(" ")[2] == "R654:"),
    ("LOG_TAIL_DECLARED_IDLE", tail.split(" ", 3)[3].startswith("declared-idle（空轮判定·五静+探针绿+四查尽")),
    ("TS_ASCII", s2["ts"] == "2026-09-29 04:59:33"),
    ("TASK_60_HEAD", s2["task"].startswith("declared-idle（")),
    ("TASK_60_LEN", len(s2["task"]) == 60),
    ("FOCUS_R655", s2["focus"].startswith("R655: 空轮判定路径开轮")),
    ("FOCUS_WINDOW_NOTE", "并窗 2/6=R654-R659" in s2["focus"]),
    ("EXPORT_TS", e2["export_ts"] == "2026-09-29T04:59:33+08:00"),
    ("RESULTS_HEAD_TICK", e2["results"][0][0] == "654"),
    ("RESULTS_TEXT_HEAD", e2["results"][0][1].startswith("declared-idle（空轮判定·五静+探针绿+四查尽")),
    ("RESULTS_COUNT", len(e2["results"]) == 19),
    ("OUTS_OS_HEAD", e2["outs"][0][-1].startswith("tick 654：R654")),
    ("LOG_TAIL_NEXT_ANCHOR", "五查锚不变（orders O-1910/ledger 34/decisions 68）" in tail),
]
fails = sum(0 if ok else 1 for _, ok in checks)
with io.open(os.path.join(ROOT, ".c3-tmp", "r654_verify3.txt"), "w", encoding="utf-8") as fh:
    fh.write("VERIFY_R654_ROUND3 startswith-semantics (check-gen root fix; data face rounds 1-2 consistent)\n")
    for name, ok in checks:
        fh.write(name + ": " + ("PASS" if ok else "FAIL") + "\n")
    fh.write("SUMMARY: " + ("16/16 ALL_PASS" if fails == 0 else str(fails) + " FAIL") + "\n")
print("VERIFY3 fails=" + str(fails))
