# -*- coding: utf-8 -*-
"""SRT post-fix tool: tolerant parse + overlap clamp + rewrite (R-C).

Why: edge-tts --write-subtitles emits word-timestamp cues that can
overlap by tens of ms (observed 50ms, tts-samples R11). The renderer's
parse_srt rightly refuses overlaps, so this is the pipeline step that
turns a raw synthesis SRT into a render-ready one.

Usage:
    python src/render/srt_fix.py --in raw.srt --out fixed.srt

ASCII rule: code/comments English; Chinese only in the UTF-8 data
files this tool consumes.

Exit codes: 0 ok; 2 parse error.
"""
import argparse
import re
import sys
from pathlib import Path

_TIME_RE = re.compile(r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})")


def _t(token):
    m = _TIME_RE.fullmatch(token.strip())
    if not m:
        raise ValueError("bad SRT time: %r" % token)
    h, mnt, sec, ms = (int(x) for x in m.groups())
    return h * 3600.0 + mnt * 60.0 + sec + ms / 1000.0


def fmt_t(x):
    ms = int(round(x * 1000.0))
    h, ms = divmod(ms, 3600000)
    mnt, ms = divmod(ms, 60000)
    sec, ms = divmod(ms, 1000)
    return "%02d:%02d:%02d,%03d" % (h, mnt, sec, ms)


def parse_srt_loose(path):
    """Tolerant parse: keep order + text, allow overlaps; skip
    malformed blocks instead of crashing the pipeline."""
    raw = Path(path).read_text(encoding="utf-8-sig")
    blocks = [b for b in re.split(r"\r?\n\s*\r?\n", raw.strip()) if b.strip()]
    cues = []
    for block in blocks:
        lines = [ln for ln in block.splitlines() if ln.strip()]
        if len(lines) < 3 or "-->" not in lines[1]:
            continue
        left, _, right = lines[1].partition("-->")
        cues.append((_t(left), _t(right),
                     "\n".join(ln.strip() for ln in lines[2:])))
    if not cues:
        raise ValueError("no valid SRT cues in %s" % path)
    return cues


def clamp_overlaps(cues):
    """start = max(start, prev_end); drop cues that go degenerate."""
    out, dropped = [], 0
    prev_end = None
    for s, e, t in cues:
        if prev_end is not None and s < prev_end:
            s = prev_end
        if e <= s:
            dropped += 1
            continue
        out.append((s, e, t))
        prev_end = e
    return out, dropped


def write_srt(cues, path):
    parts = []
    for i, (s, e, t) in enumerate(cues, 1):
        parts.append("%d\n%s --> %s\n%s" % (i, fmt_t(s), fmt_t(e), t))
    Path(path).write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description="clamp SRT overlaps for render")
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        cues = parse_srt_loose(args.inp)
    except ValueError as e:
        print("FAIL %s" % e)
        return 2
    fixed, dropped = clamp_overlaps(cues)
    write_srt(fixed, args.out)
    print("OK %s -> %s cues=%d dropped=%d"
          % (args.inp, args.out, len(fixed), dropped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
