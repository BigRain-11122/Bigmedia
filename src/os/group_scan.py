# -*- coding: utf-8 -*-
"""Group-transfer scan probe -- fixed single-truth face for the task-book
group-scan step (state/queue/tech#50).

Why (R1849 + R1879 incident family): the group-scan step used to be rebuilt
as an ad-hoc python one-liner every round, and two regex slips produced
false-quiet readings (R1849: a ``2026\\d{3}`` month-face pattern missed the
1010+ date family; R1879: a two-digit-month pattern failed the whole 8-digit
date family and read CUR=0 as quiet). This probe locks the dnum regex to the
8-digit date family, diffs the token set against the state watermark, and
FAILS loudly on read errors instead of falling back silent
(PT-20260928-01 family).

Faces:
  DECISIONS  dnum watermark diff (TRULY_NEW breaks silence -> rc 1;
            watermark-only tokens are the slim/inline-consumed family and
            are never reported as new)
  LEDGER     transfer-marker line anchors (@BigStream family + the
            @七线全司/@全司/@六司/@八线全量 patrol markers)
  MTIME      HQ orders/decisions/ledger anchors + own orders newest file

Usage:
    python src/os/group_scan.py                # print full report
    python src/os/group_scan.py --out FILE      # + UTF-8 (no BOM) evidence
    python src/os/group_scan.py --out FILE --echo

Exit codes: 0 quiet / 1 new dnum tokens / 2 usage error / 3 face read
error. Task-book wiring of this probe is an operator-domain submission
(mandate); the loop itself does not edit the mandate file.
"""

import io
import json
import re
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GROUP_ROOT = REPO.parent.parent

# 8-digit date family (YYYYMMDD). The two incident patterns (2026\d{3} and a
# 2-digit-month face) both under-matched real dnums; this one is locked by
# tests/test_group_scan.py regression cases.
DNUM_RE = re.compile(r"\b[DC]-20\d{6}-\d{1,3}(?!\d)")
# Only whitespace / list / heading markers may precede a row-anchored token.
ANCHOR_PREFIX_RE = re.compile(r"^(?:\s|[-*#>]+|\d{1,3}[.)])*$")
LEDGER_MARKERS = ("@BigStream", "@七线全司", "@全司", "@六司", "@八线全量")
PREVIEW_LEN = 110

RC_QUIET, RC_NEW, RC_USAGE, RC_READ_FAIL = 0, 1, 2, 3
USAGE = ("usage: python src/os/group_scan.py [--out FILE] [--echo] "
         "[--decisions P] [--hq-orders P] [--ledger P] "
         "[--own-orders-dir P] [--state P]")

DEFAULTS = {
    "decisions": GROUP_ROOT / "docs" / "decisions.md",
    "hq_orders": GROUP_ROOT / "docs" / "orders.md",
    "ledger": GROUP_ROOT / "cph4" / "evolution-ledger.md",
    "own_orders_dir": REPO / "orders",
    "state": REPO / "src" / "os" / "state.json",
}


def read_text(path):
    """Return (text, mtime_str, size); raise OSError so callers FAIL loud."""
    path = Path(path)
    stat = path.stat()
    with io.open(str(path), encoding="utf-8-sig", errors="replace") as fh:
        text = fh.read()
    mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    return text, mtime, stat.st_size


def extract_dnums(text):
    """Token set over the 8-digit date family (R1849/R1879 regression lock)."""
    return set(DNUM_RE.findall(text))


def is_anchor_prefix(prefix):
    """True when only whitespace/list/heading markers precede the token."""
    return ANCHOR_PREFIX_RE.match(prefix) is not None


def classify_tokens(text):
    """token -> 'row' | 'inline' (inline-only = pseudo-diff annotation)."""
    kinds = {}
    for line in text.splitlines():
        for match in DNUM_RE.finditer(line):
            token = match.group(0)
            if kinds.get(token) == "row":
                continue
            kinds[token] = "row" if is_anchor_prefix(line[:match.start()]) else "inline"
    return kinds


def diff_watermark(cur_tokens, watermark):
    """(truly_new, wm_only): watermark-only tokens are slim/inline-consumed."""
    wm = set(watermark)
    cur = set(cur_tokens)
    return sorted(cur - wm), sorted(wm - cur)


def load_watermark(state_path):
    """Watermark dnum list from state.json; missing field = empty (loud side)."""
    with io.open(str(state_path), encoding="utf-8") as fh:
        data = json.load(fh)
    return list(data.get("decisions_watermark", {}).get("dnums", []))


def scan_ledger(text):
    """{marker: (lines, occurrences)} plus last @BigStream line preview."""
    stats = {}
    last_line = None
    for line in text.splitlines():
        for marker in LEDGER_MARKERS:
            occ = line.count(marker)
            if occ:
                lines, total = stats.get(marker, (0, 0))
                stats[marker] = (lines + 1, total + occ)
        if "@BigStream" in line and line.strip():
            last_line = line.strip()
    preview = tail_preview(last_line) if last_line else ""
    return stats, preview


def tail_preview(line, limit=PREVIEW_LEN):
    """One-line anchor preview (truncated, never multi-line)."""
    line = (line or "").strip()
    if len(line) > limit:
        return line[:limit] + " ..."
    return line


def last_content_line(text):
    for line in reversed(text.splitlines()):
        if line.strip():
            return line.strip()
    return ""


def own_orders_top(directory):
    """Newest file in own orders dir -> (name, mtime_str, size) or None."""
    directory = Path(directory)
    best = None
    for path in directory.glob("*"):
        if not path.is_file():
            continue
        stat = path.stat()
        if best is None or stat.st_mtime > best[1]:
            best = (path.name, stat.st_mtime, stat.st_size)
    if best is None:
        return None
    name, mtime, size = best
    return (name, datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S"),
            size)


def face_decisions(paths):
    """Face 1: dnum watermark diff. rc 0 quiet / 1 new / 3 read error."""
    try:
        text, mtime, size = read_text(paths["decisions"])
    except OSError as exc:
        return RC_READ_FAIL, "read-fail: decisions %r" % (exc,)
    try:
        watermark = load_watermark(paths["state"])
    except (OSError, ValueError) as exc:
        return RC_READ_FAIL, "read-fail: state %r" % (exc,)

    tokens = extract_dnums(text)
    kinds = classify_tokens(text)
    truly_new, wm_only = diff_watermark(tokens, watermark)
    lines = [
        "file: %s | mtime %s | %d B | tokens=%d" % (
            paths["decisions"], mtime, size, len(tokens)),
        "watermark=%d | truly_new=%d | wm_only=%d (slim/inline-consumed family)"
        % (len(watermark), len(truly_new), len(wm_only)),
    ]
    if truly_new:
        annotated = ["%s [%s]" % (t, kinds.get(t, "row")) for t in truly_new]
        lines.append("TRULY_NEW: " + ", ".join(annotated))
    else:
        lines.append("TRULY_NEW: (none)")
    if wm_only:
        lines.append("wm_only: " + ", ".join(wm_only))
    return (RC_NEW if truly_new else RC_QUIET), "\n".join(lines)


def face_ledger(paths):
    """Face 2: transfer-marker line anchors. rc 0 / 3 read error."""
    try:
        text, mtime, size = read_text(paths["ledger"])
    except OSError as exc:
        return RC_READ_FAIL, "read-fail: ledger %r" % (exc,)
    stats, preview = scan_ledger(text)
    lines = ["file: %s | mtime %s | %d B" % (paths["ledger"], mtime, size)]
    for marker in LEDGER_MARKERS:
        hit_lines, occ = stats.get(marker, (0, 0))
        lines.append("%s lines=%d occurrences=%d" % (marker, hit_lines, occ))
    if preview:
        lines.append("last-@BigStream: " + preview)
    return RC_QUIET, "\n".join(lines)


def face_mtime(paths):
    """Face 3: HQ + own orders anchor readings. rc 0 / 3 read error."""
    lines = []
    rc = RC_QUIET
    try:
        orders_text, orders_mtime, orders_size = read_text(paths["hq_orders"])
    except OSError as exc:
        return RC_READ_FAIL, "read-fail: hq-orders %r" % (exc,)
    try:
        dec_text, dec_mtime, dec_size = read_text(paths["decisions"])
        led_mtime_line = ""
    except OSError as exc:
        dec_mtime, dec_size, dec_text = None, None, None
        rc = RC_READ_FAIL
        led_mtime_line = "decisions read-fail: %r" % (exc,)
    try:
        _, led_mtime, led_size = read_text(paths["ledger"])
    except OSError as exc:
        rc = RC_READ_FAIL
        led_mtime = led_size = None
        lines.append("ledger read-fail: %r" % (exc,))

    lines.append("hq-orders | %s | %d B" % (orders_mtime, orders_size))
    lines.append("hq-orders-tail: " + tail_preview(last_content_line(orders_text)))
    if dec_mtime is not None:
        lines.append("hq-decisions | %s | %d B" % (dec_mtime, dec_size))
        lines.append("hq-decisions-tail: " + tail_preview(last_content_line(dec_text)))
    if led_mtime_line:
        lines.append(led_mtime_line)
    if led_mtime is not None:
        lines.append("ledger | %s | %d B" % (led_mtime, led_size))

    own = Path(paths["own_orders_dir"])
    if not own.exists():
        rc = RC_READ_FAIL
        lines.append("own-orders: dir missing")
    else:
        top = own_orders_top(own)
        if top is None:
            lines.append("own-orders: (no files)")
        else:
            lines.append("own-orders-top | %s | %s | %d B" % top)
    return rc, "\n".join(lines)


def render_report(faces, ts):
    lines = ["# group-scan %s" % ts]
    for name, rc, text in faces:
        lines.append("=== %s (rc=%d) ===" % (name, rc))
        if text:
            lines.append(text)
    return "\n".join(lines) + "\n"


def write_report(path, text):
    """UTF-8 without BOM by design (PS 5.1 `>` trap root-fix)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(str(path), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return path


def overall_rc(faces):
    return max([rc for _, rc, _ in faces] + [RC_QUIET])


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    paths = dict(DEFAULTS)
    out_path, echo = None, False
    args = argv[1:]
    i = 0
    while i < len(args):
        key = args[i]
        if key in ("--decisions", "--hq-orders", "--ledger", "--own-orders-dir",
                   "--state"):
            if i + 1 >= len(args):
                print(USAGE)
                return RC_USAGE
            paths[key[2:].replace("-", "_")] = args[i + 1]
            i += 2
        elif key == "--out" and i + 1 < len(args):
            out_path = args[i + 1]
            i += 2
        elif key == "--echo":
            echo = True
            i += 1
        else:
            print(USAGE)
            return RC_USAGE

    faces = [
        ("DECISIONS", *face_decisions(paths)),
        ("LEDGER", *face_ledger(paths)),
        ("MTIME", *face_mtime(paths)),
    ]
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = render_report(faces, ts)

    if out_path is not None:
        path = write_report(out_path, report)
        print("group-scan: overall_rc=%d" % overall_rc(faces))
        for name, rc, _ in faces:
            print("  %s: rc=%d" % (name, rc))
        print("written: %s (%d bytes, utf-8 no-bom)"
              % (path, len(report.encode("utf-8"))))
        if echo:
            print(report, end="")
    else:
        print(report, end="")
    return overall_rc(faces)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
