# -*- coding: utf-8 -*-
"""Minimal unit tests for the card timeline renderer (src/render/).

Pure functions only (SRT parse / cards load / plan build): no ffmpeg run,
no font file needed, real data/ never touched. Chinese strings appear as
\\uXXXX escapes per the ASCII encoding rule (same as make_draft.py).

Run:
    python tests/test_render_card.py
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "render"))

import render_card_video as rcv  # noqa: E402


def cards_cfg(notice="AI generated content", cards=None):
    return {
        "video": {"width": 1080, "height": 1920, "fps": 30, "bg": "black"},
        "font": {"file": "C:/fake/font.ttc", "cards_size": 60, "subs_size": 44,
                 "aigc_size": 30, "subs_bottom": 300, "line_spacing": 14},
        "aigc_notice": notice,
        "tail": 0.8,
        "cards": cards if cards is not None else [
            {"start": 0, "end": 3, "lines": ["a", "b"]},
            {"start": 3, "end": 15, "lines": ["c"]},
        ],
    }


SRT_OK = "\n".join([
    "1", "00:00:00,000 --> 00:00:03,000",
    "three companies, one human",
    "",
    "2", "00:00:03,000 --> 00:00:06,500",
    "only one line",
    "",
])

SRT_CJK = "\n".join([
    "1", "00:00:00,000 --> 00:00:03,000",
    "\u4e09\u5bb6 AI \u516c\u53f8",
    "",
])


class TestParseSrt(unittest.TestCase):
    def test_ok(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "subs.srt"
            p.write_text(SRT_OK, encoding="utf-8")
            cues = rcv.parse_srt(p)
        self.assertEqual(2, len(cues))
        self.assertEqual((0.0, 3.0, "three companies, one human"), cues[0])
        self.assertEqual((3.0, 6.5, "only one line"), cues[1])

    def test_cjk_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "subs.srt"
            p.write_text(SRT_CJK, encoding="utf-8")
            cues = rcv.parse_srt(p)
        self.assertEqual("\u4e09\u5bb6 AI \u516c\u53f8", cues[0][2])

    def test_rejects_missing_timing(self):
        bad = "1\n00:00:00,000 -x- 00:00:03,000\ntext\n"
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "subs.srt"
            p.write_text(bad, encoding="utf-8")
            with self.assertRaises(ValueError):
                rcv.parse_srt(p)

    def test_rejects_overlap(self):
        bad = ("1\n00:00:00,000 --> 00:00:05,000\na\n\n"
               "2\n00:00:04,000 --> 00:00:06,000\nb\n")
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "subs.srt"
            p.write_text(bad, encoding="utf-8")
            with self.assertRaises(ValueError):
                rcv.parse_srt(p)

    def test_rejects_bad_time(self):
        bad = "1\n00:00:00 --> 00:00:03,000\ntext\n"
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "subs.srt"
            p.write_text(bad, encoding="utf-8")
            with self.assertRaises(ValueError):
                rcv.parse_srt(p)


class TestLoadCards(unittest.TestCase):
    def _write(self, d, cfg):
        p = Path(d) / "cards.json"
        p.write_text(json.dumps(cfg, ensure_ascii=False), encoding="utf-8")
        return p

    def test_ok(self):
        with tempfile.TemporaryDirectory() as d:
            cfg = rcv.load_cards(self._write(d, cards_cfg()))
        self.assertEqual(2, len(cfg["cards"]))

    def test_aigc_notice_red_line(self):
        # empty notice must be refused: AIGC labeling is a red line
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                rcv.load_cards(self._write(d, cards_cfg(notice="   ")))

    def test_missing_top_key(self):
        cfg = cards_cfg()
        del cfg["font"]
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                rcv.load_cards(self._write(d, cfg))

    def test_card_overlap(self):
        cfg = cards_cfg(cards=[
            {"start": 0, "end": 5, "lines": ["a"]},
            {"start": 4, "end": 8, "lines": ["b"]},
        ])
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                rcv.load_cards(self._write(d, cfg))

    def test_card_empty_lines(self):
        cfg = cards_cfg(cards=[{"start": 0, "end": 5, "lines": ["", "  "]}])
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                rcv.load_cards(self._write(d, cfg))

    def test_font_key_required(self):
        cfg = cards_cfg()
        del cfg["font"]["subs_bottom"]
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                rcv.load_cards(self._write(d, cfg))


class TestWrap(unittest.TestCase):
    def test_long_cjk_line_wraps(self):
        # 26 CJK chars at 44px on a 1080px frame: budget ~20.9 em -> 2 lines
        text = "\u8f6c" * 26
        wrapped = rcv.wrap_for_width(text, 44, 1080)
        lines = wrapped.split("\n")
        self.assertEqual(2, len(lines))
        for ln in lines:
            self.assertLessEqual(len(ln), 21)

    def test_short_line_untouched(self):
        text = "hello world"
        self.assertEqual(text, rcv.wrap_for_width(text, 44, 1080))

    def test_existing_newline_respected(self):
        text = "aaa\nbbb"
        self.assertEqual("aaa\nbbb", rcv.wrap_for_width(text, 44, 1080))

    def test_narrow_ascii_fits_more(self):
        # 24 ASCII chars ~ 13.2 em < 20.9 em budget -> single line
        text = "abcdefgh" * 3
        self.assertEqual(1, len(rcv.wrap_for_width(text, 44, 1080).split("\n")))

    def test_orphan_tail_pulled_up_from_previous_line(self):
        # O-20260924-1115 input #3: a wrap ending with a lone "name."
        # strand reads as a broken word; the fix pulls one char down so
        # the tail keeps >=2 glyphs.
        text = "\u7cfb" * 20 + "\u540d\u3002"  # 20 chars + orphan "名。"
        wrapped = rcv.wrap_for_width(text, 44, 1080)
        lines = wrapped.split("\n")
        self.assertGreaterEqual(len(lines), 2)
        self.assertGreaterEqual(len(lines[-1].strip()), 3)  # 名。 + 1 pulled
        self.assertEqual(len(lines[0]), 19)                 # 20 - 1 pulled down
        # no character lost
        self.assertEqual(len(wrapped.replace("\n", "")), len(text))

    def test_punctuation_preferred_break(self):
        # O-20260924-1115 input #3 round 2: the live-A cue must break at
        # a clause ender ("detected / one person" was a broken word);
        # preferred break lands after the last clause punctuation.
        text = ("\u7cfb\u7edf\u542f\u52a8\u3002\u5168\u516c\u53f8\u626b\u63cf"
                "\u5b8c\u6bd5\u2014\u2014\u4eba\u7c7b\uff0c\u68c0\u6d4b\u5230"
                "\u4e00\u540d\u3002")  # 系统启动。全公司扫描完毕——人类，检测到一名。
        wrapped = rcv.wrap_for_width(text, 44, 1080)
        lines = wrapped.split("\n")
        self.assertEqual(2, len(lines))
        self.assertTrue(lines[0].endswith("\uff0c"))  # break after the comma
        self.assertEqual("\u68c0\u6d4b\u5230\u4e00\u540d\u3002", lines[1])
        self.assertEqual(len(wrapped.replace("\n", "")), len(text))

    def test_punct_break_only_when_tail_fits(self):
        # a punctuation early in the line leaves a tail too long for one
        # line -> hard break wins (no runaway lines)
        text = "a\uff0c" + "b" * 30
        wrapped = rcv.wrap_for_width(text, 44, 1080)
        for ln in wrapped.split("\n"):
            # each line within budget (20.9 em; 30 ASCII chars ~16.5em ok)
            self.assertLessEqual(rcv._line_cost(ln), 21.0)

    def test_single_line_wrap_has_no_orphan_mending(self):
        text = "abc"
        self.assertEqual("abc", rcv.wrap_for_width(text, 44, 1080))


class TestPlanAndMatch(unittest.TestCase):
    def test_voiceover_match(self):
        cues = [(0.0, 3.0, "hello  world"), (3.0, 6.0, "foo\nbar")]
        self.assertTrue(rcv.voiceover_matches("helloworld\n foobar", cues))
        self.assertFalse(rcv.voiceover_matches("helloworld baz", cues))

    def test_build_plan(self):
        cues = rcv.parse_srt(_tmp_srt(SRT_OK))
        with tempfile.TemporaryDirectory() as d:
            plan = rcv.build_render_plan(cards_cfg(), cues, d)
            ft = plan["filter_text"]
            # "[0:v]" must sit directly before the first filter (a comma
            # after a link label = empty filter name = graph parse fail)
            self.assertTrue(ft.startswith("[0:v]drawtext="))
            self.assertTrue(ft.endswith("[v]"))
            # drawtext count = cards + cues + 1 aigc
            self.assertEqual(5, ft.count("drawtext="))
            self.assertEqual(4, ft.count("enable='between(t,"))
            # aigc notice persists for the whole video (no enable window)
            self.assertIn("alpha=0.9", ft)  # #23 v14: notice contrast notch up (0.8 gray60 -> 0.9 white)
            # duration = max end (cues 6.5, cards 15) + tail 0.8
            self.assertAlmostEqual(15.8, plan["duration"], places=3)
            for p in plan["textfiles"]:
                self.assertTrue(Path(p).exists())

    def test_build_plan_title_backing_box(self):
        # #23 v14 (2): H1/H2 render over a local dark backing box;
        # boxborderw = h1_gap/2+6 on BOTH boxes (12px overlap = one
        # seamless block). AIGC notice gets NO box (scope: contrast
        # brightening only, stays persistent top-left).
        cfg = cards_cfg()
        cfg["font"].update({
            "h1_font": "C:/fake/h1.ttc", "h1_size": 100, "h1_color": "accent",
            "h2_size": 50, "h2_color": "gray60", "h1_gap": 56,
            "optical_center": 0.42})
        cfg["cards"] = [{"start": 0, "end": 3,
                         "lines": ["head", "sub one", "sub two"]}]
        with tempfile.TemporaryDirectory() as d:
            ft = rcv.build_render_plan(cfg, [], d)["filter_text"]
        self.assertEqual(2, ft.count(
            "box=1:boxcolor=0x000000@0.55:boxborderw=34"))
        self.assertIn("fontcolor=white:alpha=0.9", ft)

    def test_build_plan_escapes_colon(self):
        cues = []
        with tempfile.TemporaryDirectory() as d:
            plan = rcv.build_render_plan(cards_cfg(), cues, d)
            self.assertIn("C\\:/fake/font.ttc", plan["filter_text"])

    def test_build_plan_percent_literal(self):
        """BS-004 first hit: a bare % in card/sub/notice text must survive
        the filtergraph. drawtext's default expansion mode parses % as a
        %{} sequence start (ffmpeg "Stray %" exit); every drawtext runs
        expansion=none (the plan never uses %{} features)."""
        cfg = cards_cfg(cards=[{"start": 0, "end": 4, "lines": ["3.8%", "pct"]}],
                        notice="AI generated 100%")
        cues = [(0.0, 4.0, "best 3.8%")]
        with tempfile.TemporaryDirectory() as d:
            plan = rcv.build_render_plan(cfg, cues, d)
            ft = plan["filter_text"]
            self.assertEqual(ft.count("drawtext="),
                             ft.count("drawtext=expansion=none:"))
            self.assertNotIn("%{", ft)
            joined = "\n".join(Path(p).read_text(encoding="utf-8")
                              for p in plan["textfiles"])
            self.assertIn("3.8%", joined)
            self.assertIn("100%", joined)

    def test_grain_appends_noise_vignette_after_text(self):
        """O-20260923-2210-bm-a: grain>0 = film grain + vignette, appended
        after all text layers (never before them), and off by default."""
        cues = []
        with tempfile.TemporaryDirectory() as d:
            base = rcv.build_render_plan(cards_cfg(), cues, d)
            self.assertNotIn("noise=alls=", base["filter_text"])
            self.assertNotIn("vignette", base["filter_text"])
            with tempfile.TemporaryDirectory() as d2:
                grainy = rcv.build_render_plan(cards_cfg(), cues, d2, grain=7)
                ft = grainy["filter_text"]
                self.assertIn("noise=alls=7:allf=t+u", ft)
                self.assertIn("vignette=angle=PI/6", ft)
                # texture stages come last: nothing after the vignette
                self.assertTrue(ft.rstrip().endswith("vignette=angle=PI/6[v]"))
                # timeline untouched by the aesthetic pass
                self.assertAlmostEqual(base["duration"], grainy["duration"])


class TestPosterTime(unittest.TestCase):
    """--poster cover-frame timestamp (audit O-1043 R1, backlog #16):
    cards fade in over 150ms (visual-spec S4), so a literal t=0 frame
    carries background + AIGC notice only - the cover frame is the
    first card at FULL opacity."""

    def test_first_card_full_visibility(self):
        # cards_cfg default first card: start=0 -> full opacity at 0.15s
        self.assertAlmostEqual(0.15, rcv.poster_time(cards_cfg()), places=3)

    def test_nonzero_start(self):
        cfg = cards_cfg(cards=[{"start": 2, "end": 8, "lines": ["a"]}])
        self.assertAlmostEqual(2.15, rcv.poster_time(cfg), places=3)

    def test_ultra_short_card_mid(self):
        # fade-in would land past the card end -> mid-card instead
        cfg = cards_cfg(cards=[{"start": 0, "end": 0.1, "lines": ["a"]}])
        self.assertAlmostEqual(0.05, rcv.poster_time(cfg), places=3)

    def test_no_cards_zero(self):
        # --no-cards documentary cut: no card moment, literal first frame
        self.assertAlmostEqual(0.0, rcv.poster_time(cards_cfg(cards=[])),
                               places=3)


class TestFcArgs(unittest.TestCase):
    """Compose-graph transport (R199): inline -filter_complex while the
    command line fits the CreateProcess 32K cap; long decks (BS-001-DD
    69 beats / 208 drawtext entries = 74825 chars) swap to
    -/filter_complex <file> (this 9.0.1 gyan build dropped
    -filter_complex_script; the generic -/<opt> <file> syntax survives)."""

    def test_short_inline(self):
        args = rcv.fc_args("[0:v]null[v]", ".")
        self.assertEqual(["-filter_complex", "[0:v]null[v]"], args)

    def test_boundary_inline(self):
        # threshold is an exclusive cap: len == limit still overflows
        # headroom, so exact-limit text goes to the file transport
        import tempfile as tf
        d = Path(tf.mkdtemp(prefix="bsrcv-fcb-"))
        try:
            text = "a" * rcv.FC_INLINE_LIMIT
            args = rcv.fc_args(text, d)
            self.assertEqual(["-/filter_complex", str(d / "fc.txt")], args)
            self.assertTrue((d / "fc.txt").exists())
        finally:
            import shutil
            shutil.rmtree(d, ignore_errors=True)

    def test_long_file_transport_roundtrip(self):
        import tempfile as tf
        d = Path(tf.mkdtemp(prefix="bsrcv-fc-"))
        try:
            text = "x" * (rcv.FC_INLINE_LIMIT + 1)
            args = rcv.fc_args(text, d)
            self.assertEqual(2, len(args))
            self.assertEqual("-/filter_complex", args[0])
            self.assertEqual(d / "fc.txt", Path(args[1]))
            self.assertEqual(text, (d / "fc.txt").read_text(encoding="utf-8"))
        finally:
            import shutil
            shutil.rmtree(d, ignore_errors=True)

    def test_real_dd_scale_uses_file(self):
        # scale regression lock: a 69-beat-scale graph (74K chars measured
        # on the real DD deck, R199) must take the file transport
        text = "drawtext=..." * 18700  # ~74800 chars
        import tempfile as tf
        d = Path(tf.mkdtemp(prefix="bsrcv-fc2-"))
        try:
            args = rcv.fc_args(text, d)
            self.assertEqual("-/filter_complex", args[0])
            self.assertGreater(rcv.FC_INLINE_LIMIT, 20000)
        finally:
            import shutil
            shutil.rmtree(d, ignore_errors=True)


class TestSeriesTemplateAndCyberSync(unittest.TestCase):
    """2026-09-27 #71 remake leg-3: visual-spec v1.2 S5.5 series template
    (T1 intro frame / T2 badge / T5 episode id) + S4.5 cyber sync dials
    (h1 glow / scanlines / sys-status). All plan-level: no ffmpeg run.
    Default-off = byte-identical legacy graph (zero-drift lock)."""

    SERIES = {"badge": True, "id": "BS-001 EP.01", "intro": False,
              "intro_s": 1.5}

    def _plan(self, cfg=None, cues=None, **kw):
        series = kw.pop("series", None)
        with tempfile.TemporaryDirectory() as d:
            plan = rcv.build_render_plan(cfg or cards_cfg(),
                                         cues if cues is not None else [],
                                         d, series=series, **kw)
            bodies = {Path(p).name: Path(p).read_text(encoding="utf-8")
                      for p in plan["textfiles"]}
        return plan, bodies

    def test_series_badge_line(self):
        plan, bodies = self._plan(series=self.SERIES)
        ft = plan["filter_text"]
        # T2: top-right, gray60, constant (no enable window on badge)
        self.assertIn("series.badge.txt", ft)
        self.assertIn("x=w-text_w-48:y=48", ft)
        self.assertIn("fontcolor=gray", ft)
        self.assertEqual("BigStream | BS-001 EP.01",
                         bodies["series.badge.txt"])
        # plan series fields = S5.5 machine-check anchor (3)
        self.assertTrue(plan["series"]["badge"])
        self.assertEqual("BS-001 EP.01", plan["series"]["id"])
        self.assertFalse(plan["series"]["intro"])
        # badge drawtext has no enable window (persistent whole video)
        badge_seg = ft.split("series.badge.txt")[1]
        self.assertNotIn("enable=", badge_seg.split("drawtext")[0])

    def test_defaults_off_legacy_graph_zero_drift(self):
        cues = rcv.parse_srt(_tmp_srt(SRT_OK))
        # same tmpdir for both builds: textfile paths embed the dir, so
        # cross-dir comparison would diff on temp paths, not on the graph
        with tempfile.TemporaryDirectory() as d:
            legacy = rcv.build_render_plan(cards_cfg(), cues, d)["filter_text"]
            plan = rcv.build_render_plan(cards_cfg(), cues, d)  # dials off
            ft = plan["filter_text"]
            self.assertEqual(legacy, ft)
        self.assertNotIn("tpad=", ft)
        self.assertNotIn("drawgrid=", ft)
        self.assertNotIn("borderw=2:bordercolor", ft)
        self.assertNotIn("series.", ft)
        self.assertEqual(0.0, plan["intro_s"])
        self.assertEqual(plan["duration"], plan["total_duration"])

    def test_series_intro_head_and_duration(self):
        cues = rcv.parse_srt(_tmp_srt(SRT_OK))
        series = {"badge": False, "id": "BS-001 EP.01",
                  "intro": True, "intro_s": 1.5}
        plan, bodies = self._plan(cues=cues, series=series)
        ft = plan["filter_text"]
        # T1: black head pad sits directly after the head label
        # (filtergraph shorthand: a link label feeds the next filter
        # with NO comma - a comma there reads as an empty filter name)
        self.assertTrue(
            ft.startswith("[0:v]tpad=start_duration=1.500:start_mode=add:color=black"),
            ft[:120])
        # duration semantics: content clock unchanged, total grows
        self.assertAlmostEqual(plan["duration"] + 1.5,
                               plan["total_duration"], places=3)
        self.assertTrue(plan["series"]["intro"])
        # intro body = episode id + brand line, accent color, fades in
        self.assertEqual("BS-001 EP.01\n" + rcv.BRAND_LINE,
                         bodies["series.intro.txt"])
        self.assertIn("fontcolor=0xE8E6DF", ft)
        # post-tpad filters read the OUTPUT clock: the first card window
        # (0-3s content in this fixture) shifts to 1.500-4.500 with the
        # 1.5s intro head (cards/SRT data files need zero migration)
        self.assertIn("between(t,1.500,4.500)", ft)
        self.assertIn("between(t,0.000,1.500)", ft)  # the intro itself

    def test_series_intro_clamped_to_spec_band(self):
        for raw, want in ((5.0, 2.0), (0.5, 1.5), (1.8, 1.8)):
            series = {"badge": False, "id": "BS-001 EP.01",
                      "intro": True, "intro_s": raw}
            plan, _ = self._plan(series=series)
            self.assertAlmostEqual(want, plan["intro_s"], places=3)

    def test_h1_glow_border(self):
        cfg = cards_cfg()
        cfg["font"].update({"h1_font": "C:/fake/h1.ttc", "h1_size": 100})
        cfg["cards"] = [{"start": 0, "end": 3, "lines": ["head", "sub"]}]
        plan, _ = self._plan(cfg=cfg, h1_glow=True)
        # S4.5(1): restrained accent halo on the H1 anchor only
        self.assertIn("borderw=2:bordercolor=0xE8E6DF@0.35",
                      plan["filter_text"])
        plan_off, _ = self._plan(cfg=cfg)
        # NB: the backing box uses boxborderw=, so the glow signature is
        # the borderw=2:bordercolor pair, not the bare "borderw=" stem
        self.assertNotIn("borderw=2:bordercolor", plan_off["filter_text"])

    def test_scanlines_ambience_under_text(self):
        plan, _ = self._plan(scanlines=True)
        ft = plan["filter_text"]
        # S4.5(3): 5% (<=8% cap), 1px every 3px, before every text layer
        self.assertIn("drawgrid=w=iw:h=3:t=1:c=0xE8E6DF@0.05", ft)
        self.assertLess(ft.index("drawgrid="), ft.index("drawtext="))

    def test_sys_status_per_cue(self):
        cues = rcv.parse_srt(_tmp_srt(SRT_OK))
        plan, bodies = self._plan(cues=cues, sys_status=True)
        self.assertIn("sys.beat=01 t=00:00", bodies["sys.beat00.txt"])
        self.assertIn("sys.beat=02 t=00:03", bodies["sys.beat01.txt"])
        # without badge the telemetry line takes the top-right slot
        self.assertIn("x=w-text_w-48:y=48:enable='between(t,0.000",
                      plan["filter_text"])
        # with badge it stacks under the badge (aigc_size 30 + 12 gap)
        plan2, _ = self._plan(cues=cues, series=self.SERIES, sys_status=True)
        self.assertIn("x=w-text_w-48:y=90:enable='between(t,0.000",
                      plan2["filter_text"])


def _tmp_srt(content):
    import tempfile as tf
    d = tf.mkdtemp(prefix="bsrcv-test-")
    p = Path(d) / "subs.srt"
    p.write_text(content, encoding="utf-8")
    return p


if __name__ == "__main__":
    unittest.main(verbosity=2)
