# -*- coding: utf-8 -*-
"""BigStream OS-loop origin-gap pre-check (idle-judgment face, five-check slot 1).

Root cause fix for the R1496(b) push-reject incident (2026-10-06 14:16):
a patrol order (O-20261006-1410-HQ-C / PT-20261006-02, pushed from the
bm-c clone) sat undetected through ~22 waiting rounds because the idle
path only scans the LOCAL orders/ mtime anchor. The loop learned about
the new order only when its own push was rejected. The waiting-object
rescan ban is fine; the blind spot was never asking the remote.

Machine teeth:
  * `git fetch <remote>` (read-only for the working tree), then compare
    local HEAD vs the branch upstream ref (<remote>/<branch>).
  * New/changed files under orders/ coming from origin -> FAIL
    origin-new-orders / origin-orders-changed (breaks the "quiet" state,
    round must go to the full task book and consume the order).
  * Behind / diverged (origin advanced without us) -> FAIL origin-behind
    (rebase before pushing anything, R1496(b) flow).
  * Fetch failure -> FAIL fetch-fail. NEVER silent: PT-20260928-01
    "probe fetch silent-fallback recurrence #3" is the defect family
    this tool exists to starve; a failed check must be loud and exit 1.
  * Quiet (fetched, in sync, nothing new from origin) -> exit 0; this is
    the evidence that slot 1 of the five quiet checks can stand.

Exit codes: 0 = quiet (info notes allowed), 1 = any FAIL, 2 = usage.

Pure-parse helpers (parse_count / classify_diff / build_findings /
render / summarize) are unit-tested offline; no git, no network.

Usage:
    python src/os/origin_gap_check.py [--root DIR] [--remote origin]
                                      [--branch BRANCH] [--timeout N]
                                      [--no-fetch]

    --no-fetch skips the network step and only compares the refs already
    known locally (offline smoke / test mode; a missing local ref still
    reports honestly instead of pretending quiet).
"""

import argparse
import subprocess
import sys
from pathlib import Path

DEFAULT_REMOTE = "origin"
DEFAULT_TIMEOUT = 30

# diff status codes: A added, M modified, D deleted, R renamed (R## forms)
_ORDER_PREFIX = "orders/"


def run_git(args, root, timeout):
    """Run a git command, return (rc, stdout, stderr). Never raises."""
    try:
        p = subprocess.run(
            ["git"] + list(args),
            cwd=str(root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return p.returncode, p.stdout or "", p.stderr or ""
    except subprocess.TimeoutExpired:
        return 124, "", "timeout after %ss" % timeout
    except OSError as exc:  # git missing, cwd gone, ...
        return 125, "", str(exc)


def current_branch(root, timeout):
    rc, out, _ = run_git(["rev-parse", "--abbrev-ref", "HEAD"], root, timeout)
    if rc != 0:
        return None
    name = out.strip()
    return name if name and name != "HEAD" else None


def parse_count(text):
    """'3\\n' -> 3; anything unparsable -> 0 (count queries are exact)."""
    try:
        return int(text.strip())
    except (ValueError, AttributeError):
        return 0


def classify_diff(name_status_lines):
    """Split `git diff --name-status HEAD <upstream>` lines into buckets.

    Returns dict with new_orders / changed_orders / other_files.
    Renames (R100 old new) are attributed to the NEW path.
    """
    new_orders, changed_orders, other_files = [], [], []
    for raw in name_status_lines:
        line = raw.rstrip("\n")
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status = parts[0].strip()
        path = parts[-1].strip()  # rename form: last field = new path
        if path.startswith(_ORDER_PREFIX):
            if status.startswith("A"):
                new_orders.append(path)
            else:
                changed_orders.append(path)
        else:
            other_files.append(path)
    return {
        "new_orders": new_orders,
        "changed_orders": changed_orders,
        "other_files": other_files,
    }


def build_findings(cls, behind, ahead, fetch_rc=None, fetch_err="",
                   upstream_missing=False):
    """Assemble the finding list. Order is stable for readable output."""
    finds = []
    if fetch_rc is not None and fetch_rc != 0:
        finds.append({
            "level": "FAIL", "code": "fetch-fail",
            "text": "git fetch rc=%s (%s) - never silent, fix before "
                    "trusting a quiet idle round" % (fetch_rc,
                                                     fetch_err.strip()[:120]),
        })
    if upstream_missing:
        finds.append({
            "level": "FAIL", "code": "upstream-missing",
            "text": "upstream ref not found locally; cannot compare",
        })
    for path in cls.get("new_orders", []):
        finds.append({
            "level": "FAIL", "code": "origin-new-orders",
            "text": "origin-only new order file %s - break quiet, go to "
                    "the full task book and consume it" % path,
        })
    for path in cls.get("changed_orders", []):
        finds.append({
            "level": "FAIL", "code": "origin-orders-changed",
            "text": "origin changed order file %s - re-read before "
                    "declaring no new orders" % path,
        })
    if behind > 0 and ahead > 0:
        finds.append({
            "level": "FAIL", "code": "diverged",
            "text": "local and origin both advanced (ahead=%d behind=%d); "
                    "rebase before pushing" % (ahead, behind),
        })
    elif behind > 0:
        finds.append({
            "level": "FAIL", "code": "origin-behind",
            "text": "origin is ahead by %d commit(s); pull --rebase before "
                    "the closing push" % behind,
        })
    others = cls.get("other_files", [])
    if behind > 0 and others:
        finds.append({
            "level": "INFO", "code": "origin-other-files",
            "text": "%d non-order file(s) changed on origin (e.g. %s)"
                    % (len(others), others[0]),
        })
    if ahead > 0:
        finds.append({
            "level": "INFO", "code": "local-ahead",
            "text": "%d local commit(s) not pushed yet (round close will "
                    "push)" % ahead,
        })
    return finds


def render(findings, ahead, behind, upstream):
    lines = []
    for f in findings:
        lines.append("- [%s] %s: %s" % (f["level"], f["code"], f["text"]))
    fails = sum(1 for f in findings if f["level"] == "FAIL")
    infos = sum(1 for f in findings if f["level"] == "INFO")
    if not findings:
        lines.append("origin-gap quiet: HEAD == %s (ahead=0 behind=0)"
                     % upstream)
    head = "origin-gap vs %s (ahead=%d behind=%d): %d fail, %d info" % (
        upstream, ahead, behind, fails, infos)
    return [head] + lines


def summarize(findings):
    """(summary_line, exit_code) - quiet only when nothing to say."""
    fails = sum(1 for f in findings if f["level"] == "FAIL")
    if fails:
        return "origin-gap: FINDINGS", 1
    if findings:
        return "origin-gap: QUIET (info only)", 0
    return "origin-gap: QUIET", 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="idle-face origin gap check")
    ap.add_argument("--root", default=".")
    ap.add_argument("--remote", default=DEFAULT_REMOTE)
    ap.add_argument("--branch", default=None,
                    help="branch to compare (default: current)")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    ap.add_argument("--no-fetch", action="store_true",
                    help="skip the network fetch (offline smoke)")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    if not (root / ".git").exists():
        print("usage error: %s is not a git work tree" % root, file=sys.stderr)
        return 2

    fetch_rc, fetch_err = 0, ""
    if not args.no_fetch:
        fetch_rc, _, fetch_err = run_git(
            ["fetch", args.remote, "--quiet"], root, args.timeout)

    branch = args.branch or current_branch(root, args.timeout)
    if not branch:
        print("origin-gap: FAIL cannot resolve current branch (detached?)")
        return 1
    upstream = "%s/%s" % (args.remote, branch)

    rc, out, _ = run_git(
        ["rev-parse", "--verify", "--quiet", "refs/remotes/%s" % upstream],
        root, args.timeout)
    upstream_missing = rc != 0

    cls = {"new_orders": [], "changed_orders": [], "other_files": []}
    behind = ahead = 0
    if not upstream_missing:
        _, out_a, _ = run_git(
            ["rev-list", "--count", "HEAD..%s" % upstream], root, args.timeout)
        _, out_b, _ = run_git(
            ["rev-list", "--count", "%s..HEAD" % upstream], root, args.timeout)
        behind = parse_count(out_a)
        ahead = parse_count(out_b)
        if behind > 0:
            _, diff_out, _ = run_git(
                ["diff", "--name-status", "HEAD", upstream], root,
                args.timeout)
            cls = classify_diff(diff_out.splitlines())

    findings = build_findings(cls, behind, ahead,
                              fetch_rc=fetch_rc, fetch_err=fetch_err,
                              upstream_missing=upstream_missing)
    for line in render(findings, ahead, behind, upstream):
        print(line)
    summary, code = summarize(findings)
    print(summary)
    return code


if __name__ == "__main__":
    sys.exit(main())
