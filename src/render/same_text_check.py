"""Same-text mechanical check: SRT cues vs beats spoken column (audio line).

Single source of truth replacing the six-generation ad-hoc same_text_r275..r1939
copy lineage (tech#87 anchor). Audio-line (SC-xxx) same-text verification:
SRT cue count must equal beats row count; each cue text must equal the beats
spoken column verbatim, space-insensitive. Optional --decl-check reports the
hook triple declaration (AI-gen / real-event archive / inference) and the close
inference declaration as advisory lines that never affect the exit code.

Usage:
  python src/render/same_text_check.py --beats X.beats.txt --srt Y.srt \
      [--decl-check] [--out evidence.txt]

Exit codes: 0 = same text (zero miss), 1 = MISS(es) found, 2 = usage or bad
input file (malformed beats row / unreadable file -> loud, never silent).
"""
from __future__ import annotations

import argparse
import io
import os
import sys

PROG = "same_text_check"


def load_srt(path):
    """Return list of cue texts (multi-line cues joined, index lines skipped)."""
    with io.open(path, encoding="utf-8") as fh:
        raw = fh.read()
    cues = []
    for block in raw.strip().split("\n\n"):
        if not block.strip():
            continue
        lines = block.splitlines()
        cues.append("".join(lines[2:]).strip())
    return cues


def load_beats_rows(path):
    """Return non-empty beats rows (raw) -- decl checks consume raw rows."""
    with io.open(path, encoding="utf-8") as fh:
        return [ln.strip() for ln in fh if ln.strip()]


def spoken_column(row):
    """Third pipe-separated column = spoken text. Raise on malformed row."""
    parts = row.split("|")
    if len(parts) < 3:
        raise ValueError("malformed beats row (needs 3 pipe columns): %s" % row[:60])
    return parts[2].strip()


def compare(cues, spoken):
    """Return (miss_count, report_lines). Space-insensitive verbatim compare."""
    lines = ["cues=%d beats=%d" % (len(cues), len(spoken))]
    miss = 0
    if len(cues) != len(spoken):
        miss += 1
        lines.append("COUNT-MISMATCH")
    for i in range(min(len(cues), len(spoken))):
        c = cues[i].replace(" ", "")
        b = spoken[i].replace(" ", "")
        if c != b:
            miss += 1
            lines.append("MISS cue%02d" % (i + 1))
            lines.append("  srt : " + cues[i][:70])
            lines.append("  beat: " + spoken[i][:70])
    return miss, lines


def decl_report(rows):
    """Advisory declaration lines (hook triple + close inference) -- r1939 logic."""
    hook = rows[0]
    close = rows[-1]
    return [
        "hook-triple-decl: ai-gen=%s archive=%s inference=%s" % (
            "AI" in hook or "AI 参与生成" in hook,
            "真实事件" in hook and "档案" in hook,
            "合理推演" in hook),
        "close-inference-decl: %s" % ("合理推演" in close),
    ]


def build_report(cues, rows, decl_check):
    try:
        spoken = [spoken_column(r) for r in rows]
    except ValueError as exc:
        return None, ["BAD-BEATS-ROW: %s" % exc]
    miss, lines = compare(cues, spoken)
    if decl_check:
        lines.extend(decl_report(rows))
    lines.append("SAME-TEXT miss=%d" % miss)
    return miss, lines


def main(argv=None):
    ap = argparse.ArgumentParser(prog=PROG, description=__doc__.splitlines()[0])
    ap.add_argument("--beats", required=True, help="beats txt (type | title | spoken)")
    ap.add_argument("--srt", required=True, help="SRT file to verify")
    ap.add_argument("--decl-check", action="store_true",
                    help="report hook triple/close inference declarations (advisory)")
    ap.add_argument("--out", help="write full report to file (UTF-8, no BOM)")
    args = ap.parse_args(argv)

    for path in (args.beats, args.srt):
        if not os.path.isfile(path):
            print("%s: file not found: %s" % (PROG, path))
            return 2
    try:
        cues = load_srt(args.srt)
        rows = load_beats_rows(args.beats)
    except (OSError, UnicodeError) as exc:
        print("%s: unreadable input: %s" % (PROG, exc))
        return 2

    miss, lines = build_report(cues, rows, args.decl_check)
    if miss is None:
        text = "\n".join(lines)
        print(text.encode("ascii", "backslashreplace").decode("ascii"))
        return 2

    text = "\n".join(lines)
    if args.out:
        with io.open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text + "\n")
    # GBK-console safe stdout (PS 5.1 op-red family: never trust console for CJK)
    print(text.encode("ascii", "backslashreplace").decode("ascii"))
    return 1 if miss else 0


if __name__ == "__main__":
    sys.exit(main())
