# -*- coding: utf-8 -*-
"""L-card pool/closing sentence reuse defense (tech#191 canonization).

The per-round ad-hoc scans (R2285 r2285_collide_scan, R2321 m1-assert A6
full-face scan + r2321_closings rotation check) promoted into one structural
pre-render assertion. Until now the defense lived only in throwaway probe
scripts -- a reused pool sentence slipped through whenever a round skipped
the manual scan (R2321 intercept was luck, not law).

Defense semantics (anchored on the R2321 production precedent):

1. pool rows (``<label>轴/池：「sentence」`` -- axis reactions, 像素灵池)
   must not reuse any sentence already on ANY historical card face
   (fleet-wide all-card-face scan: R2321 anchor: 烟火轴 candidate
   「刚赚的这份钱，得给孩子买点糖」 blocked because REACT-v3 had it).
2. closing rows (``<owner>信条/灵感条：「sentence」``) rotate within their
   OWN form only (REACT closing vs REACT closings -- the r2321_closings
   "21 款收束行全扫" rotation law). Cross-form archival citations stay
   legal (CENSUS-v20 图鉴卡 信条 == REACT-v22 收束行 was judged a legal
   documentary citation at R2321; a CENSUS card therefore never poisons
   a REACT closing candidate).

Baseline = every non ``-tmp`` card dir under the cards root EXCEPT the
card being scanned (a re-render never self-blocks; discarded ``-tmp``
draft sentences never poison the baseline). Hot/deck rows carry neither
the pool nor the closing shape, so DIGEST/CENSUS/QUOTE cards pass through
with an empty defense face by structure (zero-hardcoding: line shape
decides, never a line index).

Known gap, accepted: pre-v2 legacy closing rows without the
``信条/灵感条：「」`` shape (e.g. REACT-v1 城市律 plain line) contribute no
baseline sentence; the production line has emitted the canonical closing
shape since v2.

Exit codes: 0 clean, 1 collision (caller must refuse to render),
2 usage error. CLI:

    python tools/collide_scan.py --cards-dir data/storylines/cards/MC-...

tools/lcard_m2.py calls scan_cards() before any disk write: a hit refuses
the render with zero output (tech#191 hit = rc1 law).
"""
import argparse
import json
import os
import re
import sys

QUOTED_RE = re.compile(r'「(.+?)」')
POOL_ROW_RE = re.compile(r'^.{0,8}(?:轴|池)[：:]「')
CLOSING_RE = re.compile(r'(信条|灵感条)[：:]「(.+?)」')
DIR_RE = re.compile(r'^MC-\d{8}-([A-Z]+)-v\d+$')


def quoted_sentences(line):
    """All 「」-quoted sentences in one card row."""
    return QUOTED_RE.findall(line)


def is_pool_row(line):
    """Axis/pool reaction row: short label ending in 轴 or 池 +：「...」."""
    return bool(POOL_ROW_RE.match(line))


def is_closing_row(line):
    """Closing row: owner 信条/灵感条：「...」 (search, label not at start)."""
    return bool(CLOSING_RE.search(line))


def form_of(dirname):
    """Card form (REACT/DIGEST/CENSUS/...) from the MC-YYYYMMDD-FORM-vN dir name."""
    m = DIR_RE.match(dirname)
    return m.group(1) if m else None


def load_lines(cards_dir):
    """cards[0].lines of a card dir, or None when not a loadable card."""
    path = os.path.join(cards_dir, "cards.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        cards = d.get("cards", [])
        if not cards:
            return None
        return cards[0].get("lines", [])
    except Exception:
        return None


def collect_baseline(cards_root, exclude_dir):
    """Historical card-face sentence sets.

    Returns (all_face, form_close):
      all_face    -- {sentence: source_dir} every quoted sentence on any
                     baseline card face (fleet-wide, pool-defense face)
      form_close  -- {form: {sentence: source_dir}} closing sentences keyed
                     by card form (rotation-law face)
    """
    all_face = {}
    form_close = {}
    ex = os.path.normcase(os.path.abspath(exclude_dir))
    for name in sorted(os.listdir(cards_root)):
        path = os.path.join(cards_root, name)
        if name.endswith("-tmp"):
            continue
        if not os.path.isdir(path):
            continue
        if os.path.normcase(os.path.abspath(path)) == ex:
            continue
        lines = load_lines(path)
        if lines is None:
            continue
        form = form_of(name)
        for ln in lines:
            if not isinstance(ln, str):
                continue
            for s in quoted_sentences(ln):
                all_face.setdefault(s, name)
            for m in CLOSING_RE.finditer(ln):
                if form:
                    form_close.setdefault(form, {}).setdefault(m.group(2), name)
    return all_face, form_close


def scan_cards(cards_dir, cards_root=None):
    """Violations for the card in cards_dir; empty list = clean.

    cards_root defaults to the parent of cards_dir (the cards shelf root),
    so the defense is self-locating under the canonical layout.
    """
    cards_dir = os.path.abspath(cards_dir)
    if cards_root is None:
        cards_root = os.path.dirname(cards_dir)
    lines = load_lines(cards_dir)
    if lines is None:
        return ["cards dir has no loadable cards.json: %s" % cards_dir]
    form = form_of(os.path.basename(cards_dir))
    all_face, form_close = collect_baseline(cards_root, cards_dir)
    violations = []
    for i, ln in enumerate(lines):
        if not isinstance(ln, str):
            continue
        if is_pool_row(ln):
            for s in quoted_sentences(ln):
                if s in all_face:
                    violations.append(
                        "pool row [%d] reuses sentence already on %s: %s"
                        % (i, all_face[s], s))
        if is_closing_row(ln):
            for m in CLOSING_RE.finditer(ln):
                s = m.group(2)
                if form and s in form_close.get(form, {}):
                    violations.append(
                        "closing row [%d] reuses %s closing of %s (rotation "
                        "law): %s" % (i, form, form_close[form][s], s))
    return violations


def main():
    ap = argparse.ArgumentParser(
        description="L-card pool/closing sentence reuse defense (tech#191)")
    ap.add_argument("--cards-dir", required=True,
                    help="card directory containing cards.json (the card to scan)")
    ap.add_argument("--cards-root", default=None,
                    help="baseline cards root (default: parent of --cards-dir)")
    args = ap.parse_args()
    cards_dir = os.path.abspath(args.cards_dir)
    if not os.path.isdir(cards_dir):
        print("FAIL cards dir not found: %s" % cards_dir)
        return 2
    violations = scan_cards(cards_dir, args.cards_root)
    if violations:
        for v in violations:
            print("COLLIDE-FAIL: %s" % v)
        print("FAIL collide_scan: %d violation(s) -- refuse render (tech#191)"
              % len(violations))
        return 1
    print("collide-scan PASS (pool rows + closing rows clean, tech#191)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
