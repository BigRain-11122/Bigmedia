# -*- coding: utf-8 -*-
# r2205_close.py - canonical accounting close for round R2205 (DIGEST-v20
# preset leg). finalize_state (tech#76/#149) + run_close_commit with
# canonical export writer (tech#148). Temp file rides tech#81 self-contained
# cleanup (deleted after success by the caller shell step).
import sys, os
sys.path.insert(0, os.path.join('src', 'os'))
from close_commit import finalize_state, run_close_commit

LOG = (u"2026-10-14 00:5x R2205: \u5b9e\u6d3b\u8f6e\u00b7main#28 DIGEST-v20 CPU \u9884\u7f6e\u817f\u5168\u94fe\u6bd5"
u"\uff08\u591c\u7a97\u53d6\u6d3b\u00b7R2144 release \u626b\u63cf\u70b9\u89e3\u51bb\u6838=full234 \u4ecd False \u7ef4\u6301 MV \u4f1a\u8bdd\u57df\u96f6\u63a5\u89e6\uff09\u2014\u2014"
u"\u2460\u8f6e\u9996\u4e94\u67e5=group_scan \u516d\u9762 fresh 00:14 \u5168\u9759\uff08DECISIONS truly_new=0 \u6c34\u4f4d 155+LEDGER @BigStream 5 \u884c\u503c\u5b88\u951a"
u"+ORDERS rows=382 tail '10-13 23:5x'==stored \u6c34\u4f4d\u5e73\u3010row 382=@bm-c V3 \u4fee\u6279\u4e24\u8f6e\u5b9e\u51b5+QC \u4e2d\u7ee7=MV \u57df\u81ea\u6267\u56de\u6267\u4ef6"
u"\u00b7watermark 382 \u5df2\u5bf9\u9f50\u672c\u8f6e commit ack \u8865\u8f7d=R2204 \u9996\u626b 23:50 \u540e\u843d\u884c\u975e\u6f0f\u3011+ORIGIN-DELTA delta=0"
u"+DIGEST-SUPPLY advisory 1 row-date 10-13 age 1d=\u672c\u8f6e v20 \u4ea7\u7ebf\u6d88\u8d39\u627f\u63a5\uff09+origin_gap QUIET ahead0 behind0"
u"+own orders \u951a O-20260908-1105 mtime \u7ef4\u6301+\u6811=MV-lane \u9884\u671f\u810f\u9762\u96f6\u9501\uff08R1745 \u96f6\u63a5\u89e6\u627f\u7ee7\uff09\uff1b"
u"\u2461\u53d6\u6d3b=main#28 \u95e8\u5df2\u6ee1\u8db3\uff08\u6210\u7247\u5448\u62a5+CEO \u590d\u8bc4 60 \u5206\u5728\u6848\u00b7R2149 \u53f2\u6e90\u6269\u5bb9\u5e76\u5165 10-13 \u7c07"
u"\u00b7CPU \u9884\u7f6e\u817f\u6210\u7247\u56de\u6267\u540e\u5373\u9886=\u591c\u7a97 CPU \u9762 O-20261013-2215 \u5f00\u653e\u4ee4\u7a97\uff09"
u"\u2192**DIGEST-v20\u300a\u57ce\u5e02\u76d8\u70b9 020\u00b7\u6b7b\u7ebf\u51b2\u523a\u65e5\u6570\u5b57\u76d8\u70b9\u300bM0-M4 \u5168\u94fe\u6bd5**\uff1aM0 7/8 A \u6863"
u"\uff08\u4e8c\u5341\u8fde\u6bcd\u9898\u00b7\u300c\u8d76\u6b7b\u7ebf\u7684\u65e5\u5b50\u00b7\u6700\u9ad8\u4ee4\u662f\u8d28\u91cf\u95f8\u300d\u53cd\u5dee\u94fe\uff09\u2192M1 18 \u65ad\u8a00 ALL GREEN"
u"\uff08.c3-tmp/build_digest20.py\u00b7m1-assert-r2205.txt\uff1aA1 43 \u884c\u53f0\u8d26+A1b 18 \u9053 CEO \u4ee4"
u"+A2a \u5f15\u6587 verbatim\uff08**\u4e71\u7801\u8bfb\u6570\u8bef\u5224\u7531\u673a\u6838\u6293\u51fa\u52d8\u6b63**\uff1aCEO \u539f\u8bdd\u6b63\u8eab=\u300c\u5e94\u8be5\u8bf4 "
u"\u6bcf\u4e2a\u5757\u9762\u90fd\u8981\u662f\u5168\u7403\u4e00\u6d41\u7684\uff0c\u4e0d\u8981\u51fa\u6765\u5783\u573e\u73a9\u610f\u300d\uff09+A2b/c \u590d\u8bc4 60 \u5206+\u2468\u4e5d\u9879"
u"+A2d 90 \u5206\u95e8\u69db+A2e 9/9+A2f 41 \u66f2+A2g \u4e09\u4ee4\u53f7+A2h/i \u95f8>\u6b7b\u7ebf+\u4ea7\u7ebf\u6bcd\u6cd5\uff09"
u"\u2192M2 --poster exit 0+em 40 \u6863\uff08budget 23.0em \u6700\u957f\u884c 22.35em margin +0.65em"
u"\u00b7\u521d\u8dd1 line2 23.45em FAIL\u2192\u300c\u00b7\u300d\u7a7a\u683c\u6536\u7d27\u81ea\u64b0\u884c=\u7248\u5f0f\u4fee\u53c2\u975e\u5f15\u6587\u3010R293 \u5f8b\u3011\u2192\u590d\u68c0\u5168\u7eff"
u"\u00b7em-check-r2205.txt\uff09+\u9a8c\u56fe\u4e94\u68c0 5/5 \u4e00\u6b21\u8fc7\u521d\u7a3f\u5373\u6b63\u5b57\uff08\u591a\u6a21\u6001\u8f6c\u5199\u9010\u5b57\u5168\u4e2d"
u"\u00b7\u96f6\u91cd\u53e0\u96f6\u8d8a\u754c\u96f6\u6298\u884c\u00b7\u6765\u6e90\u884c\u300c\u57fa\u4e8e\u7845\u57fa\u57ce\u5e02\u771f\u5b9e\u4e8b\u4ef6\uff08\u6b7b\u7ebf\u51b2\u523a\u65e5\u4ee4\u6279\u53f0\u8d26\u6863\u6848\uff09\u300d\u95ed\u5408"
u"\u00b7AIGC \u89d2\u6807\u6e05\u6670\uff09\u2192M3 \u56db\u7981\u96f6\u4e2d\u2192M4 \u56db\u68c0\u8fc7\uff08\u8131\u654f=\u4e91\u7aef\u79ef\u5206/\u591c\u6ce2\u5355\u6570\u96f6\u5165\u5361\u9762"
u"+MV \u6267\u884c\u9762\u7ec6\u8282\u53ea\u5165\u4ee4\u6279\u8ba1\u6570=v18/v19 \u540c\u578b\u5206\u754c\uff09\u2192e4 trio staged"
u"\uff08MC-20261014-DIGEST-v20-tmp/\u00b7e4_call.py=tech#113 \u751f\u6210\u5668\u6b63\u5178\u51fa\u4ef6+e4-material.md+e4-body.txt\uff09"
u"\u2192**F-184 \u9884\u6307**\uff08fire \u961f\u5217\u6df1\u5ea6\u4e94\u4ef6 F-180/181/182/183/184"
u"\u00b7main#31 \u961f\u5217\u884c+main#28 done \u6807+README \u53f0\u8d26\u884c\u4e09\u4ef6\u843d\u4f4d\uff09\uff1b"
u"\u2462fire_consume --launch v20 e4_call.py --ledger=no-fire rc1 reason=card-no-fire: mv-active"
u"\uff08MV sprint \u4f1a\u8bdd 17.9min \u6d3b\u6027=\u8ba9\u4f4d\u6b63\u786e\u4fa7\u00b7\u4e94\u4ef6 fire-ready carried\u00b7\u771f\u7a97=mv \u9759+VRAM \u95e8\u5f00\uff09\uff1b"
u"\u2463\u4e09\u63a2\u9488\u5e26\u5185=board 0 FAIL\uff085 \u9898 10 \u7a3f 5 in production\uff09/readiness 3 \u963b\u585e\u7686\u5916\u90e8 CEO \u9762"
u"\uff08\u8d26\u53f7\u6279\u6b21\u2460+M4 GATE 6/10+#17 needs-CEO\uff09+1 \u53d1\u73b0 react-v16 unannot"
u"\uff08R2118 \u88c1\u5b9a\u7ef4\u6301\u00b7F-183 \u767b\u8bb0\u5373\u6e05\u00b7v20 renders mp4 \u540c\u65cf\u9884\u671f\u6ce8\u8bb0=F-184 \u767b\u8bb0\u5373\u6e05\uff09"
u"/loop_health 3F+29x W \u7686\u5728\u6848\u53f2\u5b9e\uff08\u4e09 outage \u7a97+drift 18\u226421 adjudicated\uff09\uff1b"
u"\u2464\u4f8b\u884c\u4ef6=10-14 \u65e5\u62a5\u5f53\u8f6e\u8865\u4ea7\u6bd5\uff08daily_brief.py \u96f6 token\u00b720 \u6761\u53cc\u6e90 ok\uff09\u00b7W42 \u5468\u5ba1\u5728\u6848\uff08R2011\uff09"
u"\u00b7GB \u2463 \u4e0b\u671f 10-15 \u22647d \u8df3\u8fc7\u00b7export=\u672c\u8f6e\u5b9e\u51b5\u53d8\u5316\u8d70 tech#148 canonical writer \u6b63\u8eab\u5237\uff08close --export-patch\uff09"
u"\u00b7HQ-FEEDBACK \u4e0d\u5199\uff08\u96f6\u96c6\u56e2\u5c42\u65b0 open \u95ee\u9898\uff09\u00b7T1 \u50ac\u529e\u65e0\u8d85\u7ebf\u9879\uff08\u8d26\u53f7\u7269\u7406\u4ef6=\u5448\u73b0\u72b6\u884c\u4e0d\u50ac\u529e\uff09"
u"\u00b7tokens:local=0\uff08\u673a\u6838/\u6e32\u67d3/\u751f\u6210\u5668=\u96f6\u672c\u5730\u6a21\u578b\u4ea7\u51fa\u8c03\u7528\u00b7P-54\u2465 \u8ba1\u91cf\u5f8b\uff09\uff1b"
u"\u2465\u961f\u5217\u8865\u8d27\u6b65=main#31\uff08DIGEST-v20 \u8bc4\u5ba1\u817f=fire \u961f\u5217\u6df1\u5ea6\u4e94\u884c\u771f\u79cd\u5b50\uff09"
u"\u00b7\u4e34\u65f6\u4ef6\u6e05\u7406\u94a9=.c3-tmp r2205 \u4e09\u4ef6\uff08build+ledger_edits+close\uff09\u8f6e\u672b\u5220\u51c0"
u"\u2014\u2014\u4e0b\u8f6e=MV \u8ba9\u4f4d\u5373 fire \u63a5\u529b\u5224\u8bfb\uff08\u4e94\u4ef6\uff09+10-14 \u65e5\u62a5\u5728\u6848\u4e0d\u91cd\u8dd1"
u"+08:00 tech#92/#126 \u6743\u5a01\u7a97\u8bfb\u6570+\u6668\u7a97\u56de\u6eda\u5e8f\uff08re-enable MiniGameOllama \u53cc\u4efb\u52a1\uff09")

FOCUS = (u"MV-yield fire relay (F-180~184 five-deep queue) + 10-14 08:00 tech#92/#126 "
u"authoritative window read + morning rollback (re-enable MiniGameOllama tasks) "
u"+ Toonflow #110 LEG-3 workbench full-chain test (GPU/VRAM-gated)")

FILES = [
    'data/pipeline/fire-consume-ledger.jsonl',
    'data/storylines/cards/README.md',
    'state/queue/main.md',
    'data/intel/daily/2026-10-14.md',
    'data/storylines/cards/MC-20261014-DIGEST-v20/cards.json',
    'data/storylines/cards/MC-20261014-DIGEST-v20/MC-20261014-DIGEST-v20.png',
    'data/storylines/cards/MC-20261014-DIGEST-v20/subs.srt',
    'data/storylines/cards/MC-20261014-DIGEST-v20/em-check-r2205.txt',
    'data/storylines/cards/MC-20261014-DIGEST-v20/m1-assert-r2205.txt',
    'data/storylines/cards/MC-20261014-DIGEST-v20-tmp/e4_call.py',
    'data/storylines/cards/MC-20261014-DIGEST-v20-tmp/e4-body.txt',
    'data/storylines/cards/MC-20261014-DIGEST-v20-tmp/e4-material.md',
    'src/os/state.json',
    'docs/status-export.json',
]

MSG = ("R2205: DIGEST-v20 preset leg done -- MC-20261014-DIGEST-v20 M0-M4 green "
       "(m1-assert 18/18: 10-13 cluster 43 rows/18 CEO orders; em 40dang "
       "22.35<23.0; poster+verify 5/5); e4 trio staged (tech#113), F-184 "
       "pre-pointed (main#31, depth five F-180..183 ahead); main#28 done "
       "(advisory 10-13 consumed); orders row 382 ack (MV-domain receipt, "
       "view-only); next: fire relay on GO + 08:00 tech#92/#126 + morning "
       "rollback [via bm-a]")

PATCH = {
    "do": (u"R2205 \u591c\u7a97\uff1aDIGEST-v20\u300a\u57ce\u5e02\u76d8\u70b9 020\u300bCPU \u9884\u7f6e\u817f\u6bd5"
           u"\uff08\u673a\u6838 18 \u65ad\u8a00+\u9a8c\u56fe 5/5\uff09\u00b7F-184 \u9884\u6307\u00b7fire \u4e94\u4ef6\u5019 MV \u8ba9\u4f4d\u3002"),
    "results": [
        [u"DIGEST-v20 \u9884\u7f6e\u817f\u6bd5", "r2205"],
        [u"fire no-fire x5", "f180"],
        [u"row 382 ack", "orders"],
        [u"F-184 \u9884\u6307", "v20"],
    ],
    "live": [
        (u"\u5f53\u524d\u6d3b\uff1aDIGEST-v20 \u6b7b\u7ebf\u51b2\u523a\u65e5\u6570\u5b57\u76d8\u70b9\u5361 CPU \u9884\u7f6e\u817f\u6bd5"
         u"\uff08M0-M4+e4 trio staged\uff09\u00b7\u8bc4\u5ba1\u817f F-184 gated fire \u7a97\uff08F-180~183 \u524d\u5e8f\uff09\u3002"),
        (u"\u6700\u8fd1\u5b9e\u7269\uff1adata/storylines/cards/MC-20261014-DIGEST-v20/MC-20261014-DIGEST-v20.png"
         u"\uff0810-14 00:5x\u00b7m1-assert 18 \u65ad\u8a00\u5168\u7eff+\u9a8c\u56fe\u4e94\u68c0 5/5\uff09\u3002"),
        (u"\u4e0b\u4e2a\u91cc\u7a0b\u7891\uff1aMV \u8ba9\u4f4d\u540e F-180~184 fire \u63a5\u529b\uff08\u7a97 \u226410-15\uff09"
         u"\uff1b10-14 08:00 tech#92/#126 \u6743\u5a01\u7a97+\u6668\u7a97\u56de\u6eda\uff08MiniGameOllama \u53cc\u4efb\u52a1 re-enable\uff09\u3002"),
    ],
}

finalize_state(LOG, focus=FOCUS)
rc, lines = run_close_commit(files=FILES, message=MSG, export_patch=PATCH)
for ln in lines:
    print(ln.encode('ascii', 'replace').decode('ascii'))
print('CLOSE_RC=%d' % rc)
raise SystemExit(0 if rc == 0 else 1)
