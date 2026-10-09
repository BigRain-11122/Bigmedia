# -*- coding: utf-8 -*-
"""BigStream OS-loop health probe (os-protocol section 5, capability C-20).

Machine teeth for the loop-health judgment criteria declared in
docs/os-protocol.md section 5 - until now verified by hand only:
  * heartbeat discipline: logs/probe-heartbeat.txt freshness and gaps
  * accounting continuity: state.json tick vs completed round beats
  * ledger hygiene: log-entry timestamps, state schema, regime value
Ownership: engineering dept (org-structure section 2 core metrics -
heartbeat, tick continuity, backlog burn rate). Pure read-only.

Beat vocabulary (written by src/os/iteration_loop.ps1):
  "round done exit=N"         a headless round completed (accounts a tick)
  "skip (round in flight)"    single-instance guard beat
  "round timeout killed ..."  25-min budget kill (does NOT account a tick)
  "error ..."                 launcher error beat

Thresholds:
  --max-gap MIN  beat-to-beat gap advisory bound (default 20 = fleet
                 comm SLA; a legit long round can run the full 25-min
                 budget, so a SLA breach is WARN, not FAIL)
  --max-age MIN  staleness FAIL bound (default 40 = launcher lock
                 expiry; silence beyond it means the loop stopped)
  Any historical gap over 40 min = outage FAIL (same lock-age logic).

State log entries may carry approximate minutes ("17:2x" - unknown
digit). The x is a legal placeholder, ordered lexicographically; a
backwards step in these narrative timestamps is a hygiene WARN, not
an accounting breach (the hard continuity chain is beats vs tick).

Encoding rule: this script is pure ASCII. The Chinese ledgers it
parses are read with errors="replace"; only ASCII/regex prefixes are
matched (timestamps, tick digits, [done] via shared weekly_report
regexes - one source of truth for the board format).

Findings:
  FAIL  heartbeat-file/line/order   beat log missing/garbled/rewound
  FAIL  heartbeat-stale             last beat older than --max-age
  FAIL  heartbeat-outage            historical gap beyond lock age
  FAIL  state-file/schema/tick      state ledger unusable
  FAIL  state-production             production value outside regimes
  FAIL  log-ts                       entry lacks leading timestamp
  FAIL  state-ts                     ts field missing/malformed (fleet
                                   heartbeat face, PT-20260925-02)
  FAIL  account-lag                 done beats > tick + adjudicated drift
                                   (rounds ran, accounting missing - R4/R5)
  WARN  account-drift-adjudicated   done beats within the documented drift
                                   baseline (broken-round double-body)
  WARN  state-ts-stale/future        closing step not refreshing ts /
                                   future stamping (clock skew)
  WARN  heartbeat-gap                beat gap over --max-gap (SLA)
  WARN  account-ahead                tick ahead of done beats (repair
                                   bump or off-beat accounting)
  WARN  log-order/log-gap            narrative timestamp hygiene
  WARN  backlog-file                 board missing (burn rate unknown)

Exit codes: 0 = healthy (WARN allowed), 1 = any FAIL, 2 = usage/source.

Output modes:
    default        every finding printed (audit face, unchanged)
    --loop         routine loop-consumption face: the same analysis,
                   compact output - FAILs always print in full, WARNs
                   that embed only pre-cutoff dates (adjudicated
                   log-order / heartbeat-gap history) fold into one
                   suppression count. Structural/every-run WARNs (no
                   embedded date) stay visible. Dense in-window
                   same-code WARN groups (>= --fold-dense N, default 5)
                   collapse into one count line with date span and
                   magnitude band (tech#20: high-cadence production
                   windows re-read ~40 advisory gap WARNs per round;
                   worst gap stays visible, anything past the lock-age
                   bound is a FAIL and never folds). Nothing is re-d
                   derived differently - analysis identical, verbosity only.
    --recent-days N  --loop cutoff window (default 3)
    --fold-dense N  --loop dense-group fold threshold (default 5; 0 = off)

Usage:
    python src/os/loop_health.py [--root DIR] [--max-age N] [--max-gap N]
                                 [--loop] [--recent-days N] [--fold-dense N]
"""
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(REPO / "src"))
from weekly_report import DONE_RE, ITEM_RE  # noqa: E402  board format truth

BEAT_RE = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) osloop: (.+)$")
ROUND_DONE_RE = re.compile(r"round done exit=(\d+)")
LOG_TS_RE = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d[0-9x])")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
STATE_REQUIRED = ("loop", "mode", "production", "tick", "backlog", "log", "ts", "task")
PRODUCTION_REGIMES = ("paused", "open")
LOCK_AGE_MIN = 40  # iteration_loop.ps1 LockMaxAgeMinutes - staleness bound
SLA_GAP_MIN = 20   # fleet comm SLA - advisory bound (rounds may run 25m)
STATE_TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
GAP_MIN_RE = re.compile(r"beat gap (\d+) min")
FOLD_DENSE_DEFAULT = 5  # tech#20: dense same-code WARN group fold size


def parse_beats(path):
    """Heartbeat log -> (beats [(datetime, msg)], findings)."""
    findings = []
    if not path.is_file():
        findings.append(("FAIL", "heartbeat-file", "heartbeat log missing: %s" % path))
        return [], findings
    beats = []
    for n, line in enumerate(path.read_text(encoding="utf-8-sig", errors="replace").splitlines(), 1):
        s = line.strip()
        if not s:
            continue
        m = BEAT_RE.match(s)
        if not m:
            findings.append(("FAIL", "heartbeat-line",
                             "unparseable beat (line %d): %.60s" % (n, s)))
            continue
        try:
            ts = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            findings.append(("FAIL", "heartbeat-line", "bad beat timestamp (line %d)" % n))
            continue
        beats.append((ts, m.group(2)))
    if not beats:
        findings.append(("FAIL", "heartbeat-file", "no parseable beats in %s" % path))
    for i in range(1, len(beats)):
        if beats[i][0] < beats[i - 1][0]:
            findings.append(("FAIL", "heartbeat-order",
                             "beat time goes backwards: %s -> %s"
                             % (beats[i - 1][0].strftime("%Y-%m-%d %H:%M:%S"),
                                beats[i][0].strftime("%Y-%m-%d %H:%M:%S"))))
    return beats, findings


def parse_state(path):
    """state.json -> (state-or-None, log timestamp strings, findings)."""
    findings = []
    if not path.is_file():
        findings.append(("FAIL", "state-file", "state ledger missing: %s" % path))
        return None, [], findings
    try:
        state = json.loads(path.read_text(encoding="utf-8-sig", errors="replace"))
    except ValueError as e:
        findings.append(("FAIL", "state-file", "state ledger not valid JSON: %s" % e))
        return None, [], findings
    if not isinstance(state, dict):
        findings.append(("FAIL", "state-file", "state ledger is not a JSON object"))
        return None, [], findings
    missing = [k for k in STATE_REQUIRED if k not in state]
    if missing:
        findings.append(("FAIL", "state-schema",
                         "state ledger missing keys: %s" % ", ".join(missing)))
        return state, [], findings
    if state["production"] not in PRODUCTION_REGIMES:
        findings.append(("FAIL", "state-production",
                         "unknown production regime %r (expected %s)"
                         % (state["production"], "/".join(PRODUCTION_REGIMES))))
    tick = state["tick"]
    if not isinstance(tick, int) or isinstance(tick, bool) or tick < 0:
        findings.append(("FAIL", "state-tick",
                         "tick is not a non-negative integer: %r" % (tick,)))
    log = state["log"]
    if not isinstance(log, list):
        findings.append(("FAIL", "state-log", "log is not a list"))
        return state, [], findings
    stamps = []
    for i, entry in enumerate(log, 1):
        if not isinstance(entry, str):
            findings.append(("FAIL", "log-ts", "log entry %d is not a string" % i))
            continue
        m = LOG_TS_RE.match(entry)
        if not m:
            findings.append(("FAIL", "log-ts",
                             "log entry %d lacks leading timestamp: %.40s" % (i, entry)))
            continue
        stamps.append(m.group(1))
    for i in range(1, len(stamps)):
        if stamps[i] < stamps[i - 1]:
            findings.append(("WARN", "log-order",
                             "log entry timestamps go backwards: %s -> %s "
                             "(narrative hygiene; approximate minutes allowed)"
                             % (stamps[i - 1], stamps[i])))
    if isinstance(tick, int) and not isinstance(tick, bool) and len(stamps) < tick:
        findings.append(("WARN", "log-gap",
                         "tick=%d but %d stamped log entries - multi-round "
                         "repair entry possible (see state log)" % (tick, len(stamps))))
    return state, stamps, findings


def parse_backlog(path):
    """Board -> ((total, done), findings). Burn rate is info, not a gate."""
    findings = []
    if not path.is_file():
        findings.append(("WARN", "backlog-file", "backlog board missing: %s" % path))
        return (0, 0), findings
    total = done = 0
    for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        m = ITEM_RE.match(line)
        if not m:
            continue
        total += 1
        if DONE_RE.search(m.group(2)):
            done += 1
    return (total, done), findings


def classify(beats):
    """Beats -> (done [(ts, msg)], skip_n, timeout_n, error_n)."""
    done, skip_n, timeout_n, error_n = [], 0, 0, 0
    for ts, msg in beats:
        if ROUND_DONE_RE.search(msg):
            done.append((ts, msg))
        elif "timeout" in msg:
            timeout_n += 1
        elif "skip" in msg:
            skip_n += 1
        elif "error" in msg:
            error_n += 1
    return done, skip_n, timeout_n, error_n


def warn_is_recent(msg, cutoff):
    """Loop-mode WARN visibility: a WARN that embeds no date (structural
    / every-run notes - account drift, board missing) always shows; a
    WARN whose every embedded date predates the cutoff (adjudicated
    narrative-hygiene history) folds into the suppression count. New
    findings carry fresh dates and can never be hidden."""
    dates = DATE_RE.findall(msg)
    if not dates:
        return True
    return any(d >= cutoff for d in dates)


def dense_fold(shown, fold_dense):
    """tech#20 loop-face verbosity only: a recent same-code WARN group
    of >= fold_dense lines collapses into ONE count line (occurrences,
    date span, magnitude band for heartbeat-gap, pointer to the audit
    face). SLA advisory semantics survive - worst gap value stays on
    the folded line and anything past the lock-age bound is a FAIL,
    which never folds; per-item traceability survives at the default
    audit face. Findings, verdict and exit codes are untouched."""
    if fold_dense <= 0:
        return shown
    groups, order = {}, []
    for sev, code, _msg in shown:
        if sev != "WARN":
            continue
        if code not in groups:
            groups[code] = []
            order.append(code)
        groups[code].append(_msg)
    dense = {c for c in order if len(groups[c]) >= fold_dense}
    if not dense:
        return shown
    result, emitted = [], set()
    for sev, code, msg in shown:
        if sev == "WARN" and code in dense:
            if code in emitted:
                continue
            emitted.add(code)
            msgs = groups[code]
            dates = sorted({d for m in msgs for d in DATE_RE.findall(m)})
            span = (dates[0] + ".." + dates[-1]) if len(dates) > 1 else (
                dates[0] if dates else "no embedded date")
            band = ""
            mins = [int(mm.group(1)) for m in msgs
                    for mm in [GAP_MIN_RE.search(m)] if mm]
            if mins:
                band = ", gaps %d-%d min" % (min(mins), max(mins))
            msg = ("%d occurrence(s) %s%s (dense-window fold; run "
                   "without --loop for the full list)"
                   % (len(msgs), span, band))
        result.append((sev, code, msg))
    return result


def cross_check(beats, state, done, now, max_age, max_gap, findings):
    """Protocol section 5 criteria -> findings appended in place."""
    if beats:
        for i in range(1, len(beats)):
            gap = (beats[i][0] - beats[i - 1][0]).total_seconds() / 60.0
            pair = "%s -> %s" % (beats[i - 1][0].strftime("%Y-%m-%d %H:%M"),
                                 beats[i][0].strftime("%Y-%m-%d %H:%M"))
            if gap > LOCK_AGE_MIN:
                findings.append(("FAIL", "heartbeat-outage",
                                 "beat gap %.0f min (%s) exceeds lock age %d min "
                                 "- loop outage window" % (gap, pair, LOCK_AGE_MIN)))
            elif gap > max_gap:
                findings.append(("WARN", "heartbeat-gap",
                                 "beat gap %.0f min (%s) over %d min comm SLA "
                                 "- long rounds may breach legitimately"
                                 % (gap, pair, max_gap)))
        age = (now - beats[-1][0]).total_seconds() / 60.0
        if age > max_age:
            findings.append(("FAIL", "heartbeat-stale",
                             "last beat %.0f min old (> %d min lock age) - "
                             "loop silent, machine off or task dead"
                             % (age, max_age)))
    if state and isinstance(state.get("tick"), int) and not isinstance(state.get("tick"), bool):
        tick = state["tick"]
        # R1452 caliber fix: heartbeat done-beats count body completions,
        # tick counts accounted rounds - a killed body retried under the same
        # round number (broken-round absorb convention) adds a done beat
        # without an accounted round, so a documented constant drift is
        # expected history, not the missing-accounting bug this gate exists
        # to catch. Only drift BEYOND the adjudicated baseline FAILs; the
        # baseline itself surfaces as an explicit WARN every run.
        adj = state.get("account_drift_adjudicated", 0)
        if not isinstance(adj, int) or isinstance(adj, bool) or adj < 0:
            adj = 0
        if len(done) > tick + adj:
            findings.append(("FAIL", "account-lag",
                             "%d completed round(s) without accounting "
                             "(done beats=%d > tick=%d + adjudicated=%d) - "
                             "the R4/R5 bug pattern"
                             % (len(done) - tick - adj, len(done), tick, adj)))
        elif len(done) > tick:
            findings.append(("WARN", "account-drift-adjudicated",
                             "done beats=%d vs tick=%d: %d beat(s) within "
                             "adjudicated drift baseline (broken-round "
                             "double-body history; see state "
                             "account_drift_note)" % (len(done), tick,
                                                      len(done) - tick)))
        elif tick > len(done):
            findings.append(("WARN", "account-ahead",
                             "tick=%d ahead of done beats=%d - repair bump "
                             "or off-beat accounting" % (tick, len(done))))
    # PT-20260925-02 writer face: state.ts is the machine-readable heartbeat
    # stamp the group fleet-audit reads (beats file is gitignored, so state.json
    # is the only aliveness face a remote clone can verify).
    if state:
        ts = state.get("ts")
        if not isinstance(ts, str) or not STATE_TS_RE.match(ts.strip()):
            findings.append(("FAIL", "state-ts",
                             "state ts missing/malformed (want YYYY-MM-DD "
                             "HH:MM:SS, refreshed at closing): %r" % (ts,)))
        else:
            try:
                ts_dt = datetime.strptime(ts.strip(), "%Y-%m-%d %H:%M:%S")
                age = (now - ts_dt).total_seconds() / 60.0
                if age > LOCK_AGE_MIN:
                    findings.append(("WARN", "state-ts-stale",
                                     "state ts %.0f min old (> %d min) - closing "
                                     "step not refreshing ts" % (age, LOCK_AGE_MIN)))
                elif age < -5:
                    findings.append(("WARN", "state-ts-future",
                                     "state ts %.0f min ahead of clock - future "
                                     "stamping or clock skew" % (-age)))
            except ValueError:
                findings.append(("FAIL", "state-ts",
                                 "state ts unparseable: %r" % (ts,)))


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    root, max_age, max_gap = REPO, LOCK_AGE_MIN, SLA_GAP_MIN
    loop_mode, recent_days, fold_dense = False, 3, FOLD_DENSE_DEFAULT
    args = argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--root" and i + 1 < len(args):
            root = Path(args[i + 1])
            i += 2
        elif args[i] == "--loop":
            loop_mode = True
            i += 1
        elif args[i] == "--recent-days" and i + 1 < len(args):
            try:
                recent_days = int(args[i + 1])
            except ValueError:
                print("usage: python src/os/loop_health.py [--root DIR] "
                      "[--max-age N] [--max-gap N] [--loop] [--recent-days N] "
                      "[--fold-dense N]")
                return 2
            if recent_days <= 0:
                print("--recent-days must be positive")
                return 2
            i += 2
        elif args[i] == "--fold-dense" and i + 1 < len(args):
            try:
                fold_dense = int(args[i + 1])
            except ValueError:
                print("usage: python src/os/loop_health.py [--root DIR] "
                      "[--max-age N] [--max-gap N] [--loop] [--recent-days N] "
                      "[--fold-dense N]")
                return 2
            if fold_dense < 0:
                print("--fold-dense must be >= 0 (0 disables the fold)")
                return 2
            i += 2
        elif args[i] in ("--max-age", "--max-gap") and i + 1 < len(args):
            try:
                v = int(args[i + 1])
            except ValueError:
                print("usage: python src/os/loop_health.py "
                      "[--root DIR] [--max-age N] [--max-gap N]")
                return 2
            if v <= 0:
                print("--%s must be positive" % args[i].lstrip("-"))
                return 2
            if args[i] == "--max-age":
                max_age = v
            else:
                max_gap = v
            i += 2
        else:
            print("usage: python src/os/loop_health.py [--root DIR] "
                  "[--max-age N] [--max-gap N] [--loop] [--recent-days N] "
                  "[--fold-dense N]")
            return 2
    heart = root / "logs" / "probe-heartbeat.txt"
    state_path = root / "src" / "os" / "state.json"
    board = root / "src" / "os" / "backlog.md"
    try:
        beats, findings = parse_beats(heart)
        state, _, f = parse_state(state_path)
        findings += f
        (b_total, b_done), f = parse_backlog(board)
        findings += f
    except OSError as e:
        print("source error: %s" % e)
        return 2
    done, skip_n, timeout_n, error_n = classify(beats)
    nonzero = sum(1 for _, msg in done if int(ROUND_DONE_RE.search(msg).group(1)) != 0)
    cross_check(beats, state, done, datetime.now(), max_age, max_gap, findings)
    tick = state["tick"] if state and isinstance(state.get("tick"), int) else "?"
    burn = ("%.0f%%" % (100.0 * b_done / b_total)) if b_total else "n/a"
    if not loop_mode:
        print("loop health probe: heartbeat=%s state=%s backlog=%s" % (heart, state_path, board))
    print("summary: tick=%s, beats=%d (done=%d nonzero=%d skip=%d timeout=%d "
          "error=%d), log=%d entries, backlog=%d items %d done (%s burn)"
          % (tick, len(beats), len(done), nonzero, skip_n, timeout_n, error_n,
             len(state["log"]) if state and isinstance(state.get("log"), list) else 0,
             b_total, b_done, burn))
    if loop_mode:
        cutoff = (datetime.now() - timedelta(days=recent_days)).strftime("%Y-%m-%d")
        shown = [f for f in findings
                 if f[0] != "WARN" or warn_is_recent(f[2], cutoff)]
        supp = len(findings) - len(shown)
        shown = dense_fold(shown, fold_dense)
    else:
        shown, supp = findings, 0
    for sev, code, msg in shown:
        print("- [%s] %s: %s" % (sev, code, msg))
    if supp:
        print("- [INFO] suppressed: %d historical WARN with no date on/after "
              "%s (--loop face; run without --loop for the full audit output)"
              % (supp, cutoff))
    fails = sum(1 for s, _, _ in findings if s == "FAIL")
    warns = sum(1 for s, _, _ in findings if s == "WARN")
    verdict = "FAIL" if fails else ("WARN" if warns else "PASS")
    print("loop health: %s (%d fail, %d warn)" % (verdict, fails, warns))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
