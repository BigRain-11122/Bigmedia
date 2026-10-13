# -*- coding: utf-8 -*-
"""R2187 close: workday waiting-state round + tech#149 enforcement-gap wiring.

Real work this round (not a pure declaration):
1. Finding: r2176_close.py -> r2185_close.py (10 consecutive rounds) hand-rolled
   the state.json accounting write (log.append + json.dump direct), bypassing
   the finalize_state born gate prescribed by tech#149 (R2136/R2137). The
   loop_health log-ts gate only rejects malformed prefixes, so well-formed
   hand-rolls pass silently - gate blind spot noted honestly.
2. Root cause: the task book close step wires only the export face (tech#148
   clause present since R2127) but not the state face - fresh fast-path
   sessions never re-read tech.md tail, so the prescription was unreachable.
3. Prescription (R2127 tech#148 same-shape precedent): tech#149 mandatory
   clause added to src/os/iteration_prompt.txt close step + tech#150 seed +
   THIS close routes its own accounting through finalize_state (reference
   path; the hand-rolled family is retired here).
"""
import io
import json
import sys
from datetime import datetime

REPO = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
sys.path.insert(0, REPO + r"\src\os")
from close_commit import finalize_state, run_close_commit

STATE = REPO + r"\src\os\state.json"
PROMPT = REPO + r"\src\os\iteration_prompt.txt"
TECH = REPO + r"\state\queue\tech.md"
LEDGER = REPO + r"\data\pipeline\fire-consume-ledger.jsonl"
CLOSE = REPO + r"\.c3-tmp\r2187_close.py"

# --- 0. anchor guard: last ledger line must be R2186 (concurrent-write law) ---
with io.open(STATE, "r", encoding="utf-8") as f:
    st = json.load(f)
if "R2186" not in st["log"][-1]:
    raise SystemExit("ANCHOR-GUARD-FAIL: last log line is not R2186: " + st["log"][-1][:80])
print("STEP anchor ok: last=R2186 tick=%d" % st["tick"])

# --- 1. surgical edit: task book close step gains the tech#149 state-face clause ---
ANCHOR = u"loop_health state-ts \u95e8\u6267\u6cd5\uff09"  # loop_health state-ts gate)
CLAUSE = (
    u"\u00b7**state \u5199\u5165\u9762\u5f3a\u5236\u5f8b\uff3btech#149\u00b72026-10-13 R2136\uff3d\uff1a"
    u"state \u6536\u8d26\u4e00\u5f8b\u8d70 `finalize_state` \u6b63\u8eab\uff08src/os/close_commit.py \u5185"
    u"\u00b7\u524d\u7f00\u6821\u9a8c+task 60 \u5b57\u4f8b+tick \u5b88\u536b\u5168\u5728\u5185\uff09"
    u"\u2014\u2014\u7981\u624b\u5199 `log.append`+`json.dump` \u76f4\u5199 state"
    u"\uff08\u826f\u6784\u624b\u5199\u96f6 FAIL \u68c0\u51fa=\u95f8\u76f2\u533a"
    u"\u00b7\u4efb\u52a1\u4e66\u9762\u8865\u5f8b=R2127 tech#148 \u540c\u578b\u5148\u4f8b\uff09**"
)
with io.open(PROMPT, "r", encoding="utf-8", newline="") as f:
    prompt_raw = f.read()
assert prompt_raw.count(ANCHOR) == 1, "anchor count != 1 in iteration_prompt.txt"
assert "finalize_state" not in prompt_raw, "tech#149 clause already present"
patched = prompt_raw.replace(ANCHOR, ANCHOR + CLAUSE, 1)
assert patched.count("finalize_state") == 1
with io.open(PROMPT, "w", encoding="utf-8", newline="") as f:
    f.write(patched)
print("STEP iteration_prompt.txt wired: tech#149 state-face clause (R2127 tech#148 precedent)")

# --- 2. tech.md seed #150 (this round's genuine audit finding) ---
item150 = (
    u"\n150. [R2187 \u6536\u8d26\u8f6e\u53d1\u73b0\u4f4d] **\u6536\u8d26\u6b65\u4efb\u52a1\u4e66\u9762\u7f3a tech#149 \u6b63\u8eab\u6307\u9488\uff08\u624b\u5199\u6536\u8d26\u65cf\u590d\u53d1\u6839\u56e0\u00b7\u95f8\u5347\u7ea7=\u4efb\u52a1\u4e66\u8865\u5f8b\u53e5\uff09**"
    u"\uff08\u7f3a\u53e3\u951a=R2187 \u5b9e\u8bfb\u76d8\u70b9\uff1ar2176_close.py\u2192r2185_close.py \u5341\u8f6e\u8fde\u7eed\u624b\u5199 d[\u300clog\u300d].append+json.dump \u76f4\u5199 state"
    u"\u2014\u2014tech#149\uff08R2136 \u5b9a\u8c2c\u00b7R2137 \u5b9e\u8bc1\u00b7\u300c\u58f0\u660e/\u7b49\u5f85\u6001\u8f6e\u6536\u8d26\u4e00\u5f8b\u8d70 finalize_state \u6b63\u8eab\u300d\uff09\u540e\u7167\u65e7\u590d\u53d1"
    u"\u00b7loop_health log-ts \u95f8\u53ea\u62d2\u574f\u524d\u7f00=\u826f\u6784\u624b\u5199\u96f6\u68c0\u51fa\u00b7\u95f8\u76f2\u533a\u5982\u5b9e\u6ce8"
    u"\uff08R2134/R2135 \u574f\u6863\u65cf\u540e\u7684\u826f\u6784\u65cf=\u540c\u6839\u7b2c\u4e8c\u5f62\u6001\uff09\uff1b"
    u"\u6839\u56e0=\u4efb\u52a1\u4e66\u6536\u8d26\u6b65\u53ea\u5f8b export \u9762\uff3btech#148 \u53e5\u5728\uff3d\u672a\u5f8b state \u9762"
    u"\u00b7\u65b0\u4f1a\u8bdd fast-path \u5224\u5b9a\u4e0d\u91cd\u8bfb tech \u5c3e=\u5904\u65b9\u7ed3\u6784\u6027\u4e0d\u53ef\u8fbe\uff09"
    u"\u2014\u2014\u5904\u65b9=\u2460\u4efb\u52a1\u4e66\u6536\u8d26\u6b65\u8865 tech#149 \u5f3a\u5236\u5f8b\u4e00\u53e5\uff08\u672c\u8f6e\u5df2\u6267\u884c\u00b7src/os/iteration_prompt.txt"
    u"\u00b7R2127 tech#148 \u540c\u578b\u5148\u4f8b\uff09\u2461\u672c\u8f6e\u6536\u8d26\u5373\u8d70 finalize_state \u793a\u8303\uff08\u624b\u5199\u65cf\u9000\u5f79\u627f\u7ee7\uff09"
    u"\u2014\u2014\u5224\u636e=\u540e\u7eed\u8f6e close \u811a\u672c grep `finalize_state` \u547d\u4e2d=\u95f8\u5728\u4f4d"
    u"\u00b7\u624b\u5199\u65cf\u518d\u590d\u53d1 \u22652 \u8f6e=\u5347\u88c1 lint \u9762\uff08close \u811a\u672c static check \u5019\u9009\uff09\u3002\n"
)
with io.open(TECH, "r", encoding="utf-8", newline="") as f:
    tech_raw = f.read()
assert "150." not in tech_raw.splitlines()[-1][:4], "tech tail already at 150"
prefix = "" if tech_raw.endswith("\n") else "\n"
with io.open(TECH, "a", encoding="utf-8", newline="") as f:
    f.write(prefix + item150)
print("STEP tech.md #150 appended (task-book wiring seed)")

# --- 3. this round's accounting through the born gate (finalize_state) ---
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
stamp = now[11:16]  # HH:MM real clock (R2135 date-slice bug family retired)
log_line = (
    u"2026-10-13 " + stamp + u" R2187: \u7b49\u5f85\u6001\u6536\u8f6e+\u672c\u8f6e\u5b9e\u4fee\u4e00\u4ef6=tech#149 \u6267\u6cd5\u7f3a\u53e3\u6536\u53e3"
    u"\uff08\u5de5\u4f5c\u65e5\u96f6\u6392\u5355\u7a97 08:00-23:59\u00b7O-20261012-1505 \u7eed\u6267\u00b7\u7b49\u5f85\u5bf9\u8c61\u540c\u4e0a\u8f6e\u4e0d\u91cd\u626b\uff09"
    u"\u2014\u2014\u2460\u4e94\u67e5\u5168\u9759=own orders \u951a O-20260908-1105 \u7ef4\u6301+origin_gap_check QUIET ahead0 behind0"
    u"+group_scan \u516d\u9762 fresh 19:52 \u5168\u9759\uff08DECISIONS truly_new=0 \u6c34\u4f4d 154+LEDGER @BigStream 5 \u884c\u503c\u5b88\u951a"
    u"+ORDERS rows=372 tail '10-13 18:5x'==stored \u96f6\u65b0\u884c+ORDERS-ORIGIN-DELTA delta=1=R2186 \u5df2\u6d88\u5316 row 373 \u6b8b\u5dee"
    u"\uff3bworktree FleetLink \u672a\u62c9\u5e73\u00b7tech#103 \u6c34\u4f4d\u4e0d bump \u7ef4\u6301\uff3d"
    u"+DIGEST-SUPPLY advisory 1 row-date 10-13 \u5df2\u88c1\u51b3\u9762\u7ef4\u6301\uff3bF-182 staged+\u591c\u7a97 DIGEST-v20\uff3d\uff09"
    u"+\u6811\u6001=MV-lane \u9884\u671f\u810f\u9762\uff08mv0001/mv001 \u4f1a\u8bdd\u4ef6+aihot watchdog \u81ea\u5199\u00b7R1745 \u96f6\u63a5\u89e6\u627f\u7ee7\uff09\u96f6\u9501\uff1b"
    u"\u2461\u4e09\u63a2\u9488\u5b9e\u8dd1=board 0 FAIL\uff085 \u9898 10 \u7a3f\u00b75 in production\uff09"
    u"/readiness 3 \u963b\u585e\u7686\u5916\u90e8 CEO \u9762\uff08\u8d26\u53f7\u6279\u6b21\u2460+M4 GATE 6/10+#17 needs-CEO\uff09"
    u"+1 \u53d1\u73b0 react-v16 unannot=F-183 \u591c\u7a97\u767b\u8bb0\u5373\u6e05\uff08R2118 \u88c1\u5b9a\u7ef4\u6301\uff09"
    u"/loop_health 3F+290W \u7686\u5728\u6848\u53f2\u5b9e\uff08\u4e09 outage \u7a97+drift 18\u226421 adjudicated\uff09\uff1b"
    u"\u2462fire_consume --ledger \u6b63\u8eab\u76f4\u53d1=no-fire rc1 reason=bm-a-workday-hours-zero-dispatch"
    u"\uff0819:53 \u6536\u636e\u00b7ledger \u884c\u968f\u672c commit \u5165\u8d26\uff09"
    u"\u2192F-180 SC-005-07+F-181 REACT-v15+F-182 DIGEST-v19+F-183 REACT-v16 \u56db\u4ef6 fire-ready carried"
    u"\u00b7\u771f\u7a97=10-14 \u591c\u7a97 00:00-08:00\uff08\u64a4 AIHOT pause \u65d7+worker-restart main#21+fire \u63a5\u529b+tech#126 \u6821\u51c6\u5192\u70df+DIGEST-v20\uff09\u6216 CEO \u4e0b\u73ed\u65d7\u518d\u843d\uff1b"
    u"\u2463\u672c\u8f6e\u5b9e\u4fee\u4ef6=tech#149 \u6267\u6cd5\u7f3a\u53e3\u6536\u53e3\uff1ar2176\u2192r2185 \u5341\u8f6e close \u811a\u672c\u624b\u5199 append+json.dump \u76f4\u5199 state \u590d\u53d1"
    u"\uff08log-ts \u95f8\u53ea\u62d2\u574f\u524d\u7f00=\u826f\u6784\u624b\u5199\u96f6\u68c0\u51fa\u00b7\u95f8\u76f2\u533a\u5982\u5b9e\u6ce8\uff09"
    u"\u00b7\u6839\u56e0=\u4efb\u52a1\u4e66\u6536\u8d26\u6b65\u53ea\u5f8b export \u9762\uff3btech#148 \u53e5\u5728\uff3d\u672a\u5f8b state \u9762=\u65b0\u4f1a\u8bdd fast-path \u5904\u65b9\u4e0d\u53ef\u8fbe"
    u"\u2014\u2014\u5904\u65b9=\u4efb\u52a1\u4e66\u6536\u8d26\u6b65\u8865 tech#149 \u5f3a\u5236\u5f8b\u4e00\u53e5\uff08src/os/iteration_prompt.txt\u00b7R2127 tech#148 \u540c\u578b\u5148\u4f8b\uff09"
    u"+tech#150 \u79cd\u5b50\u5165\u961f\uff08\u5224\u636e=\u540e\u7eed\u8f6e close \u811a\u672c grep finalize_state \u547d\u4e2d\uff09"
    u"+\u672c\u8f6e\u6536\u8d26\u5373\u8d70 finalize_state \u6b63\u8eab\u793a\u8303\uff08\u624b\u5199\u65cf\u9000\u5f79\u627f\u7ee7\uff09\uff1b"
    u"\u2464\u4f8b\u884c\u4ef6=export=skip <24h\uff08export_ts 12:44:35 ~7h\u00b7\u5b9e\u51b5\u96f6\u53d8\u5316\u00b7tech#148 \u5f8b\u4e0b skip=\u96f6\u5199\u5165\u5b89\u5168\u6001\uff09"
    u"\u00b7HQ-FEEDBACK \u4e0d\u5199\uff08\u96f6\u96c6\u56e2\u5c42\u65b0 open \u95ee\u9898\uff09\u00b7T1 \u50ac\u529e\u65e0\u8d85\u7ebf\u9879\uff08\u8d26\u53f7\u7269\u7406\u4ef6=\u5448\u73b0\u72b6\u884c\u4e0d\u50ac\u529e\uff09"
    u"\u00b7tokens:local=0\uff08\u63a2\u9488/\u76f4\u8bfb=\u6863\u6848\u8bfb\u5199\u96f6\u672c\u5730\u6a21\u578b\u8c03\u7528\u00b7P-54\u2465 \u8ba1\u91cf\u5f8b\uff09"
    u"\u00b7\u961f\u5217\u76d8\u70b9=queue_status fresh 19:53 \u5b9e\u8bfb\u96f6\u6f02\u79fb\uff08backlog claimable 8 \u5168 lane/gated\uff3bhead #110 Toonflow=\u591c\u7a97\u88c5\u673a\u4f4d\uff3d"
    u"+main claimable 2 \u7686 MV \u96f6\u63a5\u89e6\u67e5\u770b\u4f4d+tech claimable 1 gated\uff3b#126 \u591c\u7a97\u6821\u51c6\u00b710-14 08:00 \u6743\u5a01\u7a97\u951a\uff3d+explore 0\uff09"
    u"\u00b7\u4e09\u961f\u8865\u8d27=tech#150 \u5b9e\u79cd\u5b50\u843d\u4f4d"
    u"\u2014\u2014\u4e0b\u8f6e=\u7b49\u5f85\u6001\u7eed\uff08\u7b49\u5f85\u5bf9\u8c61\u540c\u4e0a\u4e0d\u91cd\u626b\uff09"
    u"\u00b710-14 \u591c\u7a97 00:00 \u5f00\u7a97\u5373\u8f6c\u6536\u53e3\u4e09\u8fde\uff08\u64a4\u65d7+main#21+fire \u63a5\u529b+tech#126+DIGEST-v20\uff09"
)
summary = finalize_state(log_line=log_line, ts=now)
print("STATE-FINALIZED tick=%s ts=%s" % (summary["tick"], summary["ts"]))

msg = (
    "R2187: workday waiting-state close + tech#149 enforcement-gap wiring: r2176-r2185 close "
    "scripts hand-rolled the state write (10-round recurrence past the tech#149 prescription; "
    "log-ts gate blind to well-formed hand-rolls); root cause = task book close step wires the "
    "export face (tech#148) but not the state face; fix = tech#149 mandatory clause added to "
    "iteration_prompt.txt (R2127 tech#148 precedent) + tech#150 seed + this close routes "
    "accounting via finalize_state reference path; five checks quiet, F-180~183 fire-ready "
    "carried, next window 10-14 00:00 night relay [via bm-a]"
)
rc, lines = run_close_commit(
    files=[STATE, PROMPT, TECH, LEDGER, CLOSE],
    message=msg,
)
for l in lines:
    print(l)
print("R2187 close done rc=%d" % rc)
