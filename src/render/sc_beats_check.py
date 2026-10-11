"""SC-series beats machine-check CLI: format / verbatim anchors / material inclusion /
card cross-check / leak guard (audio + drama line, single source of truth).

Replaces the eight-generation ad-hoc copy lineage r1874 -> r1970 (tech#99 anchor):
every SC piece previously hand-copied a per-piece check script. The per-piece
knowledge now lives in small data files next to the beats; this CLI is generic.

Faces (each optional except format, which always runs):
  1. format (always): rows = PROFILE | card | spoken, profile in the 9-word set.
     Malformed rows are loud -> rc2 (same_text_check BAD-BEATS-ROW precedent).
  2. --anchors FILE: one verbatim anchor per line ('#' comment / blank skipped);
     every anchor must appear in the beats text. MISS -> rc1.
  3. --material FILE (tech#96 sync guard): every non-empty beats row must be
     verbatim-embedded in the S1 material file. Bad row -> rc1.
  4. --card FILE --card-anchors FILE: each line is `beats_form||card_form`
     (or a bare form = same on both sides); the target form (card_form when
     given, else the bare form) must exist in the anchor card file. MISS -> rc1.
  5. --leak PHRASE (repeatable): composition guard (desensitization precedent);
     any hit in beats -> rc1.

Usage:
  python src/render/sc_beats_check.py --beats X.beats.txt [--material M.md]
      [--anchors A.txt] [--card C.md --card-anchors CA.txt]
      [--leak PHRASE ...] [--out evidence.txt]

Exit codes: 0 = all enabled faces green, 1 = check FAIL, 2 = usage or malformed
beats input (loud, never silent).
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys

PROG = "sc_beats_check"

PROFILES = {"hook", "punch", "body", "wink", "beat", "turn", "proof", "close", "cta"}

# r1970 spoken-char counting: CJK punctuation and whitespace stripped.
_STRIP_RE = re.compile(r"[\s\uff0c\u3002\uff1a\uff1b\u3001\uff01\uff1f\u2014\u2026"
                       r"\u300c\u300d\u300e\u300f\u300a\u300b\u00b7\uff08\uff09]")

CARD_PAIR_SEP = "||"


def load_text(path):
    with io.open(path, encoding="utf-8") as fh:
        return fh.read()


def load_rows(beats_text):
    """Return non-empty beats rows."""
    return [ln.strip() for ln in beats_text.splitlines() if ln.strip()]


def format_face(rows):
    """Return (bad_list, spoken_nchars). bad entries: (reason, lineno, detail)."""
    bad = []
    spoken_chars = 0
    for i, row in enumerate(rows, 1):
        parts = [p.strip() for p in row.split("|")]
        if len(parts) != 3:
            bad.append(("cols", i, row[:40]))
            continue
        if parts[0] not in PROFILES:
            bad.append(("profile", i, parts[0]))
            continue
        spoken_chars += len(_STRIP_RE.sub("", parts[2]))
    return bad, spoken_chars


def load_anchor_lines(path):
    """One anchor per line; '#' comments and blank lines skipped."""
    lines = []
    for ln in load_text(path).splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        lines.append(ln)
    return lines


def anchor_face(beats_text, anchors):
    """Return list of missing anchors."""
    return [a for a in anchors if a not in beats_text]


def inclusion_face(rows, material_text):
    """Return list of beats rows NOT verbatim-embedded in the material."""
    return [row for row in rows if row not in material_text]


def load_card_pairs(path):
    """Return list of (beats_form, target_form). Bare line -> (form, form)."""
    pairs = []
    for ln in load_anchor_lines(path):
        if CARD_PAIR_SEP in ln:
            beats_form, card_form = ln.split(CARD_PAIR_SEP, 1)
            pairs.append((beats_form, card_form))
        else:
            pairs.append((ln, ln))
    return pairs


def card_face(card_text, pairs):
    """Return list of target forms not found in the card text."""
    return [target for _beats_form, target in pairs if target not in card_text]


def leak_face(beats_text, leaks):
    """Return list of leak phrases present in beats."""
    return [s for s in leaks if s in beats_text]


def build_report(beats_text, material_text, anchors, card_text, card_pairs, leaks):
    """Return (rc, report_lines). rc 0/1/2 semantics per module docstring."""
    rows = load_rows(beats_text)
    bad, spoken_chars = format_face(rows)
    lines = ["rows=%d spoken_nchars=%d format_bad=%s"
             % (len(rows), spoken_chars, bad if bad else "NONE")]
    if bad:
        lines.append("SC-CHECK BAD-BEATS (format)")
        return 2, lines

    failed = []
    if anchors is not None:
        miss = anchor_face(beats_text, anchors)
        lines.append("verbatim_anchors=%d MISS=%s"
                     % (len(anchors), miss if miss else "NONE"))
        if miss:
            failed.append("anchor")
    else:
        lines.append("verbatim_anchors=SKIP (no --anchors)")
    if material_text is not None:
        bad_inc = inclusion_face(rows, material_text)
        lines.append("inclusion(beats in material)=%d/%d bad=%s"
                     % (len(rows) - len(bad_inc), len(rows), bad_inc if bad_inc else "NONE"))
        if bad_inc:
            failed.append("inclusion")
    else:
        lines.append("inclusion(beats in material)=SKIP (no --material)")
    if card_text is not None and card_pairs is not None:
        card_miss = card_face(card_text, card_pairs)
        lines.append("card_source_MISS=%s" % (card_miss if card_miss else "NONE"))
        if card_miss:
            failed.append("card")
    else:
        lines.append("card_source=SKIP (no --card/--card-anchors)")
    if leaks:
        hits = leak_face(beats_text, leaks)
        lines.append("leak_face_hits=%s" % (hits if hits else "NONE"))
        if hits:
            failed.append("leak")
    else:
        lines.append("leak_face=SKIP (no --leak)")

    if failed:
        lines.append("SC-CHECK FAIL faces=%s" % ",".join(failed))
        return 1, lines
    lines.append("SC-CHECK GREEN")
    return 0, lines


def main(argv=None):
    ap = argparse.ArgumentParser(prog=PROG, description=__doc__.splitlines()[0])
    ap.add_argument("--beats", required=True, help="beats txt (PROFILE | card | spoken)")
    ap.add_argument("--material", help="S1 material file (tech#96 inclusion face)")
    ap.add_argument("--anchors", help="anchor list file, one per line ('#' comments skipped)")
    ap.add_argument("--card", help="anchor card file (census anchor) for cross-check face")
    ap.add_argument("--card-anchors", help="card cross-check pairs file: 'beats_form||card_form' or bare form")
    ap.add_argument("--leak", action="append", default=[],
                    help="composition-guard phrase (repeatable); any hit in beats -> FAIL")
    ap.add_argument("--out", help="write full report to file (UTF-8, no BOM)")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.beats):
        print("%s: file not found: %s" % (PROG, args.beats))
        return 2
    if bool(args.card) != bool(args.card_anchors):
        print("%s: --card and --card-anchors must be given together" % PROG)
        return 2
    try:
        beats_text = load_text(args.beats)
        material_text = load_text(args.material) if args.material else None
        anchors = load_anchor_lines(args.anchors) if args.anchors else None
        card_text = load_text(args.card) if args.card else None
        card_pairs = load_card_pairs(args.card_anchors) if args.card_anchors else None
    except (OSError, UnicodeError) as exc:
        print("%s: unreadable input: %s" % (PROG, exc))
        return 2

    rc, lines = build_report(beats_text, material_text, anchors, card_text,
                             card_pairs, args.leak)
    text = "\n".join(lines)
    if args.out:
        with io.open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text + "\n")
    # GBK-console safe stdout (PS 5.1 op-red family: never trust console for CJK)
    print(text.encode("ascii", "backslashreplace").decode("ascii"))
    return rc


if __name__ == "__main__":
    sys.exit(main())
