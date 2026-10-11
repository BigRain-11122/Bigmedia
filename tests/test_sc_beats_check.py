"""Tests for sc_beats_check (tech#96+#99): SC-series beats machine-check CLI."""
import io
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from render import sc_beats_check as sbc  # noqa: E402


def _write(path, text):
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


BEATS_OK = "\n".join([
    "hook | \u6807\u9898 | \u7531 AI \u53c2\u4e0e\u751f\u6210\uff0c\u57fa\u4e8e\u771f\u5b9e\u4e8b\u4ef6\u3002",
    "body | \u6863\u6848 | \u4fe1\u6761\u53e5\u300c\u706f\u4e0d\u95ee\u6765\u8def\u300d\u5168\u5728\u3002",
    "close | \u58f0\u660e | \u7ed3\u5c3e\u4e3a\u5408\u7406\u63a8\u6f14\u3002",
]) + "\n"

MATERIAL_OK = "\u524d\u6587\n" + BEATS_OK + "\u540e\u6587\n"

ANCHORS_OK = "# comment line skipped\n\u4fe1\u6761\u53e5\u300c\u706f\u4e0d\u95ee\u6765\u8def\u300d\n\u5408\u7406\u63a8\u6f14\n"

CARD_TEXT_OK = "\u4fe1\u6761\u53e5\u300c\u706f\u4e0d\u95ee\u6765\u8def\u300d\u5168\u5728\u3002\n" \
    "\u7ea2\u706f\u662f\u4e3a\u6240\u6709\u4eba\u4eae\u7684\uff0c\u5305\u62ec\u6211\n\u5f92\u5f1f=\u65b0\u4eba\u98ce\u63a7\u5458\n"

CARD_PAIRS_OK = "\u4fe1\u6761\u53e5\u300c\u706f\u4e0d\u95ee\u6765\u8def\u300d\u5168\u5728\u3002\n" \
    "\u5f92\u5f1f\u662f\u65b0\u98ce\u63a7\u5458||\u5f92\u5f1f=\u65b0\u4eba\u98ce\u63a7\u5458\n"


class FormatFaceTests(unittest.TestCase):
    def test_format_good_rows_and_charcount(self):
        rows = sbc.load_rows(BEATS_OK)
        bad, chars = sbc.format_face(rows)
        self.assertEqual(bad, [])
        self.assertEqual(len(rows), 3)
        self.assertTrue(chars > 0)

    def test_format_bad_profile_flagged(self):
        rows = sbc.load_rows("hook | t | a\nintro | t | b\n")
        bad, _ = sbc.format_face(rows)
        self.assertEqual(bad, [("profile", 2, "intro")])

    def test_format_bad_columns_flagged(self):
        rows = sbc.load_rows("hook | t\n")
        bad, _ = sbc.format_face(rows)
        self.assertEqual(len(bad), 1)
        self.assertEqual(bad[0][0], "cols")

    def test_spoken_charcount_strips_cjk_punct(self):
        rows = sbc.load_rows("body | t | \u4e00\u4e8c\u4e09\uff0c\u56db\u3002")
        _, chars = sbc.format_face(rows)
        self.assertEqual(chars, 4)  # CJK comma/period stripped, letters kept


class FacesTests(unittest.TestCase):
    def test_anchor_face_miss_listed(self):
        miss = sbc.anchor_face(BEATS_OK, ["\u4e0d\u5b58\u5728\u7684\u951a"])
        self.assertEqual(miss, ["\u4e0d\u5b58\u5728\u7684\u951a"])

    def test_inclusion_face_full_embed_green(self):
        rows = sbc.load_rows(BEATS_OK)
        self.assertEqual(sbc.inclusion_face(rows, MATERIAL_OK), [])

    def test_inclusion_face_missing_row_reported(self):
        rows = sbc.load_rows(BEATS_OK)
        bad = sbc.inclusion_face(rows, "\u53ea\u6709\u524d\u6587\u6ca1\u6709\u5168\u6587")
        self.assertEqual(len(bad), 3)

    def test_card_pairs_bare_and_adapted(self):
        pairs = sbc.load_card_pairs(_tmp(self, CARD_PAIRS_OK))
        self.assertEqual(pairs[0], ("\u4fe1\u6761\u53e5\u300c\u706f\u4e0d\u95ee\u6765\u8def\u300d\u5168\u5728\u3002",
                                    "\u4fe1\u6761\u53e5\u300c\u706f\u4e0d\u95ee\u6765\u8def\u300d\u5168\u5728\u3002"))
        self.assertEqual(pairs[1], ("\u5f92\u5f1f\u662f\u65b0\u98ce\u63a7\u5458", "\u5f92\u5f1f=\u65b0\u4eba\u98ce\u63a7\u5458"))

    def test_card_face_target_membership(self):
        pairs = [("\u5f92\u5f1f\u662f\u65b0\u98ce\u63a7\u5458", "\u5f92\u5f1f=\u65b0\u4eba\u98ce\u63a7\u5458")]
        self.assertEqual(sbc.card_face(CARD_TEXT_OK, pairs), [])
        self.assertEqual(sbc.card_face(CARD_TEXT_OK.replace("\u5f92\u5f1f=", ""), pairs),
                         ["\u5f92\u5f1f=\u65b0\u4eba\u98ce\u63a7\u5458"])

    def test_leak_face_hit_detection(self):
        self.assertEqual(sbc.leak_face(BEATS_OK, ["\u94f6\u884c\u505a\u98ce\u63a7"]), [])
        self.assertEqual(sbc.leak_face("a\u94f6\u884c\u505a\u98ce\u63a7b", ["\u94f6\u884c\u505a\u98ce\u63a7"]),
                         ["\u94f6\u884c\u505a\u98ce\u63a7"])


class BuildReportTests(unittest.TestCase):
    def test_all_faces_green_rc0(self):
        rows_text = BEATS_OK
        rc, lines = sbc.build_report(rows_text, MATERIAL_OK,
                                     sbc.load_anchor_lines(_tmp(self, ANCHORS_OK)),
                                     CARD_TEXT_OK, sbc.load_card_pairs(_tmp(self, CARD_PAIRS_OK)),
                                     ["\u94f6\u884c\u505a\u98ce\u63a7"])
        self.assertEqual(rc, 0)
        self.assertTrue(lines[-1].startswith("SC-CHECK GREEN"))

    def test_anchor_miss_rc1_face_listed(self):
        rc, lines = sbc.build_report(BEATS_OK, None, ["\u4e0d\u5728"],
                                     None, None, [])
        self.assertEqual(rc, 1)
        self.assertEqual(lines[-1], "SC-CHECK FAIL faces=anchor")

    def test_inclusion_miss_rc1(self):
        rc, lines = sbc.build_report(BEATS_OK, "\u7a7a\u6750\u6599", None, None, None, [])
        self.assertEqual(rc, 1)
        self.assertEqual(lines[-1], "SC-CHECK FAIL faces=inclusion")

    def test_leak_hit_rc1(self):
        rc, lines = sbc.build_report(BEATS_OK, None, None, None, None, ["\u7531 AI"])
        self.assertEqual(rc, 1)
        self.assertEqual(lines[-1], "SC-CHECK FAIL faces=leak")

    def test_format_bad_rc2_loud(self):
        rc, lines = sbc.build_report("hook | t\n", None, None, None, None, [])
        self.assertEqual(rc, 2)
        self.assertIn("SC-CHECK BAD-BEATS", lines[-1])

    def test_skip_faces_noted(self):
        rc, lines = sbc.build_report(BEATS_OK, None, None, None, None, [])
        self.assertEqual(rc, 0)
        self.assertTrue(any(l.startswith("verbatim_anchors=SKIP") for l in lines))
        self.assertTrue(any(l.startswith("inclusion(beats in material)=SKIP") for l in lines))
        self.assertTrue(any(l.startswith("card_source=SKIP") for l in lines))
        self.assertTrue(any(l.startswith("leak_face=SKIP") for l in lines))


class AsrDiffTests(unittest.TestCase):
    """tech#108 --asr-diff face: canonical drift readout (advisory, never fails rc)."""

    def test_fullwidth_punct_zero_ops_r1995_regredge(self):
        # R1995 op-red regression lock: U+FF0C and friends must never produce
        # phantom delete ops (ad-hoc first calc missed U+FF0C -> +4.7pp fake).
        src = "\u4e00\u4e8c\uff0c\u4e09\u3002"
        header, details = sbc.asr_diff_face(src, "\u4e00\u4e8c\uff0c\u4e09\u3002")
        self.assertIn("diff_sites=0", header)
        self.assertIn("charpos=0.0%", header)
        self.assertEqual(details, [])

    def test_substitution_counts_site_and_chars(self):
        src = "\u57ce\u5e02\u4e0d\u4f1a\u5fd8\u8bb0"      # city will not forget
        asr = "\u57ce\u5e02\u4e0d\u4f1a\u5fd8\u8bb0".replace("\u8bb0", "\u7eaa")  # -> ji
        header, details = sbc.asr_diff_face(src, asr)
        self.assertIn("src_chars=6", header)
        self.assertIn("diff_sites=1", header)
        self.assertIn("diff_chars=1", header)
        self.assertIn("charpos=16.7%", header)
        self.assertTrue(details and details[0].startswith("replace"))

    def test_srt_parser_skips_numbers_and_timestamps(self):
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "a.srt")
            _write(p, "1\n00:00:01,000 --> 00:00:02,000\n\u7ea2\u706f\n\n2\n00:00:02,000 --> 00:00:03,000\n\u4eae\u7740\n")
            self.assertEqual(sbc.load_srt_text(p), "\u7ea2\u706f\u4eae\u7740")

    def test_compose_spoken_src_from_beats(self):
        src = sbc.compose_spoken_src(BEATS_OK)
        self.assertEqual(src, ("\u7531 AI \u53c2\u4e0e\u751f\u6210\uff0c\u57fa\u4e8e\u771f\u5b9e\u4e8b\u4ef6\u3002"
                               "\u4fe1\u6761\u53e5\u300c\u706f\u4e0d\u95ee\u6765\u8def\u300d\u5168\u5728\u3002"
                               "\u7ed3\u5c3e\u4e3a\u5408\u7406\u63a8\u6f14\u3002"))

    def test_advisory_high_drift_stays_rc0(self):
        rc, lines = sbc.build_report(BEATS_OK, None, None, None, None, [],
                                     asr_diff=("\u4e00\u4e8c\u4e09\u56db\u4e94", "\u5168\u662f\u5e7b\u89c9"))
        self.assertEqual(rc, 0)
        self.assertTrue(lines[-1].startswith("SC-CHECK GREEN"))
        self.assertTrue(any(l.startswith("asr_diff: src_chars=5") for l in lines))
        self.assertTrue(any("ADVISORY" in l for l in lines))

    def test_face_skipped_when_absent(self):
        rc, lines = sbc.build_report(BEATS_OK, None, None, None, None, [])
        self.assertEqual(rc, 0)
        self.assertTrue(any(l.startswith("asr_diff=SKIP") for l in lines))


class CliTests(unittest.TestCase):
    def _run(self, args):
        return subprocess.run(
            [sys.executable, os.path.join("src", "render", "sc_beats_check.py")] + args,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            cwd=os.path.join(os.path.dirname(__file__), ".."))

    def test_cli_full_green_rc0(self):
        with tempfile.TemporaryDirectory() as td:
            b = os.path.join(td, "b.txt"); _write(b, BEATS_OK)
            m = os.path.join(td, "m.md"); _write(m, MATERIAL_OK)
            a = os.path.join(td, "a.txt"); _write(a, ANCHORS_OK)
            c = os.path.join(td, "c.md"); _write(c, CARD_TEXT_OK)
            ca = os.path.join(td, "ca.txt"); _write(ca, CARD_PAIRS_OK)
            r = self._run(["--beats", b, "--material", m, "--anchors", a,
                           "--card", c, "--card-anchors", ca, "--leak", "\u94f6\u884c"])
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("SC-CHECK GREEN", r.stdout)

    def test_cli_anchor_miss_rc1(self):
        with tempfile.TemporaryDirectory() as td:
            b = os.path.join(td, "b.txt"); _write(b, BEATS_OK)
            a = os.path.join(td, "a.txt"); _write(a, "\u4e0d\u5b58\u5728\u7684\u951a\n")
            r = self._run(["--beats", b, "--anchors", a])
            self.assertEqual(r.returncode, 1)
            self.assertIn("MISS=", r.stdout)
            self.assertIn("SC-CHECK FAIL faces=anchor", r.stdout)

    def test_cli_bad_beats_rc2(self):
        with tempfile.TemporaryDirectory() as td:
            b = os.path.join(td, "b.txt"); _write(b, "no-pipe\n")
            r = self._run(["--beats", b])
            self.assertEqual(r.returncode, 2)
            self.assertIn("BAD-BEATS", r.stdout)

    def test_cli_missing_file_rc2(self):
        r = self._run(["--beats", "no-such-file.txt"])
        self.assertEqual(r.returncode, 2)

    def test_cli_card_without_pairs_rc2(self):
        with tempfile.TemporaryDirectory() as td:
            b = os.path.join(td, "b.txt"); _write(b, BEATS_OK)
            c = os.path.join(td, "c.md"); _write(c, "x")
            r = self._run(["--beats", b, "--card", c])
            self.assertEqual(r.returncode, 2)

    def test_cli_asr_diff_report_and_out(self):
        with tempfile.TemporaryDirectory() as td:
            b = os.path.join(td, "b.txt"); _write(b, BEATS_OK)
            srt = os.path.join(td, "asr.srt")
            _write(srt, "1\n00:00:01,000 --> 00:00:02,000\n\u5408\u7406\u63a8\u6f14\n")
            out = os.path.join(td, "evidence.txt")
            r = self._run(["--beats", b, "--asr-diff", srt, "--out", out])
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            body = open(out, "rb").read().decode("utf-8")
            self.assertIn("asr_diff: src_chars=", body)
            self.assertIn("SC-CHECK GREEN", body)

    def test_cli_src_text_only_without_asr_diff_rc2(self):
        with tempfile.TemporaryDirectory() as td:
            b = os.path.join(td, "b.txt"); _write(b, BEATS_OK)
            s = os.path.join(td, "v.txt"); _write(s, "x")
            r = self._run(["--beats", b, "--src-text", s])
            self.assertEqual(r.returncode, 2)

    def test_cli_missing_srt_rc2(self):
        with tempfile.TemporaryDirectory() as td:
            b = os.path.join(td, "b.txt"); _write(b, BEATS_OK)
            r = self._run(["--beats", b, "--asr-diff", "no-such.srt"])
            self.assertEqual(r.returncode, 2)

    def test_cli_out_evidence_utf8_no_bom(self):
        with tempfile.TemporaryDirectory() as td:
            b = os.path.join(td, "b.txt"); _write(b, BEATS_OK)
            out = os.path.join(td, "evidence.txt")
            r = self._run(["--beats", b, "--out", out])
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            raw = open(out, "rb").read()
            self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))
            self.assertIn("SC-CHECK GREEN", raw.decode("utf-8"))


def _tmp(case, text):
    import tempfile
    fd, path = tempfile.mkstemp(suffix=".txt")
    os.close(fd)
    _write(path, text)
    case.addCleanup(os.unlink, path)
    return path


if __name__ == "__main__":
    unittest.main()
