# MD-0001 T2I gate re-roll (R1790) - consistency gate FAIL iteration, 5 shots only
# Gate read (R1790 formal): 4/9 PASS -> FAIL (criterion >=8). FAIL shots:
#   03 lamp: patch not visible + photoreal drift | 06 tower: hat + uniform, dozing unclear
#   07 tower: hat + outdoor drift + no amber screen light | 10 cat: no ear notch/lick/eye-contact
#   11 cat: identity collapse (dark slim cat, no antenna), <7 plates, not eating
# Prompt-side fixes with strengthened negatives; char seeds kept (noise anchor), content driven by prompt.
# Archives v1 frames to frames-v1/ before overwrite (FAIL evidence preserved).
# Same server discipline as runner_r1789: lowvram, start-here/kill-here, VRAM guard >=4.5GB.
import json, os, sys, time, subprocess, urllib.request, urllib.parse, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.join(BASE, "frames")
V1 = os.path.join(BASE, "frames-v1")
COMFY = r"C:\Agent\ComfyUI"
CPY = os.path.join(COMFY, ".venv", "Scripts", "python.exe")
HOST, PORT = "127.0.0.1", 8188
DETACHED = 0x00000008 | 0x00000200 | 0x08000000

LOG = open(os.path.join(BASE, "reroll-r1790.log"), "a", encoding="utf-8", errors="replace")
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

# gate-fail fixes: char tokens strengthened + per-shot negatives (gate-r1790 verdicts)
FIX = {
 3: dict(seed=41041, char="lamp",
   prompt="extreme macro close-up of a small tilted rectangular metal patch welded on the side of an old cast-iron lampshade, the patch is the clear main subject, rough visible weld seam around its edges, rivets and scratches on the patch, glaring under strong warm light, rain droplets on metal, dark background",
   neg="photorealistic metal texture, metallic gradient, depth of field, bokeh, macro photograph, hat"),
 6: dict(seed=27027, char="tower",
   prompt="mid side shot inside an old signal tower station room, a sturdy 50-year-old Chinese veteran guard with bare head and short grey-streaked hair, wearing a plain worn brown work jacket, curled up asleep on a chair, head drooping to one side, eyes closed, wall of analog gauges, typhoon wind and rain howling outside the window",
   neg="hat, cap, helmet, peaked cap, beret, uniform, epaulettes, medals, standing, awake"),
 7: dict(seed=27027, char="tower",
   prompt="close-up of a weathered Chinese veteran guard's resolute side profile, bare head with short grey-streaked hair, plain worn brown work jacket, inside an old signal tower station room at night, warm amber glow from a round amber rolling display screen reflecting clearly on his face, wall of analog gauges behind him, warm amber and deep blue contrast",
   neg="hat, cap, helmet, peaked cap, beret, uniform, epaulettes, outdoor, sky, rain on face, darkness on face"),
 10: dict(seed=19019, char="cat",
   prompt="close-up of a chubby round pixel-art cat spirit's plump face made of soft square pixels, a small notch clearly cut into its left ear, one front paw raised up to its mouth licking, big innocent round eyes wide open looking straight at the camera, soft warm indoor light",
   neg="closed eyes, sleeping, sad, dark fur, black cat, slim body"),
 11: dict(seed=19019, char="cat",
   prompt="overhead top-down shot of a wooden table holding seven small breakfast plates of different flavors and colors arranged in two rows, one chubby white-and-grey round pixel-art cat spirit with plump square-pixel body and a thin radio antenna on its tail tip, bent down eating heartily from one plate, cozy morning light, homey warm mood",
   neg="dark fur, black cat, slim body, long body, smooth vector cat, empty table, single plate"),
}
CHAR_TOKENS = {
 "lamp": "an old outer-ring street lamp number 14, cast-iron pole, wide lampshade with a small tilted metal patch welded on its side, warm white light glowing",
 "tower": "a sturdy 50-year-old Chinese veteran signal-tower guard, bare head, short grey-streaked hair, plain worn brown work jacket, calm weathered face",
 "cat": "a chubby round pixel-art cat spirit, plump body of soft square pixels, white-and-grey fur, thin radio antenna on its tail tip, small notch in its left ear",
}
STYLE = "stylized flat 2D digital illustration, silicon city world, muted desaturated palette, cinematic night atmosphere, clean bold shapes, flat colors, soft film grain, game-art aesthetic"
NEG_BASE = "photorealistic, photo, 3d render, octane render, text, letters, chinese characters, numbers, watermark, signature, logo, blurry, low quality, deformed, disfigured, extra limbs, oversaturated, neon overload"

def build_wf(fix):
    pos = STYLE + ", " + CHAR_TOKENS[fix["char"]] + ", " + fix["prompt"]
    neg = NEG_BASE + ", " + fix["neg"]
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": pos, "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": neg, "clip": ["1", 1]}},
        "4": {"class_type": "EmptyLatentImage", "inputs": {"width": 1216, "height": 683, "batch_size": 1}},
        "5": {"class_type": "KSampler", "inputs": {"seed": fix["seed"], "steps": 30, "cfg": 6.5,
                "sampler_name": "dpmpp_2m", "scheduler": "karras", "denoise": 1.0,
                "model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0], "latent_image": ["4", 0]}},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"filename_prefix": "md0001_shot%02d" % fix["id"], "images": ["6", 0]}},
    }

def fetch_image(out_entry, dest):
    q = urllib.parse.urlencode({"filename": out_entry["filename"], "subfolder": out_entry.get("subfolder", ""), "type": out_entry.get("type", "output")})
    b = http("/view?" + q, timeout=120, raw=True)
    with open(dest, "wb") as f:
        f.write(b)
    return os.path.getsize(dest)

def main():
    os.makedirs(V1, exist_ok=True)
    for sid in FIX:
        src = os.path.join(FRAMES, "shot%02d.png" % sid)
        dst = os.path.join(V1, "shot%02d.png" % sid)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
    log("REROLL-START pid=%d shots=%s (v1 archived to frames-v1/)" % (os.getpid(), sorted(FIX)))

    import torch
    free_b, total_b = torch.cuda.mem_get_info()
    free_gb = free_b / (1024 ** 3)
    log("VRAM-GUARD free=%.2fGB" % free_gb)
    if free_gb < 4.5:
        log("VRAM-GUARD FAIL - defer (exit 2)")
        return 2

    server = None; started_here = False
    if alive():
        log("SERVER-ALREADY-UP - reuse (no kill at end)")
    else:
        slog = open(os.path.join(BASE, "server-r1790.log"), "a", encoding="utf-8", errors="replace")
        server = subprocess.Popen([CPY, "main.py", "--listen", "127.0.0.1", "--port", str(PORT),
                                   "--lowvram", "--disable-auto-launch", "--preview-method", "none"],
                                  cwd=COMFY, stdout=slog, stderr=subprocess.STDOUT, creationflags=DETACHED)
        started_here = True
        log("SERVER-SPAWN pid=%d - waiting (max 300s)" % server.pid)
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
        fix = dict(FIX[sid]); fix["id"] = sid
        dest = os.path.join(FRAMES, "shot%02d.png" % sid)
        t0 = time.time()
        rec = {"id": sid, "char": fix["char"], "seed": fix["seed"]}
        try:
            r = http("/prompt", {"prompt": build_wf(fix), "client_id": "md0001-reroll-r1790"}, timeout=60)
            pid = r.get("prompt_id")
            if not pid:
                rec.update(state="FAIL", err="no prompt_id"); results.append(rec); log("SHOT%02d FAIL no-prompt-id" % sid); continue
            done = False
            while time.time() - t0 < 1200:
                time.sleep(3)
                h = http("/history/" + pid, timeout=30)
                e = h.get(pid)
                if e and e.get("status", {}).get("completed"):
                    st = e["status"].get("status_str")
                    if st == "error":
                        rec.update(state="FAIL", err="exec error"); results.append(rec); log("SHOT%02d FAIL exec-error" % sid); done = True; break
                    imgs = []
                    for node in e.get("outputs", {}).values():
                        imgs.extend(node.get("images", []))
                    if not imgs:
                        rec.update(state="FAIL", err="no output images"); results.append(rec); log("SHOT%02d FAIL no-images" % sid); done = True; break
                    sz = fetch_image(imgs[0], dest)
                    rec.update(state="OK", bytes=sz, secs=round(time.time() - t0, 1))
                    results.append(rec)
                    log("SHOT%02d OK %dB in %.0fs" % (sid, sz, time.time() - t0))
                    done = True; break
            if not done:
                rec.update(state="FAIL", err="timeout"); results.append(rec); log("SHOT%02d FAIL timeout" % sid)
        except Exception as ex:
            rec.update(state="FAIL", err=str(ex)[:200]); results.append(rec); log("SHOT%02d FAIL exc=%s" % (sid, str(ex)[:200]))

    ok = sum(1 for r in results if r.get("state") == "OK")
    if started_here and server is not None:
        try:
            server.terminate()
            try:
                server.wait(timeout=20)
            except Exception:
                server.kill(); server.wait(timeout=20)
            log("SERVER-STOPPED (VRAM released)")
        except Exception as ex:
            log("SERVER-STOP exc=%s" % str(ex)[:120])
    json.dump({"state": "DONE" if ok == len(FIX) else "PARTIAL", "ok": ok, "total": len(FIX),
               "results": results, "ts": time.strftime("%Y-%m-%d %H:%M:%S")},
              open(os.path.join(BASE, "reroll-r1790-status.json"), "w"))
    log("SUMMARY ok=%d/%d" % (ok, len(FIX)))
    return 0 if ok == len(FIX) else 1

if __name__ == "__main__":
    try:
        rc = main()
    except Exception as ex:
        log("FATAL %s" % str(ex)[:300]); rc = 4
    log("REROLL-END rc=%d" % rc)
    sys.exit(rc)
