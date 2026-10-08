"""R1769d: decisive num_ctx test - completion must run past the 4096 boundary.

Short prompt (~50 tok) + max_tokens 5000:
- num_ctx honored (16384): completion can exceed 4096-50=4046.
- num_ctx ignored (default 4096): completion truncates near 4046.
"""
import json
import time
import urllib.request

BASE = "http://127.0.0.1:11434/v1/chat/completions"

for name, extra in (
    ("bare", {}),
    ("num_ctx16384", {"num_ctx": 16384}),
):
    payload = {
        "model": "qwen3.5:9b",
        "messages": [{"role": "user", "content": "List the numbers 1 to 1600, one per line."}],
        "max_tokens": 5000,
        "temperature": 0,
        **extra,
    }
    req = urllib.request.Request(
        BASE, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=300) as r:
        out = json.loads(r.read().decode())
    ch = out["choices"][0]
    u = out["usage"]
    reasoning = ch["message"].get("reasoning") or ""
    print(f"[{name}] finish={ch['finish_reason']} {time.time()-t0:.0f}s total={u['total_tokens']} "
          f"prompt={u['prompt_tokens']} completion={u['completion_tokens']} "
          f"reasoning_chars={len(reasoning)} content_lines={ch['message']['content'].count(chr(10))+1}")
