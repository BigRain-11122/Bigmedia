# -*- coding: utf-8 -*-
"""M1 verbatim assert for MC-20261024-REACT-v28 (r2424).

Checks:
 1. hot line verbatim in data/intel/daily/2026-10-24.md (zhihu-hot #3, title only,
    split at comma breaks only)
 2. three axis lines verbatim in BigLife pools.json under axis/weekend
 3. closing line verbatim in census anchor C-00025.md yearring block
 4. fiction separator line present in cards.json
 5. heat number NOT present on card face (desensitization)
 6. no named platform/company on card face
"""
import io
import json
import os
import sys

HERE = os.path.abspath(__file__)
ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
)
CARD_DIR = os.path.join(ROOT, "data", "storylines", "cards", "MC-20261024-REACT-v28")
DAILY = os.path.join(ROOT, "data", "intel", "daily", "2026-10-24.md")
POOLS = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
ANCHOR = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00025.md"

HOT_PARTS = [
    "一顺风车司机困了让乘客开车，",
    "自己睡到目的地还照常收钱，",
    "平台最初只赔20元代金券，最后全额退款，合理吗？",
]
AXES = [
    ("怀旧", "修伞老李头手里的伞骨纹丝不动，就像他的心事"),
    ("求新", "做主播也得有两把刷子，不是嘴皮子活"),
    ("秩序", "门关紧些，外面风大"),
]
CLOSING = "今夜雨还在下，撑着伞走稳当。船稳，人心才稳。"
SEP = "——以下三行为硅基城民虚构反应——"
HEAT = "295"

fails = []


def check(name, cond, detail=""):
    if cond:
        print("PASS %s %s" % (name, detail))
    else:
        print("FAIL %s %s" % (name, detail))
        fails.append(name)


def main():
    daily = io.open(DAILY, encoding="utf-8").read()
    hot = "".join(HOT_PARTS)
    check("hot-verbatim", hot in daily.replace("  ", " "), "(len=%d)" % len(hot))

    pools = json.load(io.open(POOLS, encoding="utf-8"))
    axes = pools.get("axes", {})
    for axis, line in AXES:
        bucket = axes.get(axis, {}).get("weekend", [])
        check("pool-%s" % axis, line in bucket, "(weekend bucket)")

    anchor = io.open(ANCHOR, encoding="utf-8").read()
    check("closing-verbatim", CLOSING in anchor, "(C-00025 yearring 2026-10-24)")

    cards = json.load(io.open(os.path.join(CARD_DIR, "cards.json"), encoding="utf-8"))
    lines = cards["cards"][0]["lines"]
    check("separator", SEP in lines)
    check("no-heat-on-face", not any(HEAT in l for l in lines), "(heat stays in ledger)")
    check("closing-on-card", any(CLOSING in l for l in lines))
    for part in HOT_PARTS:
        check("hot-on-card", part in lines, "(part)")
    for axis, line in AXES:
        check("axis-on-card-%s" % axis, any(line in l for l in lines))
    check("source-line-marker", "知乎热榜" in lines[1] and "热榜提问" in lines[1])
    check("series-no", lines[0] == "城市速报 028", "(series continuity)")
    named = ["滴滴", "哈啰", "嘀嗒"]
    check("no-named-platform", not any(n in l for l in lines for n in named))

    print("RESULT fails=%d" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())