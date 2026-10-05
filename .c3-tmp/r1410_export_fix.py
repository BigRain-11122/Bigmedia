# -*- coding: utf-8 -*-
# R1410 export-only fix (state.json already closed by r1410_close.py; this redoes the export leg
# whose results-append line hit a % format clash with '% hm')
import json, io, datetime

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
now = datetime.datetime.now()
now_s = now.strftime("%Y-%m-%d %H:%M:%S")
hm = "%d:%dx" % (now.hour, now.minute // 10)

ep = repo + r"\docs\status-export.json"
ex = json.load(io.open(ep, encoding="utf-8"))
ex["export_ts"] = now_s
ex["outs"][0][1] = (
    "tick 1410\uff0cR1410 \u751f\u4ea7\u8f6e=queue \u00a7D P-3 A/B \u8bd5\u70b9\u91cf\u6d4b\u5224\u636e\u4e09\u95ee\u5168\u8fc7\u6536\u53e3\uff08\u7a7a\u8f6c\u89c4\u5219\u2462\u8def=\u6e05\u5355\u9876\u9879 open \u6267\u884c\uff09\u2014\u2014\u8f7d\u4f53=BS-003/BS-004 \u5728\u6848 ASR \u7ec8\u8f68\u53cc\u4ef6\uff08A=R169 recipe \u590d\u8dd1\u4e0e\u5f52\u6863 asr-check.srt \u9010\u5b57\u4e00\u81f4=\u786e\u5b9a\u6027 1.0000\uff09\uff1a\u4e22\u540d\u9000\u5316\u4f4d\u70b9 13\u21925 \u964d 62%\uff08\u5224\u636e\u2460 \u226550% \u8fc7\uff09\u00b7prompt \u6cc4\u6f0f 0\uff08\u5224\u636e\u2461 \u8fc7\uff09\u00b7\u5168\u5b57\u4f4d\u566a\u58f0\u7387 0.1275\u21920.1176/0.3112\u21920.0918 \u53cc\u964d\uff08\u5224\u636e\u2462 \u8fc7\uff09\u2192**adopt=S2 QC recipe \u589e --initial-prompt \u4e22\u540d\u9762 leg**\u00b7\u6b63\u5178\u4f4d\u4e09\u4ef6\u540c\u6b65\uff08whisper_to_srt.py docstring+help/m2-local-stack v1.6/capabilities C-17\uff09+queue P-3 done\u00b722 align \u6d4b\u8bd5\u7eff\u3002\u4e0b\u8f6e=10-06 \u65e5\u754c\u6279\uff0810-06 \u65e5\u62a5\u8865\u4ea7\u2192REACT-v9 \u62e9\u4f18\uff09+10-07 #57 \u7ec8\u62a5+10-08 GB \u95f8\u3002\u771f\u53d1\u5e03=blocked-on-CEO \u8d26\u53f7\u7269\u7406\u4ef6\u00b7\u53d1\u5e03\u9501=M5 \u4e0d\u53d8"
)
ex["results"].append([
    "1410",
    "2026-10-05 " + hm + " R1410: \u751f\u4ea7\u8f6e\u00b7queue \u00a7D P-3 A/B \u8bd5\u70b9\u91cf\u6d4b\u5224\u636e\u4e09\u95ee\u5168\u8fc7\u6536\u53e3\uff08BS-003/BS-004 \u53cc\u8f68 13\u21925 \u964d 62%\u00b7\u6cc4\u6f0f 0\u00b7\u566a\u58f0\u7387\u53cc\u964d\u00b7QC recipe \u589e --initial-prompt \u4e22\u540d\u9762 leg \u843d\u6b63\u5178\u4f4d\u4e09\u4ef6+22 \u6d4b\u8bd5\u7eff\uff09\u2014\u2014\u8be6\u89c1 state.json log R1410 \u884c",
])
ex["live"] = [
    "\u5f53\u524d\u6d3b\uff1aR1410 P-3 \u8bd5\u70b9\u6536\u53e3\u5b8c\u6bd5\uff08\u5224\u636e\u4e09\u95ee\u5168\u8fc7\u2192S2 QC recipe \u589e --initial-prompt \u4e22\u540d\u9762 leg\u00b7\u4e0b 1-2 \u4ef6\u5728\u9014 ASR \u7ec8\u8f68\u968f\u4ef6\u514d\u8d39\u590d\u68c0\uff09\uff1b\u4e0b\u4e00\u6ce2\u5168\u5728 10-06 \u65e5\u754c\u6279",
    "\u6700\u8fd1\u5b9e\u7269\uff1aP-3 A/B \u5224\u636e\u91cf\u6d4b\u8bc1\u636e\u4ef6\u4e0e recipe leg \u5347\u7ea7\uff08.c3-tmp/r1410_p3_ab.txt+whisper_to_srt.py QC recipe \u6b63\u5178\u884c\u00b72026-10-05 22:2x\uff09\uff1b\u4e0a\u4e00\u4ef6\u6210\u54c1=DAILY v68 \u57ce\u5e02\u65e5\u7b7e F-155\uff0810-05 18:00:51\uff09",
    "\u4e0b\u4e2a\u91cc\u7a0b\u7891\uff1a10-06 \u65e5\u754c\u6279=10-06 \u65e5\u62a5\u8865\u4ea7\u2192REACT-v9 \u7a97\u62e9\u4f18\uff08F-156 \u9884\u6307\uff09\u219210-07 #57 \u66ff\u4ee3\u7387\u9996\u62a5\u7ec8\u62a5\u2014\u2014\u7a97 \u226448h",
]
io.open(ep, "w", encoding="utf-8").write(json.dumps(ex, ensure_ascii=False, indent=2))
print("export ok ts=%s" % now_s)
