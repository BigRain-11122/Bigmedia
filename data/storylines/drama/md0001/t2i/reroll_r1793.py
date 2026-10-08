# MD-0001 reroll R1793 - targeted best-of-N for the two true residual gate FAILs
# (tower shot07 was a gate-instruction mislabel, not a frame defect -> tower 2/2 stands)
# shot09 cat: antenna landed on head / left-ear notch lost / fur drift / too small
#   -> strong-bound rewrite: grey-white fur, V-notch left ear, tail-tip antenna (not head),
#      larger cat in frame, paper note kept
# shot12 lamp: distant-dot lamp unreadable -> keep ending mood but bring lamp readable:
#   tilted lampshade silhouette + welded patch catching light, closer to camera
# 3 seeds each = 6 candidates, ~60s/gen on Qwen-Image-2.1 native trio.
# Output: reroll-r1793/shotNN_sSEED.png ; status json + log for polling.
import json, os, sys, time, subprocess, urllib.request, urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "reroll-r1793")
COMFY = r"C:\Agent\ComfyUI"
CPY = os.path.join(COMFY, ".venv", "Scripts", "python.exe")
HOST, PORT = "127.0.0.1", 8188
DETACHED = 0x00000008 | 0x00000200 | 0x08000000

UNET = "qwen_image_2.1_int8_convrot.safetensors"
TE = "qwen3vl_8b_w4a8.safetensors"
VAE = "qwen_image_2.1_vae_bf16.safetensors"
W, H = 1216, 688
STEPS, CFG = 25, 1.0
SAMPLER, SCHED = "euler", "simple"

FIX9 = ("dynamic follow shot of a chubby round pixel-art cat spirit gliding through a narrow rain alley, "
        "the cat fills a large part of the frame, short grey-and-white fur with pixel-square body pattern, "
        "a clear V-shaped notch cut into the outline of its left ear, "
        "a thin metal radio antenna rod growing from the tip of its tail pointing upward (antenna on tail, not on head), "
        "carrying a small paper note in its mouth, determined cute expression, motion lines")
FIX12 = ("nearly black night frame, quiet peaceful ending mood, an old cast-iron street lamp stands in the "
         "mid-distance on the right, its wide lampshade slightly tilted, a small welded metal patch on the "
         "lampshade catches the warm glow, faint warm light halo, the dark silhouette of a signal tower far "
         "behind against the night sky, a tiny round cat curled up asleep at the base of the lamp post")

NEG_EXTRA = ", antenna growing from head, head antenna"
SEEDS = {9: [19019, 19019 + 101, 19019 + 202], 12: [13013, 13013 + 101, 13013 + 202]}

LOG = open(os.path.join(BASE, "reroll-r1793.log"), "a", encoding="utf-8", errors="replace")
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

def build_wf(prompt, neg, seed, prefix):
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": UNET, "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": TE, "type": "qwen_image", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
        "4": {"class_type": "QwenImage21Cache", "inputs": {"model": ["1", 0], "device": "auto", "dtype": "default"}},
        "5": {"class_type": "TextEncodeQwenImage21",
              "inputs": {"clip": ["2", 0], "prompt": prompt, "negative_prompt": neg, "resolution": 1024}},
        "6": {"class_type": "EmptyLatentImage", "inputs": {"width": W, "height": H, "batch_size": 1}},
        "7": {"class_type": "KSampler",
              "inputs": {"seed": seed, "steps": STEPS, "cfg": CFG, "sampler_name": SAMPLER,
                         "scheduler": SCHED, "denoise": 1.0, "model": ["4", 0],
                         "positive": ["5", 0], "negative": ["5", 1], "latent_image": ["6", 0]}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["3", 0]}},
        "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": prefix, "images": ["8", 0]}},
    }

def fetch_image(entry, dest):
    q = urllib.parse.urlencode({"filename": entry["filename"], "subfolder": entry.get("subfolder", ""),
                                "type": entry.get("type", "output")})
    b = http("/view?" + q, timeout=120, raw=True)
    with open(dest, "wb") as f:
        f.write(b)
    return os.path.getsize(dest)

def main():
    os.makedirs(OUT, exist_ok=True)
    pack = json.load(open(os.path.join(BASE, "PACK-v1.json"), encoding="utf-8"))
    style = pack["style_lock"]
    neg = pack["negative_lock"] + NEG_EXTRA
    log("REROLL-R1793-START pid=%d" % os.getpid())

    import torch
    free_b, total_b = torch.cuda.mem_get_info()
    free_gb = free_b / (1024 ** 3)
    log("VRAM-GUARD free=%.2fGB" % free_gb)
    if free_gb < 9.0:
        log("VRAM-GUARD FAIL (<9GB) - defer (exit 2)")
        json.dump({"state": "DEFERRED_VRAM", "free_gb": round(free_gb, 2), "ts": time.strftime("%Y-%m-%d %H:%M:%S")},
                  open(os.path.join(BASE, "reroll-r1793-status.json"), "w"))
        return 2

    server = None
    started_here = False
    if alive():
        log("SERVER-ALREADY-UP")
    else:
        slog = open(os.path.join(BASE, "server-r1793.log"), "a", encoding="utf-8", errors="replace")
        server = subprocess.Popen([CPY, "main.py", "--listen", "127.0.0.1", "--port", str(PORT),
                                   "--lowvram", "--disable-auto-launch", "--preview-method", "none"],
                                  cwd=COMFY, stdout=slog, stderr=subprocess.STDOUT, creationflags=DETACHED)
        started_here = True
        log("SERVER-SPAWN pid=%d" % server.pid)
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
    jobs = [(9, FIX9, s) for s in SEEDS[9]] + [(12, FIX12, s) for s in SEEDS[12]]
    for sid, prompt, seed in jobs:
        pos = style + ", " + prompt
        dest = os.path.join(OUT, "shot%02d_s%d.png" % (sid, seed))
        t0 = time.time()
        rec = {"id": sid, "seed": seed}
        try:
            r = http("/prompt", {"prompt": build_wf(pos, neg, seed, "md0001_r1793_shot%02d_s%d" % (sid, seed)),
                                 "client_id": "md0001-reroll-r1793"}, timeout=120)
            pid = r.get("prompt_id")
            if not pid:
                rec.update(state="FAIL", err="no prompt_id"); results.append(rec); log("SHOT%02d_s%d FAIL no-id" % (sid, seed)); continue
            done = False
            while time.time() - t0 < 1200:
                time.sleep(5)
                h = http("/history/" + pid, timeout=30)
                e = h.get(pid)
                if e and e.get("status", {}).get("completed"):
                    if e["status"].get("status_str") == "error":
                        rec.update(state="FAIL", err="exec error"); results.append(rec)
                        log("SHOT%02d_s%d FAIL exec" % (sid, seed)); done = True; break
                    imgs = []
                    for node in e.get("outputs", {}).values():
                        imgs.extend(node.get("images", []))
                    if not imgs:
                        rec.update(state="FAIL", err="no images"); results.append(rec)
                        log("SHOT%02d_s%d FAIL no-img" % (sid, seed)); done = True; break
                    sz = fetch_image(imgs[0], dest)
                    rec.update(state="OK", bytes=sz, secs=round(time.time() - t0, 1))
                    results.append(rec)
                    log("SHOT%02d_s%d OK %dB %.0fs" % (sid, seed, sz, time.time() - t0))
                    done = True; break
            if not done:
                rec.update(state="FAIL", err="timeout"); results.append(rec); log("SHOT%02d_s%d FAIL timeout" % (sid, seed))
        except Exception as ex:
            rec.update(state="FAIL", err=str(ex)[:200]); results.append(rec); log("SHOT%02d_s%d FAIL exc=%s" % (sid, seed, str(ex)[:200]))

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
    json.dump({"state": "DONE", "ok": ok, "total": len(jobs), "results": results,
               "ts": time.strftime("%Y-%m-%d %H:%M:%S")},
              open(os.path.join(BASE, "reroll-r1793-status.json"), "w"))
    log("SUMMARY ok=%d/%d" % (ok, len(jobs)))
    return 0 if ok == len(jobs) else 1

if __name__ == "__main__":
    try:
        rc = main()
    except Exception as ex:
        log("FATAL %s" % str(ex)[:300]); rc = 4
    log("REROLL-END rc=%d" % rc)
    sys.exit(rc)
