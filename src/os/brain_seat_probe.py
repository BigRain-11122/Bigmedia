# -*- coding: utf-8 -*-
"""Brain seat probe (tech#378, R2429).

Why this exists: the :8091 review seat can be dead for days while every
scheduled watchdog reports success. `Tools/coder-serve.ps1` (bm-a, the
seat's supervisor, every 10 minutes) exits 0 at its own provisioning
guards when the llama.cpp build or the GGUF is missing, so "task ran,
LastTaskResult=0" and "the seat is alive" are indistinguishable from
the outside. M4 then sits unrunnable and nobody is told (R2427/R2428:
two consecutive rounds read GET /health as unreachable with no
provisioning evidence to act on).

D-20261024-01 (R2431): the seat was regenerated on port :8091 with the
official Qwen3.5-35B-A3B GGUF (Q4_K_M~Q5_K_M), and that ruling calls a
scheduler task that reports success while the disk holds no model a
FAKE-GREEN. So the probe now (a) resolves the model by official quant
pattern instead of one hardcoded community-variant filename, and
(b) reads the supervisor task's last result and names FAKE-GREEN when
it claims success with missing inputs.

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
import csv
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
    "BRAIN_URL", "http://127.0.0.1:8091/v1/chat/completions")
BRAIN_HEALTH_URL = BRAIN_URL.split("/v1/")[0].rstrip("/") + "/health"
LIVENESS_CAP_S = 2

# bm-a canon: the resident 35B seat's inputs. Env overrides exist
# because the paths are machine facts, not law. The model is resolved
# by official quant pattern (D-20261024-01 bans community variants), so
# a fresh download lands without a code edit.
MODEL_DIRS = [
    Path(r"C:\Users\sjs20\models\qwen35-35b-a3b"),
    Path(r"C:\Users\sjs20\models\qwen36-35b"),
    Path(r"C:\Users\sjs20\models"),
]
MODEL_GLOBS = ("*Qwen3*35B*A3B*Q4_K_M.gguf", "*Qwen3*35B*A3B*Q5_K_M.gguf")
DEFAULT_EXE_PATH = (r"C:\Users\sjs20\models\llamacpp-b11429"
                    r"\llama-server.exe")
DEFAULT_PAUSE_FLAG = (r"C:\Users\sjs20\Desktop\FluxGroup\.codely-cli"
                      r"\engine-tick\keepwarm.pause")
EXE_PATH = os.environ.get("BRAIN_EXE_PATH", DEFAULT_EXE_PATH)
PAUSE_FLAG = os.environ.get("BRAIN_PAUSE_FLAG", DEFAULT_PAUSE_FLAG)
SUPERVISOR_TASK = os.environ.get("BRAIN_TASK_NAME", "bm-a-CoderServe")

REASON_ALIVE = "alive"
REASON_PAUSED = "paused (CEO machine-let flag; launcher must not revive)"
REASON_HEALTH = "health unreachable"
REASON_PROVISION = "provisioning inputs missing"
REASON_FAKE_GREEN = ("FAKE-GREEN: supervisor task reported success "
                     "(LastTaskResult=0) but the seat has no inputs")


def resolve_model(dirs=None, globs=None, override=None):
    """Path of the resident model, or the explicit env override.

    Pure read of the disk. Returns a Path even when absent (the
    not-found entry keeps the missing-inputs message readable)."""
    if override is None:
        override = os.environ.get("BRAIN_MODEL_PATH")
    if override:
        return Path(override)
    for folder in (dirs if dirs is not None else MODEL_DIRS):
        for pattern in (globs if globs is not None else MODEL_GLOBS):
            try:
                hits = sorted(Path(folder).glob(pattern))
            except OSError:
                hits = []
            if hits:
                return hits[0]
    return Path(dirs[0] if dirs else MODEL_DIRS[0]) / "Qwen3.5-35B-A3B-Q4_K_M.gguf"


MODEL_PATH = resolve_model()


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


def _decode_console(data):
    """Console bytes -> text, trying UTF-8 then the ANSI codepage."""
    for enc in ("utf-8", "mbcs", "gbk"):
        try:
            return data.decode(enc)
        except (LookupError, UnicodeDecodeError):
            continue
    return data.decode("utf-8", "replace")


def parse_task_result(csv_text):
    """Last result code from `schtasks /Query /V /FO CSV`, or None.

    Locale-proof by header matching (the label is localized on a zh-CN
    box). Returns None when the column is absent or unparsable, so an
    unknown never becomes an alarm."""
    lines = [ln for ln in (csv_text or "").splitlines() if ln.strip()]
    if len(lines) < 2:
        return None
    try:
        header = next(csv.reader([lines[0]]))
        row = next(csv.reader([lines[1]]))
    except (csv.Error, StopIteration):
        return None
    idx = None
    for i, name in enumerate(header):
        low = name.strip().lower()
        if "result" in low or "结果" in low:
            idx = i
            break
    if idx is None or idx >= len(row):
        return None
    raw = row[idx].strip()
    if not raw:
        return None
    low = raw.lower()
    if low.startswith("0x"):
        try:
            return int(low, 16)
        except ValueError:
            return None
    try:
        return int(raw, 0)
    except ValueError:
        pass
    if "成功" in raw or "success" in low:
        return 0
    return None


def supervisor_last_result(task=None, runner=None):
    """Last result code of the supervisor task, or None when unknown.

    `runner(cmd) -> bytes` is injectable for tests. The live call runs
    schtasks with CREATE_NO_WINDOW so a probe never flashes a console
    on the CEO desktop (zero-window law)."""
    name = task if task is not None else SUPERVISOR_TASK
    cmd = ["schtasks", "/Query", "/TN", name, "/FO", "CSV", "/V"]
    try:
        if runner is not None:
            return parse_task_result(_decode_console(runner(cmd) or b""))
        import subprocess
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        out = subprocess.run(cmd, capture_output=True, timeout=10,
                             creationflags=flags)
        if out.returncode != 0:
            return None
        return parse_task_result(_decode_console(out.stdout))
    except Exception:
        return None


def classify(alive, missing, paused, fake_green=False):
    """Pure: (alive, missing inputs, paused, fake-green) -> one reason.

    Order matters: liveness answers first (a live seat needs no
    excuse); then fake-green (a success-looking supervisor over an
    empty disk is the loudest fault); then provisioning; then pause."""
    if alive:
        return REASON_ALIVE
    if fake_green and missing:
        return "%s: %s" % (REASON_FAKE_GREEN, ", ".join(missing))
    if missing:
        return "%s: %s" % (REASON_PROVISION, ", ".join(missing))
    if paused:
        return REASON_PAUSED
    return REASON_HEALTH


def probe_row(alive, reason, ts=None, health_url=BRAIN_HEALTH_URL,
              missing=(), paused=False, fake_green=False,
              task_result=None):
    """Pure: one JSONL row for this probe run."""
    stamp = ts or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return json.dumps({
        "ts": stamp,
        "alive": bool(alive),
        "reason": reason,
        "health_url": health_url,
        "missing": list(missing),
        "paused": bool(paused),
        "fake_green": bool(fake_green),
        "task_result": task_result,
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
    task_result = None if alive else supervisor_last_result()
    fake_green = bool(task_result == 0 and missing)
    reason = classify(alive, missing, paused, fake_green)
    row = probe_row(alive, reason, missing=missing, paused=paused,
                    fake_green=fake_green, task_result=task_result)
    if not no_write:
        if not append_row(row):
            print("WARN probe ledger append failed (exit kept)")
    if as_json:
        print(row)
    else:
        print("brain-seat: %s -> %s" % ("UP" if alive else "DOWN", reason))
        print("health: %s (%ds cap)" % (BRAIN_HEALTH_URL, LIVENESS_CAP_S))
        print("model: %s" % MODEL_PATH)
        print("supervisor task: %s last-result %s"
              % (SUPERVISOR_TASK,
                 "unknown" if task_result is None else task_result))
        if paused:
            print("pause flag: %s" % PAUSE_FLAG)
    return 0 if alive else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))