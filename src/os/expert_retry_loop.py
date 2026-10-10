#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""expert_retry_loop: patient retry wrapper for call_expert --gpu-guard.

A DEFER from call_expert (rc=5, GPU window closed, tech#44 guard) is retried
every --interval seconds up to --max attempts. Any non-defer result (success
rc=0 / usage rc=2 / call-fail rc=3) stops the loop and propagates that exit
code. Exhausting all attempts on defer exits 4 (LOOP-EXHAUSTED), distinct
from every call_expert code. Defer telemetry itself is call_expert's own
ledger row (tech#89 gpu-guard-defer-ledger), so this wrapper keeps no
duplicate ledger.

Production anchors (the one-off pattern this CLI retires):
- R1943: E4 audience probe double-defer, manual same-round refire;
- R1948: hand-written ps1 retry loop (45s sweep x24 cap) landed the verdict
  same-round at 06:53:07 after 6 defers -- the pattern works, the hand copy
  is the gap. Future fire-window review legs (E4/E8/S1 on MD-0002, SC
  series, REACT re-flights) reuse one command instead of a new ad-hoc file.

ASCII rule: this source is pure ASCII; Chinese lives in data files.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time

DEFAULT_TIMEOUT = 1500
DEFAULT_INTERVAL = 45.0
DEFAULT_MAX = 24
DEFER_RC = 5          # call_expert --gpu-guard defer exit code
EXHAUSTED_RC = 4      # loop burned all attempts on defers (distinct space)
DEFAULT_CALL_EXPERT = "src/call_expert.py"


def build_argv(expert, material, timeout_s, call_expert_path):
    """Argv for one call_expert attempt (guard on, timeout explicit)."""
    return [
        sys.executable, call_expert_path,
        "--expert", expert,
        "--material", material,
        "--timeout", str(timeout_s),
        "--gpu-guard",
    ]


def _default_runner(argv):
    """Run one attempt; returns (rc, combined_output). Never raises."""
    try:
        p = subprocess.run(
            argv, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
        )
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except OSError as exc:  # python/call_expert missing -> usage-class stop
        return 2, "expert_retry_loop: cannot run call_expert: %s\n" % exc


def retry_loop(expert, material, timeout_s, interval_s, max_attempts,
               runner=None, sleeper=None, log=None):
    """Drive attempts until non-defer or exhaustion. Returns final rc.

    runner: callable(argv) -> (rc, text); injected in tests.
    sleeper: callable(seconds); injected in tests.
    log: callable(line); injected in tests.
    No sleep after the final attempt (defer or not).
    """
    if runner is None:
        runner = _default_runner
    if sleeper is None:
        sleeper = time.sleep
    if log is None:
        log = lambda line: print(line, flush=True)  # noqa: E731
    argv = build_argv(expert, material, timeout_s, DEFAULT_CALL_EXPERT)
    for i in range(1, max_attempts + 1):
        rc, out = runner(argv)
        if rc == DEFER_RC:
            log("attempt %d/%d DEFER (gpu window closed), waiting %gs" % (i, max_attempts, interval_s))
            if i < max_attempts:
                sleeper(interval_s)
            continue
        log("attempt %d/%d non-defer rc=%d" % (i, max_attempts, rc))
        if out and out.strip():
            log(out.rstrip())
        return rc
    log("loop exhausted: %d defer(s), no window landed" % max_attempts)
    return EXHAUSTED_RC


def _positive_int(value):
    iv = int(value)
    if iv <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer: %r" % value)
    return iv


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="expert_retry_loop",
        description="Retry call_expert --gpu-guard through defer windows until it lands.",
    )
    parser.add_argument("--expert", required=True, help="expert id, as call_expert")
    parser.add_argument("--material", required=True, help="material file path, as call_expert")
    parser.add_argument("--timeout", type=_positive_int, default=DEFAULT_TIMEOUT,
                        help="per-attempt call_expert timeout seconds (default %(default)s)")
    parser.add_argument("--interval", type=float, default=DEFAULT_INTERVAL,
                        help="seconds between defer retries (default %(default)s)")
    parser.add_argument("--max", dest="max_attempts", type=_positive_int, default=DEFAULT_MAX,
                        help="max attempts, defers included (default %(default)s)")
    args = parser.parse_args(argv)
    if args.interval < 0:
        parser.error("--interval must be >= 0")
    rc = retry_loop(
        args.expert, args.material, args.timeout, args.interval, args.max_attempts,
    )
    sys.exit(rc)


if __name__ == "__main__":
    main()
