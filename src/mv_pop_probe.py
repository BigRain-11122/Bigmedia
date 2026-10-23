"""Single-frame pop probe for rendered MV cuts (read-only).

Given an mp4 and candidate timestamps, extract N-1/N/N+1 frames at a small
proxy size and compute an outlier ratio:

    d1 = |f(N) - f(N-1)|, d2 = |f(N+1) - f(N)|, d3 = |f(N+1) - f(N-1)|
    outlier = (d1 + d2 - d3) / (d1 + d2)

outlier -> 1 means frame N is a one-frame pop; -> 0 means the change at N is a
genuine cut (the neighbours still differ by d3).

The ratio alone is not enough: inside a near-static shot the absolute differences
d1/d2 can be a few hundred (film grain / flame flicker) while d3 is smaller, which
pushes the ratio high on an invisible change. So a pop must also clear an absolute
magnitude gate (--min-abs, default 20000 raw rgb24 delta units; a real cut in
these 1344x768 renders measures in the millions).

Usage:
    python src/mv_pop_probe.py --video X.mp4 --times 17.5,44.0,77.333
    python src/mv_pop_probe.py --video X.mp4 --repair-json X.mp4.repair.json

Output is one JSON object per run on stdout (never modified sources).
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

W, H = 240, 136
FRAME_BYTES = W * H * 3


def _extract3(video: str, t: float, fps: float) -> list[bytes]:
    """Return [N-1, N, N+1] raw rgb24 frames around frame round(t*fps)."""
    frame = round(t * fps)
    start = max(frame - 1, 0) / fps
    cmd = [
        "ffmpeg", "-v", "error", "-nostdin",
        "-ss", f"{start:.6f}", "-i", video,
        "-frames:v", "3",
        "-vf", f"scale={W}:{H}:flags=area",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
    ]
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace")[:400])
    buf = proc.stdout
    return [buf[i:i + FRAME_BYTES] for i in range(0, len(buf) - FRAME_BYTES + 1, FRAME_BYTES)]


def _mad(a: bytes, b: bytes) -> int:
    return sum(abs(x - y) for x, y in zip(a, b))


def probe(video: str, times: list[float], fps: float = 24.0, min_abs: int = 20000) -> list[dict]:
    rows = []
    for t in times:
        try:
            frames = _extract3(video, t, fps)
        except RuntimeError as exc:
            rows.append({"t": round(t, 3), "error": str(exc)})
            continue
        if len(frames) < 3:
            rows.append({"t": round(t, 3), "error": f"only {len(frames)} frame(s) decoded"})
            continue
        f0, f1, f2 = frames[-3:]
        d1 = _mad(f1, f0)
        d2 = _mad(f2, f1)
        d3 = _mad(f2, f0)
        den = d1 + d2
        outlier = round((den - d3) / den, 4) if den else 0.0
        visible = den >= min_abs
        rows.append({
            "t": round(t, 3),
            "frame": round(t * fps),
            "outlier": outlier,
            "delta": den,
            "visible": visible,
            "pop": outlier > 0.55 and visible,
            "d1": d1, "d2": d2, "d3": d3,
        })
    return rows


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--times", default="")
    ap.add_argument("--repair-json", default="")
    ap.add_argument("--fps", type=float, default=24.0)
    ap.add_argument("--min-abs", type=int, default=20000,
                    help="raw rgb24 delta gate; below it a frame is treated as invisible change")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.video):
        print(json.dumps({"error": f"video not found: {args.video}"}), file=sys.stderr)
        return 2

    times: list[float] = []
    if args.repair_json:
        with open(args.repair_json, encoding="utf-8") as fh:
            times = [float(x) for x in json.load(fh).get("pops", [])]
    if args.times:
        times += [float(x) for x in args.times.split(",") if x.strip()]
    if not times:
        print(json.dumps({"error": "no --times and no --repair-json pops"}), file=sys.stderr)
        return 2

    rows = probe(args.video, times, args.fps, args.min_abs)
    hit = [r for r in rows if r.get("pop")]
    print(json.dumps({
        "video": os.path.basename(args.video),
        "min_abs": args.min_abs,
        "rows": rows,
        "pops_over_0.55": len(hit),
        "max_outlier": max((r.get("outlier", 0) for r in rows), default=0),
        "max_visible_outlier": max((r.get("outlier", 0) for r in rows if r.get("visible")), default=0),
    }, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))