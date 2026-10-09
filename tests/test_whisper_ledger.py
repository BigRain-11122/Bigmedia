# -*- coding: utf-8 -*-
"""Tests for the whisper exact-metering hook (state/queue/tech#19, R1830):

1. src/render/whisper_to_srt.py appends one JSONL ledger row per real
   run (success / failure / no-cues; NOT on audio-missing), honors
   --no-ledger and --purpose, and never lets a ledger write failure
   fail the run.
2. src/os/tokens_local_meter.py consumes the exact surface with
   precedence over the station-reviews approximation from the ledger
   epoch day onward (no double counting of a run that leaves both
   surfaces).
"""

import datetime
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src", "render"))
sys.path.insert(0, os.path.join(HERE, "..", "src", "os"))

import tokens_local_meter as tlm  # noqa: E402
import whisper_to_srt as w2s  # noqa: E402


def _read_rows(path):
    rows = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


class LedgerAppendBase(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="wsl_")
        self.audio = os.path.join(self.d, "a.mp3")
        with open(self.audio, "wb") as fh:
            fh.write(b"x" * 16)
        self.out = os.path.join(self.d, "a.srt")
        self.ledger = os.path.join(self.d, "ledger.jsonl")
        self._orig = w2s.transcribe_to_cues

    def tearDown(self):
        w2s.transcribe_to_cues = self._orig
        for f in os.listdir(self.d):
            os.unlink(os.path.join(self.d, f))
        os.rmdir(self.d)

    def _run(self, extra=None):
        argv = ["--audio", self.audio, "--out", self.out,
                "--ledger", self.ledger] + (extra or [])
        return w2s.main(argv)


class TestLedgerAppend(LedgerAppendBase):
    def test_success_row(self):
        w2s.transcribe_to_cues = (
            lambda *a, **k: ([(0.0, 1.2, "hi")], 0, 12.5))
        rc = self._run(["--purpose", "final-track-qc"])
        self.assertEqual(rc, 0)
        rows = _read_rows(self.ledger)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["rc"], 0)
        self.assertEqual(row["purpose"], "final-track-qc")
        self.assertEqual(row["model"], "small")
        self.assertEqual(row["cues"], 1)
        self.assertEqual(row["duration_s"], 12.5)
        self.assertTrue(row["ts"])

    def test_transcribe_failure_row(self):
        def boom(*a, **k):
            raise RuntimeError("model load")
        w2s.transcribe_to_cues = boom
        rc = self._run(["--purpose", "calibration"])
        self.assertEqual(rc, 2)
        rows = _read_rows(self.ledger)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["rc"], 2)
        self.assertIsNone(rows[0]["duration_s"])
        self.assertIsNone(rows[0]["cues"])
        self.assertEqual(rows[0]["purpose"], "calibration")

    def test_no_cues_row(self):
        w2s.transcribe_to_cues = lambda *a, **k: ([], 0, 3.0)
        rc = self._run([])
        self.assertEqual(rc, 2)
        rows = _read_rows(self.ledger)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["rc"], 2)
        self.assertEqual(rows[0]["cues"], 0)
        self.assertEqual(rows[0]["duration_s"], 3.0)
        self.assertEqual(rows[0]["purpose"], "untagged")

    def test_audio_missing_writes_no_row(self):
        rc = w2s.main(["--audio", os.path.join(self.d, "nope.mp3"),
                       "--out", self.out, "--ledger", self.ledger])
        self.assertEqual(rc, 2)
        self.assertFalse(os.path.exists(self.ledger))

    def test_no_ledger_flag_skips_append(self):
        w2s.transcribe_to_cues = (
            lambda *a, **k: ([(0.0, 1.0, "hi")], 0, 2.0))
        rc = w2s.main(["--audio", self.audio, "--out", self.out,
                      "--no-ledger", "--ledger", self.ledger])
        self.assertEqual(rc, 0)
        self.assertFalse(os.path.exists(self.ledger))


LEDGER_FIXTURE = "\n".join([
    json.dumps({"ts": "2026-10-09 07:00:00", "purpose": "final-track-qc",
               "model": "medium", "audio": "a.mp3", "rc": 0,
               "duration_s": 57.9, "cues": 12}),
    json.dumps({"ts": "2026-10-09 08:00:00", "purpose": "calibration",
               "model": "medium", "audio": "b.mp3", "rc": 2,
               "duration_s": None, "cues": None}),
    "not json at all",
    "",
])

SR_MIXED = "\ufeff# ledger\n" \
    "| 2026-10-08 | **S2** | asr-check | 9.0 |\n" \
    "| 2026-10-09 | **S2** | asr-check | 9.0 |\n" \
    "| 2026-10-10 | **S2** | asr-check | 9.0 |\n"


class TestMeterPrecedence(unittest.TestCase):
    def setUp(self):
        self.ledger = tlm.parse_whisper_ledger(LEDGER_FIXTURE)
        self.asr = tlm.parse_station_asr(SR_MIXED)

    def test_parse_ledger_rows_and_skip_malformed(self):
        self.assertEqual(len(self.ledger), 2)
        self.assertEqual(self.ledger[0][0],
                         datetime.datetime(2026, 10, 9, 7, 0))
        self.assertEqual(self.ledger[0][1], 0)
        self.assertEqual(self.ledger[1][1], 2)

    def test_epoch_day_double_count_guard(self):
        # epoch day = 10-09: station asr row of 10-09 dropped (exact
        # surface owns the day); pre-epoch 10-08 kept as approx;
        # post-epoch 10-10 station row also dropped.
        since = datetime.datetime(2026, 10, 1, 0, 0)
        out = tlm.meter([], self.asr, since, ledger_rows=self.ledger)
        self.assertEqual(out["whisper_apprx_rows"], 1)  # 10-08 only
        self.assertEqual(out["whisper_exact_produced"], 1)
        self.assertEqual(out["whisper_exact_attempted"], 1)
        self.assertEqual(out["whisper_rows"], 3)
        self.assertEqual(out["tokens_local"], 2)  # approx 1 + produced 1

    def test_window_filters_exact_rows(self):
        since = datetime.datetime(2026, 10, 9, 7, 30)
        out = tlm.meter([], self.asr, since, ledger_rows=self.ledger)
        # 07:00 ledger row and 10-08 approx row fall out of window.
        self.assertEqual(out["whisper_exact_produced"], 0)
        self.assertEqual(out["whisper_exact_attempted"], 1)
        self.assertEqual(out["whisper_apprx_rows"], 0)
        self.assertEqual(out["whisper_rows"], 1)
        self.assertEqual(out["tokens_local"], 0)

    def test_no_ledger_keeps_legacy_approx(self):
        since = datetime.datetime(2026, 10, 1, 0, 0)
        out = tlm.meter([], self.asr, since)  # ledger_rows=None
        self.assertEqual(out["whisper_rows"], 3)
        self.assertEqual(out["whisper_apprx_rows"], 3)
        self.assertEqual(out["whisper_exact_produced"], 0)
        self.assertEqual(out["tokens_local"], 3)


class TestBuildReadoutLedgerPath(unittest.TestCase):
    def test_build_readout_consumes_ledger(self):
        d = tempfile.mkdtemp(prefix="wsl_ro_")
        try:
            led = os.path.join(d, "l.jsonl")
            with open(led, "w", encoding="utf-8") as fh:
                fh.write(LEDGER_FIXTURE)
            sr = os.path.join(d, "sr.md")
            with open(sr, "w", encoding="utf-8") as fh:
                fh.write(SR_MIXED)
            since = datetime.datetime(2026, 10, 1, 0, 0)
            out = tlm.build_readout(since, expert_path=sr,
                                    station_path=sr, ledger_path=led)
            self.assertEqual(out["whisper_exact_produced"], 1)
            # SR rows carry no HH:MM time cell, so none parse as
            # expert-call rows: the ollama surface reads zero.
            self.assertEqual(out["ollama_produced"], 0)
        finally:
            for f in os.listdir(d):
                os.unlink(os.path.join(d, f))
            os.rmdir(d)


if __name__ == "__main__":
    unittest.main()
