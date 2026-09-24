# R199 diagnostic: measure compose-stage command-line length for the DD
# 69-beat piece. Hypothesis: subprocess list->command line exceeds the
# 32767-char CreateProcess limit at the compose stage (69 drawtext entries
# with long temp-path textfiles), surfacing as FileNotFoundError in _run.
# Pure measurement - no ffmpeg invocation. ASCII source (encoding law).
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "render"))
from render_card_video import build_render_plan, parse_srt, load_cards

cards_path = REPO / "data" / "sources" / "bs001-dd" / "cards-dd-v1-matched-16x9.json"
srt_path = REPO / ".bs001-dd-tmp" / "subs.srt"
audio_path = REPO / ".bs001-dd-tmp" / "audio.mp3"

cfg = load_cards(cards_path)
cues = parse_srt(srt_path)
tmpdir = Path(tempfile.mkdtemp(prefix="bsprobe-"))
try:
    plan = build_render_plan(cfg, cues, tmpdir, grain=0, bg_video=True)
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
           "-i", "edited_bg.mp4", "-i", str(audio_path)]
    cmd += ["-filter_complex", plan["filter_text"], "-map", "[v]",
            "-map", "1:a", "-c:a", "aac", "-b:a", "192k", "-shortest",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-r", "30",
            "-t", "473.400", "out.mp4"]
    cmdline = subprocess.list2cmdline(cmd)
    print("filter_complex chars: %d" % len(plan["filter_text"]))
    print("total cmdline chars: %d" % len(cmdline))
    print("LIMIT: 32767 -> %s" % ("EXCEEDED" if len(cmdline) > 32767 else "within limit"))
finally:
    import shutil
    shutil.rmtree(tmpdir, ignore_errors=True)
