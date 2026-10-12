#!/usr/bin/env python3
"""ComfyUI lane activity probe (tech#106; R1987 delivery).

Gap anchor (R1986 live evidence): a fire GO (16:40:56, util_max 32) was
consumed, the MV i2v wave re-ignited seconds later, and the S1 review
flight burned with zero verdicts. The R1986 consumption law now requires
a ComfyUI-side activity reading BEFORE consuming any fire GO -- and the
"file-quiet x hardware-busy = long render in flight" narrative
(R1936/R1937) had no attestation from the server itself: it cannot
distinguish "wave in flight" from "idle server holding VRAM while the
desktop GUI fleet pins util" (R1987 live proof: queue empty, CPU delta
0 over 4s, nvidia-smi util 100%).

Faces (both cross-repo read-only, zero write contact; the ComfyUI
server belongs to the MV session domain -- this probe never touches it
beyond GET /queue and a WMI process query):
  queue  GET {base}/queue -> {running, pending} counts. The wave
         attestation: a submitted KF/i2v batch shows here even in the
         util sampling gaps between jobs (the R1986 flip window).
  cpu    ComfyUI python process CPU-time delta over --sample-interval
         (PowerShell Get-CimInstance: Name LIKE '%python%' AND
         CommandLine match 'comfyui' -- the portable install path
         carries the token, verified live 10-11 17:2x PID 58200).
         'empty' = query ok, zero comfy processes = server down
         (nothing can render). delta >= --cpu-threshold-ms = server
         computing something.

Verdict (annotation-level, ZERO GATE -- the judgment position reads
this before consuming a fire GO; the fire card itself is untouched):
  active   queue running>0 or pending>0 (wave in flight / queued), or
           cpu delta at/over the threshold. A single readable positive
           face attests active even when the other face is unreadable
           (false-active costs an unnecessary yield; false-quiet costs
           a burned flight).
  quiet    cpu 'empty' (server down), or cpu 'ok' small-delta AND
           queue 'ok' 0/0. Lane statement, not a VRAM statement: an
           idle ComfyUI process keeps loaded models resident.
  error    no positive attestation and no coherent-idle attestation
           (fail-closed: an unreadable face never reads as quiet).

stale-render advisory: queue running>0 while cpu delta is ~0 (<
--stale-threshold-ms) = wedged-job candidate (R1876 family). Advisory
only: GPU-bound phases can legitimately show low CPU -- cross-read with
the fire card util face, never a gate.

wave-gap face (tech#136; R2075 live evidence): the probe read
queue 0/0 + cpu-quiet at 20:44 and the KF iteration loop re-ignited
minutes later -- ComfyUI output took 34 files in three waves
(20:23/20:33/20:39) WITHIN the hour. A client-driven iteration loop
(KF batch -> review -> reseed -> resubmit) leaves the server genuinely
idle for 6-10 minutes between waves, so queue+cpu alone cannot
distinguish "batch done" from "wave gap". Third face: fresh entries
(top-level files AND directories -- a file created inside a subdir
bumps the dir mtime) in the ComfyUI output tree within
--output-recency-s (default 900s) attest the loop is still alive ->
verdict active, note wave-gap-recent-output. Conservative-only wiring:
the face can ADD an active attestation, never force quiet -- an
unreadable/absent output dir (other lane installs) leaves the old
two-face behavior untouched.

rc contract (family: mv_sprint_probe / ollama_probe):
  0 = quiet   1 = active   2 = error

--ledger [PATH]: opt-in one-row-per-run JSONL (ts/verdict/rc/running/
pending/cpu_delta_ms/pids). Error runs still land their row
(fail-closed is data -- tech#52/#86 family). Best-effort write: WARN on
failure, never raises, never changes rc.
"""

import argparse
import datetime
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LEDGER = REPO_ROOT / "data" / "pipeline" / "comfy-activity-ledger.jsonl"

DEFAULT_BASE_URL = "http://127.0.0.1:8188"
DEFAULT_SAMPLE_INTERVAL_S = 4.0
DEFAULT_CPU_THRESHOLD_MS = 300.0
DEFAULT_STALE_THRESHOLD_MS = 100.0
# tech#136 wave-gap face: MV lane ComfyUI (port 8188 portable install)
# output tree. R2075 KF waves were 6-10 min apart; 900s covers the
# observed gaps with margin (false-active costs a yield, false-quiet
# costs a burned flight -- bias long).
DEFAULT_OUTPUT_DIR = Path(
    r"C:\Users\sjs20\comfyui-krea\ComfyUI_windows_portable\ComfyUI\output")
DEFAULT_OUTPUT_RECENCY_S = 900.0
PS_TIMEOUT_S = 30
QUEUE_TIMEOUT_S = 5

# Name filter keeps the powershell query process itself out of the
# match set (its own CommandLine carries the 'comfyui' token -- live
# self-match caught 10-11 17:2x); the ComfyUI server runs under
# python.exe (portable python_embeded path contains 'comfyui-krea').
PS_COMMAND = (
    "Get-CimInstance Win32_Process -Filter \"Name LIKE '%python%'\" | "
    "Where-Object { $_.CommandLine -match 'comfyui' } | "
    "Select-Object ProcessId, KernelModeTime, UserModeTime | "
    "ConvertTo-Json -Compress"
)

RC_QUIET = 0
RC_ACTIVE = 1
RC_ERROR = 2


def _real_ps_runner(command):
    """Real seam: -> (ok, stdout_str). ok=False on spawn failure,
    timeout, or nonzero rc (fail-closed: never a fake empty)."""
    try:
        p = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
             "-Command", command],
            capture_output=True, timeout=PS_TIMEOUT_S)
    except (OSError, subprocess.TimeoutExpired):
        return False, ""
    if p.returncode != 0:
        return False, ""
    return True, p.stdout.decode("utf-8", "replace")


def parse_ps_cpu(stdout):
    """ConvertTo-Json output -> {pid: cpu_100ns}.

    Empty stdout -> {} (query ran, zero comfy processes). Junk / bad
    shape / missing keys -> None (unreadable)."""
    if stdout is None:
        return None
    s = stdout.strip()
    if not s:
        return {}
    try:
        data = json.loads(s)
    except ValueError:
        return None
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        return None
    out = {}
    for item in data:
        if not isinstance(item, dict):
            return None
        try:
            pid = int(item["ProcessId"])
            raw = int(item["KernelModeTime"]) + int(item["UserModeTime"])
        except (KeyError, TypeError, ValueError):
            return None
        out[pid] = raw
    return out


def read_cpu_face(runner=None, sleeper=None,
                  interval=DEFAULT_SAMPLE_INTERVAL_S):
    """Two PS samples with --sample-interval between -> face dict.

    status: 'ok' (both parses succeeded; delta over the pid
    intersection), 'empty' (both parses ok AND zero comfy processes =
    server down), 'unreadable' (either parse failed -- fail-closed).
    pid_change=True annotates a process set that moved between samples
    (restart / mid-sample start / shutdown)."""
    run = runner or _real_ps_runner
    sleep = sleeper or (lambda s: None)

    ok1, out1 = run(PS_COMMAND)
    sample1 = parse_ps_cpu(out1) if ok1 else None
    if sample1 is None:
        return {"status": "unreadable"}
    if interval > 0:
        sleep(interval)
    ok2, out2 = run(PS_COMMAND)
    sample2 = parse_ps_cpu(out2) if ok2 else None
    if sample2 is None:
        return {"status": "unreadable"}

    if not sample1 and not sample2:
        return {"status": "empty"}

    delta_100ns = sum(sample2.get(p, 0) - sample1.get(p, 0)
                     for p in set(sample1) | set(sample2)
                     if p in sample1 and p in sample2)
    return {
        "status": "ok",
        "delta_ms": round(delta_100ns / 10000.0, 1),
        "pids": sorted(sample2),
        "pid_change": set(sample1) != set(sample2),
    }


def _real_queue_fetcher(url, timeout):
    """Real seam: -> (status_code, body_bytes) or raises."""
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return resp.getcode(), resp.read()


def read_queue_face(base_url=DEFAULT_BASE_URL, fetcher=None,
                    timeout=QUEUE_TIMEOUT_S):
    """GET /queue -> {'status': 'ok', 'running': N, 'pending': M} or
    {'status': 'unreadable'}. Any transport/parse failure is
    unreadable (connection-refused included: the cpu face carries the
    server-down attestation, not this face)."""
    fetch = fetcher or _real_queue_fetcher
    try:
        code, body = fetch(base_url.rstrip("/") + "/queue", timeout)
    except Exception:
        return {"status": "unreadable"}
    if code != 200:
        return {"status": "unreadable"}
    try:
        data = json.loads(body.decode("utf-8", "replace"))
    except (ValueError, AttributeError):
        return {"status": "unreadable"}
    if not isinstance(data, dict):
        return {"status": "unreadable"}
    running, pending = data.get("queue_running"), data.get("queue_pending")
    if not isinstance(running, list) or not isinstance(pending, list):
        return {"status": "unreadable"}
    return {"status": "ok", "running": len(running),
            "pending": len(pending)}


def read_output_face(output_dir, recency_s=DEFAULT_OUTPUT_RECENCY_S,
                    now=None):
    """Scan the ComfyUI output tree top level for fresh entries
    (tech#136 wave-gap attestation).

    Directory entries count too: creating a file inside a subdirectory
    bumps that subdirectory's own mtime (live evidence: the KF batch
    writes output/kf_bma/*.png while output/*.png stays cold), so the
    dir mtimes carry the wave signal. Only the TOP level is scanned --
    a 288-file output dir stays a ~300-entry scandir, no rglob blowup.

    -> {'status': 'ok', 'recent': N, 'newest_age_s': X} with
    newest_age_s=None when the tree is empty/cold; {'status':
    'unreadable'} when the dir is missing/unscannable (other-lane
    installs / fresh machines). Missing dir is NOT an error for the
    verdict -- the face only ever adds an active attestation."""
    if not output_dir:
        return {"status": "unreadable"}
    now_dt = now or datetime.datetime.now()
    try:
        entries = list(os.scandir(str(output_dir)))
    except (OSError, TypeError, ValueError):
        return {"status": "unreadable"}
    recent = 0
    newest_age = None
    for entry in entries:
        try:
            mtime = entry.stat().st_mtime
        except OSError:
            continue
        age = max(0.0, now_dt.timestamp() - mtime)
        if newest_age is None or age < newest_age:
            newest_age = age
        if age <= recency_s:
            recent += 1
    return {"status": "ok", "recent": recent,
            "newest_age_s": (round(newest_age, 1)
                             if newest_age is not None else None)}


def compute_verdict(queue_face, cpu_face,
                    cpu_threshold_ms=DEFAULT_CPU_THRESHOLD_MS,
                    stale_threshold_ms=DEFAULT_STALE_THRESHOLD_MS,
                    output_face=None):
    """Pure core: faces -> (verdict, notes).

    verdict 'active'/'quiet'/None (None = error path). Positive
    attestations stand on a single readable face; quiet requires
    coherent readable idle on the cpu face (the server process is the
    only thing that can render -- 'empty' attests server-down and
    overrides an unreadable queue face). The output face (tech#136)
    can only ADD an active attestation (fresh output entries = the
    client iteration loop is alive in a wave gap); an unreadable or
    cold output face never forces quiet and never blocks the
    two-face quiet path."""
    notes = []

    q_ok = queue_face.get("status") == "ok"
    if q_ok and (queue_face.get("running", 0) > 0
                 or queue_face.get("pending", 0) > 0):
        if (cpu_face.get("status") == "ok"
                and cpu_face.get("delta_ms") is not None
                and queue_face.get("running", 0) > 0
                and cpu_face["delta_ms"] < stale_threshold_ms):
            notes.append("stale-render-candidate")
        return "active", notes

    if (cpu_face.get("status") == "ok"
            and cpu_face.get("delta_ms") is not None
            and cpu_face["delta_ms"] >= cpu_threshold_ms):
        return "active", notes

    if (output_face and output_face.get("status") == "ok"
            and output_face.get("recent", 0) > 0):
        notes.append("wave-gap-recent-output")
        return "active", notes

    if cpu_face.get("status") == "empty":
        notes.append("server-down")
        return "quiet", notes

    if (cpu_face.get("status") == "ok"
            and cpu_face.get("delta_ms") is not None
            and cpu_face["delta_ms"] < cpu_threshold_ms
            and q_ok and queue_face.get("running", 0) == 0
            and queue_face.get("pending", 0) == 0):
        return "quiet", notes

    return None, notes


def run_probe(base_url=DEFAULT_BASE_URL,
              sample_interval=DEFAULT_SAMPLE_INTERVAL_S,
              cpu_threshold_ms=DEFAULT_CPU_THRESHOLD_MS,
              stale_threshold_ms=DEFAULT_STALE_THRESHOLD_MS,
              queue_fetcher=None, ps_runner=None, sleeper=None,
              now=None, output_dir=None,
              output_recency_s=DEFAULT_OUTPUT_RECENCY_S):
    """Compose the faces + verdict -> result dict (probe/ts/verdict/
    rc/thresholds/faces). Seams: queue_fetcher/ps_runner/sleeper;
    output_dir=None (default) skips the wave-gap face entirely (no
    filesystem touch -- hermetic for tests; the CLI passes the real
    default dir explicitly)."""
    now_dt = now or datetime.datetime.now()
    faces = {
        "queue": read_queue_face(base_url, fetcher=queue_fetcher),
        "cpu": read_cpu_face(runner=ps_runner, sleeper=sleeper,
                             interval=sample_interval),
    }
    if output_dir is not None:
        faces["output"] = read_output_face(output_dir,
                                           recency_s=output_recency_s,
                                           now=now_dt)
    verdict, notes = compute_verdict(faces["queue"], faces["cpu"],
                                     cpu_threshold_ms, stale_threshold_ms,
                                     faces.get("output"))
    if verdict == "active":
        rc = RC_ACTIVE
    elif verdict == "quiet":
        rc = RC_QUIET
    else:
        rc = RC_ERROR
    return {
        "probe": "comfy_activity",
        "ts": now_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "verdict": verdict,
        "rc": rc,
        "sample_interval_s": sample_interval,
        "cpu_threshold_ms": cpu_threshold_ms,
        "stale_threshold_ms": stale_threshold_ms,
        "notes": notes,
        "faces": faces,
    }


def append_ledger_row(path, result):
    """Best-effort JSONL append (tech#52/#86 family): one row per
    probe run. Error runs (rc 2, verdict None) still land their row
    -- fail-closed is data. WARN on write failure, never raises, never
    changes the exit code."""
    qf = result["faces"].get("queue", {})
    cf = result["faces"].get("cpu", {})
    of = result["faces"].get("output", {})
    row = {
        "ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "verdict": result["verdict"],
        "rc": result["rc"],
        "running": qf.get("running") if qf.get("status") == "ok" else None,
        "pending": qf.get("pending") if qf.get("status") == "ok" else None,
        "cpu_delta_ms": cf.get("delta_ms") if cf.get("status") == "ok" else None,
        "pids": cf.get("pids") if cf.get("status") in ("ok",) else [],
        "output_recent": of.get("recent") if of.get("status") == "ok" else None,
    }
    try:
        ledger_path = Path(path)
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with open(ledger_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=True) + "\n")
    except OSError as exc:
        sys.stderr.write("WARN comfy-activity-ledger append failed: %s\n" % exc)


def _face_json(face):
    out = dict(face)
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="ComfyUI lane activity probe (tech#106): queue + "
                    "process-CPU-delta attestation for the fire-GO "
                    "consumption law. rc 0=quiet, 1=active, 2=error.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL,
                        help="ComfyUI API base (default %s)" % DEFAULT_BASE_URL)
    parser.add_argument("--sample-interval", type=float,
                        default=DEFAULT_SAMPLE_INTERVAL_S,
                        help="seconds between the two CPU-time samples "
                             "(default %.0f)" % DEFAULT_SAMPLE_INTERVAL_S)
    parser.add_argument("--cpu-threshold-ms", type=float,
                        default=DEFAULT_CPU_THRESHOLD_MS,
                        help="cpu delta at/over this = server computing "
                             "(default %.0fms)" % DEFAULT_CPU_THRESHOLD_MS)
    parser.add_argument("--stale-threshold-ms", type=float,
                        default=DEFAULT_STALE_THRESHOLD_MS,
                        help="queue running>0 with cpu delta under this = "
                             "stale-render candidate note (default "
                             "%.0fms)" % DEFAULT_STALE_THRESHOLD_MS)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR),
                        help="ComfyUI output tree for the wave-gap face "
                             "(tech#136; empty string disables the face). "
                             "Default: %s" % DEFAULT_OUTPUT_DIR)
    parser.add_argument("--output-recency-s", type=float,
                        default=DEFAULT_OUTPUT_RECENCY_S,
                        help="output entries fresher than this many "
                             "seconds attest a live iteration loop "
                             "(default %.0fs)" % DEFAULT_OUTPUT_RECENCY_S)
    parser.add_argument("--json", action="store_true",
                        help="single machine-readable line")
    parser.add_argument("--ledger", nargs="?", const=str(DEFAULT_LEDGER),
                        default=None,
                        help="append one JSONL row per probe run (tech#52 "
                             "family; bare --ledger = default %s)"
                             % DEFAULT_LEDGER)
    args = parser.parse_args(argv)

    if args.sample_interval < 0:
        sys.stderr.write("bad --sample-interval (must be >= 0)\n")
        return 2
    if args.output_recency_s < 0:
        sys.stderr.write("bad --output-recency-s (must be >= 0)\n")
        return 2

    result = run_probe(base_url=args.base_url,
                       sample_interval=args.sample_interval,
                       cpu_threshold_ms=args.cpu_threshold_ms,
                       stale_threshold_ms=args.stale_threshold_ms,
                       output_dir=(args.output_dir or None),
                       output_recency_s=args.output_recency_s)
    if args.ledger:
        append_ledger_row(args.ledger, result)

    if args.json:
        payload = dict(result)
        payload["faces"] = {n: _face_json(f)
                            for n, f in result["faces"].items()}
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print("comfy_activity %s: verdict=%s rc=%d" % (
            result["ts"], result["verdict"], result["rc"]))
        qf, cf = result["faces"]["queue"], result["faces"]["cpu"]
        if qf["status"] == "ok":
            print("  queue: running=%d pending=%d" % (
                qf["running"], qf["pending"]))
        else:
            print("  queue: %s" % qf["status"])
        if cf["status"] == "ok":
            print("  cpu: delta=%.1fms pids=%s interval=%.0fs%s" % (
                cf["delta_ms"], cf["pids"], args.sample_interval,
                " (pid-set changed)" if cf.get("pid_change") else ""))
        else:
            print("  cpu: %s" % cf["status"])
        of = result["faces"].get("output")
        if of is None:
            print("  output: face-disabled")
        elif of["status"] == "ok":
            print("  output: recent=%d (recency %.0fs) newest_age=%s" % (
                of["recent"], args.output_recency_s,
                "n/a" if of["newest_age_s"] is None
                else "%.0fs" % of["newest_age_s"]))
        else:
            print("  output: %s" % of["status"])
        for n in result["notes"]:
            print("  note: %s" % n)
        if result["verdict"] == "quiet":
            print("judgment law (R1986): lane idle -- a fire GO may be "
                  "consumed once the hardware gate agrees; an idle "
                  "server may still hold VRAM residency")
        elif result["verdict"] == "active":
            print("judgment law (R1986): wave in flight / queued -- do "
                  "NOT consume a fire GO (window-flip risk)")
        else:
            print("fail-closed: no coherent attestation -- a missing "
                  "reading must never read as quiet")
    return result["rc"]


if __name__ == "__main__":
    sys.exit(main())
