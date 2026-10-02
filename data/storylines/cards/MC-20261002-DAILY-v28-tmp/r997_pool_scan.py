# -*- coding: utf-8 -*-
"""r997 pre-build pool scan: festival bucket availability for DAILY v28 (R978 interception
lesson execution). FREE/USED/AVOID(nianwei season-law R972) per line, consumed marks derived
from city-spirit.md harvest face + all piece cards.json (content-addressed, no manual list).
Output = MC-20261002-DAILY-v28-tmp/r997_pool_scan.txt (UTF-8)."""
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
TMP = os.path.dirname(os.path.abspath(__file__))
os.makedirs(TMP, exist_ok=True)
BASE = os.path.join(ROOT, "data", "storylines", "cards")

pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
cards_text = []
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cards_text.append(io.open(cj, encoding="utf-8").read())

out = []
for axis in [u"求新", u"怀旧", u"侠气", u"烟火", u"秩序", u"逍遥"]:
    out.append(u"== %s festival ==" % axis)
    for i, ln in enumerate(pool["axes"][axis][u"festival"]):
        if u"年味" in ln:
            st = u"AVOID(年味)"
        elif ln in spirit or any(ln in c for c in cards_text):
            st = u"USED"
        else:
            st = u"FREE"
        out.append(u"[%d] %s %s" % (i, st, ln))
io.open(os.path.join(TMP, "r997_pool_scan.txt"), "w", encoding="utf-8").write(u"\n".join(out))
free = sum(1 for axis in pool["axes"] for ln in pool["axes"][axis][u"festival"]
           if u"年味" not in ln and ln not in spirit and not any(ln in c for c in cards_text))
print("OK festival_free_lines=%d" % free)
