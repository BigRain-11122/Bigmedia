# -*- coding: utf-8 -*-
"""Edit-craft gate (M4 layer 1.8 - CEO edit-craft order 2026-09-24).

Machine-measurable proxies for "zero editing craft", checked on the R-E
edit plan + SRT BEFORE the human panel (same entry-ticket law as the
AI-feel gate, layer 1.6). Spec: docs/editing-craft-spec.md v1.0.

  beat-align    cut boundaries must land on voice-clause edges (cue
                starts/ends) within BEAT_TOL - cuts ON the voice, not on
                a metronome. >= ALIGN_MIN of boundaries aligned.
  static-seg    every segment must carry camera movement (ken/punch);
                a static segment = the old zero-craft tell.
  transition    types must stay in the profile pool, never repeat
                back-to-back, durations inside the profile window;
                hard cuts are legal only where the profile pattern
                allows them (bilibili = hard-cut led, shipinhao = all
                transitions).
  effect        hit beats <= profile cap; flash only where the profile
                allows; hits must actually get the punch treatment.
  timeline      the edit layer must NOT shift beats: segment durations
                must satisfy d_k = span_k + f_max (final +tail) and the
                expected duration must cover every cue.

INDEPENDENCE LAW (group governance S10 defense #2): the spec constants
below are deliberately NOT imported from render/edit_craft.py - the
executor must not self-certify. Drift between the two files must show
up here as a FAIL, not as a silent pass.

Thresholds are STATED HYPOTHESES (M6 post-launch calibration).
Exit codes: 0 = pass (WARN/INFO allowed); 1 = FAIL findings; 2 = bad args.
ASCII rule: source is pure ASCII; Chinese lives in the data files only.

Usage:
    python src/edit_craft_check.py --plan FILE --srt FILE --profile NAME [--json]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "render"))

from render_card_video import parse_srt  # noqa: E402  (battle-tested parser)

# -- independent spec constants (editing-craft-spec S4/S5) --------------
BEAT_TOL_S = 0.25        # boundary-to-cue-edge tolerance (cut-on-voice)
ALIGN_MIN = 0.90         # >= this share of boundaries aligned to voice
DUR_TOL_S = 0.05         # timeline preservation tolerance
TAIL_MAX_S = 3.0         # expected duration may exceed last cue end by <=this
MOVES = ("ken_in", "ken_out", "punch")
HARD_CUT_MAX_S = 0.08    # xfade <= this reads as a hard cut (2-frame
                         # 0.05s is the floor: sub-frame 0.001 EOFs the
                         # xfade chain - bilibili render 2026-09-24)
VISUAL_RATIO_MIN = 0.80  # footage-matching-spec S3: matched-beat share

SPEC = {
    "shipinhao": {
        "fade_min_s": 0.24, "fade_max_s": 0.32,
        "pool": {"fade", "dissolve", "smoothleft", "smoothup", "distance"},
        "transition_share_min": 0.99,  # all transitions (warm flow)
        "hit_cap": 4, "flash": False,
    },
    "bilibili": {
        "fade_min_s": 0.12, "fade_max_s": 0.20,
        "pool": {"smoothleft", "circleopen", "rectcrop",
                 "distance", "hblur", "radial", "slideup"},
        "transition_share_min": 0.40,  # hard-cut led knowledge zone
        "transition_share_max": 0.60,
        "hit_cap": 6, "flash": True,
    },
    "douyin": {
        "fade_min_s": 0.08, "fade_max_s": 0.16,
        "pool": {"zoomin", "slideup", "circleopen", "distance", "hblur"},
        "transition_share_min": 0.55,
        "transition_share_max": 0.75,
        "hit_cap": 8, "flash": True,
    },
}


def _nearest_edge_dist(t, cues):
    """Distance in s from t to the nearest cue start/end edge."""
    best = None
    for s, e, _ in cues:
        for edge in (s, e):
            d = abs(t - edge)
            if best is None or d < best:
                best = d
    return best


def check(plan, cues, profile_name):
    """Return findings: [(level, code, detail)] in FAIL/WARN/PASS."""
    findings = []
    if profile_name not in SPEC:
        return [("FAIL", "profile-unknown", "no such profile: %s" % profile_name)]
    spec = SPEC[profile_name]
    bounds = plan.get("boundaries") or []
    segs = plan.get("segments") or []
    hits = set(plan.get("hits") or [])
    expected = float(plan.get("duration_expected_s", 0.0))

    # 1. cut-on-voice: boundaries land on cue edges
    if not bounds:
        findings.append(("FAIL", "no-boundaries",
                         "zero cut boundaries: single-shot, not an edit"))
    else:
        dists = [_nearest_edge_dist(b["time_s"], cues) for b in bounds]
        aligned = sum(1 for d in dists if d <= BEAT_TOL_S)
        share = aligned / float(len(bounds))
        if share < ALIGN_MIN:
            findings.append(("FAIL", "beat-misaligned",
                             "only %d/%d boundaries within +-%.2fs of a cue "
                             "edge (share %.2f < %.2f): cuts off the voice"
                             % (aligned, len(bounds), BEAT_TOL_S, share,
                                ALIGN_MIN)))
        else:
            findings.append(("PASS", "beat-align",
                             "%d/%d boundaries on cue edges (+-%.2fs)"
                             % (aligned, len(bounds), BEAT_TOL_S)))

    # 2. no static segments; hits get the punch (cards-only beats may be
    # flat color - declared static-by-design, footage-matching-spec S3)
    static = [s for s in segs
              if s.get("treatment") not in MOVES
              and not (s.get("cards_only") and s.get("treatment") == "flat")]
    if static:
        findings.append(("FAIL", "static-seg",
                         "%d segment(s) without camera movement: the "
                         "zero-craft tell" % len(static)))
    else:
        findings.append(("PASS", "camera",
                         "all %d segments move (%s)"
                         % (len(segs),
                            "/".join(sorted(set(s["treatment"] for s in segs))))))

    # 2.5 visual matching face (footage-matching-spec S1/S3/S4)
    if plan.get("visual_mode", "legacy") != "matched":
        findings.append(("WARN", "visual-legacy",
                         "single-background legacy style: footage is a "
                         "wallpaper, not per-beat evidence (matching spec)"))
    else:
        undeclared = [s["idx"] for s in segs
                      if not s.get("cards_only") and not s.get("visual_source")]
        if undeclared:
            findings.append(("FAIL", "visual-undeclared",
                             "beats without visual declaration (default "
                             "footage banned): %s" % undeclared))
        no_reason = [s["idx"] for s in segs
                     if s.get("cards_only")
                     and not str(s.get("cards_only_reason", "")).strip()]
        if no_reason:
            findings.append(("FAIL", "cards-only-no-reason",
                             "cards-only beats without reason: %s" % no_reason))
        missing = []
        for s in segs:
            if s.get("visual_source"):
                q = Path(s["visual_source"])
                q = q if q.is_absolute() else REPO / q
                if not q.exists():
                    missing.append(s["visual_source"])
        if missing:
            findings.append(("FAIL", "visual-missing-file",
                             "declared visual sources not on disk: %s"
                             % missing))
        ratio = float(plan.get("visual_ratio", 0.0))
        if ratio < VISUAL_RATIO_MIN:
            findings.append(("FAIL", "visual-ratio",
                             "matched-beat ratio %.2f < %.2f: too many "
                             "cards-only beats" % (ratio, VISUAL_RATIO_MIN)))
        else:
            findings.append(("PASS", "visual-ratio",
                             "per-beat matched footage %.2f (%d/%d beats)"
                             % (ratio, len(segs) - len(plan.get(
                                 "cards_only_beats", [])), len(segs))))
    missed = [i for i in hits
              if not any(s["idx"] == i and s["treatment"] == "punch"
                         for s in segs)]
    if missed:
        findings.append(("FAIL", "hit-no-punch",
                         "hit beats without punch treatment: %s" % missed))
    if len(hits) > spec["hit_cap"]:
        findings.append(("FAIL", "hit-over-cap",
                         "%d hits > profile cap %d" % (len(hits),
                                                       spec["hit_cap"])))
    flash_n = sum(1 for s in segs if s.get("flash"))
    if spec["flash"]:
        bad = [s["idx"] for s in segs
               if s.get("flash") and s["idx"] not in hits]
        if bad:
            findings.append(("FAIL", "flash-off-hit",
                             "white flash on non-hit beats: %s" % bad))
        elif flash_n == 0:
            findings.append(("WARN", "flash-none",
                             "profile allows hit flashes but plan has none"))
        else:
            findings.append(("PASS", "flash",
                             "%d hit flash(es) on-profile" % flash_n))
    elif flash_n:
        findings.append(("FAIL", "flash-not-allowed",
                         "%d white flash(es) on a no-flash profile" % flash_n))

    # 3. transitions: pool, no repeats, fade window, share, cut legality
    trans = [b for b in bounds if b["type"] != "cut"]
    cuts = [b for b in bounds if b["type"] == "cut"]
    if bounds:
        share = len(trans) / float(len(bounds))
        lo = spec["transition_share_min"]
        hi = spec.get("transition_share_max", 1.0)
        if share < lo or share > hi:
            findings.append(("FAIL", "transition-share",
                             "transition share %.2f outside profile window "
                             "%.2f-%.2f" % (share, lo, hi)))
        else:
            findings.append(("PASS", "transition-share",
                             "%d transitions / %d cuts (share %.2f)"
                             % (len(trans), len(cuts), share)))
    bad_pool = [b["type"] for b in trans if b["type"] not in spec["pool"]]
    if bad_pool:
        findings.append(("FAIL", "transition-pool",
                         "off-vocabulary transitions: %s" % bad_pool))
    for c in cuts:
        if float(c["fade_s"]) > HARD_CUT_MAX_S:
            findings.append(("FAIL", "cut-too-slow",
                             "hard cut fade %.3fs > %.2fs at t=%.3f"
                             % (c["fade_s"], HARD_CUT_MAX_S, c["time_s"])))
    prev = None
    for b in trans:
        if float(b["fade_s"]) < spec["fade_min_s"] or \
                float(b["fade_s"]) > spec["fade_max_s"]:
            findings.append(("FAIL", "fade-window",
                             "transition fade %.3fs outside %.2f-%.2fs at t=%.3f"
                             % (b["fade_s"], spec["fade_min_s"],
                                spec["fade_max_s"], b["time_s"])))
        if b["type"] == prev:
            findings.append(("FAIL", "transition-repeat",
                             "back-to-back '%s' at t=%.3f" % (b["type"],
                                                              b["time_s"])))
        prev = b["type"]
    if trans and not any(f[1] == "transition-repeat" for f in findings):
        findings.append(("PASS", "transition-variety",
                         "%d transitions, no back-to-back repeat" % len(trans)))

    # 4. timeline preservation: beats unshifted, durations algebra
    times = [b["time_s"] for b in bounds]
    if any(times[k + 1] <= times[k] for k in range(len(times) - 1)):
        findings.append(("FAIL", "boundary-order", "boundaries not increasing"))
    if cues and expected < max(e for _, e, _ in cues):
        findings.append(("FAIL", "duration-short",
                         "expected %.3fs < last cue end %.3fs: text would "
                         "overrun the edit" % (expected,
                                                max(e for _, e, _ in cues))))
    if cues and expected - max(e for _, e, _ in cues) > TAIL_MAX_S:
        findings.append(("WARN", "tail-bloat",
                         "expected exceeds last cue end by %.3fs"
                         % (expected - max(e for _, e, _ in cues))))
    f_max = float(plan.get("f_max_s", 0.0))
    tail = float(plan.get("tail_s", 0.0))
    ends = [0.0] + times + [float(plan.get("last_beat_end_s", 0.0))]
    for s in segs:
        k = s["idx"]
        span = ends[k + 1] - ends[k]
        want = (span + f_max) if k < len(segs) - 1 else (span + tail + f_max)
        if abs(s["dur_s"] - want) > DUR_TOL_S + 0.01:
            findings.append(("FAIL", "timeline-drift",
                             "segment %d dur %.3fs != algebra %.3fs"
                             % (k, s["dur_s"], want)))
    if segs and not any(f[1] == "timeline-drift" for f in findings):
        findings.append(("PASS", "timeline",
                         "durations satisfy the xfade algebra (beats fixed)"))
    return findings


def main(argv):
    plan_path = srt_path = profile = None
    as_json = False
    i = 1
    while i < len(argv):
        if argv[i] == "--plan":
            i += 1
            plan_path = argv[i]
        elif argv[i] == "--srt":
            i += 1
            srt_path = argv[i]
        elif argv[i] == "--profile":
            i += 1
            profile = argv[i]
        elif argv[i] == "--json":
            as_json = True
        i += 1
    if not (plan_path and srt_path and profile):
        print("usage: edit_craft_check.py --plan FILE --srt FILE "
              "--profile NAME [--json]")
        return 2
    try:
        plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("FAIL plan: %s" % e)
        return 2
    try:
        cues = parse_srt(Path(srt_path))
    except ValueError as e:
        print("FAIL srt: %s" % e)
        return 2

    findings = check(plan, cues, profile)
    fails = [f for f in findings if f[0] == "FAIL"]
    warns = [f for f in findings if f[0] == "WARN"]
    if as_json:
        print(json.dumps({"findings": [
            {"level": lv, "code": c, "detail": d} for lv, c, d in findings],
            "fail": len(fails), "warn": len(warns)}))
    else:
        for lv, code, detail in findings:
            print("[%s] %s: %s" % (lv, code, detail))
        print("SUMMARY: %d FAIL %d WARN -> %s"
              % (len(fails), len(warns), "exit 1" if fails else "pass"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
