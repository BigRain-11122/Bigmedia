"""Unit tests for tools/cap_utf8.py (tech#216 capture widget).

ASCII per the encoding rule: non-ASCII payload reaches the child via
\\u escapes so every source here stays pure ASCII. Real child processes
are exercised - byte capture and rc passthrough are the widget's job.
Run:
    python tests/test_cap_utf8.py
"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))

import cap_utf8  # noqa: E402

WIDGET = REPO / "tools" / "cap_utf8.py"


def run_widget(out, extra, timeout=60):
    argv = [sys.executable, str(WIDGET), str(out)] + extra
    return subprocess.run(argv, cwd=str(REPO), capture_output=True,
                          timeout=timeout)


class DecodeLadderTests(unittest.TestCase):
    def test_utf8_strict_first(self):
        self.assertEqual(
            cap_utf8.decode_output("\u4e2d\u6587 ok".encode("utf-8")),
            "\u4e2d\u6587 ok")

    def test_gbk_fallback_second(self):
        self.assertEqual(cap_utf8.decode_output(b"\xd6\xd0\xce\xc4"),
                         "\u4e2d\u6587")

    def test_replace_ladder_last_resort(self):
        self.assertIn("\ufffd",
                      cap_utf8.decode_output(b"\xfe\xff\xfe\xff"))


class WriteUtf8Tests(unittest.TestCase):
    def test_no_bom_and_nested_parent_mkdir(self):
        d = Path(tempfile.mkdtemp(prefix="bs-caputf8-"))
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        target = d / "nested" / "out.txt"
        cap_utf8.write_utf8(target, "\u4e2d\u6587 line\n")
        raw = target.read_bytes()
        self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))
        self.assertNotEqual(raw[:2], b"\xff\xfe")
        self.assertNotEqual(raw[:2], b"\xfe\xff")
        self.assertEqual(raw.decode("utf-8"), "\u4e2d\u6587 line\n")


class CliTests(unittest.TestCase):
    def _out(self):
        d = Path(tempfile.mkdtemp(prefix="bs-caputf8-"))
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        return d / "cap.txt"

    def test_real_run_writes_utf8_no_bom(self):
        # judgement criterion 3: the widget's own real run produces a
        # UTF-8 no-BOM file from a child's non-ASCII stdout
        out = self._out()
        child = ("import sys; sys.stdout.buffer.write("
                 r"'\u4e2d\u6587 ok'.encode('utf-8'))")
        p = run_widget(out, ["--", sys.executable, "-c", child])
        self.assertEqual(p.returncode, 0)
        self.assertIn(b"utf-8 no-bom", p.stdout)
        raw = out.read_bytes()
        self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))
        self.assertEqual(raw.decode("utf-8"), "\u4e2d\u6587 ok\n")

    def test_child_rc_passthrough(self):
        out = self._out()
        p = run_widget(out, ["--", sys.executable, "-c",
                             "import sys; print('boom'); sys.exit(7)"])
        self.assertEqual(p.returncode, 7)
        self.assertIn("boom", out.read_text(encoding="utf-8"))

    def test_empty_child_writes_empty_file(self):
        out = self._out()
        p = run_widget(out, ["--", sys.executable, "-c", "pass"])
        self.assertEqual(p.returncode, 0)
        self.assertEqual(out.read_bytes(), b"")

    def test_timeout_rc3_and_note(self):
        out = self._out()
        p = run_widget(out, ["--timeout", "1", "--", sys.executable,
                             "-c", "import time; time.sleep(5)"],
                       timeout=30)
        self.assertEqual(p.returncode, 3)
        self.assertIn("[timeout after 1s]",
                      out.read_text(encoding="utf-8"))

    def test_usage_errors_rc2(self):
        # no args at all
        p = subprocess.run([sys.executable, str(WIDGET)], cwd=str(REPO),
                           capture_output=True, timeout=30)
        self.assertEqual(p.returncode, 2)
        # OUT but no '--' separator: nothing flies, nothing is written
        out = self._out()
        p = subprocess.run([sys.executable, str(WIDGET), str(out),
                            sys.executable, "-c", "print(1)"],
                           cwd=str(REPO), capture_output=True, timeout=30)
        self.assertEqual(p.returncode, 2)
        self.assertFalse(out.exists())
        # empty command after '--'
        p = subprocess.run([sys.executable, str(WIDGET), str(out), "--"],
                           cwd=str(REPO), capture_output=True, timeout=30)
        self.assertEqual(p.returncode, 2)


if __name__ == "__main__":
    unittest.main()
