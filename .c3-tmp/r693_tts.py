# -*- coding: utf-8 -*-
# R693 LC-006 air-budget TTS run wrapper (LC-005 r690_tts.py pattern)
import subprocess, io, os, sys

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
ver = sys.argv[1] if len(sys.argv) > 1 else "v1"
beats = "data/sources/lc006/voiceover-%s.beats.txt" % ver
cmd = ["python", "src/render/emotive_tts.py", "--beats", beats,
       "--voice", "zh-CN-YunyangNeural", "--out", ".lc006-tmp",
       "--cyber", "light", "--human", "42",
       "--template", ".lc005-tmp/cards.json", "--order", "LC-006-" + ver]
r = subprocess.run(cmd, cwd=ROOT, capture_output=True, timeout=600)
out = r.stdout.decode("utf-8", errors="replace")
err = r.stderr.decode("utf-8", errors="replace")
with io.open(os.path.join(ROOT, ".c3-tmp", "r693_tts_%s.txt" % ver), "w", encoding="utf-8") as f:
    f.write(out + "\n[stderr]\n" + err)
p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "default=nw=1:nk=1",
                    os.path.join(ROOT, ".lc006-tmp", "audio.mp3")], capture_output=True)
dur = p.stdout.decode("utf-8", errors="replace").strip()
print("tts %s exit=%d dur=%s" % (ver, r.returncode, dur))
