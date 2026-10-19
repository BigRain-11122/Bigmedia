# -*- coding: utf-8 -*-
"""Embedded accounting-close commit helper (tech#65, R1899).

R1897 kill-window form: the round body died after the close script had written
state.json / export / evidence middleware to disk but before ANY commit ran -
both two-segment commits were lost and the next round had to absorb the whole
accounting face. tech#27's two-segment protection assumes the body lives to
its commit step; R1897 showed the hole below that assumption.

This module shrinks the accounting segment's kill window from
"close script finished -> body commit finished" (many body tool-call
round-trips; the R1897 real case) to inside the close script itself: the
close script calls run_close_commit(files, message) as its LAST step, so a
body that got as far as launching the close script gets its accounting
committed (script-internal window only).

Laws encoded (why this is safe in this shared tree):
- Explicit-file law: only the paths passed via ``files`` are ever touched.
  Never ``git add -A`` / ``git add .`` - this working tree shares the MV
  sprint session's in-flight files.
- Pathspec-commit law (2026-10-09 staged-sweep incident): the commit step is
  ``git commit -m <msg> -- <files>``, which takes the WORKING-TREE state of
  ONLY the listed paths; another session's staged files stay in the index
  untouched. Listed untracked files are staged first with an explicit
  ``git add -- <files>`` (also touches only the listed paths).
- ASCII commit-message law (encoding rule): a non-ASCII message is a loud
  usage error before any git call, not a silent GBK hazard.
- Push failure is warn-only (mandate self-heal law: record, do not fix; the
  next round's origin_gap_check surfaces ahead=N).
- A listed file missing on disk is a loud usage error BEFORE any git call:
  prevents silent partial accounting commits (close scripts write files,
  never delete them, so missing = the close step itself failed).
- Message length >500 chars gets a WARN line only - an accounting close must
  never fail on a soft style bound (P-30 limit is one line <=500).
- tech#67 (.c3-tmp __pycache__ governance, R1900 anchor): every close purges
  ``.c3-tmp/**/__pycache__`` dirs. Import-side bytecode caches are never
  evidence (.gitignore already excludes *.pyc), and a regenerated cache
  would trip the round-debris guard forever (round anchor N outside
  [tick, tick+1] is always-true for a compiled artifact). Scope law: only
  the .c3-tmp subtree - caches elsewhere (src/, tests/) stay untouched.
- tech#81 (r1930 anchor) self-inclusion law: the round's own close script
  ``.c3-tmp/r{tick}_close.py`` rides the manifest automatically. The
  r1930_close.py leftover happened because the explicit manifest never
  contained the script that consumed it - a structural gap healed here,
  not by every future script remembering its own path. Advisory by
  design: an unreadable state or a missing script never fails the close.
- tech#188 (R2316 anchor) F-registration backwrite guard: a close whose
  manifest carries the finished ledger (output/finished.md) without the
  main queue (state/queue/main.md) emits a loud WARN - R2258 registered
  F-180 but forgot main#19's done mark, which then sat unwritten for 57
  rounds until tech#185's forensic pass surfaced it. Advisory only: the
  mark may legitimately live in an earlier commit, so this never fails
  an accounting close; it just makes the forget-shape loud at the one
  place that sees the whole manifest.
- tech#257 (R2398 anchor) F-registration renders birth gate: a close
  that writes the finished ledger runs the readiness render-unannot
  semantics over output/renders at close time and WARNs on unannotated
  media - R2398's single-round fast chain registered F-199 without the
  renders README row and the probe only caught it one round later
  (R2399 backfill). Content-level by design (audio/novel/comic-line F
  items legitimately carry no renders face), fail-open by design.
- tech#214 (R2351 anchor) narrative ts order advisory: finalize_state
  compares the new ledger line's fuzzy-minute prefix against the last
  on-disk line and WARNs into the close evidence face when it goes
  backwards (R2349 wrote 09:5x, R2350 wrote 09:2x - the round number
  advanced while the narrative clock went backwards, and the probe only
  surfaced it one cycle later). Advisory only, same WARN grade the
  probe gives; the comparison semantics are loop_health's own
  (single-semantics house law), so writer and probe can never disagree.
- tech#233 (R2375 anchor) UTF-16 debris close-time self-heal: the close
  transcodes root-level .c3-tmp files carrying a UTF-16 BOM into UTF-8
  in place, before the git steps. Third PS 5.1 ``>`` occurrence
  (R2331/R2355x2/R2375); the escalation is self-healing, not refusal -
  a hard close refusal would trade disposable middleware for
  accounting-tick holes (the strictly worse failure class), while the
  in-place rewrite makes the debris class unable to survive ANY round
  close. Scope mirrors the probe face (loop_health check_utf16_debris
  root-level scope); the pinned BOM heads are alias-locked to the probe
  constants by test.

rc: 0 = commit landed (push may have warned); 1 = a git add/commit step
failed; 2 = usage error; 3 = readback verify failed (tech#155 face 2:
expect_tick passed and the on-disk ledger does not carry it - the commit
stays landed, the next body absorbs the accounting). Output lines are plain ASCII text, safe for
evidence capture files.

CLI:
    python src/os/close_commit.py --files A B C --message "..."
        [--root PATH] [--no-push] [--dry-run]

PT-20261015-01 (R2308 anchor) adds pulse_state_beat(): the pulse-only
half of the heartbeat face. The inspection finding (group orders row 456,
RUN_ID=20261015-203247): the cloud-cap spawn gate (C-20261015-03) defers
every 10-min spawn while live codely.exe >= 2 - the 2026-10-15 defer
window ran 18:26->20:38 with zero round closes, so the fleet-audit ts
face read STALE 2.2h while the loop was alive and retrying every slot.
The spawner (holding round.lock - no round body can be closing
concurrently) pulses ts + marker through such windows with ZERO
accounting touch; the accounting face keeps exactly one writer
(finalize_state, tech#149 unchanged). CLI mode: --pulse REASON.

tech#76 (R1920 placeholder anchor) adds finalize_state(): the single-writer
state.json accounting step. Import-only by design (no CLI): the ledger line
is CJK prose, and CLI args are exactly the shell-quoting/GBK pit surface -
close scripts pass it as an in-script UTF-8 string literal instead.

tech#148 (R2124 relapse anchor) adds the canonical-export integration: a
close that passes export_patch/export_do refreshes docs/status-export.json
THROUGH export_refresh (tech#70 canonical writer) before the git steps, and
the refreshed export rides the commit manifest automatically. This is the
structural retirement of the hand-rolled json.dump close-script generation
(R2124 wrote a 5-entry results face the writer would have refused; R2125
re-fixed the instance, this encodes the class). Writer refusal (rc=2) is
warn-only at the close level: the export stays byte-identical (the safe
state) and the accounting commit still lands - the routine probe keeps
flagging the stale face until a clean patch is passed.
"""

import argparse
import datetime
import io
import json
import os
import re
import shutil
import subprocess
import sys

RC_OK = 0
RC_GIT = 1
RC_USAGE = 2
# tech#155 face 2 (R2214 anchor): post-close readback verify failure.
# Only reachable when the caller passes expect_tick (zero change on the
# legacy surface); the commit itself stays landed - it is real work.
RC_VERIFY = 3

# export_refresh.RC_REFUSE (the canonical writer's refusal grade). The
# sibling module is lazy-imported inside refresh_export_in_close, so the
# value is pinned here; test_close_commit locks the alias to the writer's
# own constant so drift is caught.
RC_WRITER_REFUSE = 2

MSG_MAX_SOFT = 500  # P-30 one-line convention; WARN only, never fails
PYCACHE_DIRNAME = "__pycache__"

# tech#233 (R2375 anchor): UTF-16 BOM heads for the close-time debris
# self-heal. Pinned here (same precedent as RC_WRITER_REFUSE);
# test_close_commit locks the alias to loop_health.UTF16_BOM_HEADS so the
# close face and the probe face can never drift.
UTF16_BOM_HEADS = (b"\xff\xfe", b"\xfe\xff")

# tech#188 (R2316 anchor): F-registration backwrite guard paths. A close
# that registers a new F-number in the finished ledger must also carry the
# main-queue done backwrite - R2258 missed state/queue/main.md and the
# main#19 done mark stayed unwritten for 57 rounds.
# tech#209 (R2342 anchor): station-reviews joins the guard surface -
# F-192/F-193 registered without the station-reviews row and the ledger
# tail lagged two rounds (REACT-v22/DIGEST-v23) until R2342 backfilled.
FINISHED_LEDGER_REL = "output/finished.md"
QUEUE_MAIN_REL = "state/queue/main.md"
STATION_REVIEWS_REL = "docs/reviews/station-reviews.md"
# main#139 (R2373 anchor): F-192/F-196/F-197 carried closing-position
# anchors registered without the residents appearance-ledger row; the
# misses lagged to the R2373 backfill batch.
RESIDENTS_LEDGER_REL = "data/storylines/codex/city-residents.md"
# tech#257 (R2398 anchor): renders-face paths for the F-registration
# birth gate. Content-level input, not a manifest trigger: audio-line
# F items keep their own ledger (data/storylines/audio/README.md) and
# legitimately never touch the renders face, so the ledger's absence
# from a manifest is NOT evidence - unannotated media is.
RENDERS_DIR_REL = "output/renders"
RENDERS_LEDGER_REL = "output/renders/README.md"

# tech#76: ledger prefix shape. Minute field is two chars - digit+digit
# ("23:26") or digit+x ("23:5x", fuzzy-minute house style). Anything else
# raises before the ledger is touched (born-level gate).
LOG_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{1}[0-9x] R(\d+): ")
TASK_MAX_CHARS = 60  # mandate: task = log line minus prefix, first 60 chars
TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")

# tech#214 (R2351 anchor): the fuzzy-minute prefix ts shape for the
# write-time ordering advisory - the same capture loop_health's LOG_TS_RE
# reads, so the writer and the probe share one comparison semantics
# (plain string compare; the fuzzy char "x" sorts after digits).
LOG_TS_PREFIX_RE = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d[0-9x])")

# tech#211 (R2346 anchor): "F-NNN 登记" claim shape in a log line. The
# claim verb must sit right after the number (spaces allowed); other
# mentions ("F-196·登记轮核验", "F-195 归档") are references, not claims,
# and stay out of the advisory's trigger face.
F_CLAIM_RE = re.compile(r"F-(\d{1,4})\s*登记")


def message_is_ascii(message):
    """True when every char in the message is ASCII (encoding rule)."""
    try:
        message.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False


def resolve_files(root, files):
    """Validate the explicit file list against root.

    Returns a list of repo-relative forward-slash paths (git pathspec form).
    Raises ValueError on: empty list, non-string entries, missing files, or
    paths that escape the repo root (explicit-list law: everything must live
    inside the repo the close is committing to).
    """
    if not files:
        raise ValueError("files list is empty - refusing to commit anything")
    root = os.path.abspath(root)
    rel = []
    for f in files:
        if not isinstance(f, str) or not f.strip():
            raise ValueError("bad file entry: %r" % (f,))
        abs_p = os.path.abspath(os.path.join(root, f))
        if not (abs_p == root or abs_p.startswith(root + os.sep)):
            raise ValueError("path escapes repo root: %r" % (f,))
        if not os.path.isfile(abs_p):
            raise ValueError("missing file (close step must write it first): %r" % (f,))
        rel.append(abs_p[len(root) + 1:].replace(os.sep, "/"))
    # de-dup, keep order (a file listed twice would only confuse the report)
    seen = set()
    out = []
    for p in rel:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def _git(root, args):
    """Run a git command under root; returns (rc, stdout, stderr) as text.

    Byte capture + utf-8/replace manual decode (never text=True: this is a
    zh-CN host, text=True decodes child output as GBK and crashes the reader
    thread - 2026-10-08 in-case pitfall).
    """
    proc = subprocess.run(["git"] + list(args), cwd=root,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = proc.stdout.decode("utf-8", "replace").strip()
    err = proc.stderr.decode("utf-8", "replace").strip()
    return proc.returncode, out, err


def purge_c3tmp_pycache(root, dry=False):
    """Remove every ``__pycache__`` dir under ``<root>/.c3-tmp`` (tech#67).

    Import-side bytecode caches are never evidence middleware; left in
    place, a regenerated pyc trips the round-debris guard forever (its
    round anchor sits outside [tick, tick+1] by construction). Scope law:
    ONLY the .c3-tmp subtree - caches under src/, tests/ or anywhere else
    are never touched. dry=True counts without deleting (zero side
    effects). Returns (purged_dir_count, failed_paths) and never raises:
    a cleanup step must not fail an accounting close.
    """
    base = os.path.join(root, ".c3-tmp")
    purged, failed = 0, []
    if not os.path.isdir(base):
        return 0, []
    for dirpath, dirnames, _filenames in os.walk(base):
        if PYCACHE_DIRNAME in dirnames:
            target = os.path.join(dirpath, PYCACHE_DIRNAME)
            if dry:
                purged += 1
                continue
            try:
                shutil.rmtree(target)
                purged += 1
            except OSError:
                failed.append(target)
            # do not descend into the removed/skipped cache dir
            dirnames[:] = [d for d in dirnames if d != PYCACHE_DIRNAME]
    return purged, failed


def transcode_c3tmp_utf16(root, dry=False):
    """tech#233 (R2375 anchor): self-heal UTF-16 debris at close time.

    The three-occurrence family (R2331 / R2355 x2 / R2375): a body points
    PS 5.1 ``>`` at native tool output, the redirect lands a UTF-16 BOM
    file in .c3-tmp, and the debris survives the round boundary until the
    next round's probe names it (loop_health utf16-debris WARN) and a
    successor hand-transcodes or deletes it. CEO escalation law
    (recurrence = gate escalation) asks for the script-assertion level;
    the assertion here is self-healing rather than refusing: a hard close
    refusal would trade disposable middleware for accounting-tick holes
    (the strictly worse failure class), while an in-place lossless
    UTF-16 -> UTF-8 rewrite makes the debris class structurally unable to
    survive ANY round close.

    Scope law: root-level files of <root>/.c3-tmp only, mirroring
    loop_health's check_utf16_debris face. BOM heads are the pinned
    module constants (alias-locked to the probe's own by test). dry=True
    counts without writing. Returns (transcoded_names, failed_names) and
    never raises: a cleanup step must not fail an accounting close. A
    BOM file that fails to decode is left byte-identical and reported in
    failed_names (fail-soft; the probe keeps it visible next round).
    """
    base = os.path.join(root, ".c3-tmp")
    transcoded, failed = [], []
    if not os.path.isdir(base):
        return transcoded, failed
    try:
        names = sorted(os.listdir(base))
    except OSError:
        return transcoded, failed
    for name in names:
        path = os.path.join(base, name)
        try:
            if not os.path.isfile(path):
                continue
            with open(path, "rb") as f:
                head = f.read(2)
            if not head.startswith(UTF16_BOM_HEADS):
                continue
            if dry:
                transcoded.append(name)
                continue
            with open(path, "rb") as f:
                raw = f.read()
            text = raw.decode("utf-16")  # the BOM picks the endianness
            tmp = path + ".tmp_utf16"
            with io.open(tmp, "w", encoding="utf-8", newline="") as f:
                f.write(text)
            os.replace(tmp, path)
            transcoded.append(name)
        except (OSError, ValueError, UnicodeError):
            failed.append(name)
    return transcoded, failed


def derive_task(log_line):
    """Validate the ledger prefix and derive the state ``task`` field.

    mandate rule (PT-20260925-02): task = this round's log line minus the
    "YYYY-MM-DD HH:MMx RNNNN: " prefix, first 60 chars. The prefix length
    was previously hand-computed per close script (fragile); this is the
    single tested implementation.

    Raises ValueError when the line does not match the ledger prefix
    shape - the born-level gate that keeps malformed lines out of the
    permanent ledger (and, per the R1920 anchor, out of anything that
    would silently half-substitute them).
    """
    m = LOG_PREFIX_RE.match(log_line)
    if not m:
        raise ValueError(
            "log_line does not match ledger prefix "
            "'YYYY-MM-DD HH:MMx RNNNN: ': %r" % (log_line[:40],))
    return log_line[m.end():][:TASK_MAX_CHARS]


def derive_round_number(log_line):
    """tech#196 (R2329 anchor): the round number from a ledger prefix.

    The R/tick arithmetic chain (R == the tick the finalize produces)
    held for the whole historical ledger until one body self-derived a
    wrong round number (R2334 while its real tick was 2328), which
    tripped loop_health's unaccounted-round-work WARN for a ~12-commit
    window. This helper is the born-gate input: finalize_state refuses
    any log line whose R number will not equal the new tick.

    Raises ValueError on a non-matching prefix (same shape gate as
    derive_task, single regex source).
    """
    m = LOG_PREFIX_RE.match(log_line)
    if not m:
        raise ValueError(
            "log_line does not match ledger prefix "
            "'YYYY-MM-DD HH:MMx RNNNN: ': %r" % (log_line[:40],))
    return int(m.group(1))


def f_claim_ledger_advisory(log_line, finished_path):
    """tech#211: F-claim vs finished-ledger presence check (advisory).

    R2346 anchor: that round's log line claimed "F-195 登记" while
    output/finished.md did not carry the row yet (it landed next
    round), so a premature claim read as done for a full round. This
    helper returns the claim numbers ("F-205") the finished ledger
    lacks. Best-effort by design: a missing or unreadable ledger yields
    an empty list - no evidence to check against, zero noise - and the
    caller only WARNs, never failing an accounting close.
    """
    if not finished_path or not os.path.isfile(finished_path):
        return []
    try:
        with io.open(finished_path, encoding="utf-8") as f:
            ledger = f.read()
    except (IOError, OSError):
        return []
    missing = []
    for m in F_CLAIM_RE.finditer(log_line or ""):
        fnum = "F-" + m.group(1)
        if fnum not in ledger and fnum not in missing:
            missing.append(fnum)
    return missing


def unannotated_render_media(root):
    """tech#257: unannotated renders-dir media names (birth gate input).

    Reuses readiness.parse_renders so the close-side birth gate and the
    readiness probe share one render-unannot semantics (single-semantics
    house law, tech#214 precedent) - they can never disagree. Best-effort
    by design: any import/IO failure returns an empty list (fail-open;
    readiness remains the standing general gate) - an accounting close
    never fails on this face. A missing renders dir also yields an empty
    list: no renders face, no gate (the audio/novel/comic-line shape).
    """
    try:
        from pathlib import Path  # lazy: parse_renders speaks pathlib
        src_dir = os.path.abspath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), ".."))
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)
        import readiness
        rows, _findings = readiness.parse_renders(
            Path(os.path.join(root, RENDERS_DIR_REL)),
            Path(os.path.join(root, RENDERS_LEDGER_REL)))
        return [name for name, status in rows if status is None]
    except Exception:
        return []


def log_prefix_backward_advisory(log_line, last_log_line):
    """tech#214: write-time narrative-order advisory (R2351 anchor).

    R2349's ledger line carried prefix "09:5x" and its successor R2350
    carried "09:2x" - the round number advanced but the narrative
    timestamp went backwards, and only the next loop_health run surfaced
    it (log-order WARN, one probe cycle late). This helper is the
    write-time twin: finalize_state compares the new line's prefix
    against the last on-disk line and a backwards shape gets its WARN
    into THIS round's close evidence face.

    Comparison semantics are the probe's own (single-semantics house
    law): plain string compare on the captured fuzzy-minute prefix
    "YYYY-MM-DD HH:MM" where the minute's last char may be "x" (the
    approximate-minute house style). Advisory only - never fails an
    accounting close (narrative hygiene, the same WARN grade the probe
    gives).

    Returns (backward, new_pfx, last_pfx). backward=False with empty
    stamps when either line lacks the prefix shape (zero noise: the
    born-level gate already refuses malformed NEW lines, and malformed
    history is the probe's business, not the writer's).
    """
    m_new = LOG_TS_PREFIX_RE.match(log_line or "")
    if not m_new:
        return False, "", ""
    last = last_log_line if isinstance(last_log_line, str) else ""
    m_last = LOG_TS_PREFIX_RE.match(last)
    if not m_last:
        return False, m_new.group(1), ""
    backward = m_new.group(1) < m_last.group(1)
    return backward, m_new.group(1), m_last.group(1)


def finalize_state(log_line, ts=None, focus=None, tick=None,
                   watermark_add=None, orders_watermark=None, state_path=None,
                   now=None, finished_ledger_path=None, orders_wm_scanned=None):
    """Single-writer state.json accounting step (tech#76, R1920 anchor).

    R1920 root cause: that round's log line lived in an external template
    data file with a placeholder token; the close script substituted
    "@TS@" while the template spelled "@TS" - the replace silently missed
    AND the completeness assert checked the wrong token. Double error,
    one root: the placeholder token had no single source of truth.

    Authoring law encoded here: the caller passes ``log_line`` as an
    in-script UTF-8 Python string literal. This writer performs NO
    substitution step at all, so the placeholder failure class is
    structurally impossible - what you pass lands in the ledger verbatim
    (and lengths echo in the ASCII summary). External template files with
    placeholder tokens are banned for the state accounting step.

    Steps: validate log prefix shape -> derive task (60-char law) ->
    resolve ts (explicit or injected clock, second-precision ASCII) ->
    load state -> tick guard (explicit tick must equal on-disk tick+1;
    default = auto-increment) -> round-number guard (the prefix R number
    must equal the new tick, tech#196 R2329 anchor) -> append log line -> stamp ts/task ->
    optional focus overwrite -> optional decisions_watermark.dnums append
    (dedup, order-preserving)     -> optional orders_row_watermark overwrite
    (tech#103 consumption anchor) -> beat policy block sync-on-diff
    (tech#220 self-heal) -> atomic write (temp + os.replace,
    indent=1, UTF-8, no BOM - the on-disk house format).

    Args:
        log_line: full ledger line, e.g. "2026-10-11 00:1x R1927: ..."
            (verbatim; no placeholders exist in this API).
        ts: "YYYY-MM-DD HH:MM:SS" (second-precision ASCII); default=now.
        focus: optional next-round focus string; None = leave untouched.
        tick: optional expected new tick (double-run guard: on-disk tick
            must equal tick-1); None = auto-increment from on-disk tick.
        watermark_add: optional iterable of decision/council ids appended
            to decisions_watermark.dnums (dedup, order-preserving).
        orders_watermark: optional {"rows": int >= 1, "tail_key": non-empty
            str} stored verbatim at state.json orders_row_watermark after
            the body consumes the new HQ orders rows (tech#103
            consumption anchor). MUST be the round's ORDERS-face measured
            boundary from the round-START group_scan run (the "current:
            rows=N | tail_key=..." line), NOT the close-time mechanical
            group_scan.current_orders_watermark() value: FleetLink can
            heal rows into the worktree mid-round, and a close-time read
            absorbs rows this round never scanned - the next round's
            ORDERS-NEW diff then goes permanently blind on them (tech#251,
            R2393 anchor: rows 616-617 escaped every scan face and were
            recovered only by manual log-vs-state comparison). Rows
            consumed origin-only via git show legitimately leave the
            worktree anchor BELOW the file (R2292 precedent) - that
            direction is always legal.
        orders_wm_scanned: optional {"rows": int >= 1, "tail_key":
            non-empty str} guard input = the round-start ORDERS-face
            boundary actually scanned this round (tech#251). When both
            are given and orders_watermark["rows"] >
            orders_wm_scanned["rows"] the write FAILS CLOSED (a watermark
            above the scanned boundary would absorb never-scanned rows);
            passing orders_watermark without orders_wm_scanned emits a
            non-blocking ORDERS-WM-GUARD advisory (cannot verify).
        state_path: default = state.json next to this module.
        now: injectable clock (needs strftime) for tests.
        finished_ledger_path: default = output/finished.md derived from
            state_path's repo root; tech#211 advisory input (see
            f_claim_ledger_advisory), never affects the write itself.

    Returns: summary dict {tick, ts, task, wm_added, orders_wm_rows,
    log_len, f_claims_missing, prefix_backward, orders_wm_guard}
    (orders_wm_rows None when no orders watermark was given;
    orders_wm_guard = "verified" / "unverified-no-scanned-boundary" /
    None per tech#251; f_claims_missing = tech#211
    advisory list, empty when every "F-NNN 登记" claim is present in the
    finished ledger or there was no ledger to check against;
    prefix_backward = tech#214 advisory flag, True when the new line's
    fuzzy-minute prefix sits behind the last on-disk line's;
    beat_written/beat_synced = tech#220 self-heal flags for the beat
    policy block: written = rebuilt from the constant (absent/broken
    block), synced = an existing block had policy keys healed in place).
    Raises: ValueError on any usage error - loud, zero partial writes
    (validation happens before the first disk mutation; the atomic
    replace makes the write itself all-or-nothing).
    """
    if state_path is None:
        state_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "state.json")
    if not isinstance(log_line, str) or not log_line.strip():
        raise ValueError("log_line must be a non-empty string literal")
    task = derive_task(log_line)  # raises on bad prefix shape
    if ts is None:
        clock = now if now is not None else datetime.datetime.now()
        ts = clock.strftime("%Y-%m-%d %H:%M:%S")
    elif not isinstance(ts, str) or not TS_RE.match(ts):
        raise ValueError("ts must match 'YYYY-MM-DD HH:MM:SS' (got %r)" % (ts,))
    if focus is not None and (not isinstance(focus, str) or not focus.strip()):
        raise ValueError("focus must be a non-empty string when given")

    with io.open(state_path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data.get("log"), list):
        raise ValueError("state.json 'log' is not a list - refusing to touch")

    cur = data.get("tick")
    if not isinstance(cur, int):
        raise ValueError("state.json tick is not an int: %r" % (cur,))
    if tick is None:
        new_tick = cur + 1
    else:
        if not isinstance(tick, int):
            raise ValueError("tick must be an int when given")
        if tick != cur + 1:
            raise ValueError(
                "tick guard: on-disk tick=%s, expected new tick=%s "
                "(double-run or concurrent writer?)" % (cur, tick))
        new_tick = tick

    # tech#196 born gate (R2329 anchor): R number must equal the new
    # tick, keeping the R==tick arithmetic chain true at write time -
    # a self-derived wrong round number is refused loudly instead of
    # landing in the ledger and tripping unaccounted-round-work later.
    round_num = derive_round_number(log_line)
    if round_num != new_tick:
        raise ValueError(
            "round-number invariant: log line carries R%d but the new "
            "tick is %d (on-disk tick=%d) - relabel the round number "
            "to R%d before writing (R2329 anchor: R==tick chain)"
            % (round_num, new_tick, cur, new_tick))

    # --- tech#211: premature F-claim advisory (R2346 anchor). A log
    # line may claim "F-NNN 登记" for a finished-ledger row that is not
    # on disk yet - the claim then reads as done for a full round while
    # the registration actually lands next round. Advisory only (WARN
    # printed into the close evidence face, never FAIL): the legitimate
    # mid-chain plan shape must keep closing. ---
    if finished_ledger_path is None:
        finished_ledger_path = os.path.join(
            os.path.dirname(os.path.abspath(state_path)),
            os.pardir, os.pardir, FINISHED_LEDGER_REL)
    f_claims_missing = f_claim_ledger_advisory(log_line, finished_ledger_path)
    for fnum in f_claims_missing:
        print("WARN F-CLAIM-NOT-IN-LEDGER %s claimed in log but %s "
              "lacks it (tech#211, R2346 anchor: premature claim - "
              "register next round or fix the line)" % (
                  fnum, FINISHED_LEDGER_REL))

    # --- tech#214: narrative ts order advisory (R2351 anchor). The new
    # line's fuzzy-minute prefix vs the last on-disk line's - a
    # backwards prefix gets its WARN in THIS round's close evidence
    # (the probe already grades the same shape WARN post-hoc; this is
    # the write-time twin, one cycle earlier). Advisory only: never
    # fails an accounting close. ---
    last_line = data["log"][-1] if data["log"] else None
    prefix_backward, new_pfx, last_pfx = log_prefix_backward_advisory(
        log_line, last_line)
    if prefix_backward:
        print("WARN LOG-PREFIX-BACKWARD %s after %s (tech#214, R2351 "
              "anchor: narrative prefix behind the last ledger line - "
              "fix the line's clock before it lands)" % (new_pfx, last_pfx))

    wm_added = 0
    if watermark_add is not None:
        wm = data.setdefault("decisions_watermark", {})
        if not isinstance(wm, dict):
            raise ValueError("decisions_watermark is not an object")
        dnums = wm.setdefault("dnums", [])
        if not isinstance(dnums, list):
            raise ValueError("decisions_watermark.dnums is not a list")
        for d in watermark_add:
            if not isinstance(d, str) or not d.strip():
                raise ValueError("watermark_add entries must be non-empty strings")
            if d not in dnums:
                dnums.append(d)
                wm_added += 1

    orders_wm_stored = None
    if orders_watermark is not None:
        if (not isinstance(orders_watermark, dict)
                or not isinstance(orders_watermark.get("rows"), int)
                or orders_watermark["rows"] < 1
                or not isinstance(orders_watermark.get("tail_key"), str)
                or not orders_watermark["tail_key"].strip()):
            raise ValueError(
                "orders_watermark must be {'rows': int >= 1, "
                "'tail_key': non-empty str} (got %r)" % (orders_watermark,))
        orders_wm_stored = {"rows": orders_watermark["rows"],
                            "tail_key": orders_watermark["tail_key"]}

    # tech#251 (R2394): heal-race absorption guard. The R2393 anchor:
    # finalize was passed current_orders_watermark() at close time, the
    # FleetLink pull had healed the worktree from 611 to 617 rows inside
    # the round window, the stored watermark jumped to 617, and rows
    # 616-617 (two CEO orders) escaped every scan face forever. A
    # watermark may never sit ABOVE the boundary the round actually
    # scanned; below is the R2292 origin-only consumption family and is
    # always legal (next round simply re-surfaces those rows as NEW -
    # the fail-safe direction).
    orders_wm_guard = None
    if orders_wm_scanned is not None:
        if (not isinstance(orders_wm_scanned, dict)
                or not isinstance(orders_wm_scanned.get("rows"), int)
                or orders_wm_scanned["rows"] < 1
                or not isinstance(orders_wm_scanned.get("tail_key"), str)
                or not orders_wm_scanned["tail_key"].strip()):
            raise ValueError(
                "orders_wm_scanned must be {'rows': int >= 1, "
                "'tail_key': non-empty str} (got %r)" % (orders_wm_scanned,))
        if orders_wm_stored is not None and \
                orders_wm_stored["rows"] > orders_wm_scanned["rows"]:
            raise ValueError(
                "orders_watermark rows=%d exceeds the round's scanned "
                "ORDERS-face boundary rows=%d (tech#251 heal-race "
                "guard): FleetLink healed rows into the worktree after "
                "the scan, and storing this watermark would absorb "
                "never-scanned rows permanently. Pass the round-START "
                "group_scan ORDERS-face boundary instead "
                "(tail_key=%r)." % (orders_wm_stored["rows"],
                                    orders_wm_scanned["rows"],
                                    orders_wm_scanned["tail_key"]))
        orders_wm_guard = "verified"
    elif orders_wm_stored is not None:
        orders_wm_guard = "unverified-no-scanned-boundary"
        print("ORDERS-WM-GUARD-WARN orders_watermark given without "
              "orders_wm_scanned - cannot verify heal-race absorption "
              "(tech#251); pass the round-start group_scan ORDERS-face "
              "boundary as orders_wm_scanned")

    data["tick"] = new_tick
    data["log"].append(log_line)
    data["ts"] = ts
    data["task"] = task
    if focus is not None:
        data["focus"] = focus
    if orders_wm_stored is not None:
        data["orders_row_watermark"] = orders_wm_stored

    # tech#220 (R2361): beat-block write-time self-heal - the same
    # sync-on-diff as pulse_state_beat, so a BEAT_POLICY bump in code
    # heals at the very next round close with no hand migration (the
    # R2359 violation class dies here). Same constant + idempotent =
    # no double-write conflict with the pulse wiring (which structurally
    # cannot interleave: the spawner pulses only while this round body
    # holds round.lock). Union merge - hand-tuned notes survive.
    beat_written, beat_synced = _sync_beat_policy(data)

    payload = json.dumps(data, ensure_ascii=False, indent=1)
    tmp = state_path + ".tmp_final"
    with io.open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(payload)
    os.replace(tmp, state_path)
    # ASCII-only evidence line (encoding law; task/ts contain CJK digits text)
    print("STATE-FINALIZED tick=%s ts=%s task_len=%d focus_set=%s "
          "wm_added=%d orders_wm_rows=%s log_len=%d beat_written=%s "
          "beat_synced=%s" % (
              new_tick, ts, len(task), focus is not None, wm_added,
              orders_wm_stored["rows"] if orders_wm_stored else "-",
              len(log_line), beat_written, beat_synced))
    return {"tick": new_tick, "ts": ts, "task": task,
            "wm_added": wm_added, "log_len": len(log_line),
            "f_claims_missing": f_claims_missing,
            "prefix_backward": prefix_backward,
            "beat_written": beat_written, "beat_synced": beat_synced,
            "orders_wm_rows": (orders_wm_stored["rows"]
                               if orders_wm_stored else None),
            "orders_wm_guard": orders_wm_guard}


# PT-20261015-01 option 2 declaration (beat policy block): written when
# absent, then policy-key synced to the code constant on every write
# face (tech#220 sync-on-diff). Declares the ts-face gap semantics so a
# remote fleet-audit can interpret a stale ts without a new inspection
# order, plus the D-13 machine-readable pointer (receipt channel + canon).
# tech#219 (R2360): thresholds synced to the v2 liveness budget so a
# rebuilt block matches the live state.json beat block migrated during
# the tech#217 absorb (35min retired semantics would drift the gap face).
# tech#220 (R2361): the write-once law retired - any future BEAT_POLICY
# bump heals the live block at the next pulse / round close, so the R2359
# hand-migration violation class is structurally impossible.
BEAT_POLICY = {
    "active_gap_max_min": 250,
    "active_semantics": "round schedule 10min + v2 liveness budget (tech#217, BM 945c3f60 port): 25min zero-output silence gate + 240min hard cap, kills on evidence only - a streaming long round is never wall-clock killed; ts refreshed at every round close (finalize_state)",
    "defer_semantics": "cloud-cap gate (C-20261015-03) defers spawns while live codely.exe >= 2; spawner pulses ts every 10min slot through defer windows (PT-20261015-01 option 1)",
    "pause_semantics": "CEO halt word / machine-state pause stops the loop task entirely; ts stale for the pause duration by design; liveness evidence = origin commits",
    "d13_pointer": "canon=docs/os-protocol.md s6; receipt=HQ-FEEDBACK PT-20261015-01 line + ack commit (orders row 456 + round + next action)",
}
PULSE_REASON_MAX = 80


def _sync_beat_policy(data):
    """tech#220 (R2361): beat-block write-time self-heal (sync-on-diff).

    R2359 anchor: the tech#217 semantics bump had to be hand-migrated
    into live state.json because the write-once law meant an existing
    block was never touched - a hand edit on the accounting face (state
    write-force-law violation) with zero regression gate on the gap
    face. The heal is a union merge: every BEAT_POLICY key is restored
    from the code constant (single source of truth), sub-keys outside
    BEAT_POLICY (hand-tuned notes) are preserved - a machine writer
    never silently deletes a human annotation. Idempotent by
    construction: an in-sync block is a no-op, so the pulse_state_beat
    and finalize_state wirings can never double-write-conflict. No
    rollback window on a policy downgrade either: the code constant IS
    the policy source, so a downgrade bump heals forward to the new
    (lower) constant the same way.

    Returns (policy_written, policy_synced): written = the block was
    absent/broken and rebuilt wholesale; synced = an existing dict had
    at least one policy key healed in place.
    """
    beat = data.get("beat")
    if not isinstance(beat, dict):
        data["beat"] = dict(BEAT_POLICY)
        return True, False
    synced = False
    for key, value in BEAT_POLICY.items():
        if beat.get(key) != value:
            beat[key] = value
            synced = True
    return False, synced


def pulse_state_beat(reason, state_path=None, now=None):
    """PT-20261015-01 remediation (R2308): pulse-only state beat writer.

    Freshness touch for defer windows - the inspection anchor is the
    2026-10-15 18:26->20:38 window: the spawn gate deferred every slot
    (live codely.exe >= 2), no round body ran, no closing step refreshed
    ts, and fleet-audit read the machine heartbeat face STALE 2.2h while
    the loop was alive. The SPAWNER calls this while holding round.lock -
    a live round body implies its spawner still holds the lock, so no
    finalize_state can interleave here (structural, not TOCTOU).

    Encoded laws:
    - accounting-untouched: tick / log / task / focus / watermarks are
      never modified - tech#149 stays whole, the accounting face keeps
      exactly one writer. Refuses (loud, zero partial writes) when the
      on-disk ts is missing/malformed or the pulse clock is not strictly
      newer (clock-skew guard: a pulse never moves ts backwards).
    - reason: non-empty, clamped to PULSE_REASON_MAX chars; CLI enforces
      ASCII (encoding rule - GBK console hazard).
    - beat policy block: written when absent, policy-key synced to the
      code constant otherwise (tech#220 sync-on-diff, see BEAT_POLICY);
      sub-keys outside BEAT_POLICY (hand-tuned notes) always survive.

    Returns summary dict {ts, reason, policy_written, policy_synced}.
    Raises ValueError
    on usage errors - validation happens before the first disk mutation;
    the atomic replace makes the write all-or-nothing.
    """
    if state_path is None:
        state_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "state.json")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("pulse reason must be a non-empty string")
    reason = reason.strip()[:PULSE_REASON_MAX]
    clock = now if now is not None else datetime.datetime.now()
    ts = clock.strftime("%Y-%m-%d %H:%M:%S")

    with io.open(state_path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data.get("log"), list):
        raise ValueError("state.json 'log' is not a list - refusing to touch")
    cur_ts = data.get("ts")
    if not isinstance(cur_ts, str) or not TS_RE.match(cur_ts):
        raise ValueError("state ts missing/malformed - refusing to pulse "
                         "over a broken face: %r" % (cur_ts,))
    try:
        cur_dt = datetime.datetime.strptime(cur_ts, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("state ts unparseable: %r" % (cur_ts,))
    if clock <= cur_dt:
        raise ValueError("pulse ts %s not newer than on-disk ts %s "
                         "(clock skew?) - refusing" % (ts, cur_ts))

    policy_written, policy_synced = _sync_beat_policy(data)
    data["ts"] = ts
    data["pulse"] = {"ts": ts, "reason": reason}

    payload = json.dumps(data, ensure_ascii=False, indent=1)
    tmp = state_path + ".tmp_pulse"
    with io.open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(payload)
    os.replace(tmp, state_path)
    # ASCII-only evidence line (encoding law)
    print("STATE-PULSED ts=%s reason=%r policy_written=%s "
          "policy_synced=%s" % (ts, reason, policy_written, policy_synced))
    return {"ts": ts, "reason": reason, "policy_written": policy_written,
            "policy_synced": policy_synced}


def _path_is_gitignored(root, rel_path):
    """True when git ignores rel_path (``git check-ignore -q`` advisory).

    tech#157 guard: any git failure (missing binary, not a repo) reads as
    "not ignored" so this helper can never fail a close on its own.
    """
    try:
        proc = subprocess.run(
            ["git", "-C", root, "check-ignore", "-q", rel_path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return proc.returncode == 0
    except OSError:
        return False


def autodetect_close_script(root, state_path=None):
    """tech#81: the round's own close script auto-includes itself.

    r1930 anchor: that round's close script stayed untracked across
    rounds (cleanup-hook relapse family, R1895/R1896/R1897 priors) because
    the explicit manifest never contained the script consuming it - the
    next round had to hand-patch it in. This detector returns the
    repo-relative path ``.c3-tmp/r{tick}_close.py`` when the state tick is
    readable and that exact file exists on disk; run_close_commit appends
    it to the manifest so the accounting commit is self-contained.

    Strict shape law: only the exact round-anchored name is ever returned -
    no glob, no other .c3-tmp file rides along (older-round leftovers stay
    the round-debris guard's business, tech#66). Advisory by design: an
    unreadable state, a non-int tick or a missing script all return None
    and never fail the close.

    tech#157 retirement (R2229): when the anchored script path is
    gitignored (the born-fix gitignore line ``.c3-tmp/``), the
    self-include is retired - appending an ignored path would fail the
    ``git add`` step, so an ignored close script returns None (advisory,
    same as missing; the cleanup hook owns disk deletion).
    """
    if state_path is None:
        state_path = os.path.join(root, "src", "os", "state.json")
    try:
        with io.open(state_path, encoding="utf-8") as f:
            data = json.load(f)
        tick = data.get("tick")
    except (OSError, ValueError):
        return None
    if not isinstance(tick, int):
        return None
    rel = ".c3-tmp/r%d_close.py" % tick
    if os.path.isfile(os.path.join(root, rel.replace("/", os.sep))):
        if _path_is_gitignored(root, rel):
            return None
        return rel
    return None


def read_disk_state_tick(root=None, state_path=None):
    """On-disk state.json -> tick int or None (advisory read). Any
    unreadable/malformed ledger stays None - the account faces own that
    disease; this helper only answers "what tick does the disk ledger
    carry right now"."""
    if state_path is None:
        if root is None:
            root = os.path.abspath(
                os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "..", ".."))
        state_path = os.path.join(root, "src", "os", "state.json")
    try:
        with io.open(state_path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return None
    tick = data.get("tick") if isinstance(data, dict) else None
    if isinstance(tick, int) and not isinstance(tick, bool):
        return tick
    return None


def verify_state_tick(expect_tick, root=None, state_path=None):
    """tech#155 face 2 (R2214 anchor): the post-close readback assertion.

    The anchor: a prior body landed three round commits while its
    narrative claimed the accounting was complete - finalize_state was
    never called and state.json stayed a round behind; the successor
    found the gap by manual git-log archaeology. The hand-written
    readback at the end of the R2214 absorb close script is the
    demonstration this encodes as the standing law: a round that
    commits its work re-reads its own accounting before claiming
    closure.

    Returns (ok, line) - a loud ASCII verify line for the evidence
    capture, never a silent skip. expect_tick = the tick the ledger is
    expected to carry after THIS round's finalize; the helper re-reads
    the on-disk ledger and compares (the caller's memory of calling
    finalize is exactly what the anchor proved unreliable).
    """
    if (not isinstance(expect_tick, int) or isinstance(expect_tick, bool)
            or expect_tick < 0):
        return False, ("USAGE-ERROR expect_tick must be a non-negative int "
                      "(got %r)" % (expect_tick,))
    tick = read_disk_state_tick(root, state_path)
    if tick == expect_tick:
        return True, "VERIFY-OK state tick=%d (readback)" % expect_tick
    got = tick if tick is not None else "unreadable"
    return False, ("VERIFY-FAIL state tick=%s expected %d - the round "
                  "claims accounting the ledger does not carry (R2214 "
                  "anchor: commits landed, finalize never ran) - re-run "
                  "the finalize before claiming closure" % (got, expect_tick))


def refresh_export_in_close(root, patch, do, now_fn=None, dry_run=False):
    """tech#148: refresh docs/status-export.json through the canonical
    writer (tech#70) as part of the close. Returns (rc, lines) with the
    writer's own rc (0 written / 1 io / 2 refusal). Warn-only at the close
    level: a refused write leaves the export byte-identical - the safe
    state the R2124 hand-rolled dump bypassed."""
    import export_refresh  # sibling module; lazy to keep CLI startup light
    # DEFAULT_EXPORT_REL is already OS-native (built with os.path.join)
    export_path = os.path.join(root, export_refresh.DEFAULT_EXPORT_REL)
    kwargs = {"patch": patch, "do": do, "dry_run": dry_run}
    if now_fn is not None:
        kwargs["now_fn"] = now_fn
    rc, lines, _violations = export_refresh.refresh_export(export_path, **kwargs)
    return rc, lines


def run_close_commit(files, message, root=None, push=True, dry_run=False,
                     export_patch=None, export_do=None, export_now_fn=None,
                     expect_tick=None):
    """Commit exactly `files` with `message`; push unless disabled.

    tech#148: when export_patch (dict) and/or export_do (str) is given,
    docs/status-export.json is refreshed through the canonical writer
    (export_refresh) BEFORE the git steps and rides the manifest
    automatically. Writer refusal is warn-only (see module docstring).
    export_now_fn is a test-only clock injection for the writer's
    live-clock stamp; None = the writer's real clock.

    tech#155 face 2: when expect_tick (int) is given, the close ends
    with a readback verify - the on-disk state.json is re-read AFTER the
    commit steps and must carry expect_tick (the tick this round's
    finalize wrote); a mismatch is the R2214 anchor shape (commits
    landed, accounting never ran) and returns RC_VERIFY with a loud
    VERIFY-FAIL line while the commit stays landed. None = legacy call
    surface, zero behavioral change (zero regression law).

    Returns (rc, lines) where lines is the evidence-friendly ASCII log of
    every step taken. See the module docstring for the rc contract and
    the encoded laws.
    """
    lines = []
    if root is None:
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    # --- usage validation before any git call (loud, no side effects) ---
    if not isinstance(message, str) or not message.strip():
        lines.append("USAGE-ERROR empty message")
        return RC_USAGE, lines
    if not message_is_ascii(message):
        lines.append("USAGE-ERROR message must be ASCII (encoding rule)")
        return RC_USAGE, lines
    if len(message) > MSG_MAX_SOFT:
        lines.append("WARN-COMMIT-MSG-LEN %d>%d (P-30 soft bound)" % (
            len(message), MSG_MAX_SOFT))
    if expect_tick is not None and (not isinstance(expect_tick, int)
                                    or isinstance(expect_tick, bool)
                                    or expect_tick < 0):
        lines.append("USAGE-ERROR expect_tick must be a non-negative int "
                     "when given (got %r)" % (expect_tick,))
        return RC_USAGE, lines
    try:
        rel_files = resolve_files(root, files)
    except ValueError as exc:
        lines.append("USAGE-ERROR %s" % exc)
        return RC_USAGE, lines

    # --- tech#81: self-inclusion law (r1930 anchor) - the round's own close
    # script rides the manifest automatically so it never lingers untracked
    # across rounds. Advisory: a missing anchor (test fixtures, non-standard
    # roots) never fails the close; already-listed paths are not duplicated. ---
    auto_self = autodetect_close_script(root)
    if auto_self is None:
        lines.append("NOTE close-script self-anchor absent (tech#81, advisory)")
    elif auto_self in rel_files:
        lines.append("NOTE self %s already listed (tech#81)" % auto_self)
    else:
        rel_files.append(auto_self)
        lines.append("STEP self-include %s (tech#81)" % auto_self)

    # --- tech#188: F-registration backwrite guard (R2258 anchor). The
    # anchor round registered F-180 in output/finished.md but its FILES
    # list missed state/queue/main.md - main#19's done mark stayed
    # unwritten for 57 rounds until tech#185 surfaced it. The structural
    # fix is this loud advisory at the one place that sees the whole
    # manifest: an F-registration close without the queue backwrite on
    # board is almost always the forget-shape. Advisory by design (the
    # mark may legitimately live in an earlier commit) - never fails an
    # accounting close. ---
    if (FINISHED_LEDGER_REL in rel_files
            and QUEUE_MAIN_REL not in rel_files):
        lines.append(
            "WARN F-REGISTRATION close without queue backwrite - %s "
            "missing from the manifest; backwrite the main-queue done "
            "mark for the new F-number (tech#188, R2258 anchor: main#19 "
            "stayed undone for 57 rounds)" % QUEUE_MAIN_REL)

    # --- tech#209: F-registration station-reviews backwrite guard
    # (R2342 anchor). The F-192/F-193 rounds registered their finished
    # entries but never wrote the station-reviews ledger row - the
    # station-reviews tail lagged two rounds until R2342 backfilled
    # both rows (R16/R21 repair precedent). Same advisory shape as
    # tech#188: the row may legitimately live in an earlier commit, so
    # the WARN never fails an accounting close. ---
    if (FINISHED_LEDGER_REL in rel_files
            and STATION_REVIEWS_REL not in rel_files):
        lines.append(
            "WARN F-REGISTRATION-SR close without station-reviews "
            "backwrite - %s missing from the manifest; backwrite the "
            "station-reviews row for the new F-number (tech#209, "
            "R2342 anchor: F-192/F-193 rows lagged two rounds)"
            % STATION_REVIEWS_REL)

    # --- main#139: REACT-form F-registration residents backwrite guard
    # (R2373 anchor). F-192/F-196/F-197 carried closing-position anchors
    # whose appearance-ledger rows were never written at registration -
    # the misses surfaced only via the R2373 backfill batch. Trigger
    # face: a finished-ledger write plus any REACT-form artifact path
    # (review files carry "mcreact", card dirs carry "REACT") with no
    # residents-ledger write on board. Same advisory contract as
    # tech#188/209: the row may legitimately live in an earlier commit,
    # so the WARN never fails an accounting close. ---
    if (FINISHED_LEDGER_REL in rel_files
            and RESIDENTS_LEDGER_REL not in rel_files
            and any("react" in rel.lower() for rel in rel_files)):
        lines.append(
            "WARN F-REGISTRATION-RESIDENTS close without residents "
            "backwrite - %s missing from the manifest; backwrite the "
            "closing-position appearance-ledger row for the new REACT "
            "F-number (main#139, R2373 anchor: F-192/F-196/F-197 rows "
            "lagged to the backfill batch)" % RESIDENTS_LEDGER_REL)

    # --- tech#257: F-registration renders birth gate (R2398 anchor).
    # The single-round fast chain registered F-199 in the finished
    # ledger but never wrote the renders README row - readiness only
    # surfaced the unannotated mp4 at the NEXT round's probe (R2399
    # backfill). Birth-position move: run the same render-unannot
    # semantics at close time, so the forget-shape dies inside its own
    # round. Content-level by design (audio/novel/comic-line F items
    # legitimately carry no renders face - manifest absence is not
    # evidence); advisory by design (same WARN grade as tech#188/209,
    # never fails an accounting close). The NOTE line always lands at
    # an F-registration close so the gate's execution is observable -
    # its absence would itself be fail-open evidence for the probe. ---
    if FINISHED_LEDGER_REL in rel_files:
        unannot = unannotated_render_media(root)
        lines.append("NOTE F-RENDERS-BIRTH-GATE unannot=%d (tech#257)"
                     % len(unannot))
        if unannot:
            shown = ", ".join(unannot[:3])
            if len(unannot) > 3:
                shown += " (+%d more)" % (len(unannot) - 3)
            lines.append(
                "WARN F-REGISTRATION-RENDERS close with unannotated "
                "render media - %s; backwrite the %s row(s) (tech#257, "
                "R2398 anchor: F-199 renders row lagged one round to "
                "the R2399 backfill)" % (shown, RENDERS_LEDGER_REL))

    # --- tech#148: canonical export refresh (before the git steps so the
    # refreshed export rides the same accounting commit). Refusal is
    # warn-only: the export stays byte-identical and the close continues -
    # an accounting close must never fail on the export face, and the
    # routine probe keeps flagging a stale face until a clean patch lands. ---
    if export_patch is not None or export_do is not None:
        rc_x, xlines = refresh_export_in_close(
            root, export_patch, export_do, now_fn=export_now_fn,
            dry_run=dry_run)
        lines.extend(xlines)
        if dry_run:
            lines.append("DRY-RUN manifest would include "
                         "docs/status-export.json (tech#148)")
        elif rc_x == RC_OK:
            export_rel = "docs/status-export.json"
            if export_rel not in rel_files:
                rel_files.append(export_rel)
                lines.append("STEP export %s rides manifest (tech#148)"
                             % export_rel)
        elif rc_x == RC_WRITER_REFUSE:
            lines.append("WARN EXPORT-REFUSED rc=2 - export NOT refreshed, "
                         "close continues (probe keeps flagging)")
        else:
            lines.append("WARN EXPORT-IOFAIL rc=%d - export NOT refreshed, "
                         "close continues" % rc_x)

    plan_add = ["git", "add", "--"] + rel_files
    plan_commit = ["git", "commit", "-m", message, "--"] + rel_files
    plan_sha = ["git", "rev-parse", "HEAD"]
    plan_push = ["git", "push"]

    # --- tech#67: purge .c3-tmp __pycache__ before the git steps (never
    # evidence; a regenerated cache would re-trip the round-debris guard
    # forever). Cleanup is warn-only - it must never fail the close. ---
    if dry_run:
        n_cache, _fails = purge_c3tmp_pycache(root, dry=True)
        lines.append("DRY-RUN pycache purge %d dir(s) (skipped)" % n_cache)
    else:
        n_cache, fails = purge_c3tmp_pycache(root)
        lines.append("STEP pycache purged %d dir(s) (tech#67)" % n_cache)
        for f in fails:
            lines.append("WARN pycache purge failed: %s" % f)

    # --- tech#233: UTF-16 debris self-heal (R2375 anchor, third PS 5.1
    # `>` occurrence). Root-level .c3-tmp files carrying a UTF-16 BOM are
    # losslessly transcoded to UTF-8 in place BEFORE the git steps, so the
    # debris class can no longer survive a round boundary (the probe face
    # stays live: loop_health keeps naming anything that appears mid-round).
    # Self-heal rather than refuse: a hard close refusal would trade
    # disposable middleware for accounting-tick holes - the strictly worse
    # failure class. Warn-only, never fails the close. ---
    if dry_run:
        t_names, _t_failed = transcode_c3tmp_utf16(root, dry=True)
        lines.append("DRY-RUN utf16-debris transcode %d file(s) (skipped)"
                     % len(t_names))
    else:
        t_names, t_failed = transcode_c3tmp_utf16(root)
        lines.append("STEP utf16-debris transcoded %d file(s) (tech#233)"
                     % len(t_names))
        for name in t_names:
            lines.append("STEP utf16-debris transcoded: %s" % name)
        for name in t_failed:
            lines.append("WARN utf16-debris transcode failed: %s "
                         "(left as-is; decode error)" % name)

    if dry_run:
        lines.append("DRY-RUN " + " ".join(plan_add))
        lines.append("DRY-RUN " + " ".join(plan_commit))
        lines.append("DRY-RUN " + plan_sha[1] + " (report sha)")
        if push:
            lines.append("DRY-RUN " + " ".join(plan_push))
        lines.append("DRY-RUN no steps executed")
        return RC_OK, lines

    # --- step 1: explicit add (untracked evidence files enter the index) ---
    rc, out, err = _git(root, plan_add[1:])
    if rc != 0:
        lines.append("GIT-FAIL add rc=%d %s" % (rc, (err or out).splitlines()[:1]))
        return RC_GIT, lines
    lines.append("STEP add ok (%d file(s))" % len(rel_files))

    # --- step 2: pathspec commit (other sessions' staged files untouched) ---
    rc, out, err = _git(root, ["commit", "-m", message, "--"] + rel_files)
    if rc != 0:
        first = (err or out).splitlines()
        lines.append("GIT-FAIL commit rc=%d %s" % (rc, first[:1]))
        return RC_GIT, lines
    lines.append("STEP commit ok")

    # --- step 3: report the landed sha (evidence face) ---
    rc, out, err = _git(root, ["rev-parse", "--short", "HEAD"])
    if rc == 0:
        lines.append("STEP head %s" % out)
    else:
        lines.append("WARN rev-parse failed rc=%d" % rc)

    # --- step 4: push (warn-only; mandate self-heal law) ---
    if push:
        rc, out, err = _git(root, ["push"])
        if rc == 0:
            lines.append("STEP push ok")
        else:
            lines.append("PUSH-WARN rc=%d %s (record, do not fix; next round "
                         "origin_gap_check surfaces ahead)" % (rc, (err or out).splitlines()[:1]))
    else:
        lines.append("STEP push skipped (--no-push)")

    lines.append("CLOSE-COMMIT-OK %d file(s)" % len(rel_files))
    # --- tech#155 face 2: post-close readback verify (R2214 anchor).
    # Runs AFTER push (the commit is real work and must land regardless);
    # the verify reads the ON-DISK ledger, not the caller's memory of
    # calling finalize - the anchor proved exactly that memory unreliable.
    # Only active when expect_tick was passed (legacy surface unchanged).
    if expect_tick is not None:
        ok, vline = verify_state_tick(expect_tick, root=root)
        lines.append(vline)
        if not ok:
            return RC_VERIFY, lines
    return RC_OK, lines


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Embedded accounting-close commit helper (tech#65).")
    ap.add_argument("--files", nargs="+", default=None,
                    help="explicit file list (repo-relative), never add -A; "
                         "not required in --pulse mode")
    ap.add_argument("--message", default=None,
                    help="ASCII one-line commit message; not required in "
                         "--pulse mode")
    ap.add_argument("--pulse", default=None,
                    help="PT-20261015-01: pulse-only state beat (ASCII "
                         "reason) - refreshes ts + pulse marker with zero "
                         "accounting touch (defer-window freshness)")
    ap.add_argument("--state-path", default=None,
                    help="state.json path override for --pulse (default: "
                         "the live ledger next to this module)")
    ap.add_argument("--root", default=None,
                    help="repo root (default: this module's repo)")
    ap.add_argument("--no-push", action="store_true",
                    help="skip the push step (warn-only law still applies)")
    ap.add_argument("--export-patch", default=None,
                    help="JSON object file with a subset of "
                         "do/depts/outs/chips/results/live - refreshed "
                         "through the canonical writer before the commit "
                         "(tech#148; hand-rolled json.dump is retired)")
    ap.add_argument("--export-do", default=None,
                    help='convenience: update the export "do" one-liner '
                         "via the canonical writer (tech#148)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print planned commands, execute nothing")
    ap.add_argument("--expect-tick", type=int, default=None,
                    help="tech#155 face 2: after the commit, re-read the "
                         "on-disk state.json and verify it carries this "
                         "tick (the R2214 readback law); mismatch = rc 3 "
                         "with a loud VERIFY-FAIL line")
    args = ap.parse_args(argv)

    # --- PT-20261015-01 pulse mode: no accounting, no git, exit fast ---
    if args.pulse is not None:
        if not message_is_ascii(args.pulse):
            print("USAGE-ERROR pulse reason must be ASCII (encoding rule)")
            return RC_USAGE
        try:
            pulse_state_beat(args.pulse, state_path=args.state_path)
        except ValueError as exc:
            print("PULSE-FAIL %s" % exc)
            return RC_USAGE
        except OSError as exc:
            print("PULSE-FAIL io: %.120s" % exc)
            return RC_USAGE
        return RC_OK

    if not args.files or not args.message:
        print("USAGE-ERROR --files and --message are required without "
              "--pulse")
        return RC_USAGE

    export_patch = None
    if args.export_patch:
        try:
            with open(args.export_patch, "r", encoding="utf-8-sig",
                      errors="replace") as fh:
                export_patch = json.load(fh)
        except (OSError, ValueError) as exc:
            print("USAGE-ERROR export patch file unreadable: %.80s" % exc)
            return RC_USAGE

    rc, lines = run_close_commit(args.files, args.message, root=args.root,
                                 push=not args.no_push, dry_run=args.dry_run,
                                 export_patch=export_patch,
                                 export_do=args.export_do,
                                 expect_tick=args.expect_tick)
    for line in lines:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
