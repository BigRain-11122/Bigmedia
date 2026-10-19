# -*- coding: utf-8 -*-
"""V5.11 FINAL (1344x768) verification pack.

Order 2026-10-20 00:32 row (V5.11 detached 540P proxy re-render, lane
hq-central-night-gpu) acceptance chain:
  proxy -> PROXY-PASS -> 768P final -> three-shot dense frame boards
  + PTS + transition spot-check + grade reference boards -> dual sign-off.

The proxy pack (v511_verify_pack_r2404.py, R2404) already ran on the 540P
proxy. This one runs the same machine checks against the production
master and adds the three-shot dense strips (24 fps per-frame strips, so
frozen frames / duplicated frames become visible).

Read-only with respect to the media tree: boards land under the BigStream
repo qa/ dir, never in cph4.

Usage:
    python tools/v511_final_qc.py --src <mp4> [--out qa/mv0001-v511]
Exit codes: 0 = PASS, 1 = FAIL.
"""
import argparse
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FPS = 24.0
STEP = 1.0 / FPS
TOL = 0.008

# XFS (cross-fade / splice) cut points audited in V511-GAP-AUDIT-20261019.md
CUTS = [21.900, 38.820, 40.220, 44.000, 47.500, 80.180, 102.880,
        110.520, 126.320, 131.720, 152.000, 187.260, 191.600, 227.500]

# gap-1 verse splits (1 -> 2 halves, same source)
SPLITS = [("N05", 65.4445), ("N06", 71.4940), ("R05", 129.2392), ("R06", 135.1400)]

# grade reference: amber (Babylon / stele interiors) vs cool (museum hall / night)
AMBER = [8.0, 63.0, 133.0]
COOL = [40.5, 106.0, 205.0]

# three-shot dense strips: the three cloud re-burn shots that carry the
# V5.11 fix (C03 dig reveal, D06 chisel fingertip, E03 gaze meet).
DENSE = [("C03_dig_reveal", 96.4), ("D06_chisel_fingertip", 175.6),
         ("E03_gaze_meet", 196.9)]
DENSE_FRAMES = 12


def ffprobe_json(src, entries):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", entries,
                        "-of", "json", src], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return json.loads(r.stdout or "{}")


def pts_scan(src):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "frame=pts_time", "-of", "csv=p=0",
                        src], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    ts = sorted(float(x) for x in r.stdout.replace(",", " ").split() if x.strip())
    steps = [(i, round(ts[i] - ts[i - 1], 6)) for i in range(1, len(ts))]
    bad = [(i, d) for i, d in steps if abs(d - STEP) > TOL]
    return ts, bad


def grab(src, t, dst):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "%.4f" % t, "-i", src,
                    "-frames:v", "1", "-q:v", "2", dst], check=True)
    return dst


def stack(paths, cols, dst):
    """Tile images into a grid.

    Explicit pixel coordinates, not the symbolic w0/h0 layout: ffmpeg's
    layout parser silently falls back to a 2-column grid for expressions
    like ``w0*2_0`` (verified: 4 hands of 1344x768 produced 2688x768).
    """
    w, h = 1344, 768
    inputs = []
    for p in paths:
        inputs += ["-i", p]
    n = len(paths)
    layout = "|".join("%d_%d" % ((i % cols) * w, (i // cols) * h)
                      for i in range(n))
    fc = "".join("[%d]" % i for i in range(n)) + \
        "xstack=inputs=%d:layout=%s" % (n, layout)
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + inputs +
                   ["-filter_complex", fc, "-q:v", "2", dst], check=True)
    return dst


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", default=os.path.join("qa", "mv0001-v511"))
    ap.add_argument("--label", default="V5.11")
    a = ap.parse_args()
    src = os.path.abspath(a.src)
    out = os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    tmp = os.path.join(out, "_cells")
    os.makedirs(tmp, exist_ok=True)

    meta = ffprobe_json(
        src, "format=duration,size,bit_rate:stream=codec_name,width,height,"
             "r_frame_rate,nb_frames,sample_rate,channels")
    ts, bad = pts_scan(src)
    v = next((s for s in meta.get("streams", []) if s.get("codec_name") == "h264"), {})
    au = next((s for s in meta.get("streams", []) if s.get("codec_name") == "aac"), {})

    print("==", a.label, "FINAL QC ==")
    print("file      :", src)
    print("size      : %.2f MB  bitrate %.2f Mbps" % (
        float(meta["format"]["size"]) / 1e6,
        float(meta["format"]["bit_rate"]) / 1e6))
    print("video     : %sx%s @ %s  frames=%s" % (
        v.get("width"), v.get("height"), v.get("r_frame_rate"), v.get("nb_frames")))
    print("audio     : %s %sHz %sch" % (
        au.get("codec_name"), au.get("sample_rate"), au.get("channels")))
    print("PTS       : frames=%d nonuniform=%d first=%.4f last=%.4f -> %s" % (
        len(ts), len(bad), ts[0] if ts else -1, ts[-1] if ts else -1,
        "PASS" if not bad else "FAIL"))

    boards = []

    # 1) XFS cut motion board (+/-0.21s per cut) - frozen/duplicated frame scan
    cells = []
    for i, c in enumerate(CUTS):
        cells.append(grab(src, c - 0.21, os.path.join(tmp, "x%02d_a.jpg" % i)))
        cells.append(grab(src, c + 0.21, os.path.join(tmp, "x%02d_b.jpg" % i)))
    boards.append(stack(cells, 2, os.path.join(out, "XFS-CUT-BOARD.jpg")))

    # 2) gap-1 split dense board (pre / cut / post per split)
    cells = []
    for name, c in SPLITS:
        for off, tag in ((-0.25, "a"), (0.0, "m"), (0.25, "b")):
            cells.append(grab(src, c + off, os.path.join(tmp, "s_%s_%s.jpg" % (name, tag))))
    boards.append(stack(cells, 3, os.path.join(out, "SPLIT-DENSE-BOARD.jpg")))

    # 3) grade reference board (3 amber + 3 cool)
    cells = []
    for i, t in enumerate(AMBER):
        cells.append(grab(src, t, os.path.join(tmp, "g_amber_%d.jpg" % i)))
    for i, t in enumerate(COOL):
        cells.append(grab(src, t, os.path.join(tmp, "g_cool_%d.jpg" % i)))
    boards.append(stack(cells, 3, os.path.join(out, "GRADE-DUAL-BOARD.jpg")))

    # 4) three-shot dense strips: 12 consecutive frames each (24fps steps)
    dense_rows = []
    for name, t0 in DENSE:
        row = []
        for k in range(DENSE_FRAMES):
            row.append(grab(src, t0 + k * STEP,
                            os.path.join(tmp, "d_%s_%02d.jpg" % (name, k))))
        dense_rows.append(stack(row, DENSE_FRAMES,
                                os.path.join(tmp, "strip_%s.jpg" % name)))
    boards.append(stack(dense_rows, 1, os.path.join(out, "DENSE-3SHOT.jpg")))

    pack = {
        "label": a.label,
        "file": src,
        "ffprobe": meta,
        "frames": len(ts),
        "pts_nonuniform_steps": len(bad),
        "pts_anomalies_sample": bad[:5],
        "expected_fps_step": STEP,
        "tolerance": TOL,
        "verdict": "PASS" if not bad else "FAIL",
        "boards": [os.path.basename(b) for b in boards],
        "dense_shots": [n for n, _ in DENSE],
        "note_bitrate_mbps": round(float(meta["format"]["bit_rate"]) / 1e6, 2),
    }
    pack_path = os.path.join(out, "FINAL-QC-PACK.json")
    with open(pack_path, "w", encoding="utf-8") as f:
        json.dump(pack, f, ensure_ascii=False, indent=1)

    print("boards    :", ", ".join(os.path.basename(b) for b in boards))
    print("pack      :", pack_path)
    print("VERDICT   :", pack["verdict"])
    return 0 if pack["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())