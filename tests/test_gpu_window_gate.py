"""Tests for src/os/gpu_window_gate.py (tech#57 + tech#75 stability face)."""

import contextlib
import importlib.util
import io
import json
import os
import sys
import unittest
from unittest import mock

_SPEC = importlib.util.spec_from_file_location(
    "gpu_window_gate",
    os.path.join(os.path.dirname(__file__), "..", "src", "os",
                 "gpu_window_gate.py"),
)
gate = importlib.util.module_from_spec(_SPEC)
sys.modules["gpu_window_gate"] = gate
_SPEC.loader.exec_module(gate)


class ParseTaskDisabledTests(unittest.TestCase):
    def test_en_disabled(self):
        out = ("Folder: \\\nHostName:      DASHENG\n"
               "TaskName:      \\BigCompute-OSLoop\nNext Run Time: N/A\n"
               "Status:        Disabled\nLogon Mode:    Interactive only\n")
        self.assertIs(gate.parse_task_disabled(out), True)

    def test_en_ready(self):
        out = ("TaskName:      \\BigCompute-OSLoop\n"
               "Status:        Ready\n")
        self.assertIs(gate.parse_task_disabled(out), False)

    def test_zh_disabled(self):
        out = "任务名:      \\X\n状态:        已禁用\n"
        self.assertIs(gate.parse_task_disabled(out), True)

    def test_no_status_line(self):
        self.assertIsNone(gate.parse_task_disabled("hostname only\n"))
        self.assertIsNone(gate.parse_task_disabled(None))


class ClassifyPauseFaceTests(unittest.TestCase):
    def _states(self, n_disabled, n_enabled, n_none=0):
        s = {}
        for i in range(n_disabled):
            s["d%d" % i] = True
        for i in range(n_enabled):
            s["e%d" % i] = False
        for i in range(n_none):
            s["u%d" % i] = None
        return s

    def test_fingerprint_at_six(self):
        label, dis, tot, known = gate.classify_pause_face(
            self._states(6, 2))
        self.assertEqual(label, "pause-fingerprint")
        self.assertEqual((dis, tot, known), (6, 8, 8))

    def test_ambiguous_four_five(self):
        for nd in (4, 5):
            label = gate.classify_pause_face(self._states(nd, 8 - nd))[0]
            self.assertEqual(label, "ambiguous")

    def test_clear_at_three(self):
        label = gate.classify_pause_face(self._states(3, 5))[0]
        self.assertEqual(label, "clear")

    def test_unknown_all_none(self):
        label, dis, tot, known = gate.classify_pause_face(self._states(0, 0, 8))
        self.assertEqual(label, "unknown")
        self.assertEqual(known, 0)

    def test_mixed_known_wins(self):
        # 6 disabled + 2 unreadable -> still fingerprint (6 of 8 counted)
        label, dis, tot, known = gate.classify_pause_face(self._states(6, 0, 2))
        self.assertEqual(label, "pause-fingerprint")
        self.assertEqual((dis, known), (6, 6))

    def test_empty(self):
        self.assertEqual(gate.classify_pause_face({})[0], "unknown")


class DecideTests(unittest.TestCase):
    def test_fingerprint_blocks_despite_vram_pass(self):
        v = gate.decide("pause-fingerprint", 11000, 9216)
        self.assertFalse(v["go"])

    def test_ambiguous_conservative_no_go(self):
        v = gate.decide("ambiguous", 11000, 9216)
        self.assertFalse(v["go"])

    def test_clear_vram_pass_go(self):
        v = gate.decide("clear", 10000, 9216)
        self.assertTrue(v["go"])
        self.assertEqual(len(v["reasons"]), 1)

    def test_clear_vram_fail_no_go(self):
        v = gate.decide("clear", 9000, 9216)
        self.assertFalse(v["go"])

    def test_vram_boundary_strict_less(self):
        self.assertTrue(gate.decide("clear", 9216, 9216)["go"])
        self.assertFalse(gate.decide("clear", 9215, 9216)["go"])

    def test_unknown_pause_vram_pass_go_with_note(self):
        v = gate.decide("unknown", 10000, 9216)
        self.assertTrue(v["go"])

    def test_vram_unreadable_blocks_when_clear(self):
        v = gate.decide("clear", None, 9216)
        self.assertFalse(v["go"])


class CliTests(unittest.TestCase):
    def _run_main(self, argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = gate.main(argv)
        return rc, buf.getvalue()

    def test_json_row_and_rc(self):
        with mock.patch.object(gate, "query_task_states",
                               return_value={t: True for t in
                                             gate.MACHINE_STATE_TASKS}), \
             mock.patch.object(gate, "read_vram_free_mb",
                               return_value=11000), \
             mock.patch.object(gate, "query_compute_apps",
                               return_value=None):
            rc, out = self._run_main(["--json"])
        self.assertEqual(rc, 1)
        self.assertIn("pause-fingerprint", out)

    def test_go_rc_zero(self):
        with mock.patch.object(gate, "query_task_states",
                               return_value={t: False for t in
                                             gate.MACHINE_STATE_TASKS}), \
             mock.patch.object(gate, "read_vram_free_mb",
                               return_value=11000):
            rc, out = self._run_main([])
        self.assertEqual(rc, 0)
        self.assertIn("VERDICT=GO", out)

    def test_probe_error_rc_two(self):
        with mock.patch.object(gate, "query_task_states",
                               return_value={t: None for t in
                                             gate.MACHINE_STATE_TASKS}), \
             mock.patch.object(gate, "read_vram_free_mb", return_value=None), \
             mock.patch.object(gate, "query_compute_apps",
                               return_value=None):
            rc, out = self._run_main(["--json"])
        self.assertEqual(rc, 2)
        self.assertIn("null", out)


class ReadGpuSampleTests(unittest.TestCase):
    def test_parse_ok(self):
        with mock.patch.object(gate, "_run_capture",
                               return_value="12288, 3278, 68\n"):
            r = gate.read_gpu_sample()
        self.assertEqual(r, {"free": 9010, "util": 68})

    def test_multi_gpu_first_row(self):
        with mock.patch.object(gate, "_run_capture",
                               return_value="12288, 4000, 25\n12288, 0, 0\n"):
            r = gate.read_gpu_sample()
        self.assertEqual(r, {"free": 8288, "util": 25})

    def test_probe_failure_none(self):
        with mock.patch.object(gate, "_run_capture", return_value=None):
            self.assertIsNone(gate.read_gpu_sample())
        with mock.patch.object(gate, "_run_capture", return_value="junk\n"):
            self.assertIsNone(gate.read_gpu_sample())
        with mock.patch.object(gate, "_run_capture", return_value="1,2\n"):
            self.assertIsNone(gate.read_gpu_sample())


class SampleGpuTests(unittest.TestCase):
    def test_counts_and_sleep_injection(self):
        calls = []

        def sampler():
            calls.append(1)
            return {"free": 100, "util": 5}

        sleeps = []

        def sleep_fn(s):
            sleeps.append(s)

        readings, n_fail = gate.sample_gpu(3, 5, sampler=sampler,
                                           sleep_fn=sleep_fn)
        self.assertEqual(len(readings), 3)
        self.assertEqual(n_fail, 0)
        self.assertEqual(sleeps, [5, 5])  # n-1 sleeps

    def test_failures_counted_not_fabricated(self):
        seq = [{"free": 100, "util": 5}, None, {"free": 90, "util": 9}]

        def sampler():
            return seq.pop(0) if seq else None

        readings, n_fail = gate.sample_gpu(3, 0, sampler=sampler,
                                          sleep_fn=lambda s: None)
        self.assertEqual(len(readings), 2)
        self.assertEqual(n_fail, 1)


class AggregateGpuReadingsTests(unittest.TestCase):
    def test_r1917_anchor_shape(self):
        # R1917 real readings: 3278 <-> 11692 swing, band 8414
        agg = gate.aggregate_gpu_readings([
            {"free": 9010, "util": 68}, {"free": 610, "util": 77},
        ])
        self.assertEqual(agg["free_min"], 610)
        self.assertEqual(agg["free_max"], 9010)
        self.assertEqual(agg["band_mb"], 8400)
        self.assertEqual(agg["util_max"], 77)
        self.assertEqual(agg["read_ok"], 2)
        self.assertEqual(agg["read_fail"], 0)

    def test_empty_none(self):
        self.assertIsNone(gate.aggregate_gpu_readings([], 3))

    def test_single_reading_band_zero(self):
        agg = gate.aggregate_gpu_readings([{"free": 9010, "util": 68}])
        self.assertEqual(agg["band_mb"], 0)

    def test_util_missing_column(self):
        agg = gate.aggregate_gpu_readings([{"free": 100}])
        self.assertIsNone(agg["util_max"])


class DecideStabilityTests(unittest.TestCase):
    def test_worst_case_min_fails_no_go(self):
        v = gate.decide("clear", 610, 2048, sampled=True,
                        band_mb=8400, max_util=77, util_max=80)
        self.assertFalse(v["go"])
        self.assertTrue(any("worst-case" in r for r in v["reasons"]))

    def test_band_advisory_present_but_go(self):
        v = gate.decide("clear", 9010, 2048, sampled=True,
                        band_mb=2048, max_util=77, util_max=80)
        self.assertTrue(v["go"])
        self.assertTrue(any("vram-band advisory" in r
                            for r in v["reasons"]))

    def test_band_below_threshold_no_advisory(self):
        v = gate.decide("clear", 9010, 2048, sampled=True,
                        band_mb=2047, max_util=77, util_max=80)
        self.assertTrue(v["go"])
        self.assertFalse(any("vram-band advisory" in r
                             for r in v["reasons"]))

    def test_util_gate_strict_boundary(self):
        self.assertTrue(gate.decide("clear", 9010, 2048, sampled=True,
                                    max_util=80, util_max=80)["go"])
        self.assertFalse(gate.decide("clear", 9010, 2048, sampled=True,
                                      max_util=81, util_max=80)["go"])

    def test_util_unreadable_with_gate_conservative(self):
        v = gate.decide("clear", 9010, 2048, sampled=True,
                        max_util=None, util_max=80)
        self.assertFalse(v["go"])
        self.assertTrue(any("util-face" in r for r in v["reasons"]))

    def test_read_fail_note(self):
        v = gate.decide("clear", 9010, 2048, sampled=True,
                        band_mb=0, read_fail=2)
        self.assertTrue(v["go"])
        self.assertTrue(any("2 probe sample(s) failed" in r
                            for r in v["reasons"]))

    def test_legacy_call_signature_unchanged(self):
        # 3-arg call = pre-tech#75 behavior, no new reason text
        v = gate.decide("clear", 10000, 9216)
        self.assertTrue(v["go"])
        self.assertEqual(len(v["reasons"]), 1)
        self.assertIn("both faces clear", v["reasons"][0])


class CliStabilityTests(unittest.TestCase):
    def _run_main(self, argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = gate.main(argv)
        return rc, buf.getvalue()

    def _clear_tasks(self):
        return {t: False for t in gate.MACHINE_STATE_TASKS}

    def test_samples_go_json_fields(self):
        readings = [{"free": 9010, "util": 68}, {"free": 8900, "util": 75},
                    {"free": 9050, "util": 60}]
        with mock.patch.object(gate, "query_task_states",
                               return_value=self._clear_tasks()), \
             mock.patch.object(gate, "read_gpu_sample",
                               side_effect=list(readings)), \
             mock.patch.object(gate, "time") as mt:
            mt.sleep = lambda s: None
            rc, out = self._run_main(
                ["--samples", "3", "--min-free-mb", "2048",
                 "--util-max", "80", "--json"])
        self.assertEqual(rc, 0)
        row = json.loads(out)
        self.assertTrue(row["go"])
        self.assertEqual(row["free_min_mb"], 8900)
        self.assertEqual(row["band_mb"], 150)
        self.assertEqual(row["util_max"], 75)
        self.assertEqual(row["read_ok"], 3)

    def test_samples_worst_case_no_go(self):
        readings = [{"free": 9010, "util": 68}, {"free": 610, "util": 77}]
        with mock.patch.object(gate, "query_task_states",
                               return_value=self._clear_tasks()), \
             mock.patch.object(gate, "read_gpu_sample",
                               side_effect=list(readings)), \
             mock.patch.object(gate, "query_compute_apps",
                               return_value=None), \
             mock.patch.object(gate, "time") as mt:
            mt.sleep = lambda s: None
            rc, out = self._run_main(
                ["--samples", "2", "--min-free-mb", "2048", "--json"])
        self.assertEqual(rc, 1)
        row = json.loads(out)
        self.assertFalse(row["go"])
        self.assertEqual(row["free_min_mb"], 610)
        self.assertTrue(any("worst-case" in r for r in row["reasons"]))

    def test_samples_all_fail_probe_blind(self):
        with mock.patch.object(gate, "query_task_states",
                               return_value=self._clear_tasks()), \
             mock.patch.object(gate, "read_gpu_sample",
                               return_value=None), \
             mock.patch.object(gate, "query_compute_apps",
                               return_value=None), \
             mock.patch.object(gate, "time") as mt:
            mt.sleep = lambda s: None
            rc, out = self._run_main(["--samples", "3", "--json"])
        self.assertEqual(rc, 1)  # pause clear + vram unreadable -> NO-GO
        row = json.loads(out)
        self.assertFalse(row["go"])

    def test_util_max_single_sample_uses_sampled_path(self):
        with mock.patch.object(gate, "query_task_states",
                               return_value=self._clear_tasks()), \
             mock.patch.object(gate, "read_gpu_sample",
                               return_value={"free": 9010, "util": 95}), \
             mock.patch.object(gate, "query_compute_apps",
                               return_value=None):
            rc, out = self._run_main(
                ["--min-free-mb", "2048", "--util-max", "80"])
        self.assertEqual(rc, 1)
        self.assertIn("util-face", out)

    def test_legacy_path_untouched(self):
        # no --samples/--util-max: single-sample read via read_vram_free_mb
        with mock.patch.object(gate, "query_task_states",
                               return_value=self._clear_tasks()), \
             mock.patch.object(gate, "read_vram_free_mb",
                               return_value=11000):
            rc, out = self._run_main([])
        self.assertEqual(rc, 0)
        self.assertIn("VERDICT=GO", out)

    def test_bad_samples_arg(self):
        with self.assertRaises(SystemExit):
            gate.main(["--samples", "0"])


class QueryComputeAppsTests(unittest.TestCase):
    def test_parse_ok(self):
        with mock.patch.object(
                gate, "_run_capture",
                return_value="58200, python.exe\n"
                             "38828, Tuanjie.exe\n"):
            rows = gate.query_compute_apps()
        self.assertEqual(rows, [
            {"pid": 58200, "process": "python.exe"},
            {"pid": 38828, "process": "Tuanjie.exe"},
        ])

    def test_banner_and_junk_pid_rows_skipped(self):
        # 'No running processes found' banner / non-integer pid -> skipped;
        # empty list is an honest zero-consumers reading, not None
        with mock.patch.object(
                gate, "_run_capture",
                return_value="No running processes found\n"
                             "abc, weird.exe\n"):
            self.assertEqual(gate.query_compute_apps(), [])

    def test_probe_failure_none(self):
        with mock.patch.object(gate, "_run_capture", return_value=None):
            self.assertIsNone(gate.query_compute_apps())
        with mock.patch.object(gate, "_run_capture", return_value=""):
            self.assertIsNone(gate.query_compute_apps())


class ClassifyProducersTests(unittest.TestCase):
    def test_whitelist_listed_rest_folded(self):
        att = gate.classify_producers([
            {"pid": 58200, "process": "python.exe"},
            {"pid": 67848, "process": "llama-server.exe"},
            {"pid": 38828, "process": "Tuanjie.exe"},
            {"pid": 999, "process": "dwm.exe"},
        ])
        self.assertEqual([p["pid"] for p in att["producers"]],
                         [58200, 67848, 38828])
        self.assertEqual(att["other"], 1)
        self.assertEqual(att["raw"], 4)

    def test_patterns_override(self):
        att = gate.classify_producers(
            [{"pid": 9, "process": "zzz.exe"},
             {"pid": 10, "process": "python.exe"}],
            patterns=("zzz",))
        self.assertEqual([p["pid"] for p in att["producers"]], [9])
        self.assertEqual(att["other"], 1)

    def test_match_case_insensitive(self):
        att = gate.classify_producers(
            [{"pid": 1, "process": "PYTHON.EXE"},
             {"pid": 2, "process": "ComfyUI.exe"}])
        self.assertEqual(att["other"], 0)
        self.assertEqual(len(att["producers"]), 2)


class ProducerNoiseFoldTests(unittest.TestCase):
    """tech#80: GUI tray/launcher shells fold to other before whitelist.

    R1930 live anchor: unityvcstray.exe (PlasticSCM tray) matched the
    "unity" producer pattern; Tuanjie Hub.exe (launcher shell) matched
    "tuanjie" -- both GUI noise, not VRAM producers.
    """

    def test_r1930_anchor_tray_and_hub_fold(self):
        rows = [
            {"pid": 40564, "process":
             r"C:\Program Files\PlasticSCM5\client\unityvcstray.exe"},
            {"pid": 37376, "process":
             r"C:\Program Files\Tuanjie Hub\Tuanjie Hub.exe"},
            {"pid": 58200, "process":
             r"C:\Users\sjs20\comfyui-krea\ComfyUI_windows_portable"
             r"\python_embeded\python.exe"},
            {"pid": 38828, "process":
             r"C:\Program Files\Tuanjie\Hub\Editor\2022.3.55t4\Editor"
             r"\Tuanjie.exe"},
            {"pid": 60536, "process":
             r"C:\Users\sjs20\AppData\Local\Programs\Ollama\lib"
             r"\ollama\llama-server.exe"},
        ]
        att = gate.classify_producers(rows)
        self.assertEqual([p["pid"] for p in att["producers"]],
                         [58200, 38828, 60536])
        self.assertEqual(att["other"], 2)
        self.assertEqual(att["raw"], 5)

    def test_noise_matches_basename_not_directory(self):
        # R1931 first-cut anchor: matching "hub" against the FULL path
        # false-folded the real Tuanjie editor (installed under
        # \Hub\Editor\); noise must read the exe basename only.
        att = gate.classify_producers([
            {"pid": 38828, "process":
             r"C:\Program Files\Tuanjie\Hub\Editor\2022.3.55t4\Editor"
             r"\Tuanjie.exe"},
            {"pid": 37376, "process":
             r"C:\Program Files\Tuanjie Hub\Tuanjie Hub.exe"},
        ])
        self.assertEqual([p["pid"] for p in att["producers"]], [38828])
        self.assertEqual(att["other"], 1)

    def test_noise_case_insensitive(self):
        att = gate.classify_producers(
            [{"pid": 1, "process": "UNITYVCSTRAY.EXE"},
             {"pid": 2, "process": "Tuanjie HUB.exe"},
             {"pid": 3, "process": "python.exe"}])
        self.assertEqual([p["pid"] for p in att["producers"]], [3])
        self.assertEqual(att["other"], 2)

    def test_noise_override_empty_restores_legacy_face(self):
        att = gate.classify_producers(
            [{"pid": 9, "process": "unityvcstray.exe"},
             {"pid": 10, "process": "python.exe"}],
            noise=())
        # raw-whitelist face for callers who want the unfiltered read
        self.assertEqual([p["pid"] for p in att["producers"]], [9, 10])
        self.assertEqual(att["other"], 0)

    def test_custom_noise_list_param(self):
        att = gate.classify_producers(
            [{"pid": 1, "process": "myhub-python.exe"},
             {"pid": 2, "process": "python.exe"},
             {"pid": 3, "process": "trayapp.exe"}],
            noise=("hub",))
        self.assertEqual([p["pid"] for p in att["producers"]], [2])
        self.assertEqual(att["other"], 2)

    def test_noise_row_not_matching_producers_also_folds(self):
        # noise check runs before the whitelist: a noise row that would
        # not have matched producers folds the same way (no double path)
        att = gate.classify_producers(
            [{"pid": 5, "process": "SystemTray.exe"},
             {"pid": 6, "process": "python.exe"}])
        self.assertEqual([p["pid"] for p in att["producers"]], [6])
        self.assertEqual(att["other"], 1)


class CliAttributionTests(unittest.TestCase):
    def _run_main(self, argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = gate.main(argv)
        return rc, buf.getvalue()

    def _clear_tasks(self):
        return {t: False for t in gate.MACHINE_STATE_TASKS}

    def test_no_go_json_carries_attribution(self):
        with mock.patch.object(gate, "query_task_states",
                               return_value=self._clear_tasks()), \
             mock.patch.object(gate, "read_vram_free_mb",
                               return_value=100), \
             mock.patch.object(gate, "query_compute_apps",
                               return_value=[
                                   {"pid": 58200,
                                    "process": "python.exe"},
                                   {"pid": 67848,
                                    "process": "llama-server.exe"},
                                   {"pid": 999,
                                    "process": "dwm.exe"}]):
            rc, out = self._run_main(["--json"])
        self.assertEqual(rc, 1)
        row = json.loads(out)
        att = row["attribution"]
        self.assertEqual([p["pid"] for p in att["producers"]],
                         [58200, 67848])
        self.assertEqual(att["other"], 1)
        self.assertEqual(att["raw"], 3)

    def test_go_json_has_no_attribution_face(self):
        # GO windows don't pay the extra probe (tech#79: NO-GO face only)
        with mock.patch.object(gate, "query_task_states",
                               return_value=self._clear_tasks()), \
             mock.patch.object(gate, "read_vram_free_mb",
                               return_value=11000), \
             mock.patch.object(gate, "query_compute_apps",
                               return_value=[{"pid": 1,
                                              "process": "python.exe"}]):
            rc, out = self._run_main(["--json"])
        self.assertEqual(rc, 0)
        self.assertNotIn("attribution", json.loads(out))

    def test_no_go_attribution_folds_tray_noise(self):
        # tech#80 CLI integration: tray shell never reaches producers
        with mock.patch.object(gate, "query_task_states",
                               return_value=self._clear_tasks()), \
             mock.patch.object(gate, "read_vram_free_mb",
                               return_value=100), \
             mock.patch.object(gate, "query_compute_apps",
                               return_value=[
                                   {"pid": 40564,
                                    "process": "unityvcstray.exe"},
                                   {"pid": 58200,
                                    "process": "python.exe"},
                                   {"pid": 999,
                                    "process": "dwm.exe"}]):
            rc, out = self._run_main(["--json"])
        self.assertEqual(rc, 1)
        row = json.loads(out)
        att = row["attribution"]
        self.assertEqual([p["pid"] for p in att["producers"]], [58200])
        self.assertEqual(att["other"], 2)
        self.assertEqual(att["raw"], 3)

    def test_no_go_unreadable_error_note(self):
        with mock.patch.object(gate, "query_task_states",
                               return_value=self._clear_tasks()), \
             mock.patch.object(gate, "read_vram_free_mb",
                               return_value=100), \
             mock.patch.object(gate, "query_compute_apps",
                               return_value=None):
            rc, out = self._run_main(["--json"])
        self.assertEqual(rc, 1)
        self.assertEqual(json.loads(out)["attribution"],
                         {"error": "compute-apps-unreadable"})

    def test_non_json_no_go_prints_attribution(self):
        with mock.patch.object(gate, "query_task_states",
                               return_value=self._clear_tasks()), \
             mock.patch.object(gate, "read_vram_free_mb",
                               return_value=100), \
             mock.patch.object(gate, "query_compute_apps",
                               return_value=[{"pid": 58200,
                                              "process": "python.exe"}]):
            rc, out = self._run_main([])
        self.assertEqual(rc, 1)
        self.assertIn("attribution=", out)
        self.assertIn("python.exe", out)


if __name__ == "__main__":
    unittest.main()
