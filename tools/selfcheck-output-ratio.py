#!/usr/bin/env python3
"""selfcheck-output-ratio.py -- 7-day product-vs-bookkeeping commit audit.

Born in R2394 (CEO order 2026-10-19 17:5x, "all companies self-inspect:
rules-chasing with no output"): the daily evolution shift (22:0x) needs
a reproducible git measurement of the product/bookkeeping commit ratio
for DAILY-OUTPUT-REPORT.md, not an ad-hoc .c3-tmp one-liner rebuilt
every day (anti-repetition law).

Classification buckets (commit-level: a commit is "product" when it
touches ANY product path; else "tool" when it touches src/tools/tests;
else "book"):
  product = finished-goods production chains (cards / reviews /
            finished.md / audio / drama / codex / intel daily)
  tool    = pipeline machinery + loop self-iteration code (src, tools, tests)
  book    = pure bookkeeping (state.json / status-export / backlog /
            queues / audits / tmp / logs / governance md / catch-all)

Honesty note (R2394 first measurement): the tool bucket is NOT split
between production-line machinery and loop-mechanism self-iteration;
when that split matters, extend BUCKETS rather than re-classifying by
hand (tech#252).

Usage:
  python tools/selfcheck-output-ratio.py [--since "2026-10-12 18:00"]
                                         [--repo PATH] [--out FILE]
ASCII-only stdout (encoding law); --out writes the same lines as UTF-8.
"""
import argparse
import collections
import datetime
import io
import os
import subprocess
import sys

PRODUCT_PREFIXES = (
    "data/storylines/cards/",
    "data/storylines/audio/",
    "data/storylines/drama/",
    "data/storylines/codex/",
    "docs/reviews/",
    "finished.md",
    "output/finished.md",
    "data/intel/",
)
TOOL_PREFIXES = ("src/", "tools/", "tests/")


def bucket(path):
    p = path.replace("\\", "/")
    if p.startswith(PRODUCT_PREFIXES):
        return "product"
    if p.startswith(TOOL_PREFIXES):
        return "tool"
    return "book"


def git_out(repo, args):
    return subprocess.run(["git"] + args, cwd=repo, capture_output=True,
                          text=True, encoding="utf-8", errors="replace").stdout


def measure(repo, since):
    sep = "@@@COMMIT"
    out = git_out(repo, ["log", "--since=" + since, "--name-only",
                         "--pretty=format:" + sep])
    commits = []
    cur = []
    for line in out.splitlines():
        if line == sep:
            if cur:
                commits.append(cur)
            cur = []
        elif line.strip():
            cur.append(bucket(line.strip()))
    if cur:
        commits.append(cur)

    cnt = collections.Counter()
    for buckets in commits:
        if "product" in buckets:
            cnt["product_commit"] += 1
        elif "tool" in buckets:
            cnt["tool_commit"] += 1
        else:
            cnt["book_commit"] += 1
    filecnt = collections.Counter()
    for buckets in commits:
        for b in buckets:
            filecnt[b] += 1

    total = len(commits)
    lines = ["SINCE=%s TOTAL_COMMITS=%d" % (since, total)]
    for k in ("product_commit", "tool_commit", "book_commit"):
        v = cnt[k]
        pct = ("%.1f%%" % (v * 100.0 / total)) if total else "n/a"
        lines.append("%s=%d (%s)" % (k, v, pct))
    ft = ("file_touches product=%d tool=%d book=%d"
          % (filecnt["product"], filecnt["tool"], filecnt["book"]))
    if total:
        ft += " (book share %.1f%%)" % (
            filecnt["book"] * 100.0 / max(1, sum(filecnt.values())))
    lines.append(ft)
    return lines


def main(argv=None):
    week_ago = (datetime.datetime.now()
                - datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--since", default=week_ago,
                    help='git --since value (default: 7 days back "%s")'
                         % week_ago)
    ap.add_argument("--repo", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), os.pardir))
    ap.add_argument("--out", default=None,
                    help="optional UTF-8 output file (else ASCII stdout)")
    args = ap.parse_args(argv)
    lines = measure(os.path.abspath(args.repo), args.since)
    if args.out:
        with io.open(args.out, "w", encoding="utf-8", newline="") as f:
            f.write("\n".join(lines) + "\n")
    for line in lines:  # ASCII-only by construction
        sys.stdout.write(line + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
