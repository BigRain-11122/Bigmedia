#!/usr/bin/env python3
"""Canonical status-export writer (tech#70, R1904).

R1901 defect family root cause: export refresh had no single-truth
writer - every round's close hand-rolled an ad-hoc script to write
docs/status-export.json (r1876_export / r1902_close generations in
the case log), each with its own export_ts source. That is the
breeding ground for the R1901 estimated-value defect (19:05:00
stamped into a file written at 18:49:42). The tech#68/#69 guard faces
only test - they do not treat.

This module IS the writer. Laws encoded:
- live-clock law: export_ts is ALWAYS datetime.now() stamped inside
  the writer (injectable clock for tests); callers can neither supply
  nor predict it. A patch carrying "export_ts" is a loud usage error.
- pre-write contract self-check: the merged payload runs through
  loop_health.classify_export_face - the SAME v6.2 contract the
  routine probe enforces - BEFORE any disk write. Any violation ->
  rc=2 and the export file is left byte-identical (never write a bad
  export: the CEO board silently falls back to the curated face on
  bad fields, which is how the ~1700-round drift stayed invisible).
- incremental law: callers pass a partial patch (a subset of the
  known keys); unlisted keys carry over from the existing export. A
  missing export starts from {} - the patch must then satisfy the
  contract on its own (fresh-creation path).
- atomic write: temp file in the same dir + os.replace; UTF-8 no
  BOM; indent=1 to match the v6.2 shaper conventions.
- close adoption: round close scripts call this writer (CLI or
  refresh_export()) instead of hand-rolled JSON dumps - the ad-hoc
  generation (r1876_export / r1902_close type) is retired.

Known keys (patch whitelist): do / depts / outs / chips / results /
live. Unknown keys are loud usage errors - a typo'd field name must
never silently no-op in a canonical writer.

CLI:
    python src/os/export_refresh.py --patch FILE.json [options]
    python src/os/export_refresh.py --do "one line" [options]

rc: 0 = written (or dry-run ok); 1 = IO/OS failure at write time;
2 = refusal - contract violations in the merged payload, bad patch,
or usage error. On rc=2 the export file is never modified.
"""

import argparse
import datetime
import json
import os
import sys

# repo-relative default target (same as loop_health.EXPORT_REL)
DEFAULT_EXPORT_REL = os.path.join("docs", "status-export.json")

# patch whitelist - the export's full top-level schema minus the
# writer-owned export_ts
KNOWN_KEYS = ("do", "depts", "outs", "chips", "results", "live")

RC_OK = 0
RC_IO = 1
RC_REFUSE = 2


def _stamp(now):
    """Live-clock stamp helper (kept trivial for injectability)."""
    return now.strftime("%Y-%m-%d %H:%M:%S")


def load_export(path):
    """Read the existing export. Returns (dict, err).

    A missing file is NOT an error: ({} , "") - the fresh-creation
    path starts from an empty base and the patch must carry the
    contract on its own. Unparseable JSON is a refusal-grade error
    surfaced as err (the caller refuses rather than clobber a file
    it cannot understand).
    """
    if not os.path.isfile(path):
        return {}, ""
    try:
        with open(path, "r", encoding="utf-8-sig", errors="replace") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        return None, str(exc)
    if not isinstance(data, dict):
        return None, "top level is %s, want an object" % type(data).__name__
    return data, ""


def parse_patch(patch):
    """Validate the caller-supplied patch. Returns (dict, err)."""
    if not isinstance(patch, dict):
        return None, ("patch top level is %s, want a JSON object"
                      % type(patch).__name__)
    if "export_ts" in patch:
        return None, "export_ts is writer-owned (live clock stamps it)"
    bad_keys = [k for k in patch if k not in KNOWN_KEYS]
    if bad_keys:
        return None, ("unknown patch key(s) %s - whitelist: %s"
                      % (", ".join(sorted(bad_keys)),
                         ", ".join(KNOWN_KEYS)))
    return patch, ""


def merge_payload(base, patch, do_override, now):
    """Assemble the merged payload dict (pure). Returns dict.

    Unlisted keys carry over from base; export_ts is always stamped
    here from the live clock. The do_override convenience wins over
    a patch-supplied do.
    """
    merged = dict(base)
    merged.update(patch)
    if do_override is not None:
        merged["do"] = do_override
    merged["export_ts"] = _stamp(now)
    return merged


def _classify(merged, now):
    """Run the probe-grade contract self-check against the exact stamp
    clock (a fresh ts can never read as future). Lazy import keeps CLI
    startup light and avoids a circular import at module load."""
    import loop_health
    return loop_health.classify_export_face(merged, parse_err="",
                                            now=now, mtime=None)


def _atomic_write(path, text):
    """UTF-8 no-BOM write via temp + os.replace. Returns (rc, err)."""
    tmp = path + ".tmp-export-refresh"
    try:
        with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except OSError as exc:
        try:
            if os.path.exists(tmp):
                os.unlink(tmp)
        except OSError:
            pass
        return RC_IO, str(exc)
    return RC_OK, ""


def refresh_export(export_path, patch=None, do=None,
                   now_fn=datetime.datetime.now, dry_run=False):
    """Single-truth export refresh. Returns (rc, lines, violations).

    lines: ASCII evidence log (never Chinese - encoding rule).
    violations: the contract findings list on refusal (empty on ok).
    """
    lines = []
    base, err = load_export(export_path)
    if err:
        lines.append("REFUSE existing export unreadable: %.80s" % err)
        return RC_REFUSE, lines, []
    if patch is not None:
        patch, err = parse_patch(patch)
        if err:
            lines.append("REFUSE bad patch: %.80s" % err)
            return RC_REFUSE, lines, []
    if patch is None and do is None:
        lines.append("REFUSE nothing to update - pass --patch and/or --do")
        return RC_REFUSE, lines, []

    now = now_fn()
    merged = merge_payload(base, patch or {}, do, now)
    violations = _classify(merged, now)

    if violations:
        lines.append("REFUSE %d contract violation(s) - export NOT written:"
                     % len(violations))
        for sev, code, msg in violations:
            lines.append("  %s [%s] %.120s" % (sev, code, msg))
        return RC_REFUSE, lines, violations

    text = json.dumps(merged, ensure_ascii=False, indent=1) + "\n"
    if dry_run:
        lines.append("DRY-RUN contract clean, would write %d bytes to %s"
                     % (len(text.encode("utf-8")), export_path))
        return RC_OK, lines, []

    rc, err = _atomic_write(export_path, text)
    if rc != RC_OK:
        lines.append("IO-FAIL write: %.80s" % err)
        return RC_IO, lines, []
    lines.append("WROTE %s export_ts=%s" % (export_path, merged["export_ts"]))
    return RC_OK, lines, violations


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Canonical status-export writer (tech#70). "
                    "Refuses (rc=2) to write any payload the routine "
                    "probe would flag; export file is never modified "
                    "on refusal.")
    ap.add_argument("--patch", default=None,
                    help="JSON object file with a subset of %s"
                    % "/".join(KNOWN_KEYS))
    ap.add_argument("--do", default=None,
                    help='convenience: update the "do" one-liner')
    ap.add_argument("--export", default=None,
                    help="export path (default: %s)" % DEFAULT_EXPORT_REL)
    ap.add_argument("--dry-run", action="store_true",
                    help="run the self-check, write nothing")
    args = ap.parse_args(argv)

    root = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "..", ".."))
    export_path = args.export or os.path.join(root, DEFAULT_EXPORT_REL)

    patch = None
    if args.patch:
        try:
            with open(args.patch, "r", encoding="utf-8-sig",
                      errors="replace") as fh:
                patch = json.load(fh)
        except (OSError, ValueError) as exc:
            print("REFUSE patch file unreadable: %.80s" % exc)
            return RC_REFUSE

    rc, lines, _viol = refresh_export(export_path, patch=patch, do=args.do,
                                      dry_run=args.dry_run)
    for line in lines:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
