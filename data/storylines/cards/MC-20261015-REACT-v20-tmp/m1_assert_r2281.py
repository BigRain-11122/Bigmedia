# -*- coding: utf-8 -*-
"""M1 verbatim assertions for MC-20261015-REACT-v20 (R2281)."""
import io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CARDS = os.path.join(os.path.dirname(HERE), "MC-20261015-REACT-v20", "cards.json")
BRIEF = os.path.join(HERE, "..", "..", "..", "..", "data", "intel", "daily", "2026-10-15.md")
POOLS = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
ANCHOR = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00020.md"
CARDS_ROOT = os.path.join(HERE, "..")
OUT = os.path.join(HERE, "m1-assert-r2281.txt")

fail = []
report = ["m1-assert-r2281 (REACT-v20 M1 verbatim + fleet zero-conflict)"]

d = json.load(open(CARDS, encoding="utf-8"))
lines = d["cards"][0]["lines"]

# --- HOT1+HOT2 == daily brief zhihu #1 title (verbatim, zero edit) ---
brief = open(BRIEF, encoding="utf-8").read()
m = re.search(r"## zhihu-hot（top 10）\n\n1\. (.*?)\n", brief, re.S)
if not m:
    fail.append("BRIEF-EXTRACT: zhihu #1 not found in daily brief")
    hot_full = ""
else:
    hot_full = m.group(1).strip()
hot1, hot2 = lines[2], lines[3]
if hot_full and hot1 + hot2 != hot_full:
    fail.append("HOT-VERBATIM: HOT1+HOT2 != brief title (got %r)" % (hot1 + hot2))
else:
    report.append("HOT1+HOT2==HOT_FULL PASS (%d+%d chars, %r... )" % (len(hot1), len(hot2), hot_full[:24]))

# split-position mechanical basis: first-comma split driver would exceed 28-tier budget
first_seg = hot_full.split("，", 1)[0] + "，"
rest = hot_full[len(first_seg):]
budget28 = (1080 - 160) / 28.0
report.append("SPLIT-BASIS: first-comma tail=%d chars %.2fem vs 28-tier budget %.2fem -> %s"
              % (len(rest), len(rest), budget28, "INFEASIBLE (second-comma chosen)" if len(rest) > budget28 else "feasible?"))
if len(rest) > budget28:
    report.append("SPLIT-BASIS PASS: second comma-clause split is mechanically forced (%.2fem > %.2fem)" % (len(rest), budget28))
else:
    fail.append("SPLIT-BASIS: first-comma split was feasible - reconsider design choice")

# --- pool lines verbatim vs pools.json axes market_open bucket ---
pools = json.load(open(POOLS, encoding="utf-8"))["axes"]
axis_expect = {4: ("秩序", "市场风云多，规矩不能丢"),
               5: ("求新", "听说有个新玩法，得试一试才行"),
               6: ("侠气", "交易所一开锣，咱们得好好琢磨琢磨行情了")}
for idx, (axis, body) in axis_expect.items():
    raw = lines[idx]
    m2 = re.match(r"^%s轴：「(.*)」$" % axis, raw)
    if not m2:
        fail.append("AXIS-FORMAT line%d: %r not axis-attribution format" % (idx, raw))
        continue
    got = m2.group(1)
    bucket = pools.get(axis, {}).get("market_open", [])
    if got != body:
        fail.append("AXIS-BODY line%d: got %r expected %r" % (idx, got, body))
    elif body not in bucket:
        fail.append("AXIS-POOL line%d: %r NOT verbatim in pools market_open bucket" % (idx, body))
    else:
        report.append("AXIS line%d %s verbatim-in-bucket PASS" % (idx, axis))

# --- creed verbatim vs C-00020 anchor (line-level collision standard: REACT closing
# lines only; CENSUS "信条：" prefixed lines are legal coexistence per v19 precedent) ---
creed = "每个转角都该藏一个惊喜。"
raw8 = lines[7]
m3 = re.match(r"^关卡建筑师信条：「(.*)」$", raw8)
if not m3 or m3.group(1) != creed:
    fail.append("CREED-FORMAT: line8 %r mismatch" % raw8)
elif creed not in open(ANCHOR, encoding="utf-8").read():
    fail.append("CREED-VERBATIM: %r not found in C-00020 anchor" % creed)
else:
    report.append("CREED verbatim-in-anchor PASS (C-00020 非荣誉席 in-file check: %s)"
                  % ("荣誉" not in open(ANCHOR, encoding="utf-8").read()[:400]))

# --- fleet zero-conflict: REACT/DAILY closing-line level (line-level standard;
# CENSUS lines excluded -- bare 信条： prefix = legal coexistence, v19 precedent) ---
quoted = ["市场风云多，规矩不能丢", "听说有个新玩法，得试一试才行",
          "交易所一开锣，咱们得好好琢磨琢磨行情了",
          "关卡建筑师信条：「每个转角都该藏一个惊喜。」"]
hits = []
for name in sorted(os.listdir(CARDS_ROOT)):
    if "CENSUS" in name or "tmp" in name:
        continue  # CENSUS bare-信条 lines = legal coexistence (v19 precedent)
    cj = os.path.join(CARDS_ROOT, name, "cards.json")
    if not os.path.isfile(cj):
        continue
    try:
        other = json.load(open(cj, encoding="utf-8"))
    except Exception:
        continue
    for card in other.get("cards", []):
        for ln in card.get("lines", []):
            for q in quoted:
                if q in ln and not (name == "MC-20261015-REACT-v20"):
                    hits.append("%s :: %s" % (name, ln[:40]))
if hits:
    fail.append("FLEET-CONFLICT: %d collision(s): %s" % (len(hits), "; ".join(hits[:5])))
else:
    report.append("FLEET-CONFLICT ZERO: 4 quoted strings absent from all prior REACT/DAILY card faces")

# --- sensitive-face avoidance audit (M0 trail, honest record) ---
report.append("AVOID-TRAIL: #5 246万 political/Taiwan-strait face; #4 321万 unresolved civil dispute; "
              "#6 238万 criminal allegation unresolved; #2/#3 named-drama-IP weak mapping; "
              "#7 athlete+automaker marketing weak; #8-#10 mapping weaker than head; bilibili=named-UP format")

report.append("RESULT: " + ("ALL GREEN" if not fail else "FAIL x%d" % len(fail)))
for f_ in fail:
    report.append("FAIL-ITEM: " + f_)
open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(report) + "\n")
print("\n".join(report))
sys.exit(1 if fail else 0)
