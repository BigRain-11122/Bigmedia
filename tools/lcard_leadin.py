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


def matched_units(lines, glossary):
    """Glossary units whose any term appears in the card lines, in priority order."""
    blob = "\n".join(lines)
    out = []
    for unit in glossary.get("units", []):
        if any(t in blob for t in unit.get("terms", [])):
            out.append(unit)
    return out


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


def build_leadin(cfg, glossary):
    """Return dict(form, paragraph, notes, deferred, unglossed, motif, motif_exact)."""
    lines = card_lines(cfg)
    form = detect_form(cfg)
    units = matched_units(lines, glossary)
    chosen, deferred = units[:MAX_NOTES], units[MAX_NOTES:]
    notes = [u["note"] for u in chosen]
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
    return {
        "form": form,
        "paragraph": paragraph,
        "notes": notes,
        "deferred": [u["terms"][0] for u in deferred],
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
    if result["deferred"]:
        lines.append(u"<!-- DEFERRED glossary units (beyond top-%d notes): %s -->"
                     % (MAX_NOTES, u"\u3001".join(result["deferred"])))
    if result["unglossed"]:
        lines.append(u"<!-- UNGLOSSED jargon (extend leadin-glossary.json): %s -->"
                     % u"\u3001".join(result["unglossed"]))
    if not result["motif_exact"]:
        lines.append(u"<!-- MOTIF fallback used (no \u300c...\u300d\u6bcd\u9898 in editorial_value) -->")
    lines.append(u"<!-- generated %s by tools/lcard_leadin.py (tech#194) -->"
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
    for note in result["notes"]:
        print("NOTE: " + note)
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
