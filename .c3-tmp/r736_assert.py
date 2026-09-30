# -*- coding: utf-8 -*-
# R736 verbatim assertion: col1/col2 zero-drift v1->v4, creed intact, fact digits preserved
import io, re

def rows(p):
    out = []
    for line in io.open(p, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip():
            continue
        parts = line.split(" | ")
        out.append(parts)
    return out

v1 = rows("data/sources/lc017/voiceover-v1.beats.txt")
v4 = rows("data/sources/lc017/voiceover-v4.beats.txt")
assert len(v1) == len(v4) == 12, (len(v1), len(v4))

col12_drift = []
for i, (a, b) in enumerate(zip(v1, v4)):
    if a[0] != b[0] or a[1] != b[1]:
        col12_drift.append(i)
creed_ok = v4[10][2] == v1[10][2] == "他的信条：城市不会忘记，除非我们偷懒。"
facts = ["二十六岁", "五条街区", "一万个", "三十年", "三个月"]
v4_all = "".join(r[2] for r in v4)
facts_ok = [f for f in facts if f in v4_all]
print("col12_zero_drift=%s" % (not col12_drift, ))
print("creed_verbatim=%s" % creed_ok)
print("facts_kept=%d/%d %s" % (len(facts_ok), len(facts), facts_ok))
chars = [sum(len(re.sub(r"[，。：；、\s]", "", r[2])) for r in rows("data/sources/lc017/voiceover-v%s.beats.txt" % v)) for v in (1, 2, 3, 4)]
print("voice_chars v1->v4 =", chars)
