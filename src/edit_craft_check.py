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
                must satisfy d_k = span_k + incoming fade (cuts add 0;
                final +tail) and the expected duration must cover every
                cue. Hard cuts must blend NOTHING (fade_s = 0, true
                concat splice - A3 2026-09-24).
  frame law     (--video) segment head/mid/tail sampling - the R186
                fake-green closure (2026-10-09): rounds had verified
                head frames only, so a privacy leak living in the
                source tail flowed into finished pieces unchecked.
                Machine-checkable proxies: frame-coverage (every
                segment sampled head/mid/tail, decodable),
                frame-degenerate (footage segments must not be
                near-solid frames), frame-frozen (declared ken/punch
                segments must actually move head->tail), frame-tile
                (labeled contact sheet = mid/tail frames are always in
                the inspector's view; semantic leaks stay a human/
                multimodal call on the tile).

INDEPENDENCE LAW (group governance S10 defense #2): the spec constants
below are deliberately NOT imported from render/edit_craft.py - the
executor must not self-certify. Drift between the two files must show
up here as a FAIL, not as a silent pass.

Thresholds are STATED HYPOTHESES (M6 post-launch calibration).
Exit codes: 0 = pass (WARN/INFO allowed); 1 = FAIL findings; 2 = bad args.
ASCII rule: source is pure ASCII; Chinese lives in the data files only.

Usage:
    python src/edit_craft_check.py --plan FILE --srt FILE --profile NAME [--json]
    python src/edit_craft_check.py --plan FILE --srt FILE --profile NAME \
        --video VIDEO [--frames-out DIR] [--json]
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
HARD_CUT_FADE_S = 0.0   # A3 true splice: a hard cut must blend NOTHING
                         # (concat join). Any fade_s > 0 at a cut = the
                         # retired 2-frame 0.05s approximation = FAIL.
                         # (0.001s sub-frame was never legal either: it
                         # EOFs the xfade chain - bilibili 2026-09-24)
VISUAL_RATIO_MIN = 0.80  # footage-matching-spec S3: matched-beat share

# -- frame-sampling law constants (R186 closure; independent again) ---
FRAME_EDGE_S = 0.15      # inset from segment edges for head/tail samples
FRAME_MIN_STD = 2.0      # grayscale stddev below this = near-solid frame
FRAME_FROZEN_MAD = 1.0   # head-vs-tail mean abs diff a moving seg must beat
FROZEN_MIN_SPAN_S = 1.0  # sub-second spans carry no readable KB motion
LOOP_EDGE_S = 0.10       # wrap-crossing zone half-window (spec S4 law 3)
LOOP_MAX_CROSS = 4       # crossings sampled per segment; beyond = WARN
_DUR_CACHE = {}          # visual-source duration cache (path -> seconds)
THUMB_W = 320            # contact-sheet cell width (px)

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
        if float(c["fade_s"]) != HARD_CUT_FADE_S:
            findings.append(("FAIL", "cut-blended",
                             "hard cut fade_s=%.3f != 0 at t=%.3f: cuts "
                             "must be true concat splices, no blend frame"
                             % (float(c["fade_s"]), c["time_s"])))
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
    tail = float(plan.get("tail_s", 0.0))
    ends = [0.0] + times + [float(plan.get("last_beat_end_s", 0.0))]
    for s in segs:
        k = s["idx"]
        span = ends[k + 1] - ends[k]
        # A3 algebra: incoming fade of seg k = boundary k (cuts add 0,
        # seg 0 starts at 0); the old span+f_max blanket is retired
        inc = float(bounds[k - 1]["fade_s"]) if 1 <= k <= len(bounds) else 0.0
        want = span + inc + (tail if k == len(segs) - 1 else 0.0)
        if abs(s["dur_s"] - want) > DUR_TOL_S + 0.01:
            findings.append(("FAIL", "timeline-drift",
                             "segment %d dur %.3fs != algebra %.3fs"
                             % (k, s["dur_s"], want)))
    if segs and not any(f[1] == "timeline-drift" for f in findings):
        findings.append(("PASS", "timeline",
                         "durations satisfy the run algebra "
                         "(fade chains + true-splice cuts, beats fixed)"))
    return findings


# -- segment frame-sampling law (R186 fake-green closure) --------------
def _seg_spans(plan):
    """Absolute (idx, start, end) per segment from boundaries + last end."""
    segs = plan.get("segments") or []
    times = [float(b["time_s"]) for b in (plan.get("boundaries") or [])]
    ends = [0.0] + times + [float(plan.get("last_beat_end_s", 0.0))]
    return [(k, ends[k], ends[k + 1]) for k in range(len(segs))]


def _sample_times(start, end):
    """head / mid / tail timestamps inside one segment."""
    span = max(0.0, end - start)
    inset = min(FRAME_EDGE_S, span / 4.0)
    return [("head", start + inset),
            ("mid", start + span / 2.0),
            ("tail", end - inset)]


def _extract_frame(video, t, out_png):
    """One decoded frame at t -> out_png. True iff usable."""
    import subprocess
    cmd = ["ffmpeg", "-nostdin", "-loglevel", "error",
           "-ss", "%.3f" % t, "-i", str(video),
           "-frames:v", "1", "-y", str(out_png)]
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return p.returncode == 0 and out_png.exists() \
        and out_png.stat().st_size > 0


def _probe_duration(path):
    """Source length in s via ffprobe (cached). None = unprovable."""
    key = str(path)
    if key in _DUR_CACHE:
        return _DUR_CACHE[key]
    import subprocess
    dur = None
    try:
        p = subprocess.run(["ffprobe", "-v", "error",
                            "-show_entries", "format=duration",
                            "-of", "default=nw=1:nk=1", key],
                           capture_output=True, timeout=30)
        if p.returncode == 0:
            dur = float(p.stdout.strip())
    except (OSError, ValueError, subprocess.TimeoutExpired):
        dur = None
    if dur is not None and dur <= 0:
        dur = None
    _DUR_CACHE[key] = dur
    return dur


def _wrap_crossings(seg, start, end):
    """(sampled_times, unsampled_count, error) for a stream_loop beat.

    Law 3 (footage-matching-spec v1.1 S4) samples where the RENDER
    branch actually crosses the loop boundary (tech#23 pilot, R1834):
    plain matched plays the looped source from its head (render_segments
    passes no -ss), so plan src_off_s is dead data on that branch and
    wraps land at k*src_len; ramp segments consume the looped timeline
    through variable-speed micro-blocks (ramp_filter_complex trims at
    absolute src_off_s + block positions), so crossing times are walked
    block by block - a speed>1 block reaches the boundary EARLIER than
    the linear src_len-src_off guess (pilot: 2nd crossing 5.43s actual
    vs 6.00s linear, far outside the +-LOOP_EDGE_S zone = R196 fake
    green face). Sample the true crossing zone, never the guess.
    """
    src = seg.get("visual_source")
    if not src:
        return [], 0, None
    span = end - start
    if span <= 0:
        return [], 0, None
    dur = _probe_duration(src)
    if dur is None:
        return [], 0, "source duration unprovable: %s" % src
    if dur <= 0:
        return [], 0, "source length <= 0 (degenerate): %s" % src
    beats = []                        # beat-relative wrap times, in order
    ramp = seg.get("ramp")
    if not ramp:
        t, k = dur, 1
        while t < span - 1e-3:
            beats.append(t)
            k += 1
            t = k * dur
    else:
        off = float(seg.get("src_off_s", 0.0) or 0.0)
        t_beat = 0.0
        for b in ramp:
            a = off + float(b.get("src_start_s", 0.0) or 0.0)
            e = off + float(b.get("src_end_s", 0.0) or 0.0)
            v = float(b.get("speed", 1.0) or 1.0)
            if e <= a or v <= 0:
                continue              # degenerate block: consumes nothing
            m = int(a // dur)
            if a - m * dur > 1e-9:
                m += 1                # crossings at m*dur within [a, e)
            if m < 1:
                m = 1                 # position 0 is the segment head, not a wrap
            while m * dur < e - 1e-9:
                bt = t_beat + (m * dur - a) / v
                if bt >= span - 1e-3:
                    break
                beats.append(bt)
                m += 1
            t_beat += (e - a) / v
            if t_beat >= span - 1e-3:
                break
    if not beats:
        return [], 0, None  # beat shorter than source: no wrap occurs
    sampled = min(len(beats), LOOP_MAX_CROSS)
    times = [start + b for b in beats[:sampled]]
    return times, len(beats) - sampled, None


def check_frames(video, plan, outdir):
    """Head/mid/tail + wrap-crossing frame law on the rendered video.

    Coverage / degenerate / frozen / loop-crossing are machine proxies;
    the labeled contact sheet (tile.png) forces mid/tail and wrap-zone
    frames into the inspector's view - semantic leaks (record-through,
    privacy, dirty wraps) stay a human/multimodal call on the tile,
    never skipped again. Returns findings; writes frames/ + tile.png
    under outdir.
    """
    from PIL import Image, ImageChops, ImageDraw, ImageStat  # lazy: plan-only runs stay light

    video = Path(video)
    if not video.exists():
        return [("FAIL", "frame-video", "video not on disk: %s" % video)]
    spans = _seg_spans(plan)
    if not spans:
        return [("FAIL", "frame-coverage", "plan has no segments to sample")]
    segs = plan.get("segments") or []
    outdir = Path(outdir)
    frames_dir = outdir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    rows = []  # (idx, start, end, [(tag, img)])
    bad = []
    for idx, start, end in spans:
        cells = []
        for tag, t in _sample_times(start, end):
            png = frames_dir / ("s%02d-%s.png" % (idx, tag))
            ok = _extract_frame(video, t, png)
            img = None
            if ok:
                try:
                    img = Image.open(png)
                    img.load()
                except Exception:
                    img = None
            if img is None:
                bad.append("s%02d-%s" % (idx, tag))
            cells.append((tag, img))
        rows.append((idx, start, end, cells))

    if bad:
        findings = [("FAIL", "frame-coverage",
                     "%d/%d segment frame samples failed extraction/decode: "
                     "%s" % (len(bad), len(spans) * 3, bad[:6]))]
    else:
        findings = [("PASS", "frame-coverage",
                     "%d segments x head/mid/tail sampled" % len(spans))]

    degenerate, frozen = [], []
    for idx, start, end, cells in rows:
        seg = segs[idx] if idx < len(segs) else {}
        declared_still = seg.get("cards_only") or \
            seg.get("treatment") == "flat"
        if not declared_still and not seg.get("flash"):
            for tag, img in cells:
                if img is None:
                    continue
                std = ImageStat.Stat(img.convert("L")).stddev[0]
                if std < FRAME_MIN_STD:
                    degenerate.append("s%02d-%s(std%.1f)" % (idx, tag, std))
        if seg.get("cards_only") or seg.get("treatment") not in MOVES:
            continue
        if (end - start) < FROZEN_MIN_SPAN_S:
            continue  # sub-second span: KB motion unreadable at frame level
        head, tail = cells[0][1], cells[2][1]
        if head is None or tail is None or head.size != tail.size:
            continue  # coverage already flagged; resolution jump = motion
        mad = ImageStat.Stat(ImageChops.difference(
            head.convert("L"), tail.convert("L"))).mean[0]
        if mad <= FRAME_FROZEN_MAD:
            frozen.append("s%02d(mad %.2f)" % (idx, mad))
    if degenerate:
        findings.append(("FAIL", "frame-degenerate",
                         "near-solid frames in footage segments (stddev < "
                         "%.1f): %s" % (FRAME_MIN_STD, degenerate[:6])))
    if frozen:
        findings.append(("FAIL", "frame-frozen",
                         "declared-motion segments static head->tail (mad "
                         "<= %.1f): %s" % (FRAME_FROZEN_MAD, frozen[:6])))

    # law 3: wrap-crossing zone sampling (R196 closure; spec v1.1 S4).
    # pre/x/post at +-LOOP_EDGE_S around every stream_loop wrap - the
    # zone where a dirty source tail wraps into the render is sampled,
    # machine-checked and forced into the tile, never skipped.
    xrows, xbad, xdirty, xprobe = [], [], [], []
    xsampled, xover = 0, 0
    for idx, start, end in spans:
        seg = segs[idx] if idx < len(segs) else {}
        if not seg.get("visual_source") or seg.get("cards_only"):
            continue
        times, over, err = _wrap_crossings(seg, start, end)
        if err:
            xprobe.append("s%02d: %s" % (idx, err))
            continue
        xover += over
        xsampled += len(times)
        exempt = seg.get("treatment") == "flat" or seg.get("flash")
        for k, t in enumerate(times):
            for tag, dt in (("pre", -LOOP_EDGE_S), ("x", 0.0),
                            ("post", LOOP_EDGE_S)):
                ts = min(max(t + dt, start + 1e-3), end - 1e-3)
                png = frames_dir / ("s%02d-x%d-%s.png" % (idx, k, tag))
                img = None
                if _extract_frame(video, ts, png):
                    try:
                        img = Image.open(png)
                        img.load()
                    except Exception:
                        img = None
                if img is None:
                    xbad.append("s%02d-x%d-%s" % (idx, k, tag))
                elif not exempt:
                    std = ImageStat.Stat(img.convert("L")).stddev[0]
                    if std < FRAME_MIN_STD:
                        xdirty.append("s%02d-x%d-%s(std%.1f)"
                                      % (idx, k, tag, std))
                xrows.append((idx, k, tag, img))
    if xprobe:
        findings.append(("FAIL", "loop-cross-probe",
                         "wrap-crossing zone unprovable (untested face "
                         "must stay visible): %s" % xprobe[:4]))
    if xbad:
        findings.append(("FAIL", "loop-cross-coverage",
                         "%d wrap-crossing sample(s) failed extraction/"
                         "decode (R196 zone never skipped): %s"
                         % (len(xbad), xbad[:6])))
    if xdirty:
        findings.append(("FAIL", "loop-cross-dirty",
                         "near-solid frames inside the wrap-crossing "
                         "zone (dirty-tail wrap tell, R196): %s"
                         % xdirty[:6]))
    if xover:
        findings.append(("WARN", "loop-cross-capped",
                         "%d wrap crossing(s) beyond the %d-per-segment "
                         "cap left unsampled (visible, not silent)"
                         % (xover, LOOP_MAX_CROSS)))
    if xsampled and not xbad and not xprobe:
        findings.append(("PASS", "loop-cross",
                         "%d wrap crossing(s) sampled pre/x/post +-%.2fs "
                         "(R196 zone forced into tile)"
                         % (xsampled, LOOP_EDGE_S)))

    # labeled contact sheet: rows = head/mid/tail + one sparse row per
    # wrap-crossing sample (owning segment's column), cols = segments
    tile_path = outdir / "tile.png"
    cell_h = 0
    for _, _, _, cells in rows:
        for _, img in cells:
            if img is not None:
                cell_h = max(cell_h, int(img.height * THUMB_W / img.width))
    for _, _, _, img in xrows:
        if img is not None:
            cell_h = max(cell_h, int(img.height * THUMB_W / img.width))
    cell_h = cell_h or 120
    label_h = 14
    sheet = Image.new("RGB", (THUMB_W * len(rows),
                              (cell_h + label_h) * (3 + len(xrows))),
                      (24, 24, 24))
    draw = ImageDraw.Draw(sheet)

    def _cell(x, y, label, img):
        draw.text((x + 2, y + 1), label, fill=(255, 220, 80))
        if img is None:
            draw.rectangle([x, y + label_h, x + THUMB_W,
                            y + label_h + cell_h], fill=(60, 20, 20))
            draw.text((x + 4, y + label_h + cell_h // 2),
                      "MISSING", fill=(255, 90, 90))
        else:
            sheet.paste(img.resize((THUMB_W, cell_h)).convert("RGB"),
                        (x, y + label_h))

    for r, tag in enumerate(("head", "mid", "tail")):
        y = r * (cell_h + label_h)
        for c, (idx, _, _, cells) in enumerate(rows):
            _cell(c * THUMB_W, y, "s%02d-%s" % (idx, tag),
                  cells[r][1] if r < len(cells) else None)
    for j, (idx, k, tag, img) in enumerate(xrows):
        y = (3 + j) * (cell_h + label_h)
        _cell(idx * THUMB_W, y, "s%02d-x%d-%s" % (idx, k, tag), img)
    sheet.save(tile_path)
    findings.append(("PASS", "frame-tile",
                     "contact sheet (head/mid/tail + %d wrap-crossing "
                     "row(s)): %s" % (len(xrows), tile_path)))
    return findings


def main(argv):
    plan_path = srt_path = profile = video_path = frames_out = None
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
        elif argv[i] == "--video":
            i += 1
            video_path = argv[i]
        elif argv[i] == "--frames-out":
            i += 1
            frames_out = argv[i]
        elif argv[i] == "--json":
            as_json = True
        i += 1
    if not (plan_path and srt_path and profile):
        print("usage: edit_craft_check.py --plan FILE --srt FILE "
              "--profile NAME [--video VIDEO [--frames-out DIR]] [--json]")
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
    if video_path:
        out = frames_out or str(Path(video_path).parent /
                                (".frame-probe-" + Path(video_path).stem))
        findings += check_frames(video_path, plan, out)
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
