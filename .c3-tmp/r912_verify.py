# -*- coding: utf-8 -*-
# r912_verify v2: fix section-check spacing + phrase->entry pair mapping
import io, json, re, os

BS = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP = r"C:\Users\sjs20\Desktop\FluxGroup"
ok = True
fails = []

entries = []
for ln in io.open(os.path.join(GRP, "life", "BigLife", "cognition", "interchat-ledger.jsonl"), "r", encoding="utf-8"):
    ln = ln.strip()
    if ln:
        entries.append(json.loads(ln))

hu = io.open(os.path.join(BS, "data", "storylines", "codex", "city-humanities.md"), "r", encoding="utf-8").read()
nums = [int(r) for r in re.findall(r"^\|\s*(\d+)\s*\|", hu, re.M)]
OUT = []
if max(nums) != 97:
    ok = False
    fails.append("max num %d != 97" % max(nums))
if len(set(nums)) != len(nums):
    ok = False
    fails.append("duplicate entry numbers")
OUT.append("rows=%d max=%d" % (len(nums), max(nums)))

sec_market = hu.split(u"## 风物")[0]
CHECK = [
    (92, [1], [u"夜里的 bug 果然爱出来透气", u"复现归因这活儿交关要紧", u"红灯面前没有老熟人"]),
    (93, [2, 3], [u"广场舞队又加了个新动作", u"我也想学学8bit乐曲配上舞步"]),
    (94, [4, 5], [u"听说你上次登塔检修遇到大风了", u"是挺大的，差点没稳住"]),
    (95, [6, 7], [u"大风卷起落叶满街跑", u"这风不小，你赶紧回家收衣服吧"]),
    (96, [16, 17], [u"晚归人的胃归咱管，慢慢来，比较快", u"给熬夜赶工的端一碗去", u"门禁亮绿灯，心里才亮堂"]),
    (97, [14, 15], [u"搬新家的资料我帮你整理好了", u"刚好我也在整理夜宵的菜单"]),
]
for num, idxs, phrases in CHECK:
    m = re.search(r"^\|\s*%d\s*\|(.*)$" % num, hu, re.M)
    if not m:
        ok = False
        fails.append("row %d missing" % num)
        continue
    rowtext = m.group(1)
    if ("| %d " % num) not in sec_market:
        ok = False
        fails.append("row %d not in market-trade section" % num)
    if "interchat" not in rowtext:
        ok = False
        fails.append("row %d missing interchat citation" % num)
    for ph in phrases:
        if not any(ph in entries[i]["text"] for i in idxs):
            ok = False
            fails.append("row %d phrase not in ledger %s: %s" % (num, idxs, ph[:30]))
        if ph not in rowtext:
            ok = False
            fails.append("row %d phrase not in entry row: %s" % (num, ph[:30]))

for banned in [u"O-20260923-2245-bm-a", u"U153-D05", u"C408", u"显存紧张", u"token 扛不住"]:
    if banned in hu:
        ok = False
        fails.append("banned literal present: %s" % banned)

if u"**计数**：97 条" not in hu:
    ok = False
    fails.append("count line not 97")
if u"v1.6" not in hu.splitlines()[0]:
    ok = False
    fails.append("title not v1.6")

rep = io.open(os.path.join(BS, ".c3-tmp", "r912_verify.txt"), "w", encoding="utf-8")
rep.write((u"r912 c-leg6 verify: %s\n" % ("PASS" if ok else "FAIL")) + u"\n".join(fails) + u"\nrows=%d\n" % len(nums))
rep.close()
print("VERIFY %s fails=%d rows=%d" % ("PASS" if ok else "FAIL", len(fails), len(nums)))
for f in fails:
    print("FAIL:", f.encode("unicode_escape").decode()[:130])
