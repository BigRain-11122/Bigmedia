#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Drama line takt probe: MD-0001 single-piece wall-clock back-measurement.

P3 explore.md #1 deliverable (R-20261009-bigstream-01 companion tool).
Reads the OS loop state log for the MD-0001 chain rounds (R1782-R1795)
and probes artifact mtimes on disk, so the takt table in the research
piece stays reproducible for MD-0002+ re-measurement.

ASCII-only stdout (PS 5.1 console safe); full table goes to --out (UTF-8).
Zero LLM, zero network, read-only.
"""
import argparse
import datetime
import json
import os
import re
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAIN_FIRST = 1782
CHAIN_LAST = 1795

# Log lines carry placeholder timestamps like "21:0x" / "01:04x" (minute-level
# x-masking convention). Normalize to minute precision; x -> dropped digit.
ROUND_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2}) (\d{1,2}):(\d{1,2})x?(?::\d{2})?x?\s+R(1[78]\d{2})[: ]")

ARTIFACTS = [
    "data/storylines/drama/md0001/SCRIPT-v1.md",
    "data/storylines/drama/md0001/storyboard-schema-v0.1.md",
    "data/storylines/drama/md0001/sources.md",
    "data/storylines/drama/md0001/tts/ROLE-CAST.md",
    "data/storylines/drama/md0001/tts/cast.json",
    "data/storylines/drama/md0001/tts/segments",
    "data/storylines/drama/md0001/tts/refs",
    "data/storylines/drama/md0001/t2i/PACK-v1.json",
    "data/storylines/drama/md0001/t2i/frames",
    "data/storylines/drama/md0001/t2i/frames-v1",
    "data/storylines/drama/md0001/t2i/frames-r1792",
    "data/storylines/drama/md0001/t2i/reroll-r1793",
    "output/renders/md-0001-v1-bilibili-16x9.mp4",
    "data/storylines/drama/md0001/e4-result.json",
]


def parse_round_ts(line):
    """Return (date, hh, mm, round) for a state-log round line, else None."""
    m = ROUND_RE.match(line)
    if not m:
        return None
    return m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))


def extract_chain(log, first=CHAIN_FIRST, last=CHAIN_LAST):
    rows = []
    for line in log:
        p = parse_round_ts(line)
        if not p:
            continue
        date, hh, mm, rnd = p
        if not (first <= rnd <= last):
            continue
        head = line.split("R%d" % rnd, 1)[1].lstrip(": ").strip()
        rows.append({
            "round": rnd,
            "ts": "%s %02d:%02d" % (date, hh, mm),
            "head": head[:80],
        })
    return rows


def _dt(ts):
    return datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M")


def chain_span(chain):
    """Return (total_min, gaps) using log order; gaps may be negative when
    the log carries placeholder-order artifacts (log-order WARN family)."""
    if not chain:
        return 0.0, []
    gaps = []
    for a, b in zip(chain, chain[1:]):
        dmin = (_dt(b["ts"]) - _dt(a["ts"])).total_seconds() / 60.0
        gaps.append((a["round"], b["round"], dmin))
    total = (_dt(chain[-1]["ts"]) - _dt(chain[0]["ts"])).total_seconds() / 60.0
    return total, gaps


def _fmt(epoch):
    return time.strftime("%m-%d %H:%M:%S", time.localtime(epoch))


def artifact_table(root, artifacts=None):
    rows = []
    for rel in (artifacts if artifacts is not None else ARTIFACTS):
        p = os.path.join(root, rel.replace("/", os.sep))
        if not os.path.exists(p):
            rows.append((rel, "ABSENT", "-"))
            continue
        if os.path.isdir(p):
            fs = [os.path.join(p, f) for f in os.listdir(p)
                  if os.path.isfile(os.path.join(p, f))]
            if not fs:
                rows.append((rel, "EMPTY", "-"))
                continue
            mt0 = min(os.path.getmtime(f) for f in fs)
            mt1 = max(os.path.getmtime(f) for f in fs)
            rows.append((rel, "%s -> %s" % (_fmt(mt0), _fmt(mt1)),
                         "n=%d span=%.1fmin" % (len(fs), (mt1 - mt0) / 60.0)))
        else:
            rows.append((rel, _fmt(os.path.getmtime(p)), "n=1"))
    return rows


def build_report(state_path, root):
    st = json.load(open(state_path, encoding="utf-8"))
    chain = extract_chain(st.get("log", []))
    total, gaps = chain_span(chain)
    lines = ["MD-0001 chain rounds R%d-R%d: n=%d" % (CHAIN_FIRST, CHAIN_LAST, len(chain))]
    for r in chain:
        lines.append("  R%d %s  %s" % (r["round"], r["ts"], r["head"]))
    lines.append("chain wall span (log order): %.0f min" % total)
    lines.append("inter-round gaps (min): " + ", ".join(
        "%d->%d %.0f" % g for g in gaps))
    lines.append("")
    lines.append("artifacts (disk mtime truth):")
    for rel, when, extra in artifact_table(root):
        lines.append("  %-58s %-32s %s" % (rel, when, extra))
    return "\n".join(lines), len(chain), total


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--state", default=os.path.join(REPO, "src", "os", "state.json"))
    ap.add_argument("--root", default=REPO)
    ap.add_argument("--out", help="UTF-8 report file (full table incl. CJK heads)")
    args = ap.parse_args()
    report, n, total = build_report(args.state, args.root)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report + "\n")
    print("TAKT_OK rounds=%d wall_min=%.0f out=%s" % (n, total, args.out or "stdout-only"))


if __name__ == "__main__":
    main()
