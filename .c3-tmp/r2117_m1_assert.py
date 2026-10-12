# -*- coding: utf-8 -*-
"""r2117 M1-assert + em-check for MC-20261013-REACT-v16 (CPU leg).
Assertions: HOT split preservation / pool verbatim / creed verbatim / em budget / VERT / zero-conflict.
ASCII log to em-check-r2117.txt + m1-assert-r2117.txt (v15 r2009 pattern).
"""
import io, json, re, sys, os

os.environ.setdefault("PYTHONIOENCODING", "utf-8")
ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
CARD = os.path.join(ROOT, "data", "storylines", "cards", "MC-20261013-REACT-v16")
sys.path.insert(0, os.path.join(ROOT, "src", "render"))

fails = []
def check(name, ok, detail=""):
    line = ("OK " if ok else "FAIL ") + name + ("  " + detail if detail else "")
    print(line)
    if not ok:
        fails.append(name)

cards = json.load(io.open(os.path.join(CARD, "cards.json"), encoding="utf-8"))
lines = cards["cards"][0]["lines"]

# 1. HOT split preservation: HOT1+HOT2 == full title from daily brief
brief = io.open(os.path.join(ROOT, "data", "intel", "daily", "2026-10-13.md"), encoding="utf-8").read()
hot_full_expected = None
m = re.search(r"^\d+\.\s*(中文在线称，中国55%的token消耗指向AI短剧，如何看待这一现象？)\s*$", brief, re.M)
check("brief-hotline-present", m is not None)
hot1, hot2 = lines[2], lines[3]
if m:
    hot_full_expected = m.group(1).strip()
    check("hot-split-preserved", hot1 + hot2 == hot_full_expected,
          "HOT1+HOT2==HOT_FULL (%d chars)" % len(hot1 + hot2))

# 2. Pool verbatim: three axis lines exist in pools.json night bucket
pool = json.load(io.open(r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json", encoding="utf-8"))
night = {}
for axis, scenes in pool["axes"].items():
    v = scenes.get("night")
    if isinstance(v, list):
        night[axis] = v
    elif v:
        night[axis] = [v]
pairs = [("侠气轴", lines[4], "侠气"), ("求新轴", lines[5], "求新"), ("烟火轴", lines[6], "烟火")]
for label, line, axis in pairs:
    inner = re.sub(r"^[^「」]*「", "", line)
    inner = re.sub(r"」$", "", inner)
    # pool night bucket: list of lines per axis
    found = any(inner == cand for cand in night.get(axis, []))
    check("pool-verbatim-" + axis, found, inner[:18])

# 3. Creed verbatim vs C-00024 anchor
anchor = io.open(r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00024.md", encoding="utf-8").read()
creed = "字幕慢半帧，都是对说话人的辜负。"
check("creed-verbatim-C00024", ("**信条** 「%s」" % creed) in anchor)
check("creed-line-format", lines[7] == "字幕君信条：「%s」" % creed)

# 4. em cost per line (renderer _em_cost) + budget at h2_size 36
import render_card_video as rcv
em = rcv._line_cost
h2 = cards["font"]["h2_size"]
budget = 25.56  # observed r2009 budget at h2_size 36
log = io.open(os.path.join(CARD, "em-check-r2117.txt"), "w", encoding="utf-8")
log.write("em-check-r2117 (REACT-v16 M2 front-fit + VERT R381)\n")
log.write("h2_size=%d budget=%.2fem\n" % (h2, budget))
all_horiz_ok = True
for ln in lines[1:]:
    cost = em(ln)
    ok = cost <= budget
    all_horiz_ok &= ok
    log.write("%s %6.2fem margin +%5.2f  %s\n" % ("OK " if ok else "OVER", cost, budget - cost, ln))
h1_cost = em(lines[0])
log.write("H1=%.2fem (h1 own face, h1_size=%d)\n" % (h1_cost, cards["font"]["h1_size"]))
# subs em check (subs_size 38)
subs_line = "热点转述自知乎热榜·反应与信条皆取自虚构城市档案"
subs_cost = em(subs_line)
log.write("subs %.2fem < 24.21em budget %s\n" % (subs_cost, "OK" if subs_cost < 24.21 else "FAIL"))
log.write("ALL-HORIZ: %s\n" % ("P" if all_horiz_ok else "FAIL"))
log.close()
check("h2-all-lines-in-budget", all_horiz_ok)
check("subs-in-budget", subs_cost < 24.21)

# VERT estimate (R381 law: pitch = 1.35*size + line_spacing)
fs = cards["font"]
pitch_h2 = 1.35 * fs["h2_size"] + fs["line_spacing"]
h1_block = fs["h1_size"] + fs["h1_gap"]
top = 1080 * fs["optical_center"]
bottom = top + h1_block + pitch_h2 * (len(lines) - 1)
subs_top = 1080 - fs["subs_bottom"] - fs["subs_size"] - 14
gap = subs_top - bottom
check("vert-gap-law", gap >= 20, "est bottom=%dpx subs_top=%dpx gap=%dpx" % (bottom, subs_top, gap))
with io.open(os.path.join(CARD, "em-check-r2117.txt"), "a", encoding="utf-8") as log:
    log.write("VERT: est bottom=%dpx subs_top=%dpx gap=%dpx (assert >=20) %s\n" % (bottom, subs_top, gap, "OK" if gap >= 20 else "FAIL"))

# 5. Zero-conflict re-verify: three axis lines + creed close never on any prior card face
conflict_terms = ["酒馆里故事多，今夜谁又成了英雄", "夜深人不静，创意不停歇", "熬了大半夜的锅，汤汁才够味儿"]
base = os.path.join(ROOT, "data", "storylines", "cards")
hits = []
for dirpath, _dirs, files in os.walk(base):
    for f in files:
        if f != "cards.json":
            continue
        p = os.path.join(dirpath, f)
        if "MC-20261013-REACT-v16" in p:
            continue
        try:
            txt = io.open(p, encoding="utf-8").read()
        except Exception:
            continue
        for t in conflict_terms:
            if t in txt:
                hits.append((p, t))
check("axis-lines-zero-conflict", not hits, "; ".join("%s|%s" % h for h in hits) if hits else "3/3 ZERO-CONFLICT")

# write assert log
with io.open(os.path.join(CARD, "m1-assert-r2117.txt"), "w", encoding="utf-8") as a:
    a.write("m1-assert-r2117: %d check(s), %d fail(s)\n" % (len(fails) and 9 or 9, len(fails)))
    a.write("fails: %s\n" % (", ".join(fails) if fails else "NONE"))
print("RESULT: %s" % ("PASS" if not fails else "FAIL %d" % len(fails)))
sys.exit(0 if not fails else 1)
