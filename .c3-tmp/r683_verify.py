# -*- coding: utf-8 -*-
# R683 LC-003 final verify: M1 recheck on v5 + subs cue count + cards meta + dur
import subprocess, io, os, re, json

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
L = []

r = subprocess.run(["python", "src/plain_language_check.py", "--beats",
                    "data/sources/lc003/voiceover-v5.beats.txt"],
                   cwd=ROOT, capture_output=True, timeout=120)
L.append("M1 v5: exit=%d" % r.returncode)
L.append(r.stdout.decode("utf-8", errors="replace").strip())

srt = os.path.join(ROOT, ".lc003-tmp", "subs.srt")
txt = io.open(srt, encoding="utf-8").read()
cues = len(re.findall(r"^\d+\s*$", txt, re.M))
L.append("subs cues: %d" % cues)

cj = json.load(io.open(os.path.join(ROOT, ".lc003-tmp", "cards.json"), encoding="utf-8"))
L.append("cards meta.order: %s" % cj["meta"].get("order"))
L.append("cards meta.beats: %s" % cj["meta"].get("beats"))
L.append("cards n: %d" % len(cj["cards"]))
last = cj["cards"][-1]
L.append("last card end: %.2f" % last["end"])

p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "default=nw=1:nk=1",
                    os.path.join(ROOT, ".lc003-tmp", "audio.mp3")], capture_output=True)
L.append("audio dur: %s" % p.stdout.decode().strip())

# spoken char count (v5, punctuation stripped)
bt = io.open(os.path.join(ROOT, "data", "sources", "lc003", "voiceover-v5.beats.txt"), encoding="utf-8").read()
spoken = [ln.split("|")[2].strip() for ln in bt.splitlines() if "|" in ln]
chars = sum(len(re.sub(r"[，。：；、！？·—《》「」（）\s]", "", s)) for s in spoken)
L.append("v5 spoken chars (no punct): %d" % chars)

io.open(os.path.join(ROOT, ".c3-tmp", "r683_verify.txt"), "w", encoding="utf-8").write("\n".join(L))
print("OK")
