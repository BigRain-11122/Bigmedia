# -*- coding: utf-8 -*-
"""R2137 close: workday waiting-state round via finalize_state born-gate path.

This round consumes tech#149 (its own prescription anchor): the close routes
the accounting log through finalize_state (2nd live-fire confirmation of the
born-gate path; R2136 was the reference implementation). The hand-rolled
d[log].append + json.dump state write stays retired.

tech#149 done mark: deliverables all in place -
  a) prescription anchor (the queue entry itself)
  b) detection gate live-fire (loop_health log-ts caught R2135 bad notch
     within 1 round)
  c) R2136 reference close (born-gate path)
  d) R2137 this close = second confirmation, same path, zero hand-rolled
     state writes.
"""
import io
import sys
from datetime import datetime

REPO = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
sys.path.insert(0, REPO + r"\src\os")
from close_commit import finalize_state, run_close_commit

STATE = REPO + r"\src\os\state.json"
TECH = REPO + r"\state\queue\tech.md"
LEDGER = REPO + r"\data\pipeline\fire-consume-ledger.jsonl"

# --- 1. tech#149 done mark (byte-level single-replace, fail-fast) ---
DONE_TAG = "149. [done 2026-10-13 R2137] [R2136".encode("utf-8")
ORIG = "149. [R2136".encode("utf-8")
APPEND = (
    "\u2014\u2014\u5df2\u4ea4\u4ed8\uff1a\u5904\u65b9\u951a+\u68c0\u6d4b\u95f8\u5b9e\u5f39\uff08loop_health log-ts 1 \u8f6e\u68c0\u51fa R2135 \u574f\u6863\uff09"
    "+R2136 \u53c2\u8003\u5b9e\u73b0\uff08born-gate \u6b63\u8eab\u6536\u8d26\uff09+R2137 \u4e8c\u6b21\u5b9e\u5f39\u786e\u8ba4"
    "\uff08\u672c\u8f6e\u6536\u8d26\u540c\u8d70 finalize_state\u00b7log \u524d\u7f00/task 60 \u5b57\u5f8b/tick \u5b88\u536b\u5168\u8fc7"
    "\u00b7\u624b\u5199 append \u5236\u9000\u5f79\u9762\u7ef4\u6301\uff09\u2014\u2014\u95ed\u9879\u3002\n"
).encode("utf-8")
with open(TECH, "rb") as f:
    tech_raw = f.read()
n = tech_raw.count(ORIG)
assert n == 1, "expected exactly 1 tech#149 head, found %d" % n
assert b"[done 2026-10-13 R2137]" not in tech_raw, "tech#149 already marked done"
tech_new = tech_raw.replace(ORIG, DONE_TAG, 1)
# append delivery note at end of the #149 line (line ends with \n)
marker = "born-gate \u6b63\u8eab\u8def\u7ebf\u6267\u6cd5\u793a\u8303\u3002".encode("utf-8")
m = tech_new.count(marker)
assert m == 1, "expected exactly 1 tech#149 tail marker, found %d" % m
tech_new = tech_new.replace(marker, marker.rstrip("\u3002".encode("utf-8")) + APPEND, 1)
with open(TECH, "wb") as f:
    f.write(tech_new)
print("STEP tech#149 marked done (R2136 reference + R2137 confirmation)")

# --- 2. this round's accounting through the born gate (finalize_state) ---
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
stamp = now[11:15] + "x"  # HH:Mx fuzzy from real clock (tech#149 prescription)
log_line = (
    "2026-10-13 " + stamp + " R2137: \u7b49\u5f85\u6001\u6536\u8f6e\uff08\u5de5\u4f5c\u65e5\u96f6\u6392\u5355\u7a97 08:00-23:59\u00b7O-20261012-1505 \u7eed\u6267"
    "\u00b7\u7b49\u5f85\u5bf9\u8c61\u540c\u4e0a\u8f6e\u4e0d\u91cd\u626b\uff09+\u672c\u8f6e\u6d88\u8d39\u4ef6=tech#149 done \u6807\uff08\u5904\u65b9\u951a+log-ts \u68c0\u6d4b\u95f8 1 \u8f6e\u5b9e\u5f39"
    "+R2136 \u53c2\u8003\u5b9e\u73b0+\u672c\u8f6e\u6536\u8d26\u4e8c\u6b21\u5b9e\u5f39\u786e\u8ba4 finalize_state \u6b63\u8eab\u8def\u7ebf\u00b7\u624b\u5199 append \u5236\u9000\u5f79\u9762\u7ef4\u6301\uff09\u3002"
    "\u4e94\u67e5\u5168\u9759=own orders \u951a O-20261008-1105 \u7ef4\u6301+origin_gap QUIET ahead0 behind0"
    "+group_scan \u516d\u9762 fresh 10:13 \u5168\u9759\uff08decisions truly_new=0 \u6c34\u4f4d 154+ledger @BigStream \u951a\u5e73\u7a33\uff08\u503c\u5b88 retention \u884c=\u5df2\u951a\u975e\u65b0\u8f6c\u529e\uff09"
    "+orders rows 341 tail '10-13 04:3x'==stored+origin-delta 0+DIGEST-SUPPLY advisory 1 row-date age0d \u5df2\u88c1\u51b3\u9762"
    "\uff3bF-182 staged+main#28 gated \u8986\u76d6\uff3d\uff09+\u6811=MV-lane \u9884\u671f\u810f\u9762\u96f6\u63a5\u89e6+\u65e0 index.lock\u3002"
    "\u63a2\u9488\u5e26\u5185=board 0 FAIL\uff085 \u9898 10 \u7a3f\u00b75 in production\uff09/readiness 3 \u963b\u585e\u7686\u5916\u90e8 CEO \u9762\uff08\u8d26\u53f7\u6279\u6b21\u2460+M4 GATE 6/10+#17 needs-CEO\uff09"
    "+1 \u53d1\u73b0 react-v16 unannot=F-183 \u6392\u961f\u767b\u8bb0\u4f4d/loop_health 3F+286W \u7686\u5728\u6848\u53f2\u5b9e\uff08\u4e09 outage \u7a97+drift 18\u226421 adjudicated\uff09\u3002"
    "\u961f\u5217\u96f6\u6f02\u79fb=queue_status \u590d\u8bfb\uff08backlog claimable 8 \u5168\u4ed6\u7a97 lane/gated\u00b7main claimable 2 \u7686\u5e95\u4f4d\u8f6e\u5224"
    "\uff3b#7 krea2 \u67e5\u770b\u4f4d+\u672c\u8f6e\u96f6\u65b0\u589e\u53ef\u9a8c/#27b A/B GPU \u72ec\u5360\u7a97\uff3d\u00b7tech \u6d88\u8d39 #149 done \u540e\u4f59 #126 gated \u591c\u7a97\u00b7explore 0\uff09\u3002"
    "fire_consume no-fire rc1 reason=bm-a-workday-hours-zero-dispatch \u56de\u6267\u5165\u8d26\uff0810:2x\uff09\u00b7"
    "F-180 SC-005-07+F-181 REACT-v15+F-182 DIGEST-v19+F-183 REACT-v16 \u56db\u4ef6 fire-ready carried"
    "\u00b7\u771f\u7a97=10-14 \u591c\u7a97 00:00-08:00\uff08\u64a4 AIHOT pause \u65d7+worker-restart main#21+F-180~183 fire \u63a5\u529b+tech#126 \u6821\u51c6\u5192\u70df\uff09\u6216 CEO \u4e0b\u73ed\u65d7\u518d\u843d\u3002"
    "export=skip <24h\uff08R2128 08:40 canonical writer \u5237\u65b0\u00b7\u5b9e\u51b5\u96f6\u53d8\u5316\u00b7tech#148 \u5f3a\u5236\u5f8b\u4e0b skip=\u96f6\u5199\u5165\u5b89\u5168\u6001\uff09\u3002"
    "\u4e09\u961f\u8865\u8d27=\u771f\u65e0\u65b0\u79cd\u5b50\u5982\u5b9e\u6ce8\u8bb0\u96f6\u81a8\u80c0\uff08group \u516d\u9762\u9759+\u63a2\u9488\u7a33+\u672c\u8f6e\u96f6\u65b0\u53d1\u73b0\u00b7\u672c\u8f6e\u6d88\u8d39\u4ef6\u5df2\u7531 tech#149 done \u6807\u627f\u8f7d\uff09\u3002"
    "\u4e34\u65f6\u4ef6\u6e05\u7406\u94a9=\u672c\u8f6e\u8bfb\u6570\u4f1a\u8bdd\u5185\u76f4\u8bfb\u96f6\u843d\u76d8\uff08r2137_tech_head.txt \u5199\u5165\u5c1d\u8bd5\u6b7b\u4e8e SyntaxError \u96f6\u843d\u76d8\u6838\u5b9e\uff09"
    "\u00b7close \u811a\u672c\u7167 tech#81 \u81ea\u542b\u5f8b\u5165\u8d26\u3002HQ-FEEDBACK \u4e0d\u5199\uff08\u96f6\u96c6\u56e2\u5c42\u65b0 open \u95ee\u9898\uff09"
    "\u00b7T1 \u50ac\u529e\u65e0\u8d85\u7ebf\u9879\uff08\u8d26\u53f7\u7269\u7406\u4ef6=\u5448\u73b0\u72b6\u884c\u4e0d\u50ac\u529e\uff09\u00b7tokens:local=0\u3002"
)
summary = finalize_state(log_line=log_line, ts=now)
print("STATE-FINALIZED tick=%s ts=%s" % (summary["tick"], summary["ts"]))

msg = (
    "R2137: workday waiting-state close via finalize_state born-gate path "
    "(2nd live-fire of tech#149 prescription, R2136 was reference) + tech#149 "
    "done mark: prescription anchor + log-ts detection gate 1-round catch + "
    "reference close + this round confirmation; hand-rolled state append "
    "stays retired [via bm-a]"
)
rc, lines = run_close_commit(
    files=[STATE, TECH, LEDGER,
           REPO + r"\.c3-tmp\r2137_close.py"],
    message=msg,
)
for l in lines:
    print(l)
print("R2137 close done rc=%d" % rc)
