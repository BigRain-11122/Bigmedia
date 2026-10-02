# -*- coding: utf-8 -*-
"""R978 dedup recheck: for every non-consumed, non-nianwei festival line, check presence
in city-spirit.md and in any cards.json (fleet-wide). Output UTF-8."""
import io, json, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = os.path.join(ROOT, "media", "BigStream")
BASE = os.path.join(BS, "data", "storylines", "cards")

pool = json.load(io.open(os.path.join(ROOT, "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
spirit = io.open(os.path.join(BS, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
CONSUMED = {
    u"求新": [4, 7],
    u"怀旧": [0],
    u"侠气": [5, 13],
    u"烟火": [4, 12],
    u"秩序": [4, 14, 16],  # 16 = spirit harvest #47 (守规矩也要有情味)
    u"逍遥": [3, 17],
}
cards_blobs = []
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cards_blobs.append((d, io.open(cj, encoding="utf-8").read()))

out = []
for ax, buckets in pool["axes"].items():
    fest = buckets.get(u"festival", [])
    for i, ln in enumerate(fest):
        used = ax in CONSUMED and i in CONSUMED[ax]
        nw = u"年味" in ln
        in_spirit = ln in spirit
        hits = [d for d, blob in cards_blobs if ln in blob]
        status = []
        if used:
            status.append(u"CONSUMED-DAILY/REACT")
        if nw:
            status.append(u"NIANWEI")
        if in_spirit:
            status.append(u"IN-SPIRIT")
        if hits:
            status.append(u"IN-CARDS:" + u",".join(hits))
        out.append(u"[%s][%02d] %s %s" % (ax, i, ln, (u" <== " + u" ".join(status)) if status else u"*** FRESH ***"))

io.open(os.path.join(BS, ".c3-tmp", "r978_dedup_recheck.txt"), "w", encoding="utf-8").write(u"\n".join(out))
print("RECHECK OK")
