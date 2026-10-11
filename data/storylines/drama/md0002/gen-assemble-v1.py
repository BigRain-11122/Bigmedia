#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MD-0002 assembly leg (pre-staged turnkey, R1955).

Consumes voice-v1.json (the assembly-leg consumption source per R1954:
13 shot segments with measured durations) and builds the drama-ep draft:

  frames (T2I output or PIL placeholders) -> Ken Burns per-shot segments
  -> concat -> subtitle burn (text-precise SRT cues, R1943 precedent)
  -> AIGC constant mark (D-BS-03 4.5 mechanical bracket, white@0.9)
  -> mux with gap-solved audio timeline (drama-ep law, tech#7
     LAW_PROFILES: total window [60,90]s, scene-cut gap floor 1.2s
     + 0.3s seeded jitter, tail hold).

T2I leg is gated (tech#29: CEO nod + GPU window). Until the real frames
land this tool validates the FULL chain on CPU with --placeholder frames
(PIL solid cards: shot number + scene name). Once frames/shotNN.png exist
the same one command renders the draft with real art - zero rework.

Law teeth: episode total outside [60.0, 90.0]s -> exit 1 before render.
"""

import argparse
import json
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
VOICE = os.path.join(HERE, "voice-v1.json")
AUDIO_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "audio"))
FONT = r"C:\Windows\Fonts\msyh.ttc"
FONT_BD = r"C:\Windows\Fonts\msyhbd.ttc"


def _fpath(p):
    """Escape a path for a filtergraph option value (Windows drive colon)."""
    return str(p).replace("\\", "/").replace(":", "\\:")


def _q(p):
    return "'" + _fpath(p) + "'"

WINDOW_MIN_S, WINDOW_MAX_S = 60.0, 90.0   # drama-ep law (charter)
GAP_BASE_S, GAP_SPREAD_S = 1.2, 0.3       # scene-cut floor + seeded jitter
TAIL_HOLD_S = 1.5                         # end hold after last speech
FPS = 24
AIGC_MARK = "[AIGC\u00b7AI \u751f\u6210\u5185\u5bb9]"  # U+00b7 middle dot


def run(cmd):
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        sys.stderr.write(p.stderr.decode("utf-8", "replace")[-2000:] + "\n")
        raise SystemExit("ffmpeg failed: " + " ".join(cmd[:6]) + "...")
    return p


def probe_duration(path):
    p = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path], capture_output=True)
    return float(p.stdout.decode().strip())


def build_timeline(shots, seed):
    """Return (offsets, spans, gaps, total). Span_k = speech_k + trailing
    gap; last shot's trailing gap = tail hold. Gaps seeded-jittered."""
    rng = random.Random(seed)
    gaps = [round(GAP_BASE_S + rng.random() * GAP_SPREAD_S, 3)
            for _ in range(len(shots) - 1)]
    offsets, spans, t = [], [], 0.0
    for i, s in enumerate(shots):
        offsets.append(round(t, 3))
        trail = gaps[i] if i < len(shots) - 1 else TAIL_HOLD_S
        spans.append(round(s["duration_s"] + trail, 3))
        t += s["duration_s"] + trail
    return offsets, spans, gaps, round(t, 3)


def write_srt(shots, offsets, path):
    def ts(t):
        h = int(t // 3600); m = int(t % 3600 // 60); sec = t % 60
        return "%02d:%02d:%06.3f" % (h, m, sec)
    lines = []
    for i, s in enumerate(shots):
        end = offsets[i] + s["duration_s"]
        lines.append("%d\n%s --> %s\n%s\n" % (i + 1, ts(offsets[i]), ts(end), s["line"]))
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def placeholder_frame(shot, w, h, path):
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (w, h), (26, 30, 38))
    d = ImageDraw.Draw(img)
    f_big = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 88)
    f_mid = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 44)
    f_sml = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 30)
    d.text((w // 2, h // 2 - 120), "shot %02d" % shot["id"], font=f_big,
           fill=(140, 150, 165), anchor="mm")
    d.text((w // 2, h // 2 + 10), shot["scene"], font=f_mid,
           fill=(90, 98, 112), anchor="mm")
    d.text((w // 2, h // 2 + 90), shot["speaker"], font=f_sml,
           fill=(70, 78, 92), anchor="mm")
    d.rectangle([8, 8, w - 8, h - 8], outline=(45, 50, 60), width=2)
    img.save(path)


def render(tmp, shots, offsets, spans, total, frames_dir, w, h, out,
           placeholder, aigc_textfiles, aigc_mark_file):
    seg_v, seg_a = [], []
    for i, s in enumerate(shots):
        fp = os.path.join(frames_dir, "shot%02d.png" % s["id"])
        if placeholder:
            fp = os.path.join(tmp, "ph%02d.png" % s["id"])
            placeholder_frame(s, w, h, fp)
        n = max(2, int(round(spans[i] * FPS)))
        seg = os.path.join(tmp, "v%02d.mp4" % s["id"])
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", fp,
             "-vf", ("zoompan=z='1+0.045*on/%d':d=%d:x='iw/2-(iw/zoom/2)'"
                     ":y='ih/2-(ih/zoom/2)':s=%dx%d:fps=%d"
                     % (n - 1, n, w, h, FPS)),
             "-frames:v", str(n), "-pix_fmt", "yuv420p",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", seg])
        seg_v.append(seg)
        ap = os.path.join(tmp, "a%02d.mp3" % s["id"])
        run(["ffmpeg", "-y", "-loglevel", "error",
             "-i", os.path.join(AUDIO_DIR, "MD-0002-voice-v1-shot%02d.mp3" % s["id"]),
             "-af", "apad=pad_dur=%.3f" % (spans[i] - s["duration_s"]),
             "-ar", "24000", "-ac", "1", "-c:a", "libmp3lame", "-b:a", "96k", ap])
        seg_a.append(ap)
    # concat video
    vc = os.path.join(tmp, "video.mp4")
    lst = os.path.join(tmp, "v.txt")
    with open(lst, "w", encoding="ascii", newline="\n") as f:
        for p in seg_v:
            f.write("file '%s'\n" % p.replace("\\", "/"))
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", lst, "-c", "copy", vc])
    # concat audio (padded segments -> full timeline)
    ac = os.path.join(tmp, "audio.mp3")
    lst = os.path.join(tmp, "a.txt")
    with open(lst, "w", encoding="ascii", newline="\n") as f:
        for p in seg_a:
            f.write("file '%s'\n" % p.replace("\\", "/"))
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", lst, "-ar", "24000", "-ac", "1", ac])
    # final pass: subs (drawtext per cue) + AIGC constant mark + mux
    chain = "[0:v]"
    for i, tf in enumerate(aigc_textfiles):
        chain += ("drawtext=expansion=none:fontfile=%s:textfile=%s"
                  ":fontsize=%d:fontcolor=white:borderw=2:bordercolor=black@0.6"
                  ":x=(w-text_w)/2:y=h-160:line_spacing=10"
                  ":enable='between(t,%.3f,%.3f)',"
                  % (_q(FONT), _q(tf), 34,
                     offsets[i], offsets[i] + shots[i]["duration_s"] + 0.25))
    chain += ("drawtext=expansion=none:fontfile=%s:textfile=%s:fontsize=22"
              ":fontcolor=white:alpha=0.9:x=w-text_w-24:y=20[vout]"
              % (_q(FONT_BD), _q(aigc_mark_file)))
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", vc, "-i", ac,
         "-filter_complex", chain, "-map", "[vout]", "-map", "1:a",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
         "-c:a", "aac", "-b:a", "112k", "-shortest", out])
    return probe_duration(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="MD-0002 assembly leg turnkey")
    ap.add_argument("--frames-dir", default=os.path.join(HERE, "frames"),
                    help="T2I output dir with shotNN.png (default: frames/)")
    ap.add_argument("--placeholder", action="store_true",
                    help="CPU validation mode: PIL placeholder frames")
    ap.add_argument("--seed", type=int, default=7306, help="gap jitter seed")
    ap.add_argument("--width", type=int, default=1216)
    ap.add_argument("--height", type=int, default=684,
                    help="even height (yuv420p); MD-0001 PACK was 1216x683")
    ap.add_argument("--out", default=None, help="output mp4 (gitignored)")
    args = ap.parse_args(argv)

    with open(VOICE, encoding="utf-8") as f:
        v = json.load(f)
    shots = v["shots"]
    offsets, spans, gaps, total = build_timeline(shots, args.seed)
    if not (WINDOW_MIN_S <= total <= WINDOW_MAX_S):
        print("FAIL: episode total %.2fs outside drama-ep window [%.0f,%.0f]"
              % (total, WINDOW_MIN_S, WINDOW_MAX_S))
        return 1

    srt_path = os.path.join(HERE, "MD-0002-v1.srt")
    write_srt(shots, offsets, srt_path)

    if args.out is None:
        args.out = os.path.join(HERE, "draft", "MD-0002-v1-draft.mp4")
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    tmp = tempfile.mkdtemp(prefix="md0002_asm_")
    try:
        tf = []
        for i, s in enumerate(shots):
            p = os.path.join(tmp, "cue%02d.txt" % s["id"])
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(s["line"])
            tf.append(p)
        am = os.path.join(tmp, "aigc-mark.txt")
        with open(am, "w", encoding="utf-8", newline="\n") as f:
            f.write(AIGC_MARK)
        dur = render(tmp, shots, offsets, spans, total, args.frames_dir,
                     args.width, args.height, args.out, args.placeholder, tf, am)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    report = {
        "piece": v["meta"]["piece"],
        "leg": "assemble-v1 (turnkey, %s frames)"
               % ("placeholder" if args.placeholder else "T2I"),
        "total_s": round(total, 2), "rendered_s": round(dur, 2),
        "window": [WINDOW_MIN_S, WINDOW_MAX_S],
        "window_verdict": "PASS" if WINDOW_MIN_S <= dur <= WINDOW_MAX_S else "FAIL",
        "shots": len(shots), "cues_srt": len(shots),
        "gaps_s": gaps, "tail_hold_s": TAIL_HOLD_S,
        "srt": "data/storylines/drama/md0002/MD-0002-v1.srt",
        "out_mp4": args.out,
        "aigc_mark": AIGC_MARK,
    }
    rp = os.path.join(HERE, "assemble-validate-v1.txt")
    with open(rp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    print("ASSEMBLY-OK total=%.2fs rendered=%.2fs shots=%d -> %s"
          % (total, dur, len(shots), args.out))
    print("WINDOW: %s [%.0f,%.0f] | SRT cues=%d | report=%s"
          % (report["window_verdict"], WINDOW_MIN_S, WINDOW_MAX_S,
             len(shots), rp))
    return 0 if report["window_verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
