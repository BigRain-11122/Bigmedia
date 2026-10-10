# -*- coding: utf-8 -*-
"""Tests for tools/radar_snapshot_gen.py (state/queue/tech#40, R1892).

Deliverable unlocked by group decision D-20261010-09 (BigStream = generator +
first snapshot; MiniGame integrates). Covers the four red lines from
R-20261010-bigstream-04 section 3:
- internal-anchor scrub (links.aihot / attribution.url never reach the file),
- hard gate on any surviving internal marker (rc 4, no file written),
- honest empty state (no fabricated data; available flag),
- AIGC marker in the rendered header,
plus CLI surface (fetch failure rc 2 no partial file, bad timeout, parent
dir creation) and JS rendering round-trip (JSON body parses back equal).
"""
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

_SPEC = importlib.util.spec_from_file_location(
    "radar_snapshot_gen",
    os.path.join(os.path.dirname(__file__), "..", "tools",
                 "radar_snapshot_gen.py"))
gen = importlib.util.module_from_spec(_SPEC)
sys.modules["radar_snapshot_gen"] = gen
_SPEC.loader.exec_module(gen)


def _live_empty_fixture():
    """Mirror of the real 2026-10-10 latest payload (honest empty state)."""
    return {
        "schemaVersion": 1,
        "report": {
            "date": "2026-10-10",
            "generatedAt": "2026-10-10T00:00:30.431Z",
            "windowStart": "2026-10-09T00:00:00.000Z",
            "windowEnd": "2026-10-10T00:00:00.000Z",
            "links": {"aihot": "http://127.0.0.1:3100/daily/2026-10-10"},
            "attribution": {
                "name": "雷达日报",
                "url": "http://127.0.0.1:3100/daily/2026-10-10",
            },
            "lead": {
                "title": "今日安静，无大事发生",
                "leadParagraph": "没有新的城市大事。",
            },
            "sections": [],
            "flashes": [],
        },
    }


def _full_fixture():
    """Plausible non-empty day per R-20261010-04 section 4 field mapping."""
    return {
        "schemaVersion": 1,
        "report": {
            "date": "2026-10-11",
            "generatedAt": "2026-10-11T00:00:30.000Z",
            "links": {"aihot": "http://127.0.0.1:3100/daily/2026-10-11"},
            "attribution": {
                "name": "雷达日报",
                "url": "http://127.0.0.1:3100/daily/2026-10-11",
            },
            "lead": {
                "title": "新模型发布刷屏",
                "leadParagraph": "三家厂商同日发布。",
            },
            "sections": [{
                "label": "产品发布/更新",
                "items": [{
                    "title": "Story one",
                    "summary": "A big story.",
                    "source": {"name": "来源甲"},
                    "links": {
                        "aihot": "http://127.0.0.1:3100/story/1",
                        "original": "https://example.com/news/1",
                    },
                }, {
                    "title": "Story two",
                    "summary": "Another story.",
                    "source": {"name": "来源乙"},
                    "links": {"aihot": "http://127.0.0.1:3100/story/2"},
                }],
            }],
            "flashes": [{
                "text": "快讯一条",
                "links": {
                    "aihot": "http://127.0.0.1:3100/flash/1",
                    "original": "https://example.com/flash/1",
                },
                "attribution": {
                    "name": "雷达日报",
                    "url": "http://127.0.0.1:3100/flash/1",
                },
            }],
        },
    }


class ScrubTests(unittest.TestCase):

    def test_scrub_drops_aihot_keeps_original(self):
        scrubbed = gen._scrub_internal_anchors({
            "links": {"aihot": "http://127.0.0.1:3100/x",
                      "original": "https://example.com/x"},
            "other": {"links": {"aihot": "http://127.0.0.1:3100/y"}},
        })
        self.assertEqual(scrubbed["links"], {"original": "https://example.com/x"})
        self.assertNotIn("links", scrubbed["other"])

    def test_scrub_attribution_keeps_name_only(self):
        scrubbed = gen._scrub_internal_anchors({
            "attribution": {"name": "雷达日报",
                            "url": "http://127.0.0.1:3100/daily/x"},
        })
        self.assertEqual(scrubbed["attribution"], {"name": "雷达日报"})


class BuildPayloadTests(unittest.TestCase):

    def test_full_fixture_projection_and_scrub(self):
        payload = gen.build_payload(_full_fixture())
        self.assertTrue(payload["available"])
        self.assertEqual(payload["date"], "2026-10-11")
        self.assertEqual(payload["attributionName"], "雷达日报")
        self.assertEqual(payload["lead"]["title"], "新模型发布刷屏")
        self.assertEqual(len(payload["sections"]), 1)
        item = payload["sections"][0]["items"][0]
        self.assertEqual(item["source"], "来源甲")
        self.assertEqual(item["original"], "https://example.com/news/1")
        self.assertNotIn("links", item)
        self.assertNotIn("attribution", item)
        item2 = payload["sections"][0]["items"][1]
        self.assertIsNone(item2["original"])  # aihot-only links dropped
        flash = payload["flashes"][0]
        self.assertEqual(flash["links"], {"original": "https://example.com/flash/1"})
        self.assertEqual(flash["attribution"], {"name": "雷达日报"})
        blob = json.dumps(payload, ensure_ascii=False)
        self.assertNotIn("127.0.0.1", blob)

    def test_honest_empty_state_preserved(self):
        payload = gen.build_payload(_live_empty_fixture())
        self.assertTrue(payload["available"])
        self.assertEqual(payload["sections"], [])
        self.assertEqual(payload["flashes"], [])
        self.assertEqual(payload["lead"]["title"], "今日安静，无大事发生")
        self.assertEqual(payload["attributionName"], "雷达日报")

    def test_no_report_available_false_no_fake_data(self):
        payload = gen.build_payload({"schemaVersion": 1})
        self.assertFalse(payload["available"])
        self.assertIsNone(payload["date"])
        self.assertIsNone(payload["lead"])
        self.assertIsNone(payload["attributionName"])
        self.assertEqual(payload["sections"], [])
        self.assertEqual(payload["flashes"], [])


class GateTests(unittest.TestCase):

    def test_gate_passes_clean_payload(self):
        gen.assert_no_internal_anchors(gen.build_payload(_full_fixture()))

    def test_gate_fires_on_smuggled_anchor(self):
        payload = gen.build_payload(_live_empty_fixture())
        payload["lead"] = {"title": "x http://127.0.0.1:3100/leak",
                           "leadParagraph": None}
        with self.assertRaises(gen.InternalAnchorError):
            gen.assert_no_internal_anchors(payload)


class RenderTests(unittest.TestCase):

    def test_render_roundtrip_and_markers(self):
        payload = gen.build_payload(_full_fixture())
        js = gen.render_js(payload)
        self.assertTrue(js.startswith("//"))
        self.assertIn("AI-generated content", js)
        self.assertIn("window.RADAR_DAILY = ", js)
        self.assertTrue(js.endswith(";\n"))
        body = js[js.index("window.RADAR_DAILY = ") + len("window.RADAR_DAILY = "):]
        body = body[: body.rindex(";")]
        self.assertEqual(json.loads(body), payload)

    def test_render_escapes_line_separators(self):
        payload = gen.build_payload(_live_empty_fixture())
        payload["lead"]["title"] = "a" + chr(0x2028) + "b" + chr(0x2029) + "c"
        js = gen.render_js(payload)
        self.assertNotIn(chr(0x2028), js)
        self.assertNotIn(chr(0x2029), js)
        body = js[js.index("window.RADAR_DAILY = ") + len("window.RADAR_DAILY = "):]
        body = body[: body.rindex(";")]
        self.assertEqual(json.loads(body), payload)


class CliTests(unittest.TestCase):

    def _run(self, argv, return_value=None):
        buf = io.StringIO()
        with mock.patch.object(gen, "fetch_latest",
                               return_value=return_value) as fetch, \
                mock.patch("sys.stdout", buf):
            rc = gen.main(argv)
        return rc, buf.getvalue(), fetch

    def test_cli_writes_utf8_no_bom(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "sub", "radar-daily-data.js")
            rc, outtext, fetch = self._run(
                ["--out", out], return_value=_full_fixture())
            self.assertEqual(rc, 0)
            fetch.assert_called_once_with("http://127.0.0.1:3101", 10.0)
            self.assertIn("WROTE", outtext)
            self.assertIn("available=True", outtext)
            raw = io.open(out, "rb").read()
            self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))  # no BOM
            text = raw.decode("utf-8")
            self.assertIn("window.RADAR_DAILY = ", text)
            body = text[text.index("window.RADAR_DAILY = ") + len("window.RADAR_DAILY = "):]
            self.assertEqual(
                json.loads(body[: body.rindex(";")]),
                gen.build_payload(_full_fixture()))
            self.assertNotIn("127.0.0.1", text)

    def test_cli_fetch_failure_rc2_no_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "radar-daily-data.js")
            with mock.patch.object(gen, "fetch_latest",
                                   side_effect=gen.RadarFetchError("down")):
                err = io.StringIO()
                with mock.patch("sys.stderr", err):
                    rc = gen.main(["--out", out])
            self.assertEqual(rc, 2)
            self.assertFalse(os.path.exists(out))
            self.assertIn("fetch failed", err.getvalue())

    def test_cli_gate_failure_rc4_no_file(self):
        fixture = _live_empty_fixture()
        fixture["report"]["lead"]["leadParagraph"] = "见 http://127.0.0.1:3100/x"
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "radar-daily-data.js")
            with mock.patch.object(gen, "fetch_latest", return_value=fixture):
                err = io.StringIO()
                with mock.patch("sys.stderr", err):
                    rc = gen.main(["--out", out])
            self.assertEqual(rc, 4)
            self.assertFalse(os.path.exists(out))
            self.assertIn("internal-anchor gate", err.getvalue())

    def test_cli_bad_timeout_rejected_before_fetch(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "radar-daily-data.js")
            rc, _, fetch = self._run(["--out", out, "--timeout", "0"])
            self.assertEqual(rc, 2)
            fetch.assert_not_called()
            self.assertFalse(os.path.exists(out))


if __name__ == "__main__":
    unittest.main()
