# -*- coding: utf-8 -*-
"""AI-feel gate (O-20260923-2210-bm-a: remove the AI-generated feel).

Machine-measurable proxies for the "cheap AI video" tells, checked on the
render artifacts (beats file + SRT timeline) BEFORE the human panel:

  gap gate       zero/varied gaps between cues. All-zero = TTS metronome
                 (the classic tell); near-identical gaps = machine cadence.
  pacing gate    cue-duration coefficient of variation: too low = every
                 beat the same length (template rhythm).
  prosody gate   all beats on one profile = no rise and fall at all.
  copy gate      sentence-length CV (INFO level): too uniform reads
                 machine-written even when true.

Thresholds are STATED HYPOTHESES (copy-craft anti-dogma clause applies):
calibrated on 2026-09-23 renders (v9 FAIL gap gate pre-human, v10 PASS),
to be re-validated by M6 post-launch data.

Exit codes: 0 = pass (WARN/INFO allowed); 1 = FAIL findings; 2 = bad args.
ASCII rule: source is pure ASCII; Chinese lives in the data files only.

Usage:
    python src/ai_feel_check.py --beats FILE --srt FILE [--json]
"""
import json
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "render"))

from render_card_video import parse_srt  # noqa: E402  (battle-tested SRT parser)
from emotive_tts import parse_beats  # noqa: E402  (beats contract, shared)

# -- hypothesis thresholds (M6 will confirm or falsify) --------------------
GAP_ZERO_S = 0.010        # gap below this = "no gap" (mp3 frame padding)
GAP_UNIFORM_S = 0.020      # spread below this over >=4 boundaries = uniform
DUR_CV_MIN = 0.06          # cue-duration CV below = metronome pacing
SENT_CV_INFO = 0.15        # sentence-length CV below = INFO (advisory)
MIN_BOUNDARIES = 4         # uniformity gates need at least this many


def inter_cue_gaps(cues):
    """Gaps between consecutive cues: [(start, end, text)] -> seconds."""
    return [round(cues[i + 1][0] - cues[i][1], 3) for i in range(len(cues) - 1)]


def cv(values):
    """Coefficient of variation (population sd / mean); 0.0 for n<2."""
    if len(values) < 2 or statistics.mean(values) == 0:
        return 0.0
    return statistics.pstdev(values) / statistics.mean(values)


def check(beats, cues):
    """Return findings: list of (level, code, detail). level in FAIL/WARN/PASS."""
    findings = []
    gaps = inter_cue_gaps(cues)
    if len(cues) < 2:
        findings.append(("PASS", "gaps", "single cue - nothing to check"))
    elif all(g < GAP_ZERO_S for g in gaps):
        findings.append(("FAIL", "gap-zero",
                         "all %d inter-cue gaps ~0s: zero-gap TTS metronome "
                         "(run emotive_tts with --human SEED)" % len(gaps)))
    elif len(gaps) >= MIN_BOUNDARIES and (max(gaps) - min(gaps)) < GAP_UNIFORM_S:
        findings.append(("FAIL", "gap-uniform",
                         "gaps near-identical (%.3f-%.3fs): machine cadence"
                         % (min(gaps), max(gaps))))
    else:
        findings.append(("PASS", "gaps",
                         "%d gaps, %.3f-%.3fs (varied)" % (len(gaps), min(gaps), max(gaps))))

    durations = [e - s for s, e, _ in cues]
    dcv = cv(durations)
    if len(durations) >= 2 and dcv < DUR_CV_MIN:
        findings.append(("FAIL", "pacing-metronome",
                         "cue duration CV %.3f < %.3f: every beat same length"
                         % (dcv, DUR_CV_MIN)))
    else:
        findings.append(("PASS", "pacing", "cue duration CV %.3f" % dcv))

    profiles = set(b["profile"] for b in beats)
    if len(profiles) == 1:
        findings.append(("FAIL", "prosody-flat",
                         "all %d beats on profile '%s': no rise and fall"
                         % (len(beats), profiles.pop())))
    else:
        findings.append(("PASS", "prosody",
                         "%d distinct profiles across %d beats" % (len(profiles), len(beats))))

    scv = cv([len(b["text"]) for b in beats])
    if scv < SENT_CV_INFO:
        findings.append(("WARN", "copy-uniform",
                         "sentence-length CV %.3f < %.3f: reads machine-written"
                         % (scv, SENT_CV_INFO)))
    else:
        findings.append(("PASS", "copy", "sentence-length CV %.3f" % scv))
    return findings


def main(argv):
    beats_path = srt_path = None
    as_json = False
    i = 1
    while i < len(argv):
        if argv[i] == "--beats":
            i += 1
            beats_path = argv[i]
        elif argv[i] == "--srt":
            i += 1
            srt_path = argv[i]
        elif argv[i] == "--json":
            as_json = True
        i += 1
    if not (beats_path and srt_path):
        print("usage: ai_feel_check.py --beats FILE --srt FILE [--json]")
        return 2
    try:
        beats = parse_beats(beats_path)
    except ValueError as e:
        print("FAIL beats: %s" % e)
        return 2
    try:
        cues = parse_srt(Path(srt_path))
    except ValueError as e:
        print("FAIL srt: %s" % e)
        return 2

    findings = check(beats, cues)
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
