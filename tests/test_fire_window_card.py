"""Tests for src/os/fire_window_card.py (tech#85 composite card)."""

import contextlib
import datetime
import importlib.util
import io
import json
import os
import sys
import unittest
from unittest import mock

_SPEC = importlib.util.spec_from_file_location(
    "fire_window_card",
    os.path.join(os.path.dirname(__file__), "..", "src", "os",
                 "fire_window_card.py"),
)
fwc = importlib.util.module_from_spec(_SPEC)
sys.modules["fire_window_card"] = fwc
_SPEC.loader.exec_module(fwc)

GATE_GO = {"go": True, "reasons": [], "free_min_mb": 5650,
           "free_max_mb": 5660, "band_mb": 10, "util_max": 2,
           "min_free_mb": 2048}
GATE_NOGO_UTIL = {"go": False, "reasons": [
    "util-face: worst-case util 100% > gate 80%"],
    "free_min_mb": 5669, "free_max_mb": 5686, "band_mb": 17,
    "util_max": 100, "min_free_mb": 2048}
PROBE_OK = {"rc": 0, "status": "ok", "face": "ok", "gpu_free_mb": 5650,
            "evictable_mb": None, "eviction_aware_verdict": None}
PROBE_SATURATED = {"rc": 1, "status": "saturated",
                   "face": "saturated-busy", "gpu_free_mb": 5669,
                   "evictable_mb": None, "eviction_aware_verdict": None}
PROBE_BUSY = {"rc": 2, "status": "error", "face": "busy-contended",
              "gpu_free_mb": 590, "evictable_mb": None,
              "eviction_aware_verdict": None}
PROBE_SKIP_FLY = {"rc": 2, "status": "skipped-not-resident",
                  "face": "not-resident", "gpu_free_mb": 5663,
                  "evictable_mb": 4888, "eviction_aware_verdict": "fly"}
PROBE_SKIP_NOCREDIT = {"rc": 2, "status": "skipped-not-resident",
                       "face": "not-resident", "gpu_free_mb": 3200,
                       "evictable_mb": 4888,
                       "eviction_aware_verdict": "skip"}
PROBE_SKIP_NO_EVICTABLE = {"rc": 2, "status": "skipped-not-resident",
                           "face": "not-resident", "gpu_free_mb": 5663,
                           "evictable_mb": None,
                           "eviction_aware_verdict": "fly"}
MV_QUIET = {"verdict": "quiet", "rc": 0, "newest_age_min": 318.2}
MV_ACTIVE = {"verdict": "active", "rc": 1, "newest_age_min": 4.0}
MV_ERROR = {"verdict": None, "rc": 2, "newest_age_min": None}
CREDIT_GO = {"go": True, "reasons": [], "free_min_mb": 5669,
             "free_max_mb": 5674, "band_mb": 5, "util_max": 40,
             "min_free_mb": 2048, "evictable_mb": 4888,
             "effective_free_mb": 10557}
CREDIT_NOGO = {"go": False, "reasons": [
    "util-face: worst-case util 100% > gate 80%"],
    "free_min_mb": 5669, "free_max_mb": 5674, "band_mb": 5,
    "util_max": 100, "min_free_mb": 2048, "evictable_mb": 4888,
    "effective_free_mb": 10557}


class ClassifyFireTests(unittest.TestCase):
    def test_path_a_fire(self):
        verdict, path, reasons = fwc.classify_fire(
            GATE_GO, MV_QUIET, PROBE_OK)
        self.assertEqual(verdict, "fire")
        self.assertEqual(path, "A-hot-resident")
        self.assertEqual(reasons, [])

    def test_path_a_gate_no_go(self):
        verdict, path, reasons = fwc.classify_fire(
            GATE_NOGO_UTIL, MV_QUIET, PROBE_OK)
        self.assertEqual(verdict, "no-fire")
        self.assertIsNone(path)
        self.assertEqual(reasons[0], "gate-static-no-go")
        self.assertIn(GATE_NOGO_UTIL["reasons"][0], reasons)

    def test_mv_active_blocks_both_paths(self):
        verdict, _, reasons = fwc.classify_fire(
            GATE_GO, MV_ACTIVE, PROBE_OK, CREDIT_GO)
        self.assertEqual(verdict, "no-fire")
        self.assertEqual(reasons, ["mv-active"])

    def test_mv_unreadable_fail_closed(self):
        verdict, _, reasons = fwc.classify_fire(
            GATE_GO, MV_ERROR, PROBE_OK, CREDIT_GO)
        self.assertEqual(verdict, "no-fire")
        self.assertEqual(reasons, ["mv-unreadable-fail-closed"])

    def test_probe_saturated_no_fire(self):
        verdict, _, reasons = fwc.classify_fire(
            GATE_GO, MV_QUIET, PROBE_SATURATED)
        self.assertEqual(verdict, "no-fire")
        self.assertEqual(reasons, ["probe-face-saturated-busy"])

    def test_probe_busy_no_fire(self):
        verdict, _, reasons = fwc.classify_fire(
            GATE_GO, MV_QUIET, PROBE_BUSY)
        self.assertEqual(verdict, "no-fire")
        self.assertEqual(reasons, ["probe-face-busy-contended"])

    def test_path_b_fire(self):
        verdict, path, reasons = fwc.classify_fire(
            GATE_NOGO_UTIL, MV_QUIET, PROBE_SKIP_FLY, CREDIT_GO)
        self.assertEqual(verdict, "fire")
        self.assertEqual(path, "B-eviction-credit")
        self.assertEqual(reasons, [])

    def test_path_b_counterfactual_not_fly(self):
        verdict, _, reasons = fwc.classify_fire(
            GATE_NOGO_UTIL, MV_QUIET, PROBE_SKIP_NOCREDIT)
        self.assertEqual(verdict, "no-fire")
        self.assertEqual(reasons, ["cold-skip-no-admissible-credit"])

    def test_path_b_credit_window_closed(self):
        verdict, _, reasons = fwc.classify_fire(
            GATE_NOGO_UTIL, MV_QUIET, PROBE_SKIP_FLY, None)
        self.assertEqual(verdict, "no-fire")
        self.assertEqual(reasons, ["credit-window-closed"])

    def test_path_b_credit_no_go(self):
        verdict, _, reasons = fwc.classify_fire(
            GATE_NOGO_UTIL, MV_QUIET, PROBE_SKIP_FLY, CREDIT_NOGO)
        self.assertEqual(verdict, "no-fire")
        self.assertEqual(reasons[0], "gate-credit-no-go")
        self.assertIn(CREDIT_NOGO["reasons"][0], reasons)

    def test_probe_error_without_face_cites_status(self):
        verdict, _, reasons = fwc.classify_fire(
            GATE_GO, MV_QUIET, {"status": "error", "face": None})
        self.assertEqual(verdict, "no-fire")
        self.assertEqual(reasons, ["probe-status-error"])


class OrchestrateTests(unittest.TestCase):
    def _fake_gate(self, reading):
        def fn(samples, interval, min_free, util_max):
            self.calls.append("gate(%s,%s,%s,%s)"
                              % (samples, interval, min_free, util_max))
            return reading
        return fn

    def _fake_credit(self, reading):
        def fn(credit_mb, samples, interval, min_free, util_max):
            self.calls.append("credit(%s,%s,%s,%s,%s)"
                              % (credit_mb, samples, interval, min_free,
                                 util_max))
            return reading
        return fn

    def _fake_mv(self, reading):
        def fn():
            self.calls.append("mv")
            return reading
        return fn

    def _fake_probe(self, reading):
        def fn():
            self.calls.append("probe")
            return reading
        return fn

    def setUp(self):
        self.calls = []

    def test_sequence_law_gate_first_probe_last(self):
        card = fwc.orchestrate(
            self._fake_gate(GATE_GO), self._fake_mv(MV_QUIET),
            self._fake_probe(PROBE_OK), self._fake_credit(CREDIT_GO))
        order = [c.split("(")[0] for c in self.calls]
        self.assertEqual(order, ["gate", "mv", "probe"])
        self.assertEqual(card["sequence"],
                         ["gate-static", "mv-probe", "ollama-probe"])

    def test_path_a_no_credit_rerun(self):
        card = fwc.orchestrate(
            self._fake_gate(GATE_GO), self._fake_mv(MV_QUIET),
            self._fake_probe(PROBE_OK), self._fake_credit(CREDIT_GO))
        self.assertEqual(card["verdict"], "fire")
        self.assertEqual(card["path"], "A-hot-resident")
        self.assertNotIn("gate-credit", card["sequence"])

    def test_credit_rerun_follows_skip_path_probe(self):
        card = fwc.orchestrate(
            self._fake_gate(GATE_NOGO_UTIL), self._fake_mv(MV_QUIET),
            self._fake_probe(PROBE_SKIP_FLY), self._fake_credit(CREDIT_GO),
            samples=6, interval=5, min_free=2048, util_max=80)
        self.assertEqual(card["sequence"][-1], "gate-credit")
        self.assertEqual(card["verdict"], "fire")
        self.assertEqual(card["path"], "B-eviction-credit")
        # credit value passing: probe evictable_mb fed to the gate re-run
        self.assertIn("credit(4888,6,5,2048,80)", self.calls)
        self.assertEqual(card["readings"]["gate_credit"]["evictable_mb"],
                         4888)
        self.assertEqual(card["readings"]["gate_credit"]
                         ["effective_free_mb"], 10557)

    def test_credit_rerun_blocked_when_mv_active(self):
        card = fwc.orchestrate(
            self._fake_gate(GATE_GO), self._fake_mv(MV_ACTIVE),
            self._fake_probe(PROBE_SKIP_FLY), self._fake_credit(CREDIT_GO))
        self.assertNotIn("gate-credit", card["sequence"])
        self.assertEqual(card["verdict"], "no-fire")
        self.assertEqual(card["reasons"], ["mv-active"])

    def test_credit_rerun_blocked_when_counterfactual_skip(self):
        card = fwc.orchestrate(
            self._fake_gate(GATE_NOGO_UTIL), self._fake_mv(MV_QUIET),
            self._fake_probe(PROBE_SKIP_NOCREDIT),
            self._fake_credit(CREDIT_GO))
        self.assertNotIn("gate-credit", card["sequence"])
        self.assertEqual(card["verdict"], "no-fire")
        self.assertEqual(card["reasons"],
                         ["cold-skip-no-admissible-credit"])

    def test_credit_rerun_blocked_when_evictable_missing(self):
        card = fwc.orchestrate(
            self._fake_gate(GATE_NOGO_UTIL), self._fake_mv(MV_QUIET),
            self._fake_probe(PROBE_SKIP_NO_EVICTABLE),
            self._fake_credit(CREDIT_GO))
        self.assertNotIn("gate-credit", card["sequence"])
        self.assertEqual(card["verdict"], "no-fire")
        self.assertEqual(card["reasons"], ["credit-window-closed"])

    def test_card_shape_and_slim_readings(self):
        card = fwc.orchestrate(
            self._fake_gate(GATE_NOGO_UTIL), self._fake_mv(MV_QUIET),
            self._fake_probe(PROBE_SKIP_FLY), self._fake_credit(CREDIT_GO))
        self.assertEqual(card["card"], "fire_window_card")
        for key in ("ts", "verdict", "path", "reasons", "sequence",
                    "readings"):
            self.assertIn(key, card)
        self.assertEqual(card["readings"]["gate"]["free_min_mb"], 5669)
        self.assertEqual(card["readings"]["mv"]["newest_age_min"], 318.2)
        self.assertEqual(card["readings"]["probe"]["evictable_mb"], 4888)
        self.assertEqual(card["readings"]["probe"]
                         ["eviction_aware_verdict"], "fly")


class FireFreshnessTests(unittest.TestCase):
    """tech#89 candidate (1): a fire verdict carries fired_at +
    valid_s + expires_at so a consumer can reject a stale GO
    (R1943 anchor: window closed <2min after the card said fire)."""

    NOW = datetime.datetime(2026, 10, 11, 5, 24, 11)

    def _card(self, gate, probe, credit):
        return fwc.orchestrate(
            lambda *a: gate, lambda: MV_QUIET, lambda: probe,
            lambda *a: credit, now=self.NOW)

    def test_path_a_fire_carries_freshness_fields(self):
        card = self._card(GATE_GO, PROBE_OK, CREDIT_GO)
        self.assertEqual(card["verdict"], "fire")
        self.assertEqual(card["fired_at"],
                         int(self.NOW.timestamp()))
        self.assertEqual(card["valid_s"], fwc.FIRE_VALID_S)
        self.assertEqual(card["expires_at"],
                         card["fired_at"] + fwc.FIRE_VALID_S)

    def test_path_b_fire_carries_freshness_fields(self):
        card = self._card(GATE_NOGO_UTIL, PROBE_SKIP_FLY, CREDIT_GO)
        self.assertEqual(card["verdict"], "fire")
        self.assertEqual(card["path"], "B-eviction-credit")
        self.assertEqual(card["expires_at"] - card["fired_at"],
                         fwc.FIRE_VALID_S)

    def test_no_fire_omits_freshness_fields(self):
        card = self._card(GATE_NOGO_UTIL, PROBE_OK, CREDIT_GO)
        self.assertEqual(card["verdict"], "no-fire")
        for key in ("fired_at", "valid_s", "expires_at"):
            self.assertNotIn(key, card)

    def test_human_render_carries_fire_valid_line(self):
        card = self._card(GATE_GO, PROBE_OK, CREDIT_GO)
        text = fwc._render_human(card)
        self.assertIn("fire-valid:", text)
        self.assertIn(str(fwc.FIRE_VALID_S), text)
        self.assertIn(str(card["expires_at"]), text)

    def test_human_render_no_fire_no_valid_line(self):
        card = self._card(GATE_NOGO_UTIL, PROBE_OK, CREDIT_GO)
        self.assertNotIn("fire-valid:", fwc._render_human(card))


class CliTests(unittest.TestCase):
    def _run_main(self, argv, patches):
        cm = mock.patch.multiple(fwc, **patches) if patches \
            else contextlib.nullcontext()
        with cm:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = fwc.main(argv)
        return rc, buf.getvalue()

    def test_json_fire_rc0(self):
        rc, out = self._run_main(["--json"], {
            "real_gate_static": lambda *a: GATE_GO,
            "real_mv_probe": lambda: MV_QUIET,
            "real_ollama_probe": lambda: PROBE_OK,
            "real_gate_credit": lambda *a: CREDIT_GO,
        })
        self.assertEqual(rc, 0)
        payload = json.loads(out.strip().splitlines()[-1])
        self.assertEqual(payload["verdict"], "fire")
        self.assertEqual(payload["path"], "A-hot-resident")

    def test_json_no_fire_rc1(self):
        rc, out = self._run_main(["--json"], {
            "real_gate_static": lambda *a: GATE_NOGO_UTIL,
            "real_mv_probe": lambda: MV_QUIET,
            "real_ollama_probe": lambda: PROBE_OK,
            "real_gate_credit": lambda *a: CREDIT_GO,
        })
        self.assertEqual(rc, 1)
        payload = json.loads(out.strip().splitlines()[-1])
        self.assertEqual(payload["verdict"], "no-fire")
        self.assertIn("gate-static-no-go", payload["reasons"])

    def test_child_error_rc2_fail_closed(self):
        def boom(*a, **kw):
            raise fwc.CardChildError("child failed: timeout")
        rc, out = self._run_main(["--json"], {
            "real_gate_static": boom,
            "real_mv_probe": lambda: MV_QUIET,
            "real_ollama_probe": lambda: PROBE_OK,
            "real_gate_credit": lambda *a: CREDIT_GO,
        })
        self.assertEqual(rc, 2)
        payload = json.loads(out.strip().splitlines()[-1])
        self.assertEqual(payload["verdict"], "error")

    def test_bad_args_rc2(self):
        rc, _ = self._run_main(["--samples", "0"], {})
        self.assertEqual(rc, 2)
        rc, _ = self._run_main(["--util-max", "-1"], {})
        self.assertEqual(rc, 2)


class ReadingsTimestampTests(unittest.TestCase):
    """tech#90: readings are collected sequentially, so by verdict time
    the oldest (gate) reading is already tens of seconds stale -- the
    120s fire TTL's usable margin is silently eaten. Every slim
    reading carries collected_at + age_s_at_verdict, the card carries
    oldest_reading_age_s, and the human face renders a readings-age
    line so a consumer can discount the TTL by read-side staleness."""

    BASE = datetime.datetime(2026, 10, 11, 6, 0, 0)

    def _clock(self, step_s):
        state = {"n": 0}

        def clock():
            stamp = self.BASE + datetime.timedelta(
                seconds=state["n"] * step_s)
            state["n"] += 1
            return stamp
        return clock

    def _card(self, gate, probe, credit, step_s=10, now=None):
        return fwc.orchestrate(
            lambda *a: gate, lambda: MV_QUIET, lambda: probe,
            lambda *a: credit, now=now, clock=self._clock(step_s))

    def test_age_math_deterministic_path_b(self):
        # clock calls: gate@0s mv@10s probe@20s credit@30s verdict@40s
        card = self._card(GATE_NOGO_UTIL, PROBE_SKIP_FLY, CREDIT_GO)
        self.assertEqual(card["verdict"], "fire")
        readings = card["readings"]
        self.assertEqual(readings["gate"]["age_s_at_verdict"], 40)
        self.assertEqual(readings["mv"]["age_s_at_verdict"], 30)
        self.assertEqual(readings["probe"]["age_s_at_verdict"], 20)
        self.assertEqual(readings["gate_credit"]["age_s_at_verdict"], 10)
        # oldest = the first-collected gate reading
        self.assertEqual(card["oldest_reading_age_s"], 40)

    def test_age_math_deterministic_path_a_no_credit(self):
        # clock calls: gate@0s mv@10s probe@20s verdict@30s (no credit)
        card = self._card(GATE_GO, PROBE_OK, CREDIT_GO)
        self.assertEqual(card["verdict"], "fire")
        self.assertEqual(card["readings"]["gate"]["age_s_at_verdict"],
                         30)
        self.assertNotIn("gate_credit", card["sequence"])
        self.assertIsNone(card["readings"]["gate_credit"])
        self.assertEqual(card["oldest_reading_age_s"], 30)

    def test_collected_at_string_format(self):
        card = self._card(GATE_NOGO_UTIL, PROBE_SKIP_FLY, CREDIT_GO)
        self.assertEqual(card["readings"]["gate"]["collected_at"],
                         "2026-10-11 06:00:00")
        self.assertEqual(card["readings"]["gate_credit"]
                         ["collected_at"], "2026-10-11 06:00:30")
        for name in ("gate", "mv", "probe", "gate_credit"):
            reading = card["readings"][name]
            self.assertRegex(reading["collected_at"],
                             r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
            self.assertIsInstance(reading["age_s_at_verdict"], int)

    def test_now_override_uses_now_for_verdict_ts(self):
        # explicit now still wins for the verdict ts (backward compat
        # with FireFreshnessTests); ages read against that now.
        now = datetime.datetime(2026, 10, 11, 6, 1, 0)
        card = self._card(GATE_NOGO_UTIL, PROBE_SKIP_FLY, CREDIT_GO,
                          step_s=10, now=now)
        self.assertEqual(card["ts"], "2026-10-11 06:01:00")
        self.assertEqual(card["readings"]["gate"]["age_s_at_verdict"],
                         60)
        self.assertEqual(card["oldest_reading_age_s"], 60)

    def test_human_render_carries_readings_age_line(self):
        card = self._card(GATE_NOGO_UTIL, PROBE_SKIP_FLY, CREDIT_GO)
        text = fwc._render_human(card)
        self.assertIn("readings-age:", text)
        self.assertIn("gate=40s", text)
        self.assertIn("mv=30s", text)
        self.assertIn("probe=20s", text)
        self.assertIn("gate_credit=10s", text)
        self.assertIn("oldest=40s", text)
        self.assertIn(str(fwc.FIRE_VALID_S), text)

    def test_human_render_path_a_omits_credit_age(self):
        card = self._card(GATE_GO, PROBE_OK, CREDIT_GO)
        text = fwc._render_human(card)
        self.assertIn("gate=30s", text)
        self.assertNotIn("gate_credit=", text)

    def test_no_fire_path_carries_ages_too(self):
        # freshness face is read-side, not verdict-side: a no-fire card
        # still archives the staleness readings for the record.
        card = self._card(GATE_NOGO_UTIL, PROBE_OK, CREDIT_GO)
        self.assertEqual(card["verdict"], "no-fire")
        self.assertIn("age_s_at_verdict",
                      card["readings"]["gate"])
        self.assertEqual(card["oldest_reading_age_s"], 30)


if __name__ == "__main__":
    unittest.main()
