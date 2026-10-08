# MD-0001 T2I runner R1792 - Qwen-Image-2.1 native-quant trio upgrade leg (R1791 pointer 3)
# Replaces the SDXL draft graph (runner_r1789) with the canonical Comfy-Org 0.37.0
# qwen_image21 txt2img graph, transcribed from the official template
# (comfyui_workflow_templates_json/templates/image_qwen_image_2_1_t2i.json):
#   UNETLoader(qwen_image_2.1_int8_convrot) -> QwenImage21Cache(auto/default) -> KSampler
#   CLIPLoader(qwen3vl_8b_w4a8, type=qwen_image) -> TextEncodeQwenImage21(prompt, negative_prompt)
#   EmptyLatentImage(width,height)  [fix_empty_latent_channels adapts to 64ch/16x latent]
#   KSampler(steps=25, cfg=1.0, euler, simple, denoise=1.0) -> VAEDecode(qwen_image_2.1_vae_bf16)
# Re-rolls the full 12-shot set (not only 03/10/11): same-world consistency ruling under
# O-2126 - a film cut mixing SDXL frames with Qwen-2.1 frames fails the same-world check
# at assembly/M4 anyway; one full re-roll under the upgraded model is the correct-cost path.
# Seeds stay locked to PACK-v1 character anchors (lamp 41041 / tower 27027 / cat 19019).
# Output: frames-r1792/ (frames/ = SDXL draft set preserved as gate-r1790-verdict evidence).
# VRAM guard: >= 9.0 GB free (trio stack is heavier than the SDXL 4.5 GB threshold; with the
# 7b keep-warm lane resident only ~6.4 GB can free, so this leg fires in a true yield window).
# Logs: runner-r1792.log + runner-r1792-status.json for next-round polling.
import json, os, sys, time, subprocess, urllib.request, urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.join(BASE, "frames-r1792")
COMFY = r"C:\Agent\ComfyUI"
CPY = os.path.join(COMFY, ".venv", "Scripts", "python.exe")
HOST, PORT = "127.0.0.1", 8188
DETACHED = 0x00000008 | 0x00000200 | 0x08000000  # DETACHED|NEW_PROCESS_GROUP|CREATE_NO_WINDOW (U060)

# native trio (R1791 pull, byte-verified 3/3 DONE-OK)
UNET = "qwen_image_2.1_int8_convrot.safetensors"
TE = "qwen3vl_8b_w4a8.safetensors"
VAE = "qwen_image_2.1_vae_bf16.safetensors"
# pixel dims must be multiples of 16 for the 16x latent (683 target -> 688 nearest)
W, H = 1216, 688
STEPS, CFG = 25, 1.0   # canon defaults from the official 2.1 t2i template
SAMPLER, SCHED = "euler", "simple"

LOG = open(os.path.join(BASE, "runner-r1792.log"), "a", encoding="utf-8", errors="replace")
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

def build_wf(shot, pack):
    pos = pack["style_lock"]
    ch = pack["characters"].get(shot.get("char"))
    if ch:
        pos += ", " + ch["tokens"]
    pos += ", " + shot["prompt"]
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": UNET, "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": TE, "type": "qwen_image", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
        "4": {"class_type": "QwenImage21Cache", "inputs": {"model": ["1", 0], "device": "auto", "dtype": "default"}},
        "5": {"class_type": "TextEncodeQwenImage21",
              "inputs": {"clip": ["2", 0], "prompt": pos, "negative_prompt": pack["negative_lock"], "resolution": 1024}},
        "6": {"class_type": "EmptyLatentImage", "inputs": {"width": W, "height": H, "batch_size": 1}},
        "7": {"class_type": "KSampler",
              "inputs": {"seed": shot["seed"], "steps": STEPS, "cfg": CFG, "sampler_name": SAMPLER,
                         "scheduler": SCHED, "denoise": 1.0, "model": ["4", 0],
                         "positive": ["5", 0], "negative": ["5", 1], "latent_image": ["6", 0]}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["3", 0]}},
        "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "md0001_r1792_shot%02d" % shot["id"], "images": ["8", 0]}},
    }

def fetch_image(out_entry, dest):
    q = urllib.parse.urlencode({"filename": out_entry["filename"], "subfolder": out_entry.get("subfolder", ""), "type": out_entry.get("type", "output")})
    b = http("/view?" + q, timeout=120, raw=True)
    with open(dest, "wb") as f:
        f.write(b)
    return os.path.getsize(dest)

def main():
    os.makedirs(FRAMES, exist_ok=True)
    pack = json.load(open(os.path.join(BASE, "PACK-v1.json"), encoding="utf-8"))
    only = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else None
    shots = [s for s in pack["shots"] if not s.get("program_layer")]
    if only:
        shots = [s for s in shots if s["id"] in only]
    log("RUNNER-START pid=%d model=qwen_image_2.1_native shots=%d%s (program-layer skipped by design)"
        % (os.getpid(), len(shots), (" filter=" + str(only)) if only else ""))

    # VRAM guard (co-card yielding): full 12-shot re-roll needs a real window
    import torch
    free_b, total_b = torch.cuda.mem_get_info()
    free_gb = free_b / (1024 ** 3)
    log("VRAM-GUARD free=%.2fGB total=%.2fGB" % (free_gb, total_b / (1024 ** 3)))
    if free_gb < 9.0:
        log("VRAM-GUARD FAIL (<9GB) - defer to next yield window (exit 2)")
        json.dump({"state": "DEFERRED_VRAM", "free_gb": round(free_gb, 2), "ts": time.strftime("%Y-%m-%d %H:%M:%S")},
                  open(os.path.join(BASE, "runner-r1792-status.json"), "w"))
        return 2

    server = None
    started_here = False
    if alive():
        log("SERVER-ALREADY-UP - reusing existing 8188 (no kill at end)")
    else:
        slog = open(os.path.join(BASE, "server-r1792.log"), "a", encoding="utf-8", errors="replace")
        server = subprocess.Popen([CPY, "main.py", "--listen", "127.0.0.1", "--port", str(PORT),
                                   "--lowvram", "--disable-auto-launch", "--preview-method", "none"],
                                  cwd=COMFY, stdout=slog, stderr=subprocess.STDOUT, creationflags=DETACHED)
        started_here = True
        log("SERVER-SPAWN pid=%d - waiting for /system_stats (max 300s)" % server.pid)
        t0 = time.time()
        while time.time() - t0 < 300:
            if server.poll() is not None:
                log("SERVER-DIED-EARLY rc=%d - see server-r1792.log" % server.returncode)
                return 3
            if alive():
                log("SERVER-READY in %.0fs" % (time.time() - t0))
                break
            time.sleep(3)
        else:
            log("SERVER-TIMEOUT-300s - abort (server left for post-mortem, no shots submitted)")
            return 3

    results = []
    for s in shots:
        sid = s["id"]
        dest = os.path.join(FRAMES, "shot%02d.png" % sid)
        t0 = time.time()
        rec = {"id": sid, "char": s.get("char", ""), "seed": s["seed"]}
        try:
            r = http("/prompt", {"prompt": build_wf(s, pack), "client_id": "md0001-runner-r1792"}, timeout=120)
            pid = r.get("prompt_id")
            if not pid:
                rec.update(state="FAIL", err="no prompt_id"); results.append(rec); log("SHOT%02d FAIL no-prompt-id" % sid); continue
            done = False
            while time.time() - t0 < 1800:
                time.sleep(5)
                h = http("/history/" + pid, timeout=30)
                e = h.get(pid)
                if e and e.get("status", {}).get("completed"):
                    st = e["status"].get("status_str")
                    if st == "error":
                        rec.update(state="FAIL", err="exec error"); results.append(rec); log("SHOT%02d FAIL exec-error" % sid); done=True; break
                    imgs = []
                    for node in e.get("outputs", {}).values():
                        imgs.extend(node.get("images", []))
                    if not imgs:
                        rec.update(state="FAIL", err="no output images"); results.append(rec); log("SHOT%02d FAIL no-images" % sid); done=True; break
                    sz = fetch_image(imgs[0], dest)
                    rec.update(state="OK", bytes=sz, secs=round(time.time() - t0, 1))
                    results.append(rec)
                    log("SHOT%02d OK %dB in %.0fs -> frames-r1792/shot%02d.png" % (sid, sz, time.time() - t0, sid))
                    done = True
                    break
            if not done:
                rec.update(state="FAIL", err="timeout-1800s"); results.append(rec); log("SHOT%02d FAIL timeout" % sid)
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
            log("SERVER-STOPPED (VRAM released for co-card lanes)")
        except Exception as ex:
            log("SERVER-STOP exc=%s" % str(ex)[:120])
    summary = {"state": "DONE", "model": "qwen_image_2.1_native", "ok": ok, "total": len(shots),
               "results": results, "ts": time.strftime("%Y-%m-%d %H:%M:%S")}
    json.dump(summary, open(os.path.join(BASE, "runner-r1792-status.json"), "w"))
    log("SUMMARY ok=%d/%d" % (ok, len(shots)))
    return 0 if ok == len(shots) else 1

if __name__ == "__main__":
    try:
        rc = main()
    except Exception as ex:
        log("FATAL %s" % str(ex)[:300])
        rc = 4
    log("RUNNER-END rc=%d" % rc)
    sys.exit(rc)
