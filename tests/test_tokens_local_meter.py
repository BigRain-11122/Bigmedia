# -*- coding: utf-8 -*-
"""Tests for src/os/tokens_local_meter.py (state/queue/tech#10)."""

import datetime
import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "os"))

import tokens_local_meter as tlm  # noqa: E402


EC_FIXTURE = "\ufeff# 专职专家调用台账（Expert Calls Ledger）\n" \
    "> 机制行级追加禁改写。\n" \
    "| 时间 | 专家 | 身份（部门） | 材料 | 退出 | 结论首行 |\n" \
    "|---|---|---|---|---|---|\n" \
    "| 2026-10-08 02:47 | S1-script | S1 编剧官（内容生产部） | m-v1.md | 0 | 总分：10 |\n" \
    "| 2026-10-09 07:17 | E4-audience | MD-0001 漫剧集 75.84s（wrapper） | 8.0（会看完+打 8 分明说） | expert-verdicts/x.md | 留存（参考仪·非拦截席） |\n" \
    "| 2026-09-24 22:43 | S1-script | S1 编剧官（内容生产部） | m.md | 3 | FAIL ollama timeout (300s)——无判词 |\n" \
    "| 2026-10-09 13:00 | S1-script | S1 编剧官（内容生产部） | m-v2.md | 0 | 总分：9 |\n"

SR_FIXTURE = "\ufeff# 环节评审台账\n" \
    "> 行级追加禁改写。\n" \
    "| 2026-10-08 | **S2 三门·BS-015** | 事实词核验 asr-check.srt | 读数 |\n" \
    "| 2026-10-09 | **E8 终审·MD-0001** | review 单+e4_call.py | 七席 ≥9 |\n" \
    "| 2026-10-09 | **S2 席 ASR 事实词核验·BS-014** | 终轨 12 cues·asr-check.srt 留档 | 9.0 |\n" \
    "普通文本行含 asr-check 但非台账行不算。\n"


class TestParseExpertCalls(unittest.TestCase):
    def test_rows_and_exit_tokens(self):
        rows = tlm.parse_expert_calls(EC_FIXTURE)
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0][0], datetime.datetime(2026, 10, 8, 2, 47))
        self.assertEqual(rows[0][1], "0")
        # E4 wrapper form: 6 cells with shifted meanings — the exit slot
        # holds the verdict file path (non-numeric → default produced).
        self.assertEqual(rows[1][1], "expert-verdicts/x.md")
        # Hand-added FAIL row keeps its numeric exit code.
        self.assertEqual(rows[2][1], "3")

    def test_is_produced_classification(self):
        self.assertTrue(tlm._is_produced("0"))
        self.assertFalse(tlm._is_produced("3"))
        self.assertTrue(tlm._is_produced("8.0（会看完明说）"))
        self.assertTrue(tlm._is_produced(""))  # unknown → assume produced


class TestStationAsrRows(unittest.TestCase):
    def test_asr_rows_date_level(self):
        rows = tlm.parse_station_asr(SR_FIXTURE)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], datetime.datetime(2026, 10, 8, 0, 0))


class TestMeterWindow(unittest.TestCase):
    def setUp(self):
        self.expert = tlm.parse_expert_calls(EC_FIXTURE)
        self.asr = tlm.parse_station_asr(SR_FIXTURE)

    def test_window_filters_and_classifies(self):
        since = datetime.datetime(2026, 10, 9, 0, 0)
        out = tlm.meter(self.expert, self.asr, since)
        # In-window expert rows: E4 verdict row + S1 ok row (FAIL row is
        # 09-24, out of window). In-window asr rows: one (10-09).
        self.assertEqual(out["ollama_produced"], 2)
        self.assertEqual(out["ollama_attempted_noproduct"], 0)
        self.assertEqual(out["whisper_rows"], 1)
        self.assertEqual(out["tokens_local"], 3)

    def test_wide_window_counts_fail_row_as_attempted(self):
        since = datetime.datetime(2026, 9, 1, 0, 0)
        out = tlm.meter(self.expert, self.asr, since)
        self.assertEqual(out["ollama_produced"], 3)
        self.assertEqual(out["ollama_attempted_noproduct"], 1)
        self.assertEqual(out["whisper_rows"], 2)
        self.assertEqual(out["tokens_local"], 5)

    def test_missing_files_read_as_empty(self):
        self.assertEqual(tlm.read_text(os.path.join("no", "such", "f.md")), "")


class TestBuildReadoutCli(unittest.TestCase):
    def test_build_readout_via_files(self):
        fd, path = tempfile.mkstemp(suffix=".md")
        os.close(fd)
        with io.open(path, "w", encoding="utf-8") as fh:
            fh.write(EC_FIXTURE)
        try:
            since = datetime.datetime(2026, 10, 9, 0, 0)
            out = tlm.build_readout(since, expert_path=path, station_path=path)
            # station parsing finds no dated asr rows in the EC fixture.
            self.assertEqual(out["ollama_produced"], 2)
            self.assertEqual(out["whisper_rows"], 0)
        finally:
            os.unlink(path)

    def test_main_since_json(self):
        out = tlm.main(["--since", "2026-09-01", "--json"])
        self.assertEqual(out, 0)


if __name__ == "__main__":
    unittest.main()
