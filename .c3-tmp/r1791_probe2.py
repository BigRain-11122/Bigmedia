# R1791 probe pass 4: text-encoder GGUF availability + ComfyUI-GGUF node health
import json, sys, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))

for rid in ["pottokao/Qwen-Image-2.1-Text-Encoder-Heretic-GGUF", "unsloth/Qwen-Image-2.1-Text-Encoder-GGUF", "city96/Qwen3-VL-8B-GGUF"]:
    try:
        m = get("https://hf-mirror.com/api/models/" + rid)
        print("== %s | dl=%s | mod=%s" % (rid, m.get("downloads"), str(m.get("lastModified"))[:19]))
        tree = get("https://hf-mirror.com/api/models/%s/tree/main?recursive=true" % rid)
        for f in tree:
            if f.get("type") == "file" and (f.get("size") or 0) > 80*1024*1024:
                print("   %8.2fGB  %s" % ((f.get("size") or 0)/1e9, f.get("path")))
    except Exception as e:
        print("== %s FAIL: %s" % (rid, str(e)[:60]))

# ComfyUI-GGUF custom node (canonical GGUF loader) health via GitHub API
try:
    g = get("https://api.github.com/repos/city96/ComfyUI-GGUF")
    print("NODE city96/ComfyUI-GGUF | stars=%s | pushed=%s | license=%s | default_branch=%s" % (g.get("stargazers_count"), str(g.get("pushed_at"))[:19], (g.get("license") or {}).get("spdx_id"), g.get("default_branch")))
except Exception as e:
    print("NODE check FAIL:", str(e)[:80])
