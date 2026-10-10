# -*- coding: utf-8 -*-
"""Fixed ollama generation probe (tech#41 recovery criterion; tech#51, R1881).

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
  python src/os/ollama_probe.py [--model M] [--timeout S] [--base-url URL] [--json]

The per-round recovery check (tech#41) uses this fixed probe; ad-hoc rewrites
are retired. --json emits one machine-readable line for evidence files.
"""

import argparse
import datetime
import json
import sys
import urllib.error
import urllib.request

DEFAULT_MODEL = "qwen2.5:14b-8k"
DEFAULT_TIMEOUT = 60
DEFAULT_BASE_URL = "http://localhost:11434"
GEN_PATH = "/api/generate"


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
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.timeout <= 0:
        print("GEN-ERROR bad-timeout=%s" % args.timeout)
        return 2
    result = run_probe(model=args.model, timeout=args.timeout, base_url=args.base_url)
    if args.json:
        result["ts"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(json.dumps(result, ensure_ascii=True))
    else:
        print(_human_line(result))
    return result["rc"]


if __name__ == "__main__":
    sys.exit(main())
