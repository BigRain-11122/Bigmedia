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

Exit codes: 0=GO, 1=NO-GO, 2=probe error (both faces unknown).
Consumed at GPU window judgment rounds (12:00-type); zero GPU work itself.
"""

import argparse
import json
import subprocess
import sys

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


def decide(pause_label, free_mb, min_free_mb):
    """Compose the two faces -> verdict dict (go bool + reasons)."""
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
        reasons.append(
            "vram-face: free %dMB < guard %dMB" % (free_mb, min_free_mb)
        )
    if go:
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
    ap.add_argument("--json", action="store_true",
                    help="single machine-readable line")
    args = ap.parse_args(argv)

    states = query_task_states()
    pause_label, dis, tot, known = classify_pause_face(states)
    free_mb = read_vram_free_mb()
    verdict = decide(pause_label, free_mb, args.min_free_mb)
    verdict["tasks_disabled"] = dis
    verdict["tasks_total"] = tot
    verdict["tasks_known"] = known

    if args.json:
        print(json.dumps(verdict, ensure_ascii=False))
    else:
        print("pause_face=%s (tasks %d/%d disabled, %d known)"
              % (pause_label, dis, tot, known))
        print("vram_free_mb=%s guard=%d"
              % (free_mb, args.min_free_mb))
        for r in verdict["reasons"]:
            print("- %s" % r)
        print("VERDICT=%s" % ("GO" if verdict["go"] else "NO-GO"))

    probe_error = (pause_label == "unknown") and (free_mb is None)
    if probe_error:
        return 2
    return 0 if verdict["go"] else 1


if __name__ == "__main__":
    sys.exit(main())
