"""R1880 ollama generation probe (tech#41 criteria).

Generate-probe only: /api/tags stays 200 under saturation (R1877 trap) and
therefore must never be used as the recovery signal. Exit codes:
  0 = generation returned 200 (recovered)
  1 = saturated (503 / 'maximum pending requests exceeded')
  2 = other transport/server error (ambiguous, surface raw status)
"""
import json
import sys
import urllib.error
import urllib.request

BODY = json.dumps({"model": "qwen2.5:14b-8k", "prompt": "hi", "stream": False}).encode()
REQ = urllib.request.Request(
    "http://localhost:11434/api/generate",
    data=BODY,
    headers={"Content-Type": "application/json"},
)

try:
    with urllib.request.urlopen(REQ, timeout=60) as resp:
        payload = json.loads(resp.read().decode("utf-8", "replace"))
    print("GEN-OK done_reason=%s" % payload.get("done_reason"))
    sys.exit(0)
except urllib.error.HTTPError as exc:
    try:
        detail = exc.read().decode("utf-8", "replace")[:300]
    except Exception:
        detail = ""
    print("GEN-FAIL status=%s detail=%s" % (exc.code, detail.replace("\n", " ")))
    if exc.code == 503 or "maximum pending requests" in detail:
        sys.exit(1)
    sys.exit(2)
except Exception as exc:  # transport-level
    print("GEN-FAIL transport=%r" % (exc,))
    sys.exit(2)
