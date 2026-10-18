# -*- coding: utf-8 -*-
"""Unit tests for the embedded accounting-close commit helper
(src/os/close_commit.py, tech#65, R1899).

Real-git fixtures in temp dirs (the test_lock_guard precedent: the engine is
the proof). No network: the push tests use a local bare repo as the remote.

The regression locks here are the two real incidents this module encodes:
- R1897 kill-window form -> the commit must be INSIDE the close script step
  (structural: these tests pin the run_close_commit contract the close
  script calls as its last step).
- 2026-10-09 staged-sweep incident -> a plain `git commit` sweeps another
  session's staged files; the pathspec commit here must not.

Run:
    python tests/test_close_commit.py
"""

import datetime
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "os"))

import close_commit as cc  # noqa: E402

GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")

MSG = "test close commit [via bm-a]"


class GitRepo(object):
    """Plain fixture (not a TestCase): a temp git repo with two committed
    base files. TestCase classes mix it in; standalone users destroy()."""

    def __init__(self):
        self.root = Path(tempfile.mkdtemp(prefix="close_commit_"))
        self._git(["init", "-q"])
        (self.root / "a.txt").write_text("base", encoding="utf-8")
        (self.root / "b.txt").write_text("base", encoding="utf-8")
        self._git(["add", "a.txt", "b.txt"])
        self._git(["commit", "-q", "-m", "base"])
        # normalize the branch name: plain `git push` under push.default=simple
        # refuses when local and upstream branch names differ
        self._git(["branch", "-M", "main"])
        self.head0 = self.head()

    def destroy(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def _git(self, args):
        proc = subprocess.run(["git"] + list(args), cwd=str(self.root), env=GIT_ENV,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return (proc.returncode,
                proc.stdout.decode("utf-8", "replace"),
                proc.stderr.decode("utf-8", "replace"))

    def head(self):
        rc, out, err = self._git(["rev-parse", "HEAD"])
        if rc != 0:
            raise AssertionError("rev-parse failed: %s" % err)
        return out.strip()

    def head_files(self):
        rc, out, err = self._git(["show", "--name-only", "--format=", "HEAD"])
        if rc != 0:
            raise AssertionError("show failed: %s" % err)
        return [l for l in out.splitlines() if l.strip()]

    def staged_files(self):
        rc, out, err = self._git(["diff", "--cached", "--name-only"])
        if rc != 0:
            raise AssertionError("diff --cached failed: %s" % err)
        return [l for l in out.splitlines() if l.strip()]

    def close(self, files, message=MSG, **kw):
        return cc.run_close_commit(files, message, root=str(self.root), **kw)


class GitRepoCase(unittest.TestCase, GitRepo):
    """Per-test isolated fixture for the TestCase classes below."""

    def setUp(self):
        GitRepo.__init__(self)

    def tearDown(self):
        self.destroy()


class TestValidation(unittest.TestCase):
    """Usage errors must be loud BEFORE any git call (no side effects)."""

    def test_empty_files_refused(self):
        rc, lines = cc.run_close_commit([], "msg")
        self.assertEqual(cc.RC_USAGE, rc)
        self.assertTrue(any("empty" in l for l in lines))

    def test_empty_message_refused(self):
        rc, lines = cc.run_close_commit(["a.txt"], "  ")
        self.assertEqual(cc.RC_USAGE, rc)

    def test_non_ascii_message_refused(self):
        rc, lines = cc.run_close_commit(["a.txt"], "记账 commit 中文消息")
        self.assertEqual(cc.RC_USAGE, rc)
        self.assertTrue(any("ASCII" in l for l in lines))

    def test_missing_file_is_loud(self):
        root = tempfile.mkdtemp(prefix="close_commit_")
        try:
            rc, lines = cc.run_close_commit(["nope.txt"], "msg", root=root)
            self.assertEqual(cc.RC_USAGE, rc)
            self.assertTrue(any("missing" in l for l in lines))
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def test_path_escape_refused(self):
        outside = Path(tempfile.mkdtemp(prefix="close_commit_out_"))
        try:
            (outside / "x.txt").write_text("x", encoding="utf-8")
            root = tempfile.mkdtemp(prefix="close_commit_in_")
            try:
                rc, lines = cc.run_close_commit([str(outside / "x.txt")], "msg",
                                                root=root)
                self.assertEqual(cc.RC_USAGE, rc)
                self.assertTrue(any("escapes" in l for l in lines))
            finally:
                shutil.rmtree(root, ignore_errors=True)
        finally:
            shutil.rmtree(outside, ignore_errors=True)

    def test_ascii_checker(self):
        self.assertTrue(cc.message_is_ascii("plain ascii 123"))
        self.assertFalse(cc.message_is_ascii("not ascii: 记"))


class TestContract(GitRepoCase):
    """The R1897 close-script contract: last-step embedded commit."""

    def test_long_message_warns_but_commits(self):
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        long_msg = "x" * (cc.MSG_MAX_SOFT + 1)
        rc, lines = self.close(["a.txt"], message=long_msg, push=False)
        self.assertEqual(cc.RC_OK, rc)
        self.assertTrue(any("WARN-COMMIT-MSG-LEN" in l for l in lines))
        self.assertNotEqual(self.head0, self.head())

    def test_explicit_files_only(self):
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        (self.root / "other.txt").write_text("other session", encoding="utf-8")
        rc, lines = self.close(["a.txt"], push=False)
        self.assertEqual(cc.RC_OK, rc)
        self.assertEqual(["a.txt"], self.head_files())
        self.assertNotIn("other.txt", self.head_files())
        # unlisted untracked file stays untracked
        rc, out, _ = self._git(["status", "--porcelain", "--", "other.txt"])
        self.assertIn("?? other.txt", out)

    def test_other_session_staged_not_swept(self):
        """2026-10-09 incident regression lock: a plain commit sweeps the
        index; the pathspec commit must leave another session's staged
        files in the index, untouched."""
        (self.root / "b.txt").write_text("other session edit", encoding="utf-8")
        self._git(["add", "b.txt"])  # the other session stages its file
        (self.root / "a.txt").write_text("my accounting write", encoding="utf-8")
        rc, lines = self.close(["a.txt"], push=False)
        self.assertEqual(cc.RC_OK, rc)
        self.assertEqual(["a.txt"], self.head_files())
        self.assertEqual(["b.txt"], self.staged_files())  # still staged, not swept

    def test_untracked_listed_file_committed(self):
        (self.root / "a.txt").write_text("changed too", encoding="utf-8")
        (self.root / "evidence.txt").write_text("r1899 probe capture", encoding="utf-8")
        rc, lines = self.close(["a.txt", "evidence.txt"], push=False)
        self.assertEqual(cc.RC_OK, rc)
        self.assertIn("a.txt", self.head_files())
        self.assertIn("evidence.txt", self.head_files())
        rc, out, _ = self._git(["status", "--porcelain"])
        self.assertEqual("", out)  # tree clean for both

    def test_nothing_to_commit_is_loud(self):
        """Clean tree + unchanged listed file: git commit exits nonzero;
        the close must surface it, not silently claim ok."""
        rc, lines = self.close(["a.txt"], push=False)
        self.assertEqual(cc.RC_GIT, rc)
        self.assertTrue(any("GIT-FAIL commit" in l for l in lines))

    def test_dry_run_zero_side_effects(self):
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], dry_run=True)
        self.assertEqual(cc.RC_OK, rc)
        self.assertTrue(any(l.startswith("DRY-RUN git add") for l in lines))
        self.assertTrue(any("DRY-RUN no steps executed" in l for l in lines))
        self.assertEqual(self.head0, self.head())  # no commit happened
        rc, out, _ = self._git(["status", "--porcelain"])
        self.assertIn(" M a.txt", out)  # nothing staged either

    def test_commit_reports_head_sha(self):
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], push=False)
        self.assertEqual(cc.RC_OK, rc)
        self.assertTrue(any(l.startswith("STEP head ") for l in lines))
        self.assertTrue(any(l.startswith("CLOSE-COMMIT-OK") for l in lines))


class TestPushLaw(GitRepoCase):
    """Push is warn-only (mandate self-heal law: record, do not fix)."""

    def test_push_failure_warns_but_commit_lands(self):
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], push=True)  # no remote configured
        self.assertEqual(cc.RC_OK, rc)
        self.assertTrue(any(l.startswith("PUSH-WARN") for l in lines))
        self.assertNotEqual(self.head0, self.head())  # commit landed locally

    def test_push_success_lands_on_remote(self):
        bare = Path(tempfile.mkdtemp(prefix="close_commit_bare_")) / "remote.git"
        try:
            subprocess.run(["git", "init", "-q", "--bare", str(bare)],
                           check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self._git(["remote", "add", "origin", str(bare)])
            # -u sets the upstream so the module's plain `git push` works
            self._git(["push", "-q", "-u", "origin", "HEAD:refs/heads/main"])
            (self.root / "a.txt").write_text("changed again", encoding="utf-8")
            rc, lines = self.close(["a.txt"], push=True)
            self.assertEqual(cc.RC_OK, rc)
            self.assertTrue(any(l.startswith("STEP push ok") for l in lines))
            proc = subprocess.run(
                ["git", "-C", str(bare), "rev-parse", "refs/heads/main"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(self.head(), proc.stdout.decode().strip())
        finally:
            shutil.rmtree(bare.parent, ignore_errors=True)


class TestPycachePurge(GitRepoCase):
    """tech#67: the close purges .c3-tmp __pycache__ dirs (R1900 anchor:
    a regenerated r1897_close.cpython-314.pyc would re-trip the
    round-debris guard forever - bytecode caches are never evidence)."""

    def _mk_pycache(self, *relparts):
        d = self.root.joinpath(*relparts)
        d.mkdir(parents=True, exist_ok=True)
        (d / "x.cpython-314.pyc").write_bytes(b"\x00pyc")
        return d

    def test_pycache_purged_before_commit(self):
        pc = self._mk_pycache(".c3-tmp", "__pycache__")
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], push=False)
        self.assertEqual(cc.RC_OK, rc)
        self.assertFalse(pc.exists())
        self.assertTrue(any(l.startswith("STEP pycache purged 1 dir(s)") for l in lines))

    def test_nested_pycache_dirs_purged(self):
        pc1 = self._mk_pycache(".c3-tmp", "__pycache__")
        pc2 = self._mk_pycache(".c3-tmp", "sub", "__pycache__")
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], push=False)
        self.assertEqual(cc.RC_OK, rc)
        self.assertFalse(pc1.exists())
        self.assertFalse(pc2.exists())
        self.assertTrue(any("purged 2 dir(s)" in l for l in lines))

    def test_pycache_outside_c3tmp_untouched(self):
        keep = self._mk_pycache("src", "os", "__pycache__")
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], push=False)
        self.assertEqual(cc.RC_OK, rc)
        self.assertTrue(keep.exists())  # scope law: only the .c3-tmp subtree
        self.assertTrue(any("purged 0 dir(s)" in l for l in lines))

    def test_dry_run_does_not_purge(self):
        pc = self._mk_pycache(".c3-tmp", "__pycache__")
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], dry_run=True)
        self.assertEqual(cc.RC_OK, rc)
        self.assertTrue(pc.exists())  # zero side effects
        self.assertTrue(any("DRY-RUN pycache purge 1 dir(s)" in l for l in lines))

    def test_missing_c3tmp_zero_purge(self):
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], push=False)
        self.assertEqual(cc.RC_OK, rc)
        self.assertTrue(any("purged 0 dir(s)" in l for l in lines))

    def test_purge_helper_dry_counts_without_deleting(self):
        pc = self._mk_pycache(".c3-tmp", "__pycache__")
        n, fails = cc.purge_c3tmp_pycache(str(self.root), dry=True)
        self.assertEqual((1, []), (n, fails))
        self.assertTrue(pc.exists())
        n, fails = cc.purge_c3tmp_pycache(str(self.root))
        self.assertEqual((1, []), (n, fails))
        self.assertFalse(pc.exists())

    def test_purge_helper_missing_base_ok(self):
        n, fails = cc.purge_c3tmp_pycache(str(self.root))
        self.assertEqual((0, []), (n, fails))


class TestFDoneBackwriteGuard(GitRepoCase):
    """tech#188 (R2316 anchor): the R2258 forget-shape - an F-registration
    close whose manifest misses state/queue/main.md - must be loud.
    Advisory by design: the WARN never fails the close (the done mark may
    legitimately live in an earlier commit).

    tech#209 (R2342 anchor): station-reviews joins the guard surface -
    the F-192/F-193 rounds registered finished entries without the
    station-reviews row and the ledger tail lagged two rounds until
    R2342 backfilled. Same advisory shape."""

    def _touch(self, with_queue, with_sr=False):
        fin = self.root / cc.FINISHED_LEDGER_REL
        fin.parent.mkdir(parents=True, exist_ok=True)
        fin.write_text("F-### | entry", encoding="utf-8")
        files = [cc.FINISHED_LEDGER_REL, "a.txt"]
        if with_queue:
            q = self.root / cc.QUEUE_MAIN_REL
            q.parent.mkdir(parents=True, exist_ok=True)
            q.write_text("1. item", encoding="utf-8")
            files.append(cc.QUEUE_MAIN_REL)
        if with_sr:
            sr = self.root / cc.STATION_REVIEWS_REL
            sr.parent.mkdir(parents=True, exist_ok=True)
            sr.write_text("| R### | row", encoding="utf-8")
            files.append(cc.STATION_REVIEWS_REL)
        return files

    def test_f_close_missing_queue_backwrite_warns_but_commits(self):
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(self._touch(with_queue=False), push=False)
        self.assertEqual(cc.RC_OK, rc)  # advisory: never fails the close
        self.assertTrue(any(l.startswith("WARN F-REGISTRATION")
                            and "tech#188" in l for l in lines))
        self.assertNotEqual(self.head0, self.head())  # commit still landed

    def test_f_close_missing_station_reviews_warns_but_commits(self):
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(self._touch(with_queue=True,
                                           with_sr=False), push=False)
        self.assertEqual(cc.RC_OK, rc)  # advisory: never fails the close
        self.assertTrue(any(l.startswith("WARN F-REGISTRATION-SR")
                            and "tech#209" in l for l in lines))
        self.assertFalse(any("tech#188" in l for l in lines))
        self.assertNotEqual(self.head0, self.head())  # commit still landed

    def test_f_close_with_queue_backwrite_no_warn(self):
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(self._touch(with_queue=True, with_sr=True),
                               push=False)
        self.assertEqual(cc.RC_OK, rc)
        self.assertFalse(any(l.startswith("WARN F-REGISTRATION")
                            for l in lines))
        self.assertIn(cc.QUEUE_MAIN_REL, self.head_files())
        self.assertIn(cc.STATION_REVIEWS_REL, self.head_files())

    def test_plain_close_never_warns(self):
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], push=False)
        self.assertEqual(cc.RC_OK, rc)
        self.assertFalse(any(l.startswith("WARN F-REGISTRATION")
                             for l in lines))


class TestSelfInclude(unittest.TestCase):
    """tech#81: the round's own close script rides the manifest (r1930
    anchor: that script stayed untracked across rounds because the explicit
    list never contained its own consumer)."""

    def _plain_dir(self):
        d = tempfile.mkdtemp(prefix="cc_self_")
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        return d

    def _write_state(self, root, payload):
        os.makedirs(os.path.join(root, "src", "os"), exist_ok=True)
        path = os.path.join(root, "src", "os", "state.json")
        with open(path, "w", encoding="utf-8", newline="") as f:
            json.dump(payload, f, ensure_ascii=False, indent=1)
        return path

    def _touch_script(self, root, name):
        d = os.path.join(root, ".c3-tmp")
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write("# close\n")
        return p

    def test_autodetect_found(self):
        root = self._plain_dir()
        self._write_state(root, {"tick": 41, "log": []})
        self._touch_script(root, "r41_close.py")
        self.assertEqual(".c3-tmp/r41_close.py",
                         cc.autodetect_close_script(root))

    def test_autodetect_missing_cases(self):
        root = self._plain_dir()
        # no state at all
        self.assertIsNone(cc.autodetect_close_script(root))
        # state without the script file
        self._write_state(root, {"tick": 41, "log": []})
        self.assertIsNone(cc.autodetect_close_script(root))
        # non-int tick
        self._write_state(root, {"tick": "41", "log": []})
        self.assertIsNone(cc.autodetect_close_script(root))
        # unreadable state (bad json)
        os.makedirs(os.path.join(root, "src", "os"), exist_ok=True)
        with open(os.path.join(root, "src", "os", "state.json"), "w",
                  encoding="utf-8") as f:
            f.write("{not json")
        self.assertIsNone(cc.autodetect_close_script(root))
        # script for a DIFFERENT round must not match the tick anchor
        root2 = self._plain_dir()
        self._write_state(root2, {"tick": 41, "log": []})
        self._touch_script(root2, "r40_close.py")
        self.assertIsNone(cc.autodetect_close_script(root2))


class TestSelfIncludeIntegration(GitRepoCase):
    """tech#81 end-to-end: the committed accounting contains the close
    script itself, and nothing else from .c3-tmp rides along."""

    def _seed_round(self, tick):
        os.makedirs(os.path.join(self.root, "src", "os"), exist_ok=True)
        with open(os.path.join(self.root, "src", "os", "state.json"), "w",
                  encoding="utf-8", newline="") as f:
            json.dump({"tick": tick, "log": []}, f, ensure_ascii=False, indent=1)
        d = self.root / ".c3-tmp"
        d.mkdir(exist_ok=True)
        (d / ("r%d_close.py" % tick)).write_text("# close\n", encoding="utf-8")

    def test_close_script_rides_manifest(self):
        self._seed_round(41)
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], push=False)
        self.assertEqual(cc.RC_OK, rc)
        self.assertTrue(any(
            l == "STEP self-include .c3-tmp/r41_close.py (tech#81)" for l in lines))
        heads = self.head_files()
        self.assertIn("a.txt", heads)
        self.assertIn(".c3-tmp/r41_close.py", heads)
        # r1930 anchor lock: no untracked close script lingers past the close
        rc, out, _ = self._git(["status", "--porcelain", "--", ".c3-tmp"])
        self.assertEqual("", out)

    def test_already_listed_no_duplicate(self):
        self._seed_round(41)
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(
            ["a.txt", ".c3-tmp/r41_close.py"], push=False)
        self.assertEqual(cc.RC_OK, rc)
        self.assertTrue(any("already listed" in l for l in lines))
        self.assertFalse(any("STEP self-include" in l for l in lines))
        heads = self.head_files()
        self.assertEqual(1, heads.count(".c3-tmp/r41_close.py"))

    def test_wrong_round_leftover_not_swept(self):
        os.makedirs(os.path.join(self.root, "src", "os"), exist_ok=True)
        with open(os.path.join(self.root, "src", "os", "state.json"), "w",
                  encoding="utf-8", newline="") as f:
            json.dump({"tick": 41, "log": []}, f, ensure_ascii=False, indent=1)
        (self.root / ".c3-tmp").mkdir(exist_ok=True)
        (self.root / ".c3-tmp" / "r40_close.py").write_text(
            "# stale leftover\n", encoding="utf-8")
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], push=False)
        self.assertEqual(cc.RC_OK, rc)
        self.assertTrue(any("self-anchor absent" in l for l in lines))
        self.assertNotIn(".c3-tmp/r40_close.py", self.head_files())
        # strict anchor law: the older leftover stays the debris guard's case
        # (-uall: an untracked dir collapses to "?? .c3-tmp/" otherwise)
        rc, out, _ = self._git(["status", "--porcelain", "--untracked-files=all",
                                "--", ".c3-tmp"])
        self.assertIn("r40_close.py", out)

    def test_dry_run_plan_shows_self_include(self):
        self._seed_round(41)
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], dry_run=True)
        self.assertEqual(cc.RC_OK, rc)
        self.assertTrue(any(
            l.startswith("DRY-RUN git add") and ".c3-tmp/r41_close.py" in l
            for l in lines))

    def test_gitignored_close_script_retired(self):
        # tech#157 born-fix: a .gitignore line covering .c3-tmp/ retires
        # the tech#81 self-include - an ignored close script must NOT ride
        # the manifest (git add of an ignored path would fail the close).
        self._seed_round(41)
        (self.root / ".gitignore").write_text(".c3-tmp/\n", encoding="utf-8")
        self.assertIsNone(cc.autodetect_close_script(str(self.root)))
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], push=False)
        self.assertEqual(cc.RC_OK, rc)
        self.assertFalse(any("STEP self-include" in l for l in lines))
        heads = self.head_files()
        self.assertIn("a.txt", heads)
        self.assertNotIn(".c3-tmp/r41_close.py", heads)
        # ignored + still on disk = invisible to routine status (cleanup
        # hook owns the disk deletion, never the close commit)
        rc, out, _ = self._git(["status", "--porcelain", "--", ".c3-tmp"])
        self.assertEqual("", out)


class TestCLI(unittest.TestCase):
    """The main() face the close script shell-outs to (rc propagation)."""




    def test_cli_rc_propagates(self):
        repo = GitRepo()
        try:
            rc = cc.main(["--files", "a.txt", "--message", "cli close [via bm-a]",
                          "--root", str(repo.root), "--no-push"])
            self.assertEqual(cc.RC_GIT, rc)  # unchanged file = loud nothing-to-commit
            (repo.root / "a.txt").write_text("changed", encoding="utf-8")
            rc = cc.main(["--files", "a.txt", "--message", "cli close [via bm-a]",
                          "--root", str(repo.root), "--no-push"])
            self.assertEqual(cc.RC_OK, rc)
            self.assertIn("a.txt", repo.head_files())
        finally:
            repo.destroy()


class StateFixture(object):
    """Plain fixture (not a TestCase): a minimal state.json in a temp dir.

    Mirrors the real ledger's field set (tick/log/ts/task/focus/production
    + decisions_watermark) so preservation and round-trip locks are
    meaningful.
    """

    def __init__(self):
        self.dir = tempfile.mkdtemp(prefix="finalize_state_")
        self.path = os.path.join(self.dir, "state.json")
        state = {
            "tick": 1926,
            "log": ["2026-10-10 23:5x R1926: seed round"],
            "ts": "2026-10-10 23:57:00",
            "task": "seed task",
            "focus": "seed focus",
            "production": "open",
            "decisions_watermark": {"dnums": ["D-20261010-03"], "board_rows": 28},
        }
        with open(self.path, "w", encoding="utf-8", newline="") as f:
            json.dump(state, f, ensure_ascii=False, indent=1)

    def destroy(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def read(self):
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)

    def raw_bytes(self):
        with open(self.path, "rb") as f:
            return f.read()


class TestDeriveTask(unittest.TestCase):
    """tech#76: task derivation + the born-level prefix gate."""

    def test_basic_prefix_stripped(self):
        self.assertEqual("hello world",
                         cc.derive_task("2026-10-11 00:1x R1927: hello world"))
        self.assertEqual("plain minute too",
                         cc.derive_task("2026-10-10 23:26 R1924: plain minute too"))

    def test_x_minute_and_sixty_char_cap(self):
        body = "等待轮·五查全静" * 20  # CJK body well past the cap
        line = "2026-10-10 23:5x R1926: " + body
        self.assertEqual(body[:cc.TASK_MAX_CHARS], cc.derive_task(line))

    def test_rejects_bad_shapes(self):
        for bad in (
            "no prefix at all",
            "2026-10-10 235x R1926: missing colon",
            "2026-10-10 23:xx R1926: letters in minute",
            "2026-10-10 23:5x 1926: missing R tag",
            "2026/10/10 23:5x R1926: wrong date separators",
            "",
        ):
            with self.assertRaises(ValueError):
                cc.derive_task(bad)


class TestFinalizeState(unittest.TestCase):
    """tech#76: the single-writer state accounting step (R1920 anchor)."""

    LINE = "2026-10-11 00:1x R1927: 等待轮·tech#76 交付轮"

    def _fx(self):
        fx = StateFixture()
        self.addCleanup(fx.destroy)
        return fx

    def test_happy_auto_tick_and_fields(self):
        fx = self._fx()
        summary = cc.finalize_state(self.LINE, focus="next round focus",
                                    state_path=fx.path)
        self.assertEqual(1927, summary["tick"])
        d = fx.read()
        self.assertEqual(1927, d["tick"])
        self.assertEqual(self.LINE, d["log"][-1])
        self.assertEqual("等待轮·tech#76 交付轮", d["task"])
        self.assertEqual("next round focus", d["focus"])
        # unrelated fields preserved by the round-trip
        self.assertEqual("open", d["production"])
        self.assertEqual("seed round", d["log"][0][len("2026-10-10 23:5x R1926: "):])
        # atomic write: no temp residue, no BOM (house format)
        self.assertFalse(os.path.exists(fx.path + ".tmp_final"))
        self.assertFalse(fx.raw_bytes().startswith(b"\xef\xbb\xbf"))

    def test_focus_none_leaves_untouched(self):
        fx = self._fx()
        cc.finalize_state(self.LINE, state_path=fx.path)
        self.assertEqual("seed focus", fx.read()["focus"])

    def test_tick_guard_explicit_and_mismatch(self):
        fx = self._fx()
        cc.finalize_state(self.LINE, tick=1927, state_path=fx.path)
        self.assertEqual(1927, fx.read()["tick"])
        # a re-run with a stale tick must be loud and touch nothing
        before = fx.raw_bytes()
        with self.assertRaises(ValueError):
            cc.finalize_state(self.LINE, tick=1927, state_path=fx.path)
        self.assertEqual(before, fx.raw_bytes())

    def test_ts_default_uses_injected_clock(self):
        fx = self._fx()
        fixed = datetime.datetime(2026, 10, 11, 0, 20, 33)
        summary = cc.finalize_state(self.LINE, state_path=fx.path, now=fixed)
        self.assertEqual("2026-10-11 00:20:33", summary["ts"])
        self.assertEqual(summary["ts"], fx.read()["ts"])

    def test_ts_bad_shape_rejected_before_write(self):
        fx = self._fx()
        before = fx.raw_bytes()
        with self.assertRaises(ValueError):
            cc.finalize_state(self.LINE, ts="2026-10-11 00:20", state_path=fx.path)
        self.assertEqual(before, fx.raw_bytes())

    def test_watermark_add_dedup(self):
        fx = self._fx()
        summary = cc.finalize_state(self.LINE, state_path=fx.path,
                                    watermark_add=["C-20261010-04",
                                                   "D-20261010-03"])
        self.assertEqual(1, summary["wm_added"])  # D-20261010-03 deduped
        dnums = fx.read()["decisions_watermark"]["dnums"]
        self.assertEqual(["D-20261010-03", "C-20261010-04"], dnums)
        # board_rows sibling key preserved
        self.assertEqual(28, fx.read()["decisions_watermark"]["board_rows"])

    def test_verbatim_no_substitution_r1920_anchor(self):
        """The R1920 failure class: a '@TS'-looking token in the payload.

        This API has no substitution step, so the token lands verbatim -
        visible in the ledger and in the summary lengths, never silently
        half-replaced. The defect was never the token; it was the
        external-template substitution pattern, banned here by design.
        """
        fx = self._fx()
        line = "2026-10-11 00:1x R1927: body with @TS token and @BigStream tag"
        cc.finalize_state(line, state_path=fx.path)
        self.assertEqual(line, fx.read()["log"][-1])

    def test_rejects_bad_log_line_and_non_list_log(self):
        fx = self._fx()
        before = fx.raw_bytes()
        with self.assertRaises(ValueError):
            cc.finalize_state("2026-10-11 garbage", state_path=fx.path)
        with self.assertRaises(ValueError):
            cc.finalize_state("", state_path=fx.path)
        d = fx.read()
        d["log"] = "not a list"
        with open(fx.path, "w", encoding="utf-8", newline="") as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        mid = fx.raw_bytes()
        with self.assertRaises(ValueError):
            cc.finalize_state(self.LINE, state_path=fx.path)
        self.assertEqual(mid, fx.raw_bytes())  # writer touched nothing

    def test_orders_watermark_stored(self):
        # tech#103: consumption anchor flows through the single writer.
        fx = self._fx()
        summary = cc.finalize_state(
            self.LINE, state_path=fx.path,
            orders_watermark={"rows": 1412, "tail_key": "10-11 13:4x"})
        self.assertEqual(1412, summary["orders_wm_rows"])
        self.assertEqual({"rows": 1412, "tail_key": "10-11 13:4x"},
                         fx.read()["orders_row_watermark"])
        # unrelated fields preserved by the round-trip
        self.assertEqual(28, fx.read()["decisions_watermark"]["board_rows"])

    def test_orders_watermark_bad_shape_rejected_before_write(self):
        fx = self._fx()
        before = fx.raw_bytes()
        bad_shapes = (
            {"rows": 0, "tail_key": "x"},      # rows must be >= 1
            {"rows": -3, "tail_key": "x"},    # negative
            {"rows": "12", "tail_key": "x"},  # rows not an int
            {"rows": 12, "tail_key": "  "},   # empty/blank tail_key
            {"rows": 12, "tail_key": 5},      # tail_key not a str
            {"rows": 12},                     # missing tail_key
            [12, "x"],                        # not a dict
            "1412",                           # scalar
        )
        for bad in bad_shapes:
            with self.assertRaises(ValueError):
                cc.finalize_state(self.LINE, state_path=fx.path,
                                  orders_watermark=bad)
        self.assertEqual(before, fx.raw_bytes())  # zero partial writes

    def test_orders_watermark_none_leaves_field_untouched(self):
        fx = self._fx()
        summary = cc.finalize_state(self.LINE, state_path=fx.path)
        self.assertIsNone(summary["orders_wm_rows"])
        self.assertNotIn("orders_row_watermark", fx.read())


class TestFClaimLedgerAdvisory(unittest.TestCase):
    """tech#211 (R2346 anchor): log-line F-claim vs finished-ledger
    presence, advisory-only.

    R2346 anchor reproduction: that round's log line claimed "F-195 登记"
    while output/finished.md did not carry the row yet (it landed next
    round) - a premature claim read as done for a full round. The guard
    WARNs into the close evidence face at write time; it never fails the
    accounting close.
    """

    LINE_TMPL = "2026-10-18 09:4x R1927: 实活轮·%s·tech#211 收账"

    def _fx(self):
        fx = StateFixture()
        self.addCleanup(fx.destroy)
        return fx

    def _ledger(self, fx, rows):
        path = os.path.join(fx.dir, "finished.md")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("\n".join(rows))
        return path

    def test_premature_claim_warns_but_write_lands(self):
        fx = self._fx()
        ledger = self._ledger(fx, ["## 成品库", "F-195 城市速报 025"])
        line = self.LINE_TMPL % "收官链 F-205 登记·台账落位"
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            summary = cc.finalize_state(
                line, state_path=fx.path, finished_ledger_path=ledger)
        self.assertEqual(["F-205"], summary["f_claims_missing"])
        self.assertIn("WARN F-CLAIM-NOT-IN-LEDGER F-205", buf.getvalue())
        self.assertIn("output/finished.md", buf.getvalue())
        # advisory never fails the close: the ledger write still landed
        d = fx.read()
        self.assertEqual(line, d["log"][-1])
        self.assertEqual(1927, d["tick"])

    def test_claim_present_no_warn(self):
        fx = self._fx()
        ledger = self._ledger(fx, ["F-195 城市盘点 025"])
        line = self.LINE_TMPL % "收官链 F-195 登记·台账落位"
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            summary = cc.finalize_state(
                line, state_path=fx.path, finished_ledger_path=ledger)
        self.assertEqual([], summary["f_claims_missing"])
        self.assertNotIn("WARN F-CLAIM-NOT-IN-LEDGER", buf.getvalue())

    def test_reference_mentions_stay_out_of_trigger(self):
        # "F-196·登记轮核验" and "F-195 归档" are references, not claims
        fx = self._fx()
        ledger = self._ledger(fx, [])
        line = self.LINE_TMPL % "候选 F-196·登记轮核验·F-195 归档注记"
        summary = cc.finalize_state(
            line, state_path=fx.path, finished_ledger_path=ledger)
        self.assertEqual([], summary["f_claims_missing"])

    def test_plain_line_and_missing_ledger_zero_noise(self):
        fx = self._fx()
        # no F-claim in the line; an explicit ledger path that does not
        # exist skips the check (best-effort, zero noise)
        summary = cc.finalize_state(
            self.LINE_TMPL % "声明轮·五查全静",
            state_path=fx.path,
            finished_ledger_path=os.path.join(fx.dir, "no-such-ledger.md"))
        self.assertEqual([], summary["f_claims_missing"])
        # derived default path from a fixture dir points nowhere: skip
        # (fresh fixture: the R==tick born gate counts every finalize)
        fx2 = self._fx()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            summary2 = cc.finalize_state(
                self.LINE_TMPL % "声明轮·五查全静·二连", state_path=fx2.path)
        self.assertEqual([], summary2["f_claims_missing"])
        self.assertNotIn("WARN F-CLAIM-NOT-IN-LEDGER", buf.getvalue())


class TestLogPrefixBackwardAdvisory(unittest.TestCase):
    """tech#214 (R2351 anchor): write-time narrative ts order advisory.

    R2349 wrote prefix "09:5x" while its successor R2350 wrote "09:2x" -
    the round number advanced but the narrative clock went backwards,
    and loop_health only surfaced it one probe cycle later (log-order
    WARN). finalize_state now WARNs into the close evidence face at
    write time; advisory-only, never fails the accounting close.
    """

    def _fx(self):
        fx = StateFixture()
        self.addCleanup(fx.destroy)
        return fx

    def test_backward_prefix_warns_but_write_lands(self):
        # the R2351 real shape: last line 23:5x, new line 23:2x
        fx = self._fx()
        line = "2026-10-10 23:2x R1927: 收官轮·倒退位实证·tech#214 收账"
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            summary = cc.finalize_state(line, state_path=fx.path)
        self.assertTrue(summary["prefix_backward"])
        self.assertIn("WARN LOG-PREFIX-BACKWARD 2026-10-10 23:2x after "
                      "2026-10-10 23:5x", buf.getvalue())
        # advisory never fails the close: the ledger write still landed
        d = fx.read()
        self.assertEqual(line, d["log"][-1])
        self.assertEqual(1927, d["tick"])

    def test_forward_prefix_no_warn(self):
        fx = self._fx()
        line = "2026-10-11 00:1x R1927: 等待轮·tech#214 前进位对照"
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            summary = cc.finalize_state(line, state_path=fx.path)
        self.assertFalse(summary["prefix_backward"])
        self.assertNotIn("WARN LOG-PREFIX-BACKWARD", buf.getvalue())
        # the write landed
        self.assertEqual(line, fx.read()["log"][-1])

    def test_empty_log_zero_noise(self):
        # no last line to compare against: advisory stays silent
        d = tempfile.mkdtemp(prefix="pfx_back_")
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        sp = os.path.join(d, "state.json")
        with open(sp, "w", encoding="utf-8", newline="") as f:
            json.dump({"tick": 1926, "log": [],
                       "ts": "2026-10-10 23:57:00", "task": "t"},
                      f, ensure_ascii=False, indent=1)
        line = "2026-10-10 23:2x R1927: 首笔位·零对照面"
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            summary = cc.finalize_state(line, state_path=sp)
        self.assertFalse(summary["prefix_backward"])
        self.assertNotIn("WARN LOG-PREFIX-BACKWARD", buf.getvalue())

    def test_malformed_last_line_zero_noise(self):
        # a legacy/history line without the prefix shape is the probe's
        # business - the writer never WARNs on unreadable history
        fx = self._fx()
        d = fx.read()
        d["log"] = ["legacy narrative line without prefix"]
        with open(fx.path, "w", encoding="utf-8", newline="") as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        line = "2026-10-10 23:2x R1927: 历史位不可读·零噪声实证"
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            summary = cc.finalize_state(line, state_path=fx.path)
        self.assertFalse(summary["prefix_backward"])
        self.assertNotIn("WARN LOG-PREFIX-BACKWARD", buf.getvalue())
        # and the malformed history line itself still landed intact
        self.assertEqual(2, len(fx.read()["log"]))


class TestRoundNumberInvariant(unittest.TestCase):
    """tech#196 (R2329 anchor): the R==new-tick born gate.

    One body self-derived round number R2334 while its real tick was
    2328, breaking the historical R==tick arithmetic chain and tripping
    loop_health's unaccounted-round-work WARN for a ~12-commit window.
    finalize_state now refuses any line whose R number will not equal
    the new tick - loud, zero partial writes, before any mutation.
    """

    def _state(self, tick):
        d = tempfile.mkdtemp(prefix="r_number_")
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        sp = os.path.join(d, "state.json")
        with open(sp, "w", encoding="utf-8", newline="") as f:
            json.dump({"tick": tick, "log": [],
                       "ts": "2026-10-17 13:30:00", "task": "t"},
                      f, ensure_ascii=False, indent=1)
        with open(sp, "rb") as f:
            return sp, f.read()

    def test_r2334_anchor_reproduction_refused_zero_write(self):
        # the R2329 anchor: on-disk tick 2327, the line claims R2334
        sp, before = self._state(2327)
        with self.assertRaises(ValueError) as cm:
            cc.finalize_state(
                "2026-10-17 14:2x R2334: mislabeled body round",
                state_path=sp)
        self.assertIn("round-number invariant", str(cm.exception))
        self.assertIn("R2328", str(cm.exception))  # relabel hint
        with open(sp, "rb") as f:
            self.assertEqual(before, f.read())  # zero partial writes

    def test_correct_round_number_passes(self):
        sp, _ = self._state(2327)
        summary = cc.finalize_state(
            "2026-10-17 14:2x R2328: correctly labeled round",
            state_path=sp)
        self.assertEqual(2328, summary["tick"])

    def test_gate_covers_explicit_tick_path(self):
        # an explicit tick passes the tick guard, then the R gate still
        # bites on a mismatched round number (both directions)
        sp, before = self._state(2327)
        with self.assertRaises(ValueError):
            cc.finalize_state("2026-10-17 14:2x R2334: wrong with tick",
                              tick=2328, state_path=sp)
        with open(sp, "rb") as f:
            self.assertEqual(before, f.read())
        cc.finalize_state("2026-10-17 14:2x R2328: aligned with tick",
                          tick=2328, state_path=sp)

    def test_derive_round_number_helper(self):
        self.assertEqual(2334, cc.derive_round_number(
            "2026-10-17 14:2x R2334: body"))
        self.assertEqual(7, cc.derive_round_number(
            "2026-10-10 23:5x R7: short numbers allowed"))
        with self.assertRaises(ValueError):
            cc.derive_round_number("2026-10-17 no prefix")


class TestPulseStateBeat(unittest.TestCase):
    """PT-20261015-01 (R2308): pulse-only state beat - defer-window
    freshness touch with ZERO accounting mutation (tech#149 stays whole:
    finalize_state remains the one accounting writer)."""

    def _fx(self):
        fx = StateFixture()
        self.addCleanup(fx.destroy)
        return fx

    def test_pulse_touches_ts_and_marker_only(self):
        fx = self._fx()
        fixed = datetime.datetime(2026, 10, 15, 22, 40, 0)
        summary = cc.pulse_state_beat("cloud-cap defer (live=2)",
                                     state_path=fx.path, now=fixed)
        self.assertEqual("2026-10-15 22:40:00", summary["ts"])
        self.assertEqual("cloud-cap defer (live=2)", summary["reason"])
        d = fx.read()
        self.assertEqual("2026-10-15 22:40:00", d["ts"])
        self.assertEqual("cloud-cap defer (live=2)", d["pulse"]["reason"])
        # accounting face untouched: tick/log/task/focus/production
        self.assertEqual(1926, d["tick"])
        self.assertEqual(1, len(d["log"]))
        self.assertEqual("seed task", d["task"])
        self.assertEqual("seed focus", d["focus"])
        self.assertEqual("open", d["production"])
        # option 2 declaration: static beat policy block written once
        self.assertTrue(summary["policy_written"])
        # tech#219 lock: v2 thresholds (250/240 hard cap + 25min silence
        # gate) and the rebuilt block == code canonical BEAT_POLICY dict,
        # so a rebuild can never regress to retired 35min semantics.
        self.assertEqual(250, d["beat"]["active_gap_max_min"])
        self.assertIn("silence gate", d["beat"]["active_semantics"])
        self.assertIn("240min hard cap", d["beat"]["active_semantics"])
        self.assertEqual(cc.BEAT_POLICY, d["beat"])
        self.assertIn("d13_pointer", d["beat"])
        # atomic write house format: no temp residue, no BOM
        self.assertFalse(os.path.exists(fx.path + ".tmp_pulse"))
        self.assertFalse(fx.raw_bytes().startswith(b"\xef\xbb\xbf"))

    def test_policy_block_written_once_never_overwritten(self):
        fx = self._fx()
        cc.pulse_state_beat("first", state_path=fx.path,
                            now=datetime.datetime(2026, 10, 15, 22, 40, 0))
        d = fx.read()
        d["beat"]["note"] = "hand-tuned"
        with open(fx.path, "w", encoding="utf-8", newline="") as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        summary = cc.pulse_state_beat("second", state_path=fx.path,
                                      now=datetime.datetime(2026, 10, 15,
                                                            22, 50, 0))
        d2 = fx.read()
        self.assertFalse(summary["policy_written"])
        self.assertEqual("hand-tuned", d2["beat"]["note"])
        self.assertEqual("second", d2["pulse"]["reason"])

    def test_pulse_after_finalize_preserves_accounting(self):
        # the designed interleaving: pulse (defer) -> real round close
        # (finalize) -> pulse again - accounting survives the round trip.
        fx = self._fx()
        cc.pulse_state_beat("defer pulse", state_path=fx.path,
                            now=datetime.datetime(2026, 10, 15, 22, 40, 0))
        # ts injected: finalize must not read the live clock, or this test
        # goes red for every real-world run after 2026-10-15 23:00 (the
        # frozen pulse clock below would read as clock-skew backwards).
        cc.finalize_state("2026-10-15 22:5x R1927: close after pulse",
                          state_path=fx.path,
                          ts="2026-10-15 22:50:00")
        cc.pulse_state_beat("defer pulse 2", state_path=fx.path,
                            now=datetime.datetime(2026, 10, 15, 23, 0, 0))
        d = fx.read()
        self.assertEqual(1927, d["tick"])
        self.assertEqual("2026-10-15 23:00:00", d["ts"])
        self.assertEqual(2, len(d["log"]))
        self.assertIn("close after pulse", d["log"][-1])
        self.assertEqual("defer pulse 2", d["pulse"]["reason"])

    def test_refuses_empty_reason_and_clamps_long(self):
        fx = self._fx()
        before = fx.raw_bytes()
        with self.assertRaises(ValueError):
            cc.pulse_state_beat("   ", state_path=fx.path)
        self.assertEqual(before, fx.raw_bytes())
        summary = cc.pulse_state_beat("r" * 200, state_path=fx.path,
                                      now=datetime.datetime(2026, 10, 15,
                                                            22, 40, 0))
        self.assertEqual(cc.PULSE_REASON_MAX, len(summary["reason"]))

    def test_refuses_clock_skew_backwards(self):
        # fixture ts = 2026-10-10 23:57:00; an older/equal pulse clock
        # must refuse and touch nothing (a pulse never moves ts back).
        fx = self._fx()
        before = fx.raw_bytes()
        for skewed in (datetime.datetime(2026, 10, 10, 23, 0, 0),
                       datetime.datetime(2026, 10, 10, 23, 57, 0)):
            with self.assertRaises(ValueError):
                cc.pulse_state_beat("skewed", state_path=fx.path,
                                    now=skewed)
        self.assertEqual(before, fx.raw_bytes())
        self.assertNotIn("pulse", fx.read())

    def test_refuses_broken_ts_face(self):
        fx = self._fx()
        d = fx.read()
        d["ts"] = "not-a-ts"
        with open(fx.path, "w", encoding="utf-8", newline="") as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        before = fx.raw_bytes()
        with self.assertRaises(ValueError):
            cc.pulse_state_beat("x", state_path=fx.path,
                                now=datetime.datetime(2026, 10, 15, 22, 40, 0))
        self.assertEqual(before, fx.raw_bytes())

    def test_cli_pulse_mode(self):
        fx = self._fx()
        rc = cc.main(["--pulse", "cloud-cap defer (live=3)",
                      "--state-path", fx.path])
        self.assertEqual(cc.RC_OK, rc)
        self.assertEqual("cloud-cap defer (live=3)",
                         fx.read()["pulse"]["reason"])
        # legacy contract preserved: neither mode -> loud usage error
        rc = cc.main([])
        self.assertEqual(cc.RC_USAGE, rc)
        # non-ASCII pulse reason is a loud usage error (encoding rule)
        rc = cc.main(["--pulse", "\u5e26\u4e2d", "--state-path", fx.path])
        self.assertEqual(cc.RC_USAGE, rc)
        # a refused pulse (clock skew against the real clock) is loud
        rc = cc.main(["--pulse", "skewed-older", "--state-path", fx.path])
        # fixture ts is 2026-10-10; real clock is newer, so this pulse
        # passes - instead prove the refusal path via a fresh fixture
        # whose ts is set into the future relative to the real clock
        fx2 = StateFixture()
        self.addCleanup(fx2.destroy)
        d = fx2.read()
        d["ts"] = "2099-01-01 00:00:00"
        with open(fx2.path, "w", encoding="utf-8", newline="") as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        rc = cc.main(["--pulse", "future-face", "--state-path", fx2.path])
        self.assertEqual(cc.RC_USAGE, rc)
        self.assertNotIn("pulse", fx2.read())


def clean_export_body():
    """Minimal contract-clean export body (mirrors the tech#70 writer's
    test fixture; export_ts is writer-owned)."""
    return {
        "do": "one line current activity",
        "outs": [["kept item", "on", "tag"]],
        "chips": [["kept chip", "live"]],
        "results": [["42", "kept readout"]],
        "live": ["live a", "live b", "live c"],
    }


class TestExportIntegration(GitRepoCase):
    """tech#148 (R2124 relapse anchor): the close refreshes
    docs/status-export.json THROUGH the canonical writer - never a
    hand-rolled json.dump - and the refreshed export rides the accounting
    commit manifest automatically. Writer refusal is warn-only."""

    EXPORT_REL = os.path.join("docs", "status-export.json")

    def setUp(self):
        GitRepoCase.setUp(self)
        (self.root / "docs").mkdir()
        (self.root / self.EXPORT_REL).write_text(
            json.dumps(clean_export_body(), ensure_ascii=False, indent=1)
            + "\n", encoding="utf-8")

    def _export(self):
        return json.loads(
            (self.root / self.EXPORT_REL).read_text(encoding="utf-8"))

    def test_refresh_via_writer_rides_manifest(self):
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], push=False,
                               export_do="r2127 close do line")
        self.assertEqual(cc.RC_OK, rc, lines)
        self.assertTrue(any("rides manifest" in l for l in lines), lines)
        data = self._export()
        self.assertEqual(data["do"], "r2127 close do line")
        # live-clock law: export_ts is writer-stamped, second-precision ASCII
        self.assertRegex(data["export_ts"],
                         r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
        # unlisted keys carry over (incremental law through the close path)
        self.assertEqual(data["results"], [["42", "kept readout"]])
        # refreshed export rides the same accounting commit
        head = self.head_files()
        self.assertIn("a.txt", head)
        self.assertIn("docs/status-export.json", head)

    def test_patch_dict_through_close_updates_only_patched(self):
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], push=False,
                               export_patch={"results": [["99", "new readout"]]})
        self.assertEqual(cc.RC_OK, rc, lines)
        data = self._export()
        self.assertEqual(data["results"], [["99", "new readout"]])
        self.assertEqual(data["do"], "one line current activity")
        self.assertIn("docs/status-export.json", self.head_files())

    def test_refused_patch_export_intact_close_still_commits(self):
        """The R2124 defect class, replayed: a payload the writer must
        refuse (export_ts smuggling) never lands; the accounting commit
        is unaffected (warn-only law)."""
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        before = (self.root / self.EXPORT_REL).read_bytes()
        rc, lines = self.close(["a.txt"], push=False,
                               export_patch={"export_ts":
                                             "1999-01-01 00:00:00"})
        self.assertEqual(cc.RC_OK, rc, lines)  # warn-only, close lands
        self.assertTrue(any("WARN EXPORT-REFUSED" in l for l in lines),
                       lines)
        self.assertTrue(any("writer-owned" in l for l in lines), lines)
        self.assertEqual(before, (self.root / self.EXPORT_REL).read_bytes())
        self.assertEqual(["a.txt"], self.head_files())  # no export in manifest

    def test_no_export_params_zero_side_effects(self):
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], push=False)
        self.assertEqual(cc.RC_OK, rc, lines)
        self.assertEqual(["a.txt"], self.head_files())
        self.assertEqual(self._export()["do"], "one line current activity")

    def test_dry_run_writes_nothing(self):
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        before = (self.root / self.EXPORT_REL).read_bytes()
        rc, lines = self.close(["a.txt"], push=False, dry_run=True,
                               export_do="dry-run do")
        self.assertEqual(cc.RC_OK, rc, lines)
        self.assertTrue(any("DRY-RUN contract clean" in l for l in lines),
                       lines)
        self.assertEqual(before, (self.root / self.EXPORT_REL).read_bytes())
        self.assertEqual(self.head0, self.head())

    def test_export_already_in_manifest_not_duplicated(self):
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rel = self.EXPORT_REL.replace(os.sep, "/")
        rc, lines = self.close(["a.txt", rel], push=False,
                               export_do="explicit listing")
        self.assertEqual(cc.RC_OK, rc, lines)
        # manifest dedup: the export appears exactly once in the commit
        self.assertEqual(self.head_files().count(rel), 1)
        self.assertEqual(self.head_files().count("a.txt"), 1)

    def test_refuse_alias_pinned_to_writer_constant(self):
        import export_refresh
        self.assertEqual(cc.RC_WRITER_REFUSE, export_refresh.RC_REFUSE)


class VerifyStateRepoCase(unittest.TestCase, GitRepo):
    """tech#155 fixture: GitRepo + src/os/state.json under test control.

    The state ledger rides the repo but is deliberately NOT part of the
    committed manifest in these tests - the readback verifies what the
    DISK carries, not what the commit contains."""

    def setUp(self):
        GitRepo.__init__(self)
        os.makedirs(self.root / "src" / "os", exist_ok=True)
        self.state_path = self.root / "src" / "os" / "state.json"
        self.write_state(2213)

    def tearDown(self):
        self.destroy()

    def write_state(self, tick):
        self.state_path.write_text(
            json.dumps({"tick": tick}, ensure_ascii=True), encoding="utf-8")

    def read_state(self):
        return json.loads(self.state_path.read_text(encoding="utf-8"))

    def close(self, files, message=MSG, **kw):
        return cc.run_close_commit(files, message, root=str(self.root), **kw)


class TestVerifyStateTickHelpers(unittest.TestCase):
    """tech#155 face 2: the verify helper locks both readback states."""

    def test_ok_line(self):
        d = Path(tempfile.mkdtemp(prefix="verify_tick_"))
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        sp = d / "state.json"
        sp.write_text(json.dumps({"tick": 2214}), encoding="utf-8")
        ok, line = cc.verify_state_tick(2214, state_path=str(sp))
        self.assertTrue(ok)
        self.assertEqual(line, "VERIFY-OK state tick=2214 (readback)")

    def test_fail_line_names_expected_and_anchor(self):
        d = Path(tempfile.mkdtemp(prefix="verify_tick_"))
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        sp = d / "state.json"
        sp.write_text(json.dumps({"tick": 2213}), encoding="utf-8")
        ok, line = cc.verify_state_tick(2214, state_path=str(sp))
        self.assertFalse(ok)
        self.assertIn("VERIFY-FAIL state tick=2213 expected 2214", line)
        self.assertIn("R2214 anchor", line)

    def test_unreadable_ledger_fails_loud(self):
        ok, line = cc.verify_state_tick(
            2214, state_path=str(Path(tempfile.mkdtemp()) / "gone.json"))
        self.assertFalse(ok)
        self.assertIn("VERIFY-FAIL", line)
        self.assertIn("unreadable", line)

    def test_bad_expect_shape_is_usage_line(self):
        for bad in ("2214", 1.5, True, -1):
            ok, line = cc.verify_state_tick(bad)
            self.assertFalse(ok)
            self.assertTrue(line.startswith("USAGE-ERROR"), line)

    def test_read_disk_tick_missing_and_malformed(self):
        self.assertIsNone(cc.read_disk_state_tick(
            state_path=str(Path(tempfile.mkdtemp()) / "gone.json")))
        d = Path(tempfile.mkdtemp(prefix="verify_tick_"))
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        sp = d / "state.json"
        sp.write_text("not json", encoding="utf-8")
        self.assertIsNone(cc.read_disk_state_tick(state_path=str(sp)))
        sp.write_text(json.dumps({"tick": "x"}), encoding="utf-8")
        self.assertIsNone(cc.read_disk_state_tick(state_path=str(sp)))


class TestVerifyStateTickInClose(VerifyStateRepoCase):
    """tech#155 face 2 through run_close_commit: dual-state lock
    (consistent -> VERIFY-OK / mismatch -> loud VERIFY-FAIL + rc 3)
    plus the legacy-surface zero-regression contract (expect_tick=None
    changes nothing)."""

    def test_verify_ok_after_commit(self):
        self.write_state(2214)  # the round's finalize already ran
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], push=False, expect_tick=2214)
        self.assertEqual(cc.RC_OK, rc, lines)
        self.assertTrue(any(l.startswith("VERIFY-OK state tick=2214") 
                            for l in lines), lines)
        self.assertNotEqual(self.head0, self.head())  # commit landed

    def test_verify_fail_rc3_commit_still_landed(self):
        # the R2214 anchor shape: finalize never ran, the ledger still
        # carries the old tick while the round's work commit lands -
        # loud VERIFY-FAIL, rc 3, commit NOT rolled back (real work)
        self.write_state(2213)
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], push=False, expect_tick=2214)
        self.assertEqual(cc.RC_VERIFY, rc, lines)
        self.assertEqual(rc, 3)
        self.assertTrue(any(l.startswith("VERIFY-FAIL state tick=2213 "
                                         "expected 2214") for l in lines),
                         lines)
        self.assertNotEqual(self.head0, self.head())  # commit stays landed
        self.assertEqual(self.read_state()["tick"], 2213)  # ledger untouched

    def test_legacy_surface_no_expect_unchanged(self):
        # zero-regression law: expect_tick=None -> no verify line, rc 0
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], push=False)
        self.assertEqual(cc.RC_OK, rc, lines)
        self.assertFalse(any("VERIFY-" in l for l in lines), lines)
        self.assertTrue(any(l.startswith("CLOSE-COMMIT-OK") for l in lines))

    def test_bad_expect_type_usage_before_git(self):
        # a non-int expect_tick is a loud usage error BEFORE any git call
        # (the validation block owns it; nothing lands)
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        rc, lines = self.close(["a.txt"], push=False, expect_tick="2214")
        self.assertEqual(cc.RC_USAGE, rc, lines)
        self.assertTrue(any("expect_tick" in l for l in lines), lines)
        self.assertEqual(self.head0, self.head())  # zero side effects
        rc, out, _ = self._git(["status", "--porcelain"])
        self.assertIn(" M a.txt", out)  # nothing staged either


if __name__ == "__main__":
    unittest.main(verbosity=2)
