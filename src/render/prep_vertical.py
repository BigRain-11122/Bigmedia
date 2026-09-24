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
    python src/render/prep_vertical.py --batch <dir>  # dir batch mode

Batch mode (A5): every video file in <dir> gets the same chain in one
shot. Outputs land next to their sources as <stem><suffix>.mp4
(--suffix, default -vertical; for 16:9 targets pair with --w 1920 --h
1080 and pick a suffix like -16x9). Idempotent by design: existing
outputs are skipped (--force to redo) and already-suffixed stems are
never re-processed as inputs. Replaces the x6 hand-run-per-source
routine of the matching batches.

ASCII rule: source pure ASCII. Exit codes: 0 ok; 2 bad args; 3 ffmpeg
missing/failed.
"""
import argparse
import subprocess
import sys
from pathlib import Path

W, H = 1080, 1920
VIDEO_EXTS = (".mp4", ".mov", ".mkv", ".avi", ".webm")


def build_chain(w, h):
    return ("[0:v]split=2[bg][fg];"
            "[bg]scale=%d:%d:force_original_aspect_ratio=increase,"
            "crop=%d:%d,gblur=sigma=28[b];"
            "[fg]scale=%d:%d:force_original_aspect_ratio=decrease[f];"
            "[b][f]overlay=(W-w)/2:(H-h)/2,setsar=1[v]" % (w, h, w, h, w, h))


def prep_one(src, out, w, h, fps):
    """Run the blur-pad chain once. Returns exit code (0 ok / 3 fail)."""
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
           "-i", str(src), "-vf", build_chain(w, h), "-r", str(int(fps)),
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
           "-pix_fmt", "yuv420p", str(out)]
    try:
        run = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        print("FAIL %s: ffmpeg not found on PATH" % src.name)
        return 3
    if run.returncode != 0:
        print("FAIL %s: ffmpeg exit %d" % (src.name, run.returncode))
        print(run.stderr[-800:])
        return 3
    print("OK %s (%dKB)" % (out, out.stat().st_size // 1024))
    return 0


def run_batch(folder, w, h, fps, suffix, force):
    """Prep every raw video in folder. Returns 0 / 2 bad args / 3 any fail."""
    if not folder.is_dir():
        print("FAIL batch dir not found: %s" % folder)
        return 2
    files = sorted(p for p in folder.iterdir()
                   if p.is_file() and p.suffix.lower() in VIDEO_EXTS
                   and not p.stem.endswith(suffix))
    if not files:
        print("FAIL no video files to prep in %s" % folder)
        return 2
    ok = skip = fail = 0
    for src in files:
        out = src.with_name(src.stem + suffix + ".mp4")
        if out.exists() and not force:
            print("SKIP %s (exists)" % out.name)
            skip += 1
            continue
        if prep_one(src, out, w, h, fps) == 0:
            ok += 1
        else:
            fail += 1
    print("batch: %d ok, %d skip, %d fail" % (ok, skip, fail))
    return 3 if fail else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="blur-pad canvas prep")
    ap.add_argument("--in", dest="inp",
                    help="single input file (or use --batch)")
    ap.add_argument("--out")
    ap.add_argument("--batch", help="prep every video file in this dir")
    ap.add_argument("--suffix", default="-vertical",
                    help="batch output suffix (default -vertical)")
    ap.add_argument("--force", action="store_true",
                    help="batch mode: redo existing outputs")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--w", type=int, default=W,
                    help="canvas width (platform spec prelaw 2026-09-24)")
    ap.add_argument("--h", type=int, default=H,
                    help="canvas height (16:9 targets: --w 1920 --h 1080)")
    args = ap.parse_args(argv)
    if bool(args.inp) == bool(args.batch):
        print("FAIL need exactly one of --in <file> / --batch <dir>")
        return 2
    w, h = int(args.w), int(args.h)
    if args.batch:
        return run_batch(Path(args.batch), w, h, args.fps,
                         args.suffix, args.force)
    src = Path(args.inp)
    if not src.exists():
        print("FAIL input not found: %s" % src)
        return 2
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
    return prep_one(src, out, w, h, args.fps)


if __name__ == "__main__":
    sys.exit(main())
