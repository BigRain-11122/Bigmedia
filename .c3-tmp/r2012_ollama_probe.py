# -*- coding: utf-8 -*-
"""R2012 ollama minimal generation probe (R1886 GEN-OK family)."""
import json, time, urllib.request, sys

BASE = "http://localhost:11434"


def probe(model, timeout_s=120):
    body = json.dumps({
        "model": model,
        "prompt": "Say OK.",
        "stream": False,
        "options": {"num_predict": 8},
    }).encode("utf-8")
    req = urllib.request.Request(BASE + "/api/generate", data=body,
                                headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        r = urllib.request.urlopen(req, timeout=timeout_s)
        d = json.load(r)
        dt = time.time() - t0
        done = d.get("done", False)
        text = (d.get("response") or "")[:40].replace("\n", " ")
        print("GEN model=%s rc=OK %.1fs done=%s text=%r" % (model, dt, done, text))
        return True
    except urllib.error.HTTPError as e:
        print("GEN model=%s HTTP %d %s" % (model, e.code, e.read()[:120]))
        return False
    except Exception as e:
        print("GEN model=%s FAIL %.1fs %r" % (model, time.time() - t0, e))
        return False


if __name__ == "__main__":
    ok14 = probe("qwen2.5:14b-8k", 150)
    ok7 = probe("qwen2.5:7b-instruct", 90)
    print("PROBE-SUMMARY 14b=%s 7b=%s" % (ok14, ok7))
    sys.exit(0 if (ok14 or ok7) else 1)
