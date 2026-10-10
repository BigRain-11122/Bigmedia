"""Tests for same_text_check (tech#87): audio-line same-text verification CLI."""
import io
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from render import same_text_check as stc  # noqa: E402


def _write(path, text):
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def _srt(entries):
    blocks = []
    for i, (t0, t1, txt) in enumerate(entries, 1):
        blocks.append("%d\n%s --> %s\n%s" % (i, t0, t1, txt))
    return "\n\n".join(blocks) + "\n"


def _beats(rows):
    return "\n".join(rows) + "\n"


BEATS_OK = _beats([
    "hook | t | AAA \u53e5\u4e00\u3002",
    "beat | t | BBB \u53e5\u4e8c\u3002",
    "close | t | CCC \u53e5\u4e09\u3002",
])
SRT_OK = _srt([
    ("00:00:00,000", "00:00:02,000", "AAA \u53e5\u4e00\u3002"),
    ("00:00:02,000", "00:00:04,000", "BBB \u53e5\u4e8c\u3002"),
    ("00:00:04,000", "00:00:06,000", "CCC \u53e5\u4e09\u3002"),
])


class CompareCoreTests(unittest.TestCase):
    def test_same_text_zero_miss(self):
        cues = stc.load_srt(_tmp_srt(self, SRT_OK))
        rows = stc.load_beats_rows(_tmp_beats(self, BEATS_OK))
        miss, lines = stc.compare(cues, [stc.spoken_column(r) for r in rows])
        self.assertEqual(miss, 0)
        self.assertEqual(lines[0], "cues=3 beats=3")

    def test_count_mismatch_counts_miss(self):
        rows = stc.load_beats_rows(_tmp_beats(self, BEATS_OK))
        spoken = [stc.spoken_column(r) for r in rows]
        # r1939 semantics: count mismatch +1 AND the mismatched short-side cue +1
        miss, lines = stc.compare(["only-one"], spoken)
        self.assertEqual(miss, 2)
        self.assertIn("COUNT-MISMATCH", lines)

    def test_text_miss_reports_cue_line(self):
        rows = stc.load_beats_rows(_tmp_beats(self, BEATS_OK))
        spoken = [stc.spoken_column(r) for r in rows]
        miss, lines = stc.compare(["AAA DIFFERENT", "BBB x", "CCC y"], spoken)
        self.assertEqual(miss, 3)
        self.assertIn("MISS cue01", lines)
        self.assertTrue(any(l.startswith("  srt : ") for l in lines))

    def test_space_insensitive_compare(self):
        self.assertEqual(stc.compare(["AB C"], ["ABC"]), (0, ["cues=1 beats=1"]))

    def test_malformed_beats_row_loud(self):
        with self.assertRaises(ValueError):
            stc.spoken_column("only-one-column")


class DeclReportTests(unittest.TestCase):
    def test_decl_report_advisory_lines(self):
        rows = stc.load_beats_rows(_tmp_beats(self, _beats([
            "hook | t | \u7531 AI \u53c2\u4e0e\u751f\u6210\uff0c\u57fa\u4e8e\u771f\u5b9e\u4e8b\u4ef6\u4e0e\u5728\u518c\u5c45\u6c11\u6863\u6848\u6539\u7f16\uff0c\u90e8\u5206\u60c5\u8282\u4e3a\u5408\u7406\u63a8\u6f14\u3002",
            "close | t | \u7ed3\u5c3e\u4e3a\u5408\u7406\u63a8\u6f14\u58f0\u660e\u3002",
        ])))
        lines = stc.decl_report(rows)
        self.assertEqual(lines[0], "hook-triple-decl: ai-gen=True archive=True inference=True")
        self.assertEqual(lines[1], "close-inference-decl: True")

    def test_decl_missing_reported_false(self):
        rows = stc.load_beats_rows(_tmp_beats(self, _beats([
            "hook | t | \u666e\u901a\u53e5",
            "close | t | \u666e\u901a\u53e5",
        ])))
        lines = stc.decl_report(rows)
        self.assertEqual(lines[0], "hook-triple-decl: ai-gen=False archive=False inference=False")
        self.assertEqual(lines[1], "close-inference-decl: False")


class CliTests(unittest.TestCase):
    def _run(self, args):
        return subprocess.run(
            [sys.executable, os.path.join("src", "render", "same_text_check.py")] + args,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            cwd=os.path.join(os.path.dirname(__file__), ".."))

    def test_cli_same_text_rc0(self):
        with tempfile.TemporaryDirectory() as td:
            b, s = os.path.join(td, "b.txt"), os.path.join(td, "s.srt")
            _write(b, BEATS_OK); _write(s, SRT_OK)
            r = self._run(["--beats", b, "--srt", s])
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("SAME-TEXT miss=0", r.stdout)

    def test_cli_miss_rc1(self):
        with tempfile.TemporaryDirectory() as td:
            b, s = os.path.join(td, "b.txt"), os.path.join(td, "s.srt")
            _write(b, BEATS_OK)
            _write(s, _srt([
                ("00:00:00,000", "00:00:02,000", "WRONG"),
                ("00:00:02,000", "00:00:04,000", "BBB \u53e5\u4e8c\u3002"),
                ("00:00:04,000", "00:00:06,000", "CCC \u53e5\u4e09\u3002"),
            ]))
            r = self._run(["--beats", b, "--srt", s])
            self.assertEqual(r.returncode, 1)
            self.assertIn("MISS cue01", r.stdout)

    def test_cli_bad_beats_row_rc2(self):
        with tempfile.TemporaryDirectory() as td:
            b, s = os.path.join(td, "b.txt"), os.path.join(td, "s.srt")
            _write(b, "no-pipe-column\n"); _write(s, SRT_OK)
            r = self._run(["--beats", b, "--srt", s])
            self.assertEqual(r.returncode, 2)
            self.assertIn("BAD-BEATS-ROW", r.stdout)

    def test_cli_missing_file_rc2(self):
        r = self._run(["--beats", "no-such-file.txt", "--srt", "no-such.srt"])
        self.assertEqual(r.returncode, 2)

    def test_cli_decl_check_lines(self):
        with tempfile.TemporaryDirectory() as td:
            b, s = os.path.join(td, "b.txt"), os.path.join(td, "s.srt")
            _write(b, BEATS_OK); _write(s, SRT_OK)
            r = self._run(["--beats", b, "--srt", s, "--decl-check"])
            self.assertEqual(r.returncode, 0)
            self.assertIn("hook-triple-decl:", r.stdout)
            self.assertIn("close-inference-decl:", r.stdout)

    def test_cli_out_evidence_utf8_no_bom(self):
        with tempfile.TemporaryDirectory() as td:
            b, s = os.path.join(td, "b.txt"), os.path.join(td, "s.srt")
            out = os.path.join(td, "evidence.txt")
            _write(b, BEATS_OK); _write(s, SRT_OK)
            r = self._run(["--beats", b, "--srt", s, "--decl-check", "--out", out])
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            raw = open(out, "rb").read()
            self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))
            text = raw.decode("utf-8")
            self.assertIn("SAME-TEXT miss=0", text)
            self.assertIn("hook-triple-decl", text)


class ParityAnchorTests(unittest.TestCase):
    """R1939 ad-hoc readout shape parity: report line formats are frozen."""

    def test_summary_line_format(self):
        miss, lines = stc.compare(["A"], ["A"])
        self.assertEqual(lines, ["cues=1 beats=1"])

    def test_build_report_appends_summary(self):
        miss, lines = stc.build_report(["A"], ["hook | t | A"], False)
        self.assertEqual(lines[-1], "SAME-TEXT miss=0")

    def test_miss_lines_format(self):
        miss, lines = stc.compare(["A"], ["B"])
        self.assertEqual(lines[1], "MISS cue01")
        self.assertEqual(lines[2], "  srt : A")
        self.assertEqual(lines[3], "  beat: B")


def _tmp_srt(case, text):
    import tempfile
    fd, path = tempfile.mkstemp(suffix=".srt")
    os.close(fd)
    _write(path, text)
    case.addCleanup(os.unlink, path)
    return path


def _tmp_beats(case, text):
    import tempfile
    fd, path = tempfile.mkstemp(suffix=".txt")
    os.close(fd)
    _write(path, text)
    case.addCleanup(os.unlink, path)
    return path


if __name__ == "__main__":
    unittest.main()
