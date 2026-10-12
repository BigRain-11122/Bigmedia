# -*- coding: utf-8 -*-
"""BigStream OS-loop queue compact readout (tech#145, R2119 seed).

Gap anchor (R2119 incident): the three self-drive queues are single-long-
line ledgers (tech.md items run ~1700 chars on one physical line). Round
consumption had to dump whole files (3 full reads in one round), and a
280-char truncated view misjudged "[done ...]" marks sitting beyond the
cut as missing -> 6 probe re-scans in one round. The done determination
must run over the FULL line (R2119 fail-closed doctrine: r2119_backfill
ANCHOR-MISS correctly refused to write against a false alarm).

Machine teeth:
  * parse each queue into items: head line `^N. ` at column 0 plus every
    following non-header/non-quote line until the next head (full text
    kept verbatim - no truncation anywhere in classification).
  * done  = full text matches a bracket containing `done YYYY-MM-DD`
    (covers `[done D...]`, `[RNNNN done D...]`, `**[done D...]**` forms
    and marks embedded mid-line or on continuation lines).
  * gated = not done and mentions gated / 观察位 / 到点执行
    (event-window items; not claimable in a normal round).
  * claimable = the rest. Head = first claimable in file order.
  * --item N fetches ONE full item verbatim (zero full-file reads for
    the consumer); unknown number -> exit 2 fail-closed (ANCHOR-MISS
    doctrine: never guess, never silently return empty).
  * default face is <= 15 lines: per-queue done/gated/claimable counts
    plus one claimable-head preview line.

Exit codes: 0 = readout printed, 2 = usage / item-not-found / no queue
file resolvable (fail-closed, mirrors r2119_backfill).

Pure-parse helpers (parse_items / classify_item / classify_queue /
render / build_json) are unit-tested offline; no git, no network.

Usage:
    python src/os/queue_status.py                 # compact 3-queue face
    python src/os/queue_status.py --item 145      # tech #145 full text
    python src/os/queue_status.py --queue main --item 27
    python src/os/queue_status.py --json          # machine face
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

QUEUE_FILES = {
    "main": "state/queue/main.md",
    "tech": "state/queue/tech.md",
    "explore": "state/queue/explore.md",
}
DEFAULT_QUEUE = "tech"
HEAD_PREVIEW_CHARS = 90
MAX_DEFAULT_LINES = 15

_HEAD_RE = re.compile(r"^(\d+)\.\s")
_HEADER_RE = re.compile(r"^[#>]")
# bracket holding `done YYYY-MM-DD` (dated marks only; prose like
# "验读标 done" without a date right after must NOT count as done)
_DONE_RE = re.compile(r"\[[^\[\]]*\bdone\s+(\d{4}-\d{2}-\d{2})[^\[\]]*\]")
# Window-gate markers: literal 'gated', observation/event positions, and
# the two window phrasings that mean gated without the word (calibrated
# against the live queues 2026-10-13: GPU 独占窗即领 / 窗到即领).
# Honest boundary: 判负-closed items (negative verdict, kept on record)
# stay in the claimable bucket on purpose - a bare 判负 mention also
# appears inside OPEN items as a pre-registered judging criterion
# ("不达=判负留痕"), so machine detection would misclassify; the
# preview line surfaces the verdict and the loop still judges.
_GATED_RE = re.compile(r"gated|观察位|到点执行|GPU 独占窗|窗到即领")


def parse_items(text):
    """Split queue text into items.

    Returns a list of dicts {num, head, text} in file order. Continuation
    lines (indented follow-ups, embedded notes) stay attached to their
    item so done-marks anywhere in the item are seen. Header/quote lines
    are ignored.
    """
    items = []
    cur = None
    for raw in text.splitlines():
        m = _HEAD_RE.match(raw)
        if m:
            cur = {"num": int(m.group(1)), "head": raw, "text": raw}
            items.append(cur)
        elif cur is not None and not _HEADER_RE.match(raw):
            cur["text"] += "\n" + raw
    return items


def classify_item(item):
    """Return ('done'|'gated'|'claimable', marker_or_None).

    Done determination runs the regex over the FULL item text (never a
    truncated view) - R2119 fail-closed doctrine.
    """
    m = _DONE_RE.search(item["text"])
    if m:
        return "done", m.group(0)
    if _GATED_RE.search(item["text"]):
        return "gated", None
    return "claimable", None


def classify_queue(items):
    """Bucket items into done/gated/claimable; keep file order."""
    buckets = {"done": [], "gated": [], "claimable": []}
    markers = {}
    for it in items:
        state, marker = classify_item(it)
        buckets[state].append(it)
        markers[it["num"]] = marker
    return buckets, markers


def head_preview(item, limit=HEAD_PREVIEW_CHARS):
    """First claimable-item preview: strip the 'N. ' prefix, truncate."""
    s = item["head"]
    m = _HEAD_RE.match(s)
    if m:
        s = s[m.end():]
    s = s.strip()
    if len(s) > limit:
        s = s[:limit - 3] + "..."
    return s


def load_queue(root, name):
    """Return item list or None when the queue file is missing."""
    path = Path(root) / QUEUE_FILES[name]
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    return parse_items(text)


def build_report(root, names):
    """Read the requested queues; missing files are reported, not fatal
    for the other queues."""
    report = {}
    for name in names:
        items = load_queue(root, name)
        if items is None:
            report[name] = {"missing": True}
            continue
        buckets, markers = classify_queue(items)
        report[name] = {
            "missing": False,
            "total": len(items),
            "done": len(buckets["done"]),
            "gated": len(buckets["gated"]),
            "claimable": len(buckets["claimable"]),
            "claimable_head": (buckets["claimable"][0]
                               if buckets["claimable"] else None),
            "markers": markers,
            "items": items,
        }
    return report


def render(report):
    """Compact face: one line per queue plus totals (<= 15 lines)."""
    lines = ["queue-status %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    tot = {"done": 0, "gated": 0, "claimable": 0}
    for name, face in report.items():
        if face.get("missing"):
            lines.append("%-7s: MISSING (file unreadable)" % name)
            continue
        for k in tot:
            tot[k] += face[k]
        head = face["claimable_head"]
        head_txt = ("head #%d: %s" % (head["num"], head_preview(head))
                    if head else "head: (none claimable)")
        lines.append("%-7s: %d items | done %d | gated %d | claimable %d | %s"
                     % (name, face["total"], face["done"], face["gated"],
                        face["claimable"], head_txt))
    lines.append("total  : done %d | gated %d | claimable %d"
                 % (tot["done"], tot["gated"], tot["claimable"]))
    return lines


def render_item(face, num):
    """--item face: verdict line plus the FULL item text verbatim."""
    for it in face["items"]:
        if it["num"] == num:
            state, marker = classify_item(it)
            out = ["#%d [%s]" % (num, state.upper())]
            if marker:
                shown = marker if len(marker) <= 60 else marker[:59] + "..."
                out.append("marker: %s" % shown)
            out.append(it["text"])
            return out, 0
    return ["item #%d not found in queue - fail-closed, no guess" % num], 2


def build_json(report):
    """Machine face (no full item texts - stays compact)."""
    data = {}
    for name, face in report.items():
        if face.get("missing"):
            data[name] = {"missing": True}
            continue
        head = face["claimable_head"]
        data[name] = {
            "total": face["total"],
            "done": face["done"],
            "gated": face["gated"],
            "claimable": face["claimable"],
            "claimable_head_num": head["num"] if head else None,
        }
    return data


def main(argv=None):
    ap = argparse.ArgumentParser(description="queue compact readout")
    ap.add_argument("--root", default=".",
                    help="repo root (default: cwd)")
    ap.add_argument("--queue", default=DEFAULT_QUEUE,
                    choices=sorted(QUEUE_FILES),
                    help="queue for --item (default: tech)")
    ap.add_argument("--item", type=int, default=None,
                    help="print ONE full item verbatim (fail-closed)")
    ap.add_argument("--json", action="store_true",
                    help="machine-readable face")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()

    if args.item is not None:
        items = load_queue(root, args.queue)
        if items is None:
            print("queue %s unreadable - fail-closed" % args.queue,
                  file=sys.stderr)
            return 2
        face = classify_queue(items)
        report_face = {"items": items}
        out, code = render_item(report_face, args.item)
        for line in out:
            print(line)
        return code

    names = sorted(QUEUE_FILES)
    report = build_report(root, names)
    if all(f.get("missing") for f in report.values()):
        print("no queue file readable under %s - fail-closed" % root,
              file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(build_json(report), ensure_ascii=False))
        return 0
    lines = render(report)
    for line in lines:
        print(line)
    if len(lines) > MAX_DEFAULT_LINES:
        print("warning: default face exceeded %d lines" % MAX_DEFAULT_LINES,
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
