# -*- coding: utf-8 -*-
"""R982 pool pre-check for DAILY v13: festival bucket full scan with USED marks."""
import io, json, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = os.path.join(ROOT, "media", "BigStream")
pool = json.load(io.open(os.path.join(ROOT, "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))

USED = {
 u"求新": {4: u"DAILY-v1", 7: u"DAILY-v7", 12: u"DAILY-v9"},
 u"怀旧": {0: u"DAILY-v2", 3: u"DAILY-v10"},
 u"侠气": {5: u"DAILY-v3", 13: u"DAILY-v8"},
 u"烟火": {4: u"DAILY-v4", 12: u"REACT-v8", 13: u"DAILY-v11"},
 u"秩序": {4: u"DAILY-v5", 14: u"REACT-v8"},
 u"逍遥": {3: u"DAILY-v6", 15: u"DAILY-v12", 17: u"REACT-v8"},
}
# 年味-class lines excluded per R972 rule (guonian context mismatch with National Day)
NIANWEI = {0, 6, 8, 14}

out = []
for ax in [u"烟火", u"侠气", u"求新", u"怀旧", u"秩序", u"逍遥"]:
    fest = pool["axes"][ax]["festival"]
    out.append(u"=== %s ===" % ax)
    for i, ln in enumerate(fest):
        marks = []
        if i in USED.get(ax, {}):
            marks.append(u"USED:%s" % USED[ax][i])
        if i in NIANWEI and (u"年" in ln or u"春" in ln or u"岁" in ln or u"福" in ln or u"生肖" in ln):
            marks.append(u"年味核-candidate")
        out.append(u"  [%02d] %s %s" % (i, ln, u" ".join(marks)))

io.open(os.path.join(BS, ".c3-tmp", "r982_fest_pool.txt"), "w", encoding="utf-8").write(u"\n".join(out))
print("POOL-SCAN-OK lines=%d" % len(out))
