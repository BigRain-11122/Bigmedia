# -*- coding: utf-8 -*-
# R720: b9 wrap geometry validation before the dot-break pre-split fix
import sys, io, json
sys.path.insert(0, r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\render")
from render_card_video import wrap_for_width

out = io.open(r".c3-tmp\r720_wrap_test.txt", "w", encoding="utf-8")

def show(tag, text, size=60, fw=1080):
    res = wrap_for_width(text, size, fw)
    lines = res.split("\n")
    out.write("== %s (size=%d) -> %d lines\n" % (tag, size, len(lines)))
    for i, l in enumerate(lines, 1):
        out.write("  L%d [%s] len=%d chars\n" % (i, l, len(l)))
    out.write("\n")

# 1. current b9 subtitle (43 chars) - R719 measured 4 wrapped lines
b9 = u"守门人、巡夜员、灯塔守望都收到过 · 谁也没找到全部 · 他们管这叫「梓涵的深夜惊喜」"
show("b9-subtitle-current", b9)

# 2. first segment alone at 60px - does it fit one line?
seg1 = u"守门人、巡夜员、灯塔守望都收到过"
show("seg1-only-60", seg1)

# 3. three-segment explicit split at dot breaks, size 60
three60 = seg1 + u"\n谁也没找到全部\n他们管这叫「梓涵的深夜惊喜」"
show("three-seg-60", three60)

# 4. same split at size 57 / 56 (per-card size override candidates)
for s in (57, 56, 55):
    show("three-seg-%d" % s, three60, size=s)

# 5. dot kept as trailing at line end variant, size 57
tr = seg1 + u" ·\n谁也没找到全部 ·\n他们管这叫「梓涵的深夜惊喜」"
show("trailing-dot-57", tr, size=57)

# 6. LC-012 b4 subtitle (fleet 4-line-block reference, expect 3 wrapped lines)
lc012 = json.load(io.open(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\sources\lc012\cards-v1-matched.json", encoding="utf-8"))
b4 = [c for c in lc012["cards"] if c["lines"][0] == u"转折"][0]
show("lc012-b4-fleet-ref", b4["lines"][1])
longest = max((len(l), l) for l in wrap_for_width(b4["lines"][1], 60, 1080).split("\n"))
out.write("lc012-b4 longest wrapped line: %d chars [%s]\n\n" % (longest[0], longest[1]))

# 7. fleet per-card size override precedent scan
import glob, re
hits = []
for fp in glob.glob(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\sources\lc0*\cards-v1-matched.json") + \
         glob.glob(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\sources\bs00*\cards-*-matched.json"):
    d = open(fp, encoding="utf-8").read()
    n = len(re.findall(r'"\s*size\s*"\s*:', d))
    if n:
        hits.append((fp, n))
out.write("per-card size override precedent hits: %s\n" % (hits if hits else "NONE (first-ever if used)"))
out.close()
print("DONE")
