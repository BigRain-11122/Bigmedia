# -*- coding: utf-8 -*-
"""Canonical L-card M2 render driver (em-check + subs + poster + optional mp4).

tech#177 root fix (R2287): the subs tail cue end is DERIVED from the
cards.json card end -- zero hardcoding -- plus a post-render duration
assertion, so the R2281 cross-card copy-residue class (a 3.0s DIGEST
end pasted into a 2.6s REACT card -> mp4 3.8s spec-probe FAIL) is
structurally impossible: renderer duration = max(all cue ends, all
card ends) + tail, and a tail cue end above card end inflates the mp4.

New cards call this one parametric script instead of copying a
per-card m2_em_render_rNNNN.py (historical copies stay as evidence):

    python tools/lcard_m2.py --cards-dir data/storylines/cards/MC-20261016-REACT-v22 \
        --subs-line "热点转述自知乎热榜·反应与信条皆取自虚构城市档案" \
        --tag rNNNN [--mp4]

Exit codes: 0 ok; 1 em-fit/probe/render failure (details on stdout).
tech#191 (R2331): the pool/closing sentence reuse defense
(tools/collide_scan.py) runs right after loading cards.json and before any
disk write -- a reuse hit is exit 1 with zero rendered output.
"""
import argparse
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "src", "render"))
from render_card_video import _em_cost, parse_srt  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import collide_scan  # noqa: E402

FRAME_W, MARGIN = 1080, 80
EM_FIT_FLOOR = 0.30  # zero-margin tier exclusion law (em-budget ladder)


def cost(s):
    return sum(_em_cost(ch) for ch in s)


def fmt_srt_ts(seconds):
    """Format seconds as an SRT timestamp HH:MM:SS,mmm (pure, testable)."""
    seconds = float(seconds)
    if seconds < 0:
        raise ValueError("negative timestamp: %r" % seconds)
    ms = int(round(seconds * 1000))
    h, rem = divmod(ms, 3600000)
    m, rem = divmod(rem, 60000)
    s, mm = divmod(rem, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, mm)


def build_subs(bottom_line, end):
    """Single tail cue whose end is the derived card end (zero hardcode)."""
    return "1\n00:00:00,000 --> %s\n%s\n" % (fmt_srt_ts(end), bottom_line)


def card_end_of(cfg):
    """Max card end across the timeline (L-cards are single-card today)."""
    ends = [float(c["end"]) for c in cfg["cards"]]
    if not ends:
        raise ValueError("cards.json has no cards")
    return max(ends)


def expected_duration(cfg, subs_cues):
    """Mirror of renderer duration law: max(cue ends, card ends) + tail."""
    ends = [e for _, e, _ in subs_cues] + [float(c["end"]) for c in cfg["cards"]]
    return max(ends) + float(cfg.get("tail", 0.5))


def ffprobe_duration(path):
    """Probe container duration in seconds (ffprobe on PATH)."""
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("ffprobe failed rc=%d: %s" % (
            r.returncode, r.stderr.decode("utf-8", "replace")[-300:]))
    return float(r.stdout.decode("utf-8", "replace").strip())


def main():
    ap = argparse.ArgumentParser(description="L-card M2 canonical driver")
    ap.add_argument("--cards-dir", required=True,
                    help="card directory containing cards.json")
    ap.add_argument("--subs-line", required=True,
                    help="bottom source/attribution line burned into subs")
    ap.add_argument("--tag", required=True,
                    help="round tag, e.g. r2287 (em-check filename)")
    ap.add_argument("--mp4", action="store_true",
                    help="also render the mp4 (L-card default: poster only)")
    args = ap.parse_args()

    cards_dir = os.path.abspath(args.cards_dir)
    cards_path = os.path.join(cards_dir, "cards.json")
    if not os.path.exists(cards_path):
        print("FAIL cards.json not found: %s" % cards_path)
        return 1
    dirname = os.path.basename(cards_dir)
    png = os.path.join(cards_dir, dirname + ".png")
    subs_path = os.path.join(cards_dir, "subs.srt")
    em_check = os.path.join(cards_dir, "em-check-%s.txt" % args.tag)
    mp4 = os.path.join(REPO, "output", "renders",
                       dirname.lower() + "-card.mp4")

    d = json.load(open(cards_path, encoding="utf-8"))
    lines = d["cards"][0]["lines"]

    # --- tech#191: pool/closing sentence reuse defense, BEFORE any disk
    # write. The R2285/R2321 ad-hoc scans canonized: a pool-row sentence
    # already on any historical card face, or a closing sentence already
    # used as a same-form closing, refuses the render with zero output.
    collide_violations = collide_scan.scan_cards(cards_dir)
    if collide_violations:
        for v in collide_violations:
            print("COLLIDE-FAIL: %s" % v)
        print("FAIL collide_scan refused render (tech#191 reuse defense)")
        return 1

    h1 = lines[0]
    h2s = lines[1:]
    c_h1 = cost(h1)
    costs = [(s, cost(s)) for s in h2s]

    # ladder: even steps 40..28; pick max feasible tier with >=0.30em margin
    chosen = None
    for size in range(40, 27, -2):
        budget = (FRAME_W - 2 * MARGIN) / float(size)
        worst = budget - max(c for _, c in costs)
        if worst >= EM_FIT_FLOOR:
            chosen = size
            budget_final = budget
            worst_final = worst
            break
    if chosen is None:
        print("EM-FAIL: no ladder size fits")
        return 1
    d["font"]["h2_size"] = chosen
    with open(cards_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)

    # --- tech#177 core: derive subs cue end from cards.json (zero hardcode)
    card_end = card_end_of(d)
    with open(subs_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(build_subs(args.subs_line, card_end))

    # first-run assertion BEFORE any render: tail cue must not inflate
    # duration beyond card end (R2281 incident class hard-check).
    cues = parse_srt(subs_path)
    for cs, ce, _ in cues:
        if ce > card_end + 1e-9:
            print("SUBS-TAIL-FAIL: cue end %.3fs > card end %.3fs "
                  "(duration would inflate past card end + tail)" % (ce, card_end))
            return 1
    exp_dur = expected_duration(d, cues)

    out = ["em-check-%s (%s M2 front-fit, ladder even-steps, canonical "
           "lcard_m2.py)" % (args.tag, dirname)]
    out.append("h2_size=%d budget=%.2fem" % (chosen, budget_final))
    for s, c in costs:
        m = budget_final - c
        out.append("%s %6.2fem margin %+6.2f  %s" %
                   ("OK " if m >= 0 else "NG ", c, m, s))
    out.append("H1=%.2fem (h1 own face, h1_size=%d)" % (c_h1, d["font"]["h1_size"]))
    c_subs = cost(args.subs_line)
    subs_budget = (FRAME_W - 2 * MARGIN) / float(d["font"]["subs_size"])
    out.append("subs %.2fem < %.2fem budget %s" %
               (c_subs, subs_budget, "OK" if c_subs <= subs_budget else "NG"))
    out.append("subs tail cue end derived=card end %.3fs (zero hardcode); "
               "expected duration=%.3fs (card end + tail %.2f)" %
               (card_end, exp_dur, float(d.get("tail", 0.5))))
    ok = worst_final >= EM_FIT_FLOOR and c_subs <= subs_budget
    out.append("ALL-HORIZ: %s" % ("PASS" if ok else "FAIL"))
    report = "\n".join(out) + "\n"
    with open(em_check, "w", encoding="utf-8", newline="\n") as f:
        f.write(report)
    print(report)
    if not ok:
        return 1

    r = subprocess.run(
        [sys.executable, os.path.join("src", "render", "render_card_video.py"),
         "--cards", cards_path, "--poster", png], capture_output=True)
    print("poster render rc=%d" % r.returncode)
    if r.returncode != 0:
        print(r.stdout.decode("utf-8", "replace")[-800:])
        print(r.stderr.decode("utf-8", "replace")[-800:])
        return 1
    print("poster: %s (%d bytes)" % (png, os.path.getsize(png)))

    if args.mp4:
        os.makedirs(os.path.dirname(mp4), exist_ok=True)
        r2 = subprocess.run(
            [sys.executable, os.path.join("src", "render", "render_card_video.py"),
             "--cards", cards_path, "--out", mp4], capture_output=True)
        print("mp4 render rc=%d" % r2.returncode)
        if r2.returncode != 0:
            print(r2.stdout.decode("utf-8", "replace")[-800:])
            print(r2.stderr.decode("utf-8", "replace")[-800:])
            return 1
        # post-render duration assertion BEFORE the S2 spec probe: the
        # mp4 must equal card end + tail within one frame of slack.
        act = ffprobe_duration(mp4)
        if abs(act - exp_dur) > 0.05:
            print("DUR-FAIL: mp4 %.3fs != expected %.3fs "
                  "(card end %.3f + tail)" % (act, exp_dur, card_end))
            return 1
        print("mp4: %s (%d bytes, %.3fs == expected %.3fs)" % (
            mp4, os.path.getsize(mp4), act, exp_dur))
    return 0


if __name__ == "__main__":
    sys.exit(main())
