"""Unit tests for the canonical export writer (src/os/export_refresh.py).

tech#70 judgment criteria encoded: the writer REFUSES (rc=2, export file
byte-identical) any payload the routine probe would flag - the
R1901/R1902 anchor forms are replayed as refusal fixtures - and the
live-clock stamp law kills the R1901 estimated-ts defect at the source
(export_ts comes from the injected clock inside the writer, never from
the caller; a patch carrying it is a loud refusal).

Runtime-made trees are pure ASCII per the encoding rule; one smoke case
exercises the real repo export read-only (temp copy, real file never
touched by tests).

Run:
    python tests/test_export_refresh.py
"""
import json
import shutil
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "src" / "os"))

import export_refresh  # noqa: E402

FIXED_NOW = datetime(2026, 10, 10, 20, 15, 0)
FIXED_STAMP = "2026-10-10 20:15:00"


def fixed_now():
    return FIXED_NOW


def clean_body():
    """Minimal contract-clean export body (export_ts is writer-owned)."""
    return {
        "do": "one line current activity",
        "outs": [["kept item", "on", "tag"]],
        "chips": [["kept chip", "live"]],
        "results": [["42", "kept readout"]],
        "live": ["live a", "live b", "live c"],
    }


class WriterTmpCase(unittest.TestCase):
    """tmp dir + helpers shared by all writer cases."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="export-refresh-")
        self.dir = Path(self._tmp.name)
        self.export = self.dir / "status-export.json"

    def tearDown(self):
        self._tmp.cleanup()

    def write_base(self, body=None):
        body = clean_body() if body is None else body
        self.export.write_text(
            json.dumps(body, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8")

    def refresh(self, patch=None, do=None, dry_run=False,
                export_path=None):
        return export_refresh.refresh_export(
            str(export_path or self.export), patch=patch, do=do,
            now_fn=fixed_now, dry_run=dry_run)

    def read_back(self):
        return json.loads(self.export.read_text(encoding="utf-8"))


class MergeLawTests(WriterTmpCase):
    """Incremental law: unlisted keys carry over; do convenience; the
    writer-owned / unknown-key refusals."""

    def test_partial_patch_carries_over_unlisted_keys(self):
        self.write_base()
        rc, lines, viol = self.refresh(patch={"do": "new one line"})
        self.assertEqual(rc, 0, lines)
        self.assertEqual(viol, [])
        data = self.read_back()
        self.assertEqual(data["do"], "new one line")
        self.assertEqual(data["outs"], [["kept item", "on", "tag"]])
        self.assertEqual(data["chips"], [["kept chip", "live"]])
        self.assertEqual(data["results"], [["42", "kept readout"]])
        self.assertEqual(data["live"], ["live a", "live b", "live c"])
        self.assertEqual(data["export_ts"], FIXED_STAMP)

    def test_do_convenience_updates_only_do(self):
        self.write_base()
        rc, lines, _ = self.refresh(do="solo do update")
        self.assertEqual(rc, 0, lines)
        data = self.read_back()
        self.assertEqual(data["do"], "solo do update")
        self.assertEqual(data["outs"], [["kept item", "on", "tag"]])

    def test_export_ts_is_writer_owned(self):
        self.write_base()
        before = self.export.read_bytes()
        rc, lines, _ = self.refresh(patch={"export_ts": "1999-01-01 00:00:00"})
        self.assertEqual(rc, 2, lines)
        self.assertTrue(any("writer-owned" in l for l in lines), lines)
        self.assertEqual(self.export.read_bytes(), before)

    def test_unknown_patch_key_refused(self):
        self.write_base()
        before = self.export.read_bytes()
        rc, lines, _ = self.refresh(patch={"typo_key": 1})
        self.assertEqual(rc, 2, lines)
        self.assertTrue(any("unknown patch key" in l for l in lines), lines)
        self.assertEqual(self.export.read_bytes(), before)

    def test_non_object_patch_refused(self):
        self.write_base()
        rc, lines, _ = self.refresh(patch=["not", "an", "object"])
        self.assertEqual(rc, 2, lines)
        self.assertTrue(any("want a JSON object" in l for l in lines), lines)

    def test_nothing_to_update_refused(self):
        self.write_base()
        rc, lines, _ = self.refresh()
        self.assertEqual(rc, 2, lines)
        self.assertTrue(any("nothing to update" in l for l in lines), lines)


class RefusalTests(WriterTmpCase):
    """The R1901/R1902 anchor forms replayed: every probe-flaggable
    payload must be refused BEFORE any disk write (file byte-identical)."""

    def test_refuse_do_over_budget(self):
        self.write_base()
        before = self.export.read_bytes()
        rc, lines, viol = self.refresh(patch={"do": "x" * 121})
        self.assertEqual(rc, 2, lines)
        codes = [v[1] for v in viol]
        self.assertIn("export-do", codes)
        self.assertEqual(self.export.read_bytes(), before)

    def test_refuse_outs_bare_strings(self):
        # R1901 anchor: 39/39 bare-string outs entries
        self.write_base()
        before = self.export.read_bytes()
        rc, lines, viol = self.refresh(
            patch={"outs": ["bare a", "bare b"]})
        self.assertEqual(rc, 2, lines)
        self.assertIn("export-outs", [v[1] for v in viol])
        self.assertEqual(self.export.read_bytes(), before)

    def test_refuse_results_log_line_pairs(self):
        # R1901 anchor: [tick, full log line] long-key pairs
        self.write_base()
        before = self.export.read_bytes()
        rc, lines, viol = self.refresh(
            patch={"results": [["1901", "full log line " * 10]]})
        self.assertEqual(rc, 2, lines)
        self.assertIn("export-results", [v[1] for v in viol])
        self.assertEqual(self.export.read_bytes(), before)

    def test_refuse_bad_chips_shape(self):
        # tech#71 parity facet: malformed chips cells (the same
        # classify_export_face the probe runs - one source, both
        # faces)
        self.write_base()
        before = self.export.read_bytes()
        rc, lines, viol = self.refresh(patch={
            "chips": [["ok", "done"],        # class off-enum
                      ["t" * 15, "live"],   # txt over cap
                      "bare string"]})      # not a list
        self.assertEqual(rc, 2, lines)
        self.assertIn("export-chips", [v[1] for v in viol])
        self.assertEqual(self.export.read_bytes(), before)

    def test_refuse_bad_depts_shape(self):
        # tech#71 parity facet: depts entries the shaper would drop
        # or silently relabel
        self.write_base()
        before = self.export.read_bytes()
        rc, lines, viol = self.refresh(patch={
            "depts": [{"n": "dept name", "t": "text", "s": 7},
                      {"t": "missing name"},
                      "bare string"]})
        self.assertEqual(rc, 2, lines)
        self.assertIn("export-depts", [v[1] for v in viol])
        self.assertEqual(self.export.read_bytes(), before)

    def test_refuse_caps_over(self):
        # R1902 caps face: 13 well-formed outs > cap 12
        self.write_base()
        before = self.export.read_bytes()
        outs = [["item %d" % i, "on", "tag"] for i in range(13)]
        rc, lines, viol = self.refresh(patch={"outs": outs})
        self.assertEqual(rc, 2, lines)
        self.assertIn("export-caps", [v[1] for v in viol])
        self.assertEqual(self.export.read_bytes(), before)

    def test_refuse_fresh_export_without_do(self):
        # no base file: the patch alone must satisfy the contract
        rc, lines, viol = self.refresh(patch={"outs": []})
        self.assertEqual(rc, 2, lines)
        self.assertIn("export-do", [v[1] for v in viol])
        self.assertFalse(self.export.exists(),
                         "refusal must not create a malformed export")

    def test_fresh_export_full_patch_creates(self):
        rc, lines, viol = self.refresh(patch=clean_body())
        self.assertEqual(rc, 0, lines)
        self.assertEqual(viol, [])
        data = self.read_back()
        self.assertEqual(data["export_ts"], FIXED_STAMP)
        self.assertEqual(data["do"], "one line current activity")

    def test_refuse_unparseable_existing(self):
        self.export.write_text("{not json", encoding="utf-8")
        rc, lines, _ = self.refresh(do="any")
        self.assertEqual(rc, 2, lines)
        self.assertTrue(any("unreadable" in l for l in lines), lines)


class WriteLawTests(WriterTmpCase):
    """The good path: live-clock stamp, UTF-8 no BOM, indent=1 v6.2
    shape, atomic replace, dry-run, CJK round-trip."""

    def test_write_stamps_injected_live_clock(self):
        self.write_base()
        rc, lines, _ = self.refresh(do="clock check")
        self.assertEqual(rc, 0, lines)
        self.assertEqual(self.read_back()["export_ts"], FIXED_STAMP)

    def test_no_bom_and_cjk_round_trip(self):
        rc, lines, _ = self.refresh(
            patch={"do": "量产开闸运转一行", "outs": [["中文条目", "on", "标签"]],
                   "chips": [["芯片", "live"]],
                   "results": [["168", "成品库"]],
                   "live": ["行一", "行二", "行三"]})
        self.assertEqual(rc, 0, lines)
        raw = self.export.read_bytes()
        self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))
        data = json.loads(raw.decode("utf-8"))
        self.assertEqual(data["do"], "量产开闸运转一行")
        self.assertEqual(data["outs"], [["中文条目", "on", "标签"]])

    def test_indent_one_v62_shape(self):
        self.write_base()
        self.refresh(do="shape check")
        head = self.export.read_text(encoding="utf-8")[:40]
        self.assertTrue(head.startswith('{\n "'), head)

    def test_atomic_no_temp_leftover(self):
        self.write_base()
        self.refresh(do="atomic check")
        leftovers = [p.name for p in self.dir.iterdir()
                     if "tmp-export-refresh" in p.name]
        self.assertEqual(leftovers, [])

    def test_dry_run_writes_nothing_fresh(self):
        rc, lines, _ = self.refresh(patch=clean_body(), dry_run=True)
        self.assertEqual(rc, 0, lines)
        self.assertFalse(self.export.exists())

    def test_dry_run_leaves_existing_untouched(self):
        self.write_base()
        before = self.export.read_bytes()
        rc, lines, _ = self.refresh(do="dry", dry_run=True)
        self.assertEqual(rc, 0, lines)
        self.assertEqual(self.export.read_bytes(), before)


class RealRepoSmokeTests(unittest.TestCase):
    """Read-only against the live repo export: the real current shape
    must pass the writer's pre-write self-check (temp copy only; the
    real file is never written by tests)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="export-real-")
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_real_export_shape_passes_writer_self_check(self):
        real = REPO / "docs" / "status-export.json"
        if not real.is_file():
            self.skipTest("real export absent")
        copy = self.dir / "status-export.json"
        shutil.copy2(real, copy)
        rc, lines, viol = export_refresh.refresh_export(
            str(copy), patch={"do": "smoke one line"}, now_fn=fixed_now)
        self.assertEqual(rc, 0, lines)
        self.assertEqual(viol, [], lines)
        data = json.loads(copy.read_text(encoding="utf-8"))
        # depts/live carried over intact from the real export
        self.assertIn("depts", data)
        self.assertIn("live", data)
        self.assertEqual(data["export_ts"], FIXED_STAMP)


if __name__ == "__main__":
    unittest.main(verbosity=2)
