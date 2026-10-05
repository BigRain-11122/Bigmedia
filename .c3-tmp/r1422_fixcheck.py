# -*- coding: ascii -*-
# R1422 fix-check: sibling format defects + pools content-addressed count
import io, re, json

BS = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
pools = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"

# 1) sibling single-digit-hour log entries in state.json
t = io.open(BS + r"\src\os\state.json", encoding="utf-8").read()
sib = re.findall(r'"20\d\d-\d\d-\d\d \d:[0-5]?\d[^"]{0,30}', t)
print("SINGLE_DIGIT_HOUR_HITS: %d" % len(sib))
for s in sib[:10]:
    print("  HIT: %s" % s)

# 2) pools content-addressed full count (axes 6x216 + sprite 144 baseline = 1440)
pj = json.load(io.open(pools, encoding="utf-8"))
def count_lines(obj):
    n = 0
    if isinstance(obj, list):
        n += len(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            n += count_lines(v)
    return n
total = count_lines(pj.get("axes", {}))
sprite = count_lines(pj.get("sprite", pj.get("sprites", 0)))
print("AXES_LINES: %d" % total)
print("SPRITE_LINES: %d" % sprite)
print("TOTAL_LINES: %d (baseline 1440)" % (total + sprite))
# bucket structure
ax = pj.get("axes")
if isinstance(ax, dict):
    for k, v in list(ax.items())[:8]:
        print("  AXES_KEY %s: %d" % (k, count_lines(v)))
