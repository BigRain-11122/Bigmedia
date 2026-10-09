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
  - Whisper surface (exact since tech#19, R1830):
    data/pipeline/whisper-ledger.jsonl rows appended by
    src/render/whisper_to_srt.py - one row per real run (calibration
    and QC runs included, which the old approximation never saw).
    rc==0 rows count as produced; rc!=0 rows are reported separately
    as attempted-no-output (mirroring the ollama classification).
    Station-reviews asr-check rows remain the approximation for
    history strictly BEFORE the ledger epoch date; on/after the epoch
    day they are dropped so a run that leaves both surfaces is never
    double-counted (epoch-day pre-hook runs undercount honestly).

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
WHISPER_LEDGER_PATH = REPO + "/data/pipeline/whisper-ledger.jsonl"

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


def parse_whisper_ledger(text):
    """Yield (datetime, rc) per exact-metering JSONL row (tech#19).
    Malformed lines are skipped best-effort - a metering probe must
    never crash on a partially written row."""
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
            ts = str(row.get("ts", ""))
            when = None
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
                try:
                    when = datetime.datetime.strptime(ts, fmt)
                    break
                except ValueError:
                    continue
            if when is None:
                continue
            rc = row.get("rc", 0)
            rows.append((when, rc if isinstance(rc, int) else 0))
        except ValueError:
            continue
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


def meter(expert_rows, asr_rows, since, ledger_rows=None):
    """Window-filter and classify; returns a readout dict.

    ledger_rows (tech#19): when provided, the exact whisper-ledger
    surface owns the epoch day onward and station-reviews asr rows
    stay only as pre-epoch history (no double counting)."""
    ok_rows = [r for r in expert_rows if r[0] >= since]
    attempted = [r for r in ok_rows if not _is_produced(r[1])]
    produced = [r for r in ok_rows if _is_produced(r[1])]
    base = {
        "since": since.strftime("%Y-%m-%d %H:%M"),
        "ollama_produced": len(produced),
        "ollama_attempted_noproduct": len(attempted),
    }
    if ledger_rows:
        epoch = min(r[0] for r in ledger_rows)
        epoch_day = datetime.datetime.combine(
            epoch.date(), datetime.time(0, 0))
        apprx = [d for d in asr_rows if since <= d < epoch_day]
        exact = [r for r in ledger_rows if r[0] >= since]
        ex_produced = [r for r in exact if r[1] == 0]
        ex_attempted = [r for r in exact if r[1] != 0]
        base.update({
            "whisper_apprx_rows": len(apprx),
            "whisper_exact_produced": len(ex_produced),
            "whisper_exact_attempted": len(ex_attempted),
            "whisper_rows": len(apprx) + len(exact),
            "tokens_local": len(produced) + len(apprx) + len(ex_produced),
        })
        return base
    asr = [d for d in asr_rows if d >= since]
    base.update({
        "whisper_apprx_rows": len(asr),
        "whisper_exact_produced": 0,
        "whisper_exact_attempted": 0,
        "whisper_rows": len(asr),
        "tokens_local": len(produced) + len(asr),
    })
    return base


def read_text(path):
    try:
        with io.open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def build_readout(since, expert_path=EXPERT_CALLS_PATH,
                  station_path=STATION_REVIEWS_PATH,
                  ledger_path=WHISPER_LEDGER_PATH):
    return meter(parse_expert_calls(read_text(expert_path)),
                 parse_station_asr(read_text(station_path)), since,
                 ledger_rows=parse_whisper_ledger(read_text(ledger_path))
                 or None)


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
            "{ollama_attempted_noproduct}; whisper runs {whisper_rows} "
            "= approx {whisper_apprx_rows} + exact produced "
            "{whisper_exact_produced} / attempted-no-output "
            "{whisper_exact_attempted})\n".format(**readout))
    return 0


if __name__ == "__main__":
    sys.exit(main())
