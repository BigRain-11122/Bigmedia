"""R1769c: test whether ollama /v1 honors num_ctx via extra body field.

Context burn evidence: receipt 21:07:55 had maxTokens=4608 (headroom applied)
but usage total_tokens=4096 (prompt 1855 + completion 2241) -> the ollama
context window (4096, per `ollama ps` CONTEXT col) truncated the response
before JSON landed. Fix candidate: num_ctx via LLM_EXTRA_JSON.
"""
import json
import time
import urllib.request

BASE = "http://127.0.0.1:11434/v1/chat/completions"


def call(payload, timeout=180):
    req = urllib.request.Request(
        BASE, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode()), time.time() - t0


# Force a long completion: ask for a long numbered list, capped by max_tokens,
# with num_ctx headroom. If num_ctx is honored, total_tokens can exceed 4096.
filler = "word " * 800  # ~1000+ prompt tokens
for name, extra in (
    ("num_ctx=16384", {"num_ctx": 16384}),
    ("num_ctx=16384+think_off", {"num_ctx": 16384, "think": False}),
):
    payload = {
        "model": "qwen3.5:9b",
        "messages": [
            {"role": "user", "content": filler + " List the numbers 1 to 900, one per line, then a line DONE."}
        ],
        "max_tokens": 2600,
        "temperature": 0,
        **extra,
    }
    try:
        out, dt = call(payload)
        ch = out["choices"][0]
        u = out["usage"]
        content_done = ch["message"]["content"].strip().endswith("DONE")
        print(f"[{name}] finish={ch['finish_reason']} {dt:.0f}s "
              f"total={u['total_tokens']} prompt={u['prompt_tokens']} "
              f"completion={u['completion_tokens']} endsDONE={content_done}")
    except Exception as e:  # noqa: BLE001
        print(f"[{name}] ERR {e}")
