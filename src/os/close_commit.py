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

rc: 0 = commit landed (push may have warned); 1 = a git add/commit step
failed; 2 = usage error. Output lines are plain ASCII text, safe for
evidence capture files.

CLI:
    python src/os/close_commit.py --files A B C --message "..."
        [--root PATH] [--no-push] [--dry-run]
"""

import argparse
import os
import shutil
import subprocess
import sys

RC_OK = 0
RC_GIT = 1
RC_USAGE = 2

MSG_MAX_SOFT = 500  # P-30 one-line convention; WARN only, never fails
PYCACHE_DIRNAME = "__pycache__"


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


def run_close_commit(files, message, root=None, push=True, dry_run=False):
    """Commit exactly `files` with `message`; push unless disabled.

    Returns (rc, lines) where lines is the evidence-friendly ASCII log of
    every step taken. See the module docstring for the rc contract and the
    encoded laws.
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
    try:
        rel_files = resolve_files(root, files)
    except ValueError as exc:
        lines.append("USAGE-ERROR %s" % exc)
        return RC_USAGE, lines

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
    ap.add_argument("--dry-run", action="store_true",
                    help="print planned commands, execute nothing")
    args = ap.parse_args(argv)
    rc, lines = run_close_commit(args.files, args.message, root=args.root,
                                 push=not args.no_push, dry_run=args.dry_run)
    for line in lines:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
