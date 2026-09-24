# -*- coding: utf-8 -*-
"""BigStream render station R-A - card timeline renderer (m2-local-stack.md S4).

Minimal closed loop of the local compute chain: voiceover txt + SRT +
card template -> 9:16 mp4 (black background, white card text, burned
subtitles, persistent AIGC notice). Pure local, zero install: only needs
ffmpeg on PATH. CPU-only encode (libx264), no VRAM contention - safe to
run beside the Ollama resident models (shared-machine etiquette S2).

Usage:
    python src/render/render_card_video.py --cards data/sources/bs001/cards.json
    python src/render/render_card_video.py --cards ... --dry-run     # plan only
    python src/render/render_card_video.py --cards ... --audio a.wav # mux voice
    python src/render/render_card_video.py --cards ... --strict      # srt/voiceover mismatch = FAIL
    python src/render/render_card_video.py --cards ... --poster c.png # + cover frame PNG

Inputs (defaults resolve next to the cards file):
    --cards      JSON timeline template: video/font/aigc_notice/tail/cards[]. Required.
    --srt        subtitles; default <cards dir>/subs.srt
    --voiceover  plain-text script; default <cards dir>/voiceover.txt
                 (consistency check: SRT text must equal voiceover text
                 after whitespace normalization; mismatch = WARN, or FAIL
                 with --strict)

Laws enforced:
    AIGC notice is a red line (CONSTITUTION S2-4): a cards file without a
    non-empty aigc_notice is refused (exit 2) and the notice is burned
    into every frame for the full duration.
    Encoding rule: this script is pure ASCII. Chinese lives only in the
    UTF-8 data files it consumes (cards.json / srt / txt).

Exit codes: 0 ok; 2 validation/red-line error; 3 ffmpeg/ffprobe missing;
            4 render or probe failed.
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[2]

_TIME_RE = re.compile(r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})")


def norm_text(s):
    """Whitespace-insensitive comparison form (CJK-friendly)."""
    return "".join(s.split())


def _t(seconds_str):
    m = _TIME_RE.fullmatch(seconds_str.strip())
    if not m:
        raise ValueError("bad SRT time: %r" % seconds_str)
    h, mnt, sec, ms = (int(x) for x in m.groups())
    return h * 3600.0 + mnt * 60.0 + sec + ms / 1000.0


def parse_srt(path):
    """Parse SRT into ordered, non-overlapping [(start, end, text)]."""
    raw = Path(path).read_text(encoding="utf-8-sig")
    blocks = [b for b in re.split(r"\r?\n\s*\r?\n", raw.strip()) if b.strip()]
    if not blocks:
        raise ValueError("SRT file is empty: %s" % path)
    cues = []
    for i, block in enumerate(blocks, 1):
        lines = [ln for ln in block.splitlines() if ln.strip()]
        if len(lines) < 3 or not lines[0].strip().isdigit():
            raise ValueError("SRT block %d: expected index/timing/text" % i)
        if "-->" not in lines[1]:
            raise ValueError("SRT block %d: missing '-->' timing line" % i)
        left, _, right = lines[1].partition("-->")
        start, end = _t(left), _t(right)
        text = "\n".join(ln.strip() for ln in lines[2:])
        if not text:
            raise ValueError("SRT block %d: empty cue text" % i)
        cues.append((start, end, text))
    prev_end = -1.0
    for i, (s, e, _txt) in enumerate(cues, 1):
        if e <= s:
            raise ValueError("SRT cue %d: end <= start" % i)
        if s < prev_end:
            raise ValueError("SRT cue %d: overlaps previous cue" % i)
        prev_end = e
    return cues


def load_cards(path):
    """Load + validate the card timeline template. Red-line gate inside."""
    cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    for key in ("video", "font", "aigc_notice", "cards"):
        if key not in cfg:
            raise ValueError("cards file missing key: %s" % key)
    notice = str(cfg["aigc_notice"]).strip()
    if not notice:
        raise ValueError("aigc_notice is empty - AIGC labeling is a red line"
                         " (CONSTITUTION S2-4), refusing to render")
    for section, keys in (
        ("video", ("width", "height", "fps")),
        ("font", ("file", "cards_size", "subs_size", "aigc_size", "subs_bottom")),
    ):
        for key in keys:
            if key not in cfg[section]:
                raise ValueError("cards %s section missing key: %s" % (section, key))
    cards = cfg["cards"]
    if not isinstance(cards, list) or not cards:
        raise ValueError("cards must be a non-empty list")
    prev_end = None
    for i, c in enumerate(cards, 1):
        for key in ("start", "end", "lines"):
            if key not in c:
                raise ValueError("card %d missing key: %s" % (i, key))
        s, e = float(c["start"]), float(c["end"])
        if e <= s:
            raise ValueError("card %d: end <= start" % i)
        if prev_end is not None and s < prev_end:
            raise ValueError("card %d: overlaps previous card" % i)
        if not isinstance(c["lines"], list) or not any(str(x).strip() for x in c["lines"]):
            raise ValueError("card %d: lines must be a non-empty list" % i)
        prev_end = e
    return cfg


def _em_cost(ch):
    """Rough glyph width in em units: CJK ~1.0 em, latin/digit ~0.55,
    space ~0.5. Good enough to keep drawtext inside the frame (it has
    no auto line-wrap, so oversize lines get clipped at the edges)."""
    o = ord(ch)
    if o >= 0x2E80:  # CJK ideographs + fullwidth forms + CJK punct
        return 1.0
    if ch in (" ", "\t"):
        return 0.5
    return 0.55


def _line_cost(s):
    return sum(_em_cost(ch) for ch in s)


# clause enders for punctuation-preferred subtitle breaks (O-20260924-1115)
_BREAK_AFTER = set(",.!?;:...,"
                   "\uff0c\u3002\uff01\uff1f\uff1b\uff1a\u3001\u2026")


def _prefer_punct_break(cur, next_cost, budget):
    """Given a full line `cur` that cannot take the next char, choose
    the break: prefer after the LAST clause punctuation when that
    leaves a next line that still fits; else hard-break at the edge.
    Returns (head, tail_next_line_start). Pure."""
    best = -1
    for i, ch in enumerate(cur):
        if ch in _BREAK_AFTER:
            best = i
    if best != -1:
        tail = cur[best + 1:]
        if len(tail) >= 2 and _line_cost(tail) + next_cost <= budget:
            return cur[:best + 1], tail
    return cur, ""


def wrap_for_width(text, fontsize, frame_w, margin=80):
    """Greedy-wrap text so each rendered line fits the frame budget.
    Existing newlines are respected (wrapped per paragraph).

    O-20260924-1115 iteration inputs #3 (two rounds):
    (a) punctuation-preferred breaks - when a wrap point is reached,
    prefer breaking after the last clause punctuation in the line, so
    subtitles read as natural clauses instead of splitting words like
    "detected / one person".
    (b) orphan-tail mending - a wrap stranding a tiny last line reads
    as a broken word; pull one char down so the tail keeps >=2 glyphs.
    """
    budget = (frame_w - 2 * margin) / float(fontsize)
    out_lines = []
    for para in str(text).split("\n"):
        cur, cur_cost = "", 0.0
        para_lines = []
        for ch in para:
            c = _em_cost(ch)
            if cur and cur_cost + c > budget:
                head, tail = _prefer_punct_break(cur, c, budget)
                para_lines.append(head)
                # NB: ch must join the new line - dropping it loses a
                # glyph (caught by the no-char-lost test assertions).
                cur, cur_cost = tail + ch, _line_cost(tail + ch)
            else:
                cur += ch
                cur_cost += c
        if cur:
            para_lines.append(cur)
        if (len(para_lines) >= 2
                and len(para_lines[-1].strip()) <= 2
                and len(para_lines[-2]) > 1):
            para_lines[-1] = para_lines[-2][-1] + para_lines[-1]
            para_lines[-2] = para_lines[-2][:-1]
        out_lines += para_lines
    return "\n".join(out_lines)


def _fpath(p):
    """Escape a path for a filtergraph option value (Windows drive colon)."""
    return str(p).replace("\\", "/").replace(":", "\\:")


# O-20260923-1937 visual-spec palette (visual-spec.md S3)
# NB: drawtext takes color NAMES or 0xRRGGBB only - "0.6*white" style
# expressions are not valid fontcolor values (ffmpeg exit 4294967274).
_COLORS = {
    "white": "white",
    "gray60": "gray",
    "accent": "0xE8E6DF",  # FLUX light-point platinum
}


def _visual_spec(cfg, font_path_check=True):
    """Resolve visual-spec keys from the font section (all optional;
    absent keys = legacy single-font rendering, fully backward compatible)."""
    font = cfg["font"]
    h1 = font.get("h1_font", "")
    if h1 and font_path_check and not Path(h1).exists():
        raise ValueError("font.h1_font not found: %s" % h1)
    return {
        "h1_font": h1,
        "h1_size": int(font.get("h1_size", 96)),
        "h1_color": font.get("h1_color", "white"),
        "h2_size": int(font.get("h2_size", 52)),
        "h2_color": font.get("h2_color", "gray60"),
        "h1_gap": int(font.get("h1_gap", 48)),
        "optical_center": float(font.get("optical_center", 0.42)),
    }


def _q(p):
    return "'" + _fpath(p) + "'"


def build_render_plan(cfg, cues, tmpdir, grain=0, bg_video=False):
    """Build the drawtext filtergraph. Text bodies go through temp
    textfiles so multi-line CJK renders without escaping issues.

    O-20260923-1937 visual-spec engine (backward compatible):
    - font section may carry h1_font/h1_size/h1_color/h2_size/h2_color/
      h1_gap and optical_center (default 0.42) - visual-spec.md S1-S2.
    - per card, lines[0] renders as H1 (bold anchor font, accent color,
      largest), remaining lines render as H2 block below it, both
      composed around the optical center line (42% frame height).
    - 150ms fade in/out per card (S4) via alpha expression.
    Cards without the new keys render exactly as before.

    O-20260923-2210-bm-a human-feel dial: grain>0 appends film grain
    (temporal+uniform noise) + soft vignette after all text layers - the
    flat digital "template" look reads as cheap-AI; grain+vignette read
    as produced film. Pure aesthetic pass, zero timeline impact.

    O-20260924-1115-bm-a real-footage dial: bg_video=True swaps the
    filtergraph head from a color source to [0:v] scaled to the frame -
    input-side selection (color lavfi vs recorded mp4) happens in main().
    """
    tmpdir = Path(tmpdir)
    font = cfg["font"]
    font_q = _q(font["file"])
    ls = int(font.get("line_spacing", 12))
    subs_bottom = int(font["subs_bottom"])
    frame_w = int(cfg["video"]["width"])
    frame_h = int(cfg["video"]["height"])
    spec = _visual_spec(cfg, font_path_check=False)
    made = []

    def textfile(content, name):
        p = tmpdir / name
        # LF only: CRLF makes drawtext treat \r as an extra line
        # break, doubling line pitch and clipping 3-line cues off
        # the frame bottom (pixel-measured at R-C on bs-001 v2)
        p.write_text(content, encoding="utf-8", newline="\n")
        made.append(p)
        return p

    def fade_alpha(start, end, ms=0.15):
        f = start + ms
        g = end - ms
        if g <= f:
            return None
        # NB: the whole expression must be single-quoted inside the
        # filtergraph, else its commas read as filter separators and
        # the graph collapses (crash exit 3015096584, O-1937 session).
        return ("'if(lt(t,%.3f),0,if(lt(t,%.3f),(t-%.3f)/%.3f,"
                "if(lt(t,%.3f),1,if(lt(t,%.3f),(%.3f-t)/%.3f,0))))'"
                % (start, f, start, ms, g, end, end, ms))

    aigc_p = textfile(str(cfg["aigc_notice"]).strip(), "aigc.txt")
    ends = [e for _, e, _ in cues] + [float(c["end"]) for c in cfg["cards"]]
    duration = max(ends) + float(cfg.get("tail", 0.5))

    if bg_video:
        # real-footage head: scale the recorded background to the frame.
        # NB: chain[0] "[0:v]" feeds the NEXT element directly (filtergraph
        # label shorthand - a comma after the label would read as an empty
        # filter name), so scale enters the chain as element #1.
        frame_w = int(cfg["video"]["width"])
        frame_h = int(cfg["video"]["height"])
        chain = ["[0:v]", "scale=%d:%d,setsar=1" % (frame_w, frame_h)]
    else:
        chain = ["[0:v]"]
    chain.append(
        "drawtext=fontfile=%s:textfile=%s:fontsize=%d:fontcolor=%s"
        ":alpha=0.8:x=48:y=48:line_spacing=%d"
        % (font_q, _q(aigc_p), int(font["aigc_size"]),
           _COLORS.get(spec["h2_color"], "white"), ls))
    for i, c in enumerate(cfg["cards"]):
        start, end = float(c["start"]), float(c["end"])
        alpha = fade_alpha(start, end)
        if spec["h1_font"] and c.get("lines"):
            h1_text = str(c["lines"][0]).strip()
            h2_lines = [str(x).strip() for x in c["lines"][1:] if str(x).strip()]
            h1_size = int(c.get("h1_size", spec["h1_size"]))
            h2_size = int(c.get("h2_size", spec["h2_size"]))
            h1f_q = _q(spec["h1_font"])
            h1_body = textfile(
                "\n".join(wrap_for_width(x, h1_size, frame_w) for x in [h1_text]),
                "card%02d.h1.txt" % i)
            h1_y = "(h*%.2f-text_h/2)" % spec["optical_center"]
            h1_extra = ""
            if alpha:
                h1_extra = ":alpha=%s" % alpha
            chain.append(
                "drawtext=fontfile=%s:textfile=%s:fontsize=%d:fontcolor=%s"
                ":line_spacing=%d:x=(w-text_w)/2:y=%s:enable='between(t,%.3f,%.3f)'%s"
                % (h1f_q, _q(h1_body), h1_size, _COLORS.get(spec["h1_color"], "white"),
                   ls, h1_y, start, end, h1_extra))
            if h2_lines:
                h2_body = textfile(
                    "\n".join(wrap_for_width(x, h2_size, frame_w) for x in h2_lines),
                    "card%02d.h2.txt" % i)
                h2_y = ("(h*%.2f+text_h/2+%d)"
                        % (spec["optical_center"], int(spec["h1_gap"])))
                h2_extra = ""
                if alpha:
                    h2_extra = ":alpha=%s" % alpha
                chain.append(
                    "drawtext=fontfile=%s:textfile=%s:fontsize=%d:fontcolor=%s"
                    ":line_spacing=%d:x=(w-text_w)/2:y=%s:enable='between(t,%.3f,%.3f)'%s"
                    % (font_q, _q(h2_body), h2_size,
                       _COLORS.get(spec["h2_color"], "white"),
                       ls, h2_y, start, end, h2_extra))
        else:
            size = int(c.get("size", font["cards_size"]))
            body_text = "\n".join(
                wrap_for_width(x, size, frame_w) for x in c["lines"])
            body = textfile(body_text, "card%02d.txt" % i)
            chain.append(
                "drawtext=fontfile=%s:textfile=%s:fontsize=%d:fontcolor=white"
                ":line_spacing=%d:x=(w-text_w)/2:y=(h-text_h)/2"
                ":enable='between(t,%.3f,%.3f)'"
                % (font_q, _q(body), size, ls, start, end))
    for j, (s, e, t) in enumerate(cues):
        body = textfile(wrap_for_width(t, int(font["subs_size"]), frame_w),
                        "cue%03d.txt" % j)
        chain.append(
            "drawtext=fontfile=%s:textfile=%s:fontsize=%d:fontcolor=white"
            ":line_spacing=%d:x=(w-text_w)/2:y=h-%d:enable='between(t,%.3f,%.3f)'"
            % (font_q, _q(body), int(font["subs_size"]), ls, subs_bottom, s, e))
    if grain and int(grain) > 0:
        chain.append("noise=alls=%d:allf=t+u" % int(grain))
        chain.append("vignette=angle=PI/6")
    return {
        # "[0:v]" must sit directly before the first filter: a comma after a
        # link label reads as an empty filter name to the graph parser.
        "filter_text": chain[0] + ",".join(chain[1:]) + "[v]",
        "duration": duration,
        "textfiles": made,
    }


def voiceover_matches(voiceover_text, cues):
    return norm_text(voiceover_text) == norm_text("".join(t for _, _, t in cues))


def poster_time(cfg):
    """Cover-frame timestamp for --poster (audit O-1043 R1, backlog #16).

    A literal t=0 frame is a poor cover: cards fade in over 150ms
    (visual-spec S4), so t=0 carries background + AIGC notice only.
    The cover frame = the first card at FULL opacity; an ultra-short
    first card falls back to mid-card; a no-cards documentary cut has
    no better moment than the literal first frame (t=0).
    """
    cards = cfg.get("cards") or []
    if not cards:
        return 0.0
    first = cards[0]
    s, e = float(first["start"]), float(first["end"])
    t = s + 0.15
    if e <= t:
        t = (s + e) / 2.0
    return t


def main(argv=None):
    ap = argparse.ArgumentParser(description="R-A card timeline renderer")
    ap.add_argument("--cards", required=True)
    ap.add_argument("--srt")
    ap.add_argument("--voiceover")
    ap.add_argument("--out")
    ap.add_argument("--audio")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--grain", type=int, default=0,
                    help="film grain + vignette intensity 0-20 (O-2210)")
    ap.add_argument("--bg",
                    help="override video bg color (e.g. 0x0a0a0d)")
    ap.add_argument("--bgvideo",
                    help="real-footage background video (O-20260924-1115); "
                         "looped, scaled to frame, replaces the color source")
    ap.add_argument("--no-cards", action="store_true",
                    help="pure-documentary cut: AIGC notice + subs only")
    ap.add_argument("--poster",
                    help="after a successful render, export the cover "
                         "frame to this PNG (first card at full opacity; "
                         "ignored with --dry-run) - audit O-1043 R1")
    args = ap.parse_args(argv)

    cards_path = Path(args.cards)
    try:
        cfg = load_cards(cards_path)
    except ValueError as e:
        print("FAIL cards: %s" % e)
        return 2
    if args.bg:
        cfg["video"]["bg"] = args.bg
    if args.no_cards:
        # keep the timeline (cue ends drive duration); drop card layers
        cfg["cards"] = []
    if args.bgvideo and not Path(args.bgvideo).exists():
        print("FAIL bgvideo not found: %s" % args.bgvideo)
        return 2
    font_path = Path(cfg["font"]["file"])
    if not font_path.exists():
        print("FAIL font file not found: %s (override font.file in cards JSON)" % font_path)
        return 2

    cards_dir = cards_path.parent
    srt_path = Path(args.srt) if args.srt else cards_dir / "subs.srt"
    if not srt_path.exists():
        print("FAIL srt not found: %s" % srt_path)
        return 2
    try:
        cues = parse_srt(srt_path)
    except ValueError as e:
        print("FAIL srt: %s" % e)
        return 2

    vo_path = Path(args.voiceover) if args.voiceover else cards_dir / "voiceover.txt"
    if vo_path.exists():
        vo_text = vo_path.read_text(encoding="utf-8-sig")
        if not voiceover_matches(vo_text, cues):
            msg = "voiceover txt and SRT text differ after normalization"
            if args.strict:
                print("FAIL %s (%s)" % (msg, vo_path))
                return 2
            print("WARN %s - placeholder SRT? recheck at R-C alignment" % msg)
    elif args.voiceover:
        print("FAIL voiceover not found: %s" % vo_path)
        return 2

    audio_path = Path(args.audio) if args.audio else None
    if audio_path is not None and not audio_path.exists():
        print("FAIL audio not found: %s" % audio_path)
        return 2

    meta = cfg.get("meta") or {}
    topic = str(meta.get("topic", "")).strip().lower().replace(" ", "-")
    out_path = Path(args.out) if args.out else (
        REPO / "output" / "renders" / ((topic or cards_path.stem) + "-card.mp4"))
    out_path.parent.mkdir(parents=True, exist_ok=True)

    tmpdir = Path(tempfile.mkdtemp(prefix="bsrender-"))
    try:
        plan = build_render_plan(cfg, cues, tmpdir, grain=args.grain,
                                 bg_video=bool(args.bgvideo))
        if args.dry_run:
            print("dry-run ok: cards=%d cues=%d duration=%.3fs out=%s"
                  % (len(cfg["cards"]), len(cues), plan["duration"], out_path))
            print("--- filtergraph ---")
            print(plan["filter_text"])
            return 0

        v = cfg["video"]
        if args.bgvideo:
            # real-footage head: loop the recording, drive length by -t
            cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                   "-stream_loop", "-1", "-i", str(args.bgvideo)]
        else:
            cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                   "-f", "lavfi", "-i",
                   "color=c=%s:s=%dx%d:r=%d:d=%.3f"
                   % (v.get("bg", "black"), int(v["width"]), int(v["height"]),
                      int(v["fps"]), plan["duration"])]
        if audio_path is not None:
            cmd += ["-i", str(audio_path)]
        # NB: this ffmpeg build (9.0.1 gyan full) dropped
        # -filter_complex_script, so the graph goes inline as one argv
        # element (pure ASCII, no shell quoting involved via subprocess).
        cmd += ["-filter_complex", plan["filter_text"], "-map", "[v]"]
        if audio_path is not None:
            cmd += ["-map", "1:a", "-c:a", "aac", "-b:a", "192k", "-shortest"]
        if args.bgvideo:
            cmd += ["-t", "%.3f" % plan["duration"]]
        cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                "-r", str(int(v["fps"])), str(out_path)]
        try:
            run = subprocess.run(cmd, capture_output=True, text=True)
        except FileNotFoundError:
            print("FAIL ffmpeg not found on PATH")
            return 3
        if run.returncode != 0:
            print("FAIL ffmpeg exit %d" % run.returncode)
            print(run.stderr[-2000:])
            print("--- filtergraph tail ---")
            print(plan["filter_text"][-1500:])
            return 4

        try:
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=width,height,codec_name",
                 "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1", str(out_path)],
                capture_output=True, text=True)
        except FileNotFoundError:
            print("FAIL ffprobe not found on PATH")
            return 3
        if probe.returncode != 0:
            print("FAIL ffprobe exit %d" % probe.returncode)
            return 4
        if args.poster:
            poster_path = Path(args.poster)
            poster_path.parent.mkdir(parents=True, exist_ok=True)
            t_poster = poster_time(cfg)
            cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                   "-ss", "%.3f" % t_poster, "-i", str(out_path),
                   "-frames:v", "1", str(poster_path)]
            try:
                run = subprocess.run(cmd, capture_output=True, text=True)
            except FileNotFoundError:
                print("FAIL ffmpeg not found on PATH")
                return 3
            if run.returncode != 0 or not poster_path.exists():
                print("FAIL poster export exit %d" % run.returncode)
                print(run.stderr[-800:])
                return 4
            print("poster: %s (cover frame at t=%.3fs)"
                  % (poster_path, t_poster))
        size_kb = out_path.stat().st_size // 1024
        print("OK %s" % out_path)
        print("cards=%d cues=%d duration=%.3fs size=%dKB"
              % (len(cfg["cards"]), len(cues), plan["duration"], size_kb))
        print(probe.stdout.strip())
        return 0
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
