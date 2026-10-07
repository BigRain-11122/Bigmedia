# -*- coding: utf-8 -*-
# R1692 BS-016 air-budget v3 micro-trim (bs015 v4/v6 caliber; card anchor column frozen)
import io

BEATS_V2 = io.open("data/sources/bs016/voiceover-v2.beats.txt", encoding="utf-8").read().splitlines()

SPOKEN_V3 = [
    "板块十年，第五问：十年后回头看，谁还记得第一块砖？",
    "系统回城市档案：没有砖，是三样东西。",
    "一条指令：下午两点五十，开一家媒体公司。",
    "一万个名字：一万零三落库，城有了人。",
    "最软的一块：蒸笼发光，塔顶纯白，城有了自己的事。",
    "问档案，一翻就到。",
    "时间轴倒回去：十年，三年，立国日。",
    "先亮底：往后是推演——基于硅基城市真实档案的十年推演。",
    "推演里砖都还在，谁砌的都有名有姓。",
    "交底：砖是比喻，档案是真的，一笔一笔都在。",
    "首问说：十年后回头，看得见第一块砖。兑现了，还是我剪的。",
    "五问收官。评论区说说，你的第一块砖是什么？",
]

assert len(BEATS_V2) == 12
out = []
for i, line in enumerate(BEATS_V2):
    parts = line.split(" | ")
    assert len(parts) == 3, (i, line)
    out.append(" | ".join([parts[0], parts[1], SPOKEN_V3[i]]))
io.open("data/sources/bs016/voiceover-v3.beats.txt", "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")

c2 = sum(len(p.split(" | ")[2]) for p in BEATS_V2)
c3 = sum(len(s) for s in SPOKEN_V3)
for a, b in zip(BEATS_V2, out):
    assert a.split(" | ")[1] == b.split(" | ")[1] and a.split(" | ")[0] == b.split(" | ")[0]
print("OK v2_spoken_chars=%d v3_spoken_chars=%d delta=%d" % (c2, c3, c3 - c2))
