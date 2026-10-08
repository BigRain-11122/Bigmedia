# MD-0001 T2I runner leg (R1789) - consumes t2i/PACK-v1.json (dual-consumer canon pack)
# Starts local ComfyUI (--lowvram, draft PoC path per R1788 adjudication), submits 12 txt2img
# shots sequentially, saves frames to t2i/frames/, then STOPS the server to release VRAM
# (co-card yielding discipline: AIHOT 14b-8k compose window at 08:00 must not be squeezed).
# Logs: runner-r1789.log (ASCII) + runner-r1789-status.json for next-round polling.
import json, os, sys, time, subprocess, urllib.request, urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.join(BASE, "frames")
COMFY = r"C:\Agent\ComfyUI"
CPY = os.path.join(COMFY, ".venv", "Scripts", "python.exe")
HOST, PORT = "127.0.0.1", 8188
DETACHED = 0x00000008 | 0x00000200 | 0x08000000  # DETACHED_PROCESS|CREATE_NEW_PROCESS_GROUP|CREATE_NO_WINDOW (U060)

LOG = open(os.path.join(BASE, "runner-r1789.log"), "a", encoding="utf-8", errors="replace")
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
    d = pack["defaults"]
    pos = pack["style_lock"]
    ch = pack["characters"].get(shot.get("char"))
    if ch:
        pos += ", " + ch["tokens"]
    pos += ", " + shot["prompt"]
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": pack["checkpoint"]["file"]}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": pos, "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": pack["negative_lock"], "clip": ["1", 1]}},
        "4": {"class_type": "EmptyLatentImage", "inputs": {"width": d["width"], "height": d["height"], "batch_size": 1}},
        "5": {"class_type": "KSampler", "inputs": {"seed": shot["seed"], "steps": d["steps"], "cfg": d["cfg"],
                "sampler_name": d["sampler"], "scheduler": d["scheduler"], "denoise": d["denoise"],
                "model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0], "latent_image": ["4", 0]}},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"filename_prefix": "md0001_shot%02d" % shot["id"], "images": ["6", 0]}},
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
    shots = [s for s in pack["shots"] if not s.get("program_layer")]
    log("RUNNER-START pid=%d shots=%d (program-layer shots skipped by design)" % (os.getpid(), len(shots)))

    # VRAM guard (co-card yielding): need >=4.5GB free for lowvram streaming + activations
    import torch
    free_b, total_b = torch.cuda.mem_get_info()
    free_gb = free_b / (1024 ** 3)
    log("VRAM-GUARD free=%.2fGB total=%.2fGB" % (free_gb, total_b / (1024 ** 3)))
    if free_gb < 4.5:
        log("VRAM-GUARD FAIL - defer runner leg to next window (exit 2)")
        json.dump({"state": "DEFERRED_VRAM", "free_gb": round(free_gb, 2), "ts": time.strftime("%Y-%m-%d %H:%M:%S")},
                  open(os.path.join(BASE, "runner-r1789-status.json"), "w"))
        return 2

    server = None
    started_here = False
    if alive():
        log("SERVER-ALREADY-UP - reusing existing 8188 (no kill at end)")
    else:
        slog = open(os.path.join(BASE, "server-r1789.log"), "a", encoding="utf-8", errors="replace")
        server = subprocess.Popen([CPY, "main.py", "--listen", "127.0.0.1", "--port", str(PORT),
                                   "--lowvram", "--disable-auto-launch", "--preview-method", "none"],
                                  cwd=COMFY, stdout=slog, stderr=subprocess.STDOUT, creationflags=DETACHED)
        started_here = True
        log("SERVER-SPAWN pid=%d - waiting for /system_stats (max 300s)" % server.pid)
        t0 = time.time()
        while time.time() - t0 < 300:
            if server.poll() is not None:
                log("SERVER-DIED-EARLY rc=%d - see server-r1789.log" % server.returncode)
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
            r = http("/prompt", {"prompt": build_wf(s, pack), "client_id": "md0001-runner-r1789"}, timeout=60)
            pid = r.get("prompt_id")
            if not pid:
                rec.update(state="FAIL", err="no prompt_id"); results.append(rec); log("SHOT%02d FAIL no-prompt-id" % sid); continue
            done = False
            while time.time() - t0 < 1800:
                time.sleep(3)
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
                    log("SHOT%02d OK %dB in %.0fs -> frames/shot%02d.png" % (sid, sz, time.time() - t0, sid))
                    done = True
                    break
            if not done:
                rec.update(state="FAIL", err="timeout-1800s"); results.append(rec); log("SHOT%02d FAIL timeout" % sid)
        except Exception as ex:
            rec.update(state="FAIL", err=str(ex)[:200]); results.append(rec)
            log("SHOT%02d FAIL exc=%s" % (sid, str(ex)[:200]))

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
    summary = {"state": "DONE", "ok": ok, "total": len(shots), "results": results, "ts": time.strftime("%Y-%m-%d %H:%M:%S")}
    json.dump(summary, open(os.path.join(BASE, "runner-r1789-status.json"), "w"))
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
