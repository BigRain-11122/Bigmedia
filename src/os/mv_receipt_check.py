# -*- coding: utf-8 -*-
"""MV V5 re-run receipt check (D-20261024-06, R2431).

Why this exists: `full_mv_v701~v705` landing on disk looked like a
receipt while a repair loop was still rewriting them and no director
review existed. D-20261024-06 therefore fixes three pieces that must
all be present before "the re-run answered the order":

    (a) every one of the 17 re-rendered shots is on disk in
        `bmc/i2v/v5redo/`
    (b) the edit grammar probe reads hard-cut 54 / dissolve 7 /
        defocus 2 / deep-slow 3
    (c) a `DIRECTOR-REVIEW-V5-PASS` file exists (or an explicit
        failure list plus re-shoot order -- never "v7xx exists")

Anything less is `ABSENT`, and the report says which piece is missing
so the 23:25 receipt window verdict is mechanical instead of a mood.

    python src/os/mv_receipt_check.py [--json] [--no-write]

Exit codes: 0 receipt complete; 2 receipt absent (window still open).

ASCII rule: this source is pure ASCII.
"""
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / "data" / "pipeline" / "mv-receipt-check.jsonl"

EXPECTED_SHOTS = int(os.environ.get("MV_V5REDO_SHOTS", "17"))
EXPECTED_GRAMMAR = {"hard_cut": 54, "dissolve": 7, "defocus": 2,
                    "deep_slow": 3}

SHOT_DIRS = [
    REPO / "outbound" / "bmc" / "i2v" / "v5redo",
    REPO / "outbound" / "i2v" / "v5redo",
    REPO / "data" / "storylines" / "drama" / "mv0001" / "v5redo",
]
PLAN_DIRS = [REPO / "outbound", REPO / "output" / "renders"]
REVIEW_DIRS = [REPO / "outbound", REPO / "qa",
               REPO / "data" / "storylines" / "drama" / "mv0001"]

STATUS_PRESENT = "present"
STATUS_MISSING = "missing"


def shot_numbers(names):
    """Distinct integer shot ids found in filenames (pure)."""
    found = set()
    for name in names:
        for token in re.findall(r"\d{1,4}", Path(name).stem):
            found.add(int(token))
    return sorted(found)


def check_shots(dir_path=None, expected=None):
    """(status, detail) for criterion (a)."""
    need = expected if expected is not None else EXPECTED_SHOTS
    folder = Path(dir_path) if dir_path is not None else SHOT_DIRS[0]
    if not folder.is_dir():
        return STATUS_MISSING, "no shot folder at %s" % folder
    have = shot_numbers([p.name for p in folder.iterdir() if p.is_file()])
    if len(have) >= need:
        return STATUS_PRESENT, "%d shot ids: %s" % (
            len(have), ",".join(str(n) for n in have))
    return STATUS_MISSING, "%d/%d shot ids (%s)" % (
        len(have), need, ",".join(str(n) for n in have) or "none")


def grammar_counts(plan):
    """Normalize a plan dict to the four grammar counters (pure)."""
    keys = {
        "hard_cut": ("hard_cut", "hardcut", "hard", "cut"),
        "dissolve": ("dissolve", "crossfade"),
        "defocus": ("defocus", "blur"),
        "deep_slow": ("deep_slow", "deepslow", "slow"),
    }
    flat = {}
    for key, aliases in keys.items():
        for alias in aliases:
            if alias in plan:
                try:
                    flat[key] = int(plan[alias])
                except (TypeError, ValueError):
                    pass
                break
    return flat


def check_grammar(dirs=None, expected=None):
    """(status, detail) for criterion (b): an edit-grammar reading."""
    want = expected if expected is not None else EXPECTED_GRAMMAR
    search = dirs if dirs is not None else PLAN_DIRS
    best = None
    for folder in search:
        if not Path(folder).is_dir():
            continue
        for plan_path in sorted(Path(folder).rglob("full_mv_v7*.json")):
            try:
                plan = json.loads(plan_path.read_text(
                    encoding="utf-8", errors="replace"))
            except (OSError, ValueError):
                continue
            if isinstance(plan, dict):
                counts = grammar_counts(plan)
                if counts:
                    best = (plan_path, counts)
    if best is None:
        return STATUS_MISSING, "no v7 edit-grammar reading on disk"
    plan_path, counts = best
    gaps = {k: (counts.get(k), v) for k, v in want.items()
            if counts.get(k) != v}
    if gaps:
        rendered = ", ".join("%s %s/%s" % (k, got, exp)
                             for k, (got, exp) in gaps.items())
        return STATUS_MISSING, "grammar off at %s: %s" % (
            plan_path.name, rendered)
    return STATUS_PRESENT, "grammar matches at %s" % plan_path.name


def check_review(dirs=None):
    """(status, detail) for criterion (c): a PASS or an explicit
    failure list plus re-shoot order (never a rendered file)."""
    search = dirs if dirs is not None else REVIEW_DIRS
    for folder in search:
        if not Path(folder).is_dir():
            continue
        for path in sorted(Path(folder).rglob("*DIRECTOR-REVIEW-V5-PASS*")):
            if path.is_file() and path.stat().st_size > 0:
                try:
                    return STATUS_PRESENT, str(path.relative_to(REPO))
                except ValueError:
                    return STATUS_PRESENT, str(path)
    return STATUS_MISSING, "no DIRECTOR-REVIEW-V5-PASS file"


def verdict(results):
    """'RECEIVED' only when all three pieces are present (pure)."""
    return "RECEIVED" if all(s == STATUS_PRESENT for s, _ in results) \
        else "ABSENT"


def build_report(shots, grammar, review, ts=None):
    """Pure: one JSONL row + the human verdict dict."""
    stamp = ts or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results = [shots, grammar, review]
    return {
        "ts": stamp,
        "verdict": verdict(results),
        "shots": {"status": shots[0], "detail": shots[1]},
        "grammar": {"status": grammar[0], "detail": grammar[1]},
        "review": {"status": review[0], "detail": review[1]},
    }


def append_row(report, path=None):
    """Best-effort JSONL append; a write failure never changes verdict."""
    try:
        target = Path(path) if path is not None else LEDGER
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as f:
            f.write(json.dumps(report, ensure_ascii=False) + "\n")
        return True
    except OSError:
        return False


def main(argv):
    as_json = no_write = False
    for arg in argv[1:]:
        if arg == "--json":
            as_json = True
        elif arg == "--no-write":
            no_write = True
        else:
            print("usage: python src/os/mv_receipt_check.py "
                  "[--json] [--no-write]")
            return 2
    shots = check_shots()
    grammar = check_grammar()
    review = check_review()
    report = build_report(shots, grammar, review)
    if not no_write and not append_row(report):
        print("WARN receipt ledger append failed (verdict kept)")
    if as_json:
        print(json.dumps(report, ensure_ascii=False))
    else:
        print("mv receipt: %s (D-20261024-06 three pieces)" %
              report["verdict"])
        for key in ("shots", "grammar", "review"):
            print("  %-7s %-7s %s" % (key, report[key]["status"],
                                       report[key]["detail"]))
    return 0 if report["verdict"] == "RECEIVED" else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))