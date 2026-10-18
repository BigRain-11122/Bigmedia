# -*- coding: utf-8 -*-
"""Unit tests for the queue compact readout (src/os/queue_status.py).

tech#145, R2119 seed: queue ledgers are single-long-line items; done
marks must be judged over the FULL line (a 280-char truncated view once
misjudged deep marks as missing -> 6 probe re-scans). These tests lock:
full-text done detection, the three done-marker forms in the wild,
gated classification, compact-face line cap, and the fail-closed --item
fetch (ANCHOR-MISS doctrine).

tech#146, R2124: backlog face locks - the P1 board joins as a fourth
face, and the P1-only [needs-CEO] family parks in the gated bucket with
a reported split (never claimable).

Run:
    python tests/test_queue_status.py
"""
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def run_main_silent(argv):
    """Call queue_status.main with stdout swallowed; return (rc, out)."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = qs.main(argv)
    return rc, buf.getvalue()

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "os"))

import queue_status as qs  # noqa: E402

PAD = "x" * 300  # pushes follow-up content past the 280-char cut


class TestParseItems(unittest.TestCase):
    def test_heads_and_continuations(self):
        text = ("# header\n> quote\n"
                "1. first item head\n"
                "   continuation line\n"
                "2. second item head\n")
        items = qs.parse_items(text)
        self.assertEqual([1, 2], [i["num"] for i in items])
        self.assertIn("continuation line", items[0]["text"])
        self.assertNotIn("header", items[0]["text"])

    def test_no_items(self):
        self.assertEqual([], qs.parse_items("# only header\n"))


class TestClassifyItem(unittest.TestCase):
    def test_done_at_head_bracket(self):
        it = {"num": 1, "head": "1. [done 2026-10-09 R1828] text",
              "text": "1. [done 2026-10-09 R1828] text"}
        self.assertEqual("done", qs.classify_item(it)[0])

    def test_done_round_prefixed_form(self):
        it = {"num": 3, "head": "3. [R1845 done 2026-10-10] REACT",
              "text": "3. [R1845 done 2026-10-10] REACT"}
        self.assertEqual("done", qs.classify_item(it)[0])

    def test_done_embedded_midline_beyond_280(self):
        # R2119 regression: mark sitting past the truncated-view cut
        it = {"num": 26,
              "head": "26. [R1832 seed] " + PAD,
              "text": "26. [R1832 seed] " + PAD +
                      " **[done 2026-10-11 R2005 消费验读毕]** tail"}
        state, marker = qs.classify_item(it)
        self.assertEqual("done", state)
        self.assertIn("2026-10-11", marker)

    def test_done_on_continuation_line(self):
        it = {"num": 5, "head": "5. gated ollama 恢复",
              "text": "5. gated ollama 恢复\n   [done 2026-10-11 R1952] close"}
        self.assertEqual("done", qs.classify_item(it)[0])

    def test_prose_done_without_date_is_open(self):
        it = {"num": 9, "head": "9. 待其收口 commit 后由下轮消费验读标 done",
              "text": "9. 待其收口 commit 后由下轮消费验读标 done"}
        self.assertNotEqual("done", qs.classify_item(it)[0])

    def test_gated_by_word(self):
        it = {"num": 1, "head": "1. thing ——gated 规范 v1.1 定谳",
              "text": "1. thing ——gated 规范 v1.1 定谳"}
        self.assertEqual("gated", qs.classify_item(it)[0])

    def test_gated_by_observation_or_schedule(self):
        for body in ("观察位：夜窗 i2v 波进行时领", "到点执行（REACT-v22 收官轮）",
                     "——GPU 独占窗即领", "）——窗到即领"):
            it = {"num": 2, "head": "2. " + body, "text": "2. " + body}
            self.assertEqual("gated", qs.classify_item(it)[0])

    def test_claimable_default(self):
        it = {"num": 1, "head": "1. CPU 面可即领·随轮领",
              "text": "1. CPU 面可即领·随轮领"}
        self.assertEqual("claimable", qs.classify_item(it)[0])


class TestUpstreamWaitGate(unittest.TestCase):
    """tech#189/#190 (R2317/R2319 seeds, closed R2364): waiting-upstream
    family gates. Literal marker phrases only - form 1 (backlog #31
    shape) 稿落即领 / 稿落即随轮认领; form 3 (backlog #27 shape)
    等上游源稿 / waits ... source manuscript. Done wins; the tech#210
    gate-lift note flips a stale upstream-gated row the same way."""

    def _it(self, body, num=21):
        return {"num": num, "head": "%d. %s" % (num, body),
                "text": "%d. %s" % (num, body)}

    def test_form1_markers_gate(self):
        for body in ("ch.5 v3 稿未落盘（bm-a 面）=稿落即领——观察位",
                     "后续章 v2 稿未落盘=稿落即随轮认领（新连载节律同口径）"):
            self.assertEqual("gated", qs.classify_item(self._it(body))[0])

    def test_form3_markers_gate(self):
        for body in ("唯余 ch.6 有声腿等上游源稿（SC-001-06 未撰·连载面）",
                     "only remaining leg ch.6 audio waits novel SC-001-06 "
                     "source manuscript [unwritten]"):
            self.assertEqual("gated", qs.classify_item(self._it(body))[0])

    def test_done_beats_upstream_marker(self):
        # backlog #30/#87/#88 shape: done-marked rows quoting the marker
        it = {"num": 30,
              "head": "30. [done 2026-09-25] 后续章稿未落盘=稿落即随轮认领",
              "text": "30. [done 2026-09-25] 后续章稿未落盘=稿落即随轮认领"}
        self.assertEqual("done", qs.classify_item(it)[0])

    def test_gate_lift_note_beats_upstream_marker(self):
        # tech#210 rule extends to the family: source manuscript landed
        # and an explicit lift note + 转 claimable flips the stale head.
        body = ("唯余 ch.5 等上游源稿=稿落即领 "
                "**[R2364 gate 解除注记 2026-10-18]** 源稿已落盘·转 "
                "claimable 即领")
        state, marker = qs.classify_item(self._it(body))
        self.assertEqual("claimable", state)
        self.assertIn("HEAD-INCONSISTENT", marker)

    def test_landed_or_plain_manuscript_prose_stays_claimable(self):
        # near-miss negative: manuscript landed / plain manuscript work
        for body in ("ch.6 源稿已落盘·源稿落盘即转可领·全链随轮领",
                     "拍稿 v1 落盘=随轮领", "源稿落盘后领做"):
            self.assertEqual("claimable", qs.classify_item(self._it(body))[0])


class TestNeedsCeoBucket(unittest.TestCase):
    """tech#146: [needs-CEO] items are gated semantics, never claimable."""

    def test_needs_ceo_marks_gated(self):
        it = {"num": 17, "head": "17. P1 提案件（商业化投放）[needs-CEO] 立项位",
              "text": "17. P1 提案件（商业化投放）[needs-CEO] 立项位"}
        self.assertEqual("gated", qs.classify_item(it)[0])

    def test_needs_ceo_with_annotation_form(self):
        it = {"num": 4, "head": "4. thing [needs-CEO: budget sign-off] tail",
              "text": "4. thing [needs-CEO: budget sign-off] tail"}
        self.assertEqual("gated", qs.classify_item(it)[0])

    def test_done_beats_needs_ceo(self):
        # a completed item that still mentions [needs-CEO] in prose
        it = {"num": 6, "head": "6. closed work [done 2026-10-12 R1] 后记 [needs-CEO]",
              "text": "6. closed work [done 2026-10-12 R1] 后记 [needs-CEO]"}
        state, marker = qs.classify_item(it)
        self.assertEqual("done", state)
        self.assertIn("2026-10-12", marker)

    def test_classify_queue_reports_needs_ceo_split(self):
        items = qs.parse_items(
            "1. [done 2026-10-12 R1] a\n"
            "2. proposal [needs-CEO] park\n"
            "3. gated thing\n"
            "4. claimable thing\n")
        buckets, markers, needs_ceo = qs.classify_queue(items)
        self.assertEqual(2, len(buckets["gated"]))       # #2 + #3
        self.assertEqual({2: True}, needs_ceo)          # split tracked
        self.assertEqual(1, len(buckets["claimable"]))  # #4
        self.assertEqual([4], [i["num"] for i in buckets["claimable"]])

    def test_header_needs_ceo_mention_not_an_item(self):
        # the backlog header quote mentions [needs-CEO] as convention
        # prose - header/quote lines must never become gated items
        items = qs.parse_items(
            "> 新任务=追加到末尾；P1 级提案入板须标 `[needs-CEO]`。\n"
            "1. claimable thing\n")
        buckets, markers, needs_ceo = qs.classify_queue(items)
        self.assertEqual(1, len(buckets["claimable"]))
        self.assertEqual({}, needs_ceo)


class TestQueueFaces(unittest.TestCase):
    def _face(self):
        items = qs.parse_items(
            "1. [done 2026-10-10 R1] a\n"
            "2. gated thing\n"
            "3. claimable thing\n"
            "4. 观察位 later\n")
        return qs.classify_queue(items)

    def test_counts_and_head(self):
        buckets, markers, needs_ceo = self._face()
        self.assertEqual(1, len(buckets["done"]))
        self.assertEqual(2, len(buckets["gated"]))
        self.assertEqual(1, len(buckets["claimable"]))
        self.assertEqual(3, buckets["claimable"][0]["num"])
        self.assertIn("2026-10-10", markers[1])
        self.assertEqual({}, needs_ceo)

    def test_head_preview_truncates(self):
        it = {"num": 12, "head": "12. " + "y" * 200, "text": ""}
        prev = qs.head_preview(it)
        self.assertTrue(prev.startswith("y"))
        self.assertEqual(qs.HEAD_PREVIEW_CHARS, len(prev))
        self.assertTrue(prev.endswith("..."))

    def test_render_line_cap(self):
        report = {}
        for name in ("backlog", "explore", "main", "tech"):
            report[name] = {
                "missing": False, "total": 4, "done": 1, "gated": 2,
                "needs_ceo": 1, "claimable": 1,
                "claimable_head": {"num": 3, "head": "3. head", "text": ""},
            }
        lines = qs.render(report)
        self.assertLessEqual(len(lines), qs.MAX_DEFAULT_LINES)
        self.assertTrue(lines[0].startswith("queue-status"))
        self.assertTrue(lines[-1].startswith("total"))
        # tech#146: needs-CEO split surfaced in the gated column
        self.assertTrue(any("(+needs-CEO 1)" in ln for ln in lines))

    def test_render_gated_column_without_ceo_unchanged(self):
        report = {"tech": {"missing": False, "total": 3, "done": 1,
                           "gated": 2, "needs_ceo": 0, "claimable": 0,
                           "claimable_head": None}}
        lines = qs.render(report)
        self.assertTrue(any("| gated 2 |" in ln for ln in lines))
        self.assertFalse(any("needs-CEO" in ln for ln in lines))

    def test_render_missing_queue(self):
        lines = qs.render({"tech": {"missing": True}})
        self.assertIn("MISSING", lines[1])

    def test_render_item_found_and_missing(self):
        items = qs.parse_items("7. [done 2026-10-12 R1] body " + PAD)
        face = {"items": items}
        out, rc = qs.render_item(face, 7)
        self.assertEqual(0, rc)
        self.assertTrue(out[0].startswith("#7 [DONE]"))
        self.assertTrue(any(PAD in line for line in out))  # verbatim, no cut
        out, rc = qs.render_item(face, 99)
        self.assertEqual(2, rc)  # ANCHOR-MISS fail-closed
        self.assertIn("fail-closed", out[0])

    def test_build_json_shape(self):
        report = {"tech": {"missing": False, "total": 4, "done": 1,
                           "gated": 2, "needs_ceo": 1, "claimable": 1,
                           "claimable_head": {"num": 3, "head": "", "text": ""}}}
        data = qs.build_json(report)
        self.assertEqual(1, data["tech"]["claimable"])
        self.assertEqual(3, data["tech"]["claimable_head_num"])
        self.assertEqual(1, data["tech"]["needs_ceo"])
        json.dumps(data)  # must be serializable


class TestMainCli(unittest.TestCase):
    def _repo_with_queues(self, root):
        (root / "state" / "queue").mkdir(parents=True)
        (root / "state" / "queue" / "main.md").write_text(
            "1. [R1845 done 2026-10-10] a\n2. open thing\n", encoding="utf-8")
        (root / "state" / "queue" / "tech.md").write_text(
            "1. gated thing\n2. [done 2026-10-13 R1] done\n3. claim now\n",
            encoding="utf-8")
        (root / "state" / "queue" / "explore.md").write_text(
            "1. 观察位 later\n", encoding="utf-8")
        # tech#146: P1 board face - same shape, [needs-CEO] family included
        (root / "src" / "os").mkdir(parents=True, exist_ok=True)
        (root / "src" / "os" / "backlog.md").write_text(
            "# P1 board\n"
            "> P1 级提案入板须标 `[needs-CEO]`。\n"
            "114. [done 2026-10-09 R1819] closed P1 work\n"
            "111. MV 查看位行（随轮领做·零接触）\n"
            "110. P1 提案件（商业化投放）[needs-CEO] 待裁\n"
            "109. 按认领制随轮领做 CPU 件\n",
            encoding="utf-8")

    def test_default_face_and_json(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._repo_with_queues(root)
            rc, out = run_main_silent(["--root", str(root)])
            self.assertEqual(0, rc)
            self.assertLessEqual(len(out.strip().splitlines()),
                                 qs.MAX_DEFAULT_LINES)
            self.assertIn("backlog", out)  # 4th face present
            # top uncompleted item = #111 (first not-done, not [needs-CEO])
            self.assertIn("head #111", out)
            rc, out = run_main_silent(["--root", str(root), "--json"])
            self.assertEqual(0, rc)
            data = json.loads(out)
            self.assertEqual(2, data["main"]["claimable_head_num"])
            self.assertEqual(111, data["backlog"]["claimable_head_num"])
            self.assertEqual(1, data["backlog"]["needs_ceo"])
            self.assertEqual(1, data["backlog"]["done"])
            self.assertEqual(2, data["backlog"]["claimable"])

    def test_backlog_item_fetch_and_queue_choice(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._repo_with_queues(root)
            rc, out = run_main_silent(["--root", str(root),
                                       "--queue", "backlog", "--item", "110"])
            self.assertEqual(0, rc)
            self.assertIn("#110 [GATED]", out)  # needs-CEO parks gated
            self.assertIn("needs-CEO", out)

    def test_item_fetch_and_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._repo_with_queues(root)
            rc, out = run_main_silent(["--root", str(root), "--item", "3"])
            self.assertEqual(0, rc)
            self.assertIn("#3 [CLAIMABLE]", out)
            rc, out = run_main_silent(["--root", str(root), "--item", "42"])
            self.assertEqual(2, rc)

    def test_all_missing_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(2, qs.main(["--root", td]))

    def test_cli_subprocess_default_face(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._repo_with_queues(root)
            p = subprocess.run(
                [sys.executable, str(REPO / "src" / "os" / "queue_status.py"),
                 "--root", str(root)],
                capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=60)
            self.assertEqual(0, p.returncode)
            self.assertLessEqual(len(p.stdout.strip().splitlines()),
                                  qs.MAX_DEFAULT_LINES)


class TestClaimableNums(unittest.TestCase):
    """tech#167, R2245 seed: --json claimable_nums array (file order).

    Gap anchor: the R2245 audit needed "which numbers are claimable per
    queue" and had to import the module four times (signature guessing)
    to derive the list. The array is a pure additive field - consumers
    reading only the old keys must stay green.
    """

    def test_nums_file_order_and_length_agreement(self):
        items = qs.parse_items(
            "114. [done 2026-10-09 R1] closed\n"
            "111. claimable thing\n"
            "110. gated thing\n"
            "109. claimable thing two\n")
        buckets, markers, needs_ceo = qs.classify_queue(items)
        face = {"missing": False, "total": 4, "done": 1, "gated": 1,
                "needs_ceo": 0, "claimable": len(buckets["claimable"]),
                "claimable_nums": [it["num"] for it in buckets["claimable"]],
                "claimable_head": buckets["claimable"][0]}
        data = qs.build_json({"backlog": face})
        # file order preserved (109 sits after 111 in the file)
        self.assertEqual([111, 109], data["backlog"]["claimable_nums"])
        self.assertEqual(data["backlog"]["claimable"],
                         len(data["backlog"]["claimable_nums"]))

    def test_missing_field_defaults_to_empty(self):
        # hand-built report dicts (older callers) lack the new key
        report = {"tech": {"missing": False, "total": 3, "done": 1,
                           "gated": 2, "needs_ceo": 0, "claimable": 0,
                           "claimable_head": None}}
        data = qs.build_json(report)
        self.assertEqual([], data["tech"]["claimable_nums"])

    def test_empty_claimable_gives_empty_array(self):
        items = qs.parse_items("1. gated thing\n2. [done 2026-10-12 R1] x\n")
        buckets, markers, needs_ceo = qs.classify_queue(items)
        data = qs.build_json({"tech": {
            "missing": False, "total": 2, "done": 1, "gated": 1,
            "needs_ceo": 0, "claimable": 0,
            "claimable_nums": [it["num"] for it in buckets["claimable"]],
            "claimable_head": None}})
        self.assertEqual([], data["tech"]["claimable_nums"])

    def test_cli_json_face_carries_nums(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "state" / "queue").mkdir(parents=True)
            (root / "state" / "queue" / "main.md").write_text(
                "1. [R1845 done 2026-10-10] a\n2. open thing\n",
                encoding="utf-8")
            (root / "state" / "queue" / "tech.md").write_text(
                "1. gated thing\n2. [done 2026-10-13 R1] done\n3. claim\n",
                encoding="utf-8")
            (root / "state" / "queue" / "explore.md").write_text(
                "1. 观察位 later\n", encoding="utf-8")
            rc, out = run_main_silent(["--root", str(root), "--json"])
            self.assertEqual(0, rc)
            data = json.loads(out)
            self.assertEqual([2], data["main"]["claimable_nums"])
            self.assertEqual([3], data["tech"]["claimable_nums"])
            self.assertEqual([], data["explore"]["claimable_nums"])


class TestConsoleHardening(unittest.TestCase):
    """R2276: --item once crashed live on the GBK console
    (UnicodeEncodeError: 'gbk' codec can't encode '\\u226a' - the
    character sits inside tech#151's VRAM reading). The CLI must
    degrade non-encodable characters instead of dying. Hermetic via
    PYTHONIOENCODING=gbk so the crash reproduces on any host locale.
    """

    def test_item_print_survives_non_gbk_console(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "state" / "queue").mkdir(parents=True)
            (root / "state" / "queue" / "tech.md").write_text(
                "151. 门读数 free ~1.2G≪8704MB 硬关窗\n", encoding="utf-8")
            env = dict(os.environ, PYTHONIOENCODING="gbk")
            p = subprocess.run(
                [sys.executable, str(REPO / "src" / "os" / "queue_status.py"),
                 "--root", str(root), "--item", "151"],
                capture_output=True, timeout=60, env=env)
            self.assertEqual(0, p.returncode)
            self.assertIn(b"#151 [CLAIMABLE]", p.stdout)
            self.assertIn(b"8704MB", p.stdout)  # verbatim text survives

    def test_harden_noop_on_stringio_streams(self):
        # pythonw None-stream guard (tech#169 family) + the unittest
        # harness (StringIO has no reconfigure) must both no-op.
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), \
                contextlib.redirect_stderr(err):
            self.assertIsNone(qs._harden_console_stdio())


class TestGateLiftNoteAndFaceLine(unittest.TestCase):
    """tech#210 half-unlocked rule + tech#207 --item face line (R2344).

    Live anchor: canonical --item 206 read [GATED] while the row's own
    R2340 progress note said the gate had lifted -> claimant ambiguity.
    And a bare "--item 128" once silently read the tech face while the
    caller meant main#128 (R2340 ~2min misread).
    """

    def _item(self, num, text):
        return {"num": num, "head": text, "text": text}

    def test_gate_lift_note_flips_stale_gated_head(self):
        it = self._item(206, (
            "206. [R2339 seed.gated] work ... gated=protocol file must "
            "land ... **[R2340 gate 解除注记 2026-10-18]**: file landed "
            "-> gated 前半解除·转 claimable (next round)"))
        state, marker = qs.classify_item(it)
        self.assertEqual("claimable", state)
        self.assertIn("HEAD-INCONSISTENT", marker)

    def test_gate_lift_requires_both_signals(self):
        lift_note_only = ("7. [seed.gated] x [R2340 gate 解除注记 "
                          "2026-10-18] but no lift phrase")
        self.assertEqual(
            "gated", qs.classify_item(self._item(7, lift_note_only))[0])
        phrase_only = "8. [seed.gated] x ... 转 claimable but no lift bracket"
        self.assertEqual(
            "gated", qs.classify_item(self._item(8, phrase_only))[0])

    def test_plain_gated_unchanged(self):
        text = "9. [seed.gated] pure gated row"
        self.assertEqual(("gated", None), qs.classify_item(self._item(9, text)))

    def test_bare_item_echoes_default_face(self):
        with tempfile.TemporaryDirectory() as td:
            qdir = Path(td) / "state" / "queue"
            qdir.mkdir(parents=True)
            (qdir / "tech.md").write_text("1. sample row\n", encoding="utf-8")
            rc, out = run_main_silent(["--root", td, "--item", "1"])
            self.assertEqual(0, rc)
            self.assertIn("face: tech (DEFAULT", out)
            self.assertIn("#1 [CLAIMABLE]", out)

    def test_explicit_queue_face_has_no_default_tag(self):
        with tempfile.TemporaryDirectory() as td:
            qdir = Path(td) / "state" / "queue"
            qdir.mkdir(parents=True)
            (qdir / "main.md").write_text("1. sample row\n", encoding="utf-8")
            rc, out = run_main_silent(["--root", td, "--queue", "main",
                                       "--item", "1"])
            self.assertEqual(0, rc)
            self.assertIn("face: main\n", out)
            self.assertNotIn("DEFAULT", out)


if __name__ == "__main__":
    unittest.main()
