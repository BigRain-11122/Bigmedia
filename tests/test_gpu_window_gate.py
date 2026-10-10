"""Tests for src/os/gpu_window_gate.py (tech#57)."""

import contextlib
import importlib.util
import io
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
                               return_value=11000):
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
             mock.patch.object(gate, "read_vram_free_mb", return_value=None):
            rc, out = self._run_main(["--json"])
        self.assertEqual(rc, 2)
        self.assertIn("null", out)


if __name__ == "__main__":
    unittest.main()
