# -*- coding: utf-8 -*-
"""r1003 em-budget probe for DAILY v34 candidate lines (QUOTE-v2 params verbatim)."""
import io, json, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width

QV2 = os.path.join(ROOT, "data", "storylines", "cards", "MC-20260925-QUOTE-v2")
cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))
frame_w = cfg["video"]["width"]
h1_size = cfg["font"]["h1_size"]
subs_size = cfg["font"]["subs_size"]
H1_GAP = int(cfg["font"]["h1_gap"])
OPT_C = float(cfg["font"]["optical_center"])
SUBS_TOP = cfg["video"]["height"] - int(cfg["font"]["subs_bottom"])
PITCH_F = 1.35
GAP_MIN = 20
MARGIN_EM = 0.2

LINES = [
    u"城市日签 034",
    u"2026-10-02 · 国庆假期",
    u"「街坊邻里都来串串门，热闹」",
    u"——硅基城市台词池 · 侠气轴",
]
SUBS_LINE = u"引文取自硅基城市台词池（虚构城市档案）"
LADDER = [60, 50, 46, 44, 40, 36, 32, 28, 26, 24]

def stack_bottom(size, n):
    pitch = PITCH_F * size + 12
    h2_h = size + (n - 1) * pitch
    return cfg["video"]["height"] * OPT_C + H1_GAP + 1.5 * h2_h

def all_fit(size):
    budget = (frame_w - 160) / float(size)
    for ln in LINES[1:]:
        if _line_cost(ln) > budget - MARGIN_EM or len(wrap_for_width(ln, size, frame_w).split("\n")) != 1:
            return False
    return stack_bottom(size, len(LINES) - 1) <= SUBS_TOP - GAP_MIN

out = []
for i, ln in enumerate(LINES):
    out.append(u"line%d cost=%.2fem | %s" % (i, _line_cost(ln), ln))
out.append(u"subs cost=%.2fem budget at %d = %.2fem" % (_line_cost(SUBS_LINE), subs_size, (frame_w - 160) / float(subs_size)))
for s in LADDER:
    out.append(u"notch %d: all_fit=%s | budget=%.2fem | VERT bottom=%.0f gap=%+.0f" % (
        s, all_fit(s), (frame_w - 160) / float(s), stack_bottom(s, len(LINES) - 1), SUBS_TOP - stack_bottom(s, len(LINES) - 1)))
pick = next(s for s in LADDER if all_fit(s))
out.append(u"PICK=%d" % pick)
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "r1003_em_probe.txt"), "w", encoding="utf-8").write(u"\n".join(out))
print("PICK=%d" % pick)
