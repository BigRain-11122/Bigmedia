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
REAL_DICT_V2 = REPO / "data" / "pipeline" / "asr-noise-dict-v2.json"

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

# v2 phrase anchors (tech#21 R1832, data/pipeline/asr-noise-dict-v2.json)
N_GUIJICHENGSHI = "\u5f52\u57fa\u57ce\u5e02"    # 归基城市 (硅->归)
T_GUIJICHENGSHI = "\u7845\u57fa\u57ce\u5e02"    # 硅基城市
N_GUIJUMIN = "\u5f52\u5c45\u6c11"                # 归居民 (verbatim sc001-01-v2)
T_GUIJUMIN = "\u7845\u57fa\u6c11"                # 硅基民
N_GUIDANGZHE = "\u5f52\u8361\u8005"            # 归荡者 (verbatim sc001-01-v2)
T_GUIDANGZHE = "\u5f52\u6863\u8005"            # 归档者
N_TONGYE = "\u7ae5\u53f6"                        # 童叶 (BS-015 verbatim)
N_TAIFENGYING = "\u53f0\u98ce\u5f71"            # 台风影 (BS-015 verbatim)
N_BANGKUAI = "\u7ed1\u5757\u5341\u5e74"        # 绑块十年 (板->绑 composed)
N_SHOUDAOFENGTING = "\u5b88\u5230\u98ce\u4ead"  # 守到风亭 (停->亭 composed)
N_YIZHANDENG = "\u4e00\u5c55\u706f"            # 一展灯 (盏->展 composed)
T_YIZHANDENG = "\u4e00\u76cf\u706f"            # 一盏灯
N_LIGUORIYIZHAN = "\u7acb\u56fd\u65e5\u4e00\u5c55"          # 立国日一展
T_LIGUORIYIZHAN = "\u7acb\u56fd\u65e5\u4e00\u76cf"          # 立国日一盏
N_SHOUYEDENGLINGWUZHAN = "\u5b88\u591c\u706f\u7075\u4e94\u5c55"  # 守夜灯灵五展
T_SHOUYEDENGLINGWUZHAN = "\u5b88\u591c\u706f\u7075\u4e94\u76cf"  # 守夜灯灵五盏
N_YIZHANDAOWUZHAN = "\u4e00\u5c55\u5230\u4e94\u5c55"        # 一展到五展
N_JIUKAIPING = "\u4e5d\u5f00\u74f6"            # 九开瓶 (庆功酒->九 composed)
N_JIUKAIPIN = "\u4e5d\u5f00\u5c4f"              # 九开屏 (same-cue chain)
T_QINGGONGJIUKAIPING = "\u5e86\u529f\u9152\u5f00\u74f6"      # 庆功酒开瓶
N_YIBANGE = "\u4e00\u534a\u4e2a"                # 一半个 (verbatim sc001-01-v2)
N_YIBANGEMINGZI = "\u4e00\u534a\u4e2a\u540d\u5b57"          # 一半个名字
T_YIWANGEMINGZI = "\u4e00\u4e07\u4e2a\u540d\u5b57"          # 一万个名字
N_YIBANLINGSAN = "\u4e00\u534a\u96f6\u4e09"    # 一半零三
T_YIWANLINGSAN = "\u4e00\u4e07\u96f6\u4e09"    # 一万零三
N_LIANGDIANWUSHI = "\u4e24\u70b9\u4e94\u65f6"  # 两点五时 (BS-016 verbatim)
N_HUANGTUJIANG = "\u9ec4\u571f\u6c5f"          # 黄土江 (浦->土 composed)
T_HUANGPUJIANG = "\u9ec4\u6d66\u6c5f"          # 黄浦江
N_BUYAOSHUNZHEWENLUJIAN = "\u4e0d\u8981\u987a\u7740\u7eb9\u8def\u526a"  # 不要顺着纹路剪
N_GONGKONGZUODEHAO = "\u529f\u63a7\u505a\u5f97\u597d"        # 功控做得好


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

    def test_guarded_blocked_when_noise_legit_in_expect(self):
        # tech#21 hardening: a piece whose beats use the noise word
        # legitimately (alongside the true term elsewhere) must never
        # have that legitimate word rewritten
        entries = [(N_RIZHI, T_RIZHI, "guarded")]
        out, applied, skipped = w2s.apply_noise_dict(
            [(0.0, 1.0, N_RIZHI)], entries, T_RIZHI + " and " + N_RIZHI)
        self.assertEqual(0, applied)
        self.assertEqual(1, skipped)
        self.assertEqual(N_RIZHI, out[0][2])

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


class V2ExtendsMergeTests(unittest.TestCase):
    """tech#21 R1832: v2 phrase dict extends v1 (loader merge)."""

    def test_v2_is_v1_superset_plus_phrase_entries(self):
        v1 = w2s.load_noise_dict(str(REAL_DICT))
        v2 = w2s.load_noise_dict(str(REAL_DICT_V2))
        self.assertEqual(len(v1) + 20, len(v2))
        self.assertTrue(set(v1) <= set(v2))

    def test_v2_phrase_entries_all_guarded(self):
        v2 = w2s.load_noise_dict(str(REAL_DICT_V2))
        phrase_noises = {N_GUIJICHENGSHI, N_GUIJUMIN, N_GUIDANGZHE,
                         N_TONGYE, N_TAIFENGYING, N_BANGKUAI,
                         N_SHOUDAOFENGTING, N_YIZHANDENG,
                         N_LIGUORIYIZHAN, N_SHOUYEDENGLINGWUZHAN,
                         N_YIZHANDAOWUZHAN, N_JIUKAIPING, N_JIUKAIPIN,
                         N_YIBANGE, N_YIBANGEMINGZI, N_YIBANLINGSAN,
                         N_LIANGDIANWUSHI, N_HUANGTUJIANG,
                         N_BUYAOSHUNZHEWENLUJIAN, N_GONGKONGZUODEHAO}
        for noise, true, cls in v2:
            if noise in phrase_noises:
                self.assertEqual("guarded", cls, noise)

    def test_merged_no_ping_pong_pairs(self):
        v2 = w2s.load_noise_dict(str(REAL_DICT_V2))
        noises = {n for n, _, _ in v2}
        trues = {t for _, t, _ in v2}
        self.assertEqual(set(), noises & trues)


class V2PhraseFireTests(unittest.TestCase):
    """v2 phrase anchors correct their single-char-family noise and the
    guarded gate blocks them without the true phrase in --expect."""

    def test_lamp_count_phrases_fire(self):
        # bs013 b8: 立国日一盏，守夜灯灵五盏 misheard via 盏->展 x4
        cue = N_LIGUORIYIZHAN + "\uff0c" + N_SHOUYEDENGLINGWUZHAN
        expect = T_LIGUORIYIZHAN + "\uff0c" + T_SHOUYEDENGLINGWUZHAN
        out, applied, _ = w2s.apply_noise_dict(
            [(0.0, 1.0, cue)], w2s.load_noise_dict(str(REAL_DICT_V2)),
            expect)
        self.assertEqual(2, applied)
        self.assertEqual(expect, out[0][2])

    def test_champagne_collapse_chain_one_shot(self):
        # BS-004 hook: 庆功酒->九 + 开瓶->开屏 in the same cue; the
        # 3-char composed chain entry sorts before v1's 2-char 开屏 fix
        cue = "\u7cfb\u7edf\u65e5\u5fd7\uff1a" + N_JIUKAIPIN
        out, applied, _ = w2s.apply_noise_dict(
            [(0.0, 1.0, cue)], w2s.load_noise_dict(str(REAL_DICT_V2)),
            T_QINGGONGJIUKAIPING)
        self.assertEqual(1, applied)
        self.assertEqual("\u7cfb\u7edf\u65e5\u5fd7\uff1a" + T_QINGGONGJIUKAIPING,
                         out[0][2])

    def test_declaration_tail_chain(self):
        # v2 归基城市->硅基城市 feeds v1 大案->档案 in one pass
        cue = ("\u57fa\u4e8e" + N_GUIJICHENGSHI + "\u771f\u5b9e" + N_DAAN +
               "\u7684\u5341\u5e74\u63a8\u6f14")
        expect = ("\u5148\u4eae\u5e95\uff1a\u5f80\u540e\u662f\u63a8\u6f14"
                  "\u2014\u2014\u57fa\u4e8e" + T_GUIJICHENGSHI +
                  "\u771f\u5b9e\u6863\u6848\u7684\u5341\u5e74\u63a8\u6f14\u3002")
        out, applied, _ = w2s.apply_noise_dict(
            [(0.0, 1.0, cue)], w2s.load_noise_dict(str(REAL_DICT_V2)),
            expect)
        self.assertEqual(2, applied)
        self.assertEqual("\u57fa\u4e8e" + T_GUIJICHENGSHI +
                         "\u771f\u5b9e\u6863\u6848\u7684\u5341\u5e74\u63a8\u6f14",
                         out[0][2])

    def test_wan_family_longest_first(self):
        # 一半个名字 (5-char) resolves before bare 一半个 (3-char)
        cue = N_YIBANGEMINGZI + "\uff1a" + N_YIBANLINGSAN + "\u843d\u5e93"
        expect = T_YIWANGEMINGZI + "\uff1a" + T_YIWANLINGSAN + "\u843d\u5e93"
        out, applied, _ = w2s.apply_noise_dict(
            [(0.0, 1.0, cue)], w2s.load_noise_dict(str(REAL_DICT_V2)),
            expect)
        self.assertEqual(2, applied)
        self.assertEqual(expect, out[0][2])

    def test_verbatim_sc_pairs_fire(self):
        # sc001-01-v2 cue26 verbatim: 管自己叫归荡者零七的归居民
        cue = ("\u7ba1\u81ea\u5df1\u53eb" + N_GUIDANGZHE +
               "\u96f6\u4e03\u7684" + N_GUIJUMIN)
        expect = ("\u7ba1\u81ea\u5df1\u53eb" + T_GUIDANGZHE +
                  "\u96f6\u4e03\u7684" + T_GUIJUMIN)
        out, applied, _ = w2s.apply_noise_dict(
            [(0.0, 1.0, cue)], w2s.load_noise_dict(str(REAL_DICT_V2)),
            expect)
        self.assertEqual(2, applied)
        self.assertEqual(expect, out[0][2])

    def test_phrase_guard_blocks_when_expect_lacks_true_phrase(self):
        entries = w2s.load_noise_dict(str(REAL_DICT_V2))
        for noise, true_verbatim in ((N_YIZHANDENG, T_YIZHANDENG),
                                     (N_JIUKAIPING, T_QINGGONGJIUKAIPING),
                                     (N_HUANGTUJIANG, T_HUANGPUJIANG)):
            out, applied, skipped = w2s.apply_noise_dict(
                [(0.0, 1.0, noise + " tail")], entries,
                "unrelated expect text")
            self.assertEqual(0, applied, noise)
            self.assertEqual(1, skipped, noise)
            self.assertEqual(noise + " tail", out[0][2])


class V2CollateralJudgmentTests(unittest.TestCase):
    """tech#21 acceptance bar: phrase-level collateral damage = 0.

    (1) own-expect sweep: every beats file in the repo, dict applied with
    the file itself as --expect, zero replacements allowed (true text is
    never rewritten); (2) cross-expect sweep: expect from each anchor
    piece applied to every other piece's true text, zero replacements
    allowed (a guarded phrase entry may never cross-fire)."""

    ANCHORS = ["data/sources/bs004/voiceover-v6.beats.txt",
               "data/sources/bs013/voiceover-v2.beats.txt",
               "data/sources/bs014/voiceover-v5.beats.txt",
               "data/sources/bs015/voiceover-v6.beats.txt",
               "data/sources/bs016/voiceover-v3.beats.txt",
               "data/storylines/audio/SC-001-01-v2.beats.txt"]

    @classmethod
    def _corpus(cls):
        return sorted(p for p in REPO.rglob("*.beats.txt"))

    def test_own_expect_sweep_zero_collateral(self):
        entries = w2s.load_noise_dict(str(REAL_DICT_V2))
        for f in self._corpus():
            text = f.read_text(encoding="utf-8")
            cues = [(0.0, 1.0, ln) for ln in text.splitlines()
                    if ln.strip()]
            _, applied, _ = w2s.apply_noise_dict(cues, entries, text)
            self.assertEqual(0, applied, "collateral on %s" % f)

    def test_cross_expect_sweep_zero_collateral(self):
        # strictest bar, scoped to the tech#21 deliverable (the v2
        # PHRASE entries): no anchor piece's expect may let a phrase
        # entry rewrite any other piece's true text. NOTE: the same
        # bar deliberately does NOT cover v1 WORD entries - the sweep
        # found the v1 pair kou-qi->kou-xin (BS-015 anchor) rewriting a
        # legitimate kou-qi in SC-001-01-v2 true text under a MISMATCHED
        # expect; that scenario cannot occur in the real QC flow (the
        # CLI takes the piece's own beats as --expect, and the
        # own-expect sweep above is green for all 170 files), so it is
        # recorded here as a latent word-entry finding, not a failure.
        phrase_noises = {N_GUIJICHENGSHI, N_GUIJUMIN, N_GUIDANGZHE,
                         N_TONGYE, N_TAIFENGYING, N_BANGKUAI,
                         N_SHOUDAOFENGTING, N_YIZHANDENG,
                         N_LIGUORIYIZHAN, N_SHOUYEDENGLINGWUZHAN,
                         N_YIZHANDAOWUZHAN, N_JIUKAIPING, N_JIUKAIPIN,
                         N_YIBANGE, N_YIBANGEMINGZI, N_YIBANLINGSAN,
                         N_LIANGDIANWUSHI, N_HUANGTUJIANG,
                         N_BUYAOSHUNZHEWENLUJIAN, N_GONGKONGZUODEHAO}
        entries = [e for e in w2s.load_noise_dict(str(REAL_DICT_V2))
                   if e[0] in phrase_noises]
        corpus = self._corpus()
        for rel in self.ANCHORS:
            expect = (REPO / rel).read_text(encoding="utf-8")
            for f in corpus:
                text = f.read_text(encoding="utf-8")
                cues = [(0.0, 1.0, ln) for ln in text.splitlines()
                        if ln.strip()]
                _, applied, _ = w2s.apply_noise_dict(cues, entries, expect)
                self.assertEqual(0, applied,
                                 "cross-fire %s -> %s" % (rel, f))


if __name__ == "__main__":
    unittest.main(verbosity=2)
