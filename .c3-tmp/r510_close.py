# -*- coding: utf-8 -*-
# R510 close-out: state.json (tick/log/ts/task/focus) + status-export.json refresh.
# json.load/dump full rewrite (trailing-comma hazard root-fix, R483/R504 lineage).
import io, json, re
from datetime import datetime

NOW = datetime.now()
STAMP = NOW.strftime("%Y-%m-%d %H:%M:%S")
TS_ISO = NOW.strftime("%Y-%m-%dT%H:%M:%S+08:00")

SP = r"src\os\state.json"
SX = r"docs\status-export.json"

log_line = (
    "2026-09-27 %s R510: \u751f\u4ea7\u8f6e\u00b7#79 \u4ef61 L-\u5361\u62c6\u6761\u8bd5\u6295\u8d77\u94fe\u4e94\u817f\u6bd5\uff08O-1050 \u8bae\u7a0b 2 \u7f3a\u53e3\u8865\u4ef6\u9884\u4ea7\u7ebf\u00b7\u5b9e\u6d3b\u8f6e\u00b7commit \u542b P-202609-27-07\uff09\u2014\u2014\u2460\u8f6e\u9996\u4e94\u67e5\u9759\uff08orders 35 \u4ef6\u96f6\u65b0\u589e\u00b7\u951a=O-1050 mtime 11:57:30=R509 \u6536\u8d26\u8db3\u8ff9/ledger \u4e94\u6a21\u5f0f 30=\u951a\u96f6\u65b0\u8f6c\u529e/decisions 45=\u951a\u96f6\u65b0\u884c/production open \u81ea\u6108\u6838\u5728\u4f4d/\u6811\u6001=\u4ec5\u81ea\u4ea7\u9884\u671f\u4ef6\u2014.sc003 \u4e24 tmp=SC-003 \u6279\u672a\u95ed\u9884\u671f\u6001\u2011\uff09+\u4e09\u63a2\u9488\u5b9a\u8c32\u7eff\uff08board 0 FAIL 5 \u9898 10 \u7a3f 5 in production/readiness 3 \u963b\u585e\u7686\u5916\u90e8 CEO \u9762 0 \u53d1\u73b0 46 renders \u5168\u6ce8\u8d26/loop_health 2 FAIL+21 WARN \u5168\u5728\u6848\u5b9a\u578b\u96f6\u65b0\u589e\u201449min=R425 \u8db3\u8ff9\u5df2\u88c1\u5b9a\u00b7account-lag done510>tick509=\u672c\u8f6e\u5728\u98de done-beat \u5148\u884c\u77ac\u6001 lag\u22652 \u672a\u7834\u7ebf\u00b7\u672c\u8f6e\u6536\u8d26 tick510 \u5373\u5e73\u2011\uff09\uff1b\u2461#79 \u4ef61 \u4e94\u817f=LC-001 \u5f90\u6839\u798f\u62c6\u6761\uff08\u6e90\u5361 CENSUS-v7 F-026\u00b735 \u5361\u9009\u4f18\u5b9a\u8c32 M0 \u56db\u7ef4\u5206 7/8 A \u6863\u2014\u53cd\u91cd\u590d\u6392\u9664 DIGEST-v1 \u7acb\u56fd\u65e5=F-001 \u89c6\u9891\u53f7\u7a3f\u540c\u6e90/\u987e\u963f\u51e4=SC-003-01 \u5728\u4ea7\u540c\u4eba\u7269\u00b7\u5165\u56f4\u4e09\u4ef6\u5bf9\u7167=\u5f90\u6839\u798f 7/8 vs \u5f52\u6863\u8005-07 6/8 \u672f\u8bed\u8bed\u5883\u95e8\u69db vs DIGEST-v6 6/8 \u5185\u90e8\u4e8b\u4ef6\u2011\uff09\u2192\u62cd\u7a3f 12 \u62cd v1-v5 \u7559\u6863\uff08222\u2192197 \u5b57\u00b7\u5361\u7247\u951a\u70b9\u5217\u5168\u884c\u96f6\u52a8\uff09\u2192S1 v1.5+L18-L20 \u95e8 10/10 PASS \u96f6\u8fdd\u5f8b\u4e00\u6b21\u8fc7\uff0812:06:30 \u70ed\u8f7d\u5feb\u843d\u00b7\u5224\u8bcd\u6863 20260927-120630-S1-script+expert-calls \u884c wrapper \u81ea\u52a8\u00b7\u76f2\u8bc4\u6750\u6599 v1 \u5408\u89c4\u00b7\u673a\u68b0\u88c1\u4e0d\u56de\u7089\u53e3\u5f84\uff09\u2192M1 \u5373\u68c0 0 FAIL 0 WARN\uff08\u53e5\u62c6\u4e09\u5904 b2/b6/b9 \u00b7\u9ed1\u8bdd 12 \u8bcd\u96f6\u547d\u4e2d\u00b7\u56e0\u5b50/\u590f\u666e=\u6a21\u578b/\u6253\u5206\u767d\u8bdd\u6362\u4f4d\u00b7\u5361\u53e3\u5206\u5de5\uff09\u2192\u7a7a\u6c14\u9884\u7b97 65.72\u219260.83\u219259.75\u219259.20\u219258.16s \u56db\u9053\u673a\u68b0\u88c1=\u5b9a\u7a3f 1.84s \u4f59\u91cf fleet \u5e26\u5185\uff08\u4fe1\u6761/\u8d77\u6e90/\u5f15\u6587\u4fdd\u62a4\u884c\u96f6\u52a8\u00b7\u8bed\u4e49\u96f6\u6539\uff09\u2192TTS light \u5b9a\u7a3f\u97f3\u8f68 .lc001-tmp\uff08audio 58.19s \u542b room tone/subs 12 cues\u00b7BGM-A \u7eaf\u51c0\uff09\uff1b\u2462\u53f0\u8d26\u4e94\u4ef6=data/sources/lc001/ \u4e09\u4ef6\uff08beats v1-v5+README M0 \u9009\u4f18\u5b9a\u8c32+\u6750\u6599\uff09+renders README .lc001-tmp \u58f0\u660e\u884c+backlog #79 R510 \u6ce8+orders R510 \u6536\u884c+status-export \u5237\uff1b\u2463\u7a97\u53e3\u4ef6\u968f\u67e5\uff08#78 \u6e32\u67d3\u817f\u7ef4\u6301\u7d20\u6750\u9762\u524d\u7f6e=footage \u5c3e 09-25 19:46 \u672a\u5230\u4f4d r510_check\u00b7#72 \u4e92\u804a\u53f0\u8d26 0 \u547d\u4e2d\u7ef4\u6301\u6302\u8d26\u00b7#63 C-00030/31 \u951a\u4e0d\u5728\u4f4d supply-gated \u7167\u5b88\u00b7#59 REACT 09-28 \u5c4a\u65e5\u9886\u00b7#70 OH \u4e0b\u7a97 09-29 21:40\u00b7W40 \u5468\u81ea\u5ba1 09-28 \u5f00\u5468\uff09\uff1b\u2464\u4f8b\u884c\u4ef6\uff1a\u65e5\u62a5 09-27 \u5728\u6848\u4e0d\u91cd\u8dd1\uff08R443 \u8865\u4ea7\u4ef6\u00b709-28 \u4ef6=\u660e\u5c4a\u65e5\u968f\u7a97\u8865\u4ea7\uff09\u00b7global-benchmarks day3 \u22647 \u8df3\u8fc7\uff08\u4e0b\u671f ~10-01=#80 \u5e76\u7a97\uff09\u00b7T1 \u50ac\u529e=\u5df2\u88c1\u9879\u505c\u7528\u53e3\u5f84\u00b7\u5f53\u65e5\u65e0\u96c6\u56e2\u5c42\u65b0 open \u95ee\u9898=HQ-FEEDBACK \u4e0d\u5199\uff08\u96f6\u81a8\u80c0\u00b7ledger/decisions \u53cc\u951a\u9759\uff09\u00b7tokens:local=1\uff08S1 qwen2.5:14b \u8f6e\u5185\u843d\u5730\u8bb0\u8d26\u00b7\u672c\u5730 Ollama \u96f6 API token\u00b7P-54\u2465 \u8ba1\u91cf\u5f8b\uff09\u00b7\u53d1\u5e03\u9501=M5 \u8d26\u53f7\u7269\u7406\u4ef6\u4e0d\u53d8\uff08\u672a\u4e0a\u7ebf=\u672a\u6d4b\u91cf\uff09\u2014\u2014\u957f\u8f6e\u6ce8=\u8d77\u94fe+\u56db\u9053\u7a7a\u6c14\u9884\u7b97\u8fed\u4ee3+\u53f0\u8d26\u8017\u00b7\u8d85 25 \u5206\u949f\u9884\u7b97 WARN \u7ea7\u5982\u5b9e\u5165\u8d26\uff08loop_health heartbeat-gap \u9762\uff09\uff1b\u4e0b\u8f6e=R511 #79 \u4ef61 \u6e32\u67d3\u817f\uff08\u5bf9\u4f4d\u8868\u7d20\u6750\u63a2\u9488\u5148\u884c\u2192R-E\u2014--series-badge/--series-id=\u62c6\u6761 001 \u5019\u9009+\u00a74.5\u2015\u2192S2 \u4e09\u95e8\u2192E8\u2192M4\u2192F \u767b\u8bb0\u2192D15 \u843d\u4f4d\uff09\u2192\u4ef62 \u7a3f\u96c6 BS-006+ \u8d77\u94fe\u3002" % NOW.strftime("%H:%M")
)

focus_new = (
    "R511: #79 \u4ef61 \u6e32\u67d3\u817f\u8d77\u94fe\uff08LC-001 \u5f90\u6839\u798f\u62c6\u6761\uff1a\u5bf9\u4f4d\u8868 cards-v1-matched \u7d20\u6750\u63a2\u9488\u5148\u884c\u2014\u4e94\u6e90+citywatch \u51c0\u7a97 4.066s \u94fe\u590d\u7528\u00b7BS-005 0.17 FAIL \u6559\u8bad\u6267\u884c\u2015\u2192R-E shipinhao \u6e32\u67d3\u2014--series-badge/--series-id=\u62c6\u6761 001\u00b7\u6e90\u57ce\u5e02\u56fe\u9274 007 \u5019\u9009+\u00a74.5 \u4e09\u5f00\u5173\u00b7\u00a75.5 \u89d2\u6807\u5e38\u9a7b\u4f4d\u2015\u2192S2 \u4e09\u95e8\u2192\u5e27\u9a8c\u4e09\u5f8b\u2192E8 \u7ec8\u5ba1\u2014E4 \u53c2\u8003\u4eea\u968f\u884c\u2015\u2192M4\u2192F \u767b\u8bb0\u2192D15 \u843d\u4f4d=\u4ef61 \u6536\u53e3\uff09\u2192\u4ef62 \u7a3f\u96c6 BS-006+ \u8d77\u94fe\uff08\u677f\u6e90 drafts\u00b7\u62cd\u7a3f\u538b\u7f29\u94fe\u540c BS-002~004 \u5148\u4f8b\uff09\uff1b#78 \u6e32\u67d3\u817f\u7ef4\u6301\u7d20\u6750\u9762\u524d\u7f6e\uff08FluxVerse \u57ce\u5e02\u7a97\u9762\u5b9e\u5f55\u672a\u5230\u4f4d\u00b7\u8f6e\u9996\u63a2\u9488\u6838\u00b7\u5230\u4f4d\u5373\u5bf9\u4f4d\u8868 cards-v3-matched\u2192R-E\u2192S2\u2192E8\u2192M4\u2192F \u767b\u8bb0=\u8bae\u7a0b 3 \u6536\u53e3\uff09\uff1b\u7a97\u53e3\u4ef6\u968f\u67e5\uff08#59 REACT 09-28 \u5c4a\u65e5\u9886\u00b7daily_brief 09-28 \u7f3a\u5219\u5148\u8865\u4ea7\u00b7W40 \u5468\u81ea\u5ba1 09-28 \u5f00\u5468+\u6708\u5ea6\u7edf\u8ba1\u6ce8\u8bb0\u9996\u4ef6 \u226409-30\u00b7#72 BigLife \u4e92\u804a\u53f0\u8d26 \u226409-28 12:00 \u5230\u4f4d\u5373\u5e76\u5165 SC-003\u00b7#80 global-benchmarks 10-01 \u5e76\u7a97\u00b7#70 OH \u4e0b\u7a97 09-29 21:40 \u540e\u5f00\u00b7#63 C-00030/31 \u951a supply-gated \u7167\u5b88\uff09\uff1b\u63a2\u9488\u6267\u884c\u6ce8=loop_health account-lag +1 \u77ac\u6001=\u5c3e\u8f6e\u81eabeat \u6b8b\u5dee\u65e2\u88c1\u5b9a\u578b\uff08lag \u22652 \u624d=\u65b0\u65ad\u6d1e\u5224\u636e\uff09\uff1bdecisions \u951a=45\uff1bledger \u4e94\u6a21\u5f0f\u951a=30\uff08\u5927\u5c0f\u5199\u654f\u611f\u53e3\u5f84\uff09"
)

# --- state.json ---
with io.open(SP, encoding="utf-8") as f:
    st = json.load(f)
assert st["tick"] == 509, "tick drift: %s" % st["tick"]
st["tick"] = 510
st["log"].append(log_line)
st["ts"] = STAMP
st["task"] = log_line.split("R510: ", 1)[1][:60]
st["focus"] = focus_new
with io.open(SP, "w", encoding="utf-8") as f:
    json.dump(st, f, ensure_ascii=False, indent=1)
    f.write("\n")

# --- status-export.json ---
with io.open(SX, encoding="utf-8") as f:
    sx = json.load(f)
sx["export_ts"] = TS_ISO

# engineering dept machine-readable line (English, as-established)
for d in sx["depts"]:
    if d["n"] == "\u5de5\u7a0b\u6280\u672f\u90e8":
        d["s"] = ("R510: #79 piece-1 L-card clip-cut pilot kickoff done (LC-001 source=CENSUS-v7 F-026 selected by "
                  "M0 4-dim 7/8 A-grade; anti-dup exclusions DIGEST-v1 founding-day=F-001 same-source, GAF=SC-003-01 in-flight); "
                  "12-beat script v1->v5 archived; S1 v1.5+L18-L20 gate 10/10 PASS one-pass (12:06:30); M1 plain-language 0F/0W "
                  "after 3 sentence-splits; air-budget 65.72s->58.16s via 4 mechanical trims, 1.84s headroom in fleet band; "
                  "TTS light final track in .lc001-tmp; render leg next (probe-first matched-cards -> R-E shipinhao -> "
                  "S2 tri-gate -> E8 -> M4 -> F-reg -> D15 slot)")

# OS loop out row: current=R510, previous=R509
old_cur = sx["outs"][0][1]
sx["outs"][0][1] = ("tick 510\uff0cR510 \u751f\u4ea7\u8f6e\u00b7#79 \u4ef61 L-\u5361\u62c6\u6761\u8bd5\u6295\u8d77\u94fe\u4e94\u817f\u6bd5\uff08LC-001 \u5f90\u6839\u798f\uff1a35 \u5361\u9009\u4f18\u5b9a\u8c32=CENSUS-v7 F-026\u00b7M0 \u56db\u7ef4\u5206 7/8 A \u6863\u2014\u53cd\u91cd\u590d\u6392\u9664 DIGEST-v1 \u7acb\u56fd\u65e5=F-001 \u540c\u6e90/\u987e\u963f\u51e4=SC-003-01 \u5728\u4ea7\u2015+\u62cd\u7a3f 12 \u62cd v1-v5 \u7559\u6863+S1 v1.5+L18-L20 \u95e8 10/10 PASS \u96f6\u8fdd\u5f8b\u4e00\u6b21\u8fc7+M1 \u5373\u68c0 0 FAIL 0 WARN\u2014\u53e5\u62c6\u4e09\u5904\u2015+\u7a7a\u6c14\u9884\u7b97 65.72\u219258.16s \u56db\u9053\u673a\u68b0\u88c1\u5b9a\u7a3f 1.84s \u4f59\u91cf+TTS light \u5b9a\u7a3f\u97f3\u8f68 .lc001-tmp\uff09\u00b7\u4f59\u817f=\u5bf9\u4f4d\u8868\u7d20\u6750\u63a2\u9488\u5148\u884c\u2192R-E \u6e32\u67d3\u2192S2\u2192E8\u2192M4\u2192F \u767b\u8bb0\u2192D15 \u843d\u4f4d\u00b7#78 \u6e32\u67d3\u817f\u7ef4\u6301\u7d20\u6750\u9762\u524d\u7f6e\uff08FluxVerse \u5b9e\u5f55\u672a\u5230\u4f4d\uff09")
sx["outs"][0][2] = old_cur

# media-self-drive row
for row in sx["outs"]:
    if row[0] == "media-self-drive O-20260927-1050":
        row[2] = (row[2] + "; R510: #79 piece-1 clip-cut pilot LC-001 kickoff legs done "
                  "(M0 selection + script v5 + S1 10/10 one-pass + M1 0F/0W + air-budget 58.16s in-window + TTS final track); "
                  "render leg next")

# results rows: [0]=current round, tail=previous round
prev_line = sx["results"][0][1]
sx["results"][0] = ["510", "R510 \u751f\u4ea7\u8f6e\uff1a#79 \u4ef61 L-\u5361\u62c6\u6761\u8bd5\u6295\u8d77\u94fe\u4e94\u817f\u6bd5\uff08LC-001 \u9009\u5361\u5b9a\u8c32+\u62cd\u7a3f v5+S1 10/10 PASS \u4e00\u6b21\u8fc7+M1 0F0W+\u7a7a\u6c14\u9884\u7b97 58.16s \u5b9a\u7a3f+TTS \u5b9a\u7a3f\u97f3\u8f68\uff09\u3002\u63a2\u9488 board 0 FAIL/readiness 3 \u5916\u90e8\u963b\u585e 0 \u53d1\u73b0/loop_health 2F+21W \u5728\u6848\u5b9a\u578b\uff08account-lag +1 \u77ac\u6001\u6536\u8d26\u5373\u5e73\uff09\u3002"]
sx["results"][-1] = ["509", prev_line]

# expert-calls derived count (F3: derive, never hardcode)
cnt = 0
with io.open(r"docs\reviews\expert-calls.md", encoding="utf-8") as f:
    for ln in f:
        if re.match(r"^\|\s*20\d\d", ln):
            cnt += 1
for row in sx["results"]:
    if row[0].isdigit() and row[1].startswith("\u4e13\u804c\u4e13\u5bb6\u8c03\u7528"):
        row[0] = str(cnt)
        row[1] = "\u4e13\u804c\u4e13\u5bb6\u8c03\u7528\uff08expert-calls \u53f0\u8d26 %s \u884c\u00b7\u542b R510 LC-001 S1 \u95e8\u8c03\u7528\u00b7E4 \u53c2\u8003\u4eea=\u975e\u540d\u518c\u5e2d\u76f4\u8c03\u4e0d\u8ba1\u6570\uff09" % cnt

with io.open(SX, "w", encoding="utf-8") as f:
    json.dump(sx, f, ensure_ascii=False, indent=1)
    f.write("\n")

print("close OK tick=510 expert_calls=%d ts=%s" % (cnt, STAMP))
