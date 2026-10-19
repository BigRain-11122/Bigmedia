# -*- coding: utf-8 -*-
"""M1 verbatim assert for MC-20261020-REACT-v25 (R2410).

Checks:
 1. HOT1 + HOT2 == hot title verbatim from data/intel/daily/2026-10-20.md (zhihu #2)
 2. three reaction lines exist verbatim in BigLife pools.json at the stated axes/bucket
 3. closing line exists verbatim in C-00029 anchor year-ring block
Exits 0 on all pass, 1 otherwise.
"""
import io
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
CARDS = os.path.join(REPO, "data", "storylines", "cards", "MC-20261020-REACT-v25", "cards.json")
DAILY = os.path.join(REPO, "data", "intel", "daily", "2026-10-20.md")
POOLS = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
ANCHOR = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00029.md"

HOT_PREFIX = "汇源集团发布严正声明"
REACTIONS = [
    ("怀旧", "market_open", "旧衫破了洞，换件新衫轻"),
    ("求新", "market_open", "快去看看，又有啥新鲜货？"),
    ("秩序", "market_open", "开张头一天，规矩一条不能松"),
]
CLOSING = "今天风挺大，罐头都得拿稳点儿才不会飞走呢~"


def main():
    fails = []
    cfg = json.load(io.open(CARDS, encoding="utf-8"))
    lines = cfg["cards"][0]["lines"]

    daily = io.open(DAILY, encoding="utf-8").read()
    hot_full = None
    for raw in daily.splitlines():
        s = raw.strip()
        if s[:2].isdigit() or s[:1].isdigit():
            s = s.split(".", 1)[1].strip() if "." in s else s
        if s.startswith(HOT_PREFIX):
            hot_full = s
            break
    if hot_full is None:
        fails.append("hot title not found in daily brief")
    else:
        parts = [ln for ln in lines if ln.startswith("汇源集团") or ln.startswith("推出新品牌")]
        joined = "".join(parts)
        if joined != hot_full:
            fails.append("hot split mismatch: %r != %r" % (joined, hot_full))
        if hot_full not in daily:
            fails.append("hot full not verbatim in daily")

    pools = json.load(io.open(POOLS, encoding="utf-8"))["axes"]
    for axis, bucket, line in REACTIONS:
        bucket_lines = pools.get(axis, {}).get(bucket, [])
        if line not in bucket_lines:
            fails.append("reaction not verbatim in pool %s/%s: %s" % (axis, bucket, line))
        if not any(line in ln for ln in lines):
            fails.append("reaction missing from card: %s" % line)

    anchor = io.open(ANCHOR, encoding="utf-8").read()
    if CLOSING not in anchor:
        fails.append("closing not verbatim in anchor C-00029")
    if not any(CLOSING in ln for ln in lines):
        fails.append("closing missing from card")

    for f in fails:
        print("FAIL " + f)
    print("ASSERT-%s %d checks" % ("OK" if not fails else "FAIL", 4 + len(REACTIONS)))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())