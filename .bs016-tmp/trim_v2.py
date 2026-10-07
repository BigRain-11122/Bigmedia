# -*- coding: utf-8 -*-
# R1692 BS-016 air-budget v2 mechanical trim (bs013 v2 clause-level caliber; card anchor column frozen)
import io

BEATS_V1 = io.open("data/sources/bs016/voiceover-v1.beats.txt", encoding="utf-8").read().splitlines()

SPOKEN_V2 = [
    "板块十年，第五问：十年后回头看，谁还记得第一块砖？",
    "系统回城市档案：没有砖，是三样东西。",
    "一条指令：下午两点五十，开一家媒体公司。",
    "一万个名字：一万零三个落库，城有了人。",
    "最软的一块：蒸笼发光，塔顶纯白，城有了自己的事。",
    "不用问人，问档案，一翻就到。",
    "时间轴倒回去：十年，三年，立国日。",
    "先亮底：往后是推演——基于硅基城市真实档案的十年推演。",
    "推演里，砖都还在，谁砌的都有名有姓。",
    "交底：砖是比喻，档案是真的，一笔一笔都在。",
    "首问说：十年后回头，看得见第一块砖。兑现了，还是我剪的。",
    "五问收官。评论区说说，你的第一块砖是什么？",
]

assert len(BEATS_V1) == 12
out = []
for i, line in enumerate(BEATS_V1):
    parts = line.split(" | ")
    assert len(parts) == 3, (i, line)
    out.append(" | ".join([parts[0], parts[1], SPOKEN_V2[i]]))
io.open("data/sources/bs016/voiceover-v2.beats.txt", "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")

c1 = sum(len(p.split(" | ")[2]) for p in BEATS_V1)
c2 = sum(len(s) for s in SPOKEN_V2)
# anchor column byte-identical check
for a, b in zip(BEATS_V1, out):
    assert a.split(" | ")[1] == b.split(" | ")[1] and a.split(" | ")[0] == b.split(" | ")[0]
print("OK v1_spoken_chars=%d v2_spoken_chars=%d delta=%d" % (c1, c2, c2 - c1))
