# -*- coding: utf-8 -*-
"""GPU ledger attribution analyzer (P2 tech#16, self-drive 2/7.1).

Reads the P-33 collector ledger (BigCompute state/gpu-util/samples.jsonl,
one JSON row per ~15min sample: ts / util_pct / mem_used_mib / power_w)
and splits the utilization picture into attribution bands so the weekly
8%-mean reading can be judged against the only enforcement line
(self-drive 7.1: 3 consecutive watch windows below 30% with no
protected-state exemption = name-and-shame row).

Zero LLM, pure ledger analysis. Same parsing discipline as
weekly_report.gpu_ledger_weekly: malformed / out-of-window rows are
skipped, never guessed; a missing ledger degrades to an honest error.

Usage:
    python src/gpu_attribution.py [--since YYYY-MM-DD] [--until YYYY-MM-DD]
                                  [--ledger PATH] [--json PATH]

Defaults: full ledger window. Output: compact report to stdout, plus
optional machine-readable JSON dump.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

# Reuse the weekly_report window filter so day-window semantics stay
# identical to the already-shipped weekly GPU row (tech#8).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from weekly_report import gpu_ledger_weekly  # noqa: E402

DEFAULT_LEDGER = (Path(__file__).resolve().parents[3]
                  / "compute" / "BigCompute" / "state" / "gpu-util"
                  / "samples.jsonl")

# Utilization bands for attribution (percent).
BANDS = [
    ("<10 (idle/keep-warm)", 0.0, 10.0),
    ("10-30 (light)", 10.0, 30.0),
    ("30-70 (workload)", 30.0, 70.0),
    (">=70 (saturated)", 70.0, 101.0),
]

WATCH_WINDOW_HOURS = 6          # watch rounds run 03:07 / 15:07 -> 6h buckets
LOW_LINE = 30.0                 # 7.1 enforcement line (percent util)


def parse_rows(path, since=None, until=None):
    """Ledger rows -> [(dt, util, mem_mib, power_w)], skipping bad rows.

    since/until are inclusive YYYY-MM-DD bounds (None = unbounded).
    """
    rows = []
    try:
        raw = Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise SystemExit("gpu_attribution: cannot read ledger: %s" % exc)
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if not isinstance(rec, dict):
            continue
        ts = str(rec.get("ts", ""))[:19]
        try:
            dt = datetime.fromisoformat(ts)
        except ValueError:
            continue
        if since is not None and dt.date().isoformat() < since:
            continue
        if until is not None and dt.date().isoformat() > until:
            continue
        util = rec.get("util_pct")
        mem = rec.get("mem_used_mib")
        power = rec.get("power_w")
        if not isinstance(util, (int, float)):
            continue
        rows.append((dt,
                     float(util),
                     float(mem) if isinstance(mem, (int, float)) else None,
                     float(power) if isinstance(power, (int, float)) else None))
    return rows


def band_stats(rows):
    """Sample counts per utilization band + share of total."""
    counts = Counter()
    for _, util, _, _ in rows:
        for name, lo, hi in BANDS:
            if lo <= util < hi:
                counts[name] += 1
                break
    total = sum(counts.values())
    return {name: (counts[name], (100.0 * counts[name] / total) if total else 0.0)
            for name, _, _ in BANDS}, total


def group_means(rows, key):
    """Mean util per key(dt) bucket (returns sorted [(key, mean, n)])."""
    buckets = {}
    for dt, util, _, _ in rows:
        buckets.setdefault(key(dt), []).append(util)
    return sorted((k, sum(v) / len(v), len(v)) for k, v in buckets.items())


def watch_windows_low(rows, hours=WATCH_WINDOW_HOURS, line=LOW_LINE):
    """7.1-style reading: 6h watch windows whose mean util < line.

    Returns [(window_start_str, mean, n, low_flag)] sorted by start.
    """
    buckets = {}
    for dt, util, _, _ in rows:
        start = dt.replace(hour=(dt.hour // hours) * hours, minute=0, second=0)
        buckets.setdefault(start, []).append(util)
    out = []
    for start in sorted(buckets):
        vals = buckets[start]
        mean = sum(vals) / len(vals)
        out.append((start.strftime("%Y-%m-%d %H:%M"),
                    round(mean, 1), len(vals), mean < line))
    return out


def consecutive_low_windows(windows):
    """Longest run of consecutive low(<30%) watch windows."""
    best = run = 0
    for _, _, _, low in windows:
        run = run + 1 if low else 0
        best = max(best, run)
    return best


def analyze(path, since=None, until=None):
    rows = parse_rows(path, since, until)
    if not rows:
        raise SystemExit("gpu_attribution: no usable rows in window")
    bands, total = band_stats(rows)
    utils = [r[1] for r in rows]
    mems = [r[2] for r in rows if r[2] is not None]
    report = {
        "ledger": str(path),
        "n": total,
        "first": rows[0][0].isoformat(),
        "last": rows[-1][0].isoformat(),
        "mean_util": round(sum(utils) / len(utils), 1),
        "max_util": round(max(utils), 1),
        "low_share_pct": round(100.0 * sum(1 for u in utils if u < LOW_LINE) / len(utils), 1),
        "bands": {name: {"n": n, "pct": round(pct, 1)} for name, (n, pct) in bands.items()},
        "day_means": [(d, round(m, 1), n) for d, m, n in group_means(rows, lambda dt: dt.date().isoformat())],
        "hour_means": [(h, round(m, 1), n) for h, m, n in group_means(rows, lambda dt: dt.hour)],
        "mem_baseline_mib": round(min(mems), 0) if mems else None,
        "mem_max_mib": round(max(mems), 0) if mems else None,
        "watch_windows": watch_windows_low(rows),
        "max_consecutive_low_windows": consecutive_low_windows(watch_windows_low(rows)),
    }
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--since", default=None, help="YYYY-MM-DD inclusive")
    ap.add_argument("--until", default=None, help="YYYY-MM-DD inclusive")
    ap.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    ap.add_argument("--json", default=None, help="optional JSON dump path")
    args = ap.parse_args(argv)

    rep = analyze(args.ledger, args.since, args.until)
    # Cross-check against the shipped weekly reader (tech#8) on the same
    # window: same source, so means must match; honest hard fail if not.
    # weekly_report.in_window compares against date objects.
    from datetime import date as _date
    wk_since = (_date.fromisoformat(args.since) if args.since
                else _date.fromisoformat(rep["first"][:10]))
    wk_until = (_date.fromisoformat(args.until) if args.until
                else _date.fromisoformat(rep["last"][:10]))
    weekly = gpu_ledger_weekly(Path(args.ledger), wk_since, wk_until)
    if weekly and abs(weekly["mean"] - rep["mean_util"]) > 0.51:
        raise SystemExit("gpu_attribution: cross-check mismatch vs "
                         "weekly_report.gpu_ledger_weekly")

    print("GPU attribution  n=%(n)d  %(first)s -> %(last)s" % rep)
    print("mean=%(mean_util)s%%  max=%(max_util)s%%  <30%%-share=%(low_share_pct)s%%"
          % rep)
    for name, _, _ in BANDS:
        n, pct = rep["bands"][name]["n"], rep["bands"][name]["pct"]
        print("  band %-22s n=%-4d %5.1f%%" % (name, n, pct))
    print("day means:")
    for d, m, n in rep["day_means"]:
        print("  %s  mean=%5.1f%%  n=%d" % (d, m, n))
    print("watch windows (6h, 7.1 line=30%%):")
    for w, m, n, low in rep["watch_windows"]:
        flag = "LOW" if low else "ok"
        print("  %s  mean=%5.1f%%  n=%-3d %s" % (w, m, n, flag))
    print("max consecutive low windows: %d" % rep["max_consecutive_low_windows"])
    if rep["mem_baseline_mib"] is not None:
        print("mem: baseline=%(mem_baseline_mib).0fMiB max=%(mem_max_mib).0fMiB" % rep)
    if args.json:
        Path(args.json).write_text(json.dumps(rep, ensure_ascii=False, indent=1),
                                   encoding="utf-8")
        print("json -> %s" % args.json)


if __name__ == "__main__":
    main()
