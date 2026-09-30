# -*- coding: utf-8 -*-
"""R664 close: R663 fast-exit hole absorption (tick 662->664, R656+R657 precedent) + window
R659-R664 full -> batch close. P-61 export step. Round-trip fidelity checked first.
state.json indent=2 / status-export indent=1 (R659 export-rewrite law)."""
import json, io, sys
from datetime import datetime

now = datetime.now()
ts = now.strftime('%Y-%m-%d %H:%M:%S')
ts_iso = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')

log_line = (
    "R664: declared-idle \u7a7a\u8f6e\u5224\u5b9a+R663 \u5feb\u9000\u6d1e\u5438\u6536+\u7a97 R659-R664 \u6ee1\u516d\u6536\u7a97\uff08\u4e94\u9759+\u63a2\u9488\u7eff+\u53ef\u9886\u5e8f\u5c3d\u00b7P-20260928-02 \u2461\u2463\u5e8f\u00b7os-protocol \u00a76 \u5e76\u7a97\u5f8b\uff09\u2014\u2014"
    "\u2460\u8f6e\u53f7\u5b9a\u8c2d=R664\uff08beat \u9762\u5b9e\u8bc1\uff1a07:12 \u8f6e .out \u7a7a 4s \u5feb\u9000 exit=0 \u96f6\u5de5\u4ef6=R663 \u7a7a\u8d26\u6d1e\u3010R656+R657 \u5148\u4f8b\u578b\u3011\u00b7\u672c\u8f6e 07:22 \u8d77\u00b7tick 662\u2192664 \u53cc\u8df3\u5438\u6536=account-lag \u6536\u8d26\u81ea\u5e73\uff09+\u73af\u5883\u6ce8\u8bb0=CLI \u68c0\u51fa\u65b0 project hook cockpit-heartbeat\uff08blocked-untrusted \u6001\u00b7\u4e0d\u4fe1\u4efb\u4e0d\u52a8\u4f5c=bm-a/CEO \u51b3\u7b56\u9762\u00b7\u4ec5\u8bb0\u5f55\uff09\uff1b"
    "\u2461\u4e94\u67e5\u9759\uff1a\u65e0\u65b0\u4ee4\uff08orders \u9876=O-20260928-1910 19:12:33 \u951a\u672a\u52a8\uff09+\u65e0\u65b0\u96c6\u56e2\u8f6c\u529e\uff08ledger \u516d\u6a21\u5f0f 34 \u884c=\u951a\u00b7rowdiff vs r644_lednew5 \u57fa\u7ebf NEW=0 GONE=0=r663_probe.py \u5b9e\u8dd1\u96f6\u65b0 CEO \u4ee4\u7ea7\u4e8b\u4ef6\u3010#67 \u89e6\u53d1\u5f8b\u4e0d\u89e3\u9501\u3011\uff09+\u65e0\u65b0\u51b3\u7b56\u884c\uff08decisions UTF8 \u975e\u7a7a\u884c 68=\u951a\uff09+production=open \u81ea\u6108\u6838\u5728\u4f4d\u96f6\u7ffb\u6b63+\u65e0 index.lock\uff1b"
    "\u2462\u6811\u6001=bm-a codex \u6279\u672a\u95ed\uff08README/city-humanities worktree \u672a\u6682\u5b58\u00b7mtime 04:06:09/04:06:16 \u5b9e\u8bfb\u672a\u52a8\u00b7HEAD b8344d0 R658 \u540e\u96f6\u65b0 commit\uff09=\u8ba9\u4f4d\u7ef4\u6301+untracked \u81ea\u4ea7 tmp \u65cf\u9884\u671f\u6001+state/status-export M=\u5e76\u7a97\u81ea\u8bb0\u8d26\u9884\u671f\u6001\uff1b"
    "\u2463\u53ef\u9886\u5e8f\u5c3d\uff08\u672c\u8f6e\u8f83 R662 \u589e\u503c\u6838=\u4f8b\u884c\u4ef6\u53cc\u7a97 Test-Path \u5b9e\u8bc1\uff1a\u6708\u5ea6\u7edf\u8ba1\u6ce8\u8bb0 R-20260928-03 \u5728\u6848\u3010\u226409-30 \u7a97\u5df2\u6ee1\u8db3\u00b7R661/R662 \u4f8b\u884c\u4ef6\u6e05\u5355\u672a\u5217\u6b64\u4ef6\u00b7\u672c\u8f6e\u8865\u6838\u9632\u6f0f\u3011+W40 \u5468\u5ba1 R576 \u5728\u6848\uff09\uff1b"
    "#86 \u56db\u817f\u5168 gated\uff08a \u6e90\u95ed/b \u951a\u6b62 C-00030 False \u672c\u8f6e Test-Path \u590d\u6838/c+d bm-a \u8ba9\u4f4d\u533a\uff09\u00b7#70 OSS \u4e0b\u7a97\u5207\u7247 2=21:40 \u540e\u5f00\u672a\u5230\uff08\u5207\u7247 1 \u5df2\u6bd5 R644=\u7a97\u9762\u4e49\u52a1\u8db3\uff09\u00b7#67 \u96f6\u65b0\u4e8b\u4ef6\u00b7#63 \u56fe\u9274 supply-gated \u540c\u951a\u00b7#59 REACT v6 \u6302 09-30 \u7a97\uff08\u4eca\u65e5\u7a97 v5 R643 \u5df2\u7528\uff09\u00b7#31 ch5 \u7a3f\u672a\u843d\uff08bm-a \u9762\uff09\u00b7#78 \u7d20\u6750\u95e8\u524d\u7f6e blocked\u00b7#17 needs-CEO\u00b7#66 blocked-on-CEO\u00b7#57 10-07/#80 10-01/#82 10-05 \u6302\u8d26\u7a97\u00b7queue \u9876\u9879\u5168 gated\u2192W40 \u7a97\u63d0\u6848 P-1 \u5df2\u4ea4=\u4fdd\u62a4\u6001\u8c41\u514d\u9762\u5728\u6848\u2192\u4e00\u884c\u58f0\u660e\u6536\u8f6e\u5408\u6cd5\uff08\u7981\u4ee5\u58f0\u660e\u4ee3\u53d6\u6d3b\u81ea\u68c0=\u53ef\u9886\u9879\u9010\u4ef6\u6838\u8fc7\u975e\u300c\u60f3\u4e0d\u51fa\u6d3b\u300d\uff09\uff1b"
    "\u2464\u4e09\u63a2\u9488=board 0 FAIL\uff085 \u9898 10 \u7a3f\u00b75 in production\uff09/readiness 3 \u963b\u585e 0 \u53d1\u73b0\uff08\u8d26\u53f7\u6279\u6b21\u2460+GATE 6/10+#17 \u7686\u5916\u90e8 CEO \u9762\u00b7\u963b\u585e\u2260\u5931\u8d25\u53e3\u5f84\uff09/loop_health 3 FAIL+42 WARN \u5168\u5728\u6848\u7c7b\uff082 outage \u540c\u4e8b\u4ef6\u8db3\u8ff9\u5df2\u88c1\u5b9a\u4e0d\u91cd\u590d\u89e6\u53d1+account-lag beat664>tick662=tick664 \u6536\u8d26\u81ea\u5e73\u00b742 WARN \u4e0e R661/R662 \u6301\u5e73\u96f6\u65b0\u589e\uff09\uff1b"
    "\u2465\u4f8b\u884c\u4ef6\uff1a\u65e5\u62a5 09-29 \u5728\u6848\u4e0d\u91cd\u8dd1\uff08R637 \u65ad\u8f6e\u4ef6\u8865\u4ea7\uff09/W40 \u5468\u5ba1\u5728\u6848\uff08R576\uff09/W41 \u5468\u62a5=10-05 \u540e\u9996\u4e2a\u5468\u8f6e/global-benchmarks \u22647 \u8df3\u8fc7\uff08\u4e0b\u671f 10-01=#80 \u5e76\u7a97\uff09/T1 \u50ac\u529e=\u5df2\u88c1\u9879\u505c\u7528\u53e3\u5f84/\u5f53\u65e5\u65e0\u96c6\u56e2\u5c42\u65b0 open \u95ee\u9898=HQ-FEEDBACK \u4e0d\u5199\uff08\u96f6\u81a8\u80c0\uff09/tokens:local=0\uff08\u63a2\u9488+\u6838\u9a8c\u7eaf\u811a\u672c\u96f6\u672c\u5730\u6a21\u578b\u8c03\u7528\u00b7P-54\u2464 \u8ba1\u91cf\u5f8b\uff09\u00b7\u53d1\u5e03\u9501=M5 \u8d26\u53f7\u7269\u7406\u4ef6\u4e0d\u53d8\uff08\u672a\u4e0a\u7ebf=\u672a\u6d4b\u91cf\uff09\uff1b"
    "\u2466\u6536\u7a97=P-61 \u5bfc\u51fa\u6b65\u7167\u8d70\uff08export_ts \u5237+results 664 \u884c\u672b\u4f4d\u8ffd\u52a0+OS \u884c\u5347 tick 664\uff09+batch commit+push\uff08pathspec=state.json+status-export \u4e24\u4ef6\u5957\u00b7codex \u8ba9\u4f4d\u533a\u96f6\u63a5\u89e6\u00b7commit \u6ce8\u533a\u95f4 R659-R664\u00b7R654-R657 \u5148\u4f8b\uff09\u2014\u2014"
    "\u4e0b\u8f6e R665=\u65b0\u7a97 R665-R670 \u8d77\uff1a\u53ef\u9886\u5e8f=\u2460#86 codex\uff08\u8ba9\u4f4d\u89e3\u9664\u5224\u636e=bm-a \u6279\u95ed commit \u843d\u5730\u00b7C-00030 \u951a\u8f6e\u9996\u6838\uff09\u2461#70 OSS \u4e0b\u7a97\u5207\u7247 2\uff0821:40 \u540e\u00b7OH-20260929 \u7eed\u5199\uff09\u2462#67 \u89e6\u53d1\u5f8b\u2463#59 REACT v6=09-30 \u7a97 P-1 \u8bd5\u70b9\u4ef6 2/2 \u7ec8\u5224\u3002"
)
full_log = now.strftime('%Y-%m-%d %H:%M') + " " + log_line
task = log_line[:60]

focus_new = (
    "R665: \u7a7a\u8f6e\u5224\u5b9a\u8def\u5f84\u5f00\u8f6e\uff08\u65b0\u7a97 1/6=R665-R670\uff09\u2014\u2014\u53ef\u9886\u5e8f=\u2460#86 codex \u7eed\u91c7\u4f59\u91cf\uff08\u8ba9\u4f4d\u89e3\u9664\u5224\u636e=bm-a \u6279\u95ed commit \u843d\u5730\u00b7\u56db\u817f\u6001\uff1aa \u817f\u6e90\u95ed\u3010pools.json \u53f6\u6570 1440\u3011/"
    "b \u817f\u951a\u6b62 C-00029 supply-gated\u3010\u624b\u5199\u951a\u6b63\u5178\u4f4d=census/anchors/\u00b7registry \u751f\u6210\u5361\u2260\u951a R316 \u88c1\u5b9a\u3011/c+d \u817f=bm-a \u8ba9\u4f4d\u533a\uff09"
    "\u2461#70 OSS \u4e0b\u7a97\u5207\u7247 2\uff0809-29 21:40 \u540e\u5f00\u00b7OH-20260929-bigstream.md \u7eed\u5199\u00b7\u5b9e\u641c\u9762 \u22652+\u5019\u9009 \u22651 \u4e94\u95e8\u8bc4\u4f30\uff09"
    "\u2462#67 \u7f16\u5e74\u53f2\u4e8b\u4ef6\u5019\u9009\uff08ledger \u65b0 CEO \u4ee4\u7ea7\u4e8b\u4ef6\u89e6\u53d1\u5f8b\u00b7\u53cd\u81a8\u80c0\u5f8b\u7167\u5b88\uff09"
    "\u2463#59 REACT v6=09-30 \u70ed\u70b9\u7a97 P-1 \u8bd5\u70b9\u4ef6 2/2 \u7ec8\u5224\u2014\u2014W40 \u7a97\u63d0\u6848 P-1 \u5df2\u4ea4\uff08\u8bd5\u70b9 1/2 \u5224\u8bfb\u6bd5\uff09"
    "\u2014\u2014\u4e94\u67e5\u951a=orders \u9876 O-20260928-1910 19:12:33\u00b7ledger 34\uff08rowdiff \u57fa\u7ebf=.c3-tmp/r644_lednew5.txt\u00b7\u516d\u6a21\u5f0f\u00b7CaseSensitive \u8ba1\u6570\u5f8b\uff09\u00b7decisions 68"
    "\u2014\u2014R663 \u5feb\u9000\u6d1e\u5df2\u5438\u6536\uff08tick=664 \u5bf9\u8d26\u5e73\uff09\u00b7\u7a97 R659-R664 \u5df2\u6536\uff08batch commit \u843d\u5730\uff09\u3002"
)

# ---- state.json ----
with io.open('src/os/state.json', encoding='utf-8') as f:
    raw_state = f.read()
d = json.loads(raw_state)
old_tick = d['tick']
assert old_tick == 662, old_tick
rt = json.dumps(d, ensure_ascii=False, indent=2)
if rt != raw_state:
    if rt + '\n' == raw_state:
        state_trail = '\n'
    elif rt == raw_state.rstrip('\n') and not raw_state.endswith('\n'):
        state_trail = ''
    else:
        print('STATE ROUNDTRIP MISMATCH len', len(rt), len(raw_state))
        for i, (a, b) in enumerate(zip(rt, raw_state)):
            if a != b:
                print('first diff at', i, repr(rt[i-30:i+30]), '||', repr(raw_state[i-30:i+30]))
                break
        sys.exit(2)
else:
    state_trail = ''
print('state roundtrip OK')
d['tick'] = 664
d['focus'] = focus_new
d['log'].append(full_log)
d['ts'] = ts
d['task'] = task
with io.open('src/os/state.json', 'w', encoding='utf-8', newline='\n') as f:
    f.write(json.dumps(d, ensure_ascii=False, indent=2) + state_trail)
print('state.json written: tick 662->664 (R663 hole absorbed), log R664 appended, ts/task/focus refreshed')

# ---- status-export.json ----
with io.open('docs/status-export.json', encoding='utf-8') as f:
    raw_exp = f.read()
e = json.loads(raw_exp)
rt2 = json.dumps(e, ensure_ascii=False, indent=1)
if rt2 != raw_exp:
    if rt2 + '\n' == raw_exp:
        exp_trail = '\n'
    elif rt2 == raw_exp.rstrip('\n') and not raw_exp.endswith('\n'):
        exp_trail = ''
    else:
        print('EXPORT ROUNDTRIP MISMATCH len', len(rt2), len(raw_exp))
        for i, (a, b) in enumerate(zip(rt2, raw_exp)):
            if a != b:
                print('first diff at', i, repr(rt2[i-30:i+30]), '||', repr(raw_exp[i-30:i+30]))
                break
        sys.exit(3)
else:
    exp_trail = ''
print('export roundtrip OK')
e['export_ts'] = ts_iso

res_desc = (
    "R664 declared-idle+R663 \u5feb\u9000\u6d1e\u5438\u6536 tick662->664\uff0807:12 \u8f6e exit=0 \u96f6\u5de5\u4ef6\u00b7R656+R657 \u5148\u4f8b\uff09+\u7a97 R659-R664 \u6ee1\u516d\u6536\u7a97\uff08batch commit+push \u6ce8\u533a\u95f4\uff09\uff1a"
    "\u4e94\u67e5\u951a\u9759\uff08orders O-1910/ledger 34 rowdiff 0\u3010r663_probe \u516d\u6a21\u5f0f\u5b9e\u8dd1\u3011/decisions 68\uff09"
    "\u00b7\u589e\u503c\u6838=\u4f8b\u884c\u4ef6\u53cc\u7a97\u5b9e\u8bc1\uff08\u6708\u5ea6\u7edf\u8ba1\u6ce8\u8bb0 R-20260928-03 \u5728\u6848\u226409-30 \u7a97\u5df2\u6ee1\u8db3+W40 \u5468\u5ba1 R576 \u5728\u6848\uff09"
    "\u00b7bm-a codex \u6279\u672a\u95ed\u8ba9\u4f4d\u7ef4\u6301\uff08mtime 04:06 \u672a\u52a8\uff09"
    "\u00b7\u53ef\u9886\u5e8f\u5c3d\uff08#86 \u56db\u817f gated/#70 21:40 \u672a\u5230/#67 \u96f6\u65b0\u4e8b\u4ef6/C-00030 False/queue gated/W40 \u63d0\u6848 P-1 \u5df2\u4ea4\uff09=\u4fdd\u62a4\u6001\u8c41\u514d\u9762"
    "\u00b7\u4e09\u63a2\u9488 board 0F/readiness 3 \u5916\u90e8 0 \u53d1\u73b0/loop 3F+42W \u5728\u6848\u7c7b\uff08account-lag tick664 \u6536\u8d26\u81ea\u5e73\uff09"
    "\u00b7\u73af\u5883\u6ce8\u8bb0=CLI \u68c0\u51fa\u65b0 project hook cockpit-heartbeat\uff08blocked-untrusted\u00b7\u4e0d\u52a8\u4f5c\uff09"
    "\u00b7tokens:local=0\u00b7\u65b0\u7a97 R665-R670 \u8d77"
)
e['results'].append(["664", res_desc])

os_row_new = (
    "tick 664\uff1aR664 declared-idle \u7a7a\u8f6e\u5224\u5b9a+R663 \u5feb\u9000\u6d1e\u5438\u6536\uff0807:12 \u8f6e exit=0 \u96f6\u5de5\u4ef6\u00b7tick 662\u2192664 \u53cc\u8df3\uff09"
    "+\u7a97 R659-R664 \u6ee1\u516d\u6536\u7a97 batch commit+push\uff08pathspec \u4e24\u4ef6\u5957\u00b7codex \u8ba9\u4f4d\u533a\u96f6\u63a5\u89e6\uff09\uff1a"
    "\u4f8b\u884c\u4ef6\u53cc\u7a97\u5b9e\u8bc1\uff08\u6708\u5ea6\u7edf\u8ba1\u6ce8\u8bb0 R-20260928-03+R576 W40 \u5468\u5ba1\u7686\u5728\u6848\uff09"
    "\u00b7bm-a codex \u6279\u672a\u95ed\u8ba9\u4f4d\u7ef4\u6301\uff08mtime 04:06 \u672a\u52a8\uff09"
    "\u00b7\u4e09\u63a2\u9488 board 0F/readiness 3 \u7686\u5916\u90e8 0 \u53d1\u73b0/loop 3F+42W \u5728\u6848\u7c7b\uff08account-lag tick664 \u6536\u8d26\u81ea\u5e73\uff09"
    "\u00b7tokens:local=0\u2014\u2014\u4e0b\u8f6e R665 \u65b0\u7a97 R665-R670 \u53ef\u9886\u5e8f=\u2460#86\uff08bm-a \u6279\u95ed\u5224\u636e\uff09\u2461#70 \u5207\u7247 2\uff0821:40 \u540e\uff09\u2462#67 \u89e6\u53d1\u5f8b\u2463REACT v6=09-30 \u7a97"
)
assert e['outs'][0][0] == 'OS \u5faa\u73af', e['outs'][0][0]
e['outs'][0][1] = os_row_new

with io.open('docs/status-export.json', 'w', encoding='utf-8', newline='\n') as f:
    f.write(json.dumps(e, ensure_ascii=False, indent=1) + exp_trail)
print('status-export.json written: export_ts + results 664 + OS row tick 664')
print('DONE ts=' + ts)
