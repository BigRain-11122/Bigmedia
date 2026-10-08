# MD-0001 gate re-roll iteration 2 (R1790) - 3 residual FAILs after iter-1:
#   03 lamp: patch still not the subject (full lamp drawn) -> lampshade side view, patch dominant
#   10 cat: not a cat-face close-up -> face-portrait framing, ears+eyes+paw explicit
#   11 cat: not eating, antenna missing, pixel feel lost -> lean-down eating + antenna + chunky pixels
# Same discipline: lowvram, kill-after, VRAM guard, frames-v1 archive untouched (v1 = gate evidence).
import json, os, sys, time, subprocess, urllib.request, urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.join(BASE, "frames")
COMFY = r"C:\Agent\ComfyUI"
CPY = os.path.join(COMFY, ".venv", "Scripts", "python.exe")
HOST, PORT = "127.0.0.1", 8188
DETACHED = 0x00000008 | 0x00000200 | 0x08000000

LOG = open(os.path.join(BASE, "reroll2-r1790.log"), "a", encoding="utf-8", errors="replace")
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

FIX = {
 3: dict(seed=41042,  # +1: iter-1 seed kept drawing full street-lamp scene; nudge noise
   pos="stylized flat 2D digital illustration, silicon city world, muted desaturated palette, cinematic night atmosphere, clean bold shapes, flat colors, game-art aesthetic. An old cast-iron street-lamp head seen from the side at night, its wide lampshade fills the left half of the frame, a LARGE visibly tilted square metal repair patch welded onto the side of the lampshade is the main subject of the picture, rough dark weld seams around the patch edges, rivets and scratches on the patch, strong warm light glaring from below, rain droplets, dark background",
   neg="photorealistic, photo, 3d render, text, letters, chinese characters, numbers, watermark, logo, blurry, low quality, full street scene, wide shot, entire lamp post, pole, depth of field, bokeh"),
 10: dict(seed=19019,
   pos="stylized flat 2D digital illustration, silicon city world, clean bold shapes, flat colors, game-art aesthetic. Big close-up portrait of a chubby round pixel-art cat spirit's face filling most of the frame, white-and-grey fur rendered as soft square pixel blocks, two pointed cat ears clearly visible on top of its head, a small notch cut into its left ear, two big round innocent eyes wide open looking straight at the camera, one small front paw raised up to its mouth as if licking, soft warm indoor light, plain simple background",
   neg="photorealistic, photo, 3d render, text, letters, numbers, watermark, blurry, low quality, city scene, landscape, closed eyes, sleeping, no ears, human, dark fur, slim body"),
 11: dict(seed=19019,
   pos="stylized flat 2D digital illustration, silicon city world, clean bold shapes, flat colors, game-art aesthetic. Overhead top-down shot of a round wooden breakfast table in cozy morning light, seven small plates of colorful breakfast food arranged around the table, one chubby white-and-grey pixel-art cat spirit with chunky visible pixel-square body leaning its head down eating from one plate, its tail with a thin radio antenna on the tip clearly visible beside its round body, homey warm mood",
   neg="photorealistic, photo, 3d render, text, letters, numbers, watermark, blurry, low quality, smooth vector cat, dark fur, black cat, slim body, sitting still, empty table, one plate only"),
}

def build_wf(fix, sid):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": fix["pos"], "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": fix["neg"], "clip": ["1", 1]}},
        "4": {"class_type": "EmptyLatentImage", "inputs": {"width": 1216, "height": 683, "batch_size": 1}},
        "5": {"class_type": "KSampler", "inputs": {"seed": fix["seed"], "steps": 30, "cfg": 6.5,
                "sampler_name": "dpmpp_2m", "scheduler": "karras", "denoise": 1.0,
                "model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0], "latent_image": ["4", 0]}},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"filename_prefix": "md0001_shot%02d" % sid, "images": ["6", 0]}},
    }

def fetch_image(out_entry, dest):
    q = urllib.parse.urlencode({"filename": out_entry["filename"], "subfolder": out_entry.get("subfolder", ""), "type": out_entry.get("type", "output")})
    b = http("/view?" + q, timeout=120, raw=True)
    with open(dest, "wb") as f:
        f.write(b)
    return os.path.getsize(dest)

def main():
    log("REROLL2-START pid=%d shots=%s" % (os.getpid(), sorted(FIX)))
    import torch
    free_gb = torch.cuda.mem_get_info()[0] / (1024 ** 3)
    log("VRAM-GUARD free=%.2fGB" % free_gb)
    if free_gb < 4.5:
        log("VRAM-GUARD FAIL - defer (exit 2)"); return 2

    server = None; started_here = False
    if alive():
        log("SERVER-ALREADY-UP - reuse (no kill at end)")
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
            log("SERVER-TIMEOUT-300s"); return 3

    results = []
    for sid in sorted(FIX):
        dest = os.path.join(FRAMES, "shot%02d.png" % sid)
        t0 = time.time()
        rec = {"id": sid, "seed": FIX[sid]["seed"]}
        try:
            r = http("/prompt", {"prompt": build_wf(FIX[sid], sid), "client_id": "md0001-reroll2-r1790"}, timeout=60)
            pid = r.get("prompt_id")
            if not pid:
                rec.update(state="FAIL", err="no prompt_id"); results.append(rec); log("SHOT%02d FAIL" % sid); continue
            done = False
            while time.time() - t0 < 1200:
                time.sleep(3)
                e = http("/history/" + pid, timeout=30).get(pid)
                if e and e.get("status", {}).get("completed"):
                    if e["status"].get("status_str") == "error":
                        rec.update(state="FAIL", err="exec error"); results.append(rec); log("SHOT%02d FAIL exec" % sid); done = True; break
                    imgs = []
                    for node in e.get("outputs", {}).values():
                        imgs.extend(node.get("images", []))
                    if not imgs:
                        rec.update(state="FAIL", err="no images"); results.append(rec); log("SHOT%02d FAIL noimg" % sid); done = True; break
                    sz = fetch_image(imgs[0], dest)
                    rec.update(state="OK", bytes=sz, secs=round(time.time() - t0, 1)); results.append(rec)
                    log("SHOT%02d OK %dB in %.0fs" % (sid, sz, time.time() - t0)); done = True; break
            if not done:
                rec.update(state="FAIL", err="timeout"); results.append(rec); log("SHOT%02d FAIL timeout" % sid)
        except Exception as ex:
            rec.update(state="FAIL", err=str(ex)[:200]); results.append(rec); log("SHOT%02d FAIL exc=%s" % (sid, str(ex)[:150]))

    ok = sum(1 for r in results if r.get("state") == "OK")
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
    json.dump({"state": "DONE" if ok == len(FIX) else "PARTIAL", "ok": ok, "total": len(FIX), "results": results,
               "ts": time.strftime("%Y-%m-%d %H:%M:%S")},
              open(os.path.join(BASE, "reroll2-r1790-status.json"), "w"))
    log("SUMMARY ok=%d/%d" % (ok, len(FIX)))
    return 0 if ok == len(FIX) else 1

if __name__ == "__main__":
    try:
        rc = main()
    except Exception as ex:
        log("FATAL %s" % str(ex)[:300]); rc = 4
    log("REROLL2-END rc=%d" % rc)
    sys.exit(rc)
