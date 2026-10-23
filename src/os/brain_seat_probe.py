# -*- coding: utf-8 -*-
"""Brain seat probe (tech#378, R2429).

Why this exists: the :8090 review seat can be dead for days while every
scheduled watchdog reports success. `Tools/coder-serve.ps1` (bm-a, the
seat's supervisor, every 10 minutes) exits 0 at its own provisioning
guards when the llama.cpp build or the GGUF is missing, so "task ran,
LastTaskResult=0" and "the seat is alive" are indistinguishable from
the outside. M4 then sits unrunnable and nobody is told (R2427/R2428:
two consecutive rounds read GET /health as unreachable with no
provisioning evidence to act on).

This probe asks the seat, and when it is down it says WHY:

    python src/os/brain_seat_probe.py [--json] [--no-write]

- wire: one GET <brain-base>/health with a 2s cap (same cap and same
  base as src/call_expert.py, so "probe says up" and "call can fly"
  agree by construction).
- provisioning: the model / binary inputs the launcher needs, read
  from BRAIN_MODEL_PATH / BRAIN_EXE_PATH (defaults = bm-a's canon
  paths in coder-serve.ps1) -- a missing input is a human-action
  finding, not a retry candidate.
- pause: the CEO machine-let flag (BRAIN_PAUSE_FLAG). A paused seat is
  a legitimate down (the launcher must not revive it), so it is
  reported as its own reason instead of an alarm.

Every run appends one JSONL row to
data/pipeline/brain-seat-probe.jsonl: a multi-day death becomes a
readable series instead of a memory. Readiness reads the latest row
(readiness.parse_seat_probe) and names the seat in its findings, which
is the "nobody told" half of tech#378.

Exit codes: 0 seat alive; 2 seat down.

ASCII rule: this source is pure ASCII.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROBE_LEDGER = REPO / "data" / "pipeline" / "brain-seat-probe.jsonl"

# Same env contract as src/call_expert.py (one line per machine in the
# fleet canon); the health URL derives from the same base so the two
# faces cannot drift apart.
BRAIN_URL = os.environ.get(
    "BRAIN_URL", "http://127.0.0.1:8090/v1/chat/completions")
BRAIN_HEALTH_URL = BRAIN_URL.split("/v1/")[0].rstrip("/") + "/health"
LIVENESS_CAP_S = 2

# bm-a canon (Tools/coder-serve.ps1): the resident 35B seat's inputs.
# Env overrides exist because the paths are machine facts, not law.
DEFAULT_MODEL_PATH = (r"C:\Users\sjs20\models\qwen36-35b"
                      r"\Qwen3.6-35B-A3B-UD-IQ4_XS.gguf")
DEFAULT_EXE_PATH = (r"C:\Users\sjs20\models\llamacpp-b11429"
                    r"\llama-server.exe")
DEFAULT_PAUSE_FLAG = (r"C:\Users\sjs20\Desktop\FluxGroup\.codely-cli"
                      r"\engine-tick\keepwarm.pause")

MODEL_PATH = os.environ.get("BRAIN_MODEL_PATH", DEFAULT_MODEL_PATH)
EXE_PATH = os.environ.get("BRAIN_EXE_PATH", DEFAULT_EXE_PATH)
PAUSE_FLAG = os.environ.get("BRAIN_PAUSE_FLAG", DEFAULT_PAUSE_FLAG)

REASON_ALIVE = "alive"
REASON_PAUSED = "paused (CEO machine-let flag; launcher must not revive)"
REASON_HEALTH = "health unreachable"
REASON_PROVISION = "provisioning inputs missing"


def health_ok(url=BRAIN_HEALTH_URL, cap_s=LIVENESS_CAP_S):
    """True when the seat answers /health inside the cap. Never raises."""
    try:
        with urllib.request.urlopen(url, timeout=cap_s) as resp:
            resp.read()
        return True
    except Exception:
        return False


def missing_inputs(pairs=None):
    """Names of provisioning inputs that are absent (pure).

    pairs = [(name, path), ...]; None resolves the module defaults at
    call time so env changes and tests both see fresh values."""
    if pairs is None:
        pairs = [("model", MODEL_PATH), ("exe", EXE_PATH)]
    return [name for name, path in pairs if not Path(path).is_file()]


def pause_active(path=None):
    """True when the CEO machine-let flag blocks seat revival."""
    return Path(path if path is not None else PAUSE_FLAG).exists()


def classify(alive, missing, paused):
    """Pure: (alive, missing inputs, paused) -> one human reason string.

    Order matters: liveness answers first (a live seat needs no
    excuse); then provisioning (the actionable half); then pause (a
    legitimate down)."""
    if alive:
        return REASON_ALIVE
    if missing:
        return "%s: %s" % (REASON_PROVISION, ", ".join(missing))
    if paused:
        return REASON_PAUSED
    return REASON_HEALTH


def probe_row(alive, reason, ts=None, health_url=BRAIN_HEALTH_URL,
              missing=(), paused=False):
    """Pure: one JSONL row for this probe run."""
    stamp = ts or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return json.dumps({
        "ts": stamp,
        "alive": bool(alive),
        "reason": reason,
        "health_url": health_url,
        "missing": list(missing),
        "paused": bool(paused),
    }, ensure_ascii=False)


def append_row(row, path=None):
    """Best-effort JSONL append; a write failure never changes the
    probe's exit code (same law as the other pipeline ledgers)."""
    try:
        target = Path(path) if path is not None else PROBE_LEDGER
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as f:
            f.write(row + "\n")
        return True
    except OSError:
        return False


def latest_row(path=None):
    """Last parsable row of the probe ledger, or None (pure read)."""
    p = Path(path) if path is not None else PROBE_LEDGER
    if not p.is_file():
        return None
    last = None
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if isinstance(row, dict) and "alive" in row:
            last = row
    return last


def main(argv):
    as_json = no_write = False
    for arg in argv[1:]:
        if arg == "--json":
            as_json = True
        elif arg == "--no-write":
            no_write = True
        else:
            print("usage: python src/os/brain_seat_probe.py [--json] [--no-write]")
            return 2
    alive = health_ok()
    missing = missing_inputs()
    paused = pause_active()
    reason = classify(alive, missing, paused)
    row = probe_row(alive, reason, missing=missing, paused=paused)
    if not no_write:
        if not append_row(row):
            print("WARN probe ledger append failed (exit kept)")
    if as_json:
        print(row)
    else:
        print("brain-seat: %s -> %s" % ("UP" if alive else "DOWN", reason))
        print("health: %s (%ds cap)" % (BRAIN_HEALTH_URL, LIVENESS_CAP_S))
        if paused:
            print("pause flag: %s" % PAUSE_FLAG)
    return 0 if alive else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))