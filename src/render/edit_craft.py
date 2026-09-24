# -*- coding: utf-8 -*-
"""BigStream edit station R-E - platform-taste editing craft layer.

CEO feedback 2026-09-24: "no beat-cuts, no transitions, no effects, and
every platform has a different taste" - the live cuts were zero-craft.
Spec: docs/editing-craft-spec.md v1.0 (cut-on-voice / transition /
effect / platform profiles). Local FFmpeg only, deterministic, zero API.

Three stages, absolute timeline preserved (the text layers of R-A burn
at fixed timestamps, so the edit layer MUST NOT shift beats):

  1. segments   : each beat = one camera-treated segment cut from the
                  looped footage intermediate (zoompan ken_in/ken_out/
                  punch + optional 60ms white flash-in on hit beats);
                  d_k = span_k + F_max so the xfade algebra always has
                  enough tail (overshoot is trimmed by -t at the end).
  2. xfade chain: per-boundary fades END at the beat boundary (the new
                  card lands exactly when its transition completes);
                  hard cuts = 1-frame 0.001s xfade (bilibili knowledge
                  style) with the profile's transition/cut pattern.
  3. compose    : R-A text plan (cards + subs + AIGC notice) burned over
                  the edited background + voice mux, same encode as R-A.

Usage:
    python src/render/edit_craft.py --profile shipinhao \
        --cards output/renders/.v10-light/cards.json \
        --srt   output/renders/.v10-light/subs.srt \
        --bgvideo data/sources/footage/biggame-cockpit-vertical.mp4 \
        --audio output/renders/.v10-light/audio.mp3 --grain 7 \
        --out   output/renders/bs-001-live-A-edit-shipinhao.mp4
    --plan-only  write the edit plan JSON, render nothing (tests)

Plan JSON lands next to --out as <out>.plan.json and feeds
src/edit_craft_check.py (M4 layer 1.8).

Exit codes: 0 ok; 2 validation error; 3 ffmpeg/ffprobe missing;
            4 render failed.
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_card_video import (  # noqa: E402  (battle-tested R-A pieces)
    load_cards, parse_srt, build_render_plan)

# -- platform taste profiles (editing-craft-spec S4; hypotheses, M6) ------
# pattern: per-boundary True=transition False=hard cut (cycled k=1..n-1)
# pool: xfade transition vocabulary; fade_s: transition duration window
# hit_cap / flash: max emphasized beats; white 60ms flash-in on hits
PROFILES = {
    "shipinhao": {
        "label": "weixin channels - warm flow, all transitions",
        "pattern": [True],
        "pool": ["fade", "dissolve", "smoothleft", "smoothup", "distance"],
        "fade_s": 0.28,
        "hit_cap": 4,
        "flash": False,
    },
    "bilibili": {
        "label": "bilibili knowledge zone - hard-cut led, punchy",
        "pattern": [True, False],
        # NB: the real 2026-09-24 crash was xfade transition="cut" (plan
        # vocabulary leaking into ffmpeg - no such xfade name); "zoomin"
        # probes OK on this build and stays legal vocabulary.
        "pool": ["smoothleft", "circleopen", "rectcrop", "distance",
                 "hblur", "radial", "slideup"],
        "fade_s": 0.16,
        "hit_cap": 6,
        "flash": True,
    },
    "douyin": {
        "label": "douyin - fast, dense, strong stimuli",
        "pattern": [True, True, False, True, False],
        "pool": ["zoomin", "slideup", "circleopen", "distance", "hblur"],
        "fade_s": 0.12,
        "hit_cap": 8,
        "flash": True,
    },
}
HARD_CUT_S = 0.05       # 2-frame xfade ~= hard cut (0.001s sub-frame
                        # duration EOFs the chain - bilibili 2026-09-24
                        # render came out 11.2s, stopped at first cut)
# platform duration windows (playbook single truth; pre-flight WARN so a
# window breach surfaces BEFORE burning render minutes - platform spec
# prelaw 2026-09-24. WARN not FAIL: the bilibili deep-dive (#14) knowingly
# renders short until the content expansion is unsealed)
PROFILE_WINDOW_S = {"shipinhao": (30, 60), "bilibili": (180, 900),
                    "douyin": (15, 60)}
INTER_S = 70.0          # looped footage intermediate length (s)
SRC_OFF_MOD = 40.0      # per-segment source window offset modulus (s)
PUNCH_FRAMES = 10       # 0.35s at 30fps punch-in ramp
FPS = 30


def beat_boundaries(cfg):
    """b_0=0 ... b_n=last card end; one beat = one card = one cut."""
    cards = cfg["cards"]
    if not cards:
        raise ValueError("no cards - nothing to edit")
    b = [float(c["start"]) for c in cards[1:]]
    return [0.0] + b + [float(cards[-1]["end"])]


def build_fades(profile, n_seg):
    """Per-boundary fade list k=1..n-1: {'fade_s','type'} (type=cut|name)."""
    pat = profile["pattern"]
    fades = []
    last_type = None
    for k in range(1, n_seg):
        if pat[(k - 1) % len(pat)]:
            idx = k % len(profile["pool"])
            t = profile["pool"][idx]
            if t == last_type:                    # no consecutive same type
                t = profile["pool"][(idx + 1) % len(profile["pool"])]
            fades.append({"fade_s": profile["fade_s"], "type": t})
            last_type = t
        else:
            fades.append({"fade_s": HARD_CUT_S, "type": "cut"})
            last_type = None
    return fades


def pick_hits(cards, cap, exclude=()):
    """Deterministic hit beats: open + evenly-spaced digit beats + last;
    cards-only beats never carry punch/flash (they have no footage)."""
    skip = set(exclude)
    n = len(cards)
    digit = [i for i, c in enumerate(cards)
             if any(ch.isdigit() for ch in str(c["lines"][0]))]
    digit = [i for i in digit if i != 0 and i != n - 1 and i not in skip]
    ends = [i for i in (0, n - 1) if i not in skip]
    mid_need = max(0, cap - len(ends))
    mids = []
    if digit and mid_need:
        mids = ([digit[int(k * (len(digit) - 1) / max(mid_need - 1, 1))]
                 for k in range(mid_need)] if mid_need > 1 else digit[:1])
    seen, hits = set(), []
    for i in ends[:1] + mids + (ends[1:] if len(ends) > 1 else []):
        if i not in seen and len(hits) < cap:
            seen.add(i)
            hits.append(i)
    return sorted(hits)


def _plan_visuals(cards):
    """Validate + normalize per-beat visual declarations (footage-matching
    spec S1). All-or-nobody: one declared beat makes undeclared beats an
    error (no silent default footage = the wallpaper sin). None declared
    = legacy single-background mode (archived style, gate WARNs it)."""
    if not any(c.get("visual") for c in cards):
        return None
    vis = []
    for i, c in enumerate(cards):
        v = c.get("visual")
        if not v:
            raise ValueError("beat %d has no visual declaration "
                             "(footage-matching-spec S1: source or "
                             "cards-only, default footage banned)" % i)
        if v.get("cards-only"):
            reason = str(v.get("reason", "")).strip()
            if not reason:
                raise ValueError("beat %d cards-only without reason" % i)
            vis.append({"cards_only": True, "reason": reason, "source": None})
        else:
            src = str(v.get("source", "")).strip()
            if not src:
                raise ValueError("beat %d visual missing source" % i)
            vis.append({"cards_only": False, "reason": "",
                        "source": src})
    return vis


def pick_treatments(n_seg, hits, flat=()):
    """punch on hits; ken_in/ken_out alternating elsewhere; flat color
    for cards-only beats (declared static-by-design, gate exempts)."""
    out = []
    flat = set(flat)
    flip = False
    for i in range(n_seg):
        if i in flat:
            out.append("flat")
        elif i in hits:
            out.append("punch")
        else:
            out.append("ken_in" if not flip else "ken_out")
            flip = not flip
    return out


def plan_edit(cfg, profile_name):
    """Pure planner: edit plan for one platform profile."""
    if profile_name not in PROFILES:
        raise ValueError("unknown profile: %s (have %s)"
                         % (profile_name, sorted(PROFILES)))
    profile = PROFILES[profile_name]
    cards = cfg["cards"]
    n = len(cards)
    bounds = beat_boundaries(cfg)
    fades = build_fades(profile, n)
    vis = _plan_visuals(cards)
    matched = vis is not None
    cards_only = ([i for i in range(n) if vis[i]["cards_only"]]
                  if matched else [])
    hits = pick_hits(cards, profile["hit_cap"], exclude=cards_only)
    treat = pick_treatments(n, hits, flat=cards_only)
    f_max = profile["fade_s"]
    tail = float(cfg.get("tail", 0.5))
    spans = [bounds[k + 1] - bounds[k] for k in range(n)]
    durs = [spans[k] + f_max for k in range(n - 1)] + [spans[-1] + tail + f_max]
    segments = []
    for k in range(n):
        # flash fires AFTER the incoming transition completes - otherwise
        # it plays mid-blend and is swallowed (hit beats 3/7/11 showed no
        # YAVG spike, 2026-09-24 probe). Hard cuts land fast, transitions
        # land at fade end = exactly when the new card is fully visible.
        incoming = fades[k - 1]["fade_s"] if k > 0 else 0.0
        flash = bool(profile["flash"] and k in hits)
        segments.append({
            "idx": k,
            "src_off_s": 0.0 if matched else
            round((bounds[k] * 0.9) % SRC_OFF_MOD, 3),
            "dur_s": round(durs[k], 3),
            "treatment": treat[k],
            "hit": k in hits,
            "flash": flash,
            "flash_st_s": round(incoming, 3) if flash else 0.0,
            "cards_only": k in cards_only,
            "cards_only_reason": (vis[k]["reason"] if matched
                                  and vis[k]["cards_only"] else ""),
            "visual_source": (vis[k]["source"] if matched
                              and not vis[k]["cards_only"] else None),
        })
    ratio = (n - len(cards_only)) / float(n) if matched else 0.0
    return {
        "engine": "R-E",
        "spec": "docs/editing-craft-spec.md",
        "visual_spec": "docs/footage-matching-spec.md",
        "profile": profile_name,
        "visual_mode": "matched" if matched else "legacy",
        "visual_ratio": round(ratio, 3),
        "cards_only_beats": cards_only,
        "boundaries": [{"k": k + 1, "time_s": round(bounds[k + 1], 3),
                        "fade_s": fades[k]["fade_s"], "type": fades[k]["type"]}
                       for k in range(n - 1)],
        "segments": segments,
        "hits": hits,
        "f_max_s": f_max,
        "last_beat_end_s": round(bounds[-1], 3),
        "tail_s": tail,
        "duration_expected_s": round(bounds[-1] + tail, 3),
        "hard_cut_s": HARD_CUT_S,
    }


def _zoom_expr(treatment, n_frames):
    """zoompan z expression for one segment (single-quoted, commas safe)."""
    if treatment == "punch":
        n2 = max(n_frames - PUNCH_FRAMES, 1)
        return ("'if(lt(on,%d),1.0+0.09*on/%d,"
                "max(1.09-0.03*(on-%d)/%d,1.06))'"
                % (PUNCH_FRAMES, PUNCH_FRAMES, PUNCH_FRAMES, n2))
    if treatment == "ken_out":
        return "'max(1.06-0.06*on/%d,1.0)'" % n_frames
    return "'min(1.0+0.05*on/%d,1.05)'" % n_frames


def _run(cmd):
    try:
        run = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        print("FAIL ffmpeg not found on PATH")
        sys.exit(3)
    if run.returncode != 0:
        print("FAIL ffmpeg exit %d" % run.returncode)
        print(run.stderr[-1500:])
        return False
    return True


CARD_ONLY_BG = "0x0a0a0d"   # deep gray (human-feel era bg) for cards-only


def _resolve_src(p):
    """Repo-relative visual source paths resolve against the repo root."""
    q = Path(p)
    return q if q.is_absolute() else REPO / q


def render_segments(plan, cfg, footage, tmpdir):
    """Stage 1: one camera-treated segment per beat.

    Matched mode (footage-matching spec): each beat renders from ITS
    declared visual source (short recordings loop inside the beat);
    cards-only beats render a flat deep-gray source (declared
    static-by-design). Legacy mode keeps the single looped intermediate
    (archived wallpaper style - the gate WARNs it, new pieces must not).
    """
    w, h = int(cfg["video"]["width"]), int(cfg["video"]["height"])
    matched = plan.get("visual_mode") == "matched"
    inter = None
    if not matched:
        inter = tmpdir / "inter.mp4"
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
               "-stream_loop", "-1", "-i", str(footage),
               "-vf", "scale=%d:%d,setsar=1,fps=%d" % (w, h, FPS),
               "-t", "%.2f" % INTER_S, "-c:v", "libx264", "-preset", "veryfast",
               "-crf", "18", "-pix_fmt", "yuv420p", str(inter)]
        if not _run(cmd):
            return None
    segs = []
    for s in plan["segments"]:
        nf = int(round(s["dur_s"] * FPS))
        seg = tmpdir / ("seg%02d.mp4" % s["idx"])
        flat = matched and s.get("cards_only")
        if flat:
            cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                   "-f", "lavfi", "-i",
                   "color=c=%s:s=%dx%d:r=%d:d=%.3f"
                   % (CARD_ONLY_BG, w, h, FPS, s["dur_s"]),
                   "-vf", "setsar=1,fps=%d" % FPS, "-r", str(FPS),
                   "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                   "-pix_fmt", "yuv420p", str(seg)]
            if not _run(cmd):
                return None
            segs.append(seg)
            continue
        # setpts rebase FIRST: -ss before -i keeps input PTS at the seek
        # offset, so a segment-head fade at st=0 never fires (the bilibili
        # white flash silently vanished until this rebase, 2026-09-24).
        vf = ("setpts=PTS-STARTPTS,scale=%d:%d,setsar=1,fps=%d,"
              "zoompan=z=%s:x='iw/2-(iw/zoom)/2':y='ih/2-(ih/zoom)/2'"
              ":d=1:s=%dx%d:fps=%d"
              % (w, h, FPS, _zoom_expr(s["treatment"], nf), w, h, FPS))
        if s["flash"]:
            vf += ",fade=t=in:st=%.3f:d=0.06:color=white" % s.get("flash_st_s", 0.0)
        if matched:
            src = _resolve_src(s["visual_source"])
            if not src.exists():
                print("FAIL visual source not found (beat %d): %s"
                      % (s["idx"], src))
                return None
            cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                   "-stream_loop", "-1", "-i", str(src),
                   "-t", "%.3f" % s["dur_s"], "-vf", vf, "-r", str(FPS),
                   "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                   "-pix_fmt", "yuv420p", str(seg)]
        else:
            cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                   "-ss", "%.3f" % s["src_off_s"], "-i", str(inter),
                   "-t", "%.3f" % s["dur_s"], "-vf", vf, "-r", str(FPS),
                   "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                   "-pix_fmt", "yuv420p", str(seg)]
        if not _run(cmd):
            return None
        segs.append(seg)
    return segs


def xfade_chain(plan, segs, tmpdir, w, h):
    """Stage 2: chain per-boundary xfades (fades END at beat boundaries)."""
    n = len(segs)
    if n == 1:
        return segs[0]
    parts, prev = [], "0:v"
    for k in range(1, n):
        b = plan["boundaries"][k - 1]
        out = "v%d" % k if k < n - 1 else "vbg"
        # NB: "cut" is plan vocabulary only - ffmpeg xfade has no such
        # transition (exit 3131621040 "Not yet implemented", 2026-09-24
        # bilibili render crash). A 0.001s fade = the 1-frame hard cut.
        t = b["type"] if b["type"] != "cut" else "fade"
        parts.append("[%s][%d:v]xfade=transition=%s:duration=%.3f:"
                     "offset=%.3f[%s]"
                     % (prev, k, t, b["fade_s"], b["time_s"] - b["fade_s"],
                        out))
        prev = out
    edited = tmpdir / "edited_bg.mp4"
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    for seg in segs:
        cmd += ["-i", str(seg)]
    cmd += ["-filter_complex", ";".join(parts), "-map", "[vbg]",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-pix_fmt", "yuv420p", str(edited)]
    return edited if _run(cmd) else None


def compose(cfg, cues, edited, audio, out_path, grain, duration):
    """Stage 3: R-A text plan burned over the edited background + voice."""
    tmpdir = Path(tempfile.mkdtemp(prefix="bsedit-tail-"))
    try:
        plan = build_render_plan(cfg, cues, tmpdir, grain=grain, bg_video=True)
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
               "-i", str(edited)]
        if audio:
            cmd += ["-i", str(audio)]
        cmd += ["-filter_complex", plan["filter_text"], "-map", "[v]"]
        if audio:
            cmd += ["-map", "1:a", "-c:a", "aac", "-b:a", "192k", "-shortest"]
        cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                "-r", str(int(cfg["video"]["fps"])),
                "-t", "%.3f" % duration, str(out_path)]
        if not _run(cmd):
            return False
        return True
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description="R-E platform-taste edit station")
    ap.add_argument("--profile", required=True, choices=sorted(PROFILES))
    ap.add_argument("--cards", required=True)
    ap.add_argument("--srt", required=True)
    ap.add_argument("--bgvideo",
                    help="legacy single-background footage; unused when "
                         "cards declare per-beat visuals")
    ap.add_argument("--audio")
    ap.add_argument("--out")
    ap.add_argument("--grain", type=int, default=0)
    ap.add_argument("--plan-only", action="store_true")
    args = ap.parse_args(argv)

    try:
        cfg = load_cards(Path(args.cards))
    except ValueError as e:
        print("FAIL cards: %s" % e)
        return 2
    if not Path(args.srt).exists():
        print("FAIL srt not found: %s" % args.srt)
        return 2
    try:
        cues = parse_srt(Path(args.srt))
    except ValueError as e:
        print("FAIL srt: %s" % e)
        return 2

    plan = plan_edit(cfg, args.profile)
    win = PROFILE_WINDOW_S.get(args.profile)
    if win and not (win[0] <= plan["duration_expected_s"] <= win[1]):
        print("WARN duration %.2fs outside the %s window %d-%ds "
              "(platform spec prelaw 2026-09-24 - fix the script budget "
              "or the target platform, do not ship the breach)"
              % (plan["duration_expected_s"], args.profile, win[0], win[1]))
    if plan.get("visual_mode") != "matched" and not args.bgvideo:
        print("FAIL bgvideo required for legacy (non-matched) cards")
        return 2
    if args.bgvideo and not Path(args.bgvideo).exists():
        print("FAIL bgvideo not found: %s" % args.bgvideo)
        return 2
    meta = cfg.get("meta") or {}
    topic = str(meta.get("topic", "")).strip().lower().replace(" ", "-") or "edit"
    out_path = (Path(args.out) if args.out else
                REPO / "output" / "renders" /
                ("%s-%s-edit-%s.mp4" % (topic, "live", args.profile)))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path = Path(str(out_path) + ".plan.json")
    plan_path.write_text(json.dumps(plan, indent=1), encoding="utf-8")

    if args.plan_only:
        print("plan ok: profile=%s segments=%d boundaries=%d hits=%s -> %s"
              % (args.profile, len(plan["segments"]), len(plan["boundaries"]),
                 plan["hits"], plan_path))
        return 0

    tmpdir = Path(tempfile.mkdtemp(prefix="bsedit-"))
    try:
        segs = render_segments(plan, cfg,
                               Path(args.bgvideo) if args.bgvideo else None,
                               tmpdir)
        if segs is None:
            return 4
        w, h = int(cfg["video"]["width"]), int(cfg["video"]["height"])
        edited = xfade_chain(plan, segs, tmpdir, w, h)
        if edited is None:
            return 4
        if not compose(cfg, cues, edited, Path(args.audio) if args.audio else None,
                       out_path, args.grain, plan["duration_expected_s"]):
            return 4
        print("OK %s" % out_path)
        print("profile=%s treatments=%d transitions=%d hardcuts=%d hits=%s"
              % (args.profile, len(plan["segments"]),
                 sum(1 for b in plan["boundaries"] if b["type"] != "cut"),
                 sum(1 for b in plan["boundaries"] if b["type"] == "cut"),
                 plan["hits"]))
        print("duration_expected=%.3fs plan=%s" % (plan["duration_expected_s"],
                                                    plan_path))
        return 0
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
