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
  ORDERS     HQ orders.md row watermark (tech#103): |-row count + last-row
            first-cell fingerprint vs state.json orders_row_watermark
            {rows, tail_key}; any deviation breaks silence (rc 1); a
            MISSING watermark is first-run rc 1 with a watermark-missing
            note (consume-then-store once). Root fix: R1975-R1977 rounds
            judged the orders face quiet by mtime-anchor MEMORY comparison
            while three new CEO rows had not yet landed in the local tree
            -- the orders face had no content-addressing judgment at all
            (structural second-class citizen vs the decisions dnum
            watermark).
  DIGEST-SUPPLY  supply-gap advisory backstop for the DIGEST 史源 trigger
            law (#67, tech#129): orders-row dates NEWER than the latest
            DIGEST card date that have sat unconsumed for >2 days break
            silence as a WARN. Historical root: R870/R1095/R1303/R1536/
            R2050 -- five manual "supply-blindspot correction" rounds
            where a new CEO-order cluster dropped and no round re-derived
            it into the DIGEST pool. Machine = hint surface only; the
            creative judgment (A-grade + number-density grading) stays
            with the loop body (no-auto-trigger law). Day-granularity
            note: same-day-evening clusters (e.g. 10-11 晚 vs v18 10-11)
            are below this face's resolution -- the >2d WARN is the
            chronic-blindness backstop, the age<=2d advisory line keeps
            the unconsumed cluster in per-round view. Cards dir missing =
            face inactive (quiet) -- the DIGEST production line itself is
            absent then.
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
from datetime import date, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GROUP_ROOT = REPO.parent.parent

# 8-digit date family (YYYYMMDD). The two incident patterns (2026\d{3} and a
# 2-digit-month face) both under-matched real dnums; this one is locked by
# tests/test_group_scan.py regression cases.
DNUM_RE = re.compile(r"\b[DC]-20\d{6}-\d{1,3}(?!\d)")
# Orders first-cell date shapes: "10-12 13:5x" (MM-DD, current year assumed)
# and the full-date "2026-09-28 18:1x" family (6 live rows). Full-date arm
# first so the 2-digit face cannot steal a slice of it.
ORDERS_CELL_DATE_RE = re.compile(
    r"^(20\d{2})-(\d{2})-(\d{2})(?!\d)|^(\d{2})-(\d{2})(?!\d)")
# DIGEST card dir name: MC-YYYYMMDD-DIGEST-vNN[-tmp]. -tmp staging dirs are a
# legitimate consumption signal (CPU pre-stage counts -- the cluster has been
# derived even while the F-registration waits for a GPU fire window).
DIGEST_CARD_RE = re.compile(r"^MC-(20\d{2})(\d{2})(\d{2})-DIGEST-v\d+")
DIGEST_SUPPLY_GAP_DAYS = 2
# Only whitespace / list / heading markers may precede a row-anchored token.
ANCHOR_PREFIX_RE = re.compile(r"^(?:\s|[-*#>]+|\d{1,3}[.)])*$")
LEDGER_MARKERS = ("@BigStream", "@七线全司", "@全司", "@六司", "@八线全量")
PREVIEW_LEN = 110

RC_QUIET, RC_NEW, RC_USAGE, RC_READ_FAIL = 0, 1, 2, 3
USAGE = ("usage: python src/os/group_scan.py [--out FILE] [--echo] "
         "[--decisions P] [--hq-orders P] [--ledger P] "
         "[--own-orders-dir P] [--state P] [--cards-dir P]")

DEFAULTS = {
    "decisions": GROUP_ROOT / "docs" / "decisions.md",
    "hq_orders": GROUP_ROOT / "docs" / "orders.md",
    "ledger": GROUP_ROOT / "cph4" / "evolution-ledger.md",
    "own_orders_dir": REPO / "orders",
    "state": REPO / "src" / "os" / "state.json",
    "cards_dir": REPO / "data" / "storylines" / "cards",
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


def load_orders_watermark(state_path):
    """{rows, tail_key} from state.json; missing/bad shape -> None.

    None is the loud side: face_orders then reports watermark-missing and
    breaks silence (first-run consume-then-store semantics, tech#103).
    """
    with io.open(str(state_path), encoding="utf-8") as fh:
        data = json.load(fh)
    wm = data.get("orders_row_watermark")
    if not isinstance(wm, dict) or "rows" not in wm or "tail_key" not in wm:
        return None
    return {"rows": wm.get("rows"), "tail_key": wm.get("tail_key")}


def _orders_first_cell(line):
    """First cell of a |-row (caller guarantees the leading '|')."""
    rest = line.strip()[1:]
    nxt = rest.find("|")
    cell = rest if nxt < 0 else rest[:nxt]
    return cell.strip()


def orders_row_stats(text):
    """(rows, tail_key) over the |-row family (tech#103 fingerprint).

    rows counts every line whose first non-space char is '|'; tail_key is
    the first cell of the LAST such row. Appends bump rows and (almost
    always) move tail_key; removals bump rows down; last-row edits move
    tail_key. Any deviation from the stored watermark breaks silence
    (fail-closed direction, tech#50 philosophy).
    """
    rows = 0
    tail_key = ""
    for line in text.splitlines():
        if line.lstrip().startswith("|"):
            rows += 1
            tail_key = _orders_first_cell(line)
    return rows, tail_key


def current_orders_watermark(hq_orders_path=None):
    """Turnkey {rows, tail_key} for the close step (consumption anchor).

    The close script calls this and passes the result to
    close_commit.finalize_state(orders_watermark=...) so the baseline
    update flows through the single state writer (tech#76 law).
    """
    path = Path(hq_orders_path) if hq_orders_path else DEFAULTS["hq_orders"]
    text, _, _ = read_text(path)
    rows, tail_key = orders_row_stats(text)
    return {"rows": rows, "tail_key": tail_key}


def orders_row_dates(text, year=None):
    """Set of dates parsed from orders |-row first cells (tech#129 face).

    Both live shapes: "10-12 13:5x" (MM-DD, ``year`` assumed = current
    year -- the orders file is a rolling 2026 ledger) and the full-date
    "2026-09-28 18:1x" family. Non-date cells (header/separator) yield
    nothing.
    """
    if year is None:
        year = datetime.now().year
    found = set()
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cell = _orders_first_cell(line)
        match = ORDERS_CELL_DATE_RE.match(cell)
        if not match:
            continue
        if match.group(1):
            found.add(date(int(match.group(1)), int(match.group(2)),
                           int(match.group(3))))
        else:
            found.add(date(year, int(match.group(4)), int(match.group(5))))
    return found


def latest_digest_card(cards_dir):
    """(date, dir_name) of the newest MC-YYYYMMDD-DIGEST-vNN card, or None.

    Staging dirs (``-tmp`` suffix) are valid consumption signal; at equal
    dates the non-tmp name wins for reporting.
    """
    cards_dir = Path(cards_dir)
    best = None
    try:
        entries = list(cards_dir.iterdir())
    except OSError:
        return None
    for entry in entries:
        match = DIGEST_CARD_RE.match(entry.name)
        if not match:
            continue
        when = date(int(match.group(1)), int(match.group(2)),
                    int(match.group(3)))
        is_tmp = entry.name.endswith("-tmp")
        if best is None or when > best[0] or (when == best[0] and
                                              is_tmp < best[2]):
            best = (when, entry.name, is_tmp)
    if best is None:
        return None
    return best[0], best[1]


def classify_digest_supply_gap(orders_dates, latest, today,
                               threshold_days=DIGEST_SUPPLY_GAP_DAYS):
    """Pure core for the DIGEST supply-gap advisory face (tech#129).

    Returns a dict: status inactive|quiet|advisory|gap + reading fields.
    - unconsumed = row dates strictly newer than the latest DIGEST card
      (day granularity; same-day clusters are below face resolution)
    - advisory: unconsumed exists but oldest age <= threshold (per-round
      hint line, silence NOT broken)
    - gap: oldest unconsumed age > threshold -> WARN breaks silence (the
      chronic-blindness backstop for the R870/R1095/R1303/R1536/R2050
      manual-correction family). Creative judgment stays with the body.
    """
    if latest is None and not orders_dates:
        return {"status": "quiet", "unconsumed": 0, "oldest": None,
                "age_days": None, "threshold": threshold_days}
    unconsumed = sorted(d for d in orders_dates
                        if latest is None or d > latest)
    if not unconsumed:
        return {"status": "quiet", "unconsumed": 0, "oldest": None,
                "age_days": None, "threshold": threshold_days}
    oldest = unconsumed[0]
    age_days = (today - oldest).days
    status = "gap" if age_days > threshold_days else "advisory"
    return {"status": status, "unconsumed": len(unconsumed),
            "oldest": oldest, "age_days": age_days,
            "threshold": threshold_days}


def face_digest_supply(paths, today=None):
    """Face: DIGEST 史源 supply-gap advisory backstop (#67 trigger law).

    rc 0 quiet/advisory/inactive / 1 gap WARN (breaks silence) / 3 read
    error. Cards dir missing = face inactive (the DIGEST production line
    itself is absent) -- never a read failure.
    """
    cards = Path(paths["cards_dir"])
    latest = latest_digest_card(cards)
    if latest is None:
        return RC_QUIET, ("cards: %s | (no DIGEST card dir)\n"
                          "DIGEST-SUPPLY: inactive (no cards dir)"
                          % (cards,))
    try:
        text, mtime, size = read_text(paths["hq_orders"])
    except OSError as exc:
        return RC_READ_FAIL, "read-fail: hq-orders %r" % (exc,)
    if today is None:
        today = datetime.now().date()
    dates = orders_row_dates(text)
    verdict = classify_digest_supply_gap(dates, latest[0], today)
    lines = ["cards: %s | latest DIGEST card %s (%s) | orders rows "
             "mtime %s | row-dates=%d"
             % (cards, latest[0].isoformat(), latest[1], mtime, len(dates))]
    if verdict["status"] == "quiet":
        lines.append("DIGEST-SUPPLY: quiet (orders rows covered by "
                     "latest DIGEST card %s)" % latest[0].isoformat())
        return RC_QUIET, "\n".join(lines)
    detail = ("%d unconsumed orders row-date(s) after latest DIGEST card "
              "%s (oldest %s, age %dd)"
              % (verdict["unconsumed"], latest[0].isoformat(),
                 verdict["oldest"].isoformat(), verdict["age_days"]))
    if verdict["status"] == "advisory":
        lines.append("DIGEST-SUPPLY: %s -- advisory (age <= %dd; "
                     "judgment stays with the loop)" % (detail,
                                                       verdict["threshold"]))
        return RC_QUIET, "\n".join(lines)
    lines.append("DIGEST-SUPPLY-GAP: %s -- WARN (age > %dd): supply "
                  "blindspot backstop (R870/R1095/R1303/R1536/R2050 "
                  "manual-correction family; derive-into-pool evaluation "
                  "due)" % (detail, verdict["threshold"]))
    return RC_NEW, "\n".join(lines)


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


def face_orders(paths):
    """Face: ORDERS row watermark (tech#103, decisions_watermark sibling).

    rc 0 quiet (watermark matches) / 1 new-or-missing (breaks silence) /
    3 read error. A missing watermark is first-run rc 1 with the
    watermark-missing note so the body must consume-then-store once --
    never read quiet on a missing baseline (false-quiet direction lock).
    """
    try:
        text, mtime, size = read_text(paths["hq_orders"])
    except OSError as exc:
        return RC_READ_FAIL, "read-fail: hq-orders %r" % (exc,)
    try:
        stored = load_orders_watermark(paths["state"])
    except (OSError, ValueError) as exc:
        return RC_READ_FAIL, "read-fail: state %r" % (exc,)

    rows, tail_key = orders_row_stats(text)
    cur = {"rows": rows, "tail_key": tail_key}
    lines = [
        "file: %s | mtime %s | %d B" % (paths["hq_orders"], mtime, size),
        "current: rows=%d tail_key=%r" % (rows, tail_key),
    ]
    if stored is None:
        lines.append("stored: watermark-missing (first-run: consume then "
                     "store {rows, tail_key})")
        lines.append("ORDERS-NEW: watermark-missing")
        return RC_NEW, "\n".join(lines)
    lines.append("stored: rows=%r tail_key=%r" % (stored["rows"],
                                                  stored["tail_key"]))
    if stored == cur:
        lines.append("ORDERS: quiet (watermark matches)")
        return RC_QUIET, "\n".join(lines)
    lines.append("ORDERS-NEW: rows %r->%r | tail_key %r->%r"
                 % (stored["rows"], rows, stored["tail_key"], tail_key))
    return RC_NEW, "\n".join(lines)


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
                   "--state", "--cards-dir"):
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
        ("ORDERS", *face_orders(paths)),
        ("DIGEST-SUPPLY", *face_digest_supply(paths)),
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
