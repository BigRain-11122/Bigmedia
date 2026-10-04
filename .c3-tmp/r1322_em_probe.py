# -*- coding: utf-8 -*-
"""r1322 em-ladder probe for DAILY v67 (侠气/weekend/5) - machine band pick before build."""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src', 'render'))
from render_card_video import _line_cost, wrap_for_width  # noqa

QV2 = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260925-QUOTE-v2')
cfg = json.load(io.open(os.path.join(QV2, 'cards.json'), encoding='utf-8'))

LINES = [
    u'城市日签 067',
    u'2026-10-05 · 国庆假期 · 晨',
    u'「茶余饭后讲讲闲话，才不闷」',
    u'——硅基城市台词池 · 侠气轴',
]
SUBS_LINE = u'引文取自硅基城市台词池（虚构城市档案）'

frame_w = cfg['video']['width']
h1_size = cfg['font']['h1_size']
subs_size = cfg['font']['subs_size']
LADDER = [60, 50, 46, 44, 40, 36, 32, 28, 26, 24]
MARGIN_EM = 0.2
H1_GAP = int(cfg['font']['h1_gap'])
OPT_C = float(cfg['font']['optical_center'])
SUBS_TOP = cfg['video']['height'] - int(cfg['font']['subs_bottom'])
PITCH_F = 1.35
GAP_MIN = 20


def stack_bottom(size, n):
    pitch = PITCH_F * size + 12
    h2_h = size + (n - 1) * pitch
    return cfg['video']['height'] * OPT_C + H1_GAP + 1.5 * h2_h


def all_fit(size):
    budget = (frame_w - 160) / float(size)
    for ln in LINES[1:]:
        if _line_cost(ln) > budget - MARGIN_EM or len(wrap_for_width(ln, size, frame_w).split('\n')) != 1:
            return False
    return stack_bottom(size, len(LINES) - 1) <= SUBS_TOP - GAP_MIN


out = ['frame_w=%d h1=%d subs=%d SUBS_TOP=%d base_px=%.1f' % (
    frame_w, h1_size, subs_size, SUBS_TOP,
    cfg['video']['height'] * OPT_C + H1_GAP)]
for ln in LINES:
    out.append(u'cost %.2fem | %s' % (_line_cost(ln), ln))
out.append('subs cost %.2fem budget %.2fem' % (_line_cost(SUBS_LINE), (frame_w - 160) / float(subs_size)))
for s in LADDER:
    budget = (frame_w - 160) / float(s)
    margins = [_line_cost(ln) - budget for ln in LINES[1:]]
    sb = stack_bottom(s, len(LINES) - 1)
    out.append('band %2d: budget %.2fem margins %s stack_bottom %.0f gap %+.0f fit=%s' % (
        s, budget, ' '.join('%+.2f' % m for m in margins), sb, SUBS_TOP - sb, all_fit(s)))
pick = next(s for s in LADDER if all_fit(s))
out.append('LADDER_PICK=%d' % pick)
io.open(os.path.join(ROOT, '.c3-tmp', 'r1322_em_probe.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('pick=%d' % pick)
