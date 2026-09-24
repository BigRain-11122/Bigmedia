# -*- coding: utf-8 -*-
"""Vertical blur-pad preprocessor (footage-matching-spec S2).

Any landscape/odd-ratio recording -> 1080x1920 vertical: blurred
scaled-to-fill background + original-ratio foreground centered. This is
the standard pre-R-E format so every per-beat source matches the frame
without distortion (the old single-bg pipeline pre-padded once by hand;
the matching workflow makes it a station step).

Usage:
    python src/render/prep_vertical.py --in raw.mp4 --out vertical.mp4
    python src/render/prep_vertical.py --in raw.mp4   # dry-run probe

ASCII rule: source pure ASCII. Exit codes: 0 ok; 2 bad args; 3 ffmpeg
missing/failed.
"""
import argparse
import subprocess
import sys
from pathlib import Path

W, H = 1080, 1920
CHAIN = (
    "[0:v]split=2[bg][fg];"
    "[bg]scale=%d:%d:force_original_aspect_ratio=increase,"
    "crop=%d:%d,gblur=sigma=28[b];"
    "[fg]scale=%d:%d:force_original_aspect_ratio=decrease[f];"
    "[b][f]overlay=(W-w)/2:(H-h)/2,setsar=1[v]" % (W, H, W, H, W, H)
)


def main(argv=None):
    ap = argparse.ArgumentParser(description="blur-pad canvas prep")
    ap.add_argument("--in", required=True, dest="inp")
    ap.add_argument("--out")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--w", type=int, default=W,
                    help="canvas width (platform spec prelaw 2026-09-24)")
    ap.add_argument("--h", type=int, default=H,
                    help="canvas height (16:9 targets: --w 1920 --h 1080)")
    args = ap.parse_args(argv)
    w, h = int(args.w), int(args.h)
    src = Path(args.inp)
    if not src.exists():
        print("FAIL input not found: %s" % src)
        return 2
    chain = ("[0:v]split=2[bg][fg];"
             "[bg]scale=%d:%d:force_original_aspect_ratio=increase,"
             "crop=%d:%d,gblur=sigma=28[b];"
             "[fg]scale=%d:%d:force_original_aspect_ratio=decrease[f];"
             "[b][f]overlay=(W-w)/2:(H-h)/2,setsar=1[v]" % (w, h, w, h, w, h))
    out = Path(args.out) if args.out else src.with_name(
        src.stem + "-vertical.mp4")
    if not args.out:
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height",
             "-of", "default=noprint_wrappers=1", str(src)],
            capture_output=True, text=True)
        print("dry-run: %s %s -> would write %s" % (src, probe.stdout.strip(),
                                                    out))
        return 0
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
           "-i", str(src), "-vf", chain, "-r", str(int(args.fps)),
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
           "-pix_fmt", "yuv420p", str(out)]
    try:
        run = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        print("FAIL ffmpeg not found on PATH")
        return 3
    if run.returncode != 0:
        print("FAIL ffmpeg exit %d" % run.returncode)
        print(run.stderr[-800:])
        return 3
    print("OK %s (%dKB)" % (out, out.stat().st_size // 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
