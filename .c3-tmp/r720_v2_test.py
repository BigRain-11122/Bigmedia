# -*- coding: utf-8 -*-
# R720: verbatim-preserving V2 split (leading separators) wrap validation @57
import sys, io
sys.path.insert(0, r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\render")
from render_card_video import wrap_for_width

out = io.open(r".c3-tmp\r720_v2_test.txt", "w", encoding="utf-8")

# verbatim text (all original chars in order, \n inserted at the two dot breaks,
# separators ride at line starts)
orig = u"守门人、巡夜员、灯塔守望都收到过 · 谁也没找到全部 · 他们管这叫「梓涵的深夜惊喜」"
v2 = u"守门人、巡夜员、灯塔守望都收到过\n · 谁也没找到全部\n · 他们管这叫「梓涵的深夜惊喜」"

# verbatim check: strip newlines -> must equal original
assert v2.replace(u"\n", u"") == orig, "NOT VERBATIM"
out.write("verbatim check: PASS (%d chars preserved)\n" % len(orig))

for s in (57, 56):
    res = wrap_for_width(v2, s, 1080)
    lines = res.split(u"\n")
    out.write("V2 @ size=%d -> %d lines\n" % (s, len(lines)))
    for i, l in enumerate(lines, 1):
        # em cost like the renderer
        def em(ch):
            o = ord(ch)
            if o >= 0x2E80: return 1.0
            if ch in (" ", "\t"): return 0.5
            return 0.55
        cost = sum(em(c) for c in l)
        px = cost * s
        out.write(u"  L%d [%s] em=%.2f px=%.0f (budget em=%.2f px=%d)\n"
                  % (i, l, cost, px, 920.0/s, 920))
    # block geometry: title 1 line + N subtitle lines, legacy drawtext centered
    n = len(lines) + 1  # + title line
    for fs in (57, 60):
        pass
    h = 4 * (57 * 1.2) + 3 * 14  # 4-line block at 57
    top = (1920 - h) / 2.0
    out.write("  block: 4 lines @57px -> text_h=%.0f top_y=%.0f (band bottom 767, clear=%.0fpx)\n"
              % (h, top, top - 767))
out.close()
print("V2DONE")
