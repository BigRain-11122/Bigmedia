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
  WARN  root-probe-litter            1-2 root-level r<digit>/r_ probe/temp
                                   files left behind (round-end cleanup
                                   hook debt; C-20261009-02 order-3 face)
  FAIL  root-probe-litter            >= 3 root-level r<digit>/r_ probe
                                   files (recurring-litter pattern -
                                   episodic sweeps R1807/R1816/R1828)
  WARN  stale-dirty                uncommitted file(s) whose on-disk
                                   mtime is older than 7 days
                                   (C-20261009-03 workspace baseline v1
                                   dirty-face split law: in-flight files
                                   belong to their authoring window and
                                   are naturally fresh; sediment gets
                                   named - tech#31)
  WARN  aihot-stack               AIHOT radar-stack HTTP face(s) down or
                                   unreachable (api :3101 / web :3100);
                                   four deaths were all found after the
                                   fact (R1727/R1750/R1752/R1891) - this
                                   face names a dead stack within one
                                   round (tech#58)
  WARN  queue-glue               queue entry head 'NN. [' at a non-zero
                                   column in state/queue/*.md - entry
                                   written without a leading newline;
                                   line-anchored head scans miss glued
                                   entries (R1891 anchor: seed 58 glued
                                   to entry 57 tail went unsighted five
                                   rounds; tech#60)
  WARN  account-uncommitted     on-disk state.json tick ahead of the
                                   git-HEAD tick with the file dirty -
                                   closing stage-2 wrote the accounting
                                   but the round died before the commit
                                   (R1893 anchor; the push-missing half
                                   is the origin_gap_check face; tech#61)

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
import os
import re
import subprocess
import sys
import urllib.request
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
# tech#22: root-level probe/temp leftovers - both historical families
# (r_cur_* 28 files R1816 sweep + r<digits>* 107 files R1828 sweep; three
# episodic manual sweeps R1807/R1816/R1828 before this guard existed).
# README-style repo files never match (r must be followed by a digit or
# an underscore); subdirectories are not scanned.
PROBE_LITTER_RE = re.compile(r"^r[\d_]")
LITTER_FAIL_N = 3  # >= 3 leftovers = recurring pattern, not a one-off
# tech#31: sediment-dirty guard. C-20261009-03 workspace baseline v1
# dirty-face split law - in-flight files belong to their authoring window,
# sediment older than 7 days gets named. Before this machine face the
# naming was episodic human bookkeeping (same disease as tech#22: rule on
# the books, no machine teeth). In-flight files are naturally fresh, so an
# uncommitted file whose on-disk mtime predates the sediment bound is
# sediment by definition. Concurrent-session active batch domains are
# whitelisted (R1745 zero-contact carryover: an in-flight batch may
# legitimately hold old-mtime source assets the owning window will commit).
STALE_DIRTY_DAYS = 7
INFLIGHT_DIR_PREFIXES = (
    "data/storylines/drama/mv0001/",  # MV-session batch domain (+ release/)
    "data/sources/mv001/",           # MV-session source assets (song/frames)
)
GIT_TIMEOUT_S = 30
# tech#37: codex supply-freshness guard. The codex five-dimension files
# are the shared supply source for the DIGEST / drama / card lines; the
# README "refresh every batch" discipline had no machine face before this
# guard (R1844 arrears anchor: the chronicle went 09-29..10-09 - eleven
# days of zero continuation - before a human sweep cleared the debt).
# Freshness only: a missing dimension file is the content board's matter,
# never this guard's face (None mtime -> skipped, like deleted paths in
# the sediment guard).
CODEX_DIR = Path("data") / "storylines" / "codex"
CODEX_DIMENSIONS = ("city-chronicle.md", "city-culture.md",
                    "city-humanities.md", "city-residents.md",
                    "city-spirit.md")
CODEX_FRESH_DAYS = 7  # > 7 days unrefreshed = supply-sediment WARN
# tech#58: AIHOT stack liveness guard. The self-hosted radar stack
# (api :3101 / web :3100, PG reported inside the api health JSON) died
# four times and every death was discovered after the fact by a human
# (R1727/R1750/R1752/R1891 - the R1891 case sat dead 1.5h through
# running rounds because api health was only ever verified when some
# consumer needed it). This face probes both HTTP faces on every
# routine probe run, so a dead stack gets named within one round (the
# judging criterion). WARN level - recovery is an operational action
# and the guard must never break the probe: any probe error reports as
# the face being down/unreachable. Worker-only hangs are a different
# failure family (all four anchor deaths were full-stack kills) and
# stay out of scope. URLs env-overridable for future port changes.
AIHOT_API_URL = "http://127.0.0.1:3101/api/health"
AIHOT_WEB_URL = "http://127.0.0.1:3100/"
AIHOT_PROBE_TIMEOUT_S = 4.0
# tech#60: queue entry-glue guard. Queue entries live in state/queue/*.md
# as single lines starting 'NN. ['; a seed written without its leading
# newline glues onto the previous entry's tail (R1891 anchor: seed entry
# 58 sat glued to entry 57's tail - 'v1.65' + '58. [' direct join - and
# every line-anchored head scan missed it for five rounds while the
# round focus lines kept claiming 'tech#58 due any round'). This face
# names a glued head within one round on the routine probe consumption.
# WARN level per the guard family law (tech#22/#31/#37/#58): advisory,
# never breaks the probe. Head pattern per the tech#60 seed spec.
QUEUE_DIR = Path("state") / "queue"
QUEUE_ENTRY_HEAD_RE = re.compile(r"\d{1,3}\. \[")
QUEUE_GLUE_SHOW_N = 3  # glued lines shown per file before the "+N more" tail
# tech#61: round accounting-chain completeness guard. R1893 anchor: the
# two-stage closing died between its stages - tick 1893 + log + export
# refresh + queue restock were all written to disk and left uncommitted
# (origin ahead=1), and the next round had to absorb them. The existing
# account faces reconcile beats vs the ON-DISK tick, so accounting that
# was written but never committed had no reconciliation face at all. This
# guard compares the git-HEAD state.json tick with the on-disk one: HEAD
# behind + state.json dirty = account-uncommitted WARN (advisory per the
# guard family law; the write->commit window inside a live round's
# closing is a legal transient that round-open probe consumption never
# sees). The push-missing half (committed but not pushed) stays with
# origin_gap_check - one disease, two existing tools, no duplication.
STATE_REL = "src/os/state.json"


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


def check_root_litter(root, findings):
    """tech#22 guard: root-level r<digit>/r_ probe/temp files left behind by
    rounds past. The round-end cleanup hook (C-20261009-02 order 3) makes
    leaving them a violation; before this machine face the only detection
    was episodic human sweeps (R1807 28 files, R1816 28, R1828 107 - three
    recurrences = the gap anchor). 1-2 files = WARN (single-round debt,
    possibly another session's in-flight file - advisory), >= 3 = FAIL
    (recurring pattern). Non-recursive, files only; README-style names
    never match (r must be followed by a digit or underscore)."""
    try:
        names = sorted(p.name for p in root.iterdir()
                       if p.is_file() and PROBE_LITTER_RE.match(p.name))
    except OSError:
        return
    if not names:
        return
    shown = ", ".join(names[:5]) + (" ..." if len(names) > 5 else "")
    if len(names) >= LITTER_FAIL_N:
        findings.append(("FAIL", "root-probe-litter",
                         "%d root-level probe/temp leftover(s): %s - "
                         "round-end cleanup hook debt (C-20261009-02 order 3)"
                         % (len(names), shown)))
    else:
        findings.append(("WARN", "root-probe-litter",
                         "%d root-level probe/temp leftover(s): %s - clean "
                         "at round end" % (len(names), shown)))


def _parse_porcelain_z(data):
    """`git status --porcelain -z` stdout -> [relpath]. -z records are
    NUL-separated with no path quoting (raw UTF-8 bytes); a rename/copy
    record is followed by a second NUL field holding the old path, which
    is skipped. Short/garbled chunks never crash the guard."""
    paths, skip_next = [], False
    for chunk in data.split(b"\0"):
        if not chunk:
            continue
        if skip_next:
            skip_next = False
            continue
        if len(chunk) < 4:
            continue
        xy = chunk[:2]
        if b"R" in xy or b"C" in xy:
            skip_next = True
        paths.append(chunk[3:].decode("utf-8", "replace"))
    return paths


def _git_status_files(root):
    """Working-tree dirty/untracked relpaths (all untracked files listed
    individually so file-level mtimes, not parent-dir stamps, age the
    sediment test). Any git failure - not a work tree, git missing,
    timeout - yields [] : this guard is advisory and never breaks the
    probe (fake-repo CLI tests and non-git roots silently skip it)."""
    try:
        p = subprocess.run(
            ["git", "status", "--porcelain", "-z", "--untracked-files=all"],
            cwd=str(root), capture_output=True, timeout=GIT_TIMEOUT_S)
    except (OSError, subprocess.TimeoutExpired):
        return []
    if p.returncode != 0:
        return []
    return _parse_porcelain_z(p.stdout)


def classify_stale_dirty(entries, now, stale_days=STALE_DIRTY_DAYS,
                         prefixes=INFLIGHT_DIR_PREFIXES):
    """[(relpath, mtime-or-None)] -> sorted stale relpaths (pure core).
    Deleted paths (None mtime) and whitelisted in-flight-domain paths
    never flag; an mtime strictly older than stale_days flags."""
    bound = stale_days * 86400.0
    stale = []
    for rel, mtime in entries:
        if rel is None or mtime is None:
            continue
        if any(rel.startswith(p) for p in prefixes):
            continue
        if (now - mtime).total_seconds() > bound:
            stale.append(rel)
    return sorted(stale)


def check_stale_dirty(root, now, findings):
    """tech#31 guard face: name uncommitted sediment (one WARN with the
    file list). Fresh-mtime in-flight files never flag - see
    classify_stale_dirty - so the finding IS the C-20261009-03 baseline
    "sediment > 7 days gets named" line, machine-enforced every round
    by the routine probe consumption."""
    paths = _git_status_files(root)
    if not paths:
        return
    entries = []
    for rel in paths:
        mtime = None
        try:
            mtime = datetime.fromtimestamp((root / rel).stat().st_mtime)
        except OSError:
            pass
        entries.append((rel, mtime))
    stale = classify_stale_dirty(entries, now)
    if not stale:
        return
    shown = ", ".join(stale[:5]) + (" ..." if len(stale) > 5 else "")
    findings.append(("WARN", "stale-dirty",
                     "%d uncommitted file(s) unchanged on disk for over %d "
                     "days: %s - sediment naming (C-20261009-03 dirty-face "
                     "split law; fresh-mtime in-flight files never flag)"
                     % (len(stale), STALE_DIRTY_DAYS, shown)))


def classify_codex_freshness(entries, now, fresh_days=CODEX_FRESH_DAYS):
    """[(name, mtime-or-None)] -> sorted stale names (pure core). A None
    mtime (missing file) never flags: existence is the content board's
    face, freshness is this guard's."""
    bound = fresh_days * 86400.0
    return sorted(name for name, mtime in entries
                  if mtime is not None
                  and (now - mtime).total_seconds() > bound)


def check_codex_freshness(root, now, findings):
    """tech#37 guard face: name codex dimension files unrefreshed for over
    CODEX_FRESH_DAYS (one WARN with the list). Machine-enforced every round
    by the routine probe consumption; the R1844 11-day uncaptured-node
    arrears window (09-29..10-09, zero continuation) is the anchor."""
    entries = []
    for name in CODEX_DIMENSIONS:
        mtime = None
        try:
            mtime = datetime.fromtimestamp(
                (root / CODEX_DIR / name).stat().st_mtime)
        except OSError:
            pass
        entries.append((name, mtime))
    stale = classify_codex_freshness(entries, now)
    if not stale:
        return
    shown = ", ".join(stale[:5]) + (" ..." if len(stale) > 5 else "")
    findings.append(("WARN", "codex-stale",
                     "%d codex supply file(s) unrefreshed for over %d days: "
                     "%s - supply freshness debt (R1844 arrears anchor; "
                     "DIGEST/drama/cards shared source)"
                     % (len(stale), CODEX_FRESH_DAYS, shown)))


def probe_http_face(url, timeout_s=AIHOT_PROBE_TIMEOUT_S, _urlopen=None):
    """url -> (ok, detail); advisory HTTP probe, never raises. ok means
    HTTP 200; detail carries the body head (api face: health JSON) or a
    short failure reason. _urlopen is the injection seam for tests."""
    if _urlopen is None:
        _urlopen = urllib.request.urlopen
    try:
        with _urlopen(url, timeout=timeout_s) as resp:
            status = getattr(resp, "status", None) or resp.getcode()
            body = resp.read(4096)
            if status != 200:
                return False, "HTTP %s" % status
            return True, body.decode("utf-8", "replace")
    except Exception as e:  # transport/timeout/decode - advisory only
        return False, "%s: %.80s" % (type(e).__name__, e)


def classify_aihot_faces(api, web):
    """((api_ok, api_detail), (web_ok, web_detail)) -> findings (pure
    core). The api face additionally parses its health JSON: an api that
    answers but reports db != ok names the database face. A healthy
    stack yields no findings (silent PASS like the other guard faces);
    a body that fails to parse is ignored (the face answered)."""
    findings = []
    down = []
    if not api[0]:
        down.append("api down/unreachable (%s)" % api[1])
    else:
        try:
            health = json.loads(api[1])
        except ValueError:
            health = None
        if isinstance(health, dict) and health.get("db") not in (None, "ok"):
            down.append("api up, db face %r" % (health.get("db"),))
    if not web[0]:
        down.append("web down/unreachable (%s)" % web[1])
    if down:
        findings.append(("WARN", "aihot-stack",
                         "AIHOT stack face(s) %s - radar product line "
                         "supply chain (#112 criteria window); recovery "
                         "runbook = R1891 (pg_ctl/api/worker/web restart)"
                         % "; ".join(down)))
    return findings


def check_aihot_stack(findings, timeout_s=AIHOT_PROBE_TIMEOUT_S,
                      probe=None):
    """tech#58 guard face: probe the AIHOT stack HTTP faces and name any
    down face (one WARN). Machine-enforced every round by the routine
    probe consumption - a dead stack is named within one round."""
    if probe is None:
        probe = probe_http_face  # module global read at call time (test seam)
    api_url = os.environ.get("AIHOT_API_URL", AIHOT_API_URL)
    web_url = os.environ.get("AIHOT_WEB_URL", AIHOT_WEB_URL)
    findings.extend(classify_aihot_faces(probe(api_url, timeout_s),
                                         probe(web_url, timeout_s)))


def classify_queue_glue(files):
    """{name: text} -> findings (pure core). A queue entry head is
    'NN. [' at column 0; the same pattern at any non-zero column is an
    entry glued to the previous line's tail without a newline separator
    (the R1891 anchor form: 'v1.65' + '58. [' direct join - invisible to
    every line-anchored head scan). One WARN per file, the first
    QUEUE_GLUE_SHOW_N glued lines shown (first glued head per line
    names the line). Clean queue files yield no findings (silent PASS
    like the other guard faces)."""
    findings = []
    for name in sorted(files):
        glued = []
        for lineno, line in enumerate(files[name].splitlines(), 1):
            for m in QUEUE_ENTRY_HEAD_RE.finditer(line):
                if m.start() > 0:
                    glued.append((lineno, m.start(), m.group(0)))
                    break
        if not glued:
            continue
        shown = ", ".join("line %d col %d head %r" % g
                          for g in glued[:QUEUE_GLUE_SHOW_N])
        if len(glued) > QUEUE_GLUE_SHOW_N:
            shown += " (+%d more)" % (len(glued) - QUEUE_GLUE_SHOW_N)
        findings.append(("WARN", "queue-glue",
                         "%d glued queue entry head(s) in %s: %s - entry "
                         "head at a non-zero column = entry written "
                         "without a leading newline; line-anchored queue "
                         "head scans miss glued entries (R1891 anchor: "
                         "seed 58 glued to entry 57 tail went unsighted "
                         "five rounds) - split the line"
                         % (len(glued), name, shown)))
    return findings


def check_queue_glue(root, findings):
    """tech#60 guard face: scan every state/queue/*.md for entry heads
    glued at a non-zero column. Machine-enforced every round by the
    routine probe consumption - a glued entry is named within one round
    instead of five. A missing queue dir stays silent (existence is the
    loop engine's face, not this guard's); unreadable files are skipped
    (not the glue face's matter)."""
    qdir = root / QUEUE_DIR
    if not qdir.is_dir():
        return
    files = {}
    for path in sorted(qdir.glob("*.md")):
        try:
            files[path.name] = path.read_text(
                encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
    findings.extend(classify_queue_glue(files))


def _git_show_state(root, _run=None):
    """`git show HEAD:<state.json>` stdout bytes, or None on any failure
    (not a work tree, state never committed, git missing, timeout).
    _run is the injection seam for tests (subprocess.run signature)."""
    if _run is None:
        _run = subprocess.run
    try:
        p = _run(["git", "show", "HEAD:" + STATE_REL],
                 cwd=str(root), capture_output=True, timeout=GIT_TIMEOUT_S)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if p.returncode != 0:
        return None
    return p.stdout


def read_head_state_tick(root, show=None):
    """git-HEAD state.json -> tick int or None. `show` is the
    data-provider injection seam (root -> bytes-or-None); an absent or
    malformed HEAD copy stays None (advisory skip - the account faces
    already FAIL a broken disk ledger; this face only reconciles two
    readable ticks)."""
    data = (show or _git_show_state)(root)
    if not data:
        return None
    try:
        state = json.loads(data.decode("utf-8", "replace"))
    except ValueError:
        return None
    tick = state.get("tick") if isinstance(state, dict) else None
    if isinstance(tick, int) and not isinstance(tick, bool):
        return tick
    return None


def classify_account_uncommitted(head_tick, disk_tick, state_dirty):
    """(head_tick, disk_tick, state_dirty) -> findings (pure core). The
    R1893 anchor form names exactly one WARN: disk tick ahead of the
    HEAD tick with state.json dirty = closing stage-2 wrote the
    accounting but the round died before the commit. A clean tree, equal
    ticks (the same-tick closing transient), an unreadable side (None)
    or HEAD ahead of disk are all silent - scope is exactly the seed
    form, nothing looser."""
    if head_tick is None or disk_tick is None or not state_dirty:
        return []
    if disk_tick > head_tick:
        return [("WARN", "account-uncommitted",
                 "state.json tick=%d on disk > HEAD tick=%d - round "
                 "accounting written but not committed (R1893 anchor: "
                 "closing stage-2 died before commit; push-missing half "
                 "= origin_gap_check face) - commit the accounting"
                 % (disk_tick, head_tick))]
    return []


def check_account_uncommitted(root, state, findings):
    """tech#61 guard face: compare the git-HEAD state.json tick with the
    on-disk ledger and name written-but-uncommitted accounting. Enforced
    every round by the routine probe consumption - the R1893 absorb
    pattern is named within one round instead of being silently
    absorbed by the next. Unusable disk ledger / unreadable HEAD copy /
    non-git tree all stay silent (other faces own those diseases)."""
    tick = state.get("tick") if isinstance(state, dict) else None
    if not isinstance(tick, int) or isinstance(tick, bool):
        return  # parse_state already FAILed the ledger
    head_tick = read_head_state_tick(root)
    if head_tick is None:
        return
    dirty = STATE_REL in _git_status_files(root)
    findings.extend(classify_account_uncommitted(head_tick, tick, dirty))


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
        check_root_litter(root, findings)
        check_stale_dirty(root, datetime.now(), findings)
        check_codex_freshness(root, datetime.now(), findings)
        check_queue_glue(root, findings)
        check_account_uncommitted(root, state, findings)
        check_aihot_stack(findings)
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
