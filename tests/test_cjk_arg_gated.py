# -*- coding: utf-8 -*-
"""Permanent arg-gated CJK console smoke gate (tech#248, R2391).

tech#247 (R2390) live-smoked the three arg-gated console faces by hand
in .c3-tmp (wiped each round end); this module pins them into the suite
so a GBK-codepage regression cannot come back silently:

  A. src/board_check.py on a stale ledger fixture (Chinese finding echo)
  B. src/platform_spec_check.py on a tiny lavfi mp4 (platform name echo)
  C. src/intel/daily_brief.py with a stubbed collect() (CJK --out path
     echo) - ZERO NETWORK: collect() is replaced in-process by a temp
     driver script; the canonical daily file is never touched
     (--date 2000-01-01 + temp out dir, tech#248 criterion 1).

Judgement mirrors tools/cjk_console_audit.py: every child runs under a
hostile PYTHONIOENCODING=gbk console; its stdout must still decode as
STRICT UTF-8, carry CJK, and contain no U+FFFD. The canary test proves
the detector is not vacuous (tech#248 criterion 2): a child that
prints CJK WITHOUT hardening emits GBK bytes under the same env and
MUST be caught - so removing _harden_console_stdio from any of the
three tools turns this module red. Suite increment budget < 30s
(criterion 3).
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"

CJK_RE = re.compile(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]")
WECHAT_VIDEO = "\u5fae\u4fe1\u89c6\u9891\u53f7"  # WeChat video account
CN_DIR = "\u4e2d\u6587\u76ee\u5f55"             # CJK --out dir name


def _hostile_env():
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "gbk"  # hostile codepage injection
    return env


def _run(argv, timeout=90):
    return subprocess.run(argv, capture_output=True, timeout=timeout,
                          cwd=str(REPO), env=_hostile_env())


def assert_utf8_cjk(raw, label):
    """Strict UTF-8 decode + CJK present + no replacement char."""
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AssertionError(
            "%s: stdout is not UTF-8 (GBK codepage writer regression): %s"
            % (label, exc))
    if "\ufffd" in text:
        raise AssertionError("%s: U+FFFD replacement char in output" % label)
    if not CJK_RE.search(text):
        raise AssertionError("%s: no CJK found in console output" % label)
    return text


class CanaryTests(unittest.TestCase):
    def test_gbk_writer_without_hardening_is_caught(self):
        """Negative control: the strict-UTF-8 detector must reject GBK
        bytes emitted by an UNhardened CJK writer under the same hostile
        env (proves removing _harden_console_stdio turns fixtures red)."""
        child = subprocess.run(
            [sys.executable, "-c",
             "import sys; sys.stdout.write('\\u4e2d\\u6587 canary\\n')"],
            capture_output=True, timeout=60, cwd=str(REPO), env=_hostile_env())
        self.assertRaises(UnicodeDecodeError, child.stdout.decode, "utf-8")


class ArgGatedSmokeTests(unittest.TestCase):
    def test_a_board_check_fixture_console_stays_utf8(self):
        manifest = json.loads((FIXTURES / "manifest.json")
                              .read_text(encoding="utf-8"))
        ledger = FIXTURES / manifest["board_ideas_stale"]
        drafts = Path(tempfile.mkdtemp(prefix="bs-cjkA-"))
        self.addCleanup(shutil.rmtree, drafts, ignore_errors=True)
        (drafts / "20260923-BS-902-x-v1.md").write_text("fixture\n",
                                                        encoding="utf-8")
        proc = _run([sys.executable, "src/board_check.py",
                     str(ledger), str(drafts)])
        self.assertIn(proc.returncode, (0, 1))  # probe verdict, not usage
        text = assert_utf8_cjk(proc.stdout, "board_check")
        self.assertIn("stale", text)

    def test_b_platform_spec_check_console_stays_utf8(self):
        tmp = Path(tempfile.mkdtemp(prefix="bs-cjkB-"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        mp4 = tmp / "tiny.mp4"
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi",
                        "-i", "testsrc=duration=1.0:size=160x90:rate=10",
                        "-pix_fmt", "yuv420p", str(mp4)],
                       capture_output=True, timeout=60, cwd=str(REPO))
        self.assertTrue(mp4.is_file(), "ffmpeg lavfi sample not generated")
        proc = _run([sys.executable, "src/platform_spec_check.py",
                     "--video", str(mp4), "--platform", WECHAT_VIDEO])
        self.assertIn(proc.returncode, (0, 1))  # tiny sample may FAIL spec
        text = assert_utf8_cjk(proc.stdout, "platform_spec_check")
        self.assertIn("SUMMARY", text)
        self.assertIn(WECHAT_VIDEO, text)

    def test_c_daily_brief_stubbed_collect_console_stays_utf8(self):
        tmp = Path(tempfile.mkdtemp(prefix="bs-cjkC-"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        out_dir = tmp / CN_DIR
        driver = tmp / "db_driver.py"
        db_path = REPO / "src" / "intel" / "daily_brief.py"
        driver.write_text(
            "import importlib.util, sys\n"
            "spec = importlib.util.spec_from_file_location('db_stub', %r)\n"
            "db = importlib.util.module_from_spec(spec)\n"
            "spec.loader.exec_module(db)\n"
            "def _stub_collect(limit=None):\n"
            "    return {'ok': {'stub-source': [('\u4e2d\u6587\u6807\u9898',"
            " '\u5143\u6ce8\u6570\u636e')]}, 'fail': {}}\n"
            "db.collect = _stub_collect\n"
            "sys.exit(db.main(['daily_brief', '--date', '2000-01-01',"
            " '--out', sys.argv[1]]))\n"
            % (str(db_path),), encoding="utf-8")
        proc = _run([sys.executable, str(driver), str(out_dir)])
        self.assertEqual(proc.returncode, 0)
        text = assert_utf8_cjk(proc.stdout, "daily_brief")
        self.assertIn("stub-source", text)
        self.assertIn(CN_DIR, text)  # CJK --out path echoed back clean
        proc.stderr.decode("utf-8")  # stderr must be GBK-free too


if __name__ == "__main__":
    unittest.main(verbosity=2)
