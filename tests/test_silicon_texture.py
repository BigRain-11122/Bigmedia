# -*- coding: utf-8 -*-
"""Unit tests for tools/silicon_texture.py -- the tech#259 M0
sentence-picking silicon-identity pre-filter canonized from the R2401
E4 verdict on MC-20261019-DAILY-v71.

Regression locks (the real incidents this module encodes):
- R2401 anchor: DAILY-v71 quote 「听说城主有令，咱先别急着打听」 scored
  E4 6.0 (first break of the v61-v70 8.0 band) precisely because the
  line "fits any dynasty once the title is stripped" -- it MUST
  downgrade (no lexicon hit, and 城主 is deliberately NOT in the
  lexicon: the E4 verdict said the word does not carry the silicon
  identity).
- v61-v70 band positive faces: textured pool lines (脑塔/白光/版本/
  数据...) pass on lexical hits alone.
- REACT/other forms are out of scope by line-shape law (their pool
  rows are real-world mapped; axis_anchor_check guards them), and a
  REACT pool line with zero texture must NOT be reported by the batch
  face.

Run:
    python tests/test_silicon_texture.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))

import silicon_texture  # noqa: E402


# Production anchors (verbatim from the pool / card faces).
V71_QUOTE = "听说城主有令，咱先别急着打听"          # R2401 downgrade anchor
TEXTURED_BRAIN = "脑塔一亮，今儿可有新鲜事？"        # infra hit (脑塔)
TEXTURED_WHITE = "白光一闪，心跳跟着快了几拍"        # infra hit (白光)
TEXTURED_VERSION = "跟版本一起长的娃"                # tech hit (版本)
TEXTURED_DATA = "数据粥铺的口味账又添了一笔"          # tech hit (数据)
GENERIC_MARKET = "别看这市场热闹，咱得守好规矩，才安稳"  # generic pool line
GENERIC_CLOSING = "队形不能乱，人心更不能散。"        # generic closing


def write_card(cards_root, dirname, lines, meta=None):
    d = os.path.join(cards_root, dirname)
    os.makedirs(d, exist_ok=True)
    card = {
        "meta": meta or {"topic": dirname},
        "font": {"h1_size": 44, "h2_size": 40, "subs_size": 24},
        "tail": 0.5,
        "cards": [{"start": 0.0, "end": 3.4, "lines": lines}],
    }
    with open(os.path.join(d, "cards.json"), "w", encoding="utf-8",
              newline="\n") as f:
        json.dump(card, f, ensure_ascii=False, indent=1)
    return d


class TestLineVerdict(unittest.TestCase):
    def test_v71_production_anchor_downgrades(self):
        """The exact R2401 E4 downgrade line must downgrade."""
        v = silicon_texture.line_verdict(V71_QUOTE)
        self.assertEqual(v["verdict"], "downgrade")
        self.assertEqual(v["hits"], [])

    def test_textured_lines_pass_with_category(self):
        for line, cat in ((TEXTURED_BRAIN, "infra"),
                          (TEXTURED_WHITE, "infra"),
                          (TEXTURED_VERSION, "tech"),
                          (TEXTURED_DATA, "tech")):
            v = silicon_texture.line_verdict(line)
            self.assertEqual(v["verdict"], "texture-pass", line)
            self.assertIn(cat, v["categories"], line)

    def test_generic_lines_downgrade(self):
        for line in (GENERIC_MARKET, GENERIC_CLOSING,
                     "街角的咖啡还香"):
            self.assertEqual(
                silicon_texture.line_verdict(line)["verdict"],
                "downgrade", line)

    def test_declared_anchor_upgrades_zero_hit_line(self):
        v = silicon_texture.line_verdict(V71_QUOTE,
                                         anchor="机械×市井反差自述位")
        self.assertEqual(v["verdict"], "anchor-pass")
        self.assertEqual(v["hits"], [])
        self.assertIn("机械×市井反差自述位", v["reason"])

    def test_lexicon_categories_nonempty_and_multichar(self):
        """Every lexicon entry is >=2 chars (single-char CJK matches like
        钢/铁/塔 are false-positive machines and stay banned)."""
        for name, words in silicon_texture.CATEGORIES:
            self.assertTrue(words, name)
            for w in words:
                self.assertGreaterEqual(len(w), 2, name + ":" + w)
        self.assertNotIn("城主", silicon_texture.TECH_WORDS +
                         silicon_texture.INFRA_WORDS +
                         silicon_texture.MECH_IMAGERY)


class TestScanCards(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="st259-")
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def test_daily_card_quote_downgrades(self):
        d = write_card(self.root, "MC-20261019-DAILY-v71",
                       ["城市日签 071", "怀旧轴：「%s」" % V71_QUOTE,
                        "来源行：BigLife 台词池"])
        rows = silicon_texture.scan_cards(d)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["verdict"], "downgrade")
        self.assertEqual(rows[0]["card_verdict"], "downgrade")

    def test_daily_card_with_meta_anchor_passes(self):
        d = write_card(self.root, "MC-20261019-DAILY-v71",
                       ["城市日签 071", "怀旧轴：「%s」" % V71_QUOTE,
                        "来源行：BigLife 台词池"],
                       meta={"silicon_anchor": "连令日×老街坊从容反差锚"})
        rows = silicon_texture.scan_cards(d)
        self.assertEqual(rows[0]["verdict"], "anchor-pass")
        self.assertEqual(rows[0]["card_verdict"], "anchor-pass")

    def test_daily_textured_card_passes(self):
        d = write_card(self.root, "MC-20261019-DAILY-v72",
                       ["城市日签 072", "怀旧轴：「%s」" % TEXTURED_BRAIN,
                        "来源行：BigLife 台词池"])
        rows = silicon_texture.scan_cards(d)
        self.assertEqual(rows[0]["verdict"], "texture-pass")
        self.assertEqual(rows[0]["card_verdict"], "texture-pass")

    def test_react_form_out_of_scope(self):
        d = write_card(self.root, "MC-20261019-REACT-v24",
                       ["城市速报 024", "侠气轴：「%s」" % V71_QUOTE,
                        "C-00012 晨操领队沈佩兰信条：「%s」"
                        % GENERIC_CLOSING])
        rows = silicon_texture.scan_cards(d)
        self.assertEqual(rows[0]["verdict"], "out-of-scope")

    def test_no_cards_json_is_error_row(self):
        rows = silicon_texture.scan_cards(os.path.join(self.root, "void"))
        self.assertEqual(rows[0]["verdict"], "error")


class TestCLI(unittest.TestCase):
    @staticmethod
    def _run(args):
        # house pattern (test_collide_scan): byte capture; the child
        # console emits CJK under the GBK code page, assertion
        # substrings stay ASCII so a replace-decode is contract-safe.
        return subprocess.run(
            [sys.executable, os.path.join(REPO, "tools",
                                          "silicon_texture.py")]
            + list(args),
            capture_output=True, cwd=REPO)

    @staticmethod
    def _out(r):
        return r.stdout.decode("utf-8", errors="replace")

    def test_line_downgrade_rc1(self):
        r = self._run(["--line", V71_QUOTE])
        self.assertEqual(r.returncode, 1)
        self.assertIn("DOWNGRADE", self._out(r))

    def test_line_texture_rc0(self):
        r = self._run(["--line", TEXTURED_BRAIN])
        self.assertEqual(r.returncode, 0)
        self.assertIn("texture-pass", self._out(r))

    def test_anchor_flag_rc0(self):
        r = self._run(["--line", V71_QUOTE, "--anchor", "连令日反差锚"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("anchor-pass", self._out(r))

    def test_usage_error_rc2(self):
        r = self._run([])
        self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main()
