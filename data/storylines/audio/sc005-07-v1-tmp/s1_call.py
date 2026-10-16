#!/usr/bin/env python3
"""SC-005-07 S1 staged launcher (fire-window turnkey, R2008 prestage).

Pre-staged per the R1995/R1999 double window-loss gate: fire_consume.py
dispatches THIS file the moment the card says fire, so no material
discovery or command assembly ever happens inside the 120s TTL.

Flight: S1-script v1.5 gate on the SC-005-07 s1-material (C-00012
沈佩兰 season-2 opener, R2007 preload, F-180 pre-registered).
--gpu-guard defers cheaply if the window flips after dispatch (R1986
verdict-void law: an in-flight call that hit a flipped window is
discarded and re-dispatched, never trusted). --wedge-probe (tech#120,
R2012/R2013 anchor: two 1500s flights burned zero-verdict in wedged
ollama windows) micro-probes the generation face first: a wedged
server bails in <=90s with rc 6 instead of burning the full cap.
Pre-flight hardening (tech#122, flight-3 burn R2025): the S1 seat is
the BASE qwen2.5:14b (~9.4GB). Flight-3 dispatched with free=4679MB
(AIHOT keep-warm 14b-8k runner + GUI crowd holding the rest), the
seat loaded partially CPU-offloaded and generation crawled past the
1500s cap with zero verdict (third burn). The 7b wedge probe passed
because it probed a different face than the one that burned.
Fix, all launcher-local (shared infra untouched):
  1. relief - stop IDLE ollama residents (only when util < 60%) so
     the seat can load fully into VRAM (R2011 precedent: keep-warm
     self-heals, no service debt);
  2. seat rate probe - tiny generation on the REAL seat model with a
     240s cap; slower than 150s = CPU-offload face -> rc 7, do not
     burn 1500s on a guaranteed-slow window (re-dispatch next one).
  3. util >= 60% at preflight = window flipped post-card -> rc 4
     defer, re-dispatch next window (R1986 verdict-void law).
Exit codes: 0 dispatched | 4 window-flip defer | 7 slow-window bail.
Verdict auto-archives to
docs/reviews/expert-verdicts/<ts>-S1-script.md + expert-calls.md line
(call_expert single-writer).

[RETIRED 2026-10-17 R2316, tech#185] GPU-lane zombie retirement guard.
Evidence: this launcher holds 208 fire-consume ledger rows, ALL no-fire
(99 workday-block + 42 mv-active + 26 cold-skip/load-class-starved +
minor gate families) - it never dispatched once, and no row has landed
since 2026-10-15 10:08. Its payload was completed on the CPU lane
(s1_call_cpu.py, R2257: S1 10/10, verdict 20261014-225340-S1-script.md)
and the full chain closed with F-180 registered (R2258,
review-20261015-sc00707-v1.md). ZERO undelivered batches. Any future
dispatch exits rc 3 immediately: a zombie re-invocation can never
re-run a finished review. Future S1 needs = a new CPU-lane launcher
(tech#169 lane), not this file.
"""

import sys as _retd_sys
_retd_sys.stderr.write(
    "RETIRED (tech#185, R2316): SC-005-07 GPU-lane S1 launcher - "
    "payload completed on CPU lane (F-180, R2257/R2258); rc 3\n")
_retd_sys.exit(3)

import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
OUT = Path(__file__).with_name("s1-run.out")
ERR = Path(__file__).with_name("s1-run.err")

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

MATERIAL = "data/storylines/audio/SC-005-07-v1-s1-material.md"
TIMEOUT_S = "1500"

RC_WINDOW_FLIP = 4
RC_SLOW_WINDOW = 7

UTIL_FLIP_PCT = 60          # preflight flip line (card gate is 80)
SEAT_PROBE_CAP_S = 240      # hard cap for the tiny seat generation
SEAT_PROBE_SLOW_S = 150     # elapsed above this = CPU-offload face
SEAT_PROBE_PROMPT = "Reply with exactly two chars: OK"


def _run(cmd, timeout, input_bytes=None):
    return subprocess.run(cmd, input=input_bytes, capture_output=True,
                          timeout=timeout)


def _gpu_headroom():
    """(util_pct, free_mb) or None - probe face, never raises."""
    try:
        p = _run(["nvidia-smi",
                  "--query-gpu=utilization.gpu,memory.free",
                  "--format=csv,noheader,nounits"], 15)
        first = p.stdout.decode("utf-8", "replace").strip().splitlines()[0]
        util_s, free_s = first.split(",")[:2]
        return int(util_s.strip()), int(free_s.strip())
    except Exception:
        return None


def _seat_model():
    """Seat model from the expert registry (never hardcoded)."""
    reg = json.loads((REPO / "data" / "experts" / "registry.json")
                     .read_text(encoding="utf-8"))
    return str(reg.get("model", ""))


def preflight():
    """Relief + seat rate probe. Returns (ok, rc, lines of evidence)."""
    ev = []
    h = _gpu_headroom()
    if h is None:
        ev.append("PREFLIGHT nvidia-smi unreadable - proceeding unguarded")
        return True, 0, ev
    util, free = h
    ev.append("PREFLIGHT util=%d%% free=%dMB" % (util, free))
    if util >= UTIL_FLIP_PCT:
        ev.append("DEFER window flipped after card (util %d%% >= %d%%)"
                 % (util, UTIL_FLIP_PCT))
        return False, RC_WINDOW_FLIP, ev
    # relief: stop idle ollama residents (safe - util just read < 60)
    try:
        ps = _run(["ollama", "ps"], 15)
        names = [ln.split()[0] for ln in
                 ps.stdout.decode("utf-8", "replace").strip().splitlines()
                 if ln.strip() and not ln.lstrip().lower().startswith("name")]
        for name in names:
            _run(["ollama", "stop", name], 30)
            ev.append("RELIEF stopped idle resident %s" % name)
    except Exception as exc:
        ev.append("RELIEF skip (ollama ps/stop unavailable: %s)" % exc)
    h2 = _gpu_headroom()
    if h2:
        ev.append("RELIEF free now %dMB" % h2[1])
    # seat rate probe: tiny generation on the REAL seat model
    seat = _seat_model()
    if not seat:
        ev.append("RATE-FAIL registry model unreadable")
        return False, RC_SLOW_WINDOW, ev
    t0 = time.time()
    try:
        p = _run(["ollama", "run", seat], SEAT_PROBE_CAP_S,
                 input_bytes=SEAT_PROBE_PROMPT.encode("utf-8"))
    except subprocess.TimeoutExpired:
        ev.append("RATE-FAIL seat probe timed out (%ds cap, model %s) - "
                  "slow window; re-dispatch next fire window"
                  % (SEAT_PROBE_CAP_S, seat))
        return False, RC_SLOW_WINDOW, ev
    elapsed = time.time() - t0
    if p.returncode != 0:
        ev.append("RATE-FAIL seat probe exit %d (model %s) - server face"
                  % (p.returncode, seat))
        return False, RC_SLOW_WINDOW, ev
    if elapsed > SEAT_PROBE_SLOW_S:
        ev.append("RATE-FAIL seat probe %ds > %ds (model %s) - CPU-offload"
                  " face; do not burn %ss on a slow window"
                  % (int(elapsed), SEAT_PROBE_SLOW_S, seat, TIMEOUT_S))
        return False, RC_SLOW_WINDOW, ev
    ev.append("RATE-OK seat probe %ds (model %s, %ds cap) - GO"
              % (int(elapsed), seat, SEAT_PROBE_CAP_S))
    return True, 0, ev


ok, rc, ev = preflight()
for line in ev:
    print(line, flush=True)
if not ok:
    print("PREFLIGHT-BAIL rc=%d" % rc, flush=True)
    sys.exit(rc)

with OUT.open("wb") as fo, ERR.open("wb") as fe:
    proc = subprocess.Popen(
        [sys.executable, "src/call_expert.py",
         "--expert", "S1-script",
         "--material", MATERIAL,
         "--timeout", TIMEOUT_S, "--gpu-guard", "--wedge-probe"],
        cwd=str(REPO), stdout=fo, stderr=fe,
        creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
print("SC-005-07 S1 flight dispatched pid=%d" % proc.pid)
