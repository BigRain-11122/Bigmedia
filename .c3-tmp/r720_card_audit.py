# -*- coding: utf-8 -*-
# R720: full 12-card block-geometry audit (line counts -> block top -> band intrusion)
# Empirical anchors from R719 PIL + this round: 60px line pitch ~86px, block top =
# (1920 - n_lines*86)/2 for size-60 cards; band = y745-767 (source line). Intrusion
# iff block top < 767 i.e. n_lines >= 5 (430px -> top 745). Clean: n <= 4 (top 788).
import sys, io, json
sys.path.insert(0, r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\render")
from render_card_video import wrap_for_width

out = io.open(r".c3-tmp\r720_card_audit.txt", "w", encoding="utf-8")
cfg = json.load(io.open(r"data\sources\lc013\cards-v1-matched.json", encoding="utf-8"))
fw = int(cfg["video"]["width"])
base_size = int(cfg["font"]["cards_size"])

out.write("frame_w=%d base_size=%d budget_em=%.2f\n" % (fw, base_size, (fw - 160.0) / base_size))
out.write("band y745-767; intrusion iff block_top < 767 (n_lines>=5 @60px)\n\n")
problems = []
for i, c in enumerate(cfg["cards"]):
    size = int(c.get("size", base_size))
    n = 0
    for x in c["lines"]:
        n += len(wrap_for_width(str(x), size, fw).split("\n"))
    # line pitch: fontsize*1.2 + line_spacing(14) approx per R719/R720 empirical (86@60, 82@57)
    pitch = size * 1.2 + 14
    text_h = n * pitch
    top = (1920 - text_h) / 2.0
    verdict = "INTRUDES" if top < 767 else "clean"
    if top < 767:
        problems.append(i)
    out.write("card%02d b%-2d [%s] size=%d lines=%d block_top=%.0f -> %s\n"
              % (i, i, c["lines"][0][:12], size, n, top, verdict))
    if i == 9:
        for l in wrap_for_width(str(c["lines"][1]), size, fw).split("\n"):
            out.write("      b9 L: [%s]\n" % l)
out.write("\nproblems: %s\n" % (["b%d" % p for p in problems] if problems else "NONE"))
out.close()
print("AUDITDONE")
