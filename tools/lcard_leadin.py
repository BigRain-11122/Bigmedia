# -*- coding: utf-8 -*-
"""L-card off-card lead-in builder (tech#194, M5 publish-case slot).

E4 brain three-flight reads (DIGEST 5.5 / REACT 5.0 / DIGEST 2.0) flagged
the context threshold: card faces stay verbatim-factual (v22 precedent,
untouchable), so the plain-language fix lands OFF the card. Each card's
M5 publish case carries one lead-in paragraph:

    city setting (1-2 sentences) + this-issue term notes (2-3 sentences,
    top glossary units by editorial priority) + one motif sentence.

Glossary + templates live in data/storylines/cards/leadin-glossary.json
(Chinese data per encoding law). Matched glossary units beyond the top-3
notes are reported as DEFERRED (editor footer), and watch-pattern hits
missing from the glossary are UNGLOSSED -- --check exits 1 on them
(E4 context-threshold gate, mechanical counterpart).

Usage:
    python tools/lcard_leadin.py --cards data/storylines/cards/MC-20261017-DIGEST-v23/cards.json
    python tools/lcard_leadin.py --cards <...> --check      # gate only, no write
    python tools/lcard_leadin.py --cards <...> --out <path> # default <card_dir>/leadin.md

Publishing stays locked on M5 account physicals; generated lead-ins are
design-state publish-case drafts (negative-result logging is legitimate).
Exit codes: 0 ok; 1 unglossed jargon present (check mode) or bad input.

tech#200: matched units are ranked by per-card hit density (number of
text positions covered by any term, longest-match first), tie-broken by
glossary order. The old static order let a once-mentioned unit at the
top of the glossary outrank the card's own core jargon (R2334 anchor:
v22 deferred its core units, v23 deferred T1); density makes the
top-notes selection per-card and mechanical.

tech#204: the editor footer carries density readings. DEFERRED lines
read "term (N hit(s)*marker)" where the marker is the boundary-tie mark
(reorder the glossary to promote this unit) or "low density" (lever =
change the card-face word or accept); NOTE lines carry the same hits
basis. R2339 anchor: v23's T1 sat in a 1-hit tie set and fell behind
only by glossary order, but the footer showed "who" not "why" -- the
glossary-order tuning lever was invisible to the editor.
"""
import argparse
import datetime
import io
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLOSSARY_PATH = os.path.join(REPO, "data", "storylines", "cards", "leadin-glossary.json")
MOTIF_RE = re.compile(u"\u300c([^\u300c\u300d]{4,40})\u300d\u6bcd\u9898")  # "<...> motif"

MAX_NOTES = 3


def load_glossary(path=GLOSSARY_PATH):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def card_lines(cfg):
    return [ln for card in cfg.get("cards", []) for ln in card.get("lines", [])]


def detect_form(cfg):
    meta = cfg.get("meta", {})
    blob = (meta.get("form", "") + " " + meta.get("topic", "")).upper()
    return "REACT" if "REACT" in blob else "DIGEST"


def unit_hits(blob, terms):
    """Positions in the card text covered by any term (longest-match first)."""
    pats = sorted((t for t in terms if t), key=len, reverse=True)
    if not pats:
        return 0
    rx = re.compile("|".join(re.escape(t) for t in pats))
    return len(rx.findall(blob))


def matched_units(lines, glossary):
    """Glossary (unit, hits) pairs whose any term appears in the card lines.

    tech#200 density ranking: ordered by per-card hit count (descending),
    tie-broken by glossary order (editorial priority). What the card talks
    about most is what the lead-in glosses first. Hits stay attached to
    each unit so the editor footer can show WHY each unit ranked where it
    did (tech#204).
    """
    blob = "\n".join(lines)
    ranked = []
    for idx, unit in enumerate(glossary.get("units", [])):
        hits = unit_hits(blob, unit.get("terms", []))
        if hits:
            ranked.append((-hits, idx, unit, hits))
    ranked.sort(key=lambda r: (r[0], r[1]))
    return [(r[2], r[3]) for r in ranked]


def unglossed_terms(lines, glossary):
    """Watch-pattern hits that no glossary unit covers (E4 context gate)."""
    blob = "\n".join(lines)
    hits = []
    for pat in glossary.get("watch_patterns", []):
        if pat not in blob:
            continue
        covered = any(
            (pat in t or t in pat)
            for unit in glossary.get("units", [])
            for t in unit.get("terms", [])
        )
        if not covered:
            hits.append(pat)
    return hits


def extract_motif(cfg, glossary):
    edv = cfg.get("meta", {}).get("editorial_value", "")
    m = MOTIF_RE.search(edv)
    if m:
        return m.group(1), True
    return glossary.get("motif_fallback", ""), False


TIE_MARK = u"\u5e73\u624b\u96c6\u6309\u672f\u8bed\u7c3f\u5e8f"  # tie set, ranked by glossary order
LOW_DENSITY_MARK = u"\u4f4e\u5bc6\u5ea6"  # below the notes boundary


def _hits_label(hits):
    return "%d %s" % (hits, "hit" if hits == 1 else "hits")


def deferred_reading(term, hits, boundary_hits):
    """tech#204: why this unit fell behind -- boundary tie (reorder the
    glossary to promote it) vs genuinely lower density (lever = change
    the card-face word or accept)."""
    mark = TIE_MARK if hits == boundary_hits else LOW_DENSITY_MARK
    return u"%s (%s\u00b7%s)" % (term, _hits_label(hits), mark)


def note_reading(term, hits, tied):
    """tech#204: hits basis for a chosen note; the tie mark flags notes
    whose position was decided by glossary order inside a tie set."""
    if tied:
        return u"%s (%s\u00b7%s)" % (term, _hits_label(hits), TIE_MARK)
    return u"%s (%s)" % (term, _hits_label(hits))


def build_leadin(cfg, glossary):
    """Return dict(form, paragraph, notes, note_readings, deferred,
    unglossed, motif, motif_exact)."""
    lines = card_lines(cfg)
    form = detect_form(cfg)
    ranked = matched_units(lines, glossary)
    chosen, deferred = ranked[:MAX_NOTES], ranked[MAX_NOTES:]
    notes = [u["note"] for u, _ in chosen]
    unglossed = unglossed_terms(lines, glossary)
    motif, motif_exact = extract_motif(cfg, glossary)
    setting = glossary.get("city_setting", [])
    parts = list(setting)
    if form == "REACT":
        parts.append(glossary.get("react_two_state", ""))
    parts.extend(notes)
    if form == "DIGEST":
        parts.append(motif + u"\u3002")
    paragraph = "".join(p for p in parts if p)
    hit_counts = [h for _, h in ranked]
    boundary = chosen[-1][1] if chosen else 0
    note_readings = [
        note_reading(u["terms"][0], h, hit_counts.count(h) > 1)
        for u, h in chosen
    ]
    deferred_readings = [
        deferred_reading(u["terms"][0], h, boundary)
        for u, h in deferred
    ]
    return {
        "form": form,
        "paragraph": paragraph,
        "notes": notes,
        "note_readings": note_readings,
        "deferred": deferred_readings,
        "unglossed": unglossed,
        "motif": motif,
        "motif_exact": motif_exact,
    }


def render_md(cfg, result, glossary):
    topic = cfg.get("meta", {}).get("topic", "")
    lines = [
        u"# M5 \u53d1\u5e03\u6848\u5bfc\u8bed\u6bb5\u8349\u7a3f\uff08" + topic + u"\uff09",
        u"",
        result["paragraph"],
        u"",
        u"---",
        u"<!-- editor footer (design-state draft; publish opens with M5 account physicals) -->",
    ]
    if result["note_readings"]:
        lines.append(u"<!-- NOTES density basis (top-%d by per-card hits): %s -->"
                     % (MAX_NOTES, u"\u3001".join(result["note_readings"])))
    if result["deferred"]:
        lines.append(u"<!-- DEFERRED glossary units (beyond top-%d notes): %s -->"
                     % (MAX_NOTES, u"\u3001".join(result["deferred"])))
    if result["unglossed"]:
        lines.append(u"<!-- UNGLOSSED jargon (extend leadin-glossary.json): %s -->"
                     % u"\u3001".join(result["unglossed"]))
    if not result["motif_exact"]:
        lines.append(u"<!-- MOTIF fallback used (no \u300c...\u300d\u6bcd\u9898 in editorial_value) -->")
    lines.append(u"<!-- generated %s by tools/lcard_leadin.py (tech#194/#200/#204) -->"
                 % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="L-card off-card lead-in builder (tech#194)")
    ap.add_argument("--cards", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--check", action="store_true", help="gate only: exit 1 on unglossed jargon, no write")
    args = ap.parse_args(argv)

    with io.open(args.cards, encoding="utf-8") as f:
        cfg = json.load(f)
    glossary = load_glossary()
    result = build_leadin(cfg, glossary)

    print("form=%s notes=%d deferred=%d unglossed=%d motif_exact=%s"
          % (result["form"], len(result["notes"]), len(result["deferred"]),
             len(result["unglossed"]), result["motif_exact"]))
    for note, reading in zip(result["notes"], result["note_readings"]):
        print("NOTE %s: %s" % (reading, note))
    for t in result["deferred"]:
        print("DEFERRED: " + t)
    for t in result["unglossed"]:
        print("UNGLOSSED: " + t)

    if args.check:
        return 1 if result["unglossed"] else 0
    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.cards)), "leadin.md")
    with io.open(out, "w", encoding="utf-8") as f:
        f.write(render_md(cfg, result, glossary))
    print("WROTE " + out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
