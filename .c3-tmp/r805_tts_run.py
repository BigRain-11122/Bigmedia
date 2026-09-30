# -*- coding: utf-8 -*-
# R805 BS-010 air-budget TTS detached runner (r802_tts_run.py lineage).
# Usage: python .c3-tmp/r805_tts_run.py v1
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ver = sys.argv[1] if len(sys.argv) > 1 else "v1"
beats = "data/sources/bs010/voiceover-%s.beats.txt" % ver
cmd = ["python", "src/render/emotive_tts.py", "--beats", beats,
       "--voice", "zh-CN-YunyangNeural", "--out", ".bs010-tmp",
       "--cyber", "light", "--human", "42",
       "--template", ".bs009-tmp/cards.json", "--order", "BS-010-" + ver]
r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, timeout=900)
p = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                   "format=duration", "-of", "default=nw=1:nk=1",
                   str(ROOT / ".bs010-tmp" / "audio.mp3")],
                  cwd=str(ROOT), capture_output=True)
dur = p.stdout.decode("utf-8", errors="replace").strip()
log = ("TTS %s exit=%d dur=%s\n[stdout-tail]\n%s\n[stderr-tail]\n%s"
       % (ver, r.returncode, dur,
          r.stdout.decode("utf-8", errors="replace")[-600:],
          r.stderr.decode("utf-8", errors="replace")[-300:]))
(ROOT / ".c3-tmp" / ("r805_tts_%s.txt" % ver)).write_text(
    log, encoding="utf-8")
print("DONE tts %s exit=%d dur=%s" % (ver, r.returncode, dur))
