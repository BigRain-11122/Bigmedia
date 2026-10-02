import os, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = os.path.join(ROOT, "r1035_lag.txt")
L = []
def w(s=""): L.append(str(s))

heart = os.path.join(ROOT, "logs", "probe-heartbeat.txt")
BEAT_RE = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) osloop: (.+)$")
ROUND_DONE_RE = re.compile(r"round done exit=(\d+)")
beats = []
with open(heart, encoding="utf-8-sig", errors="replace") as fh:
    for line in fh:
        m = BEAT_RE.match(line.strip())
        if m:
            beats.append((m.group(1), m.group(2)))

done = [(t, m) for t, m in beats if ROUND_DONE_RE.search(m)]
w("total beats=%d done beats=%d" % (len(beats), len(done)))
w("== tail 18 raw beats ==")
for t, m in beats[-18:]:
    w("%s  %s" % (t, m[:140]))
w("== done beats since 2026-10-03 05:00 ==")
for t, m in done:
    if t >= "2026-10-03 05:00":
        w("%s  %s" % (t, m[:140]))
w("== done beats 2026-10-03 00:00..05:00 count + tail ==")
cnt = 0
for t, m in done:
    if "2026-10-03 00:00" <= t < "2026-10-03 05:00":
        cnt += 1
w("count=%d" % cnt)

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L))
print("OK total=%d done=%d" % (len(beats), len(done)))
