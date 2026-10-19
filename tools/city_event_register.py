#!/usr/bin/env python3
"""city_event_register - append a city-bridge event to the BigStream outbox.

D-20261019-07 / C-20261019-01: BigStream drama/growth-milestone events reach the
city event stream through a FILE BRIDGE, never by writing world-events.jsonl
directly (P-43 single-writer law - the perceptor scan is the only stream
writer). This tool appends one JSON line to output/city-events-outbox.jsonl;
the FluxVerse perceptor probe
(Tools/perceptor/probes/bigstream_city_events.ps1) reads the outbox read-only
and emits each line into world-events.jsonl as MEDIA_OUTPUT / CONTENT_PUBLISH.

Event types (registered in events-registry.json, zero schema change):
  MEDIA_OUTPUT      content production milestone (artifact drop / jman growth
                    milestone / drama beat happening in the city)
  CONTENT_PUBLISH   reserved for a REAL publish only - nothing publishes yet
                    (accounts are a CEO physical-item gate), so this tool
                    accepts the type but the production line must not use it
                    until M5 publish gate is green (honesty law, r47 family).

Laws enforced here:
  - append-only: existing lines are never edited or deleted (probe cursor
    keys are content hashes; an in-place edit would double-fire the event)
  - dedup: an exact (type, summary) duplicate already in the outbox is refused
  - actor/repo/zone pinned to bigstream/bigstream/media (media zone face)
  - summary/ref are the only free fields; summary must be non-empty

Usage:
  python tools/city_event_register.py --type MEDIA_OUTPUT --summary "..." [--ref "..."]
  python tools/city_event_register.py --list
  python tools/city_event_register.py --check   # validate outbox well-formedness
"""
import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTBOX = REPO_ROOT / "output" / "city-events-outbox.jsonl"
ALLOWED_TYPES = ("MEDIA_OUTPUT", "CONTENT_PUBLISH")
ACTOR = "bigstream"
REPO = "bigstream"
ZONE = "media"


def _harden_console_stdio():
    """Console CJK hardening (tech#243 family): PS5.1 console defaults to the
    system codepage (GBK); reconfigure to UTF-8 with errors=replace so list
    output survives capture. No-op when stdout lacks reconfigure (redirect/
    pythonw)."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass


def _load_lines():
    if not OUTBOX.exists():
        return []
    out = []
    for raw in OUTBOX.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            raise SystemExit(f"OUTBOX-DECRYPT-FAIL: unparsable line: {line[:80]}")
        out.append(obj)
    return out


def cmd_register(args):
    if args.type not in ALLOWED_TYPES:
        raise SystemExit(f"TYPE-REFUSED: {args.type} not in {ALLOWED_TYPES}")
    summary = args.summary.strip()
    if not summary:
        raise SystemExit("SUMMARY-EMPTY: refused")
    existing = _load_lines()
    for obj in existing:
        if obj.get("type") == args.type and obj.get("summary") == summary:
            raise SystemExit("DEDUP-REFUSED: identical (type, summary) already in outbox")
    record = {
        "type": args.type,
        "actor": ACTOR,
        "repo": REPO,
        "zone": ZONE,
        "summary": summary,
    }
    if args.ref:
        record["ref"] = args.ref.strip()
    OUTBOX.parent.mkdir(parents=True, exist_ok=True)
    with OUTBOX.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"OK: appended {args.type} -> {OUTBOX} (total lines {len(existing) + 1})")


def cmd_list(_args):
    for i, obj in enumerate(_load_lines(), 1):
        print(f"{i:3d} {obj.get('type')} | {obj.get('summary')}")


def cmd_check(_args):
    objs = _load_lines()
    bad = 0
    for obj in objs:
        if obj.get("type") not in ALLOWED_TYPES:
            print(f"BAD-TYPE: {obj.get('type')}")
            bad += 1
        if not obj.get("summary"):
            print("BAD-SUMMARY: empty")
            bad += 1
        if obj.get("actor") != ACTOR or obj.get("repo") != REPO or obj.get("zone") != ZONE:
            print(f"BAD-FACE: {obj}")
            bad += 1
    print(f"CHECK: {len(objs)} lines, {bad} bad")
    sys.exit(1 if bad else 0)


def main():
    _harden_console_stdio()
    ap = argparse.ArgumentParser(description="BigStream city-bridge event register (append-only outbox)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_reg = sub.add_parser("register")
    p_reg.add_argument("--type", required=True, choices=ALLOWED_TYPES)
    p_reg.add_argument("--summary", required=True)
    p_reg.add_argument("--ref", default="")
    p_reg.set_defaults(func=cmd_register)
    p_list = sub.add_parser("list")
    p_list.set_defaults(func=cmd_list)
    p_chk = sub.add_parser("check")
    p_chk.set_defaults(func=cmd_check)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
