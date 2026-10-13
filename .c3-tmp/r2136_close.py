# -*- coding: utf-8 -*-
"""R2136 close: workday waiting-state round + R2135 log-notch repair + tech#149.

Real work this round (not a pure declaration round):
1. Repair the R2135 malformed log prefix "2026-10-13 2026-x R2135:" ->
   "2026-10-13 09:5x R2135:" (ts field 09:54:05 is authoritative; R2134
   fixup precedent b301e1f6). Byte-level single-replace, no re-serialize.
2. Verify inside this close: loop_health log-ts FAIL must clear (4F -> 3F
   historical-only) BEFORE the accounting line is written.
3. tech#149 seed appended to state/queue/tech.md: declaration-round close
   scripts hand-rolled the state write (json.dump direct) bypassing the
   finalize_state born gate; R2135 root cause = stamp = now[:5]+"x" sliced
   the DATE segment (produced "2026-x"); R2134 wrong notch = same family.
   Prescription: declaration/waiting rounds route log accounting through
   finalize_state. Detection gate (loop_health log-ts) live-fire validated:
   the bad entry was caught within one round.
4. THIS close routes its own accounting through finalize_state (born-gate
   reference path; the hand-rolled append pattern is retired here).
"""
import io
import subprocess
import sys
from datetime import datetime

REPO = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
sys.path.insert(0, REPO + r"\src\os")
from close_commit import finalize_state, run_close_commit

STATE = REPO + r"\src\os\state.json"
TECH = REPO + r"\state\queue\tech.md"
LEDGER = REPO + r"\data\pipeline\fire-consume-ledger.jsonl"

# --- 1. byte-level repair of the R2135 malformed notch (fail-fast) ---
BAD = "2026-10-13 2026-x R2135:".encode("utf-8")
GOOD = "2026-10-13 09:5x R2135:".encode("utf-8")
with open(STATE, "rb") as f:
    raw = f.read()
n = raw.count(BAD)
assert n == 1, "expected exactly 1 malformed notch, found %d" % n
with open(STATE, "wb") as f:
    f.write(raw.replace(BAD, GOOD))
print("STEP repaired R2135 notch: 2026-x -> 09:5x (ts field 09:54:05 authoritative)")

# --- 2. in-close verification: loop_health log-ts must be cleared ---
proc = subprocess.run([sys.executable, REPO + r"\src\os\loop_health.py", "--loop"],
                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
lh = proc.stdout.decode("utf-8", "replace")
assert "lacks leading timestamp" not in lh, "log-ts FAIL still present after repair"
assert "loop health: FAIL (3 fail" in lh, "unexpected fail count after repair:\n" + lh[-600:]
print("STEP loop_health post-repair verified: 4F -> 3F, log-ts cleared")

# --- 3. tech.md seed #149 (this round's genuine audit discovery) ---
item149 = (
    "\n149. [R2136 \u6536\u8d26\u8f6e\u53d1\u73b0\u4f4d] **\u58f0\u660e\u8f6e\u6536\u8d26\u811a\u672c\u624b\u5199 state \u5199\u5165\u7ed5\u8fc7 finalize_state born gate\uff08log \u524d\u7f00\u574f\u6863\u590d\u53d1\u65cf\uff09**\uff1a"
    "\u7f3a\u53e3\u951a=R2135 \u574f\u6863\u5b9e\u5f55\uff08log \u524d\u7f00\u300c2026-10-13 2026-x\u300d\u00b7loop_health log-ts FAIL 1 \u8f6e\u5b9e\u5f39\u68c0\u51fa"
    "\u00b7\u6839\u56e0=r2135_close.py \u7684 stamp=now[:5]+\u300cx\u300d \u5207\u65e5\u671f\u6bb5\u800c\u975e\u65f6\u95f4\u6bb5\u2014\u2014\u6ce8\u91ca\u81ea\u8bc1\u300c09:5x\u300d\u610f\u56fe\u4e0e\u4ea7\u51fa\u7269\u80cc\u79bb\uff09"
    "+R2134 \u9519\u6863\u540c\u65cf\uff0809:5x vs ts 09:47:08\u00b7fixup b301e1f6\uff09\u2014\u2014\u4e24\u8f6e\u7686\u624b\u5199 d[\u300clog\u300d].append+json.dump \u76f4\u5199 state\u3001"
    "\u7ed5\u8fc7 tech#76 \u5355\u5199\u8005\u6b63\u8eab\uff08derive_task \u672c\u53ef\u5728 born \u62d2\u6389\u574f\u524d\u7f00\uff09\u2014\u2014\u4e0e tech#148\uff08export \u9762\u540c\u75c5\uff1aclose \u811a\u672c\u624b\u5199\u5df2\u6709 canonical writer "
    "\u7684\u5199\u5165\u9762\uff09\u4e3a\u540c\u4e00\u75c5\u6839\u65cf\u3002\u5904\u65b9=**\u58f0\u660e/\u7b49\u5f85\u6001\u8f6e\u6536\u8d26\u4e00\u5f8b\u8d70 finalize_state \u6b63\u8eab**\uff08\u524d\u7f00\u6821\u9a8c+task 60 \u5b57\u5f8b+tick \u5b88\u536b\u5168\u5728\u5185"
    "\u00b7\u624b\u5199 append \u5236\u5c31\u6b64\u9000\u5f79\u00b7R2136 \u6536\u8d26\u5373\u53c2\u8003\u5b9e\u73b0\uff09\u3002\u68c0\u6d4b\u95f8=loop_health log-ts \u5df2\u5b9e\u5f39\u9a8c\u8bc1\uff081 \u8f6e\u68c0\u51fa\u7a97\uff09\u2014\u2014\u95f8\u5728\u4f4d\u00b7\u672c\u6761=\u590d\u53d1\u65cf\u5904\u65b9\u951a+born-gate \u6b63\u8eab\u8def\u7ebf\u6267\u6cd5\u793a\u8303\u3002\n"
)
with io.open(TECH, "r", encoding="utf-8", newline="") as f:
    tech_raw = f.read()
prefix = "" if tech_raw.endswith("\n") else "\n"
with io.open(TECH, "a", encoding="utf-8", newline="") as f:
    f.write(prefix + item149)
print("STEP tech.md #149 appended (declaration-round finalize_state prescription)")

# --- 4. this round's accounting through the born gate (finalize_state) ---
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
stamp = now[11:15] + "x"  # HH:Mx fuzzy from real clock (R2135 now[:5] date-slice bug retired)
log_line = (
    "2026-10-13 " + stamp + " R2136: \u7b49\u5f85\u6001\u6536\u8f6e\uff08\u5de5\u4f5c\u65e5\u96f6\u6392\u5355\u7a97 08:00-23:59\u00b7O-20261012-1505 \u7eed\u6267\u00b7\u7b49\u5f85\u5bf9\u8c61\u540c\u4e0a\u8f6e\u4e0d\u91cd\u626b\uff09"
    "+\u672c\u8f6e\u5b9e\u4fee\u4e00\u4ef6=R2135 log \u574f\u6863\u4fee\u590d\uff1a\u524d\u7f00\u300c2026-10-13 2026-x\u300d\u2192\u300c2026-10-13 09:5x\u300d"
    "\uff08ts \u5b57\u6bb5 09:54:05 \u6743\u5a01\u00b7R2134 fixup b301e1f6 \u540c\u6b3e\u5148\u4f8b\u00b7loop_health \u65b0 FAIL log-ts 4F \u7684\u5904\u7f6e\uff09"
    "\u00b7\u673a\u5185\u9a8c\u95f8\u5b9e\u6d4b 4F\u21923F log-ts \u6e05\u96f6\u3002\u6839\u56e0\u4e0e\u79cd\u5b50=tech#149 \u843d\u4f4d\uff1ar2135_close.py \u7684 stamp=now[:5]+x \u5207\u65e5\u671f\u6bb5\u4ea7\u51fa 2026-x"
    "\uff08\u6ce8\u91ca\u81ea\u8bc1\u300c09:5x\u300d\u610f\u56fe\uff09+\u58f0\u660e\u8f6e\u6536\u8d26\u811a\u672c\u624b\u5199 d[log].append+json.dump \u76f4\u5199 state \u7ed5\u8fc7 tech#76 finalize_state born gate"
    "\uff08derive_task \u672c\u53ef born \u62d2\uff09\u2014\u2014R2134 \u9519\u6863 09:5x vs 09:4x \u540c\u65cf\u590d\u53d1\u3001\u4e0e tech#148\uff08export \u9762\u540c\u75c5\u6839\uff09\u540c\u6e90\uff1b"
    "\u5904\u65b9=\u58f0\u660e/\u7b49\u5f85\u6001\u8f6e\u6536\u8d26\u4e00\u5f8b\u8d70 finalize_state \u6b63\u8eab\uff08\u672c\u8f6e\u6536\u8d26\u5373\u793a\u8303\u00b7\u68c0\u6d4b\u95f8 loop_health log-ts 1 \u8f6e\u5b9e\u5f39\u68c0\u51fa\u5df2\u9a8c\u8bc1\uff09\u3002"
    "\u4e94\u67e5\u5168\u9759=own orders \u951a O-20261008-1105 \u7ef4\u6301+origin_gap QUIET ahead0 behind0"
    "+group_scan \u516d\u9762 fresh 10:03 \u5168\u9759\uff08decisions truly_new=0 \u6c34\u4f4d 154+ledger @BigStream \u951a\u5e73\u7a33"
    "+orders rows 341 tail '10-13 04:3x'==stored+origin-delta 0+DIGEST-SUPPLY advisory 1 row-date age0d \u5df2\u88c1\u51b3\u9762"
    "\uff3bF-182 staged+main#28 gated \u8986\u76d6\uff3d\uff09+\u6811=MV-lane \u9884\u671f\u810f\u9762\u96f6\u63a5\u89e6+\u65e0 index.lock\u3002"
    "\u63a2\u9488\u5e26\u5185=board 0 FAIL\uff085 \u9898 10 \u7a3f\u00b75 in production\uff09/readiness 3 \u963b\u585e\u7686\u5916\u90e8 CEO \u9762\uff08\u8d26\u53f7\u6279\u6b21\u2460+M4 GATE 6/10+#17 needs-CEO\uff09"
    "+1 \u53d1\u73b0 react-v16 unannot=F-183 \u6392\u961f\u767b\u8bb0\u4f4d/loop_health 3F+286W \u7686\u5728\u6848\u53f2\u5b9e\uff08\u4e09 outage \u7a97+drift 18\u226421 adjudicated\uff09\u3002"
    "\u961f\u5217\u96f6\u6f02\u79fb=queue_status \u590d\u8bfb\uff08backlog claimable 8 \u5168\u4ed6\u7a97 lane/gated\uff3b#111 MV \u96f6\u63a5\u89e6/#112 tech#92 \u7a97/#110 Toonflow \u591c\u7a97\u4f4d/"
    "#70 \u226410-15/#59/#63/#67 fire \u7a97/#31 render \u7a97/#15 \u9648\u6848\uff3d\u00b7main claimable 2 \u7686\u5e95\u4f4d\u8f6e\u5224\uff3b#7 krea2 \u67e5\u770b\u4f4d+#27b A/B GPU \u72ec\u5360\u7a97\uff3d"
    "\u00b7tech claimable 1 gated\uff3b#126 \u591c\u7a97\u6821\u51c6=10-14 08:00 \u6743\u5a01\u7a97\u951a\uff3d\u00b7explore 0\uff09\u3002"
    "fire_consume no-fire rc1 reason=bm-a-workday-hours-zero-dispatch \u56de\u6267\u5165\u8d26\u00b7"
    "F-180 SC-005-07+F-181 REACT-v15+F-182 DIGEST-v19+F-183 REACT-v16 \u56db\u4ef6 fire-ready carried"
    "\u00b7\u771f\u7a97=10-14 \u591c\u7a97 00:00-08:00\uff08\u64a4 AIHOT pause \u65d7+worker-restart main#21+F-180~183 fire \u63a5\u529b+tech#126 \u6821\u51c6\u5192\u70df\uff09\u6216 CEO \u4e0b\u73ed\u65d7\u518d\u843d\u3002"
    "export=skip <24h\uff08R2128 08:40 canonical writer \u5237\u65b0\u00b7\u5b9e\u51b5\u96f6\u53d8\u5316\u00b7tech#148 \u5f3a\u5236\u5f8b\u4e0b skip=\u96f6\u5199\u5165\u5b89\u5168\u6001\uff09\u3002"
    "\u4e09\u961f\u8865\u8d27=tech#149 \u5b9e\u53d1\u73b0\u79cd\u5b50\u843d\u4f4d\uff08\u672c\u8f6e\u4fee\u590d\u4ef6+\u590d\u53d1\u65cf\u5904\u65b9\u951a\uff09\u3002"
    "\u4e34\u65f6\u4ef6\u6e05\u7406\u94a9=\u672c\u8f6e\u96f6\u843d\u76d8\u4e2d\u95f4\u4ef6\uff08\u8bfb\u6570\u4f1a\u8bdd\u5185\u76f4\u8bfb\uff09\u00b7close \u811a\u672c\u7167 tech#81 \u81ea\u542b\u5f8b\u5165\u8d26\u3002"
    "HQ-FEEDBACK \u4e0d\u5199\uff08\u96f6\u96c6\u56e2\u5c42\u65b0 open \u95ee\u9898\uff09\u00b7T1 \u50ac\u529e\u65e0\u8d85\u7ebf\u9879\uff08\u8d26\u53f7\u7269\u7406\u4ef6=\u5448\u73b0\u72b6\u884c\u4e0d\u50ac\u529e\uff09\u00b7tokens:local=0\u3002"
)
summary = finalize_state(log_line=log_line, ts=now)
print("STATE-FINALIZED tick=%s ts=%s" % (summary["tick"], summary["ts"]))

msg = (
    "R2136: workday waiting-state close + R2135 log-notch repair (2026-x -> 09:5x per ts "
    "field, R2134 fixup precedent, loop_health 4F->3F verified in-close) + tech#149 seed: "
    "declaration-round close scripts hand-rolled state write bypassing finalize_state born "
    "gate (root cause now[:5] date-segment slice; R2134/R2135 same family as tech#148 "
    "export-face sibling); prescription = route log accounting via finalize_state, this "
    "close is the reference path; log-ts detection gate live-fire 1-round catch validated "
    "[via bm-a]"
)
rc, lines = run_close_commit(
    files=[STATE, TECH, LEDGER,
           REPO + r"\.c3-tmp\r2136_close.py"],
    message=msg,
)
for l in lines:
    print(l)
print("R2136 close done rc=%d" % rc)
