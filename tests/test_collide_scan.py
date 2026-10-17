# -*- coding: utf-8 -*-
"""Unit tests for tools/collide_scan.py -- the tech#191 pool/closing
sentence reuse defense canonized from the R2285/R2321 ad-hoc scans.

Regression locks (the real incidents this module encodes):
- R2321 anchor: REACT-v22 烟火轴 candidate 「刚赚的这份钱，得给孩子买点糖」
  was caught ONLY by a throwaway A6 scan because REACT-v3 already had it --
  the defense must now fire structurally, before any render/disk write.
- R2321 rotation-law anchor: the closing row rotates within its own form;
  the CENSUS-v20 图鉴卡 信条 == REACT-v22 收束行 case is a legal
  cross-form documentary citation and must stay legal.

Run:
    python tests/test_collide_scan.py
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

import collide_scan  # noqa: E402


def write_card(cards_root, dirname, lines):
    d = os.path.join(cards_root, dirname)
    os.makedirs(d, exist_ok=True)
    card = {
        "meta": {"topic": dirname},
        "font": {"h1_size": 44, "h2_size": 40, "subs_size": 24},
        "tail": 0.5,
        "cards": [{"start": 0.0, "end": 3.4, "lines": lines}],
    }
    with open(os.path.join(d, "cards.json"), "w", encoding="utf-8",
              newline="\n") as f:
        json.dump(card, f, ensure_ascii=False, indent=1)
    return d


def react_lines(pool_a, pool_b, pool_c, closing):
    return [
        "城市速报 099",
        "今日热点 · 知乎热榜 2026-10-17",
        "热点正文行甲",
        "热点正文行乙",
        "秩序轴：「%s」" % pool_a,
        "侠气轴：「%s」" % pool_b,
        "逍遥轴：「%s」" % pool_c,
        closing,
    ]


class TestRowShapes(unittest.TestCase):
    def test_pool_row_shapes(self):
        self.assertTrue(collide_scan.is_pool_row("秩序轴：「今儿个结算顺利完成，心里头才踏实」"))
        self.assertTrue(collide_scan.is_pool_row("像素灵池：「喵呜一声，雨中觅食欢腾」"))
        self.assertTrue(collide_scan.is_pool_row("烟火轴：「刚赚的这份钱，得给孩子买点糖」"))
        # closing rows are NOT pool rows (信条 label must not match 轴/池)
        self.assertFalse(collide_scan.is_pool_row("QUANT 食堂信条：「行情再绿，汤是热的。」"))
        self.assertFalse(collide_scan.is_pool_row("伴居灵感条：「蹭饭是门艺术，报恩是门手艺。」"))
        # hot/deck rows are never defense faces
        self.assertFalse(collide_scan.is_pool_row("「机制呢？自我学习呢?」"))
        self.assertFalse(collide_scan.is_pool_row("深夜 V5 正片 17/17 回采入库"))

    def test_closing_row_shapes(self):
        self.assertTrue(collide_scan.is_closing_row("渡轮船长信条：「船稳，人心才稳。」"))
        self.assertTrue(collide_scan.is_closing_row("伴居灵感条：「蹭饭是门艺术，报恩是门手艺。」"))
        self.assertFalse(collide_scan.is_closing_row("秩序轴：「今儿个结算顺利完成，心里头才踏实」"))
        self.assertFalse(collide_scan.is_closing_row("硅基城市雨天律：人人进骑楼，路面可见不到三成"))

    def test_form_of(self):
        self.assertEqual(collide_scan.form_of("MC-20260927-REACT-v3"), "REACT")
        self.assertEqual(collide_scan.form_of("MC-20261017-DIGEST-v22"), "DIGEST")
        self.assertEqual(collide_scan.form_of("MC-20260926-CENSUS-v20"), "CENSUS")
        self.assertIsNone(collide_scan.form_of("MC-20261008-DAILY-v70-tmp"))
        self.assertIsNone(collide_scan.form_of("readme"))


class TestDefenseSemantics(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="collide_r2331_")
        self.root = os.path.join(self.tmp, "cards")
        os.makedirs(self.root, exist_ok=True)
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def test_pool_reuse_blocked_r2321_anchor(self):
        # REACT-v3 historical card already burned the sugar sentence
        write_card(self.root, "MC-20260927-REACT-v3", react_lines(
            "交易盘了，咱就图个心宽",
            "刚赚的这份钱，得给孩子买点糖",
            "喵呜一声，今日利润喜上眉梢",
            "渡轮船长信条：「船稳，人心才稳。」"))
        cur = write_card(self.root, "MC-20261018-REACT-v23", react_lines(
            "全新的秩序句",
            "刚赚的这份钱，得给孩子买点糖",  # R2321 anchor: must fire now
            "全新的逍遥句",
            "夜灯员信条：「灯不问来路，只管照路。」"))
        v = collide_scan.scan_cards(cur)
        self.assertEqual(len(v), 1)
        self.assertIn("刚赚的这份钱，得给孩子买点糖", v[0])
        self.assertIn("MC-20260927-REACT-v3", v[0])
        self.assertIn("pool row", v[0])

    def test_pool_fresh_sentences_pass(self):
        write_card(self.root, "MC-20260927-REACT-v3", react_lines(
            "交易盘了，咱就图个心宽",
            "刚赚的这份钱，得给孩子买点糖",
            "喵呜一声，今日利润喜上眉梢",
            "渡轮船长信条：「船稳，人心才稳。」"))
        cur = write_card(self.root, "MC-20261018-REACT-v23", react_lines(
            "全新的秩序句甲",
            "全新的侠气句乙",
            "全新的逍遥句丙",
            "夜灯员信条：「灯不问来路，只管照路。」"))
        self.assertEqual(collide_scan.scan_cards(cur), [])

    def test_closing_rotation_same_form_blocked(self):
        write_card(self.root, "MC-20260927-REACT-v3", react_lines(
            "甲句", "乙句", "丙句",
            "渡轮船长信条：「船稳，人心才稳。」"))
        cur = write_card(self.root, "MC-20261018-REACT-v23", react_lines(
            "丁句", "戊句", "己句",
            "老船长信条：「船稳，人心才稳。」"))  # same-form closing reuse
        v = collide_scan.scan_cards(cur)
        self.assertEqual(len(v), 1)
        self.assertIn("closing row", v[0])
        self.assertIn("REACT", v[0])

    def test_closing_cross_form_stays_legal_r2321_citation(self):
        # CENSUS-v20 图鉴卡 carries the same belief text -- archival
        # citation across forms is legal (R2321 note), must NOT block a
        # REACT closing.
        write_card(self.root, "MC-20260926-CENSUS-v20",
                   ["图鉴 020", "伴居灵", "个性字段", "能力字段", "档案注记",
                    "伴居灵信条：「蹭饭是门艺术，报恩是门手艺。」"])
        cur = write_card(self.root, "MC-20261017-REACT-v22", react_lines(
            "今儿个结算顺利完成，心里头才踏实",
            "算盘这会儿打清了，该收心回家了",
            "偶尔空手而归，也挺好",
            "伴居灵感条：「蹭饭是门艺术，报恩是门手艺。」"))
        self.assertEqual(collide_scan.scan_cards(cur), [])

    def test_self_dir_never_blocks_rerender(self):
        cur = write_card(self.root, "MC-20261018-REACT-v23", react_lines(
            "某秩序句", "某侠气句", "某逍遥句",
            "夜灯员信条：「灯不问来路，只管照路。」"))
        # re-scan the same card: its own sentences must not self-block
        self.assertEqual(collide_scan.scan_cards(cur), [])

    def test_tmp_dirs_never_poison_baseline(self):
        # a discarded draft sentence lived only in a -tmp dir: reusing it
        # in a fresh card must stay legal
        write_card(self.root, "MC-20261018-REACT-v23-tmp", react_lines(
            "弃稿秩序句", "弃稿侠气句", "弃稿逍遥句",
            "夜灯员信条：「灯不问来路，只管照路。」"))
        cur = write_card(self.root, "MC-20261018-REACT-v23", react_lines(
            "弃稿秩序句", "弃稿侠气句", "弃稿逍遥句",
            "夜灯员信条：「灯不问来路，只管照路。」"))
        self.assertEqual(collide_scan.scan_cards(cur), [])

    def test_hot_deck_rows_ignored_digest_face(self):
        # DIGEST-style rows (no pool/closing shape) never trip the defense:
        # the CEO-quote row is a baseline sentence, but the scanned card has
        # no pool/closing rows, so it stays clean even with identical deck rows
        write_card(self.root, "MC-20261017-DIGEST-v22",
                   ["城市盘点 022", "治本大修日", "「机制呢？自我学习呢?」",
                    "V4 终审未过 → V5 17 镜重烧单派发",
                    "全机制普查 113 项任务 · 66 行法"])
        cur = write_card(self.root, "MC-20261018-DIGEST-v23",
                         ["城市盘点 023", "另一标题",
                          "「机制呢？自我学习呢?」",
                          "V4 终审未过 → V5 17 镜重烧单派发"])
        self.assertEqual(collide_scan.scan_cards(cur), [])

    def test_missing_cards_json_reported(self):
        empty = os.path.join(self.root, "MC-20261018-REACT-v24")
        os.makedirs(empty, exist_ok=True)
        v = collide_scan.scan_cards(empty)
        self.assertEqual(len(v), 1)
        self.assertIn("no loadable cards.json", v[0])


class TestCliAndDriverIntegration(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="collide_cli_r2331_")
        self.root = os.path.join(self.tmp, "cards")
        os.makedirs(self.root, exist_ok=True)
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def _run(self, *args):
        return subprocess.run(
            [sys.executable] + list(args),
            capture_output=True, cwd=REPO)

    @staticmethod
    def _out(r):
        # child console emits CJK under the GBK code page; assertion
        # substrings are ASCII so a replace-decode is contract-safe
        return (r.stdout.decode("utf-8", errors="replace")
                + r.stderr.decode("utf-8", errors="replace"))

    def test_cli_rc1_on_collision(self):
        write_card(self.root, "MC-20260927-REACT-v3", react_lines(
            "交易盘了，咱就图个心宽",
            "刚赚的这份钱，得给孩子买点糖",
            "喵呜一声，今日利润喜上眉梢",
            "渡轮船长信条：「船稳，人心才稳。」"))
        cur = write_card(self.root, "MC-20261018-REACT-v23", react_lines(
            "全新秩序句", "刚赚的这份钱，得给孩子买点糖", "全新逍遥句",
            "夜灯员信条：「灯不问来路，只管照路。」"))
        r = self._run(os.path.join("tools", "collide_scan.py"),
                      "--cards-dir", cur)
        self.assertEqual(r.returncode, 1)
        self.assertIn("COLLIDE-FAIL", self._out(r))

    def test_cli_rc0_on_clean(self):
        write_card(self.root, "MC-20260927-REACT-v3", react_lines(
            "甲句", "乙句", "丙句", "渡轮船长信条：「船稳，人心才稳。」"))
        cur = write_card(self.root, "MC-20261018-REACT-v23", react_lines(
            "丁句", "戊句", "己句", "夜灯员信条：「灯不问来路，只管照路。」"))
        r = self._run(os.path.join("tools", "collide_scan.py"),
                      "--cards-dir", cur)
        self.assertEqual(r.returncode, 0)
        self.assertIn("PASS", self._out(r))

    def test_lcard_m2_refuses_render_before_disk_write(self):
        # the driver integration law: a collision hit = exit 1 with ZERO
        # disk write -- no em-check file, no subs, no poster, no cards.json
        # rewrite. The card under scan reuses the v3 sugar sentence, so the
        # tech#191 gate must fire before the em ladder even runs.
        write_card(self.root, "MC-20260927-REACT-v3", react_lines(
            "交易盘了，咱就图个心宽",
            "刚赚的这份钱，得给孩子买点糖",
            "喵呜一声，今日利润喜上眉梢",
            "渡轮船长信条：「船稳，人心才稳。」"))
        cur = write_card(self.root, "MC-20261018-REACT-v23", react_lines(
            "全新秩序句", "刚赚的这份钱，得给孩子买点糖", "全新逍遥句",
            "夜灯员信条：「灯不问来路，只管照路。」"))
        before = open(os.path.join(cur, "cards.json"), encoding="utf-8").read()
        r = self._run(os.path.join("tools", "lcard_m2.py"),
                      "--cards-dir", cur,
                      "--subs-line", "热点转述自知乎热榜·反应与信条皆取自虚构城市档案",
                      "--tag", "r2331t")
        self.assertEqual(r.returncode, 1)
        out = self._out(r)
        self.assertIn("COLLIDE-FAIL", out)
        self.assertIn("tech#191", out)
        # zero disk write: cards.json byte-identical, no em-check, no poster
        after = open(os.path.join(cur, "cards.json"), encoding="utf-8").read()
        self.assertEqual(before, after)
        self.assertFalse(
            os.path.exists(os.path.join(cur, "em-check-r2331t.txt")))
        png = os.path.join(cur, "MC-20261018-REACT-v23.png")
        self.assertFalse(os.path.exists(png))
        self.assertFalse(os.path.exists(os.path.join(cur, "subs.srt")))


if __name__ == "__main__":
    unittest.main()
