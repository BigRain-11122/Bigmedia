"""tokens:local auto-metering probe (P-54⑤; state/queue/tech#10).

Counts local-model invocations from auto-ledger surfaces within a time
window, so the loop collection step can paste a probe readout instead of
relying on per-round memory:

  - Ollama surface (exact): docs/reviews/expert-calls.md table rows — every
    call_expert.py / wrapper call auto-appends one row (``| 时间 | 专家 |
    身份 | 材料 | 退出 | 结论首行 |``). Rows whose exit cell parses as a
    non-zero int (hand-added FAIL/timeout rows) are reported separately as
    attempted-no-output and count 0, per the 2026-09-24 convention (R175:
    timeout with no verdict = 0). Rows with a verdict-style exit cell
    (E4 wrapper form, e.g. ``8.0（…）``) count as produced.
  - Whisper surface (approx): docs/reviews/station-reviews.md rows
    mentioning ``asr-check`` within the window — one row ≈ one
    faster-whisper medium run at current S2 practice (row-evidence
    approximation, not an exact hook).

Not auto-countable (hand-note only): direct ``ollama run`` warm-ups and
whisper calibration runs that leave no ledger row.

Chain position: the state.json log line stays the single truth consumed by
src/os/local_rate_report.py; this probe only supplies the number. Pure
script — zero model calls, zero tokens.
"""

from __future__ import unicode_literals

import argparse
import datetime
import io
import json
import re
import sys

REPO = __file__.replace("\\", "/").rsplit("/src/os/", 1)[0]
EXPERT_CALLS_PATH = REPO + "/docs/reviews/expert-calls.md"
STATION_REVIEWS_PATH = REPO + "/docs/reviews/station-reviews.md"

# expert-calls row: | 2026-10-09 07:17 | S1-script | … | material | 0 | … |
EC_ROW_RE = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})\s*\|")
# station-reviews row: | 2026-10-09 | … |
SR_ROW_RE = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|")
ASR_MARK = "asr-check"


def parse_expert_calls(text):
    """Yield (datetime, exit_token) per ledger row; exit_token is the raw
    5th cell string (empty when a row has fewer cells than the schema)."""
    rows = []
    for line in text.splitlines():
        m = EC_ROW_RE.match(line.lstrip("\ufeff"))
        if not m:
            continue
        when = datetime.datetime.strptime(
            m.group(1) + " " + m.group(2), "%Y-%m-%d %H:%M")
        cells = line.split("|")
        exit_token = cells[5].strip() if len(cells) > 5 else ""
        rows.append((when, exit_token))
    return rows


def parse_station_asr(text):
    """Yield datetimes (date-level precision, 00:00) of asr-check rows."""
    rows = []
    for line in text.splitlines():
        if ASR_MARK not in line:
            continue
        m = SR_ROW_RE.match(line.lstrip("\ufeff"))
        if not m:
            continue
        rows.append(datetime.datetime.strptime(m.group(1), "%Y-%m-%d"))
    return rows


def _is_produced(exit_token):
    """True when the row represents a model call that produced a verdict.

    Exit-cell forms: ``0`` (standard success), ``3`` (hand-added FAIL /
    timeout — not produced), ``8.0（…）`` (E4 wrapper verdict form —
    produced). Unknown non-numeric tokens default to produced (a ledger row
    implies a real call was made).
    """
    token = exit_token.strip()
    if re.match(r"^\d+$", token):
        return int(token) == 0
    return True


def meter(expert_rows, asr_rows, since):
    """Window-filter and classify; returns a readout dict."""
    ok_rows = [r for r in expert_rows if r[0] >= since]
    attempted = [r for r in ok_rows if not _is_produced(r[1])]
    produced = [r for r in ok_rows if _is_produced(r[1])]
    asr = [d for d in asr_rows if d >= since]
    return {
        "since": since.strftime("%Y-%m-%d %H:%M"),
        "ollama_produced": len(produced),
        "ollama_attempted_noproduct": len(attempted),
        "whisper_rows": len(asr),
        "tokens_local": len(produced) + len(asr),
    }


def read_text(path):
    try:
        with io.open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def build_readout(since, expert_path=EXPERT_CALLS_PATH,
                  station_path=STATION_REVIEWS_PATH):
    return meter(parse_expert_calls(read_text(expert_path)),
                 parse_station_asr(read_text(station_path)), since)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--since", metavar="YYYY-MM-DD[ HH:MM]",
                    help="window start (default: today 00:00)")
    ap.add_argument("--json", action="store_true",
                    help="machine-readable output")
    args = ap.parse_args(argv)

    if args.since:
        stamp = args.since.strip()
        for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                since = datetime.datetime.strptime(stamp, fmt)
                break
            except ValueError:
                continue
        else:
            ap.error("bad --since format: " + stamp)
    else:
        since = datetime.datetime.combine(
            datetime.date.today(), datetime.time(0, 0))

    readout = build_readout(since)
    if args.json:
        print(json.dumps(readout, ensure_ascii=True, sort_keys=True))
    else:
        sys.stdout.write(
            "tokens:local={tokens_local} since {since} "
            "(ollama produced {ollama_produced} / attempted-no-output "
            "{ollama_attempted_noproduct}; whisper asr-check rows "
            "{whisper_rows})\n".format(**readout))
    return 0


if __name__ == "__main__":
    sys.exit(main())
