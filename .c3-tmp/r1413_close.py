# -*- coding: utf-8 -*-
# R1413 close: waiting-state declared-idle one-line round (window 2/6, no commit)
# legs: state.json tick/log/ts/task + watermark phantom cleanup (D-20260930-1 artifact)
import json, io, datetime

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
now = datetime.datetime.now()
now_s = now.strftime("%Y-%m-%d %H:%M:%S")
hm = "%d:%dx" % (now.hour, now.minute // 10)

sp = repo + r"\src\os\state.json"
st = json.load(io.open(sp, encoding="utf-8"))

line_tmpl = (
    "2026-10-05 @HM@ R1413: declared-idle \u4e00\u884c\u58f0\u660e\u6536\u8f6e\uff08\u7a7a\u8f6e\u5224\u5b9a\u8def\u5f84\u2463\u00b7\u4e94\u9759 fresh \u5b9e\u8bc1 r1413_check.txt 22:43+\u4e09\u63a2\u9488\u7167\u8dd1\u4e0d\u7701 r1413_probes.txt \u57fa\u7ebf\u5e73+\u56db\u67e5\u5c3d\u627f R1412 derive \u7981\u91cd\u626b\u00b7\u58f0\u660e\u8f6e\u5e76\u7a97 2/6=R1412 \u540c\u7a97\u7eed\u9759\u96f6\u6f02\u79fb\u00b7\u5f00\u7a97 commit \u9501\u7a97\u672b\u6536 os-protocol \u00a76\uff09\u2014\u2014"
    "\u2460\u4e94\u67e5 fresh \u9759\uff1aorders \u9876=O-20260928-1910 \u672a\u53d8 mtime 09-28 19:12/decisions dnum \u5185\u5bb9\u5bfb\u5740\u5dee\u96c6 NEW=[]\u3010GONE=[D-20260930-1]=watermark \u5e7b\u5f71\u6761\u76ee\u00b7\u5386\u53f2\u5355\u6570\u5b57 regex \u8bef\u6355\u4ea7\u7269\u00b7\u771f\u503c 148 \u5168\u8986\u76d6\u96f6\u65b0\u884c\u00b7\u672c\u8f6e\u6e05\u9664\u5bf9\u9f50 148==148\u3011\u00b7mtime 10-05 12:04:20 \u96f6\u6f02\u79fb\u3010D-20260930-19 \u6c34\u4f4d\u5dee\u96c6\u5236\u3011/ledger strict @tag 43==43 \u951a\u9759 mtime 10-05 15:13:46 \u96f6\u65b0\u884c/\u6d3e\u5de5\u677f\u968f decisions \u6574\u4ef6 mtime \u672a\u52a8=R1356 \u6d88\u8d39\u6001\u627f\u7ee7\u96f6 BS \u65b0\u884c/\u96f6 index.lock/production=open/\u6811\u6001=M state.json+\u63a2\u9488\u4ef6=\u58f0\u660e\u7a97\u81ea\u8bb0\u8d26\u9884\u671f\u6001\u96f6 bm-a \u8ff9\u8c61\u00b7LAST_COMMIT=4d38d073 R1411\u3010\u5176\u540e\u96f6\u63d2\u961f\u3011/backlog mtime 21:40:18+queue mtime 22:02:52 \u672a\u52a8=R1412 \u5168 lane \u95e8\u63a7 derive \u627f\u7ee7\uff08\u7981\u91cd\u626b\u5f8b\uff09\uff1b"
    "\u2461\u4e09\u63a2\u9488=r1413_probes.txt\uff1aboard 0 FAIL\u30105 ideas/10 drafts/5 in production\u3011/readiness 3 \u963b\u585e\u7686\u5916\u90e8 CEO \u9762\u3010\u8d26\u53f7\u6279\u6b21\u2460+M4 GATE 6/10+#17 needs-CEO\u30110 \u53d1\u73b0\u3010\u963b\u585e\u2260\u5931\u8d25\u53e3\u5f84\u3011/loop_health 3 FAIL+141 WARN==R1412 \u57fa\u7ebf\u6301\u5e73\u96f6\u65b0\u589e\u3010\u4e24 outage 09-26/09-28 \u6848\u53f2\u8db3\u8ff9+account-lag done beats1418>tick1412=+6 \u5728\u8f6e beat \u77ac\u6001\u6b8b\u5dee R981/R1054 \u5b9a\u8c2d\u65cf\u00b7tick1413 \u6536\u8d26\u81ea\u5e73\u3011\uff1b"
    "\u2462\u56db\u67e5\u5c3d=\u4fdd\u62a4\u6001\u8c41\u514d\u9762\u5728\u6848\uff08\u5168 lane \u65f6\u95f4\u95f8/\u4f9b\u7ed9\u95f8/CEO \u95f8\u00b7\u7ed3\u6784\u6027\u6ee1\u8f7d\u2260\u95f2\u7f6e P-2026-09-28-02 \u2463\u00b7\u672c\u7a97\u63d0\u6848\u5df2\u4ea4 W41 P-2/P-3 \u4e49\u52a1\u6ee1\uff09\u2192 waiting: 10-06 day-boundary batch\uff0810-06 \u65e5\u62a5\u8865\u4ea7\u2192E31 REACT-v9 \u62e9\u4f18 F-156 \u9884\u6307\u4f4d\uff09ETA 2026-10-06 00:0x\u00b7export 24h \u95f8=22:19:42 R1411 \u521a\u5237\u5b9e\u51b5\u96f6\u53d8\u5316\u4e0d\u5237\u3010\u4ea7\u54c1\u4f18\u5148\u5f8b\u2461\u00b7\u65e5\u754c\u8f6e\u81ea\u7136\u518d\u5237\u3011\u00b7HQ-FEEDBACK \u4e0d\u5199\u3010\u65e0\u96c6\u56e2\u5c42\u65b0 open \u9879\u96f6\u81a8\u80c0\u3011\u00b7tokens:local=0\u3010\u4e09\u63a2\u9488\u7eaf\u811a\u672c\u96f6\u672c\u5730\u6a21\u578b\u8c03\u7528 P-54\u2464\u3011"
)
line = line_tmpl.replace("@HM@", hm)

# watermark phantom cleanup: D-20260930-1 is a historical single-digit regex artifact
wm = st.get("decisions_watermark", {})
dnums = wm.get("dnums", [])
before = len(dnums)
if "D-20260930-1" in dnums:
    dnums.remove("D-20260930-1")
wm["dnums"] = dnums
wm["ts"] = now_s
st["decisions_watermark"] = wm

st["tick"] = st.get("tick", 0) + 1
st["log"].append(line)
st["ts"] = now_s
prefix = "2026-10-05 %s R1413: " % hm
body = line[len(prefix):]
st["task"] = body[:60]
io.open(sp, "w", encoding="utf-8").write(json.dumps(st, ensure_ascii=False, indent=2))
print("state tick=%s ts=%s log_len=%d wm=%d->%d" % (st["tick"], st["ts"], len(st["log"]), before, len(dnums)))
