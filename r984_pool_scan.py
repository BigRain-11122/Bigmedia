# -*- coding: utf-8 -*-
"""R984 pool scan: unused festival-bucket lines for DAILY v15 selection (UTF-8 file output)."""
import io, json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()

# consumed festival lines: DAILY v1-v14 (14) + REACT-v8 trio (3) = 17
consumed = {
    (u"求新", 4), (u"怀旧", 0), (u"侠气", 5), (u"烟火", 4), (u"秩序", 4), (u"逍遥", 3),
    (u"求新", 7), (u"侠气", 13), (u"求新", 12), (u"怀旧", 3), (u"烟火", 13), (u"逍遥", 15),
    (u"侠气", 2), (u"求新", 3),
    (u"逍遥", 17), (u"烟火", 12), (u"秩序", 14),
}
# python console cannot hold CJK axis keys reliably on this box; map by order
axes = list(pool["axes"].keys())
cn = {axes[0]: u"轴1", axes[1]: u"轴2", axes[2]: u"轴3", axes[3]: u"轴4", axes[4]: u"轴5", axes[5]: u"轴6"}

lines_out = []
total_unused = 0
for ax in axes:
    fest = pool["axes"][ax].get("festival", [])
    for i, ln in enumerate(fest):
        if (ax, i) in consumed:
            continue
        total_unused += 1
        tag = u"IN-SPIRIT" if ln in spirit else u""
        lines_out.append(u"%s/%d %s %s" % (cn[ax], i, ln, tag))

io.open(os.path.join(ROOT, "r984_pool_scan.txt"), "w", encoding="utf-8").write(
    u"axes order: %s\nunused=%d\n" % (u" ".join(u"%s=%s" % (cn[a], a) for a in axes), total_unused)
    + u"\n".join(lines_out) + u"\n")
print("scan written, unused=%d" % total_unused)
