# R1791 probe pass 5: exact bytes + HEAD URL verification for the 3 native-quant files
import json, sys, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))

tree = get("https://hf-mirror.com/api/models/Comfy-Org/Qwen-Image-2.1/tree/main?recursive=true")
picks = ["diffusion_models/qwen_image_2.1_int8_convrot.safetensors",
         "text_encoders/qwen3vl_8b_w4a8.safetensors",
         "vae/qwen_image_2.1_vae_bf16.safetensors"]
sizes = {}
for f in tree:
    if f.get("path") in picks:
        sizes[f["path"]] = f.get("size")

total = 0
for p in picks:
    exp = sizes.get(p)
    print("%s = %s bytes" % (p, exp))
    if exp is None:
        print("MISSING in tree!"); sys.exit(1)
    total += exp
    url = "https://hf-mirror.com/Comfy-Org/Qwen-Image-2.1/resolve/main/" + p
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            cl = r.headers.get("Content-Length")
            ar = r.headers.get("Accept-Ranges")
            print("  HEAD %s len=%s accept-ranges=%s" % (r.status, cl, ar))
            if int(cl or 0) != exp:
                print("  SIZE-MISMATCH head=%s tree=%s" % (cl, exp))
    except Exception as e:
        print("  HEAD FAIL:", str(e)[:80])
print("TOTAL = %d bytes (%.2f GB)" % (total, total/1e9))
