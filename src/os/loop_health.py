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
  "round killed ..."          v2 liveness-budget evidence kill, silence
                              gate or hard cap (does NOT account a tick)
  "error ..."                 launcher error beat

Thresholds:
  --max-gap MIN  beat-to-beat gap advisory bound (default 20 = fleet
                 comm SLA; a legit v2 long round can run the full
                 240-min hard cap, so a SLA breach is WARN, not FAIL)
  --max-age MIN  staleness FAIL bound (default 288 = launcher lock
                 hard cap, tech#217 v2 budget: 1.2 x 240 min;
                 silence beyond it means the loop stopped)
  Any historical gap over 288 min = outage FAIL (same lock-age logic).
  A gap carried on the state outage_adjudicated ledger (documented
  historical window, tech#241) downgrades to a tagged WARN instead.

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
  WARN  heartbeat-outage-adjudicated documented outage window on the
                                   state outage_adjudicated ledger
                                   (tech#241); unlisted gaps still FAIL
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
  WARN  utf16-debris              root-level .c3-tmp file whose head
                                   bytes are a UTF-16 BOM - PS 5.1 `>`
                                   redirect residue (tech#198 family;
                                   R2331/R2355 anchors; tech#216)
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
                                   round (tech#58). Stays WARN unless a
                                   fresh watchdog heal row is in the
                                   ledger (tech#239, see INFO below).
  INFO  aihot-stack               down faces with an autoheal-watchdog
                                   heal row fresher than 3 x PT5M - the
                                   healer (tech#127) is live and owns
                                   the recovery; a manual heal on top
                                   would be the duplicate-healer race
                                   (tech#239 10-19 anchor: R2381 manual
                                   prose recovery raced the watchdog's
                                   three-cycle heal). Unreadable/stale/
                                   empty ledger keeps the WARN - a dead
                                   watchdog is the real gap (fail-closed).
  WARN  queue-glue               queue entry head 'NN. [' at a non-zero
                                   column in state/queue/*.md - entry
                                   written without a leading newline;
                                   line-anchored head scans miss glued
                                   entries (R1891 anchor: seed 58 glued
                                   to entry 57 tail went unsighted five
                                   rounds; tech#60)
  WARN  queue-dup-numbers        the same entry number heading two
                                   entries in one state/queue/*.md file -
                                   every queue cite of the number (focus
                                   lines, done notes, ledger references)
                                   turns ambiguous under a double-held
                                   number (R1895 anchor: tech.md held 41
                                   twice; tech#62)
  WARN  account-uncommitted     on-disk state.json tick ahead of the
                                   git-HEAD tick with the file dirty -
                                   closing stage-2 wrote the accounting
                                   but the round died before the commit
                                   (R1893 anchor; the push-missing half
                                   is the origin_gap_check face; tech#61)
  WARN  unaccounted-round-work  round-anchored commits (message head
                                   "R<N>") ahead of the state tick - a
                                   body landed round work whose
                                   accounting never ran (R2214 anchor;
                                   tech#155)
  WARN  orphan-work-face          deliverable-class file(s) (src/tests/
                                   tools/docs) uncommitted with mtime
                                   older than 48h - dead-round orphan
                                   work the 7-day sediment line misses
                                   (R2298/R2308 anchors; tech#187)

Exit codes: 0 = healthy (WARN allowed), 1 = any FAIL, 2 = usage/source.

Output modes:
    default        every finding printed (audit face, unchanged)
    --loop         routine loop-consumption face: the same analysis,
                   compact output - FAILs always print in full, WARNs
                   that embed only pre-cutoff dates (adjudicated
                   log-order / heartbeat-gap history) fold into one
                   suppression count; log-order pairs carried on the
                   state log_order_adjudicated ledger (tech#215) fold
                   into a separate suppressed-adjudicated count.
                   Structural/every-run WARNs (no
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
LOCK_AGE_MIN = 288  # iteration_loop.ps1 LockMaxAgeMinutes (tech#217 v2: auto = 1.2 x 240min hard cap) - staleness bound
SLA_GAP_MIN = 20   # fleet comm SLA - advisory bound (v2 rounds may run the 240m hard cap)
STATE_TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
GAP_MIN_RE = re.compile(r"beat gap (\d+) min")
FOLD_DENSE_DEFAULT = 5  # tech#20: dense same-code WARN group fold size
# tech#215 (R2353): log-order adjudication ledger tag. A backward
# narrative pair carried on state.log_order_adjudicated gets this tag at
# parse time; the --loop face folds tagged pairs into a separate
# suppressed-adjudicated count (account_drift_adjudicated's structural
# twin), while the full audit face prints them unchanged.
LOG_ORDER_ADJ_TAG = " [adjudicated: tech#215]"
# tech#221 (R2362): canon-doc constant drift guard. The code-level
# BEAT_POLICY constant is the single source of truth (tech#220 ruling 3);
# the os-protocol s6 law line is the machine-consumed canon face. The
# 2026-10-18 35min lag (tech#219 code bump -> doc law line left stale
# until the tech#220 round) is the anchored miss this probe guards.
# Section scoping is the zero-false-positive law (criterion 1): the
# changelog keeps retired values in prose ("active 间隙 <=35min") that
# must never leak a false positive into the live law face.
OS_PROTOCOL_S6_HEADING_RE = re.compile(r"^##\s*§?6\b")
NEXT_SECTION_RE = re.compile(r"^##\s")
ACTIVE_LAW_RE = re.compile(r"active\s*≤\s*(\d+)\s*min")
# tech#222 (R2363): second canon-drift anchor - the s5 lock-age law
# line ("锁龄 N 分钟=FAIL") vs loop_health.LOCK_AGE_MIN. Anchored miss:
# tech#217 v2 raised LOCK_AGE_MIN 40->288 while the doc law line kept
# the retired 40 value until the R2362 hand-sync (tech#219 35min lag
# family, second case). Section scoping is the same zero-false-positive
# law; the changelog keeps retired "锁龄 40 分钟" prose that must never
# leak in. Seed correction (honest note): the tech#222 seed and the
# v1.16 changelog row call this the "s4" line, but the law line lives
# in s5 度量 - the s4 heading body has no lock-age text, so scoping to
# s4 would anchor nothing (a guard that can never fire).
OS_PROTOCOL_S5_HEADING_RE = re.compile(r"^##\s*§?5\b")
LOCK_AGE_LAW_RE = re.compile(r"锁龄\s*(\d+)\s*分钟\s*=\s*FAIL")
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
# tech#107: codex canonical version-face drift guard. The README section-1
# five-dimension table carries one version cell per dimension file while
# each dimension file carries its own header version. Two historical
# anchors: R1992 (chronicle header stuck at v1.1 while the README cell and
# changelog had moved to v1.2, caught by a human re-read across days) and
# R1998 (humanities header stuck at v1.6 while README cell + changelog +
# in-file content were already v1.7, caught by this guard's own probe).
# Freshness (tech#37) watches mtime; this face watches the version lineage.
CODEX_README_NAME = "README.md"
CODEX_README_SECTION_RE = re.compile(r"§1[^\n]*五维目录|五维目录")
CODEX_README_SECTION_END_RE = re.compile(r"§2\b")
CODEX_README_ROW_RE = re.compile(r"^\|.*`([^`]+\.md)`")
CODEX_VER_RE = re.compile(r"\bv(\d+\.\d+)\b")
# tech#111: the changelog tail is the batch-first surface - R1992 and
# R1998 both wrote the 变更记录 line first, so a batch that bumps the
# changelog but leaves BOTH the section-1 cell and the file header
# behind reads as a false two-face agreement. Third face of the same
# guard: only names the changelog-alone-leads shape, numeric compare
# (v1.10 > v1.9), section-scoped to the 变更记录 block.
CODEX_CHANGELOG_SECTION_RE = re.compile(r"变更记录")
CODEX_CHANGELOG_ENTRY_RE = re.compile(
    r"(city-chronicle|city-culture|city-humanities|"
    r"city-residents|city-spirit)\s+v(\d+\.\d+)")
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
# tech#239: the autoheal watchdog (src/os/aihot_watchdog.py, tech#127)
# heals the stack on a PT5M cadence and appends every heal row to this
# ledger. A heal row fresher than 3 x PT5M means the down faces below
# are already being fixed - naming the WARN inside that window is the
# duplicate-healer race (10-19 anchor: 10:1x four-face kill healed by
# the watchdog at 10:20:30/10:25:29/10:30:28 while R2381 ran a 6-minute
# manual prose recovery on top of it).
AIHOT_WATCHDOG_LEDGER_REL = ("data", "pipeline",
                             "aihot-watchdog-ledger.jsonl")
AIHOT_HEAL_FRESH_WINDOW_S = 3 * 5 * 60  # 3 x PT5M watchdog cycles
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
QUEUE_HEAD_NUM_RE = re.compile(r"^(\d{1,3})\. ")  # entry head at column 0
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
# tech#64: .c3-tmp cross-round leftover guard. The root litter face
# (tech#22) only scans root-level r<digit> probe files, so the .c3-tmp
# evidence dir had no machine face at all - the R1895 anchor: five
# closing-stage files (close script + data + three probe evidence files)
# sat uncommitted through a whole round because the two-stage closing
# commit picked up only the state/export files (cleanup-hook recurrence
# case 3, C-20261009-02 order 3; R1896 round-open git status was the
# only detector). Committed evidence files are in the account by
# definition; in-flight files are naturally fresh (written this
# round), so a .c3-tmp file with mtime > 24h is a leftover by
# definition. Under LITTER_FAIL_N stale files = one WARN per file;
# at LITTER_FAIL_N+ = one aggregate FAIL (recurring pattern, the
# check_root_litter calibration) - advisory per the guard family law
# (tech#22/#31/#37/#58/#60/#61/#62).
# Boundary note (tech#114 correction, superseded by tech#234): the
# pre-234 face listed via _git_untracked_files (--exclude-standard),
# so .gitignore applied - and .gitignore's ".c3-tmp/" rule (tech#157
# born-fix) made the whole face silently blind on the real repo: the
# R2375/R2376 11-file debris sat with every probe reading zero rows,
# and the 48h bound was never the binding constraint. tech#234
# switches the face to a direct filesystem walk (the tech#216
# utf16-debris method), so ignore-status no longer matters;
# __pycache__ segments are exempt (an imported .c3-tmp script drops a
# bytecode cache - not round debt). The git seam stays unchanged for
# its other consumers (audio-tmp-residue, broken-round debris).
C3TMP_DIR_PREFIX = ".c3-tmp/"
C3TMP_STALE_HOURS = 24.0
# Round-numbered middleware name convention: r<N>_<rest> under .c3-tmp/
ROUND_DEBRIS_RE = re.compile(r"^r(\d+)_")
# tech#216: PS 5.1 `>` redirect residue guard. The pit law lived only in
# tools/run_suite.ps1's header (tech#198) while ad-hoc round probes kept
# re-treading it (R2331 + R2355 x2 anchors: UTF-16 BOM evidence files
# that read_file rejects as binary). This face names the debris at the
# round-end probe so recurrence no longer relies on self-recall.
UTF16_BOM_HEADS = (b"\xff\xfe", b"\xfe\xff")
# tech#114: audio-line TTS tmp working-dir residue guard. R2005 anchor:
# 75 untracked TTS intermediates (10.59 MB) sat across rounds under
# data/storylines/audio/sc005-0X-v1-tmp/ because every hand-built close
# list committed only the hand-off faces (s1/e4-material/beats) and
# missed the tmp working-dir face - the round-end cleanup hook
# (C-20261009-02 order 3) failed twice (R1895 .c3-tmp first case,
# R2005 audio tmp second case), so per the 2026-10-10 13:07 CEO order
# (recurrence = gate failure = escalate: checklist -> script assertion)
# the residue face gets a machine guard. Close action = batch-commit the
# tmp dir (sc001/sc005-01..03 full-commit precedent; .gitignore L24
# covers only audio root *.mp3, tmp subdir files are committable).
# Ignored artifacts (*.wav bed assets, *.pyc) are deliberately out of
# the git account and never read as residue - the listing seam applies
# .gitignore (tech#114 correction above).
AUDIO_DOMAIN_PREFIX = "data/storylines/audio/"
AUDIO_TMP_DIR_SUFFIX = "-tmp"
AUDIO_TMP_LIST_CAP = 3
# tech#187: orphan-deliverable guard. R2298/R2308 anchors: two rounds
# died post-suite pre-commit, leaving landed src deliverables
# uncommitted; the stale-dirty face names sediment only at 7 days, so
# the 2-7 day band had no machine face and the orphans waited for a
# human adopt (R2315). Deliverable-class trees only (src/tests/tools/
# docs); in-flight domain whitelist is defense-in-depth (dirty-face
# split law); an uncommitted file with mtime > 48h in a deliverable
# tree is orphan work by definition.
ORPHAN_DELIVERABLE_HOURS = 48.0
ORPHAN_DELIVERABLE_DIR_PREFIXES = ("src/", "tests/", "tools/", "docs/")
# tech#68: status-export contract guard. R1901 anchor: the CEO-facing
# docs/status-export.json drifted silently for ~1700 rounds - "do" grew
# into a 3406-char paragraph (product-priority law section 5 wants a
# one-line current-activity), 39 outs entries degraded to bare strings
# and 67 results entries became [tick, full-log-line] pairs, while the
# MiniGame siliconwatch generate.ps1 v6.2 shaper silently fell back to
# the curated face on every bad field - the board went stale with zero
# alarm anywhere on the producing side. This guard enforces the
# producing side so drift is named within one round, not 1700.
# Contract constants are same-source with the generator-side caps
# (MiniGame tools/siliconwatch generate.ps1 v6.2 field-shaping law);
# WARN level per the guard family law (tech#22/#31/#37/#58/#60/#61/
# #62/#64/#71).
EXPORT_REL = Path("docs") / "status-export.json"
EXPORT_DO_MAX_CHARS = 120  # "current activity" is one line (law sec.5)
EXPORT_OUT_MAX_N = 12
EXPORT_CHIP_MAX_N = 14
EXPORT_RES_MAX_N = 4
EXPORT_OUT_STATES = ("on", "wait", "off")
EXPORT_OUT_TXT_MAX = 64
EXPORT_OUT_TAG_MAX = 24
EXPORT_RES_V_MAX = 16
EXPORT_RES_K_MAX = 14
# tech#71 parity facets - caps mirrored from the consumer truth
# (MiniGame tools/siliconwatch strings.json labels.export_face +
# generate.ps1 v6.2 normalization loop): the shaper drops depts/chips
# cells whose text is missing or shorter than 2 chars, silently renames
# any non live|wip chip class to 'wip' and any non 0|1|2 dept s to 1,
# and truncates over-cap text - all invisible on the CEO board.
EXPORT_DEPT_N_MAX = 24     # shaper EF.dept_n_max
EXPORT_DEPT_T_MAX = 96     # shaper EF.dept_t_max
EXPORT_DEPT_STATES = (0, 1, 2)  # shaper: missing s defaults to 1
EXPORT_CHIP_TXT_MAX = 14   # shaper EF.chip_txt_max
EXPORT_CHIP_CLASSES = ("live", "wip")
EXPORT_CELL_MIN_TXT = 2    # shaper drops cells with text shorter than 2
EXPORT_TS_FUTURE_TOL_MIN = 5.0   # mirror cross_check state-ts-future
EXPORT_TS_STALE_COPY_MIN = 60.0  # ts far behind its own file write time
EXPORT_TS_MAX_AGE_MIN = 1440.0   # P-61 export refresh law (<=24h)
# tech#155: unaccounted-round-work guard. The R2214 anchor: a prior body
# landed three round commits (delivery + export + fire receipt, every
# message head-anchored "R2214:") while its narrative claimed the
# accounting was complete - finalize_state was never called, state.json
# stayed at tick 2213 with no R2214 ledger line, and the successor body
# found the gap only by manual git-log archaeology. The beats-vs-tick
# faces cannot see this shape at all (a body that dies before closing
# writes no done beat either - the commits are the only trace). This
# face reads recent commit subjects and names any head-anchored round
# AHEAD of the state tick: work committed but never accounted. A subject
# without an R-anchor is another window's commit (MV sprint session /
# interactive session) and never counts; a git failure stays
# advisory-silent (never breaks the probe). Two-segment middle state
# (the legal transient): a live round's own intermediate commits
# legitimately sit ahead of the tick between commit and close - that
# window IS the work-ahead-of-accounting shape and reads WARN by
# design (advisory); the next round-open probe after a healthy close
# reads zero (anchored R == tick). WARN level per the guard family law
# (tech#22/#31/#37/#58/#60/#61/#62/#64).
COMMIT_ROUND_RE = re.compile(r"^R(\d{3,6})\b")
GIT_LOG_SCAN_N = 12  # one broken round's whole commit trail fits


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


def load_outage_adjudicated(state):
    """tech#241 (R2388): state-carried ledger of documented historical
    heartbeat-outage windows, account_drift_adjudicated's outage twin.
    Entry shape: {"date": "YYYY-MM-DD", "gap_min": <int>}. An outage FAIL
    whose (start date, rounded gap minutes) matches an entry downgrades to
    a tagged WARN; anything unrecognized stays a FAIL like any new window
    (fail-closed - malformed shapes widen nothing)."""
    block = state.get("outage_adjudicated") if isinstance(state, dict) else None
    out = set()
    if isinstance(block, dict):
        block = block.get("windows")
    if not isinstance(block, list):
        return out
    for w in block:
        if not isinstance(w, dict):
            continue
        d, g = w.get("date"), w.get("gap_min")
        if (isinstance(d, str) and len(d) == 10 and d[4] == "-" and d[7] == "-"
                and isinstance(g, int) and not isinstance(g, bool) and g > 0):
            out.add((d, g))
    return out


def load_log_order_adjudicated(state):
    """tech#215 (R2352 probe anchor: 47 backward log-order pairs, 46 of
    them pre-10-15 history the --loop date cutoff already folds, plus the
    R2349/R2350 pair - a fresh in-window pair that re-WARNs every loop
    face). State-carried adjudication ledger, account_drift_adjudicated's
    narrative twin: {"pairs": [["<prev-ts>", "<cur-ts>"], ...]} (a bare
    list of pairs also accepted). Malformed data widens nothing -
    unrecognized shapes return an empty set and the pair keeps warning
    like any new finding."""
    block = state.get("log_order_adjudicated") if isinstance(state, dict) else None
    if isinstance(block, dict):
        block = block.get("pairs")
    if not isinstance(block, list):
        return set()
    pairs = set()
    for item in block:
        if (isinstance(item, (list, tuple)) and len(item) == 2
                and all(isinstance(x, str) for x in item)):
            pairs.add((item[0], item[1]))
    return pairs


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
    adj_pairs = load_log_order_adjudicated(state)
    for i in range(1, len(stamps)):
        if stamps[i] < stamps[i - 1]:
            msg = ("log entry timestamps go backwards: %s -> %s "
                   "(narrative hygiene; approximate minutes allowed)"
                   % (stamps[i - 1], stamps[i]))
            if (stamps[i - 1], stamps[i]) in adj_pairs:
                msg += LOG_ORDER_ADJ_TAG
            findings.append(("WARN", "log-order", msg))
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
    """Beats -> (done [(ts, msg)], skip_n, timeout_n, error_n).

    timeout bucket = evidence kills that do NOT account a tick: the
    historical "round timeout killed ..." wall-clock face and the v2
    liveness-budget faces "round killed (budget=silence-kill ...)" /
    "round hard-cap killed ..." (tech#217)."""
    done, skip_n, timeout_n, error_n = [], 0, 0, 0
    for ts, msg in beats:
        if ROUND_DONE_RE.search(msg):
            done.append((ts, msg))
        elif "timeout" in msg or "killed" in msg:
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


def classify_orphan_deliverable(entries, now,
                                 hours=ORPHAN_DELIVERABLE_HOURS,
                                 prefixes=ORPHAN_DELIVERABLE_DIR_PREFIXES,
                                 skip=INFLIGHT_DIR_PREFIXES):
    """[(relpath, mtime-or-None)] -> sorted orphan relpaths (pure core).
    Deliverable-class trees only; deleted paths and whitelisted
    in-flight-domain paths never flag; an mtime older than `hours` in a
    deliverable tree flags (no upper band - a 9-day orphan is still an
    orphan; the 7-day sediment face names it too, advisory overlap)."""
    bound = hours * 3600.0
    orphan = []
    for rel, mtime in entries:
        if rel is None or mtime is None:
            continue
        if not any(rel.startswith(p) for p in prefixes):
            continue
        if any(rel.startswith(p) for p in skip):
            continue
        if (now - mtime).total_seconds() > bound:
            orphan.append(rel)
    return sorted(orphan)


def check_orphan_deliverable(root, now, findings):
    """tech#187 guard face: name deliverable-class orphan work (one WARN
    with the file list) - rounds that die post-suite pre-commit leave
    landed-but-uncommitted src/tests/tools/docs files; this face names
    them within one round on the routine probe consumption instead of
    waiting for the 7-day sediment line (R2298/R2308 anchors, human
    adopt R2315 - machine teeth per the escalation law)."""
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
    orphan = classify_orphan_deliverable(entries, now)
    if not orphan:
        return
    shown = ", ".join(orphan[:5]) + (" ..." if len(orphan) > 5 else "")
    findings.append(("WARN", "orphan-work-face",
                     "%d deliverable-class file(s) uncommitted for over "
                     "%g h: %s - dead-round orphan work (tech#187; "
                     "adopt-or-commit, not sediment yet)"
                     % (len(orphan), ORPHAN_DELIVERABLE_HOURS, shown)))


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


def parse_codex_readme_cells(text):
    """README text -> {filename: version-or-None}. Only section-1 (五维目录)
    table rows count: a backticked <name>.md plus the first vX.Y on the
    line. A row whose cell carries no version maps to None (cell-missing
    face). Rows outside the section never match (changelog lines mention
    bare filenames without backticks, section-2 tables carry no .md
    backticks). Pure core."""
    cells = {}
    in_section = False
    for line in text.splitlines():
        if CODEX_README_SECTION_RE.search(line):
            in_section = True
            continue
        if in_section and CODEX_README_SECTION_END_RE.search(line):
            in_section = False
        if not in_section or not line.lstrip().startswith("|"):
            continue
        m = CODEX_README_ROW_RE.search(line)
        if not m:
            continue
        vm = CODEX_VER_RE.search(line)
        cells[m.group(1)] = vm.group(1) if vm else None
    return cells


def parse_codex_header_version(text):
    """Dimension-file text -> header version or None. The established
    header form puts the version on line 1
    ('# 硅基城市编年史志（City Chronicle）v1.3'). Pure core."""
    first = text.splitlines()[0] if text else ""
    m = CODEX_VER_RE.search(first)
    return m.group(1) if m else None


def classify_codex_version_face(cells, headers):
    """cells: {filename: version-or-None} from README section-1;
    headers: {filename: version-or-None} for dimension files that exist
    on disk (missing files are the content board's face, never this
    guard's - tech#37 family law). -> sorted list of
    (code, filename, readme_version, header_version) where code is
    'drift' (both present, differ), 'cell' (README row without a version)
    or 'header' (existing file without a parseable header version).
    Pure core."""
    out = []
    for fn, header_ver in sorted(headers.items()):
        readme_ver = cells.get(fn, "missing")
        if readme_ver == "missing":
            out.append(("row", fn, None, header_ver))
        elif readme_ver is None:
            out.append(("cell", fn, None, header_ver))
        elif header_ver is None:
            out.append(("header", fn, readme_ver, None))
        elif readme_ver != header_ver:
            out.append(("drift", fn, readme_ver, header_ver))
    return out


def parse_codex_changelog_versions(text):
    """README text -> {filename.md: latest version} from the 变更记录
    section. Section-scoped like the section-1 cell parser (bare names
    outside the block never match); inside the block each line may
    mention one or more 'city-<dim> vX.Y' and the LAST mention per
    dimension wins (newest batch lines sit at the tail). Pure core."""
    versions = {}
    in_section = False
    for line in text.splitlines():
        if CODEX_CHANGELOG_SECTION_RE.search(line):
            in_section = True
            continue
        if in_section and line.startswith("#"):
            in_section = False  # a later section closes the block
        if not in_section:
            continue
        for m in CODEX_CHANGELOG_ENTRY_RE.finditer(line):
            versions[m.group(1) + ".md"] = m.group(2)
    return versions


def codex_version_tuple(v):
    """'1.10' -> (1, 10) so the leads-test compares numerically, never
    lexically ('1.10' > '1.9' as strings would say False). Pure core."""
    return tuple(int(part) for part in v.split("."))


def classify_codex_changelog_face(cells, headers, changelog):
    """-> sorted [(filename, changelog_ver, readme_ver, header_ver)]
    for dimensions whose changelog tail version leads BOTH faces that
    hold a version. The two-sided face above already names cell/header
    drift and the absent-version faces name missing cells/headers, so
    this third face only fires on the tech#111 gap shape: changelog
    moved, both faces stuck (false agreement). Pure core."""
    out = []
    for fn, cl_ver in sorted(changelog.items()):
        readme_ver = cells.get(fn)
        header_ver = headers.get(fn)
        if not (readme_ver and header_ver):
            continue  # absent/versionless sides belong to the cell/header
            # (or content-board) faces - never noise-overlap here
        cl_t = codex_version_tuple(cl_ver)
        if (cl_t > codex_version_tuple(readme_ver)
                and cl_t > codex_version_tuple(header_ver)):
            out.append((fn, cl_ver, readme_ver, header_ver))
    return out


def check_codex_version_face(root, findings):
    """tech#107 guard face: WARN when a codex dimension file's header
    version drifts from the README section-1 version cell (R1992
    chronicle + R1998 humanities anchors). Advisory family law: never
    breaks the probe rc; a missing dimension file stays the content
    board's matter; an unreadable README (with the codex dir present) is
    one fail-closed WARN."""
    codex_dir = root / CODEX_DIR
    if not codex_dir.is_dir():
        return  # no codex layer at all -> content board's face, silent
    try:
        readme_text = (codex_dir / CODEX_README_NAME).read_text(
            encoding="utf-8")
    except OSError:
        findings.append(("WARN", "codex-version-readme",
                         "codex README unreadable - version-face guard "
                         "fail-closed (tech#107)"))
        return
    cells = parse_codex_readme_cells(readme_text)
    headers = {}
    for name in CODEX_DIMENSIONS:
        try:
            head_text = (codex_dir / name).read_text(
                encoding="utf-8")
        except OSError:
            continue  # existence = content board's face
        headers[name] = parse_codex_header_version(head_text)
    for code, fn, readme_ver, header_ver in classify_codex_version_face(
            cells, headers):
        if code == "drift":
            msg = ("%s: header v%s != README cell v%s - version-lineage "
                   "drift (R1992 chronicle / R1998 humanities anchors)"
                   % (fn, header_ver, readme_ver))
        elif code == "row":
            msg = ("%s: no README section-1 row - dimension file "
                   "orphaned from the five-dimension table" % fn)
        elif code == "cell":
            msg = "%s: README section-1 row carries no version cell" % fn
        else:  # header
            msg = "%s: file header carries no parseable version" % fn
        findings.append(("WARN", "codex-version-" + code, msg))
    changelog = parse_codex_changelog_versions(readme_text)
    for fn, cl_ver, readme_ver, header_ver in classify_codex_changelog_face(
            cells, headers, changelog):
        r_txt = "v" + readme_ver if readme_ver else "absent"
        h_txt = "v" + header_ver if header_ver else "absent"
        findings.append(("WARN", "codex-version-changelog",
                         "%s: changelog tail v%s leads README cell %s and "
                         "header %s - batch wrote the changelog line but "
                         "bumped neither face (tech#111 third face; "
                         "R1992/R1998 batch-first anchors)"
                         % (fn, cl_ver, r_txt, h_txt)))


def _beat_policy_active_min():
    """close_commit.BEAT_POLICY.active_gap_max_min, or None when the
    module/constant is unreachable (advisory face stays silent)."""
    try:
        import close_commit  # src/os sibling (sys.path[0] when run as script)
        v = close_commit.BEAT_POLICY.get("active_gap_max_min")
    except Exception:
        return None
    return v if isinstance(v, int) and not isinstance(v, bool) else None


def _protocol_section(text, heading_re):
    """os-protocol text + heading regex -> that section's body (lines
    between the matched heading and the next '## ' heading), joined as
    one string. Shared by the section-scoped canon parsers so retired
    values in other sections and changelog prose never leak in."""
    section, in_section = [], False
    for line in text.splitlines():
        if in_section and NEXT_SECTION_RE.match(line):
            break
        if heading_re.match(line):
            in_section = True
            continue
        if in_section:
            section.append(line)
    return "\n".join(section)


def parse_beat_law_min(text):
    """os-protocol text -> the single 'active <=Nmin' value in the s6
    law section, or None. Section-scoped by design: the changelog keeps
    retired values in prose that must never leak in (tech#221 criterion
    1). Zero or multiple anchors -> None (ambiguous input never guesses)."""
    section = _protocol_section(text, OS_PROTOCOL_S6_HEADING_RE)
    values = [int(m.group(1)) for m in ACTIVE_LAW_RE.finditer(section)]
    return values[0] if len(values) == 1 else None


def parse_lock_age_law_min(text):
    """os-protocol text -> the single '锁龄 N分钟=FAIL' value in the s5
    measurement section, or None. Same section-scoped design as
    parse_beat_law_min (tech#222 criterion 1): the changelog keeps
    retired 40min prose that must never leak in. Zero or multiple
    anchors -> None (ambiguous input never guesses)."""
    section = _protocol_section(text, OS_PROTOCOL_S5_HEADING_RE)
    values = [int(m.group(1)) for m in LOCK_AGE_LAW_RE.finditer(section)]
    return values[0] if len(values) == 1 else None


def classify_beat_policy_drift(doc_value, code_value):
    """(doc, code) -> WARN finding or None. None on either side stays
    silent (one-way advisory: unanchored/ambiguous law text or an
    unreachable constant is a skip, never a false positive)."""
    if doc_value is None or code_value is None or doc_value == code_value:
        return None
    return ("WARN", "canon-beat-policy-drift",
            "os-protocol s6 law line 'active <=%dmin' disagrees with "
            "close_commit BEAT_POLICY.active_gap_max_min=%d - the code "
            "constant is the single source of truth (tech#220), update "
            "the doc law line (tech#219 35min lag pattern)"
            % (doc_value, code_value))


def classify_lock_age_drift(doc_value, code_value):
    """(doc, code) -> WARN finding or None. Same one-way advisory
    contract as classify_beat_policy_drift: None on either side stays
    silent (unanchored/ambiguous law text or an unreachable constant is
    a skip, never a false positive)."""
    if doc_value is None or code_value is None or doc_value == code_value:
        return None
    return ("WARN", "canon-lock-age-drift",
            "os-protocol s5 law line 'lock-age %dmin = FAIL' disagrees "
            "with loop_health LOCK_AGE_MIN=%d - the code constant is "
            "the single source of truth (tech#217 v2), update the doc "
            "law line (tech#222: R2362 40min lag pattern)"
            % (doc_value, code_value))


def check_canon_beat_policy_drift(root, findings):
    """tech#221/tech#222: canon-doc vs code-constant consistency probe
    (advisory, never breaks the probe; absent/unreadable canon file
    stays silent). Two anchors, both one-way WARN advisories: s6
    'active <=Nmin' law line vs close_commit BEAT_POLICY.active_gap_max_min
    (tech#221), and s5 lock-age law line vs loop_health LOCK_AGE_MIN
    (tech#222)."""
    path = root / "docs" / "os-protocol.md"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return
    f = classify_beat_policy_drift(parse_beat_law_min(text),
                                   _beat_policy_active_min())
    if f:
        findings.append(f)
    f = classify_lock_age_drift(parse_lock_age_law_min(text),
                                LOCK_AGE_MIN)
    if f:
        findings.append(f)


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


def read_watchdog_ledger(path):
    """Ledger path -> text or None. Any read error maps to None so the
    caller fail-closes to the plain WARN (tech#239 Q3: an unreadable
    ledger must never suppress the down-stack finding)."""
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def watchdog_heal_fresh(ledger_text, now_dt=None,
                        window_s=AIHOT_HEAL_FRESH_WINDOW_S):
    """Ledger jsonl text -> (fresh, detail) pure core (tech#239).

    Scans rows for event == "heal" with a parsable "ts"
    ("YYYY-MM-DD HH:MM:SS", the aihot_watchdog append_row format); the
    newest decides. Malformed/non-heal rows are skipped, never fatal
    (append-only jsonl). A future-stamped row still counts as fresh
    (clock-skew guard, same family as the state-ts faces). No parsable
    heal row -> (False, ...) so a dead watchdog keeps the WARN."""
    if now_dt is None:
        now_dt = datetime.now()
    newest = None
    for line in (ledger_text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if not isinstance(row, dict) or row.get("event") != "heal":
            continue
        try:
            stamp = datetime.strptime(str(row.get("ts")),
                                      "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
        if newest is None or stamp > newest:
            newest = stamp
    if newest is None:
        return False, "no parsable heal row in ledger"
    age = (now_dt - newest).total_seconds()
    if age < 0:
        age = 0.0  # future stamp: clock skew, still a live healer
    detail = ("newest heal row %s (%.0fs old, window %ds)"
              % (newest.strftime("%Y-%m-%d %H:%M:%S"), age, window_s))
    return (age <= window_s), detail


def check_aihot_stack(findings, timeout_s=AIHOT_PROBE_TIMEOUT_S,
                      probe=None, ledger_path=None, now_dt=None,
                      ledger_reader=None):
    """tech#58 guard face: probe the AIHOT stack HTTP faces and name any
    down face (one WARN). Machine-enforced every round by the routine
    probe consumption - a dead stack is named within one round.

    tech#239: a down stack is not automatically a WARN. The autoheal
    watchdog ledger (aihot_watchdog, tech#127) is consulted first: a
    heal row fresher than 3 x PT5M means the healer is live and mid-
    cycle, so the finding is downgraded to INFO "watchdog healing in
    progress" (a manual heal on top would be the duplicate-healer race,
    10-19 anchor). Zero/stale/unreadable ledger keeps the WARN - a dead
    watchdog is the real gap and must stay loud (fail-closed)."""
    if probe is None:
        probe = probe_http_face  # module global read at call time (test seam)
    api_url = os.environ.get("AIHOT_API_URL", AIHOT_API_URL)
    web_url = os.environ.get("AIHOT_WEB_URL", AIHOT_WEB_URL)
    down = classify_aihot_faces(probe(api_url, timeout_s),
                                probe(web_url, timeout_s))
    if down:
        if ledger_reader is None:
            ledger_reader = read_watchdog_ledger
        if ledger_path is None:
            ledger_path = REPO.joinpath(*AIHOT_WATCHDOG_LEDGER_REL)
        try:
            text = ledger_reader(ledger_path)
        except Exception:
            text = None  # contract break: fail closed to the WARN below
        if text is not None:
            fresh, detail = watchdog_heal_fresh(text, now_dt=now_dt)
            if fresh:
                findings.append(("INFO", "aihot-stack",
                                 "AIHOT stack face(s) down - watchdog "
                                 "healing in progress (%s); autoheal on "
                                 "the PT5M cadence owns the recovery "
                                 "(tech#127), a manual heal on top would "
                                 "be the duplicate-healer race (tech#239)"
                                 % detail))
                return
    findings.extend(down)


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


def classify_queue_dup_numbers(files):
    """{name: text} -> findings (pure core). An entry head number is
    'NN. ' at column 0; the same number heading two entries in one
    file is a double-booked queue slot - every cite of the number
    (focus lines, done notes, ledger references) becomes ambiguous
    about which entry it means (the R1895 anchor: tech.md held 41
    twice - the ollama saturation monitor and the lcard pilot). One
    WARN per file naming each reused number with its count. Out-of-
    order numbers are NOT a finding (append order = delivery order
    is legal; only reuse is the disease - tech#62 scope note).
    Clean queue files yield no findings (silent PASS like the other
    guard faces)."""
    findings = []
    for name in sorted(files):
        seen = {}
        for line in files[name].splitlines():
            m = QUEUE_HEAD_NUM_RE.match(line)
            if not m:
                continue
            seen.setdefault(m.group(1), []).append(m.start(1))
        reused = {n: pos for n, pos in seen.items() if len(pos) >= 2}
        if not reused:
            continue
        shown = ", ".join("%s x%d" % (n, len(reused[n]))
                          for n in sorted(reused, key=int))
        findings.append(("WARN", "queue-dup-numbers",
                         "%d reused entry number(s) in %s: %s - a "
                         "double-held number makes every queue cite of "
                         "it ambiguous (focus lines / done notes / "
                         "ledger references); renumber the "
                         "less-referenced arrival and leave a cross-ref "
                         "note (R1895 anchor: 41 held twice in tech.md); "
                         "append order is legal, only reuse is the "
                         "disease" % (len(reused), name, shown)))
    return findings


def check_queue_dup_numbers(root, findings):
    """tech#62 guard face: scan every state/queue/*.md for entry head
    numbers reused by two entries. Machine-enforced every round by the
    routine probe consumption - a double-booked number is named within
    one round instead of at the next hand-written head count. A
    missing queue dir stays silent (existence is the loop engine's
    face, not this guard's); unreadable files are skipped (not this
    face's matter)."""
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
    findings.extend(classify_queue_dup_numbers(files))


def _git_untracked_files(root, _run=None):
    """`git ls-files --others --exclude-standard` stdout -> [relpath]
    (untracked only, git's forward-slash form, .gitignore APPLIED).
    Any git failure - not a work tree, git missing, timeout - yields
    []: this face is advisory and never breaks the probe. _run is the
    injection seam for tests. tech#114 correction: the bare --others
    form does NOT apply .gitignore (the tech#64 note claiming it did
    was wrong - the R1900 *.pyc catch and the sc001-01-v4-tmp *.wav
    assets both surfaced only because exclusions were off); passing
    --exclude-standard makes ignored files - deliberately out of the
    git account - never read as residue for any consumer of this
    seam (tech#64/#66/#114)."""
    if _run is None:
        _run = subprocess.run
    try:
        p = _run(["git", "ls-files", "--others", "--exclude-standard",
                  "-z"],
                 cwd=str(root), capture_output=True, timeout=GIT_TIMEOUT_S)
    except (OSError, subprocess.TimeoutExpired):
        return []
    if p.returncode != 0:
        return []
    return [c.decode("utf-8", "replace") for c in p.stdout.split(b"\0") if c]


def classify_c3tmp_stale(entries, now, stale_hours=C3TMP_STALE_HOURS):
    """[(relpath, mtime-or-None)] -> sorted stale relpaths (pure core).
    Only paths under .c3-tmp/ age the test; an mtime strictly older
    than stale_hours flags. __pycache__ segments never flag (an
    imported .c3-tmp script drops a bytecode cache - not round debt).
    Deleted/unreadable paths (None) never flag - same advisory skip
    as the sediment guard's deleted paths."""
    bound = stale_hours * 3600.0
    stale = []
    for rel, mtime in entries:
        if rel is None or mtime is None:
            continue
        if not rel.startswith(C3TMP_DIR_PREFIX):
            continue
        if "__pycache__/" in rel:
            continue
        if (now - mtime).total_seconds() > bound:
            stale.append(rel)
    return sorted(stale)


def check_c3tmp_stale(root, now, findings):
    """tech#64 guard face, tech#234 repair + escalation: name .c3-tmp
    evidence files left behind across rounds (mtime > 24h). The walk
    is a direct recursive filesystem scan (tech#216 method):
    .gitignore's ".c3-tmp/" rule (tech#157) made the pre-234 git-seam
    listing (--exclude-standard) read zero rows on this repo - the
    R2375/R2376 11-file debris anchor sat invisible to every probe.
    A missing .c3-tmp dir and unreadable files stay silent (advisory
    face, never breaks the probe). Under LITTER_FAIL_N stale files =
    one WARN per file (single-round debt, advisory); at LITTER_FAIL_N+
    = one aggregate FAIL (recurring cleanup-hook pattern, the
    check_root_litter calibration). Enforced every round by the
    routine probe consumption - an R1895-form leftover is named
    within one round instead of at the next round's git status read."""
    c3 = Path(root) / C3TMP_DIR_PREFIX
    if not c3.is_dir():
        return
    entries = []
    mtimes = {}
    for path in sorted(c3.rglob("*")):
        try:
            if not path.is_file():
                continue
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
        except OSError:
            continue
        rel = C3TMP_DIR_PREFIX + path.relative_to(c3).as_posix()
        entries.append((rel, mtime))
        mtimes[rel] = mtime
    stale = classify_c3tmp_stale(entries, now)
    if not stale:
        return
    if len(stale) >= LITTER_FAIL_N:
        shown = ", ".join(
            "%s (%.1f h)" % (
                rel, (now - mtimes[rel]).total_seconds() / 3600.0)
            for rel in stale[:5])
        fold = " ..." if len(stale) > 5 else ""
        findings.append(("FAIL", "c3tmp-stale",
                         "%d cross-round .c3-tmp leftover(s) older than "
                         "%g h: %s%s - recurring cleanup-hook debt "
                         "(R2375/R2376 anchor: 11 files sat invisible "
                         "while every probe read zero; C-20261009-02 "
                         "order 3) - batch-commit or delete at round end"
                         % (len(stale), C3TMP_STALE_HOURS, shown, fold)))
        return
    for rel in stale:
        age_h = (now - mtimes[rel]).total_seconds() / 3600.0
        findings.append(("WARN", "c3tmp-stale",
                         "%s uncommitted for %.1f h (> %g h) - round "
                         "evidence written but never settled (R1895 "
                         "anchor: five closing-stage files sat a full "
                         "round; cleanup hook C-20261009-02 order 3) - "
                         "batch-commit or delete at round end"
                         % (rel, age_h, C3TMP_STALE_HOURS)))


def classify_utf16_debris(samples):
    """[(relpath, head-bytes)] -> sorted relpaths whose head is a
    UTF-16 BOM (pure core). None heads (unreadable) never flag."""
    flagged = []
    for rel, head in samples:
        if head is None:
            continue
        for bom in UTF16_BOM_HEADS:
            if head.startswith(bom):
                flagged.append(rel)
                break
    return sorted(flagged)


def check_utf16_debris(root, findings):
    """tech#216 guard face: name root-level .c3-tmp files that start
    with a UTF-16 BOM - the residue of pointing PS 5.1 ``>`` at a
    native tool's output (tech#198 pit family; R2331 + R2355 x2
    anchors: the evidence file came back as binary that read_file
    rejects, killing the chain). Recapture with tools/cap_utf8.py and
    delete the debris at round end. A missing .c3-tmp dir and
    unreadable files stay silent (advisory face, never breaks the
    probe)."""
    c3 = Path(root) / C3TMP_DIR_PREFIX
    if not c3.is_dir():
        return
    samples = []
    for child in sorted(c3.iterdir()):
        if not child.is_file():
            continue
        try:
            with open(child, "rb") as fh:
                head = fh.read(2)
        except OSError:
            continue
        samples.append((C3TMP_DIR_PREFIX + child.name, head))
    for rel in classify_utf16_debris(samples):
        findings.append(("WARN", "utf16-debris",
                         "%s starts with a UTF-16 BOM - PS 5.1 `>` "
                         "redirect residue (tech#198 family; R2331/R2355 "
                         "anchors) - recapture via tools/cap_utf8.py and "
                         "delete the debris at round end" % rel))


def classify_audio_tmp_residue(relpaths, domain_prefix=AUDIO_DOMAIN_PREFIX,
                                list_cap=AUDIO_TMP_LIST_CAP):
    """untracked paths under data/storylines/audio/*-tmp/ -> one WARN
    row or none (pure core). A file counts only inside a tmp WORKING
    DIR (a directory component ending in -tmp below the domain
    prefix): loose audio-root files are their own face, and the cards
    domain (data/storylines/cards/*-tmp/) is deliberately out of scope -
    this guard's anchor is the audio TTS face; cards stays on the
    hand-built close lists until it produces its own case. Backslashes
    normalize to git's forward-slash form. One WARN per repo (not per
    file): count + capped examples + the tech#60 "+N more" fold."""
    rows = []
    hits = []
    for rel in relpaths:
        if not rel:
            continue
        norm = rel.replace("\\", "/")
        if not norm.startswith(domain_prefix):
            continue
        parts = norm[len(domain_prefix):].split("/")
        # last part is always the file name; any deeper directory
        # component naming a tmp working dir puts the file in scope
        if any(p.endswith(AUDIO_TMP_DIR_SUFFIX) for p in parts[:-1]):
            hits.append(norm)
    if not hits:
        return rows
    hits.sort()
    shown = ", ".join(hits[:list_cap])
    extra = len(hits) - min(len(hits), list_cap)
    fold = " (+%d more)" % extra if extra > 0 else ""
    rows.append(("WARN", "audio-tmp-residue",
                 "%d untracked file(s) under audio tmp working dirs: %s%s"
                 " - TTS intermediates outside the close list (R2005 "
                 "anchor: 75 files / 10.59 MB sat 9+ rounds; sc001/sc005 "
                 "full-commit precedent) - batch-commit or delete the "
                 "tmp dir at the piece's closing round"
                 % (len(hits), shown, fold)))
    return rows


def check_audio_tmp_residue(root, findings, _run=None):
    """tech#114 guard face: name untracked audio-line TTS tmp working
    files left outside every hand-built close list. Fires on ANY
    untracked count - a fresh in-flight batch reads as advisory
    pressure to commit its hand-off faces promptly, while committed tmp
    dirs stay silent per the sc001/sc005 full-commit precedent. A
    non-git tree or any git failure stays silent (advisory face, never
    breaks the probe). Enforced every round by the routine probe
    consumption - an R2005-form residue is named within one round
    instead of at the next round's manual git status read. _run is the
    injection seam for tests."""
    findings.extend(classify_audio_tmp_residue(
        _git_untracked_files(root, _run)))


def classify_broken_round_debris(relpaths, tick):
    """untracked round-numbered .c3-tmp middleware (rN_*) whose round
    anchor N is neither the just-accounted round (tick) nor the round
    in flight (tick+1) -> sorted debris paths (pure core). Timing-robust
    against the probe running before or after the round's tick
    increment: the current round's own in-flight files never flag in
    either flow; anything numbered for an already-settled round is
    debris. tick None/non-int -> [] (no state anchor, advisory skip)."""
    if not isinstance(tick, int):
        return []
    debris = []
    for rel in relpaths:
        if not rel or not rel.startswith(C3TMP_DIR_PREFIX):
            continue
        m = ROUND_DEBRIS_RE.match(rel.split("/")[-1])
        if not m:
            continue
        if int(m.group(1)) not in (tick, tick + 1):
            debris.append(rel)
    return sorted(debris)


def check_broken_round_debris(root, state, findings):
    """tech#66 guard face: name untracked .c3-tmp middleware left by a
    broken-round prior body, keyed by the round-number anchor in the
    file name (R1893/R1895/R1897/R1899 family: a body dies before its
    delivery commit and the successor rebuilds context only via manual
    git-status archaeology). Catches what the mtime face (tech#64)
    cannot - fresh debris sits far inside its 48h bound. Advisory WARN;
    a missing state tick, a non-git tree or any git failure stays
    silent (never breaks the probe)."""
    tick = state.get("tick") if isinstance(state, dict) else None
    if not isinstance(tick, int):
        return
    for rel in classify_broken_round_debris(_git_untracked_files(root), tick):
        msg = ("%s untracked round middleware (round anchor "
               "outside [tick=%d, in-flight=%d]) - broken-round "
               "prior-body debris: absorb via git-status "
               "archaeology or delete (R1895/R1899 anchors)"
               % (rel, tick, tick + 1))
        if rel.endswith(".pyc"):
            # tech#67: a .pyc is an import-side bytecode cache, never
            # evidence - regenerated caches re-trip this guard forever.
            msg += (" [pyc bytecode cache: delete it and set "
                    "PYTHONDONTWRITEBYTECODE=1 when importing .c3-tmp "
                    "middleware - tech#67]")
        findings.append(("WARN", "round-debris", msg))


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


def _git_log_subjects(root, n=GIT_LOG_SCAN_N, _run=None):
    """`git log -N --format=<sha>TAB<subject>` -> [(sha, subject)]
    newest-first; [] on any git failure (not a work tree, git missing,
    timeout) - advisory face, never breaks the probe. _run is the
    injection seam for tests (subprocess.run signature)."""
    if _run is None:
        _run = subprocess.run
    try:
        p = _run(["git", "log", "-%d" % n, "--format=%h%x09%s"],
                 cwd=str(root), capture_output=True, timeout=GIT_TIMEOUT_S)
    except (OSError, subprocess.TimeoutExpired):
        return []
    if p.returncode != 0:
        return []
    rows = []
    for line in p.stdout.decode("utf-8", "replace").splitlines():
        if "\t" not in line:
            continue
        sha, subject = line.split("\t", 1)
        rows.append((sha.strip(), subject.strip()))
    return rows


def classify_unaccounted_round_work(subjects, tick):
    """[(sha, subject)] + tick -> findings (pure core). Only a subject
    head-anchored R<N> counts as loop-round work (house commit
    convention: the close/export/receipt commits all open with the
    round anchor); any anchored round > tick is work committed whose
    accounting never ran. One WARN per distinct round number with the
    anchored shas shown (the R2214 anchor trail was three commits of
    one round). Non-int tick yields nothing (state faces own that)."""
    if not isinstance(tick, int) or isinstance(tick, bool):
        return []
    by_round = {}
    for sha, subject in subjects:
        if not isinstance(subject, str):
            continue
        m = COMMIT_ROUND_RE.match(subject)
        if not m:
            continue  # other-window commit (MV sprint / interactive session)
        r = int(m.group(1))
        if r > tick:
            by_round.setdefault(r, []).append(sha)
    findings = []
    for r in sorted(by_round):
        shas = by_round[r]
        shown = ", ".join(shas[:4]) + (" ..." if len(shas) > 4 else "")
        findings.append(("WARN", "unaccounted-round-work",
                         "round R%d work committed (%s) but state tick=%d - a "
                         "body landed round commits whose accounting never ran "
                         "(R2214 anchor: delivery+export+fire-receipt commits "
                         "landed, finalize_state never called, successor found "
                         "the gap by manual git-log archaeology) - absorb the "
                         "accounting under the round number" % (r, shown, tick)))
    return findings


def check_unaccounted_round_work(root, state, findings):
    """tech#155 guard face: name committed-but-unaccounted round work.
    Enforced every round by the routine probe consumption - the R2214
    shape is named within one round instead of by successor
    archaeology. A non-git tree or any git failure stays silent
    (advisory face, never breaks the probe)."""
    tick = state.get("tick") if isinstance(state, dict) else None
    if not isinstance(tick, int) or isinstance(tick, bool):
        return  # parse_state already FAILed the ledger
    findings.extend(classify_unaccounted_round_work(
        _git_log_subjects(root), tick))


def _export_cell_preview(entry):
    """Compact shape description of a bad list entry for WARN text."""
    if isinstance(entry, str):
        return "bare string %r" % (entry[:24],)
    if isinstance(entry, list):
        kinds = ",".join(type(c).__name__ for c in entry)
        return "%d-cell [%s]" % (len(entry), kinds)
    return type(entry).__name__


def _export_out_cell_ok(entry):
    """[txt<=64, on|wait|off, tag<=24] triple per the v6.2 contract."""
    if not isinstance(entry, list) or len(entry) != 3:
        return False
    txt, state, tag = entry
    if not isinstance(txt, str) or not isinstance(tag, str):
        return False
    return (len(txt) <= EXPORT_OUT_TXT_MAX
            and state in EXPORT_OUT_STATES
            and len(tag) <= EXPORT_OUT_TAG_MAX)


def _export_result_cell_ok(entry):
    """[v<=16, k<=14] short value/key pair per the v6.2 contract."""
    if not isinstance(entry, list) or len(entry) != 2:
        return False
    v, k = entry
    if isinstance(v, bool) or not isinstance(v, (str, int)):
        return False
    if not isinstance(k, str):
        return False
    return len(str(v)) <= EXPORT_RES_V_MAX and len(k) <= EXPORT_RES_K_MAX


def _export_chip_cell_ok(entry):
    """[txt<=14, live|wip] pair per the v6.2 contract (tech#71). The
    shaper drops cells whose txt is missing/shorter than 2 and silently
    renames any other class to 'wip' - that silent rename is the
    invisible mislabel this guard must name."""
    if not isinstance(entry, list) or len(entry) != 2:
        return False
    txt, cls = entry
    if not isinstance(txt, str) or not isinstance(cls, str):
        return False
    return (EXPORT_CELL_MIN_TXT <= len(txt) <= EXPORT_CHIP_TXT_MAX
            and cls in EXPORT_CHIP_CLASSES)


def _export_dept_cell_ok(entry):
    """{n<=24, t<=96, s in 0|1|2} object per the v6.2 contract
    (tech#71). The shaper drops entries whose n/t is missing or
    shorter than 2, truncates over-cap text, and silently defaults a
    missing (or off-enum) s to 1 - parity means naming every shape the
    consumer would drop, truncate or silently relabel."""
    if not isinstance(entry, dict):
        return False
    n, t = entry.get("n"), entry.get("t")
    if not isinstance(n, str) or not isinstance(t, str):
        return False
    if not EXPORT_CELL_MIN_TXT <= len(n) <= EXPORT_DEPT_N_MAX:
        return False
    if not EXPORT_CELL_MIN_TXT <= len(t) <= EXPORT_DEPT_T_MAX:
        return False
    s = entry.get("s", 1)
    if isinstance(s, bool) or not isinstance(s, int):
        return False
    return s in EXPORT_DEPT_STATES


def _export_ts_face(ts, now=None, mtime=None):
    """tech#69: export_ts sanity faces (pure core). The R1901 anchor:
    the refresh script stamped 19:05:00 into a file written at
    18:49:42 - an estimated value, not the live clock (the same
    round's state.ts was 18:58:00, so the value came from neither
    the state face nor the writer's clock). A ts ahead of the file's
    own write time is future stamping detectable at any later probe;
    a ts far behind the write time means the writer copied a stale
    value; a ts older than the 24h refresh law is a stale export.
    A missing/malformed export_ts breaks the P-61 required field and
    the freshness face alike. One WARN per face family, advisor
    grade - never a probe-break FAIL. now/mtime None (pure calls)
    skip the clock comparisons, keeping the legacy call shape silent
    on a well-formed ts."""
    if not isinstance(ts, str) or not STATE_TS_RE.match(ts.strip()):
        return [("WARN", "export-ts",
                 "export_ts missing/malformed (want YYYY-MM-DD "
                 "HH:MM:SS written from the live clock - P-61 "
                 "required field): %r" % (ts,))]
    try:
        ts_dt = datetime.strptime(ts.strip(), "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return [("WARN", "export-ts",
                 "export_ts unparseable: %r" % (ts,))]
    future, stale = [], []
    if mtime is not None:
        lag = (ts_dt - mtime).total_seconds() / 60.0
        if lag > EXPORT_TS_FUTURE_TOL_MIN:
            future.append("%.0f min ahead of the file's own write "
                          "time (R1901 anchor: 19:05:00 stamped at "
                          "18:49:42)" % lag)
        elif lag < -EXPORT_TS_STALE_COPY_MIN:
            stale.append("%.0f min behind the file's write time - "
                         "the writer copied a stale value instead "
                         "of the live clock" % (-lag))
    if now is not None:
        ahead = (ts_dt - now).total_seconds() / 60.0
        if ahead > EXPORT_TS_FUTURE_TOL_MIN:
            future.append("%.0f min ahead of the probe clock" % ahead)
        elif -ahead > EXPORT_TS_MAX_AGE_MIN:
            stale.append("%.1f h old - beyond the P-61 <=24h refresh "
                         "law" % (-ahead / 60.0))
    findings = []
    if future:
        findings.append(("WARN", "export-ts-future",
                         "export_ts %s - future stamping; write the "
                         "live clock at refresh time, not an estimate"
                         % "; ".join(future)))
    if stale:
        findings.append(("WARN", "export-ts-stale",
                         "export_ts %s - refresh the export" %
                         "; ".join(stale)))
    return findings


def classify_export_face(data, parse_err="", now=None, mtime=None):
    """(parsed-export-or-None, parse_err, now, mtime) -> findings
    (pure core). The R1901 anchor form: the export drifted for ~1700
    rounds because the consuming shaper falls back to the curated face
    on every bad field, so no alarm fired anywhere. Faces named here,
    one WARN per face: "do" over the one-line budget (product-priority
    law section 5), depts entries that are not well-formed {n<=24,
    t<=96, s in 0|1|2} objects, outs entries that are not well-formed
    3-cell [txt, on|wait|off, tag] arrays, chips entries that are not
    [txt<=14, live|wip] pairs (tech#71 parity facets - the shaper
    drops/truncates/relabels those silently), results entries that are
    not [v<=16, k<=14] short value/key pairs, any of the three lists
    over its entry cap, and the tech#69 export_ts faces (future stamp /
    stale copy / 24h staleness / malformed - see _export_ts_face). A
    parse failure or non-object top level is one WARN (the shaper
    falls back wholesale). None without an error (missing export) is
    silent - the export freshness step owns that disease. Clean
    exports yield no findings (silent PASS like the other guard
    faces)."""
    if parse_err:
        return [("WARN", "export-contract",
                 "status-export.json unparseable (%.60s) - the v6.2 "
                 "shaper falls back to the curated face wholesale, the "
                 "board goes stale with zero alarm - fix the writer"
                 % parse_err)]
    if data is None:
        return []
    if not isinstance(data, dict):
        return [("WARN", "export-contract",
                 "status-export.json top level is %s, want an object - "
                 "the shaper falls back wholesale; fix the writer"
                 % type(data).__name__)]
    findings = []
    do = data.get("do")
    if not isinstance(do, str) or len(do) > EXPORT_DO_MAX_CHARS:
        findings.append(("WARN", "export-do",
                         '"do" is %s (want a one-line string <= %d '
                         "chars, product-priority law section 5) - the "
                         "shaper truncates or drops it; write the "
                         "current activity as ONE line"
                         % (("%d chars" % len(do)) if isinstance(do, str)
                            else "not a string", EXPORT_DO_MAX_CHARS)))
    depts = data.get("depts")
    if isinstance(depts, list):
        bad = [e for e in depts if not _export_dept_cell_ok(e)]
        if bad:
            findings.append(("WARN", "export-depts",
                             "%d/%d depts entries are not well-formed "
                             "{n<=24, t<=96, s in 0|1|2} objects (first: "
                             "%s) - the v6.2 shaper drops every bad "
                             "entry and falls back to the curated face "
                             "when none survive, silently defaults a "
                             "missing/off-enum s to 1; the CEO board "
                             "goes stale dept by dept (tech#71 parity "
                             "gap: depts was unchecked); write depts as "
                             "{n, t, s} objects"
                             % (len(bad), len(depts),
                                _export_cell_preview(bad[0]))))
    outs = data.get("outs")
    if isinstance(outs, list):
        bad = [e for e in outs if not _export_out_cell_ok(e)]
        if bad:
            findings.append(("WARN", "export-outs",
                             "%d/%d outs entries are not well-formed "
                             "3-cell [txt<=64, on|wait|off, tag<=24] "
                             "arrays (first: %s) - the v6.2 shaper drops "
                             "every bad entry to the curated fallback, "
                             "the CEO board goes stale entry by entry "
                             "(R1901 anchor: 39/39 bare strings); write "
                             "outs as 3-cell arrays"
                             % (len(bad), len(outs),
                                _export_cell_preview(bad[0]))))
    chips = data.get("chips")
    if isinstance(chips, list):
        bad = [e for e in chips if not _export_chip_cell_ok(e)]
        if bad:
            findings.append(("WARN", "export-chips",
                             "%d/%d chips entries are not [txt<=14, "
                             "live|wip] pairs (first: %s) - the v6.2 "
                             "shaper drops every bad entry, silently "
                             "renames any other class to 'wip' and "
                             "falls back to the curated face when none "
                             "survive; the CEO board goes stale chip by "
                             "chip (tech#71 parity gap: chips had only "
                             "the entry cap); write chips as [txt, "
                             "live|wip] pairs"
                             % (len(bad), len(chips),
                                _export_cell_preview(bad[0]))))
    results = data.get("results")
    if isinstance(results, list):
        bad = [e for e in results if not _export_result_cell_ok(e)]
        if bad:
            findings.append(("WARN", "export-results",
                             "%d/%d results entries are not [v<=16, "
                             "k<=14] short value/key pairs (first: %s) - "
                             "the R1901 anchor form [tick, full log "
                             "line] made the CEO board render raw log "
                             "lines; keep results as short readouts"
                             % (len(bad), len(results),
                                _export_cell_preview(bad[0]))))
    over = []
    for key, cap in (("outs", EXPORT_OUT_MAX_N),
                     ("chips", EXPORT_CHIP_MAX_N),
                     ("results", EXPORT_RES_MAX_N)):
        entries = data.get(key)
        if isinstance(entries, list) and len(entries) > cap:
            over.append("%s %d>%d" % (key, len(entries), cap))
    if over:
        findings.append(("WARN", "export-caps",
                         "%d list(s) over the v6.2 entry caps: %s - the "
                         "shaper truncates silently; trim to the caps"
                         % (len(over), ", ".join(over))))
    findings.extend(_export_ts_face(data.get("export_ts"), now, mtime))
    return findings


def check_export_face(root, findings):
    """tech#68/#69/#71 guard face: parse docs/status-export.json and
    name the v6.2 contract violations (do budget / depts cells / outs
    cells / chips cells / results cells / entry caps) plus the export_ts
    faces (future stamp vs the file's own mtime, stale copy, 24h
    refresh law, malformed). Enforced every round by the routine probe
    consumption - export drift is named within one round instead of
    1700. A missing export file stays silent (the export refresh step
    owns that disease)."""
    path = root / EXPORT_REL
    if not path.is_file():
        return
    mtime = None
    try:
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
    except OSError:
        pass
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig",
                                         errors="replace"))
        err = ""
    except (OSError, ValueError) as e:
        data, err = None, str(e)
    findings.extend(classify_export_face(data, err, now=datetime.now(),
                                         mtime=mtime))


def cross_check(beats, state, done, now, max_age, max_gap, findings):
    """Protocol section 5 criteria -> findings appended in place."""
    adj_outages = load_outage_adjudicated(state)
    if beats:
        for i in range(1, len(beats)):
            gap = (beats[i][0] - beats[i - 1][0]).total_seconds() / 60.0
            pair = "%s -> %s" % (beats[i - 1][0].strftime("%Y-%m-%d %H:%M"),
                                 beats[i][0].strftime("%Y-%m-%d %H:%M"))
            if gap > max_age:
                key = (beats[i - 1][0].strftime("%Y-%m-%d"), int(round(gap)))
                if key in adj_outages:
                    # tech#241 (R2388): a documented historical window on
                    # the state outage_adjudicated ledger downgrades to a
                    # tagged WARN - visible on the full audit face, folded
                    # by the --loop date cutoff like other pre-cutoff
                    # history; unlisted windows keep failing.
                    findings.append(("WARN", "heartbeat-outage-adjudicated",
                                     "beat gap %.0f min (%s) over %d min lock "
                                     "age - adjudicated historical outage "
                                     "window (state outage_adjudicated, "
                                     "tech#241)" % (gap, pair, max_age)))
                else:
                    findings.append(("FAIL", "heartbeat-outage",
                                     "beat gap %.0f min (%s) exceeds lock age %d min "
                                     "- loop outage window" % (gap, pair, max_age)))
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
                if age > max_age:
                    findings.append(("WARN", "state-ts-stale",
                                     "state ts %.0f min old (> %d min) - closing "
                                     "step not refreshing ts" % (age, max_age)))
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
        check_c3tmp_stale(root, datetime.now(), findings)
        check_utf16_debris(root, findings)
        check_audio_tmp_residue(root, findings)
        check_broken_round_debris(root, state, findings)
        check_stale_dirty(root, datetime.now(), findings)
        check_orphan_deliverable(root, datetime.now(), findings)
        check_codex_freshness(root, datetime.now(), findings)
        check_codex_version_face(root, findings)
        check_canon_beat_policy_drift(root, findings)
        check_queue_glue(root, findings)
        check_queue_dup_numbers(root, findings)
        check_account_uncommitted(root, state, findings)
        check_unaccounted_round_work(root, state, findings)
        check_export_face(root, findings)
        check_aihot_stack(
            findings,
            ledger_path=root.joinpath(*AIHOT_WATCHDOG_LEDGER_REL))
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
        shown = []
        adj_supp = 0
        for f in findings:
            if f[0] == "WARN" and LOG_ORDER_ADJ_TAG in f[2]:
                adj_supp += 1
                continue
            if f[0] != "WARN" or warn_is_recent(f[2], cutoff):
                shown.append(f)
        supp = len(findings) - len(shown) - adj_supp
        shown = dense_fold(shown, fold_dense)
    else:
        shown, supp, adj_supp = findings, 0, 0
    for sev, code, msg in shown:
        print("- [%s] %s: %s" % (sev, code, msg))
    if supp:
        print("- [INFO] suppressed: %d historical WARN with no date on/after "
              "%s (--loop face; run without --loop for the full audit output)"
              % (supp, cutoff))
    if adj_supp:
        print("- [INFO] suppressed-adjudicated: %d log-order WARN pair(s) "
              "carried on the state log_order_adjudicated ledger (tech#215; "
              "run without --loop for the full audit output)" % adj_supp)
    fails = sum(1 for s, _, _ in findings if s == "FAIL")
    warns = sum(1 for s, _, _ in findings if s == "WARN")
    verdict = "FAIL" if fails else ("WARN" if warns else "PASS")
    print("loop health: %s (%d fail, %d warn)" % (verdict, fails, warns))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
