import json, re
from pathlib import Path

srt = Path(".bs001-dd-tmp/subs.srt").read_text(encoding="utf-8")
cues = []
for block in srt.strip().split("\n\n"):
    lines = block.splitlines()
    m = re.match(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", lines[1])
    g = [int(x) for x in m.groups()]
    st = g[0]*3600 + g[1]*60 + g[2] + g[3]/1000
    en = g[4]*3600 + g[5]*60 + g[6] + g[7]/1000
    cues.append((st, en))

assert len(cues) == 69, len(cues)

# segment map per R194: seg1=beats1-7, seg2=8-17, seg3=18-41, seg4=42-55, seg5=56-63, seg6=64-69
SEG_BOUNDS = [(1,7),(8,17),(18,41),(42,55),(56,63),(64,69)]
total = cues[-1][1] - cues[0][0]
print("total_span_s=%.2f (%dm%02ds)" % (total, int(total)//60, int(total)%60))
spoken_total = sum(en-st for st,en in cues)
print("spoken_total_s=%.2f spoken_ratio=%.3f" % (spoken_total, spoken_total/total))

for i,(a,b) in enumerate(SEG_BOUNDS,1):
    seg = cues[a-1:b]
    span = seg[-1][1]-seg[0][0]
    spoken = sum(en-st for st,en in seg)
    print("seg%d beats=%d span=%.2f (%dm%02ds) spoken=%.2f ratio60=%.1fs/60s" % (
        i, b-a+1, span, int(span)//60, int(span)%60, spoken, spoken/span*60))

# rolling 60s window max spoken
events = []
for st,en in cues:
    events.append((st,1)); events.append((en,-1))
events.sort()
best = 0; cur = 0; t_best = 0
for t,d in events:
    cur += d
    if cur > best: best = cur; t_best = t
# max simultaneous is trivial; instead compute spoken in any 60s window via prefix sums
import bisect
starts = [st for st,en in cues]
ends = [en for st,en in cues]
def spoken_in(w0, w1):
    i0 = bisect.bisect_left(ends, w0)
    s = 0.0
    for st,en in cues[i0:]:
        if st >= w1: break
        s += min(en,w1) - max(st,w0)
    return s
mx = 0; mx_t = 0
t = 0.0
while t + 60 <= total:
    v = spoken_in(t, t+60)
    if v > mx: mx = v; mx_t = t
    t += 5
print("max_rolling60_spoken=%.2fs at t=%.0fs (law<=55s)" % (mx, mx_t))

# segment boundary gaps in current assembly
bounds = [7,17,41,55,63]
for i,bi in enumerate(bounds,1):
    gap = cues[bi][0] - cues[bi-1][1]
    print("boundary seg%d->seg%d current_gap=%.2fs (need>=2s)" % (i,i+1,gap))

out = {"total_span_s": round(total,2), "spoken_total_s": round(spoken_total,2),
       "max_rolling60_spoken_s": round(mx,2), "segments": []}
for i,(a,b) in enumerate(SEG_BOUNDS,1):
    seg = cues[a-1:b]
    out["segments"].append({"seg": i, "beats": b-a+1,
        "span_s": round(seg[-1][1]-seg[0][0],2),
        "spoken_s": round(sum(en-st for st,en in seg),2)})
Path(".bs001-dd-tmp/air-budget-v1.json").write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding="utf-8")
print("saved air-budget-v1.json")
