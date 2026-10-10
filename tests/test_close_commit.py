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
            "tick": 5,
            "log": ["2026-10-10 23:5x R0005: seed round"],
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
        self.assertEqual(6, summary["tick"])
        d = fx.read()
        self.assertEqual(6, d["tick"])
        self.assertEqual(self.LINE, d["log"][-1])
        self.assertEqual("等待轮·tech#76 交付轮", d["task"])
        self.assertEqual("next round focus", d["focus"])
        # unrelated fields preserved by the round-trip
        self.assertEqual("open", d["production"])
        self.assertEqual("seed round", d["log"][0][len("2026-10-10 23:5x R0005: "):])
        # atomic write: no temp residue, no BOM (house format)
        self.assertFalse(os.path.exists(fx.path + ".tmp_final"))
        self.assertFalse(fx.raw_bytes().startswith(b"\xef\xbb\xbf"))

    def test_focus_none_leaves_untouched(self):
        fx = self._fx()
        cc.finalize_state(self.LINE, state_path=fx.path)
        self.assertEqual("seed focus", fx.read()["focus"])

    def test_tick_guard_explicit_and_mismatch(self):
        fx = self._fx()
        cc.finalize_state(self.LINE, tick=6, state_path=fx.path)
        self.assertEqual(6, fx.read()["tick"])
        # a re-run with a stale tick must be loud and touch nothing
        before = fx.raw_bytes()
        with self.assertRaises(ValueError):
            cc.finalize_state(self.LINE, tick=6, state_path=fx.path)
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
