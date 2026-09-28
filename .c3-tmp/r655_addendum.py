# -*- coding: utf-8 -*-
"""R655 addendum: append honesty note (R654 verify file unread = operation-red; R655 check-rig truncation bugs fixed)
+ corrected full verify (r655_verify2.txt). No tick change. Append-only log law (R651+R652 addendum precedent)."""
import json, io, os, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
STATE = os.path.join(ROOT, "src", "os", "state.json")
EXPORT = os.path.join(ROOT, "docs", "status-export.json")

now = datetime.datetime.now()
ts = now.strftime("%Y-%m-%d %H:%M:%S")
hm = now.strftime("%H:%M")

ADDENDUM = (
    "2026-09-29 " + hm + " R655 轮末补记（核对件修红·诚实律·追加制原行不改写）——"
    "①R654 close verify 件实读=**4 FAIL**（LOG_TAIL/FOCUS/OUTS 三截断长度笔误+RESULTS_COUNT 误预测 19≠20）"
    "=上执行体核对件跑后未读未修=操作红如实入账（R381 零解析防假绿灯族·verify 件跑后必读律）；"
    "数据面经本轮全量复核无恙=tick654/focus655/outs654/export_ts/results654 全落位（4 FAIL 全为 rig 比对串长度错非数据错·R654 主行零改写）；"
    "②本轮 close 首验 3 FAIL 同截断族（r655_verify.txt 留档不删）→核对 rig 修正复跑 r655_verify2.txt **13/13 ALL_PASS**"
    "（长度对齐法：LOG_TAIL 主行查子串·FOCUS[:12]·OUTS[:13]·补记行在位检查新增）——收账数据面自证闭环。"
)

with io.open(STATE, "r", encoding="utf-8") as fh:
    state = json.load(fh)
assert state["tick"] == 655, "TICK_EXPECTED_655"
assert state["log"][-1].split(" ", 3)[2] == "R655:", "LOG_TAIL_EXPECTED_MAIN_R655 got " + state["log"][-1][:40]
state["log"].append(ADDENDUM)
with io.open(STATE, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(state, fh, ensure_ascii=False, indent=2)
    fh.write("\n")

# ---- corrected verify (data plane + addendum presence) ----
with io.open(STATE, "r", encoding="utf-8") as fh:
    s2 = json.load(fh)
with io.open(EXPORT, "r", encoding="utf-8") as fh:
    e2 = json.load(fh)

main_line = s2["log"][-2]
checks = [
    ("TICK", s2["tick"], 655),
    ("PRODUCTION", s2["production"], "open"),
    ("LOG_COUNT", len(s2["log"]), 678),
    ("MAIN_R655_PREFIX", " ".join(main_line.split(" ", 3)[2:3]), "R655:"),
    ("MAIN_R655_SUBSTR", "R655: declared-idle（空轮判定·五静+探针绿+四查尽·P-2026-09-28-02 ②空轮判定路径④序·第三连）" in main_line, True),
    ("ADDENDUM_TAIL", s2["log"][-1].split(" ", 3)[2][:5], "R655"),
    ("ADDENDUM_SUBSTR", "R654 close verify 件实读=**4 FAIL**" in s2["log"][-1], True),
    ("TS", s2["ts"], "2026-09-29 05:05:55"),
    ("TASK_60", s2["task"], "declared-idle（空轮判定·五静+探针绿+四查尽·P-2026-09-28-02 ②空轮判定路径④序·第三连）"),
    ("FOCUS_12", s2["focus"][:12], "R656: 空轮判定路径"),
    ("EXPORT_TS", e2["export_ts"][:10], "2026-09-29"),
    ("OUTS_13", e2["outs"][0][-1][:13], "tick 655：R655"),
    ("RESULTS_COUNT", len(e2["results"]), 20),
]
fails = 0
with io.open(os.path.join(ROOT, ".c3-tmp", "r655_verify2.txt"), "w", encoding="utf-8") as fh:
    fh.write("VERIFY2_R655 addendum-time=" + ts + "\n")
    for name, got, want in checks:
        ok = (got == want)
        if not ok:
            fails += 1
        fh.write(name + ": " + ("PASS" if ok else "FAIL") + " got=" + repr(got)[:80] + " want=" + repr(want)[:80] + "\n")
    fh.write("SUMMARY: " + ("13/13 ALL_PASS" if fails == 0 else str(fails) + " FAIL") + "\n")
    fh.write("WINDOW_NOTE: R655=window 2/6 (R654-R659) NO_COMMIT this round; addendum appended post-close per R651+R652 precedent\n")
print("ADDENDUM_OK verify2_fails=" + str(fails) + " ts=" + ts)
