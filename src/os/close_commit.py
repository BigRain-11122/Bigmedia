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

rc: 0 = commit landed (push may have warned); 1 = a git add/commit step
failed; 2 = usage error; 3 = readback verify failed (tech#155 face 2:
expect_tick passed and the on-disk ledger does not carry it - the commit
stays landed, the next body absorbs the accounting). Output lines are plain ASCII text, safe for
evidence capture files.

CLI:
    python src/os/close_commit.py --files A B C --message "..."
        [--root PATH] [--no-push] [--dry-run]

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

# tech#76: ledger prefix shape. Minute field is two chars - digit+digit
# ("23:26") or digit+x ("23:5x", fuzzy-minute house style). Anything else
# raises before the ledger is touched (born-level gate).
LOG_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{1}[0-9x] R\d+: ")
TASK_MAX_CHARS = 60  # mandate: task = log line minus prefix, first 60 chars
TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")


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


def finalize_state(log_line, ts=None, focus=None, tick=None,
                   watermark_add=None, orders_watermark=None, state_path=None,
                   now=None):
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
    default = auto-increment) -> append log line -> stamp ts/task ->
    optional focus overwrite -> optional decisions_watermark.dnums append
    (dedup, order-preserving) -> optional orders_row_watermark overwrite
    (tech#103 consumption anchor) -> atomic write (temp + os.replace,
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
            the body consumes the new HQ orders rows (tech#103; compute
            turnkey via group_scan.current_orders_watermark()).
        state_path: default = state.json next to this module.
        now: injectable clock (needs strftime) for tests.

    Returns: summary dict {tick, ts, task, wm_added, orders_wm_rows,
    log_len} (orders_wm_rows None when no orders watermark was given).
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

    data["tick"] = new_tick
    data["log"].append(log_line)
    data["ts"] = ts
    data["task"] = task
    if focus is not None:
        data["focus"] = focus
    if orders_wm_stored is not None:
        data["orders_row_watermark"] = orders_wm_stored

    payload = json.dumps(data, ensure_ascii=False, indent=1)
    tmp = state_path + ".tmp_final"
    with io.open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(payload)
    os.replace(tmp, state_path)
    # ASCII-only evidence line (encoding law; task/ts contain CJK digits text)
    print("STATE-FINALIZED tick=%s ts=%s task_len=%d focus_set=%s "
          "wm_added=%d orders_wm_rows=%s log_len=%d" % (
              new_tick, ts, len(task), focus is not None, wm_added,
              orders_wm_stored["rows"] if orders_wm_stored else "-",
              len(log_line)))
    return {"tick": new_tick, "ts": ts, "task": task,
            "wm_added": wm_added, "log_len": len(log_line),
            "orders_wm_rows": (orders_wm_stored["rows"]
                               if orders_wm_stored else None)}


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
    ap.add_argument("--files", nargs="+", required=True,
                    help="explicit file list (repo-relative), never add -A")
    ap.add_argument("--message", required=True,
                    help="ASCII one-line commit message")
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
