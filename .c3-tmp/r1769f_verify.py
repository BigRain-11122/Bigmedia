"""R1769f: verify qwen3.5:9b-16k context actually exceeds 4096 via /v1."""
import json
import time
import urllib.request

BASE = "http://127.0.0.1:11434/v1/chat/completions"
payload = {
    "model": "qwen3.5:9b-16k",
    "messages": [{"role": "user", "content": "List the numbers 1 to 1600, one per line."}],
    "max_tokens": 5000,
    "temperature": 0,
}
req = urllib.request.Request(
    BASE, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}
)
t0 = time.time()
with urllib.request.urlopen(req, timeout=300) as r:
    out = json.loads(r.read().decode())
ch = out["choices"][0]
u = out["usage"]
print(f"finish={ch['finish_reason']} {time.time()-t0:.0f}s total={u['total_tokens']} "
      f"prompt={u['prompt_tokens']} completion={u['completion_tokens']} "
      f"reasoning_chars={len(ch['message'].get('reasoning') or '')} "
      f"content_lines={ch['message']['content'].count(chr(10))+1}")
print("VERDICT:", "CTX>4096 OK" if u["completion_tokens"] > 4046 else "STILL CAPPED 4096")
