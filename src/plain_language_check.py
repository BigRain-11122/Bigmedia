# -*- coding: utf-8 -*-
"""BigStream plain-language wording gate (copy-craft.md section 2.8, L18-L20).

Machine side of the wording law from group order P-2026-09-26-11
("wording must be simple and easy to understand"):

    jargon-title   internal jargon term found in --title      [FAIL]
    jargon-term    internal jargon term hits in spoken text  [WARN]
                   (first line + count per term; whether the first
                   occurrence carries a plain-language gloss is a
                   human/S1 ruling - the machine only lists hits)
    longsentence   sentence >40 chars (punct-stripped) or
                   >=3 commas                          [WARN]

Term list (single machine truth): data/pipeline/jargon-terms.txt
Canonical spec: docs/copy-craft.md section 2.8 (term changes need both).

Usage:
    python src/plain_language_check.py --beats FILE [--srt FILE] [--title "..."]

Exit codes: 0 = PASS (WARN allowed), 1 = any FAIL, 2 = usage error.
This gate is NECESSARY not sufficient: gloss adequacy and abstract-noun
scene support (L18/L20 semantics) stay human/S1 review duties.
"""
import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TERMS_FILE = REPO / "data" / "pipeline" / "jargon-terms.txt"

SENT_SPLIT_RE = re.compile(r"[。！？!?;\n]+")
STRIP_RE = re.compile(r"[\s，。！？、；：:,.\"'“”‘’（）()\[\]【】·—…-]")
COMMA_RE = re.compile(r"[，,]")
SRT_NOISE_RES = (re.compile(r"^\d+\s*$"), re.compile(r"-->"))


def load_terms(path=TERMS_FILE):
    terms = []
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        terms.append(line)
    return terms


def srt_text(raw):
    """Drop srt cue numbers and timestamp lines, keep cue text."""
    kept = [ln for ln in raw.splitlines()
            if not any(rx.search(ln) for rx in SRT_NOISE_RES)]
    return "\n".join(kept)


def check_title(title, terms):
    findings = []
    low = title.lower()
    for t in terms:
        if t.lower() in low:
            findings.append(("FAIL", "jargon-title",
                             "term '%s' in title (L19: no jargon in titles)" % t))
    return findings


def check_text(text, terms, origin):
    findings = []
    lines = text.splitlines()
    for t in terms:
        low_t = t.lower()
        hits = [i for i, ln in enumerate(lines, 1) if low_t in ln.lower()]
        if hits:
            findings.append(("WARN", "jargon-term",
                             "term '%s' first@L%d x%d (%s) - L18: needs gloss "
                             "same/next beat (human ruling)" % (t, hits[0], len(hits), origin)))
    for s in SENT_SPLIT_RE.split(text):
        s = s.strip()
        if not s:
            continue
        n = len(STRIP_RE.sub("", s))
        commas = len(COMMA_RE.findall(s))
        if n > 40 or commas >= 3:
            findings.append(("WARN", "longsentence",
                             "%d chars/%d commas: '%s...'" % (n, commas, s[:24])))
    return findings


def main(argv=None):
    ap = argparse.ArgumentParser(description="Plain-language wording gate (copy-craft 2.8)")
    ap.add_argument("--beats", help="beats/voiceover text file")
    ap.add_argument("--srt", help="subtitle srt file (cue text scanned)")
    ap.add_argument("--title", help="title string to check (FAIL on jargon hit)")
    args = ap.parse_args(argv)

    if not (args.beats or args.srt or args.title):
        print("usage: plain_language_check.py --beats F [--srt F] [--title S]", file=sys.stderr)
        return 2

    try:
        terms = load_terms()
    except OSError as e:
        print("FAIL load-terms %s: %s" % (TERMS_FILE, e), file=sys.stderr)
        return 2

    findings = []
    if args.title:
        findings += check_title(args.title, terms)
    if args.beats:
        raw = Path(args.beats).read_text(encoding="utf-8")
        findings += check_text(raw, terms, Path(args.beats).name)
    if args.srt:
        raw = Path(args.srt).read_text(encoding="utf-8")
        findings += check_text(srt_text(raw), terms, Path(args.srt).name)

    fails = [f for f in findings if f[0] == "FAIL"]
    warns = [f for f in findings if f[0] == "WARN"]
    for sev, code, msg in findings:
        print("%s %s %s" % (sev, code, msg))
    print("SUMMARY terms=%d FAIL=%d WARN=%d" % (len(terms), len(fails), len(warns)))
    print("PASS" if not fails else "FAIL")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
