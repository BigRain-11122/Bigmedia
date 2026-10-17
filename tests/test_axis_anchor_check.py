# -*- coding: utf-8 -*-
"""Unit tests for tools/axis_anchor_check.py -- the tech#192 M1
axis-selection event-anchoring pre-check (advisory, never a hard gate).

Regression anchor (E4 live-fire, review-20261017-mcreact-v22 L39/L41):
REACT-v22 reaction rows read as universal templates with no event
anchoring (万能句式缺事件锚定) while every structural gate passed --
the pre-check exists to surface that gap at M1 selection time, with
the swap-axis hint being advisory and the verbatim 纪实律 untouched.

All brain-lane flights are mocked -- unit tests never burn a flight.
Run:
    python tests/test_axis_anchor_check.py
"""

import json
import os
import shutil
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))

import axis_anchor_check as aac  # noqa: E402
import collide_scan  # noqa: E402

# REACT-v22 production anchor (real card face, real E4 flag target)
V22_TOPIC = ("女子在自己手机上登录前男友账号以「1314」等金额转走近二十万，"
             "法院判决全部返还，如何从法律角度解读？")
V22_ROWS = [
    "秩序轴：「今儿个结算顺利完成，心里头才踏实」",
    "侠气轴：「算盘这会儿打清了，该收心回家了」",
    "逍遥轴：「偶尔空手而归，也挺好」",
    "伴居灵感条：「蹭饭是门艺术，报恩是门手艺。」",
]


def v22_card_dir(root):
    d = os.path.join(root, "MC-20261017-REACT-v22")
    os.makedirs(d, exist_ok=True)
    lines = [
        "城市速报 022",
        "今日热点 · 知乎热榜 2026-10-17",
        "女子在自己手机上登录前男友账号以「1314」等金额转走近二十万，",
        "法院判决全部返还，如何从法律角度解读？",
    ] + V22_ROWS
    card = {"meta": {"topic": "MC-20261017-REACT-v22"},
            "cards": [{"start": 0.0, "end": 2.6, "lines": lines}]}
    with open(os.path.join(d, "cards.json"), "w", encoding="utf-8",
              newline="\n") as f:
        json.dump(card, f, ensure_ascii=False, indent=1)
    return d


def brain_ok(scores, eyes=("转账", "返还", "判决")):
    """Mock brain wire payload builder: 1-based idx matching rows order."""
    body = {"题眼": list(eyes),
            "rows": [{"idx": i + 1, "score": s, "reason": "测试理由%d" % (i + 1)}
                     for i, s in enumerate(scores)]}
    return (0, json.dumps(body, ensure_ascii=False))


class TestExtractFaces(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="aac-test-")
        self.addCleanup(shutil.rmtree, self.root, True)

    def test_react_card_faces(self):
        d = v22_card_dir(self.root)
        lines = collide_scan.load_lines(d)
        topic, rows, closing = aac.extract_faces(lines)
        self.assertIn("1314", topic)
        self.assertIn("法院判决", topic)  # two-line hot title joined
        self.assertEqual(len(rows), 3)
        self.assertTrue(all(collide_scan.is_pool_row(r) for r in rows))
        self.assertTrue(collide_scan.is_closing_row(closing))

    def test_non_react_passthrough(self):
        d = os.path.join(self.root, "MC-20261017-QUOTE-v9")
        os.makedirs(d, exist_ok=True)
        lines = ["城市语录 009", "老街的灯光，照亮了我半辈子的梦",
                 "来源：BigLife 台词池 night 桶 verbatim"]
        topic, rows, closing = aac.extract_faces(lines)
        self.assertIsNone(topic)
        self.assertEqual(rows, [])
        self.assertIsNone(closing)

    def test_pool_rows_without_hot_header(self):
        lines = ["城市速报 099"] + V22_ROWS
        topic, rows, closing = aac.extract_faces(lines)
        self.assertIsNone(topic)
        self.assertEqual(len(rows), 3)
        self.assertTrue(collide_scan.is_closing_row(closing))


class TestParseScores(unittest.TestCase):
    def test_strict_json(self):
        text = json.dumps({"题眼": ["转账", "返还"],
                          "rows": [{"idx": 1, "score": 5.0, "reason": "弱"},
                                   {"idx": 2, "score": "7.5", "reason": "字符串分数"},
                                   {"idx": 3, "score": 8, "reason": "整数分数"}]},
                         ensure_ascii=False)
        eyes, scores, reasons = aac.parse_scores(text, 3)
        self.assertEqual(eyes, ["转账", "返还"])
        self.assertEqual(scores, [5.0, 7.5, 8.0])
        self.assertEqual(len(reasons), 3)

    def test_pollution_around_json_and_clamp(self):
        text = ('前置噪声 row: {"题眼": ["判决"], "rows": ['
                '{"idx": 1, "score": 11, "reason": "超界"},'
                '{"idx": 2, "score": -2, "reason": "负分"}]} 尾部噪声')
        _, scores, _ = aac.parse_scores(text, 2)
        self.assertEqual(scores, [10.0, 0.0])  # clamped to [0, 10]

    def test_idx_mismatch_raises(self):
        text = json.dumps({"题眼": ["x"], "rows": [
            {"idx": 1, "score": 5.0, "reason": "缺 2"}]})
        with self.assertRaises(ValueError):
            aac.parse_scores(text, 2)

    def test_no_json_raises(self):
        with self.assertRaises(ValueError):
            aac.parse_scores("模型拒绝输出 JSON", 1)


class TestVerdict(unittest.TestCase):
    def test_below_threshold_indexes(self):
        self.assertEqual(aac.verdict([5.0, 7.0, 6.0], 6.0), [0])
        self.assertEqual(aac.verdict([7.0, 8.0], 6.0), [])
        self.assertEqual(aac.verdict([1.0, 2.0, 3.0], 6.0), [0, 1, 2])


class TestRunCheck(unittest.TestCase):
    def _patch(self, ret):
        self._orig = aac.call_model
        aac.call_model = lambda model, prompt, timeout: ret
        self.addCleanup(setattr, aac, "call_model", self._orig)

    def test_v22_anchor_all_hint(self):
        # E4 live-fire regression: all four v22 rows scored weak
        self._patch(brain_ok([4.0, 3.0, 5.5, 3.5]))
        result = aac.run_check(V22_TOPIC, V22_ROWS, 6.0, 240, "m")
        self.assertEqual(result["rc"], 1)  # advisory hints, never a block
        self.assertEqual(result["hint_idx"], [0, 1, 2, 3])
        self.assertTrue(result["advisory"])
        self.assertEqual(len(result["rows"]), 4)
        self.assertEqual(result["rows"][0]["row"], V22_ROWS[0])  # rows passed verbatim

    def test_all_pass_rc0(self):
        self._patch(brain_ok([7.5, 8.0, 9.0, 6.5]))
        result = aac.run_check(V22_TOPIC, V22_ROWS, 6.0, 240, "m")
        self.assertEqual(result["rc"], 0)
        self.assertEqual(result["hint_idx"], [])

    def test_brain_down_rc3_unverified(self):
        self._patch((3, "brain wire timeout (240s cap)"))
        result = aac.run_check(V22_TOPIC, V22_ROWS, 6.0, 240, "m")
        self.assertEqual(result["rc"], 3)
        self.assertIn("timeout", result["unverified_reason"])

    def test_brain_garbage_rc2(self):
        self._patch((0, "我觉得这些句子都挺好的"))
        result = aac.run_check(V22_TOPIC, V22_ROWS, 6.0, 240, "m")
        self.assertEqual(result["rc"], 2)
        self.assertIn("parse_error", result)


class TestMainCli(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="aac-cli-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self._orig = aac.call_model
        aac.call_model = lambda model, prompt, timeout: brain_ok([4.0, 3.0, 5.5, 3.5])
        self.addCleanup(setattr, aac, "call_model", self._orig)

    def test_cards_dir_end_to_end(self):
        d = v22_card_dir(self.root)
        rc = aac.main(["--cards-dir", d, "--json"])
        self.assertEqual(rc, 1)  # hints present, advisory

    def test_cards_dir_missing_fixture(self):
        rc = aac.main(["--cards-dir", os.path.join(self.root, "nope")])
        self.assertEqual(rc, 2)

    def test_manual_mode(self):
        aac.call_model = lambda model, prompt, timeout: brain_ok([4.0])
        rc = aac.main(["--topic", V22_TOPIC, "--row", V22_ROWS[0],
                       "--threshold", "3.0"])
        self.assertEqual(rc, 0)  # 4.0 >= 3.0 -> clean

    def test_pool_rows_without_topic_usage_error(self):
        rc = aac.main(["--row", V22_ROWS[0]])  # no --topic, no header
        self.assertEqual(rc, 2)

    def test_empty_face_passthrough_rc0(self):
        d = os.path.join(self.root, "MC-20261017-QUOTE-v9")
        os.makedirs(d, exist_ok=True)
        card = {"meta": {"topic": "q"}, "cards": [
            {"start": 0.0, "end": 2.6,
             "lines": ["城市语录 009", "老街的灯光，照亮了我半辈子的梦"]}]}
        with open(os.path.join(d, "cards.json"), "w", encoding="utf-8",
                  newline="\n") as f:
            json.dump(card, f, ensure_ascii=False, indent=1)
        rc = aac.main(["--cards-dir", d])
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
