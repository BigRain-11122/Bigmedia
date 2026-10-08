# R1786 disambiguation probe: short line via cross_lingual + repo human prompt wav
import sys, os, time
BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
REPO = os.path.join(BASE, "data", "assets", "cosyvoice-runtime", "CosyVoice")
sys.path.insert(0, os.path.join(REPO, "third_party", "Matcha-TTS"))
sys.path.insert(0, REPO)
import torch
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
model = AutoModel(model_dir=MODEL_DIR)
model.model.llm.llm.model.float()
PROMPT_WAV = os.path.join(REPO, "asset", "zero_shot_prompt.wav")
OUT = os.path.join(BASE, ".c3-tmp", "r1786_probe_shot7_crosslingual.wav")
t1 = time.time()
chunks = []
for out in model.inference_cross_lingual(
        "You are a helpful assistant.<|endofprompt|>台风天的日志最见人品。", PROMPT_WAV, stream=False):
    chunks.append(out["tts_speech"])
speech = torch.cat(chunks, dim=1)
_ta.save(OUT, speech, model.sample_rate)
print("PROBE dur=%.2fs infer=%.1fs" % (speech.shape[1] / model.sample_rate, time.time() - t1), flush=True)
from faster_whisper import WhisperModel
wm = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = wm.transcribe(OUT, beam_size=5, condition_on_previous_text=False, language="zh")
print("ASR:", "".join(s.text for s in segs), flush=True)
