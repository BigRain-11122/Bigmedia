# -*- coding: utf-8 -*-
"""R978 DAILY v9 anchor scan: dump festival bucket lines for all 6 axes with indices,
mark consumed indices, em cost, and nianwei-exclusion flags. Output UTF-8 file."""
import io, json, os, sys

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = os.path.join(ROOT, "media", "BigStream")
sys.path.insert(0, os.path.join(BS, "src", "render"))
from render_card_video import _line_cost

pool = json.load(io.open(os.path.join(ROOT, "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
CONSUMED = {
    u"求新": [4, 7],
    u"怀旧": [0],
    u"侠气": [5, 13],
    u"烟火": [4, 12],
    u"秩序": [4, 14],
    u"逍遥": [3, 17],
}
out = []
out.append(u"top-level keys: %s" % u",".join(pool.keys()))
axes = pool["axes"]
out.append(u"axes: %s" % u",".join(axes.keys()))
for ax, buckets in axes.items():
    fest = buckets.get(u"festival", [])
    out.append(u"")
    out.append(u"=== axis %s festival (%d lines) ===" % (ax, len(fest)))
    for i, ln in enumerate(fest):
        flags = []
        if ax in CONSUMED and i in CONSUMED[ax]:
            flags.append(u"CONSUMED")
        if u"年味" in ln:
            flags.append(u"NIANWEI-EXCLUDE(R972)")
        cost = _line_cost(ln)
        out.append(u"[%s][festival][%02d] em=%.2f %s %s" % (ax, i, cost, ln, u" ".join(flags)))

spirit = io.open(os.path.join(BS, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
out.append(u"")
out.append(u"=== city-spirit.md (38 harvest) head check ===")
spirit_lines = [l.strip() for l in spirit.splitlines() if l.strip() and not l.strip().startswith(u"#")]
out.append(u"spirit non-empty lines: %d" % len(spirit_lines))
for l in spirit_lines[:45]:
    out.append(u"SPIRIT: %s" % l)

io.open(os.path.join(BS, ".c3-tmp", "r978_fest_scan.txt"), "w", encoding="utf-8").write(u"\n".join(out))
print("SCAN OK lines written")
