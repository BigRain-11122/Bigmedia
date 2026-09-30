# -*- coding: utf-8 -*-
# R800: BS-008 full 12-card block-geometry audit (R760 card_audit.py adapted;
# standing pre-render face per R720 law / R721 E8 note)
import sys, io, json
sys.path.insert(0, r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\render")
from render_card_video import wrap_for_width

out = io.open(r".c3-tmp\r800_card_audit.txt", "w", encoding="utf-8")
cfg = json.load(io.open(r"data\sources\bs008\cards-v2-matched.json", encoding="utf-8"))
fw = int(cfg["video"]["width"])
base_size = int(cfg["font"]["cards_size"])

out.write("frame_w=%d base_size=%d budget_em=%.2f\n" % (fw, base_size, (fw - 160.0) / base_size))
out.write("band y745-767; intrusion iff block_top < 767; net>=20px target (R720 floor)\n\n")
problems = []
for i, c in enumerate(cfg["cards"]):
    size = int(c.get("size", base_size))
    n = 0
    for x in c["lines"]:
        n += len(wrap_for_width(str(x), size, fw).split("\n"))
    pitch = size * 1.2 + 14
    text_h = n * pitch
    top = (1920 - text_h) / 2.0
    verdict = "INTRUDES" if top < 767 else ("thin" if top < 787 else "clean")
    if top < 767:
        problems.append(i)
    out.write("card%02d b%-2d [%s] size=%d lines=%d pitch=%.1f block_top=%.0f net=%.0fpx -> %s\n"
              % (i, i, c["lines"][0][:12], size, n, pitch, top, top - 767, verdict))
    if n >= 4:
        for l in wrap_for_width(str(c["lines"][1]), size, fw).split("\n"):
            out.write("      b%d L: [%s]\n" % (i, l))
out.write("\nproblems: %s\n" % (["b%d" % p for p in problems] if problems else "NONE"))
out.close()
print("AUDITDONE problems=%s" % (problems if problems else "NONE"))
