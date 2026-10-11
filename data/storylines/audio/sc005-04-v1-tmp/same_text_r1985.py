import io, re, sys

BS = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
beats_path = BS + r"\data\storylines\audio\SC-005-04-v1.beats.txt"
srt_path = BS + r"\data\storylines\audio\sc005-04-v1-tmp\subs.srt"

beats = []
with io.open(beats_path, encoding="utf-8") as f:
    for ln in f:
        ln = ln.strip()
        if not ln:
            continue
        parts = [x.strip() for x in ln.split("|")]
        if len(parts) >= 3:
            beats.append((parts[0], parts[1], parts[2]))

cues = []
with io.open(srt_path, encoding="utf-8") as f:
    content = f.read()
for b in re.split(r"\n\s*\n", content.strip()):
    lines = [x for x in b.splitlines() if x.strip()]
    if len(lines) >= 2:
        cues.append("".join(lines[2:]).strip() if len(lines) > 2 else "")

print("beats=%d cues=%d" % (len(beats), len(cues)))
miss = 0
for i, (prof, title, text) in enumerate(beats):
    if i >= len(cues):
        print("MISS beat %d has no cue" % i)
        miss += 1
        continue
    if cues[i] != text:
        print("BEAT %d DIFF (%s / %s)" % (i, prof, title))
        print("  beats: %r" % text[:100])
        print("  cue  : %r" % cues[i][:100])
        miss += 1
print("same_text_result=%d/%d miss=%d" % (len(beats) - miss, len(beats), miss))
sys.exit(1 if miss else 0)
