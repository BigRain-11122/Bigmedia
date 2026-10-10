# -*- coding: utf-8 -*-
"""Tests for the fixed ollama generation probe (state/queue/tech#51, R1881).

Covers the two trap families the probe retires:
- 503 saturation vs other HTTP errors (rc 1 vs rc 2 differentiation saved),
- a genuine 400 observed through the clean urllib client is rc 2 (the
  historical 400 was a PS inline-quoting transport artifact, R1880),
plus CLI surface (--model/--timeout/--json) and the main-guard import
safety (no probe flight on import).
"""

import io
import json
import os
import sys
import unittest
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src", "os"))

import ollama_probe as op  # noqa: E402


class _FakeResp(object):
    def __init__(self, payload):
        self._bytes = payload

    def read(self):
        return self._bytes

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _http_error(code, detail):
    return urllib.error.HTTPError(
        "http://localhost:11434/api/generate", code, "err", None,
        io.BytesIO(detail.encode("utf-8")))


SATURATION_DETAIL = '{"error":"server busy, please try again.  maximum pending requests exceeded"}'


class BuildBodyTests(unittest.TestCase):
    def test_body_is_valid_json_with_model(self):
        body = json.loads(op.build_request_body("qwen2.5:14b-8k").decode("utf-8"))
        self.assertEqual(body["model"], "qwen2.5:14b-8k")
        self.assertEqual(body["prompt"], "hi")
        self.assertFalse(body["stream"])

    def test_no_shell_quoting_surface(self):
        # The R1880 trap: inline PS JSON lost quotes -> 400 fake signal.
        # Body built inside Python must round-trip through json.loads.
        raw = op.build_request_body("m:1").decode("utf-8")
        self.assertEqual(raw, json.dumps(json.loads(raw)))


class ClassifyTests(unittest.TestCase):
    def test_503_code_is_saturated(self):
        self.assertEqual(op.classify(503, "anything"), 1)

    def test_saturation_message_is_saturated(self):
        self.assertEqual(op.classify(400, SATURATION_DETAIL), 1)

    def test_other_http_is_error_rc2(self):
        self.assertEqual(op.classify(400, '{"error":"bad request"}'), 2)
        self.assertEqual(op.classify(500, "boom"), 2)
        self.assertEqual(op.classify(400, None), 2)
        self.assertEqual(op.classify(404, ""), 2)


class RunProbeTests(unittest.TestCase):
    def setUp(self):
        self._orig = op._http_post

    def tearDown(self):
        op._http_post = self._orig

    def _patch(self, raiser=None, resp=None):
        def fake(base_url, body, timeout):
            if raiser is not None:
                raise raiser
            return resp
        op._http_post = fake

    def test_rc0_on_200(self):
        resp = _FakeResp(json.dumps({"done_reason": "stop"}).encode("utf-8"))
        self._patch(resp=resp)
        result = op.run_probe()
        self.assertEqual(result["rc"], 0)
        self.assertEqual(result["status"], "ok")

    def test_rc1_on_503_saturation(self):
        self._patch(raiser=_http_error(503, SATURATION_DETAIL))
        result = op.run_probe()
        self.assertEqual(result["rc"], 1)
        self.assertEqual(result["status"], "saturated")
        self.assertEqual(result["http_status"], 503)

    def test_rc1_on_503_with_unreadable_detail(self):
        err = _http_error(503, "")
        err.read = None  # detail read fails -> empty string, code still classifies
        self._patch(raiser=err)
        result = op.run_probe()
        self.assertEqual(result["rc"], 1)

    def test_rc2_on_genuine_400(self):
        self._patch(raiser=_http_error(400, '{"error":"bad request"}'))
        result = op.run_probe()
        self.assertEqual(result["rc"], 2)
        self.assertEqual(result["status"], "error")

    def test_rc2_on_transport_error(self):
        self._patch(raiser=urllib.error.URLError("connection refused"))
        result = op.run_probe()
        self.assertEqual(result["rc"], 2)
        self.assertEqual(result["status"], "error")
        self.assertIn("connection refused", result["detail"])


class CliTests(unittest.TestCase):
    def setUp(self):
        self._orig = op._http_post

    def tearDown(self):
        op._http_post = self._orig

    def _patch_saturation(self):
        def fake(base_url, body, timeout):
            raise _http_error(503, SATURATION_DETAIL)
        op._http_post = fake

    def test_human_line_saturation(self):
        self._patch_saturation()
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = op.main([])
        self.assertEqual(rc, 1)
        self.assertIn("GEN-SATURATED", buf.getvalue())
        self.assertIn("503", buf.getvalue())

    def test_json_line_matches_rc(self):
        self._patch_saturation()
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = op.main(["--json"])
        line = buf.getvalue().strip()
        self.assertEqual(json.loads(line)["rc"], rc)
        self.assertEqual(json.loads(line)["status"], "saturated")
        self.assertIn("ts", json.loads(line))

    def test_bad_timeout_rejected(self):
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = op.main(["--timeout", "0"])
        self.assertEqual(rc, 2)
        self.assertIn("bad-timeout", buf.getvalue())

    def test_model_passed_through(self):
        captured = {}

        def fake(base_url, body, timeout):
            captured["body"] = body
            return _FakeResp(json.dumps({"done_reason": "stop"}).encode("utf-8"))
        op._http_post = fake
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = op.main(["--model", "probe-model:1b"])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(captured["body"])["model"], "probe-model:1b")

    def test_import_does_not_fly(self):
        # main-guard safety: importing the module must not run a probe
        # (importing must not raise or print; 2026-10-09 hairera lesson).
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            import importlib
            importlib.reload(op)
        self.assertEqual(buf.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
