# -*- coding: utf-8 -*-
"""M1 verbatim assert for MC-20261024-REACT-v27 (r2423).

Checks:
 1. hot line verbatim in data/intel/daily/2026-10-24.md (zhihu-hot #4, title only,
    split at the comma break only)
 2. three axis lines verbatim in BigLife pools.json under axis/weekend
 3. closing line verbatim in census anchor C-00011.md yearring block
 4. fiction separator line present in cards.json
 5. heat number NOT present on card face (desensitization)
"""
import io
import json
import os
import sys

HERE = os.path.abspath(__file__)
ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
)
CARD_DIR = os.path.join(ROOT, "data", "storylines", "cards", "MC-20261024-REACT-v27")
DAILY = os.path.join(ROOT, "data", "intel", "daily", "2026-10-24.md")
POOLS = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
ANCHOR = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00011.md"

HOT_PARTS = [
    "Anthropic 科学家称「AGI 若三年内到来读博将失去意义」，",
    "如何看待这一观点？",
]
AXES = [
    ("怀旧", "捡到一本旧书，封皮都发黄了"),
    ("求新", "学了个新画法，周末正好练练手"),
    ("秩序", "规矩不能乱，但偶尔放松一下也行"),
]
CLOSING = "OK 的呀，今夜风挺大，游丝又得好好对秒才行。"
SEP = "——以下三行为硅基城民虚构反应——"
HEAT = "197"

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
    check("closing-verbatim", CLOSING in anchor, "(C-00011 yearring 2026-10-24)")

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
    check("series-no", lines[0] == "城市速报 027", "(series continuity)")

    print("RESULT fails=%d" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())