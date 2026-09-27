# -*- coding: utf-8 -*-
# R618 addendum: record verify-generation third-offense op-red (R585/R615 precedent) + harden
# the r619_verify generation law in focus (enumerated number-expectation checklist).
import io, json, os, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = os.path.join(ROOT, "src", "os", "state.json")

now_hm = time.strftime("%H:%M")
state = json.load(io.open(SP, encoding="utf-8"))
assert state["tick"] == 618, "expected tick 618, got %s" % state["tick"]

LQ = u"\u3014"  # 〔
RQ = u"\u3015"  # 〕
old_clause = u"r619_verify \u751f\u6210\u5f8b=\u6587\u4ef6\u540d\u66ff\u6362+\u6570\u5b57\u9884\u671f\u540c\u6b65\u6539" + LQ + u"R615 \u8865\u8bb0\u5f8b" + RQ
new_clause = (
    u"r619_verify \u751f\u6210\u5f8b=\u6570\u5b57\u9884\u671f\u6e05\u5355\u5236\u4e03\u9879\u679a\u4e3e\u66ff\u6362" + LQ +
    u"R618 \u4e09\u72af\u5b9e\u8bc1\u5f3a\u5316\uff1a\u2460tick==619\u2461task \u8f6e\u53f7 R619:\u2462log tail \u8f6e\u53f7 R619: +\u7a97\u8ba1\u6570 \u65b0\u7a97 5/6\u2463focus \u6b21\u8f6e\u53f7 R620: +baseline r619_lednew5\u2464OS row tick 619+R619+5/6\u2465LOG_COUNT \u2265643\u2466\u5934\u884c VERIFY_R619\u2014\u2014\u5927\u5199 R \u4e0e\u88f8\u6570\u5b57\u9010\u9879\u624b\u6539\u00b7\u5c0f\u5199 rN \u5168\u5c40\u66ff\u6362\u4e0d\u89e6\u6b64\u9762" + RQ
)
assert old_clause in state["focus"], "focus clause not found"
state["focus"] = state["focus"].replace(old_clause, new_clause)

state["log"].append(
    u"2026-09-28 " + now_hm + u" R618 \u8f6e\u672b\u8865\u8bb0\uff08\u64cd\u4f5c\u7ea2\u5982\u5b9e\u5165\u8d26\u00b7R585/R615 \u5728\u6848\u540c\u578b\u7b2c\u4e09\u72af\uff09\uff1ar618_gen \u751f\u6210 r618_verify "
    u"\u6570\u5b57\u9884\u671f\u4ec5\u540c\u6b65\u56db\u9879\uff08\u7a97\u8ba1\u6570/LOG_COUNT/FOCUS_WINDOW/OS row 4/6\uff09\u6f0f\u4f59\u9879\uff08TICK==617/task R617:/log tail R617:/focus \u6b21\u8f6e\u53f7 R618:/OS row tick 617 R617/\u5934\u884c VERIFY_R617\uff09\u2192\u9996\u8dd1 6 \u4f2a FAIL=\u68c0\u67e5\u9762\u54ac\u4f4f\u00b7\u6570\u636e\u9762\u96f6\u635f\u4f24\uff08close \u4ef6 json.dump \u76f4\u5199 UTF-8 \u6b63\u786e\u00b7tick618/log 642/ts \u4e94\u9762\u5b9e\u8bfb\u590d\u6838\u5373\u8bc1\uff09\u2192r618_verify \u4ef6\u5185\u9010\u9879\u679a\u4e3e\u6539\u540e\u590d\u8dd1 12/12 ALL_PASS\uff08\u8bc1\u636e\u4ef6 r618_verify.txt\uff09\u2014\u2014verify \u751f\u6210\u5f8b\u5347\u7ea7=\u6570\u5b57\u9884\u671f\u6e05\u5355\u5236" + LQ +
    u"R615 \u8865\u8bb0\u5f8b\u539f\u6587\u4e0d\u8db3\u4ee5\u9632\uff1a\u6e05\u5355\u4e03\u9879\u9010\u8f6e\u679a\u4e3e\u66ff\u6362\u2014\u2014\u5927\u5199 R \u4e0e\u88f8\u6570\u5b57\u5fc5\u987b\u9010\u9879\u624b\u6539\u00b7\u5c0f\u5199 rN \u5168\u5c40\u66ff\u6362\u4e0d\u89e6\u5927\u5199\u4e0e\u6570\u5b57\u9762\u00b7R619 focus \u5df2\u5e26\u6b64\u5f8b" + RQ +
    u"\uff1b\u968f\u884c\u4fee\u7ea2\u4e8c=\u672c\u4ef6\u9996\u7248 \uff3b \u62ec\u53f7\u7f16\u7801\u8bef\u7528 \uff3d U+FF3B \u5168\u89d2\u65b9\u62ec\u53f7 \u2260 \u9f9f\u7532\u62ec\u53f7 U+3014\u3015\uff08assert \u54ac\u4f4f\u96f6\u526f\u4f5c\u7528\u5373\u4fee\uff09"
)
json.dump(state, io.open(SP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ADDENDUM OK: log_count=%d focus_law=hardened" % len(state["log"]))
