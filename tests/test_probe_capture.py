# -*- coding: utf-8 -*-
"""Tests for probe_capture (state/queue/tech#25, R1838): one-shot runner for
the three routine probes with UTF-8-safe file output — the PS 5.1 `>` UTF-16
redirection trap root-fix (R1831 four-rework incident).
"""

import contextlib
import io
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src", "os"))

import probe_capture as pc  # noqa: E402


class BuildProbesTests(unittest.TestCase):
    def test_order_and_names(self):
        self.assertEqual([n for n, _ in pc.build_probes(False)],
                         ["board_check", "readiness", "loop_health"])

    def test_compact_faces(self):
        probes = dict((n, a) for n, a in pc.build_probes(False))
        self.assertEqual(probes["readiness"][-1], "--summary")
        self.assertEqual(probes["loop_health"][-1], "--loop")
        for name, argv in probes.items():
            self.assertTrue(argv[1].endswith(name + ".py"), msg=name)
            self.assertEqual(argv[0], sys.executable)

    def test_full_faces(self):
        probes = dict((n, a) for n, a in pc.build_probes(True))
        self.assertNotIn("--summary", probes["readiness"])
        self.assertNotIn("--loop", probes["loop_health"])


class ChildEnvTests(unittest.TestCase):
    def test_utf8_env(self):
        env = pc.child_env()
        self.assertEqual(env["PYTHONIOENCODING"], "utf-8")
        self.assertEqual(env["PYTHONUTF8"], "1")
        self.assertIn("PATH", env)  # passthrough preserved


class RunProbeTests(unittest.TestCase):
    def _run_code(self, code, timeout_s=30):
        return pc.run_probe([sys.executable, "-c", code], pc.child_env(),
                            os.getcwd(), timeout_s)

    def test_stdout_and_rc(self):
        rc, text = self._run_code("print('héllo'); import sys; sys.exit(1)")
        self.assertEqual(rc, 1)
        self.assertIn("héllo", text)

    def test_stderr_merged(self):
        rc, text = self._run_code(
            "import sys; sys.stderr.write('boom'); sys.exit(0)")
        self.assertEqual(rc, 0)
        self.assertIn("[stderr] boom", text)

    def test_timeout_marks_rc3(self):
        rc, text = self._run_code("import time; time.sleep(30)", timeout_s=1)
        self.assertEqual(rc, 3)
        self.assertIn("[timeout after", text)


class ReportTests(unittest.TestCase):
    def test_render_sections(self):
        text = pc.render_report(
            [("board_check", 0, "ok"), ("readiness", 1, "blocked")],
            "compact", "2026-10-09 19:00:00")
        self.assertIn("# probe-capture 2026-10-09 19:00:00 mode=compact", text)
        self.assertIn("=== board_check (rc=0) ===", text)
        self.assertIn("=== readiness (rc=1) ===", text)
        self.assertTrue(text.endswith("blocked\n"))

    def test_overall_rc(self):
        self.assertEqual(pc.overall_rc([("a", 0, ""), ("b", 2, "")]), 2)
        self.assertEqual(pc.overall_rc([("a", 0, ""), ("b", -1, "")]), 0)
        self.assertEqual(pc.overall_rc([]), 0)


class WriteReportTests(unittest.TestCase):
    def test_utf8_no_bom(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "sub", "probes.txt")
            returned = pc.write_report(path, "héllo===中文\n")
            self.assertEqual(str(returned), path)
            with open(path, "rb") as fh:
                data = fh.read()
            self.assertFalse(data.startswith(b"\xef\xbb\xbf"), "BOM leaked")
            self.assertEqual(data.decode("utf-8"), "héllo===中文\n")


class MainTests(unittest.TestCase):
    """Integration: real repo probes (read-only, ~0.5s per face)."""

    def _run(self, args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = pc.main(["probe_capture"] + args)
        return rc, buf.getvalue()

    def test_out_file_utf8_and_sections(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "probes.txt")
            rc, stdout = self._run(["--out", out])
            self.assertIn(rc, (0, 1))  # 1 = live blockers/lh-fail expected
            self.assertIn("written: %s" % out, stdout)
            self.assertIn("readiness: rc=", stdout)
            with open(out, "rb") as fh:
                data = fh.read()
            self.assertFalse(data.startswith(b"\xef\xbb\xbf"))
            text = data.decode("utf-8")
            self.assertIn("mode=compact", text)
            self.assertIn("=== board_check (rc=", text)
            self.assertIn("=== readiness (rc=", text)
            self.assertIn("=== loop_health (rc=", text)
            self.assertNotIn("=== board_check", stdout)  # stdout trimmed

    def test_default_stdout_full_report(self):
        rc, stdout = self._run([])
        self.assertIn(rc, (0, 1))
        self.assertIn("=== board_check (rc=", stdout)
        self.assertIn("=== loop_health (rc=", stdout)

    def test_usage_error(self):
        self.assertEqual(self._run(["--bogus"])[0], 2)

    def test_bad_timeout(self):
        self.assertEqual(self._run(["--timeout", "0"])[0], 2)
        self.assertEqual(self._run(["--timeout", "x"])[0], 2)


if __name__ == "__main__":
    unittest.main()
