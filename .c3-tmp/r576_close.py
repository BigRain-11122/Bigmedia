# r576 collection: state.json + status-export.json update (python io UTF-8 direct write)
import io, json, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
now = datetime.datetime.now()
ts = now.strftime("%Y-%m-%d %H:%M:%S")
ts_iso = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
logts = now.strftime("%Y-%m-%d %H:%M")

L1 = u"%s R576 \u8f6c\u529e\u6536\u8bab\uff08\u96c6\u56e2 ledger \u626b\u63cf\u884c\u7ea7 diff \u5b9a\u8c23\u00b7\u5b9e\u6d3b\u8f6e\u8f6c\u5168\u4efb\u52a1\u4e66\uff09\u2014\u2014\u4e94\u6a21\u5f0f 31\u219230 \u5dee\u989d\u5b9a\u8c23=r576_rowdiff \u884c\u7ea7 diff\uff08r533 \u57fa\u7ebf 30 P \u884c+1 \u503c\u5b88\u884c\u2192\u73b0\u76d8 29 P \u884c+1 \u503c\u5b88\u884c\uff09=**P-20260926-01 \u6280\u80fd\u52a8\u5458\u4ee4\u884c\u81ea\u5339\u914d\u9762\u6d88\u5931**\uff0800:10:41 \u96c6\u56e2\u4fa7\u5199\u5165\u7a97\uff09+\u503c\u5b88\u884c\u5348\u73ed\u2192\u591c\u73ed\u8f6e\u6362\uff08\u4f8b\u884c\uff09\u2192**\u96f6\u65b0\u8f6c\u529e**\u00b7\u672c\u53f8\u6536\u6267\u94fe\u5b8c\u6574\uff08R377 \u6536\u8bab\u5165\u677f+R378 \u5efa\u88c5\u4ea4\u4ed8\u6bd5+R444 P-51 \u53cc\u8f7d\u4f53\u6838\u9a8c+F-20260927-01 \u8ba1\u6570\u66f4\u6b63\uff09=\u96f6\u4e49\u52a1\u5f71\u54cd\u2192\u53f0\u8d26\u5b8c\u6574\u6027\u7591\u70b9\u5448\u62a5 F-20260928-02\uff08D-20260927-06 b0f08ff \u540c\u65cf\u00b7\u53f8\u7981\u5199\u4ec5\u5448\u8bc1\u636e\uff09\u00b7\u626b\u63cf\u951a\u540c\u6b65\u7ffb\u6b63 31\u219230"

L2 = u"%s R576 \u51b3\u7b56\u56de\u6267\uff08docs/decisions.md \u626b\u63cf\u00b7\u975e\u7a7a\u884c 56\u219263=7 \u65b0\u884c\u00b7mtime 00:10:41=09-28 00:00 \u51b3\u7b56\u8f6e\u6279\u5199\u5165\uff09\u2014\u2014\u59d4\u5458\u4f1a\u8282\u9996\u7acb\uff08council.md v1.0\u00b7CEO \u4ee4 09-27 ~07:5x\u00b7\u51b3\u7b56\u8f6e=\u5e38\u8bbe\u79d8\u4e66\u5904\u00b7\u5e2d\u4f4d\u610f\u89c1\u7ecf\u5404\u53f8\u53cd\u9988\u9762\u51fa\u5177\u00b7\u98ce\u63a7\u5e2d\u5fc5\u8bae\u00b7\u666e\u901a\u8fc7 \u22654/7\uff09+C-20260927-01/C-02 \u767b\u8bb0\u884c\u79d1\u5b66\u5224\u65ad\u95f8\u5168\u8fc7\u5ba1\u96f6\u9a73\u56de\uff1bC-01 \u5e2d6\uff08BigLife+BigStream\uff09\u672c\u53f8\u4fa7\u610f\u89c1\u5df2\u5728\u7a97\u5185\uff08F-20260927-05\u00b7\u72b6\u6001\u5217\u56db\u5e2d\u5df2\u6536\u00b7\u8bb0\u7968\u968f\u7a97\u6bd5\u540e HQ \u51b3\u7b56\u8f6e\uff09=\u77e5\u6089\u96f6\u65b0\u52a8\u4f5c\uff1b**C-02 \u4f59\u4e94\u5e2d\u542b\u5e2d6=\u672c\u53f8\u4efd\u989d\u5f53\u8f6e\u51fa\u5177**\u2192F-20260928-01\uff08\u7968\u6863=\u8d5e\u6210\u6709\u4fee\u6539\uff1aA1-A5+\u00a7\u56db \u5206\u671f\u8d5e\u6210+\u4e09\u4fee\u6539=\u9000\u5f79\u4ef6\u8f6c\u6307\u9488\u4ef6\u5236\u5f15\u7528\u9762\u96f6\u65ad\u5f8b/L0-L4 \u7f16\u53f7\u53e3\u5f84\u968f\u96c6\u56e2\u5b9a\u8c23\u5373\u6539/\u6cbb\u7406 \u226410 \u9884\u7b97\u6309\u73b0\u884c\u6b63\u5178\u4ef6\u8ba1\u6570\u00b7\u6307\u9488\u4ef6\u4e0d\u8ba1+\u5206\u671f\u5f52\u62e2\u975e\u5373\u5220\u00b7\u7a97 \u226409-29 ~10:0x \u5185\u63d0\u524d\u6bd5\uff09"

L3 = u"%s R576: \u5468\u81ea\u5ba1 W40 \u671f+\u6708\u5ea6\u7edf\u8ba1\u6ce8\u8bb0\u9996\u4ef6\u4ea4\u4ed8\u8f6e\uff08\u5b9e\u6d3b\u8f6e\u00b7W40 \u5f00\u5468\u5c4a\u65e5\u4ef6\uff09\u2014\u2014\u2460\u5468\u81ea\u5ba1=self_audit.py \u6570\u636e\u5305\uff08packs/2026-W40-pack.md\u00b7\u96f6 token\u00b7\u4e09\u63a2\u9488\u968f\u5305\u8dd1\uff09+\u5224\u8bfb\u5c42\u4e94\u9879\u586b\u6bd5 docs/audits/2026-W40-self-audit.md\uff08\u4e09\u7ef4\u5065\u5eb7\u5747\u5408\u7406\u96f6\u6f02\u79fb+W39 \u56db\u6574\u6539\u5168\u590d\u67e5\u95ed\u73af/B5 \u4e24\u8f6e\u94fe\u63d0\u901f\u4e09\u8fde\u8bc1+\u5347\u88c1\u96f6\u6b21/\u6574\u6539\u9762\u6e05\u96f6 #23+#26 \u6bd5/\u672a\u4e0a\u7ebf=\u672a\u6d4b\u91cf E4 \u5e26\u72b6\u7a33\u5b9a\uff09\u2461\u6708\u5ea6\u7edf\u8ba1\u6ce8\u8bb0\u9996\u4ef6=docs/research/R-20260928-bigstream-03-\u6708\u5ea6\u7edf\u8ba1\u6ce8\u8bb0.md\uff08P-20260926-18 \u8c03\u7814\u90e8 \u2462\u7edf\u8ba1\u9762\u677f\u00b7\u9996\u4ef6 \u226409-30 \u968f W40 \u5468\u5ba1\u8f6e\u63d0\u524d\u6bd5\u00b7\u56db\u7ef4=\u4ea7\u51fa\u91cf 50 \u4ef6\u5206\u7ebf\u00b7\u91cc\u7a0b\u7891 09-23~09-28/\u5065\u5eb7\u5ea6\u4e09\u63a2\u9488/\u914d\u989d\u53d1\u5e03\u9501\u00b7\u96c6\u56e2\u6708\u5bf9\u8d26 M5 \u76f4\u8bfb\u6e90\u00b7\u96f6\u65b0\u91c7\u96c6\u56db\u6e90\u53ef\u6eaf\uff09\u2462\u4e09\u63a2\u9488=W40 \u6570\u636e\u5305\u8bfb\u6570\uff08board 0 FAIL/readiness 3 \u963b\u585e\u7686\u5916\u90e8 CEO \u9762 0 \u53d1\u73b0/loop_health 2 FAIL+25 WARN \u5168\u5728\u6848\u5b9a\u8c23\u7c7b\u96f6\u65b0\u589e\uff09\u2463\u4f8b\u884c\u4ef6\uff1a\u65e5\u62a5 09-28 \u5728\u6848\u4e0d\u91cd\u8dd1\uff08R575 \u8865\u4ea7\uff09\u00b7#63 C-00030/31 \u951a\u53cc False supply-gated \u7167\u5b88\u00b7#70 OH \u4e0b\u7a97 09-29 21:40 \u540e\u5f00\uff08\u9996\u7a97\u4e09\u5207\u7247\u9f50\uff09\u00b7#31 ch.5 \u7a3f\u672a\u843d supply-gated\u00b7#67 \u53f2\u6e90\u5019\u9009=\u59d4\u5458\u4f1a\u8282\u9996\u7acb+C-02 \u8865\u767b\u53cc\u951a\uff08DIGEST v8 \u968f\u8f6e\u9886\u00b7\u672c\u8f6e\u9884\u7b97\u8017\u4e8e\u5c4a\u65e5\u4ef6\u56db\u4ef6\uff09\u00b7#57 10-07\u00b7#80 benchmarks 10-01\u00b7T1 \u50ac\u529e\u5df2\u88c1\u9879\u505c\u7528\u00b7tokens:local=0\uff08\u6570\u636e\u5305+\u63a2\u9488\u7eaf\u811a\u672c\u96f6\u672c\u5730\u6a21\u578b\u8c03\u7528\u00b7P-54\u2465 \u8ba1\u91cf\u5f8b\u5982\u5b9e\u8bb0\uff09\u00b7\u53d1\u5e03\u9501=M5 \u8d26\u53f7\u7269\u7406\u4ef6\u4e0d\u53d8\uff08\u672a\u4e0a\u7ebf=\u672a\u6d4b\u91cf\uff09\u2014\u2014\u5b9e\u6d3b\u8f6e\u89e6\u53d1\u6536\u8d26 commit+push\uff08\u663e\u5f0f\u5217\u6587\u4ef6\uff09"

# --- state.json ---
sp = ROOT + r"\src\os\state.json"
with io.open(sp, "r", encoding="utf-8") as f:
    st = json.load(f)
st["tick"] = 576
st["log"].append(L1)
st["log"].append(L2)
st["log"].append(L3)
st["ts"] = ts
st["task"] = (u"R576: \u5468\u81ea\u5ba1 W40 \u671f+\u6708\u5ea6\u7edf\u8ba1\u6ce8\u8bb0\u9996\u4ef6\u4ea4\u4ed8\u8f6e\uff08\u5b9e\u6d3b\u8f6e\u00b7W40 \u5f00\u5468\u5c4a\u65e5\u4ef6\uff09\u2014\u2014")[:60]
st["focus"] = u"R577: \u5feb\u901f\u8def\u5f84\u4e94\u67e5\u9996\u884c\u2014\u2014\u951a=orders 35\u301413:53:11\u3015\u00b7ledger \u4e94\u6a21\u5f0f 30\u3010\u65b0\u951a\u00b7mtime 00:10:41\u00b7P-20260926-01 \u884c\u6d88\u5931\u5df2\u5448 F-20260928-02\u3011\u00b7decisions 63\u3010\u65b0\u951a\u00b7mtime 00:10:41\u00b7\u59d4\u5458\u4f1a\u8282+C-01/C-02 \u5df2\u6536\u8bab\u3011\u2014\u2014\u53ef\u8ba4\u9886\u6d3b\u4f18\u5148\u5e8f=\u2460#67 DIGEST v8 \u5c4a\u53f2\u6e90\u9886\uff0809-28 \u59d4\u5458\u4f1a\u8282\u9996\u7acb+C-20260927-02 \u8865\u767b\u53cc\u951a\u00b7research \u00a75 \u89e6\u53d1\u5f8b\u00b7M0 \u56db\u7ef4\u5206\u8d77\u94fe\u5168\u94fe\u8d70\u95e8\uff09\u2461#63 C-00030/31 \u4f9b\u7ed9\u95e8\u951a\u6838\u2462#70 OH \u4e0b\u7a97 09-29 21:40 \u540e\u5f00\u2463C-01/C-02 \u8bb0\u7968\u968f HQ \u51b3\u7b56\u8f6e\uff08\u672c\u53f8\u610f\u89c1\u5df2\u51fa\u96f6\u52a8\u4f5c\uff09\u2014\u2014\u4e94\u67e5\u9759\u4e14\u65e0\u53ef\u9886=idle-fast \u4e00\u884c\u6536\u8d26\uff08\u65b0\u7a97 R576-R581\u00b7\u8ba1 1/6\u00b7R576 \u5b9e\u6d3b\u8f6e\u5df2\u6536\u8d26 commit\uff09"
with io.open(sp, "w", encoding="utf-8") as f:
    json.dump(st, f, ensure_ascii=False, indent=1)
    f.write(u"\n")

# --- status-export.json ---
xp = ROOT + r"\docs\status-export.json"
with io.open(xp, "r", encoding="utf-8") as f:
    ex = json.load(f)
ex["export_ts"] = ts_iso
dept_t = u"R576: full task-book round (five-checks broken by 7 new decision rows + due-date W40 audit): ledger row-level diff 31->30 pinned to P-20260926-01 row gone from five-mode scan (own receipt chain intact R377/R378/R444, integrity observation F-20260928-02, scan anchor flipped to 30, zero new transfers); committee section + C-01/C-02 registrations all passed review: C-01 seat-6 opinion already in-window (F-20260927-05), C-02 seat-6 opinion issued in-round F-20260928-01 approve-with-modifications (pointer-file retirement law for merged/retired files, L0-L4 numbering follows group canon once settled, governance<=10 budget counts active canon only, staged consolidation not deletion); W40 weekly self-audit delivered (2026-W40-self-audit.md five-item layer: W39 four rectifications all closed, zero drift, B5 two-round-chain speedup 3rd proof, rectification face clear #23+#26 done, not-live=not-measured held); monthly-stats note first piece R-20260928-bigstream-03 delivered (P-20260926-18 research-dept charter, <=09-30 met early, four-dimension group monthly-reconciliation source); probes per W40 pack: board 0 FAIL, readiness rc1 3 external blockers 0 findings, loop 2F+25W all in-case; tokens:local=0; production candidate next rounds #67 DIGEST v8 (council-section + C-02 dual anchor); active-work round -> collection commit+push same round"
for d in ex["depts"]:
    if d["n"] == u"\u5de5\u7a0b\u6280\u672f\u90e8":
        d["t"] = dept_t
    if d["n"] == u"\u9009\u9898\u7814\u7a76\u90e8":
        if u"\u6708\u5ea6\u6ce8\u8bb0\u9996\u4ef6 \u226409-30" in d["t"]:
            d["t"] = d["t"].replace(u"\u6708\u5ea6\u6ce8\u8bb0\u9996\u4ef6 \u226409-30", u"\u6708\u5ea6\u6ce8\u8bb0\u9996\u4ef6\u5df2\u6bd5 09-28\uff3bR-20260928-bigstream-03\uff3d")
r576 = [u"576", u"R576 \u8f6c\u529e/\u51b3\u7b56\u6536\u8bab+\u5468\u81ea\u5ba1 W40+\u6708\u5ea6\u7edf\u8ba1\u6ce8\u8bb0\u9996\u4ef6\uff08\u5b9e\u6d3b\u8f6e\uff09\uff1aledger 31\u219230 \u884c\u7ea7 diff \u5b9a\u8c23=P-20260926-01 \u884c\u6d88\u5931\uff08\u96f6\u65b0\u8f6c\u529e\u00b7\u6536\u6267\u94fe\u5b8c\u6574\u00b7\u5448\u62a5 F-20260928-02\uff09+decisions 7 \u65b0\u884c=\u59d4\u5458\u4f1a\u8282+C-01/C-02\uff08C-02 \u5e2d6 \u610f\u89c1\u5f53\u8f6e\u51fa\u5177 F-20260928-01 \u8d5e\u6210\u6709\u4fee\u6539\uff09+W40 \u5468\u5ba1\u4e94\u9879\u586b\u6bd5\uff08W39 \u56db\u6574\u6539\u5168\u95ed\u73af\u00b7\u96f6\u6f02\u79fb\uff09+\u6708\u5ea6\u6ce8\u8bb0\u9996\u4ef6\u63d0\u524d\u6bd5\uff08\u226409-30 \u7a97\u00b7\u56db\u7ef4\u76f4\u8bfb\u6e90\uff09\u00b7\u4e09\u63a2\u9488\u5728\u6848\u7c7b\u7eff\u00b7\u6536\u8d26 commit+push"]
ex["results"].insert(0, r576)
with io.open(xp, "w", encoding="utf-8") as f:
    json.dump(ex, f, ensure_ascii=False, indent=1)
    f.write(u"\n")

# verify
with io.open(sp, "r", encoding="utf-8") as f:
    st2 = json.load(f)
with io.open(xp, "r", encoding="utf-8") as f:
    ex2 = json.load(f)
print("OK tick=%d loglines=%d ts=%s export_ts=%s results_head=%s" % (st2["tick"], len(st2["log"]), st2["ts"], ex2["export_ts"], ex2["results"][0][0]))
