"""Probe qwen3.5:9b think:false support via OpenAI-compat endpoint (R1769).

Evidence for AIHOT PoC model-slot decision: reasoning model burned output
budget (finish_reason=length, 11/11 prefilter receipts failed at 20:4x-20:5x).
Two candidate fixes from AIHOT llm.ts: LLM_EXTRA_JSON think off vs
LLM_REASONING_TOKENS headroom. This probe tests the clean path first.
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
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            out = json.loads(r.read().decode())
        return out, time.time() - t0, None
    except Exception as e:  # noqa: BLE001 - probe reports errors verbatim
        return None, time.time() - t0, str(e)


PROMPT = (
    "You are a strict JSON API. Reply with exactly this JSON object and nothing else: "
    '{"ok": true}'
)

# Test A: think disabled via extra body field (ollama native param name)
for extra in ({"think": False}, {"enable_thinking": False}):
    payload = {
        "model": "qwen3.5:9b",
        "messages": [{"role": "user", "content": PROMPT}],
        "max_tokens": 200,
        **extra,
    }
    out, dt, err = call(payload)
    if err:
        print(f"[{extra}] ERR {err} ({dt:.1f}s)")
        continue
    ch = out["choices"][0]
    content = ch["message"]["content"]
    reasoning = ch["message"].get("reasoning") or ch["message"].get("reasoning_content")
    print(f"[extra={extra}] finish={ch['finish_reason']} {dt:.1f}s")
    print(f"  content={content[:200]!r}")
    print(f"  reasoning_field={'YES len=' + str(len(reasoning)) if reasoning else 'none'}")
    print(f"  usage={out.get('usage', {})}")

# Test B: baseline no extra field, tight budget (expect the failure signature)
payload = {"model": "qwen3.5:9b", "messages": [{"role": "user", "content": PROMPT}], "max_tokens": 200}
out, dt, err = call(payload)
if err:
    print(f"[baseline] ERR {err} ({dt:.1f}s)")
else:
    ch = out["choices"][0]
    content = ch["message"]["content"]
    reasoning = ch["message"].get("reasoning") or ch["message"].get("reasoning_content")
    print(f"[baseline no-extra] finish={ch['finish_reason']} {dt:.1f}s")
    print(f"  content={content[:200]!r}")
    print(f"  reasoning_field={'YES len=' + str(len(reasoning)) if reasoning else 'none'}")
    print(f"  usage={out.get('usage', {})}")
