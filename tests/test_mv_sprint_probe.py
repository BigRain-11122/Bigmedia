"""Tests for src/os/mv_sprint_probe.py (tech#84; tech#86 --ledger).

All hermetic: git is an injected seam, outbound faces are tmpdirs, the
verdict core is pure. No real repo walk, no network, no GPU. CLI tests
patch run_probe/append_ledger_row at module level (main() resolves them
as module globals).
"""

import contextlib
import datetime
import importlib.util
import io
import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "mv_sprint_probe",
    os.path.join(os.path.dirname(__file__), "..", "src", "os",
                 "mv_sprint_probe.py"),
)
probe = importlib.util.module_from_spec(_SPEC)
sys.modules["mv_sprint_probe"] = probe
_SPEC.loader.exec_module(probe)


def _face_ok(age_min, path="x.png", now=None):
    now = now or time.time()
    return {"status": "ok", "mtime": now - age_min * 60.0, "path": path}


class ParsePorcelainTests(unittest.TestCase):
    def test_plain_entries(self):
        raw = b" M data/sources/mv001/a.json\0?? data/sources/mv001/b/\0"
        self.assertEqual(probe.parse_porcelain_z_paths(raw),
                         ["data/sources/mv001/a.json", "data/sources/mv001/b/"])

    def test_rename_skips_old_field(self):
        raw = b"R  data/sources/mv001/new.json\0data/sources/mv001/old.json\0"
        self.assertEqual(probe.parse_porcelain_z_paths(raw),
                         ["data/sources/mv001/new.json"])

    def test_short_chunk_ignored(self):
        # chunks under 4 bytes (status+space+path) are garbled -> skipped;
        # a 4-byte chunk "?? a" is a legitimate 1-char-path entry
        self.assertEqual(probe.parse_porcelain_z_paths(b"??\0 M b\0X\0"), ["b"])


class FilterMvDomainTests(unittest.TestCase):
    def test_tokens_kept(self):
        paths = ["data/storylines/drama/mv0001/PRODUCTION.md",
                 "data/sources/mv001/structure.json",
                 "data/pipeline/whisper-ledger.jsonl",
                 "src/render/whisper_to_srt.py",
                 "data/storylines/drama/mv0001/full_mv_v2.py"]
        kept = probe.filter_mv_domain(paths)
        self.assertEqual(kept, [paths[0], paths[1], paths[4]])

    def test_shared_infra_never_counts(self):
        # token-free shared-infra surfaces stay excluded even though the
        # MV session writes them (ledger/noise dict discipline)
        self.assertEqual(probe.filter_mv_domain(
            ["data/pipeline/whisper-ledger.jsonl",
             "data/pipeline/asr-noise-dict-v3.json"]), [])


class RepoFaceTests(unittest.TestCase):
    def test_unreadable_on_git_failure(self):
        face = probe.collect_repo_face(
            "Z:\\no-such-root", git_runner=lambda root: (False, b""))
        self.assertEqual(face["status"], "unreadable")

    def test_empty_when_clean_tree(self):
        face = probe.collect_repo_face(
            ".", git_runner=lambda root: (True, b""))
        self.assertEqual(face["status"], "empty")

    def test_empty_when_only_non_mv_dirty(self):
        face = probe.collect_repo_face(
            ".", git_runner=lambda root: (True, b" M docs/other.md\0"))
        self.assertEqual(face["status"], "empty")

    def test_ok_picks_newest_mv_file(self):
        with tempfile.TemporaryDirectory() as td:
            old = Path(td) / "data" / "sources" / "mv001" / "old.json"
            new = Path(td) / "data" / "storylines" / "drama" / "mv0001" / "new.md"
            for p in (old, new):
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("x", encoding="utf-8")
            stamp_old = time.time() - 5000
            stamp_new = time.time() - 60
            os.utime(old, (stamp_old, stamp_old))
            os.utime(new, (stamp_new, stamp_new))
            raw = ((" M data/sources/mv001/old.json\0"
                    "?? data/storylines/drama/mv0001/new.md\0").encode())
            face = probe.collect_repo_face(td, git_runner=lambda root: (True, raw))
            self.assertEqual(face["status"], "ok")
            self.assertEqual(face["path"],
                             "data/storylines/drama/mv0001/new.md")
            self.assertAlmostEqual(face["mtime"], stamp_new, delta=2.0)

    def test_deleted_entries_do_not_crash(self):
        # stat fails (file gone between status and stat) -> other files decide
        with tempfile.TemporaryDirectory() as td:
            keep = Path(td) / "data" / "sources" / "mv001" / "keep.json"
            keep.parent.mkdir(parents=True, exist_ok=True)
            keep.write_text("x", encoding="utf-8")
            raw = (("?? data/sources/mv001/vanished.json\0"
                    "?? data/sources/mv001/keep.json\0").encode())
            face = probe.collect_repo_face(td, git_runner=lambda root: (True, raw))
            self.assertEqual(face["status"], "ok")
            self.assertEqual(face["path"], "data/sources/mv001/keep.json")


class ScanDirTests(unittest.TestCase):
    def test_newest_across_tree(self):
        with tempfile.TemporaryDirectory() as td:
            a = Path(td) / "a" / "one.png"
            b = Path(td) / "b" / "c" / "two.png"
            for p in (a, b):
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("x", encoding="utf-8")
            stamp = time.time() - 120
            os.utime(a, (stamp, stamp))
            t, p = probe.scan_dir_newest(td)
            self.assertEqual(p, os.path.join("b", "c", "two.png"))
            self.assertGreater(t, stamp)

    def test_absent_root(self):
        t, p = probe.scan_dir_newest(Path(tempfile.gettempdir()) / "no-such-bs-face")
        self.assertIsNone(t)
        self.assertIsNone(p)

    def test_empty_dir_face(self):
        with tempfile.TemporaryDirectory() as td:
            face = probe.scan_outbound_face(td)
            self.assertEqual(face["status"], "empty")


class ComputeVerdictTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime(2026, 10, 11, 3, 30, 0)
        self.now_ts = self.now.timestamp()

    def test_active_when_any_face_fresh(self):
        faces = {"repo": _face_ok(600, now=self.now_ts),
                 "mv-outbound": _face_ok(30, now=self.now_ts),
                 "h3-outbound": _face_ok(700, now=self.now_ts)}
        verdict, newest, err = probe.compute_verdict(
            faces, self.now_ts, threshold_min=90)
        self.assertEqual(verdict, "active")
        self.assertAlmostEqual(newest, 30.0)
        self.assertFalse(err)

    def test_quiet_when_all_stale(self):
        faces = {"repo": _face_ok(1390, now=self.now_ts),
                 "mv-outbound": _face_ok(230, now=self.now_ts)}
        verdict, newest, err = probe.compute_verdict(
            faces, self.now_ts, threshold_min=90)
        self.assertEqual(verdict, "quiet")
        self.assertAlmostEqual(newest, 230.0)
        self.assertFalse(err)

    def test_boundary_at_threshold_is_quiet(self):
        faces = {"repo": _face_ok(90.0, now=self.now_ts)}
        verdict, _, _ = probe.compute_verdict(
            faces, self.now_ts, threshold_min=90)
        self.assertEqual(verdict, "quiet")  # strict <

    def test_no_ok_faces_is_none(self):
        faces = {"repo": {"status": "empty"},
                 "mv-outbound": {"status": "absent"},
                 "h3-outbound": {"status": "empty"}}
        verdict, newest, err = probe.compute_verdict(
            faces, self.now_ts, threshold_min=90)
        self.assertIsNone(verdict)
        self.assertIsNone(newest)
        self.assertFalse(err)

    def test_unreadable_face_sets_error_even_when_quiet(self):
        # fail-closed: a missing reading must never read as quiet
        faces = {"repo": {"status": "unreadable"},
                 "mv-outbound": _face_ok(230, now=self.now_ts)}
        verdict, _, err = probe.compute_verdict(
            faces, self.now_ts, threshold_min=90)
        self.assertEqual(verdict, "quiet")
        self.assertTrue(err)


class RunProbeTests(unittest.TestCase):
    def _faces(self, td, age_min):
        roots = {"mv-outbound": Path(td) / "mv",
                 "h3-outbound": Path(td) / "h3"}
        for name, root in roots.items():
            root.mkdir(parents=True, exist_ok=True)
            f = root / "shot.png"
            f.write_text("x", encoding="utf-8")
            stamp = time.time() - age_min * 60
            os.utime(f, (stamp, stamp))
        return roots

    def test_rc_active_on_fresh_outbound(self):
        with tempfile.TemporaryDirectory() as td:
            roots = self._faces(td, age_min=10)
            result = probe.run_probe(
                repo_root=td, face_roots=roots, threshold_min=90,
                git_runner=lambda root: (False, b""))  # repo face unreadable
            # unreadable repo face => fail-closed rc 2 despite fresh outbound
            self.assertEqual(result["rc"], probe.RC_ERROR)

    def test_rc_quiet_on_stale_everywhere(self):
        with tempfile.TemporaryDirectory() as td:
            roots = self._faces(td, age_min=200)
            result = probe.run_probe(
                repo_root=td, face_roots=roots, threshold_min=90,
                git_runner=lambda root: (True, b""))  # repo face empty (clean)
            self.assertEqual(result["verdict"], "quiet")
            self.assertEqual(result["rc"], probe.RC_QUIET)
            self.assertAlmostEqual(result["newest_age_min"], 200.0, delta=1.0)

    def test_rc_error_when_no_face_readable(self):
        with tempfile.TemporaryDirectory() as td:
            roots = {"mv-outbound": Path(td) / "mv",  # absent
                     "h3-outbound": Path(td) / "h3"}  # absent
            result = probe.run_probe(
                repo_root=td, face_roots=roots, threshold_min=90,
                git_runner=lambda root: (True, b""))
            self.assertEqual(result["rc"], probe.RC_ERROR)
            self.assertIsNone(result["verdict"])

    def test_repo_face_fresh_flips_active(self):
        with tempfile.TemporaryDirectory() as td:
            roots = self._faces(td, age_min=400)  # outbound stale
            mv = Path(td) / "data" / "storylines" / "drama" / "mv0001" / "a.md"
            mv.parent.mkdir(parents=True, exist_ok=True)
            mv.write_text("x", encoding="utf-8")
            stamp = time.time() - 5 * 60
            os.utime(mv, (stamp, stamp))
            raw = "?? data/storylines/drama/mv0001/a.md\0".encode()
            result = probe.run_probe(
                repo_root=td, face_roots=roots, threshold_min=90,
                git_runner=lambda root: (True, raw))
            self.assertEqual(result["verdict"], "active")
            self.assertEqual(result["rc"], probe.RC_ACTIVE)


class LedgerTests(unittest.TestCase):
    """tech#86 --ledger JSONL face (tech#52 ollama_probe --ledger family:
    row fields / error-run nulls / two runs two rows / CLI wiring incl.
    bare-flag default / no-flag zero writes / best-effort failure)."""

    @staticmethod
    def _quiet_result():
        return {
            "probe": "mv_sprint_probe",
            "ts": "2026-10-11 03:33:40",
            "verdict": "quiet", "rc": probe.RC_QUIET,
            "threshold_min": 90, "newest_age_min": 247.7,
            "faces": {"repo-mv-dirty": {"status": "empty"},
                      "mv-outbound": {"status": "empty"},
                      "h3-outbound": {"status": "absent"}},
        }

    def test_row_fields_exact(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "ledger.jsonl"
            probe.append_ledger_row(str(path), self._quiet_result())
            rows = [json.loads(l) for l in
                    path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(rows), 1)
            row = rows[0]
            self.assertEqual(sorted(row.keys()),
                             ["newest_age_min", "rc", "threshold_min", "ts",
                              "verdict"])
            self.assertEqual(row["verdict"], "quiet")
            self.assertEqual(row["rc"], 0)
            self.assertEqual(row["newest_age_min"], 247.7)
            self.assertEqual(row["threshold_min"], 90)
            # ts is live-clock stamped, shape-locked only
            self.assertRegex(row["ts"], r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")

    def test_error_run_row_carries_nulls(self):
        # fail-closed is data: an rc-2 run (verdict None, newest None)
        # still gets its row so the judgment position can cite it
        result = self._quiet_result()
        result.update({"verdict": None, "rc": probe.RC_ERROR,
                       "newest_age_min": None})
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "ledger.jsonl"
            probe.append_ledger_row(str(path), result)
            row = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(row["verdict"], None)
            self.assertEqual(row["rc"], 2)
            self.assertEqual(row["newest_age_min"], None)

    def test_two_runs_two_rows(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "ledger.jsonl"
            probe.append_ledger_row(str(path), self._quiet_result())
            active = self._quiet_result()
            active.update({"verdict": "active", "rc": probe.RC_ACTIVE,
                           "newest_age_min": 12.3})
            probe.append_ledger_row(str(path), active)
            rows = [json.loads(l) for l in
                    path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(rows), 2)
            self.assertEqual([r["verdict"] for r in rows],
                             ["quiet", "active"])

    def test_parent_dir_autocreated(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "a" / "b" / "ledger.jsonl"
            probe.append_ledger_row(str(path), self._quiet_result())
            self.assertTrue(path.is_file())

    def test_append_failure_warns_never_raises(self):
        # pointing the ledger at a directory makes open() raise OSError:
        # best-effort contract = WARN to stderr, no exception, rc untouched
        with tempfile.TemporaryDirectory() as td:
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                probe.append_ledger_row(td, self._quiet_result())  # td is a dir
            self.assertIn("WARN mv-sprint-probe-ledger append failed", err.getvalue())

    def test_cli_writes_row_and_propagates_rc(self):
        original_run = probe.run_probe
        original_append = probe.append_ledger_row
        try:
            probe.run_probe = lambda **kw: self._quiet_result()
            with tempfile.TemporaryDirectory() as td:
                path = Path(td) / "ledger.jsonl"
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    rc = probe.main(["--ledger", str(path), "--json"])
                self.assertEqual(rc, probe.RC_QUIET)
                row = json.loads(
                    path.read_text(encoding="utf-8").splitlines()[0])
                self.assertEqual(row["verdict"], "quiet")
                self.assertEqual(row["newest_age_min"], 247.7)
                self.assertIn('"verdict": "quiet"', out.getvalue())
        finally:
            probe.run_probe = original_run
            probe.append_ledger_row = original_append

    def test_cli_bare_flag_resolves_default_path(self):
        original_run = probe.run_probe
        original_append = probe.append_ledger_row
        captured = []
        try:
            probe.run_probe = lambda **kw: self._quiet_result()
            probe.append_ledger_row = lambda path, result: captured.append(path)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                probe.main(["--ledger"])  # bare flag
            self.assertEqual(captured, [str(probe.DEFAULT_LEDGER)])
        finally:
            probe.run_probe = original_run
            probe.append_ledger_row = original_append

    def test_cli_no_flag_zero_writes(self):
        # existing call surface zero-drift: no --ledger => no ledger write
        original_run = probe.run_probe
        original_append = probe.append_ledger_row
        try:
            probe.run_probe = lambda **kw: self._quiet_result()
            probe.append_ledger_row = lambda path, result: self.fail(
                "append_ledger_row must not fire without --ledger")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                probe.main(["--json"])
        finally:
            probe.run_probe = original_run
            probe.append_ledger_row = original_append


if __name__ == "__main__":
    unittest.main()
