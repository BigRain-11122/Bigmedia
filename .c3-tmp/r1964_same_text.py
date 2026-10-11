import io, sys

# same-text mechanical check: every SRT cue text must appear verbatim in the beats body (normalized)
BEATS = r"data\storylines\audio\SC-005-02-v1.beats.txt"
SRT = r"data\storylines\audio\SC-005-02-v1.srt"

with io.open(BEATS, "r", encoding="utf-8") as f:
    beats = f.read()
with io.open(SRT, "r", encoding="utf-8") as f:
    srt = f.read()

# beats body text (strip pipe headers and beat labels)
body = []
for line in beats.splitlines():
    if "|" in line:
        body.append(line.split("|", 2)[2])
body_text = "".join(body)

# parse srt cues
cues = []
cur = []
for block in srt.replace("\r\n", "\n").split("\n\n"):
    lines = [l for l in block.strip().splitlines() if l.strip()]
    if len(lines) >= 2:
        text = " ".join(lines[2:]).strip()
        if text:
            cues.append(text)

def norm(s):
    for ch in "，。：；！？、—…「」『』（）,.:;!?\"'（） ":
        s = s.replace(ch, "")
    return s

bt = norm(body_text)
miss = 0
for i, c in enumerate(cues, 1):
    if norm(c) not in bt:
        miss += 1
        print("MISS cue%02d: %s" % (i, c[:40]))
print("cues=%d miss=%d" % (len(cues), miss))
sys.exit(1 if miss else 0)
