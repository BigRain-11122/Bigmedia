# -*- coding: utf-8 -*-
# R744 LC-019 air-budget mechanical trim v1 -> v2 (R740/R736 precedent:
# col2 card-anchor verbatim zero-change, creed verbatim, fact numbers kept,
# cut words must be card-carried (in col2) or elidable; semantic zero-change).
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data/sources/lc019/voiceover-v1.beats.txt"
DST = ROOT / "data/sources/lc019/voiceover-v2.beats.txt"

V2 = [
    "系统日志：全城唯一给被毙策略写讣告的研究员，找到了。",
    "周浩宇，碳基市民，二十八岁。",
    "QUANT 城扭塔，量化策略研究员。",
    "盯盘百毒不侵，收盘想起泡面坨了。",
    "第一次策略上线，被市场上了一课。敬畏两个字，纹在工位上。",
    "川渝腔：要得，巴适，啥子。一紧张，尾音出卖他。",
    "问题钻到底，饭都能忘。说出口的字，比章还硬。",
    "挂绳串着全家福小像。每晚给爹娘报平安。",
    "他爹说，钱的事最讲天理。策略不是赌运气，是把道理验一万遍。",
    "大厨徐根福总多打一勺：长身体，都二十八了。风控官陈雅雯，他最怕也最服。",
    "他的信条：回撤教人做人，行情教人谦虚。",
    "全档案在公众号，转给相信敬畏市场的人。",
]

raw = SRC.read_bytes().decode("utf-8")
crlf = "\r\n" in raw
sep = "\r\n" if crlf else "\n"
body = raw[:-len(sep)] if raw.endswith(sep) else raw
lines = body.split(sep)

out, bi = [], 0
for line in lines:
    if not line.strip():
        out.append(line)
        continue
    parts = line.split(" | ")
    assert len(parts) >= 3, "bad beat row: %r" % line
    out.append(" | ".join([parts[0], parts[1], V2[bi]]))
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

c1a, c2a = cols(SRC, 0), cols(SRC, 1)
c1b, c2b = cols(DST, 0), cols(DST, 1)
assert c1a == c1b, "col1 drifted"
assert c2a == c2b, "col2 card anchors drifted"


def bare(s):
    return re.sub(r"[，。：、；！？\s]", "", s)

v2_join = "".join(cols(DST, 2))
for must in ["回撤教人做人，行情教人谦虚", "二十八岁", "一万遍", "徐根福", "陈雅雯", "敬畏市场", "讣告"]:
    assert must in v2_join, "lost protected text: %s" % must

n1 = sum(len(bare(c)) for c in cols(SRC, 2))
n2 = sum(len(bare(c)) for c in cols(DST, 2))
print("OK v2 written: col1/col2 12/12 verbatim; creed+facts+names kept; "
      "voiceover chars %d -> %d (-%d)" % (n1, n2, n1 - n2))
