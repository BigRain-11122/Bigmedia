# -*- coding: utf-8 -*-
# R746 LC-019 ASR supplementary coverage pass: vad_filter=False variant.
# Context: QC recipe (medium-int8+beam5+noctx via whisper_to_srt.py) stably drops
# b7-b10 (27.667-47.516s) on this audio - tool hardcodes vad_filter=True (never part
# of the R169 recipe text). This pass reuses build_cues/clamp_overlaps/write_srt
# from the same tool, only flipping vad_filter, to verify the VAD-drop hypothesis
# and give the S2 seat a full-coverage fact-word reading.
import os, sys
os.environ["HF_HUB_OFFLINE"] = "1"
sys.path.insert(0, r"src/render")
from pathlib import Path
sys.path.insert(0, str(Path(r"src/render").resolve()))
from whisper_to_srt import build_cues
from srt_fix import clamp_overlaps, write_srt
from faster_whisper import WhisperModel

model = WhisperModel("medium", device="cpu", compute_type="int8")
segments, info = model.transcribe(
    r".lc019-tmp/audio.mp3", language="zh", word_timestamps=True,
    vad_filter=False, beam_size=5, condition_on_previous_text=False)
words = []
for seg in segments:
    for w in (seg.words or []):
        words.append({"start": w.start, "end": w.end, "word": w.word})
cues = build_cues(words, 20)
fixed, dropped = clamp_overlaps(cues)
write_srt(fixed, r".lc019-tmp/asr-check-novad.srt")
print("OK novad cues=%d dropped=%d audio_dur=%.2fs" % (len(fixed), dropped, float(info.duration)))
