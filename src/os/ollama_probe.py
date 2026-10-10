# -*- coding: utf-8 -*-
"""Fixed ollama generation probe (tech#41 recovery criterion; tech#51, R1881;
tech#52 --ledger JSONL evidence face, R1883).

Recovery criterion for a saturated ollama server (F-20261010-03 family):
generate-probe only. Two trap families this probe permanently retires:

1. /api/tags stays 200 under saturation (R1877 trap) -> never a signal.
2. PS 5.1 inline JSON loses its quotes through the shell wrapper ->
   ollama answers 400 Bad Request (R1880 operation red). That 400 was a
   TRANSPORT ARTIFACT, not a server signal. This probe builds the body with
   json.dumps inside Python (no shell quoting surface), so a 400 observed
   through it is genuine server-side rejection and stays classified rc=2.

Exit codes:
  0 = generation returned 200 (recovered)
  1 = saturated (503 / 'maximum pending requests exceeded')
  2 = other transport/server error (ambiguous, raw status surfaced)

Usage:
  python src/os/ollama_probe.py [--model M] [--timeout S] [--base-url URL] [--json] [--ledger [PATH]]

The per-round recovery check (tech#41) uses this fixed probe; ad-hoc rewrites
are retired. --json emits one machine-readable line for evidence files.

--ledger (tech#52, R1883) appends one JSONL row (ts/rc/status/http_status/
model) per real probe flight to the given path (bare --ledger = default
data/pipeline/ollama-probe-ledger.jsonl). Opt-in only: without the flag the
existing call surface is untouched. Best-effort (whisper-ledger tech#19
pattern): a failed append WARNs on stderr and never changes the exit code.
No probe flight (bad timeout) -> no row.

Rows also carry gpu_util/gpu_mem context columns (tech#54, R1888): a
best-effort nvidia-smi CSV read so a saturation row shows whether the GPU
was actually generating at probe time (the R1883-R1885 wedged-slot case was
only diagnosable by hand because 503 rows carried no GPU context). Any
read failure -> "NONE" markers; never raises, never changes the exit code.

tech#55 (R1889): advisory `face` column -- the three-face reading discipline
for probe rows consumed by GPU-window scheduling decisions (gap anchor:
the R1888 10:59 flight read rc2 timeout during a 100%/11348MiB generation
window; without a face label that is one manual misread away from
"service broken"). Faces, advisory only, rc semantics never move:
  rc=0                    -> ok
  503 + GPU idle (<80%)   -> slot-wedged      (queue wedged, R1883-85 family)
  503 + GPU busy (>=80%)   -> saturated-busy   (genuine queue-full, generating)
  timeout + GPU busy      -> busy-contended   (server healthy, slow under load: YIELD, not broken)
  timeout + GPU idle + gpu_mem < 4000MiB
                          -> cold-reload      (no ollama model resident: the probe itself started
                                               a cold load that outran the request cap; service
                                               may still be healthy -- tech#56, R1889 11:28:48
                                               anchor rc2/gpu_mem=2012 13 min after a clean GEN-OK)
  timeout + GPU idle (model resident)
                          -> service-anomaly  (genuine service trouble face)
  rc=2 non-timeout        -> error
  GPU context unavailable -> gpu-ctx-none
GPU busy threshold util>=80 aligns with the tech#44 defer threshold. The
face lands on the --json line, the human line (non-ok) and every --ledger
row, so window judgments read the discipline straight off the evidence.

tech#56 (R1890): cold-reload face. The 4000MiB residency line sits below
the smallest ollama model we probe (qwen2.5:7b needs ~4.7GB VRAM), so a
timeout row with gpu_mem under the line means no model was resident at
probe time -- the probe itself triggered the cold load and the 60s cap
expired mid-load. That is a scheduling fact (wait for residency), not a
service fault; mislabeling it service-anomaly invites a pointless service
restart. Unreadable mem stays the conservative anomaly face.
"""

import argparse
import datetime
import json
import socket
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_MODEL = "qwen2.5:14b-8k"
DEFAULT_TIMEOUT = 60
DEFAULT_BASE_URL = "http://localhost:11434"
GEN_PATH = "/api/generate"
DEFAULT_LEDGER = Path(__file__).resolve().parents[2] / "data" / "pipeline" / "ollama-probe-ledger.jsonl"


def build_request_body(model):
    """Build the JSON request body as bytes (no shell-quoting surface)."""
    return json.dumps({"model": model, "prompt": "hi", "stream": False}).encode("utf-8")


def _http_post(base_url, body, timeout):
    """Single injection seam for tests: real call is urllib, never inline PS."""
    req = urllib.request.Request(
        base_url.rstrip("/") + GEN_PATH,
        data=body,
        headers={"Content-Type": "application/json"},
    )
    return urllib.request.urlopen(req, timeout=timeout)


def classify(http_status, detail):
    """Pure classifier: 503 or the saturation message -> 1, else 2."""
    if http_status == 503 or "maximum pending requests" in (detail or ""):
        return 1
    return 2


def _is_timeout(exc):
    """True when the transport exception family is a timeout (tech#55).

    urllib surfaces request timeouts either as a bare TimeoutError/
    socket.timeout, or wrapped as URLError(reason=...). Pure substring
    fallback on the rendered message keeps exotic wrappers honest.
    """
    if isinstance(exc, (TimeoutError, socket.timeout)):
        return True
    reason = getattr(exc, "reason", None)
    if reason is not None:
        if isinstance(reason, (TimeoutError, socket.timeout)):
            return True
        if "timed out" in str(reason).lower():
            return True
    return "timed out" in str(exc).lower()


FACE_GPU_BUSY_UTIL = 80  # tech#44 defer threshold
# tech#56: below this much VRAM in use no probed ollama model can be
# resident (the smallest we run, qwen2.5:7b, needs ~4.7GB), so a timeout
# with gpu_mem under the line means the probe itself started a cold load.
FACE_COLD_RELOAD_VRAM_MB = 4000


def compute_face(result, gpu_ctx):
    """Advisory face reading (tech#55 + tech#56). Never moves rc semantics.

    Faces: ok / slot-wedged / saturated-busy / busy-contended /
    cold-reload / service-anomaly / error / gpu-ctx-none (see module
    docstring).
    """
    rc = result.get("rc")
    if rc == 0:
        return "ok"
    util = (gpu_ctx or {}).get("gpu_util", "NONE")
    try:
        busy = int(util) >= FACE_GPU_BUSY_UTIL
    except (TypeError, ValueError):
        return "gpu-ctx-none"
    if rc == 1:
        return "saturated-busy" if busy else "slot-wedged"
    if rc == 2 and result.get("timeout"):
        if busy:
            return "busy-contended"
        # tech#56 cold-reload face: timeout + GPU idle + no model resident
        # (gpu_mem below the smallest model's footprint) = the probe itself
        # triggered a cold load that outran the request cap; the service can
        # still be healthy (R1889 11:28:48 anchor: rc2/gpu_mem=2012, 13 min
        # after a clean GEN-OK). Unreadable mem -> conservative anomaly.
        mem = (gpu_ctx or {}).get("gpu_mem", "NONE")
        try:
            return "cold-reload" if int(mem) < FACE_COLD_RELOAD_VRAM_MB else "service-anomaly"
        except (TypeError, ValueError):
            return "service-anomaly"
    return "error"


def run_probe(model=DEFAULT_MODEL, timeout=DEFAULT_TIMEOUT, base_url=DEFAULT_BASE_URL):
    """Run one generate probe. Returns a dict result; never raises."""
    result = {
        "rc": 2,
        "status": "error",
        "http_status": None,
        "detail": "",
        "model": model,
        "base_url": base_url,
        "timeout": False,
    }
    body = build_request_body(model)
    try:
        with _http_post(base_url, body, timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8", "replace"))
        result["rc"] = 0
        result["status"] = "ok"
        result["detail"] = str(payload.get("done_reason", ""))
    except urllib.error.HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8", "replace")[:300]
        except Exception:
            detail = ""
        result["http_status"] = exc.code
        result["detail"] = detail.replace("\n", " ")
        result["rc"] = classify(exc.code, detail)
        result["status"] = "saturated" if result["rc"] == 1 else "error"
    except Exception as exc:  # transport-level (connection refused, timeout, ...)
        result["detail"] = repr(exc)[:300]
        result["timeout"] = _is_timeout(exc)
        result["status"] = "error"
    return result


def _human_line(result):
    face = " face=%s" % result["face"] if result.get("face") and result["rc"] != 0 else ""
    if result["status"] == "ok":
        return "GEN-OK done_reason=%s model=%s" % (result["detail"], result["model"])
    if result["status"] == "saturated":
        return "GEN-SATURATED status=%s detail=%s%s" % (
            result["http_status"], result["detail"], face)
    if result["http_status"] is not None:
        return "GEN-ERROR status=%s detail=%s%s" % (
            result["http_status"], result["detail"], face)
    return "GEN-ERROR transport=%s%s" % (result["detail"], face)


def _nvidia_smi_query():
    """Injection seam for tests: run the nvidia-smi CSV query, return stdout.

    Raises on any failure (binary missing, timeout, bad rc) - the caller
    converts every failure into NONE markers.
    """
    out = subprocess.run(
        ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used",
         "--format=csv,noheader,nounits"],
        capture_output=True, text=True, timeout=15)
    if out.returncode != 0:
        raise RuntimeError("nvidia-smi rc=%s" % out.returncode)
    return out.stdout


def read_gpu_context():
    """Best-effort GPU context for ledger rows (tech#54).

    Returns {"gpu_util": ..., "gpu_mem": ...} parsed from the first
    nvidia-smi CSV row; any failure -> "NONE" markers. Never raises.
    """
    try:
        text = _nvidia_smi_query()
        first = text.strip().splitlines()[0] if text.strip() else ""
        parts = [p.strip() for p in first.split(",")]
        if len(parts) < 2 or not parts[0] or not parts[1]:
            raise ValueError("unparseable nvidia-smi csv: %r" % first[:80])
        return {"gpu_util": parts[0], "gpu_mem": parts[1]}
    except Exception:
        return {"gpu_util": "NONE", "gpu_mem": "NONE"}


def append_ledger_row(path, result, gpu_ctx=None):
    """Best-effort JSONL append (tech#52): one row per real probe flight.

    Rows carry gpu_util/gpu_mem context columns (tech#54, R1883-R1885
    wedged-slot diagnosis gap: saturation + zero GPU activity is only
    visible when the row records GPU state at probe time) and the advisory
    face column (tech#55) so window judgments read the three-face
    discipline straight off the ledger row.

    gpu_ctx: pre-read context reused when the caller already has it (one
    nvidia-smi per probe flight, not two); None -> read here (tech#52
    call surface). WARN on failure, never raises, never changes the exit code.
    """
    gpu = gpu_ctx if gpu_ctx is not None else read_gpu_context()
    row = {
        "ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rc": result["rc"],
        "status": result["status"],
        "http_status": result["http_status"],
        "model": result["model"],
    }
    row.update(gpu)
    row["face"] = compute_face(result, gpu)
    try:
        ledger_path = Path(path)
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with open(ledger_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=True) + "\n")
    except OSError as exc:
        sys.stderr.write("WARN ollama-probe-ledger append failed: %s\n" % exc)


def build_parser(argv=None):
    parser = argparse.ArgumentParser(
        description="Ollama generation probe (recovery criterion, exit 0/1/2).")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help="model to probe (default: %s)" % DEFAULT_MODEL)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help="per-request timeout seconds (default: %d)" % DEFAULT_TIMEOUT)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL,
                        help="ollama base url (default: %s)" % DEFAULT_BASE_URL)
    parser.add_argument("--json", action="store_true",
                        help="emit one machine-readable JSON line")
    parser.add_argument("--ledger", nargs="?", const=str(DEFAULT_LEDGER), default=None,
                        help="append one JSONL row per probe flight to this path "
                             "(tech#52; bare --ledger = default %s)" % DEFAULT_LEDGER)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.timeout <= 0:
        print("GEN-ERROR bad-timeout=%s" % args.timeout)
        return 2
    result = run_probe(model=args.model, timeout=args.timeout, base_url=args.base_url)
    gpu_ctx = read_gpu_context()
    result["face"] = compute_face(result, gpu_ctx)
    if args.ledger:
        append_ledger_row(args.ledger, result, gpu_ctx)
    if args.json:
        result.update(gpu_ctx)
        result["ts"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(json.dumps(result, ensure_ascii=True))
    else:
        print(_human_line(result))
    return result["rc"]


if __name__ == "__main__":
    sys.exit(main())
