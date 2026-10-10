#!/usr/bin/env python3
"""Review-leg fire-window composite judgment card (tech#85 remainder).

Why: the first true fire window (R1938) was adjudicated BY HAND from
three scattered probe readings (gate --json x mv_sprint_probe --json x
ollama_probe --json). This card mechanizes that adjudication into ONE
command producing ONE citable line, so the four-legs fire decision
reads the card output instead of re-deriving the chain by hand each
round. Credit value passing follows the documented tech#75/#83 SOP
verbatim:

  sequence law (tech#77): gate static FIRST, ollama probe LAST among
  the GPU-touching steps -- the gate sampling window must not be
  polluted by the probe's own cold load (a probe that actually flew
  leaves its generation load in the sampling window). The mv probe is
  pure file reads and sits between them.

  credit re-run law (tech#75 SOP + tech#82 yield discipline): the
  --eviction-aware-mb re-run is attempted ONLY after a skip-path
  probe whose counterfactual verdict reads "fly", ONLY with a positive
  evictable_mb reading, and ONLY when the MV lanes read quiet -- a
  probe that flew never triggers a credit re-run, and an active MV
  window never gets eviction credit.

Verdict core (classify_fire, pure):
  FIRE path A (hot-resident): mv quiet + probe GEN-OK + static gate GO
  FIRE path B (eviction credit): mv quiet + probe cold-skip +
        counterfactual fly + credit re-run gate GO
  no-fire otherwise. An active or unreadable MV face is fail-closed:
  a missing reading must never read as quiet, and the card never fires
  on it.

rc contract (consumers gate on rc, not on parsing):
  0 = fire window open (verdict "fire")
  1 = no-fire (verdict "no-fire", reasons cited)
  2 = usage error or tooling failure (child probe could not run or its
      JSON line was unparseable -- fail-closed, never reads as fire)

Usage:
  python src/os/fire_window_card.py [--json] [--samples N]
      [--sample-interval S] [--min-free-mb M] [--util-max U]
"""

import argparse
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GATE_SCRIPT = REPO / "src" / "os" / "gpu_window_gate.py"
MV_PROBE_SCRIPT = REPO / "src" / "os" / "mv_sprint_probe.py"
OLLAMA_PROBE_SCRIPT = REPO / "src" / "os" / "ollama_probe.py"

DEFAULT_SAMPLES = 6
DEFAULT_INTERVAL = 5
REVIEW_MIN_FREE_MB = 2048
REVIEW_UTIL_MAX = 80
CHILD_TIMEOUT_S = 240
# Fire-verdict freshness (tech#89): R1943 anchor -- the window closed
# <2min after the card said fire (MV i2v wave re-occupied the card, two
# guard defers followed). A consumer holding a fire verdict older than
# this TTL must re-run the card instead of consuming a stale GO.
FIRE_VALID_S = 120

# tech#90: readings are collected SEQUENTIALLY (gate 6x5s ~30s, then
# mv, then probe, then an optional credit re-run), so by verdict time
# the oldest reading is already ~40-70s stale -- the 120s fire TTL's
# usable margin is silently eaten by read-side staleness (R1943
# anchor: the shadow window closed <2min after fire). Each slim
# reading therefore carries collected_at + age_s_at_verdict, plus a
# card-level oldest_reading_age_s, so a consumer can discount the TTL
# by the reading age instead of consuming an implicitly stale GO.
COLLECTED_AT_FMT = "%Y-%m-%d %H:%M:%S"

PROBE_SKIP_STATUS = "skipped-not-resident"
PATH_A = "A-hot-resident"
PATH_B = "B-eviction-credit"

USAGE = ("usage: python src/os/fire_window_card.py [--json] "
         "[--samples N] [--sample-interval S] [--min-free-mb M] "
         "[--util-max U]")


class CardChildError(Exception):
    """A child probe failed to run or its JSON line was unparseable."""


def _child_env():
    """Child probes print UTF-8 on pipes regardless of console code page."""
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    return env


def _run_json(argv, timeout_s=CHILD_TIMEOUT_S):
    """Run one child probe, parse its single JSON line -> dict.

    A nonzero child rc is a legitimate reading (gate NO-GO, probe
    saturation, mv fail-closed) -- the payload is parsed and returned.
    CardChildError is raised only when the reading itself is missing:
    launch failure, timeout, empty stdout, or an unparseable line
    (fail-closed: the card must never guess a reading)."""
    try:
        proc = subprocess.run([sys.executable] + [str(a) for a in argv],
                              cwd=str(REPO), env=_child_env(),
                              capture_output=True, timeout=timeout_s)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CardChildError("child failed: %s" % exc)
    text = (proc.stdout or b"").decode("utf-8", "replace").strip()
    if not text:
        raise CardChildError("child rc=%d, no stdout" % proc.returncode)
    line = text.splitlines()[-1]
    try:
        payload = json.loads(line)
    except ValueError as exc:
        raise CardChildError("child JSON unparseable: %s" % exc)
    if not isinstance(payload, dict):
        raise CardChildError("child JSON not an object")
    return payload


def real_gate_static(samples, interval, min_free, util_max):
    """Reading 1: static review-leg gate (samples face, tech#75)."""
    return _run_json([GATE_SCRIPT, "--samples", samples,
                      "--sample-interval", interval,
                      "--min-free-mb", min_free, "--util-max", util_max,
                      "--json"])


def real_gate_credit(credit_mb, samples, interval, min_free, util_max):
    """Reading 4 (conditional): gate re-run with eviction credit
    (tech#83 --eviction-aware-mb; credit value = the probe's ps
    evictable_mb reading, passed by the card per the SOP)."""
    return _run_json([GATE_SCRIPT, "--samples", samples,
                      "--sample-interval", interval,
                      "--min-free-mb", min_free, "--util-max", util_max,
                      "--eviction-aware-mb", credit_mb, "--json"])


def real_mv_probe():
    """Reading 2: MV lanes write-silence face (tech#84; zero GPU)."""
    return _run_json([MV_PROBE_SCRIPT, "--json"])


def real_ollama_probe():
    """Reading 3: ollama service/residency face (tech#51/77/78/82)."""
    return _run_json([OLLAMA_PROBE_SCRIPT, "--json"])


def classify_fire(gate, mv, probe, gate_credit=None):
    """Pure core -> (verdict, path, reasons).

    The mv face gates both paths: "quiet" is required, "active" blocks
    (yield discipline), anything else (None/error) is fail-closed. The
    credit re-run reading participates only through path B; the static
    gate is cited in the reasons on a path A miss."""
    mv_verdict = (mv or {}).get("verdict")
    if mv_verdict != "quiet":
        tag = "mv-active" if mv_verdict == "active" \
            else "mv-unreadable-fail-closed"
        return "no-fire", None, [tag]
    status = (probe or {}).get("status")
    if status == "ok":
        # GEN-OK: resident/hot service confirmed by the probe flight.
        if (gate or {}).get("go"):
            return "fire", PATH_A, []
        return "no-fire", None, ["gate-static-no-go"] + \
            list((gate or {}).get("reasons") or [])
    if status == PROBE_SKIP_STATUS:
        # Cold-skip path: model not resident, static free under the
        # cold-load envelope. Credit is the only admissible unlock.
        if probe.get("eviction_aware_verdict") != "fly":
            return "no-fire", None, ["cold-skip-no-admissible-credit"]
        if gate_credit is None:
            return "no-fire", None, ["credit-window-closed"]
        if gate_credit.get("go"):
            return "fire", PATH_B, []
        return "no-fire", None, ["gate-credit-no-go"] + \
            list(gate_credit.get("reasons") or [])
    # Saturated / contended / cold-reload / error faces: cite the face
    # token when present, else the raw status.
    face = (probe or {}).get("face")
    tag = "probe-face-%s" % face if face else "probe-status-%s" % status
    return "no-fire", None, [tag]


def _slim_gate(g):
    if not isinstance(g, dict):
        return None
    out = {
        "go": g.get("go"),
        "reasons": g.get("reasons") or [],
        "free_min_mb": g.get("free_min_mb"),
        "free_max_mb": g.get("free_max_mb"),
        "band_mb": g.get("band_mb"),
        "util_max": g.get("util_max"),
        "min_free_mb": g.get("min_free_mb"),
    }
    if g.get("evictable_mb") is not None:
        out["evictable_mb"] = g.get("evictable_mb")
    if g.get("effective_free_mb") is not None:
        out["effective_free_mb"] = g.get("effective_free_mb")
    return out


def _slim_mv(m):
    if not isinstance(m, dict):
        return None
    return {"verdict": m.get("verdict"), "rc": m.get("rc"),
            "newest_age_min": m.get("newest_age_min")}


def _slim_probe(p):
    if not isinstance(p, dict):
        return None
    return {"status": p.get("status"), "face": p.get("face"),
            "rc": p.get("rc"), "gpu_free_mb": p.get("gpu_free_mb"),
            "evictable_mb": p.get("evictable_mb"),
            "eviction_aware_verdict": p.get("eviction_aware_verdict")}


def orchestrate(gate_static_fn, mv_fn, probe_fn, gate_credit_fn,
                samples=DEFAULT_SAMPLES, interval=DEFAULT_INTERVAL,
                min_free=REVIEW_MIN_FREE_MB, util_max=REVIEW_UTIL_MAX,
                now=None, clock=None):
    """Run the three readings in sequence-law order, attempt the credit
    re-run only per the SOP, and compose the one-line card dict.

    The four function arguments are the injection seams (real seams =
    real_gate_static / real_mv_probe / real_ollama_probe /
    real_gate_credit); tests inject fakes for hermetic runs. ``clock``
    (tech#90) stamps each reading's collection time; tests inject a
    deterministic advancing clock for age-math verification."""
    clock = clock or datetime.datetime.now
    sequence = ["gate-static"]
    gate_at = clock()
    gate = gate_static_fn(samples, interval, min_free, util_max)
    sequence.append("mv-probe")
    mv_at = clock()
    mv = mv_fn()
    sequence.append("ollama-probe")
    probe_at = clock()
    probe = probe_fn()

    gate_credit = None
    credit_at = None
    if (probe.get("status") == PROBE_SKIP_STATUS
            and probe.get("eviction_aware_verdict") == "fly"
            and mv.get("verdict") == "quiet"):
        credit_mb = probe.get("evictable_mb") or 0
        if isinstance(credit_mb, (int, float)) and credit_mb > 0:
            sequence.append("gate-credit")
            credit_at = clock()
            gate_credit = gate_credit_fn(credit_mb, samples, interval,
                                         min_free, util_max)

    verdict, path, reasons = classify_fire(gate, mv, probe, gate_credit)
    now_dt = now or clock()
    card = {
        "card": "fire_window_card",
        "ts": now_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "verdict": verdict,
        "path": path,
        "reasons": reasons,
        "sequence": sequence,
        "readings": {
            "gate": _slim_gate(gate),
            "mv": _slim_mv(mv),
            "probe": _slim_probe(probe),
            "gate_credit": _slim_gate(gate_credit),
        },
    }
    stamps = {"gate": gate_at, "mv": mv_at, "probe": probe_at,
              "gate_credit": credit_at}
    oldest_age_s = 0
    for name, reading in card["readings"].items():
        stamp = stamps.get(name)
        if reading is None or stamp is None:
            continue
        age_s = int((now_dt - stamp).total_seconds())
        reading["collected_at"] = stamp.strftime(COLLECTED_AT_FMT)
        reading["age_s_at_verdict"] = age_s
        oldest_age_s = max(oldest_age_s, age_s)
    card["oldest_reading_age_s"] = oldest_age_s
    if verdict == "fire":
        fired_epoch = int(now_dt.timestamp())
        card["fired_at"] = fired_epoch
        card["valid_s"] = FIRE_VALID_S
        card["expires_at"] = fired_epoch + FIRE_VALID_S
    return card


def _render_human(card):
    lines = ["fire-window-card %s: verdict=%s path=%s"
             % (card["ts"], card["verdict"], card["path"])]
    if card["reasons"]:
        lines.append("  reasons: %s" % "; ".join(str(r) for r in
                                                 card["reasons"]))
    gate = card["readings"]["gate"] or {}
    lines.append("  gate: go=%s free_min=%s util_max=%s band=%s"
                 % (gate.get("go"), gate.get("free_min_mb"),
                    gate.get("util_max"), gate.get("band_mb")))
    mv = card["readings"]["mv"] or {}
    lines.append("  mv: verdict=%s newest_age_min=%s"
                 % (mv.get("verdict"), mv.get("newest_age_min")))
    probe = card["readings"]["probe"] or {}
    lines.append("  probe: status=%s face=%s evictable=%s counterfactual=%s"
                 % (probe.get("status"), probe.get("face"),
                    probe.get("evictable_mb"),
                    probe.get("eviction_aware_verdict")))
    credit = card["readings"]["gate_credit"]
    if credit:
        lines.append("  gate-credit: go=%s evictable=%s effective_free=%s"
                     % (credit.get("go"), credit.get("evictable_mb"),
                        credit.get("effective_free_mb")))
    age_parts = []
    for name in ("gate", "mv", "probe", "gate_credit"):
        reading = card["readings"].get(name)
        if isinstance(reading, dict) and "age_s_at_verdict" in reading:
            age_parts.append("%s=%ss" % (name,
                                         reading["age_s_at_verdict"]))
    if age_parts:
        lines.append("  readings-age: %s (oldest=%ss vs fire TTL %ss"
                     " -- count reading staleness against the TTL, the"
                     " verdict-ts clock starts the window)"
                     % (" ".join(age_parts),
                        card.get("oldest_reading_age_s"), FIRE_VALID_S))
    if card.get("verdict") == "fire":
        lines.append("  fire-valid: %ss (expires epoch %s; re-run the "
                     "card after expiry, never consume a stale GO)"
                     % (card.get("valid_s"), card.get("expires_at")))
    return "\n".join(lines)


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    parser = argparse.ArgumentParser(
        description="Review-leg fire-window composite judgment card "
                    "(tech#85): gate x mv-sprint x ollama-probe -> one "
                    "fire/no-fire line. rc 0=fire, 1=no-fire, 2=tooling "
                    "error (fail-closed).")
    parser.add_argument("--json", action="store_true",
                        help="single machine-readable line")
    parser.add_argument("--samples", type=int, default=DEFAULT_SAMPLES,
                        help="consecutive nvidia-smi readings for the "
                             "stability face (default %d)" % DEFAULT_SAMPLES)
    parser.add_argument("--sample-interval", type=int,
                        default=DEFAULT_INTERVAL,
                        help="seconds between samples (default %d)"
                             % DEFAULT_INTERVAL)
    parser.add_argument("--min-free-mb", type=int,
                        default=REVIEW_MIN_FREE_MB,
                        help="review-leg VRAM free guard in MB (default %d)"
                             % REVIEW_MIN_FREE_MB)
    parser.add_argument("--util-max", type=int, default=REVIEW_UTIL_MAX,
                        help="review-leg compute gate worst-case util cap "
                             "(default %d)" % REVIEW_UTIL_MAX)
    args = parser.parse_args(argv)

    if args.samples < 1 or args.sample_interval < 1 \
            or args.util_max < 0 or args.min_free_mb < 0:
        print(USAGE)
        return 2

    try:
        card = orchestrate(real_gate_static, real_mv_probe,
                           real_ollama_probe, real_gate_credit,
                           samples=args.samples,
                           interval=args.sample_interval,
                           min_free=args.min_free_mb,
                           util_max=args.util_max)
    except CardChildError as exc:
        payload = {"card": "fire_window_card", "verdict": "error",
                   "path": None, "reasons": [str(exc)],
                   "ts": datetime.datetime.now().strftime(
                       "%Y-%m-%d %H:%M:%S")}
        print(json.dumps(payload, ensure_ascii=False)
              if args.json else "fire-window-card: verdict=error "
              "reason=%s" % exc)
        return 2

    if args.json:
        print(json.dumps(card, ensure_ascii=False))
    else:
        print(_render_human(card))
    return 0 if card["verdict"] == "fire" else 1


if __name__ == "__main__":
    sys.exit(main())
