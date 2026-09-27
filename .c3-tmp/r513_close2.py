# -*- coding: utf-8 -*-
"""R513 close amendment (same round, pre-commit, own uncommitted line):
rebuild the R513 log line with the completed 4-trim air budget, refresh
ts/task, point focus at the R514 render leg, refresh status-export rows."""
import io, json, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
now = datetime.datetime.now()
ts = now.strftime("%Y-%m-%d %H:%M:%S")

sp = ROOT + r"\src\os\state.json"
st = json.load(io.open(sp, "r", encoding="utf-8"))
# rebuild own uncommitted R513 log line
out = []
for ln in st["log"]:
    if ln.startswith("2026-09-27 13:") and "R513:" in ln:
        ln = ln.replace(
            "\u7a7a\u6c14\u9884\u7b97=TTS light \u5b9e\u6d4b v2=65.36s \u8d85\u7a97 5.36s"
            "\uff08YunyangNeural+cyber light+human 42\u00b712 cues\u00b7.bs006-tmp/audio.mp3\uff09"
            "\u2192v3 \u673a\u68b0\u88c1 ~22 \u5b57\u88c1\u53e3\u8ba1\u5212\u843d README"
            "\uff08\u8bed\u901f ~3.3 \u5b57/s\u00b7fleet \u5e26 1.2-2.8s \u4f59\u91cf\u76ee\u6807 57.2-58.8s\u00b7"
            "\u5361\u7247\u951a\u70b9\u5217\u4e0e\u6bcd\u7a3f verbatim \u4fdd\u62a4\u884c\u96f6\u52a8\uff09=R514 \u6267\u884c\uff1b",
            "\u7a7a\u6c14\u9884\u7b97=\u56db\u9053\u673a\u68b0\u88c1\u94fe\u6bd5\uff1aTTS light \u5b9e\u6d4b v2=65.36s "
            "\u8d85\u7a97\u2192v3 \u7f16\u53f7\u5f52\u5361[\u89c4\u77e9\u4e00~\u56db\u5361\u951a\u5217\u627f\u8f7d\u00b7"
            "L7 \u5361\u53e3\u5206\u5de5]+\u586b\u5145\u8bcd\u88c1 24 \u5b57=61.40s\u2192v4 \u5168\u7eff\u624d\u53d1\u5f52 close"
            "[b11 \u95e8\u4e0d\u8fc7\u5b57\u4e0d\u51fa\u540c\u4e49\u627f\u63a5]+\u6240\u6709/\u4efb\u4f55/\u80fd/\u4e0a\u88c1=59.07s"
            "[0.93s \u4f59\u91cf\u8584\u4e8e fleet \u5e26\u4e0b\u7f18 1.19s\u00b7R185 \u9632\u7ffb\u7a97\u6559\u8bad\u7eed\u88c1]"
            "\u2192v5 hook \u516c\u5e03\u5168\u90e8\u771f\u5b9e\u6570\u636e\u5f52\u5361\u7535\u62a5\u5f0f 0 \u5217\u8868="
            "**57.32s \u5b9a\u7a3f\u5165\u7a97 2.66s \u4f59\u91cf**\uff08fleet \u5e26 1.2-2.8s \u5185\u00b7"
            "ffprobe 57.343 \u5b9e\u8bc1\u00b7M1 \u9010\u7248\u590d\u68c0 0 FAIL 0 WARN\u00b7\u5361\u7247\u951a\u70b9\u5217"
            "\u4e0e\u6bcd\u7a3f verbatim \u4fdd\u62a4\u884c\u5168\u7a0b\u96f6\u52a8\uff09+TTS light \u5b9a\u7a3f\u97f3\u8f68 "
            ".bs006-tmp\uff08--order BS-006-v5\u00b7BGM-A \u7eaf\u51c0\uff09\uff1b")
        ln = ln.replace(
            "\u4e0b\u8f6e=R514 BS-006 \u7a7a\u6c14\u9884\u7b97 v3 \u673a\u68b0\u88c1+TTS light \u5b9a\u7a3f\u97f3\u8f68"
            "\u2192\u6e32\u67d3\u94fe\uff08\u5bf9\u4f4d\u8868\u7d20\u6750\u63a2\u9488\u5148\u884c\u2192R-E shipinhao"
            "\u3014--series-id=BS-006 EP.06+\u00a74.5\u3015\u2192S2 \u4e09\u95e8\u2192E8\u3014E4 \u968f\u884c\u3015"
            "\u2192M4\u2192F-049 \u767b\u8bb0\u2192D18 \u843d\u4f4d\uff09",
            "\u4e0b\u8f6e=R514 BS-006 \u6e32\u67d3\u94fe\uff08\u5bf9\u4f4d\u8868 cards-v1-matched \u7d20\u6750\u63a2\u9488"
            "\u5148\u884c\u2192R-E shipinhao\u3014--series-id=BS-006 EP.06+\u00a74.5 \u4e09\u5f00\u5173\u3015\u2192S2 \u4e09\u95e8"
            "\u2192\u5e27\u9a8c\u4e09\u5f8b\u2192E8\u3014E4 \u968f\u884c\u3015\u2192M4\u2192F-049 \u767b\u8bb0"
            "\u2192D18 \u843d\u4f4d\uff09")
    out.append(ln)
st["log"] = out
st["focus"] = ("R514: #79 \u4ef6 2 BS-006 \u6e32\u67d3\u94fe\uff08\u5bf9\u4f4d\u8868 cards-v1-matched \u7d20\u6750\u63a2\u9488\u5148\u884c\u3014"
  "\u7d20\u6750\u6c60=\u4e94\u6e90+\u81ea\u4ea7\u5b57\u5361\u7f51\u683c\u00b7\u9898\u6750\u5bf9\u4f4d=\u53d1\u5e03\u95e8/\u53f0\u8d26/\u5ba1\u8ba1\u9762\u2014\u2014"
  "looplog \u547d\u4ee4\u53f0\u8d26\u00b7reviewsdoc \u8bc4\u5ba1\u53f0\u8d26\u00b7citywatch \u503c\u5b88\u5c4f\u4e3b\u5019\u00b7cards-only \u9010\u62cd\u6ce8\u7406\u7531"
  "\u3015\u2192R-E shipinhao \u6e32\u67d3\u3014--series-badge/--series-id=BS-006 EP.06+\u00a74.5 \u4e09\u5f00\u5173\u00b7S5.5 \u89d2\u6807\u5e38\u9a7b\u4f4d\u3015"
  "\u2192S2 \u4e09\u95e8\u2192\u5e27\u9a8c\u4e09\u5f8b\u2192ASR \u7ec8\u8f68\u2192E8 \u7ec8\u5ba1\u3014E4 \u968f\u884c\u3015\u2192M4\u2192F-049 \u767b\u8bb0\u2192**D18 \u843d\u4f4d**"
  "\u00b7\u6392\u671f\u8868\u4e94\u5904\u540c\u6b65\uff09\uff1b\u7a97\u53e3\u4ef6\u968f\u67e5\uff08#59 REACT 09-28 \u5c4a\u65e5\u9886\u00b7daily_brief 09-28 "
  "\u7f3a\u5219\u5148\u8865\u4ea7\u00b7W40 \u5468\u81ea\u5ba1 09-28 \u5f00\u5468+\u6708\u5ea6\u7edf\u8ba1\u6ce8\u8bb0\u9996\u4ef6 \u226409-30\u00b7"
  "#70 OH \u4e0b\u7a97 09-29 21:40 \u540e\u5f00\u00b7#80 global-benchmarks 10-01 \u5e76\u7a97\u00b7#63 C-00030/31 \u951a supply-gated "
  "\u7167\u5b88\u00b7C-20260927-01 \u59d4\u5458\u4f1a\u610f\u89c1\u7a97 \u226409-29 12:00 \u8bb0\u7968\u5f52 HQ \u51b3\u7b56\u8f6e\u00b7"
  "#78 SC-003 \u6e32\u67d3\u817f=FluxVerse \u5b9e\u5f55\u5230\u4f4d\u6838\u9a8c\uff09\uff1b\u951a=orders 35\uff08O-1050 mtime 12:36:52="
  "R511 \u6536\u884c\u8db3\u8ff9\uff09/decisions 56/ledger 31")
st["ts"] = ts
st["task"] = ("R513: \u751f\u4ea7\u8f6e\u00b7#79 \u4ef6 2 \u7a3f\u96c6 BS-006 \u8d77\u94fe\u4e09\u817f\u6bd5+\u7a7a\u6c14\u9884\u7b97\u56db\u9053\u6bd5"
  "\uff08\u62cd\u7a3f v1-v5 \u88c1\u94fe 65.36\u219257.32s \u5b9a\u7a3f")
json.dump(st, io.open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

xp = ROOT + r"\docs\status-export.json"
ex = json.load(io.open(xp, "r", encoding="utf-8"))
ex["export_ts"] = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
for row in ex.get("outs", []):
    if row and row[0] == "OS \u5faa\u73af":
        row[-1] = ("tick 513\uff1aR513 \u4ef6 2 \u8d77\u94fe\u4e09\u817f\u6bd5+\u7a7a\u6c14\u9884\u7b97\u56db\u9053\u6bd5\u3002"
          "\uff08BS-006\u300a\u56db\u6761\u89c4\u77e9\u300b\u7a3f\u96c6\u9996\u4ef6=\u516c\u4f17\u53f7\u6bcd\u7a3f\u672a\u7528\u5207\u9762"
          "\u3014\u00a7\u4e3a\u4ec0\u4e48\u53ef\u4fe1+\u00a7\u5982\u5b9e\u4ea4\u5e95\u3015\u00b7M0 \u56db\u7ef4\u5206 7/8+\u62cd\u7a3f v1-v5 "
          "\u88c1\u94fe\uff08v2 \u53e5\u62c6 M1 0F/0W+v3 \u7f16\u53f7\u5f52\u5361+v4 \u5f52\u5e42+v5 \u5f52\u5361\u7535\u62a5\u5f0f\u005d"
          "\uff09+TTS light 65.36\u219261.40\u219259.07\u219257.32s \u5b9a\u7a3f\u5165\u7a97 2.66s \u4f59\u91cf+S1 "
          "v1.5+L18-L20 \u95e8 10/10 PASS \u96f6\u8fdd\u5f8b\u4e00\u6b21\u8fc7\uff0813:06:53\uff09\uff1b\u63a2\u9488 board 0 FAIL"
          "/readiness 3 \u5916\u90e8\u963b\u585e 0 \u53d1\u73b0/loop_health 2F+21W \u5728\u6848\u5b9a\u578b\u96f6\u65b0\u589e\uff09")
for d in ex.get("depts", []):
    if d.get("n") == "\u5de5\u7a0b\u6280\u672f\u90e8":
        d["s"] = ("R513: #79 piece-2 BS-006 kickoff done - draft-collection piece-1 from mp-article "
          "unused cut (M0 7/8 + M1 0F/0W + S1 gate 10/10 PASS one-pass + air-budget 4 mechanical "
          "trims 65.36->61.40->59.07->57.32s final in-window 2.66s headroom + TTS light final track "
          "staged in .bs006-tmp). Next R514: render leg (cards-matched probe-first -> R-E shipinhao "
          "-> S2 gates -> E8 + M4 -> F-049 register -> D18 slot)")
json.dump(ex, io.open(xp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("OK amended ts=%s" % ts)
