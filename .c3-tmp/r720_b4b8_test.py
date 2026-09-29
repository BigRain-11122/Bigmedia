# -*- coding: utf-8 -*-
# R720: b4/b8 fix variants wrap validation (verbatim, minimal size, trailing style)
import sys, io
sys.path.insert(0, r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\render")
from render_card_video import wrap_for_width

out = io.open(r".c3-tmp\r720_b4b8_test.txt", "w", encoding="utf-8")

# b4 verbatim: trailing-dot 3-split (binding line = seg3, 17.0 em pure CJK)
b4_orig = u"第一个署名关卡上线那晚 · 蹲在城门口听了一夜玩家的议论 · 第二天把最狠的差评打印出来贴在工位"
b4_fix = u"第一个署名关卡上线那晚 · \n蹲在城门口听了一夜玩家的议论 · \n第二天把最狠的差评打印出来贴在工位"
assert b4_fix.replace(u"\n", u"") == b4_orig
out.write("b4 verbatim: PASS\n")
for s in (54, 53):
    lines = wrap_for_width(b4_fix, s, 1080).split(u"\n")
    out.write("b4 trailing @%d -> %d lines\n" % (s, len(lines)))
    for l in lines:
        out.write(u"   [%s]\n" % l)

# b8 verbatim: trailing-dot 3-split at native 60px (no size override)
b8_orig = u"她说：好关卡像好弄堂 · 走一遍就舍不得搬走 · 新手道永远比规程多留半步余量"
b8_fix = u"她说：好关卡像好弄堂 · \n走一遍就舍不得搬走 · \n新手道永远比规程多留半步余量"
assert b8_fix.replace(u"\n", u"") == b8_orig
out.write("b8 verbatim: PASS\n")
lines = wrap_for_width(b8_fix, 60, 1080).split(u"\n")
out.write("b8 trailing @60 -> %d lines\n" % len(lines))
for l in lines:
    out.write(u"   [%s]\n" % l)

# block tops: title+3 lines
for tag, s in [("b4@54", 54), ("b8@60", 60)]:
    pitch = s * 1.2 + 14
    top = (1920 - 4 * pitch) / 2.0
    out.write("%s block: 4 lines, top=%.0f (clear of band 767: %.0fpx)\n" % (tag, top, top - 767))
out.close()
print("B4B8DONE")
