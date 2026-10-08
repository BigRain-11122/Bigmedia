# MD-0001 gate re-roll iteration 3 (R1790) - best-of-N sweep for 3 residual FAILs
# SDXL base draft-tier weak on fine-feature control -> generate N=3 candidates per shot,
# pick winners via multimodal gate read. Candidates to reroll3-candidates/, frames/ untouched.
import json, os, sys, time, subprocess, urllib.request, urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.join(BASE, "reroll3-candidates")
COMFY = r"C:\Agent\ComfyUI"
CPY = os.path.join(COMFY, ".venv", "Scripts", "python.exe")
HOST, PORT = "127.0.0.1", 8188
DETACHED = 0x00000008 | 0x00000200 | 0x08000000

LOG = open(os.path.join(BASE, "reroll3-r1790.log"), "a", encoding="utf-8", errors="replace")
def log(m):
    LOG.write(time.strftime("%Y-%m-%d %H:%M:%S ") + m + "\n"); LOG.flush()

def http(path, data=None, timeout=180, raw=False):
    url = "http://%s:%d%s" % (HOST, PORT, path)
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        b = r.read()
        return b if raw else json.loads(b.decode() or "{}")

def alive():
    try:
        http("/system_stats", timeout=5); return True
    except Exception:
        return False

STYLE = "stylized flat 2D digital illustration, silicon city world, muted desaturated palette, cinematic night atmosphere, clean bold shapes, flat colors, game-art aesthetic"
NEGB = "photorealistic, photo, 3d render, text, letters, chinese characters, numbers, watermark, signature, logo, blurry, low quality, deformed, oversaturated"

JOBS = [
 dict(id=3, seeds=[41043, 41044, 41045],
   pos="close side view of an old cast-iron street lamp head at night, its wide round lampshade occupying the center of the frame, a large dark square metal patch visibly TILTED about fifteen degrees welded onto the side of the lampshade, covering one quarter of the lampshade surface, rough weld seams outlining the patch, rivets and scratches, the tilted patch is the main subject, warm light glowing from the lamp, rain droplets",
   neg="full street scene, entire lamp post, pole only, clean lampshade without patch, depth of field, bokeh"),
 dict(id=10, seeds=[19019, 19021, 19023],
   pos="big close-up portrait of a chubby round pixel-art cat spirit's face filling most of the frame, white-and-grey fur made of soft square pixel blocks, two pointed ears with a small triangular piece missing from the edge of its left ear like a notch cut, two big round innocent eyes wide open looking straight at the camera, one small front paw raised up to its mouth as if licking the paw, soft warm indoor light, plain cozy background",
   neg="closed eyes, sleeping, no ears, human, city skyline, landscape, dark fur, slim body, extra limbs"),
 dict(id=11, seeds=[19019, 19025, 19029],
   pos="overhead top-down view of a cozy wooden breakfast table in warm morning light, a chubby white-and-grey pixel-art cat spirit with chunky square pixel body sits in the center of the table leaning its head down eating from a small plate in front of it, its tail with a thin radio antenna on the tip visibly sticking up beside its round body, several small colorful breakfast plates arranged around the table, homey warm mood",
   neg="no cat, empty table, smooth vector style, dark fur, black cat, slim body, food only, one plate only"),
]

def build_wf(pos, neg, seed, sid):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": STYLE + ", " + pos, "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": NEGB + ", " + neg, "clip": ["1", 1]}},
        "4": {"class_type": "EmptyLatentImage", "inputs": {"width": 1216, "height": 683, "batch_size": 1}},
        "5": {"class_type": "KSampler", "inputs": {"seed": seed, "steps": 30, "cfg": 6.5,
                "sampler_name": "dpmpp_2m", "scheduler": "karras", "denoise": 1.0,
                "model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0], "latent_image": ["4", 0]}},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"filename_prefix": "md0001_cand_shot%02d" % sid, "images": ["6", 0]}},
    }

def fetch_image(out_entry, dest):
    q = urllib.parse.urlencode({"filename": out_entry["filename"], "subfolder": out_entry.get("subfolder", ""), "type": out_entry.get("type", "output")})
    b = http("/view?" + q, timeout=120, raw=True)
    with open(dest, "wb") as f:
        f.write(b)
    return os.path.getsize(dest)

def main():
    os.makedirs(CAND, exist_ok=True)
    log("REROLL3-START best-of-3 x 3 shots")
    import torch
    free_gb = torch.cuda.mem_get_info()[0] / (1024 ** 3)
    log("VRAM-GUARD free=%.2fGB" % free_gb)
    if free_gb < 4.5:
        log("VRAM-GUARD FAIL - defer (exit 2)"); return 2

    server = None; started_here = False
    if alive():
        log("SERVER-ALREADY-UP - reuse")
    else:
        slog = open(os.path.join(BASE, "server-r1790.log"), "a", encoding="utf-8", errors="replace")
        server = subprocess.Popen([CPY, "main.py", "--listen", "127.0.0.1", "--port", str(PORT),
                                   "--lowvram", "--disable-auto-launch", "--preview-method", "none"],
                                  cwd=COMFY, stdout=slog, stderr=subprocess.STDOUT, creationflags=DETACHED)
        started_here = True
        t0 = time.time()
        while time.time() - t0 < 300:
            if server.poll() is not None:
                log("SERVER-DIED-EARLY rc=%d" % server.returncode); return 3
            if alive():
                log("SERVER-READY in %.0fs" % (time.time() - t0)); break
            time.sleep(3)
        else:
            log("SERVER-TIMEOUT"); return 3

    ok = 0; total = 0; results = []
    for job in JOBS:
        for seed in job["seeds"]:
            total += 1
            dest = os.path.join(CAND, "shot%02d_s%d.png" % (job["id"], seed))
            t0 = time.time()
            try:
                r = http("/prompt", {"prompt": build_wf(job["pos"], job["neg"], seed, job["id"]), "client_id": "md0001-reroll3"}, timeout=60)
                pid = r.get("prompt_id")
                if not pid:
                    results.append({"id": job["id"], "seed": seed, "state": "FAIL", "err": "no pid"}); continue
                done = False
                while time.time() - t0 < 1200:
                    time.sleep(3)
                    e = http("/history/" + pid, timeout=30).get(pid)
                    if e and e.get("status", {}).get("completed"):
                        if e["status"].get("status_str") == "error":
                            results.append({"id": job["id"], "seed": seed, "state": "FAIL", "err": "exec"}); done = True; break
                        imgs = []
                        for node in e.get("outputs", {}).values():
                            imgs.extend(node.get("images", []))
                        if not imgs:
                            results.append({"id": job["id"], "seed": seed, "state": "FAIL", "err": "no img"}); done = True; break
                        sz = fetch_image(imgs[0], dest)
                        ok += 1
                        results.append({"id": job["id"], "seed": seed, "state": "OK", "bytes": sz, "secs": round(time.time() - t0, 1)})
                        log("CAND shot%02d s%d OK %dB in %.0fs" % (job["id"], seed, sz, time.time() - t0))
                        done = True; break
                if not done:
                    results.append({"id": job["id"], "seed": seed, "state": "FAIL", "err": "timeout"})
            except Exception as ex:
                results.append({"id": job["id"], "seed": seed, "state": "FAIL", "err": str(ex)[:150]})
                log("CAND shot%02d s%d FAIL %s" % (job["id"], seed, str(ex)[:100]))

    if started_here and server is not None:
        try:
            server.terminate()
            try:
                server.wait(timeout=20)
            except Exception:
                server.kill(); server.wait(timeout=20)
            log("SERVER-STOPPED")
        except Exception as ex:
            log("SERVER-STOP exc=%s" % str(ex)[:120])
    json.dump({"state": "DONE" if ok == total else "PARTIAL", "ok": ok, "total": total, "results": results,
               "ts": time.strftime("%Y-%m-%d %H:%M:%S")},
              open(os.path.join(BASE, "reroll3-r1790-status.json"), "w"))
    log("SUMMARY ok=%d/%d" % (ok, total))
    return 0 if ok == total else 1

if __name__ == "__main__":
    try:
        rc = main()
    except Exception as ex:
        log("FATAL %s" % str(ex)[:300]); rc = 4
    log("REROLL3-END rc=%d" % rc)
    sys.exit(rc)
