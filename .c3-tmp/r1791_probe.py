# R1791 three-gate pre-check pass 3: file trees + recency for candidate repos
import json, sys, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))

for rid in ["Comfy-Org/Qwen-Image-2.1", "unsloth/Qwen-Image-2.1-GGUF", "unsloth/Qwen-Image-2512-GGUF", "Qwen/Qwen-Image-2512"]:
    try:
        m = get("https://hf-mirror.com/api/models/" + rid)
        print("== %s | dl=%s likes=%s | mod=%s | tags=%s" % (rid, m.get("downloads"), m.get("likes"), str(m.get("lastModified"))[:19], ",".join((m.get("tags") or [])[:8])))
        try:
            tree = get("https://hf-mirror.com/api/models/%s/tree/main?recursive=true" % rid)
            big = [f for f in tree if f.get("type") == "file" and (f.get("size") or 0) > 80*1024*1024]
            print("   files>80MB: %d (total tree files %d)" % (len(big), len(tree)))
            for f in sorted(big, key=lambda x: -(x.get("size") or 0))[:28]:
                print("   %9.2fGB  %s" % ((f.get("size") or 0)/1e9, f.get("path")))
        except Exception as e:
            print("   TREE FAIL:", str(e)[:80])
    except Exception as e:
        print("== %s FAIL: %s" % (rid, str(e)[:80]))
