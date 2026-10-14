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


if __name__ == "__main__":
    unittest.main()
