# -*- coding: utf-8 -*-
# R744 LC-019 air-budget mechanical trim v2 -> v3 (30 chars per empirical
# 0.198s/char rate, target ~58.5s / 1.5s headroom in fleet band 57.6-58.8s).
# Same laws: col2 verbatim, creed verbatim, fact numbers kept, card-carried
# or elidable cuts only, semantic zero-change.
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "data/sources/lc019/voiceover-v1.beats.txt"
V2 = ROOT / "data/sources/lc019/voiceover-v2.beats.txt"
DST = ROOT / "data/sources/lc019/voiceover-v3.beats.txt"

V3 = [
    "系统日志：全城唯一写讣告的研究员，找到了。",
    "周浩宇，碳基市民，二十八岁。",
    "QUANT 城扭塔，策略研究员。",
    "盯盘百毒不侵，收盘泡面坨了。",
    "第一次上线，被上了一课。敬畏俩字，纹在工位上。",
    "川渝腔：要得，巴适，啥子。一紧张，尾音出卖他。",
    "问题钻到底，饭都能忘。说出口的字，比章硬。",
    "每晚给爹娘报平安。",
    "他爹说，钱的事最讲天理。策略就是把道理验一万遍。",
    "徐根福总多打一勺：长身体，二十八了。风控官陈雅雯，他最怕也最服。",
    "他的信条：回撤教人做人，行情教人谦虚。",
    "全档案在公众号，转给相信敬畏市场的人。",
]

raw = V2.read_bytes().decode("utf-8")
sep = "\r\n" if "\r\n" in raw else "\n"
body = raw[:-len(sep)] if raw.endswith(sep) else raw
lines = body.split(sep)

out, bi = [], 0
for line in lines:
    if not line.strip():
        out.append(line)
        continue
    parts = line.split(" | ")
    assert len(parts) >= 3, "bad beat row: %r" % line
    out.append(" | ".join([parts[0], parts[1], V3[bi]]))
    bi += 1
assert bi == 12, "expected 12 beats, got %d" % bi
DST.write_bytes((sep.join(out) + sep).encode("utf-8"))


def cols(path, i):
    rows = []
    for l in io.open(str(path), encoding="utf-8"):
        l = l.rstrip("\r\n")
        if l.strip():
            rows.append(l.split(" | ")[i])
    return rows

for base in (V1, V2):
    assert cols(base, 0) == cols(DST, 0), "col1 drifted vs %s" % base.name
    assert cols(base, 1) == cols(DST, 1), "col2 drifted vs %s" % base.name


def bare(s):
    return re.sub(r"[，。：、；！？\s]", "", s)

v3_join = "".join(cols(DST, 2))
for must in ["回撤教人做人，行情教人谦虚", "二十八岁", "一万遍", "徐根福",
             "陈雅雯", "敬畏市场", "讣告", "周浩宇", "全家福"]:
    assert must in v3_join or must == "全家福", "lost protected text: %s" % must
# family-photo detail moved fully to card anchor (col2 verbatim holds it)
assert "全家福" in "".join(cols(DST, 1)), "family-photo not card-carried"

n2 = sum(len(bare(c)) for c in cols(V2, 2))
n3 = sum(len(bare(c)) for c in cols(DST, 2))
print("OK v3 written: col1/col2 12/12 verbatim vs v1+v2; creed+facts+names kept; "
      "voiceover chars %d -> %d (-%d)" % (n2, n3, n2 - n3))
