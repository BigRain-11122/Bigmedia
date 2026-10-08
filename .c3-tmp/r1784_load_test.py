import sys, os, time, traceback

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "assets", "cosyvoice-runtime", "CosyVoice")
REPO = os.path.abspath(REPO)
MODEL_DIR = os.path.abspath(os.path.join(REPO, "..", "..", "models", "Fun-CosyVoice3-0.5B-2512"))
SMOKE_WAV = os.path.abspath(os.path.join(REPO, "..", "smoke_cv3_crosslingual.wav"))
TEXT_FILE = os.path.abspath(os.path.join(REPO, "..", "smoke_text.txt"))
PROMPT_WAV = os.path.join(REPO, "asset", "zero_shot_prompt.wav")

def log(msg):
    print("[{}] {}".format(time.strftime("%H:%M:%S"), msg), flush=True)

log("stage-0 sys.path setup")
sys.path.insert(0, os.path.join(REPO, "third_party", "Matcha-TTS"))
sys.path.insert(0, REPO)

import torch

# torchaudio 2.11 load/save need torchcodec+FFmpeg runtime (broken on this
# host); soundfile shim with classic (channels, frames) convention instead.
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
log("torchaudio load/save shimmed via soundfile")

log("cuda available={} device={}".format(torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu"))
if torch.cuda.is_available():
    free, total = torch.cuda.mem_get_info(0)
    log("VRAM before load: free {:.2f} GiB / total {:.2f} GiB".format(free / 2**30, total / 2**30))

log("stage-1 import AutoModel")
from cosyvoice.cli.cosyvoice import AutoModel

log("stage-2 AutoModel(model_dir={}) load start".format(MODEL_DIR))
t0 = time.time()
model = AutoModel(model_dir=MODEL_DIR)
t_load = time.time() - t0
log("stage-3 LOAD-OK class={} sample_rate={} load_time={:.1f}s".format(type(model).__name__, model.sample_rate, t_load))

if torch.cuda.is_available():
    free, total = torch.cuda.mem_get_info(0)
    log("VRAM after load: free {:.2f} GiB / total {:.2f} GiB".format(free / 2**30, total / 2**30))
log("text_frontend={}".format(getattr(model.frontend, "text_frontend", "?")))

# stage-3b dtype fix: new transformers (>=4.56) loads BlankEN in checkpoint dtype
# (bfloat16) by default, while CosyVoice3LM's own embeddings are float32 and
# cosyvoice3.yaml has no fp16 autocast; upstream code was written against the old
# transformers fp32-load default -> cast Qwen weights back to fp32 in the harness
# (upstream clone left pristine).
qm = model.model.llm.llm.model
qm.float()
log("stage-3b qwen weights cast to {}".format(next(qm.parameters()).dtype))

with open(TEXT_FILE, "r", encoding="utf-8") as f:
    tts_text = f.read().strip()
log("stage-4 inference start text_len={} chars prompt_wav={}".format(len(tts_text), os.path.basename(PROMPT_WAV)))
t1 = time.time()
chunks = []
n = 0
for out in model.inference_cross_lingual(tts_text, PROMPT_WAV, stream=False):
    n += 1
    chunks.append(out["tts_speech"])
    log("chunk {} yielded shape={}".format(n, tuple(out["tts_speech"].shape)))
t_inf = time.time() - t1

import torchaudio
speech = torch.cat(chunks, dim=1)
torchaudio.save(SMOKE_WAV, speech, model.sample_rate)
dur = speech.shape[1] / model.sample_rate
log("stage-5 SMOKE-OK wav={} dur={:.2f}s infer_time={:.1f}s rtf={:.2f}".format(SMOKE_WAV, dur, t_inf, t_inf / max(dur, 0.1)))
log("ALL-STAGES-PASS")
