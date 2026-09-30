# -*- coding: utf-8 -*-
# R690 LC-005 air-budget TTS run wrapper (absorb interrupted R689 attempt, killed at seg01)
import subprocess, io, os, sys

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
ver = sys.argv[1] if len(sys.argv) > 1 else "v3"
beats = "data/sources/lc005/voiceover-%s.beats.txt" % ver
cmd = ["python", "src/render/emotive_tts.py", "--beats", beats,
       "--voice", "zh-CN-YunyangNeural", "--out", ".lc005-tmp",
       "--cyber", "light", "--human", "42",
       "--template", ".lc004-tmp/cards.json", "--order", "LC-005-" + ver]
r = subprocess.run(cmd, cwd=ROOT, capture_output=True, timeout=600)
out = r.stdout.decode("utf-8", errors="replace")
err = r.stderr.decode("utf-8", errors="replace")
with io.open(os.path.join(ROOT, ".c3-tmp", "r690_tts_%s.txt" % ver), "w", encoding="utf-8") as f:
    f.write(out + "\n[stderr]\n" + err)
p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "default=nw=1:nk=1",
                    os.path.join(ROOT, ".lc005-tmp", "audio.mp3")], capture_output=True)
dur = p.stdout.decode("utf-8", errors="replace").strip()
print("tts %s exit=%d dur=%s" % (ver, r.returncode, dur))
