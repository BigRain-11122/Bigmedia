#!/usr/bin/env python3
"""GPU window scheduling gate -- CEO pause face + VRAM face (tech#57).

R1891 gap anchor: 11:3x CEO order -> machine-state pause was executed by the
MV session (disables the 8 GPU production scheduled tasks), but the
`machine-state.ps1 -Mode status` inference can read MODE=resume when ollama
and ComfyUI are up with VRAM>10GB -- authorized-domain restarts (MV session
starting ComfyUI/ollama for its own sanctioned low-res keyframe batch) fool
that inference. The durable pause fingerprint is the SCHEDULED TASK STATES
(the machine-state.ps1 LOCALIZE-1 task list), not the MODE inference line.

Faces:
  pause_face: >=6 of the 8 machine-state tasks Disabled -> pause-fingerprint
              (CEO let-through order still active) -> NO-GO regardless of
              VRAM. 4-5 Disabled -> ambiguous -> conservative NO-GO.
              <=3 -> clear. Probe failure -> unknown (honest note; VRAM face
              still decides -- documented fallback to the pre-tech#57
              single-gate behavior). Allows 1-2 standalone-disabled tasks
              (e.g. MiniGameOllamaKeepWarm was Disabled pre-pause, R1878).
  vram_face:  nvidia-smi free MB < --min-free-mb -> NO-GO
              (default 9216 = MD-0002 script-leg guard line).
  stability:  tech#75 face (R1917 anchor): under a co-lane load cycle
              (MV sprint Krea2 gen cycles swing free 3278<->11692 MB on a
              seconds scale) a single-sample free reading is unreliable --
              a 1500s review flight spans many cycles. --samples N takes N
              consecutive readings --sample-interval seconds apart and the
              verdict uses the WORST-CASE (min) free / (max) util.
              Band (max-min) is reported and >= VRAM_BAND_ADVISE_MB adds an
              advisory reason (oscillating regime; long-flight contention
              risk) without changing the verdict on its own.
  util_face:  --util-max P adds a compute gate (tech#75 three-gate member):
              worst-case util > P -> NO-GO (boundary strict, tech#44 parity).

Exit codes: 0=GO, 1=NO-GO, 2=probe error (both faces unknown).
Consumed at GPU window judgment rounds (12:00-type); zero GPU work itself.
"""

import argparse
import json
import subprocess
import sys
import time

# machine-state.ps1 LOCALIZE-1 task list (bm-a deploy face, r798 kit)
MACHINE_STATE_TASKS = [
    "BigCompute-OSLoop",
    "BigCompute-OSLoop-PM",
    "BigCompute-GPU-IdleWatch",
    "BigCompute-CleanWindowProbe",
    "BigCompute-OrderSentinel",
    "BigCompute-ResidentQA",
    "MiniGameOllamaKeepWarm",
    "MiniGameOllamaServe",
]

# >=6/8 disabled = pause fingerprint; 4-5 = ambiguous (conservative NO-GO)
PAUSE_FINGERPRINT_MIN = 6
PAUSE_AMBIGUOUS_MIN = 4

# tech#75 stability face: sampled free band >= this (MB) within the sampling
# window -> oscillating-regime advisory (R1917 anchor band was 8414MB:
# 3278 <-> 11692 swing between two probes ~110s apart).
VRAM_BAND_ADVISE_MB = 2048


def _run_capture(cmd, timeout=10):
    """Run a console probe, return decoded stdout or None on any failure."""
    try:
        p = subprocess.run(
            cmd, capture_output=True, timeout=timeout
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if p.returncode != 0:
        return None
    return p.stdout.decode("utf-8", errors="replace")


def parse_task_disabled(text):
    """Parse `schtasks /query /tn <t> /fo LIST` output -> True/False/None.

    Locale-tolerant: matches the status line by label (Status/状态) and
    detects the disabled value in zh-CN (已禁用/已停用) or en (Disabled).
    Returns None when the status line cannot be found (probe-unreadable).
    """
    if not text:
        return None
    disabled = False
    found = False
    for line in text.splitlines():
        stripped = line.strip()
        low = stripped.lower()
        if low.startswith("status") or stripped.startswith("状态"):
            found = True
            if "禁用" in stripped or "停用" in stripped or "disabled" in low:
                disabled = True
            break
    if not found:
        return None
    return disabled


def query_task_states(tasks=None):
    """Query each machine-state task -> {name: True(disabled)/False/None}."""
    names = MACHINE_STATE_TASKS if tasks is None else list(tasks)
    states = {}
    for name in names:
        out = _run_capture(
            ["schtasks", "/query", "/tn", name, "/fo", "LIST"]
        )
        states[name] = parse_task_disabled(out)
    return states


def classify_pause_face(states):
    """Classify CEO pause face from task states.

    Returns (label, disabled_count, total, known) where label is one of
    pause-fingerprint / ambiguous / clear / unknown.
    """
    total = len(states)
    if total == 0:
        return ("unknown", 0, 0, 0)
    disabled = sum(1 for v in states.values() if v is True)
    known = sum(1 for v in states.values() if v is not None)
    if known == 0:
        return ("unknown", disabled, total, 0)
    if disabled >= PAUSE_FINGERPRINT_MIN:
        return ("pause-fingerprint", disabled, total, known)
    if disabled >= PAUSE_AMBIGUOUS_MIN:
        return ("ambiguous", disabled, total, known)
    return ("clear", disabled, total, known)


def read_vram_free_mb():
    """nvidia-smi total/used -> free MB, or None on probe failure."""
    out = _run_capture(
        ["nvidia-smi", "--query-gpu=memory.total,memory.used",
         "--format=csv,noheader,nounits"],
        timeout=15,
    )
    if not out:
        return None
    first = out.strip().splitlines()[0]
    parts = [p.strip() for p in first.split(",")]
    if len(parts) < 2:
        return None
    try:
        total, used = int(parts[0]), int(parts[1])
    except ValueError:
        return None
    return total - used


def read_gpu_sample():
    """One nvidia-smi query -> {'free': MB, 'util': pct} or None.

    Single query carries both the VRAM and the compute columns so a sampled
    window never doubles the probe cost (tech#54 read_gpu_context parity).
    """
    out = _run_capture(
        ["nvidia-smi",
         "--query-gpu=memory.total,memory.used,utilization.gpu",
         "--format=csv,noheader,nounits"],
        timeout=15,
    )
    if not out:
        return None
    first = out.strip().splitlines()[0]
    parts = [p.strip() for p in first.split(",")]
    if len(parts) < 3:
        return None
    try:
        total, used = int(parts[0]), int(parts[1])
        util = int(parts[2])
    except ValueError:
        return None
    return {"free": total - used, "util": util}


def sample_gpu(n, interval, sampler=None, sleep_fn=None):
    """Take n consecutive GPU readings, `interval` seconds apart.

    Returns (readings, n_fail): readings = list of {'free','util'} dicts
    (successful probes only), n_fail = probe failure count (honest note,
    never fabricated as data). sleep_fn injectable for tests.
    """
    if sampler is None:
        sampler = read_gpu_sample
    if sleep_fn is None:
        sleep_fn = time.sleep
    readings = []
    n_fail = 0
    for i in range(n):
        if i > 0 and interval > 0:
            sleep_fn(interval)
        r = sampler()
        if r is None:
            n_fail += 1
        else:
            readings.append(r)
    return readings, n_fail


def aggregate_gpu_readings(readings, n_fail=0):
    """Pure core: aggregate sampled readings -> worst-case stats dict.

    Returns {'free_min','free_max','band_mb','util_max','read_ok','read_fail'}
    or None when no reading succeeded (probe-unreadable face).
    """
    if not readings:
        return None
    frees = [r["free"] for r in readings]
    utils = [r.get("util") for r in readings if r.get("util") is not None]
    return {
        "free_min": min(frees),
        "free_max": max(frees),
        "band_mb": max(frees) - min(frees),
        "util_max": max(utils) if utils else None,
        "read_ok": len(readings),
        "read_fail": n_fail,
    }


# tech#79 attribution face: known GPU producer patterns (case-insensitive
# substring on process_name). Non-whitelist rows fold into one count.
# R1929 anchor: manual attribution read = ComfyUI python + Tuanjie +
# llama-server. WDDM blocks per-process VRAM (used_memory=[N/A]) so the
# face is process_name/pid only -- advisory, never a gate.
PRODUCER_PATTERNS = ("python", "llama", "ollama", "tuanjie", "unity",
                     "comfy")

# tech#80: GUI-noise exclusion (advisory face only). Families that can
# FALSE-match a producer pattern are folded to other BEFORE the whitelist
# check -- R1930 live anchor: PlasticSCM "unityvcstray.exe" matched the
# "unity" pattern, "Tuanjie Hub.exe" matched "tuanjie"; both are tray /
# launcher shells, not VRAM producers. Noise is matched against the
# executable BASENAME only: the families are exe-name traits, and a
# full-path match false-folds real producers installed under e.g.
# C:\Program Files\Tuanjie\Hub\Editor\... (R1931 first-cut anchor).
# GUI rows that can never match a producer pattern already fold
# naturally, so the list stays minimal (tray/hub).
GUI_NOISE_PATTERNS = ("tray", "hub")


def query_compute_apps(timeout=10):
    """nvidia-smi --query-compute-apps -> [{'pid','process'}] or None.

    Locale-tolerant parse: rows whose first cell is not a plain integer
    (e.g. the 'No running processes found' banner, junk) are skipped --
    an empty list is an honest 'no consumers' reading, None is unreadable.
    """
    out = _run_capture(
        ["nvidia-smi", "--query-compute-apps=pid,process_name",
         "--format=csv,noheader,nounits"],
        timeout=timeout,
    )
    if not out:
        return None
    rows = []
    for line in out.strip().splitlines():
        parts = [p.strip() for p in line.strip().split(",")]
        if len(parts) < 2 or not parts[0].isdigit():
            continue
        rows.append({"pid": int(parts[0]), "process": parts[1]})
    return rows


def classify_producers(rows, patterns=None, noise=None):
    """Fold compute-app rows -> attribution dict (advisory only).

    Whitelist-matched processes are listed with pid; GUI-noise rows
    (tray/launcher shells -- GUI_NOISE_PATTERNS) and everything else fold
    into a single other count so GUI noise never floods the reading.
    ``noise=()`` restores the raw-whitelist face (no exclusion).
    """
    pats = PRODUCER_PATTERNS if patterns is None else tuple(patterns)
    npats = GUI_NOISE_PATTERNS if noise is None else tuple(noise)
    producers = []
    other = 0
    for r in rows:
        name = r["process"].lower()
        # noise families are exe-name traits: match basename only, else
        # directory names (\Hub\Editor\) false-fold real producers.
        tail = name.replace("/", "\\").split("\\")[-1]
        if any(n in tail for n in npats):
            other += 1
            continue
        if any(p in name for p in pats):
            producers.append(r)
        else:
            other += 1
    return {"producers": producers, "other": other, "raw": len(rows)}


def decide(pause_label, free_mb, min_free_mb, util_max=None, max_util=None,
           band_mb=None, read_fail=None, sampled=False):
    """Compose the faces -> verdict dict (go bool + reasons).

    Backward-compatible: the extra kwargs default to None and the
    single-sample path (legacy callers/tests) is behavior-identical.
    Sampled path: free_mb must be the WORST-CASE (min) reading; band_mb /
    read_fail add honest notes; util_max adds the compute gate
    (worst-case max_util; boundary strict, tech#44 parity).
    """
    reasons = []
    go = True
    if pause_label == "pause-fingerprint":
        go = False
        reasons.append(
            "ceo-pause-face: machine-state tasks disabled (pause order active)"
        )
    elif pause_label == "ambiguous":
        go = False
        reasons.append("pause-face-ambiguous: conservative NO-GO")
    if free_mb is None:
        if not go:
            reasons.append("vram-face: probe-unreadable")
        else:
            go = False
            reasons.append("vram-face: probe-unreadable (cannot verify)")
    elif free_mb < min_free_mb:
        go = False
        if sampled:
            reasons.append(
                "vram-face: worst-case free %dMB < guard %dMB"
                % (free_mb, min_free_mb)
            )
        else:
            reasons.append(
                "vram-face: free %dMB < guard %dMB" % (free_mb, min_free_mb)
            )
    if util_max is not None:
        if max_util is None:
            go = False
            reasons.append(
                "util-face: probe-unreadable (cannot verify max %d%%)"
                % util_max
            )
        elif max_util > util_max:
            go = False
            reasons.append(
                "util-face: worst-case util %d%% > gate %d%%"
                % (max_util, util_max)
            )
    if sampled and band_mb is not None and band_mb >= VRAM_BAND_ADVISE_MB:
        reasons.append(
            "vram-band advisory: free oscillates band %dMB within sampling "
            "window (>= %dMB) -- sec-scale load-cycle regime, long-flight "
            "contention risk (tech#75/R1917 anchor)" % (band_mb,
                                                        VRAM_BAND_ADVISE_MB)
        )
    if read_fail:
        reasons.append(
            "vram-face note: %d probe sample(s) failed; verdict on "
            "measured samples only" % read_fail
        )
    if go:
        if sampled:
            reasons.append(
                "faces clear (pause-face clear, worst-case free %sMB >= "
                "%dMB across samples)" % (free_mb, min_free_mb)
            )
        else:
            reasons.append(
                "both faces clear (pause-face clear, vram free %sMB >= %dMB)"
                % (free_mb, min_free_mb)
            )
    return {"go": go, "pause_face": pause_label,
            "vram_free_mb": free_mb, "min_free_mb": min_free_mb,
            "reasons": reasons}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--min-free-mb", type=int, default=9216,
                    help="VRAM free guard line in MB (default 9216)")
    ap.add_argument("--samples", type=int, default=1,
                    help="consecutive nvidia-smi readings for the stability "
                         "face (tech#75); 1 = legacy single-sample path")
    ap.add_argument("--sample-interval", type=int, default=5,
                    help="seconds between samples (samples > 1 only)")
    ap.add_argument("--util-max", type=int, default=None,
                    help="compute gate: worst-case util %% must be <= this "
                         "(tech#75 three-gate member; boundary strict)")
    ap.add_argument("--json", action="store_true",
                    help="single machine-readable line")
    args = ap.parse_args(argv)
    if args.samples < 1:
        ap.error("--samples must be >= 1")
    if args.sample_interval < 0:
        ap.error("--sample-interval must be >= 0")

    states = query_task_states()
    pause_label, dis, tot, known = classify_pause_face(states)

    max_util = None
    band_mb = None
    read_fail = None
    sampled = args.samples > 1
    if sampled or args.util_max is not None:
        readings, read_fail = sample_gpu(
            args.samples, args.sample_interval)
        agg = aggregate_gpu_readings(readings, read_fail)
        if agg is None:
            free_mb = None
        else:
            free_mb = agg["free_min"]
            max_util = agg["util_max"]
            band_mb = agg["band_mb"]
        sampled = True
    else:
        free_mb = read_vram_free_mb()
    verdict = decide(pause_label, free_mb, args.min_free_mb,
                     util_max=args.util_max, max_util=max_util,
                     band_mb=band_mb, read_fail=read_fail,
                     sampled=sampled)
    verdict["tasks_disabled"] = dis
    verdict["tasks_total"] = tot
    verdict["tasks_known"] = known
    if sampled:
        verdict["samples"] = args.samples
        verdict["free_min_mb"] = free_mb
        if band_mb is not None:
            verdict["free_max_mb"] = agg["free_max"]
            verdict["band_mb"] = band_mb
            verdict["util_max"] = max_util
            verdict["read_ok"] = agg["read_ok"]
            verdict["read_fail"] = agg["read_fail"]

    # tech#79: attach the producer attribution face on NO-GO only (the
    # judgment position needs to explain a blocked window, not a clear
    # one). Advisory -- never touches go/reasons/exit code. Unreadable
    # probe -> explicit error note (honest absence, not silent omission).
    if not verdict["go"]:
        apps = query_compute_apps()
        if apps is None:
            verdict["attribution"] = {"error": "compute-apps-unreadable"}
        else:
            verdict["attribution"] = classify_producers(apps)

    if args.json:
        print(json.dumps(verdict, ensure_ascii=False))
    else:
        print("pause_face=%s (tasks %d/%d disabled, %d known)"
              % (pause_label, dis, tot, known))
        if sampled:
            print("vram_free_mb=%s (worst-case of %d samples, band %sMB)"
                  % (free_mb, args.samples, band_mb))
        else:
            print("vram_free_mb=%s guard=%d"
                  % (free_mb, args.min_free_mb))
        for r in verdict["reasons"]:
            print("- %s" % r)
        if "attribution" in verdict:
            print("attribution=%s"
                  % json.dumps(verdict["attribution"], ensure_ascii=False))
        print("VERDICT=%s" % ("GO" if verdict["go"] else "NO-GO"))

    probe_error = (pause_label == "unknown") and (free_mb is None)
    if probe_error:
        return 2
    return 0 if verdict["go"] else 1


if __name__ == "__main__":
    sys.exit(main())
