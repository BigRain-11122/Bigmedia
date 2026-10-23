"""Duplicate-shot probe for full MV renders.

Why this exists: the v700 repair round left one item unverified - the C item
"a repeated shot must come back with a changed composition (1.34x)". A pop /
flash scan cannot answer that, because a duplicated shot is not a defect in
time, it is a repetition in content. This probe compares shot mid-frames
against each other and reports, for every near-identical pair, the plain
similarity and the best-matching zoom factor.

Method:
  * shot list = detect_cuts() from edit_craft_check (same cut set as the
    flash face, so both faces cannot disagree about where shots start).
  * one mid-frame per shot, decoded on a second stream pass at 240x136.
  * similarity = mean-subtracted cosine on a 48x27 luma grid, i.e. it answers
    "same framing and same content", not "same colours".
  * zoom search: crop the centre 1/z of frame A, resample back to the same
    grid, compare with B. z=1.34 means the second occurrence is the first
    one recomposed by a 1.34x push-in.
  * near-black frames (mean luma < BLACK_LUMA) are skipped: fades and black
    slugs are 100% similar to each other and would drown the report.

Exit code 0 = probe ran (read the report for the verdict), 2 = could not run.
"""

import argparse
import itertools
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

from edit_craft_check import detect_cuts, FLASH_PROXY_W, FLASH_PROXY_H

GRID_W, GRID_H = 48, 27
BLACK_LUMA = 24.0
ZOOM_TARGET = 1.34
ZOOM_GRID = tuple(round(1.0 + 0.02 * i, 2) for i in range(0, 51))  # 1.00-2.00
PAIR_FLOOR = 0.70     # report pairs at or above this plain similarity
MIN_SHOT_FRAMES = 6   # shorter runs are the flash face's business
INTRA_WINDOW_S = 3.0  # repeats closer than this sit in one lyric window
DUP_SIM = 0.90        # plain similarity that counts as "same framing"
ZOOM_TOL = 0.05       # |best_zoom - 1.34| within this = "recomposed"


def shots_from_cuts(cuts, total_frames):
    """[(start_frame, end_frame_exclusive)] in playback order."""
    bounds = [0] + [c + 1 for c in cuts] + [total_frames]
    out = []
    for a, b in zip(bounds, bounds[1:]):
        if b > a:
            out.append((a, b))
    return out


def grab_frames(video, indices):
    """Decode once and return {index: rgb proxy frame}."""
    wanted = set(indices)
    nbytes = FLASH_PROXY_W * FLASH_PROXY_H * 3
    cmd = ["ffmpeg", "-nostdin", "-loglevel", "error", "-i", str(video),
           "-vf", "scale=%d:%d:flags=area" % (FLASH_PROXY_W, FLASH_PROXY_H),
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL)
    got = {}
    i = 0
    try:
        while wanted:
            buf = proc.stdout.read(nbytes)
            if not buf or len(buf) < nbytes:
                break
            if i in wanted:
                got[i] = np.frombuffer(buf, dtype=np.uint8).reshape(
                    FLASH_PROXY_H, FLASH_PROXY_W, 3)
                wanted.discard(i)
            i += 1
    finally:
        try:
            proc.stdout.close()
        except OSError:
            pass
        proc.wait()
    return got


def block_grid(rgb):
    """240x136 rgb -> GRID_H x GRID_W luma, block mean."""
    luma = rgb.astype(np.float32).mean(axis=2)
    bh = FLASH_PROXY_H // GRID_H
    bw = FLASH_PROXY_W // GRID_W
    luma = luma[:bh * GRID_H, :bw * GRID_W]
    return luma.reshape(GRID_H, bh, GRID_W, bw).mean(axis=(1, 3))


def centre_crop_zoom(rgb, z):
    """Centre crop to 1/z of each side, resampled back to proxy size."""
    h, w = rgb.shape[0], rgb.shape[1]
    ch, cw = int(round(h / z)), int(round(w / z))
    top, left = (h - ch) // 2, (w - cw) // 2
    crop = rgb[top:top + ch, left:left + cw]
    ys = np.clip((np.arange(h) * ch // h), 0, ch - 1)
    xs = np.clip((np.arange(w) * cw // w), 0, cw - 1)
    return crop[ys][:, xs]


def sim(a, b):
    """Mean-subtracted cosine similarity on the luma grid."""
    a = a - a.mean()
    b = b - b.mean()
    na = float(np.sqrt((a * a).sum()))
    nb = float(np.sqrt((b * b).sum()))
    if na < 1e-6 or nb < 1e-6:
        return 0.0
    return float((a * b).sum() / (na * nb))


def probe(video, fps=24.0, pair_floor=PAIR_FLOOR):
    video = Path(video)
    if not video.exists():
        raise SystemExit("video not on disk: %s" % video)
    cuts, _r, frames, err = detect_cuts(video, fps)
    if err:
        raise SystemExit("cut detection failed: %s" % err)
    shots = [s for s in shots_from_cuts(cuts, frames)
             if s[1] - s[0] >= MIN_SHOT_FRAMES]
    mids = [a + (b - a) // 2 for a, b in shots]
    grabbed = grab_frames(video, mids)

    recs = []
    for (a, b), mid in zip(shots, mids):
        rgb = grabbed.get(mid)
        if rgb is None:
            recs.append({"start": a, "end": b, "skipped": "frame missing"})
            continue
        grid = block_grid(rgb)
        recs.append({
            "start": a, "end": b, "mid": mid,
            "t": round(mid / fps, 3),
            "dur": round((b - a) / fps, 3),
            "luma": round(float(grid.mean()), 1),
            "grid": grid,
            "rgb": rgb,
        })

    pairs = []
    usable = [r for r in recs if "grid" in r and r["luma"] >= BLACK_LUMA]
    for x, y in itertools.combinations(usable, 2):
        plain = sim(x["grid"], y["grid"])
        if plain < pair_floor:
            continue
        best_z, best_s = 1.0, plain
        for z in ZOOM_GRID:
            s = sim(block_grid(centre_crop_zoom(x["rgb"], z)), y["grid"])
            if s > best_s:
                best_z, best_s = z, s
        pairs.append({
            "a": x["start"], "b": y["start"],
            "a_t": x["t"], "b_t": y["t"],
            "dt": round(y["t"] - x["t"], 3),
            "a_dur": x["dur"], "b_dur": y["dur"],
            "plain": round(plain, 4),
            "best_zoom": best_z,
            "best_zoom_sim": round(best_s, 4),
            "zoom_at_target": ZOOM_TARGET,
            "sim_at_target": round(
                sim(block_grid(centre_crop_zoom(x["rgb"], ZOOM_TARGET)),
                    y["grid"]), 4),
        })
    pairs.sort(key=lambda p: -p["plain"])
    for r in recs:
        r.pop("grid", None)
        r.pop("rgb", None)
    return {
        "video": str(video),
        "fps": fps,
        "frames": frames,
        "cuts": len(cuts),
        "shots_ge_min": len(shots),
        "shots_compared": len(usable),
        "pair_floor": pair_floor,
        "pairs": pairs,
    }


def _fmt(res):
    lines = ["video=%s frames=%d cuts=%d shots=%d compared=%d"
             % (res["video"], res["frames"], res["cuts"],
                res["shots_ge_min"], res["shots_compared"])]
    if not res["pairs"]:
        lines.append("duplicate pairs at or above %.2f: none"
                     % res["pair_floor"])
        return lines
    intra = [p for p in res["pairs"] if p["dt"] <= INTRA_WINDOW_S]
    cross = [p for p in res["pairs"] if p["dt"] > INTRA_WINDOW_S]
    dups = [p for p in cross if p["plain"] >= DUP_SIM]
    recomposed = [p for p in dups
                  if abs(p["best_zoom"] - ZOOM_TARGET) <= ZOOM_TOL]
    lines.append("VERDICT: cross-beat duplicates (sim >= %.2f) = %d; of them "
                 "recomposed near %.2fx = %d"
                 % (DUP_SIM, len(dups), ZOOM_TARGET, len(recomposed)))
    if dups and not recomposed:
        lines.append("  -> repeats are framed the same, NOT recomposed: "
                     "the C-item variant is absent")
    head = ("  t_a     t_b     dt     plain   bestZ  sim@Z   sim@1.34")
    lines.append("pairs >= %.2f: %d (intra-beat %d / cross-beat %d)"
                 % (res["pair_floor"], len(res["pairs"]), len(intra),
                    len(cross)))
    lines.append("cross-beat = dt > %.1fs (different lyric window):"
                 % INTRA_WINDOW_S)
    lines.append(head)
    for p in cross[:12]:
        lines.append("  %-7.3f %-7.3f %-6.3f %-7.4f %-6.2f %-7.4f %-7.4f"
                     % (p["a_t"], p["b_t"], p["dt"], p["plain"],
                        p["best_zoom"], p["best_zoom_sim"],
                        p["sim_at_target"]))
    lines.append("intra-beat repeats (same lyric window, usually one "
                 "continuous shot split by a brightness spike):")
    lines.append(head)
    for p in intra[:10]:
        lines.append("  %-7.3f %-7.3f %-6.3f %-7.4f %-6.2f %-7.4f %-7.4f"
                     % (p["a_t"], p["b_t"], p["dt"], p["plain"],
                        p["best_zoom"], p["best_zoom_sim"],
                        p["sim_at_target"]))
    return lines


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Find duplicate shots in a full render and report the "
                    "zoom factor each repeat was recomposed at.")
    ap.add_argument("--video", required=True)
    ap.add_argument("--fps", type=float, default=24.0)
    ap.add_argument("--pair-floor", type=float, default=PAIR_FLOOR)
    ap.add_argument("--json", help="write the full result as JSON here")
    args = ap.parse_args(argv)

    res = probe(args.video, args.fps, args.pair_floor)
    for line in _fmt(res):
        print(line)
    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(
            json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
        print("json=%s" % args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())