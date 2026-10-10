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
"""

import argparse
import datetime
import json
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


def run_probe(model=DEFAULT_MODEL, timeout=DEFAULT_TIMEOUT, base_url=DEFAULT_BASE_URL):
    """Run one generate probe. Returns a dict result; never raises."""
    result = {
        "rc": 2,
        "status": "error",
        "http_status": None,
        "detail": "",
        "model": model,
        "base_url": base_url,
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
        result["status"] = "error"
    return result


def _human_line(result):
    if result["status"] == "ok":
        return "GEN-OK done_reason=%s model=%s" % (result["detail"], result["model"])
    if result["status"] == "saturated":
        return "GEN-SATURATED status=%s detail=%s" % (
            result["http_status"], result["detail"])
    if result["http_status"] is not None:
        return "GEN-ERROR status=%s detail=%s" % (
            result["http_status"], result["detail"])
    return "GEN-ERROR transport=%s" % result["detail"]


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


def append_ledger_row(path, result):
    """Best-effort JSONL append (tech#52): one row per real probe flight.

    Rows carry gpu_util/gpu_mem context columns (tech#54, R1883-R1885
    wedged-slot diagnosis gap: saturation + zero GPU activity is only
    visible when the row records GPU state at probe time).

    WARN on failure, never raises, never changes the probe exit code.
    """
    row = {
        "ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rc": result["rc"],
        "status": result["status"],
        "http_status": result["http_status"],
        "model": result["model"],
    }
    row.update(read_gpu_context())
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
    if args.ledger:
        append_ledger_row(args.ledger, result)
    if args.json:
        result["ts"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(json.dumps(result, ensure_ascii=True))
    else:
        print(_human_line(result))
    return result["rc"]


if __name__ == "__main__":
    sys.exit(main())
