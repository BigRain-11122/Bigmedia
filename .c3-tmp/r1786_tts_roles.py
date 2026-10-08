# R1786 MD-0001 multi-role TTS first production runner (ASCII law; Chinese only in data files)
# Stage A: edge-tts reference prompts per role (CPU) -> refs/*.mp3 + wav24k
# Stage B: map emotive_tts narrator segs -> segments/shotNN.mp3
# Stage C: QC - ffprobe durations + whisper small int8 CPU spot check on narrator concat
# Stage D: CosyVoice3 zero-shot for 5 character lines (GPU, VRAM gate >= 6.5 GiB; exit 3 = window blocked)
import sys, os, time, json, subprocess, shutil

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
MD = os.path.join(BASE, "data", "storylines", "drama", "md0001", "tts")
SEG = os.path.join(MD, "segments")
REFS = os.path.join(MD, "refs")
NARR = os.path.join(MD, "narrator")
for d in (SEG, REFS, NARR):
    os.makedirs(d, exist_ok=True)

cast = json.load(open(os.path.join(MD, "cast.json"), encoding="utf-8"))
NARR_SHOTS = [1, 3, 5, 6, 8, 9, 12, 13]

def log(m):
    print("[%s] %s" % (time.strftime("%H:%M:%S"), m), flush=True)

def dur(path):
    out = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True)
    return round(float(out.stdout.strip()), 2)

# ---- Stage A: reference prompts (edge-tts, CPU) ----
for rid, r in sorted(cast["roles"].items()):
    if r.get("engine") != "cosyvoice3-zero-shot":
        continue
    mp3 = os.path.join(REFS, rid + ".mp3")
    wav = os.path.join(REFS, rid + ".wav")
    if not os.path.exists(mp3):
        cmd = ["edge-tts", "--voice", r["ref_voice"]] + r["ref_flags"] + \
              ["--text", r["ref_text"], "--write-media", mp3]
        subprocess.run(cmd, check=True)
    if not os.path.exists(wav):
        subprocess.run(["ffmpeg", "-y", "-v", "quiet", "-i", mp3, "-ar", "24000", "-ac", "1", wav], check=True)
    log("stage-A ref %s voice=%s dur=%.2fs" % (rid, r["ref_voice"], dur(mp3)))
log("stage-A REFS-OK")

# ---- Stage B: narrator segment mapping ----
mapped = 0
for i, shot in enumerate(NARR_SHOTS):
    src = os.path.join(NARR, "seg%02d.mp3" % i)
    dst = os.path.join(SEG, "shot%02d.mp3" % shot)
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy(src, dst)
        mapped += 1
log("stage-B narrator segs mapped=%d (of %d)" % (mapped, len(NARR_SHOTS)))

# ---- Stage C: QC (durations + whisper small spot check) ----
qc = {"segments": {}, "narrator_asr": ""}
for f in sorted(os.listdir(SEG)):
    p = os.path.join(SEG, f)
    qc["segments"][f] = dur(p)
narr_mp3 = os.path.join(NARR, "audio.mp3")
if os.path.exists(narr_mp3):
    from faster_whisper import WhisperModel
    wm = WhisperModel("small", device="cpu", compute_type="int8")
    segs, info = wm.transcribe(narr_mp3, beam_size=5, condition_on_previous_text=False, language="zh")
    txt = "".join(s.text for s in segs).replace(" ", "")
    qc["narrator_asr"] = txt
exp = ["台风梅花过境之夜", "疤是资历", "超载运行，无损耗", "守了一宿", "全城灯带如常亮起",
       "尾巴天线立了大功", "把夜交给早晨", "真实档案改编"]
hits = sum(1 for a in exp if all(ch in txt for ch in a[:3])) if (txt := qc["narrator_asr"]) else 0
qc["anchor_hits"] = "%d/8" % hits
json.dump(qc, open(os.path.join(MD, "qc-r1786.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
log("stage-C QC segs=%d anchors=%s/8" % (len(qc["segments"]), hits))

# ---- Stage D: CosyVoice3 zero-shot (GPU) ----
import torch
free, total = torch.cuda.mem_get_info(0)
log("stage-D VRAM free=%.2f GiB (gate 6.50)" % (free / 2**30))
if free / 2**30 < 6.5:
    log("VRAM-WINDOW-BLOCKED: load+cast consumes ~6.7 GiB (R1784 log anchor 9.87->4.18+cast); retry when free")
    sys.exit(3)

REPO = os.path.join(BASE, "data", "assets", "cosyvoice-runtime", "CosyVoice")
sys.path.insert(0, os.path.join(REPO, "third_party", "Matcha-TTS"))
sys.path.insert(0, REPO)
import torchaudio as _ta
import numpy as _np
import soundfile as _sf

def _sf_load(filepath, *a, **k):
    data, sr = _sf.read(filepath, dtype="float32", always_2d=True)
    return torch.from_numpy(_np.ascontiguousarray(data.T)), sr

def _sf_save(filepath, tensor, sr, *a, **k):
    _sf.write(filepath, _np.asarray(tensor.detach().cpu().numpy().T), sr)

_ta.load = _sf_load
_ta.save = _sf_save

from cosyvoice.cli.cosyvoice import AutoModel
MODEL_DIR = os.path.join(BASE, "data", "assets", "models", "Fun-CosyVoice3-0.5B-2512")
t0 = time.time()
model = AutoModel(model_dir=MODEL_DIR)
model.model.llm.llm.model.float()
log("stage-D model loaded %.1fs (fp32 recast done)" % (time.time() - t0))

PREFIX = cast["cosyvoice3_prefix"]
for rid, r in sorted(cast["roles"].items()):
    if r.get("engine") != "cosyvoice3-zero-shot":
        continue
    wav = os.path.join(REFS, rid + ".wav")
    prompt_text = PREFIX + r["ref_text"]
    for shot, line in sorted(r["lines"].items(), key=lambda kv: int(kv[0])):
        out_path = os.path.join(SEG, "shot%02d.wav" % int(shot))
        if os.path.exists(out_path):
            log("skip existing %s" % os.path.basename(out_path))
            continue
        t1 = time.time()
        chunks = []
        for out in model.inference_zero_shot(line, prompt_text, wav, stream=False):
            chunks.append(out["tts_speech"])
        speech = torch.cat(chunks, dim=1)
        _ta.save(out_path, speech, model.sample_rate)
        log("stage-D shot%s [%s] dur=%.2fs infer=%.1fs" % (shot, rid, speech.shape[1] / model.sample_rate, time.time() - t1))
log("stage-D ZERO-SHOT-OK")
print("ALL-STAGES-PASS")
