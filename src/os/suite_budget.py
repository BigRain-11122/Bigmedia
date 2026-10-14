#!/usr/bin/env python3
"""Suite duration budget line (tech#168, R2248).

Root gap: the full regression suite grew to 123.2s/1385 tests (R2247
measurement) - tech#34's negative verdict premise ("full suite <60s
candidate line") has dissolved (2.9x duration, 2.9x cases vs the
10-13 verdict point). A growing verification cost with no budget line
is a structural gap: nothing names the growth, so nothing forces the
layered-suite decision until the cost is already large.

This module is the single-truth classifier for the budget verdict.
The wrapper (tools/run_suite.ps1) emits SUITE_SECONDS=<n> parsed
verbatim from unittest's own "Ran N tests in X.Ys" line (single timing
source: the runner's own clock, no wrapper-side stopwatch); consumers
call classify()/the CLI to name the verdict:

    <  120s  -> OK
    >= 120s  -> WARN        (budget line named: growth visible per-run)
    >= 180s  -> FORCED-EVAL (layered-suite re-evaluation - tech#34
                             re-open - becomes mandatory at the next
                             src-change round)

Selection record (tech#168 three candidates): (1) budget line - THIS
delivery - plus (3) monitoring note (growth curve rides the weekly
report via self_audit) selected; (2) layered suite re-open DEFERRED -
its trigger is the FORCED-EVAL verdict, not a calendar date.

CLI:
    python src/os/suite_budget.py --seconds 123.2
    python src/os/suite_budget.py --result <log>.result   (reads SUITE_SECONDS=)
Output: SUITE_BUDGET=<verdict> <seconds>s budget-line=<WARN at 120s,
FORCED-EVAL at 180s> (tech#168)
rc: 0 = verdict delivered (OK/WARN/FORCED-EVAL are readings, not
failures); 2 = usage/parse error (no verdict fabricated).
"""

import argparse
import math
import re
import sys

BUDGET_WARN_S = 120.0
BUDGET_FORCED_EVAL_S = 180.0

VERDICT_OK = "OK"
VERDICT_WARN = "WARN"
VERDICT_FORCED_EVAL = "FORCED-EVAL"

_RAN_RE = re.compile(r"in (\d+(?:\.\d+)?)s")


def classify(seconds):
    """Pure verdict for a suite duration in seconds.

    Raises TypeError/ValueError on non-numeric, non-finite, or negative
    input - a budget line must never silently swallow a garbage reading
    (a fabricated verdict is worse than a loud parse error).
    """
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)):
        raise TypeError("seconds must be a number (got %r)" % (seconds,))
    if not math.isfinite(seconds):
        raise ValueError("seconds must be finite (got %r)" % (seconds,))
    if seconds < 0:
        raise ValueError("seconds must be >= 0 (got %r)" % (seconds,))
    if seconds >= BUDGET_FORCED_EVAL_S:
        return VERDICT_FORCED_EVAL
    if seconds >= BUDGET_WARN_S:
        return VERDICT_WARN
    return VERDICT_OK


def seconds_from_ran(line):
    """Duration parsed from unittest's 'Ran N tests in X.Ys' line.

    Returns float or None on no match (missing duration is the caller's
    loud problem, never a fabricated 0).
    """
    if not line:
        return None
    m = _RAN_RE.search(line)
    if not m:
        return None
    return float(m.group(1))


def seconds_from_result_file(path):
    """Duration from a run_suite result file.

    Prefers the SUITE_SECONDS= line; falls back to parsing the SUITE_RAN=
    line (pre-tech#168 result files still carry the duration inline).
    Returns float or None when neither carries a parseable duration.
    """
    try:
        with open(path, "r", encoding="utf-8-sig", errors="replace") as fh:
            text = fh.read()
    except OSError:
        return None
    seconds = None
    ran_line = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("SUITE_SECONDS="):
            try:
                return float(stripped.split("=", 1)[1])
            except ValueError:
                continue
        if stripped.startswith("SUITE_RAN=") and ran_line is None:
            ran_line = stripped.split("=", 1)[1]
    if ran_line is not None:
        return seconds_from_ran(ran_line)
    return seconds


def verdict_line(seconds):
    """Machine-readable verdict line for logs and weekly reports."""
    verdict = classify(seconds)
    return ("SUITE_BUDGET=%s %.1fs budget-line=WARN at %ds, FORCED-EVAL at "
            "%ds (tech#168)" % (verdict, seconds, BUDGET_WARN_S,
                                BUDGET_FORCED_EVAL_S))


def main(argv=None):
    ap = argparse.ArgumentParser(description="suite duration budget line")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--seconds", default=None,
                     help="duration in seconds (direct reading)")
    src.add_argument("--result", default=None,
                     help="run_suite result file (reads SUITE_SECONDS=)")
    args = ap.parse_args(argv)

    if args.seconds is not None:
        try:
            seconds = float(args.seconds)
        except ValueError:
            print("SUITE_BUDGET-ERROR unparsable --seconds %r" % args.seconds)
            return 2
    else:
        seconds = seconds_from_result_file(args.result)
        if seconds is None:
            print("SUITE_BUDGET-ERROR no parseable duration in %r" % args.result)
            return 2
    print(verdict_line(seconds))
    return 0


if __name__ == "__main__":
    sys.exit(main())
