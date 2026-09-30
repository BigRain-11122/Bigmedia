# -*- coding: utf-8 -*-
# R752 LC-020 air-budget mechanical trim v1 -> v2 (heavy structural cut,
# R744_trim channel: card-carried or elidable cuts only, semantic zero-change,
# col2 verbatim, creed verbatim, fact numbers kept).
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "data/sources/lc020/voiceover-v1.beats.txt"
DST = ROOT / "data/sources/lc020/voiceover-v2.beats.txt"

# fleet norms: hook formula kept; faction -> card (LC-019 v3 b2 same-cut);
# tagline kept this pass (v3 candidate); 整层楼吃饭/立下规矩/上海话底色/
# 骂人最高级句/塔顶的白句/绿红 elaboration -> card-carried (col2 verbatim).
V2 = [
    "系统日志：全城唯一按涨跌换菜谱的大厨，找到了。",
    "徐根福，碳基市民，六十六岁。",
    "QUANT 城 K 线广场，食堂大厨。不谈数字，只谈火候。",
    "收盘铃就是开饭铃。凌晨四点去菜市挑时令。",
    "那年行情大跌，整层楼没人下来。他把汤一勺一勺送到工位：绿盘日，例汤免费。",
    "吃过了伐？多加一勺，不许还价。",
    "三十年大勺，颠勺比钟还稳。淋过雨，想给人撑伞。",
    "厨房的白是本分。木勺用了二十年。",
    "他不懂数字，只懂一样：人吃饱了，才有底气。",
    "惦记名单第一名，周浩宇。那娃光吃泡面，成啥体统。",
    "他的信条：行情再绿，汤是热的。",
    "全档案在公众号，转给相信好好吃饭的人。",
]

raw = V1.read_bytes().decode("utf-8")
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

assert cols(V1, 0) == cols(DST, 0), "col1 drifted vs v1"
assert cols(V1, 1) == cols(DST, 1), "col2 drifted vs v1"


def bare(s):
    return re.sub(r"[，。：、；！？\s]", "", s)

v2_join = "".join(cols(DST, 2))
for must in ["行情再绿，汤是热的", "六十六岁", "三十年", "凌晨四点", "二十年",
             "周浩宇", "好好吃饭", "徐根福", "按涨跌换菜谱"]:
    assert must in v2_join, "lost protected text: %s" % must

n1 = sum(len(bare(c)) for c in cols(V1, 2))
n2 = sum(len(bare(c)) for c in cols(DST, 2))
rep = io.open(str(ROOT / ".c3-tmp/r752_trim_v2.txt"), "w", encoding="utf-8")
rep.write("OK v2 written: col1/col2 verbatim 12/12 vs v1; creed+facts+names "
          "kept; voiceover chars %d -> %d (-%d)\n" % (n1, n2, n1 - n2))
rep.close()
print("OK v2 chars %d -> %d (-%d)" % (n1, n2, n1 - n2))
