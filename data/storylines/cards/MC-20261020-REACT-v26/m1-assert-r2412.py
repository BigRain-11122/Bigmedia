# -*- coding: utf-8 -*-
"""M1 verbatim assert for MC-20261020-REACT-v26 (r2412).

Checks:
 1. hot line verbatim in data/intel/daily/2026-10-20.md (zhihu-hot #8, title only)
 2. three axis lines verbatim in BigLife pools.json under axis/morning
 3. closing line verbatim in census anchor C-00023.md yearring block
 4. fiction separator line present in cards.json
 5. heat number NOT present on card face (desensitization)
"""
import io
import json
import os
import re
import sys

HERE = os.path.abspath(__file__)
ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
)
CARD_DIR = os.path.join(ROOT, "data", "storylines", "cards", "MC-20261020-REACT-v26")
DAILY = os.path.join(ROOT, "data", "intel", "daily", "2026-10-20.md")
POOLS = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
ANCHOR = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00023.md"

HOT = "如何看待日文“の”在中文互联网上的广泛使用？"
AXES = [
    ("怀旧", "街坊邻里见了面，总爱唠叨两句闲话"),
    ("求新", "新画作出炉了，快来看看有没有你喜欢的吧！"),
    ("秩序", "守规矩，才稳得住这超体宇宙城的根"),
]
CLOSING = "再挖一层，这稿子角度不对，得再琢磨琢磨。"
SEP = "——以下三行为硅基城民虚构反应——"

fails = []


def check(name, cond, detail=""):
    if cond:
        print("PASS %s %s" % (name, detail))
    else:
        print("FAIL %s %s" % (name, detail))
        fails.append(name)


def main():
    daily = io.open(DAILY, encoding="utf-8").read()
    check("hot-verbatim", HOT in daily, "(len=%d)" % len(HOT))

    pools = json.load(io.open(POOLS, encoding="utf-8"))
    axes = pools.get("axes", {})
    for axis, line in AXES:
        bucket = axes.get(axis, {}).get("morning", [])
        check("pool-%s" % axis, line in bucket, "(morning bucket)")

    anchor = io.open(ANCHOR, encoding="utf-8").read()
    check("closing-verbatim", CLOSING in anchor, "(C-00023 yearring)")

    cards = json.load(io.open(os.path.join(CARD_DIR, "cards.json"), encoding="utf-8"))
    lines = cards["cards"][0]["lines"]
    check("separator", SEP in lines)
    check("no-heat-on-face", not any("124" in l for l in lines), "(heat stays in ledger)")
    check("closing-on-card", any(CLOSING in l for l in lines))
    check("hot-on-card", HOT in lines)
    for axis, line in AXES:
        check("axis-on-card-%s" % axis, any(line in l for l in lines))
    check("source-line-marker", "知乎热榜" in lines[1] and "热榜提问" in lines[1])

    print("RESULT fails=%d" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())