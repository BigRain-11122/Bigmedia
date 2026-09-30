# -*- coding: utf-8 -*-
# R744 LC-019 air-budget TTS detached runner (r739_tts_run.py channel:
# machine under full fleet load, 5-min no-output guard kills inline runs).
# Usage: python .c3-tmp/r744_tts_run.py v2
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ver = sys.argv[1] if len(sys.argv) > 1 else "v2"
beats = "data/sources/lc019/voiceover-%s.beats.txt" % ver
cmd = ["python", "src/render/emotive_tts.py", "--beats", beats,
       "--voice", "zh-CN-YunyangNeural", "--out", ".lc019-tmp",
       "--cyber", "light", "--human", "42",
       "--template", ".lc018-tmp/cards.json", "--order", "LC-019-" + ver]
r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, timeout=900)
p = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                   "format=duration", "-of", "default=nw=1:nk=1",
                   str(ROOT / ".lc019-tmp" / "audio.mp3")],
                  cwd=str(ROOT), capture_output=True)
dur = p.stdout.decode("utf-8", errors="replace").strip()
log = ("TTS %s exit=%d dur=%s\n[stdout-tail]\n%s\n[stderr-tail]\n%s"
       % (ver, r.returncode, dur,
          r.stdout.decode("utf-8", errors="replace")[-600:],
          r.stderr.decode("utf-8", errors="replace")[-300:]))
(ROOT / ".c3-tmp" / ("r744_tts_%s.txt" % ver)).write_text(
    log, encoding="utf-8")
print("DONE tts %s exit=%d dur=%s" % (ver, r.returncode, dur))
