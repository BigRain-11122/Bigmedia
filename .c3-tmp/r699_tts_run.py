# -*- coding: utf-8 -*-
# R699 LC-008 air-budget TTS detached runner (machine under full fleet load,
# 5-min no-output guard killed the inline run at seg05 19:20:24).
# Usage: python .c3-tmp/r699_tts_run.py v4
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ver = sys.argv[1] if len(sys.argv) > 1 else "v4"
beats = "data/sources/lc008/voiceover-%s.beats.txt" % ver
cmd = ["python", "src/render/emotive_tts.py", "--beats", beats,
       "--voice", "zh-CN-YunyangNeural", "--out", ".lc008-tmp",
       "--cyber", "light", "--human", "42",
       "--template", ".lc007-tmp/cards.json", "--order", "LC-008-" + ver]
r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, timeout=900)
p = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                   "format=duration", "-of", "default=nw=1:nk=1",
                   str(ROOT / ".lc008-tmp" / "audio.mp3")],
                  cwd=str(ROOT), capture_output=True)
dur = p.stdout.decode("utf-8", errors="replace").strip()
log = ("TTS %s exit=%d dur=%s\n[stdout-tail]\n%s\n[stderr-tail]\n%s"
       % (ver, r.returncode, dur,
          r.stdout.decode("utf-8", errors="replace")[-600:],
          r.stderr.decode("utf-8", errors="replace")[-300:]))
(ROOT / ".c3-tmp" / ("r699_tts_%s.txt" % ver)).write_text(
    log, encoding="utf-8")
print("DONE tts %s exit=%d dur=%s" % (ver, r.returncode, dur))
