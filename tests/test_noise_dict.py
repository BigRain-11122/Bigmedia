# -*- coding: utf-8 -*-
"""Unit tests for the ASR noise dictionary hook (tech#12 R1827,
src/render/whisper_to_srt.py: load_noise_dict / apply_noise_dict).

Pure functions only: no model load, no audio, no network, real
data/ read-only where used. Chinese strings appear as \\uXXXX
escapes per the ASCII encoding rule (same as test_render_card.py).

Run:
    python tests/test_noise_dict.py
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "render"))
import whisper_to_srt as w2s  # noqa: E402

REAL_DICT = REPO / "data" / "pipeline" / "asr-noise-dict-v1.json"

# real evidence pairs (station-reviews asr-check rows)
N_RIZHI = "\u65e5\u6cbb"          # ASR wrote (BS-004)
T_RIZHI = "\u65e5\u5fd7"          # true term (log)
N_JIHUA = "\u8ba1\u5212"          # ASR wrote (BS-002, common word)
T_JINHUA = "\u8fdb\u5316"         # true term (evolution)
N_XINPIAO = "\u5fc3\u7968"        # ASR wrote (BS-003, implausible)
T_XINTIAO = "\u5fc3\u8df3"        # true term (heartbeat)
N_CHENGSHIDAAN = "\u7a0b\u5e08\u5927\u6848"  # ASR wrote (BS-016)
T_CHENGSHIDAAN = "\u57ce\u5e02\u6863\u6848"  # true term (city archive)
N_DAAN = "\u5927\u6848"           # substring noise (BS-014/016 family)


def _fixture(entries):
    tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                      encoding="utf-8")
    json.dump({"entries": entries}, tmp, ensure_ascii=False)
    tmp.close()
    return Path(tmp.name)


class LoadNoiseDictTests(unittest.TestCase):
    def test_load_parses_and_sorts_longest_first(self):
        p = _fixture([{"noise": N_DAAN, "true": T_RIZHI, "class": "guarded"},
                      {"noise": N_CHENGSHIDAAN, "true": T_CHENGSHIDAAN,
                       "class": "safe"}])
        try:
            entries = w2s.load_noise_dict(str(p))
            self.assertEqual(2, len(entries))
            self.assertEqual(N_CHENGSHIDAAN, entries[0][0])
        finally:
            p.unlink()

    def test_missing_class_defaults_to_guarded(self):
        p = _fixture([{"noise": N_XINPIAO, "true": T_XINTIAO}])
        try:
            entries = w2s.load_noise_dict(str(p))
            self.assertEqual("guarded", entries[0][2])
        finally:
            p.unlink()


class ApplyNoiseDictTests(unittest.TestCase):
    CUES = [(0.0, 1.0, "a"), (1.0, 2.0, "b")]

    def test_safe_fires_without_expect(self):
        entries = [(N_XINPIAO, T_XINTIAO, "safe")]
        out, applied, skipped = w2s.apply_noise_dict(
            [(0.0, 1.0, N_XINPIAO)], entries, None)
        self.assertEqual(1, applied)
        self.assertEqual(0, skipped)
        self.assertEqual(T_XINTIAO, out[0][2])

    def test_guarded_skipped_without_expect(self):
        entries = [(N_RIZHI, T_RIZHI, "guarded")]
        out, applied, skipped = w2s.apply_noise_dict(
            [(0.0, 1.0, N_RIZHI)], entries, None)
        self.assertEqual(0, applied)
        self.assertEqual(1, skipped)
        self.assertEqual(N_RIZHI, out[0][2])

    def test_guarded_fires_when_expect_contains_true(self):
        entries = [(N_RIZHI, T_RIZHI, "guarded")]
        out, applied, skipped = w2s.apply_noise_dict(
            [(0.0, 1.0, N_RIZHI)], entries, T_RIZHI + " x")
        self.assertEqual(1, applied)
        self.assertEqual(0, skipped)
        self.assertEqual(T_RIZHI, out[0][2])

    def test_guarded_skipped_when_expect_lacks_true(self):
        # collision guard: common-word noise must not fire when the
        # piece's own reference has no such true term
        entries = [(N_JIHUA, T_JINHUA, "guarded")]
        out, applied, skipped = w2s.apply_noise_dict(
            [(0.0, 1.0, N_JIHUA)], entries, "unrelated beats")
        self.assertEqual(0, applied)
        self.assertEqual(1, skipped)
        self.assertEqual(N_JIHUA, out[0][2])

    def test_longest_first_prevents_substring_double_fire(self):
        entries = sorted([(N_DAAN, "\u6863\u6848", "guarded"),
                          (N_CHENGSHIDAAN, T_CHENGSHIDAAN, "safe")],
                         key=lambda x: len(x[0]), reverse=True)
        out, applied, _ = w2s.apply_noise_dict(
            [(0.0, 1.0, N_CHENGSHIDAAN)], entries, None)
        self.assertEqual(1, applied)
        self.assertEqual(T_CHENGSHIDAAN, out[0][2])

    def test_timestamps_untouched(self):
        entries = [(N_XINPIAO, T_XINTIAO, "safe")]
        out, _, _ = w2s.apply_noise_dict(
            [(1.5, 2.5, N_XINPIAO + " tail")], entries, None)
        self.assertEqual((1.5, 2.5), (out[0][0], out[0][1]))

    def test_empty_entries_noop(self):
        out, applied, skipped = w2s.apply_noise_dict(
            [(0.0, 1.0, N_RIZHI)], [], None)
        self.assertEqual(0, applied)
        self.assertEqual(0, skipped)
        self.assertEqual(N_RIZHI, out[0][2])


class RealDictContractTests(unittest.TestCase):
    """Regression locks on the shipped data/pipeline dictionary."""

    def test_real_dict_loads_with_entries(self):
        entries = w2s.load_noise_dict(str(REAL_DICT))
        self.assertGreaterEqual(len(entries), 30)
        classes = {cls for _, _, cls in entries}
        self.assertTrue(classes <= {"safe", "guarded"})
        self.assertIn("safe", classes)
        self.assertIn("guarded", classes)

    def test_no_ping_pong_pairs(self):
        # a true term must never also be a noise string, or one
        # replacement could feed the next entry
        entries = w2s.load_noise_dict(str(REAL_DICT))
        noises = {n for n, _, _ in entries}
        trues = {t for _, t, _ in entries}
        self.assertEqual(set(), noises & trues)

    def test_parser_defaults_off(self):
        args = w2s.build_parser().parse_args(
            ["--audio", "a.mp3", "--out", "a.srt"])
        self.assertIsNone(args.noise_dict)
        self.assertIsNone(args.expect)


if __name__ == "__main__":
    unittest.main(verbosity=2)
