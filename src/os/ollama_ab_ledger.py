# -*- coding: utf-8 -*-
"""Direct-call ollama A/B probe ledger (tech#119; tech#52 craft reuse).

Gap anchor (R2011): the ad-hoc A/B probe family (r1877 / r1880 / r1956
type scripts, each written fresh under .c3-tmp) invokes ``ollama run`` /
the OpenAI-compatible endpoint directly - no expert-calls row, so
tokens_local_meter structurally cannot see those calls. That blind spot
was the main mass behind the meter-vs-manual-note divergence family
(10-02 +59 / 09-25 +34 / 10-11 +6 readouts, tech#24).

Convention (the manual state.json line stays the single truth - tech#24
caliber; this ledger only makes the direct-call face machine-readable):

    from ollama_ab_ledger import append_ab_row
    proc = subprocess.run([...])          # direct ollama call
    append_ab_row(purpose="prefilter-ab", model="qwen2.5:14b-8k",
                  rc=proc.returncode, n=idx)

One JSONL row per direct call: ts / purpose / model / rc (+ n, note when
provided). Best-effort: any write failure WARNs to stderr and never
raises - metering must never break the probe it measures. Pure file
append; zero model calls, zero tokens.
"""

from __future__ import unicode_literals

import datetime
import io
import json
import os
import sys

REPO = __file__.replace("\\", "/").rsplit("/src/os/", 1)[0]
DEFAULT_LEDGER_PATH = REPO + "/data/pipeline/ollama-ab-ledger.jsonl"


def append_ab_row(purpose, model, rc, n=None, note=None,
                  path=DEFAULT_LEDGER_PATH, when=None):
    """Append one best-effort JSONL row for a direct ollama A/B call.

    Returns True on write, False on failure (WARN only, never raises;
    parent directories are auto-created). ``when`` is an injectable
    clock for tests; ``n`` is the call index within the A/B batch and
    ``note`` free-form context - both omitted from the row when None.
    """
    row = {
        "ts": (when or datetime.datetime.now()).strftime(
            "%Y-%m-%d %H:%M:%S"),
        "purpose": str(purpose),
        "model": str(model),
        "rc": rc,
    }
    if n is not None:
        row["n"] = n
    if note is not None:
        row["note"] = str(note)
    try:
        parent = os.path.dirname(path)
        if parent and not os.path.isdir(parent):
            os.makedirs(parent)
        with io.open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")
        return True
    except OSError as exc:
        sys.stderr.write("WARN ab-ledger append failed: %s\n" % exc)
        return False
