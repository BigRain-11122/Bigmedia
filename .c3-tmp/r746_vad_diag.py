# -*- coding: utf-8 -*-
# R746 ASR degradation diagnosis: VAD on/off raw segment comparison on .lc019-tmp/audio.mp3
import os
os.environ["HF_HUB_OFFLINE"] = "1"
from faster_whisper import WhisperModel

model = WhisperModel("medium", device="cpu", compute_type="int8")

for vad in (True, False):
    segs, info = model.transcribe(
        r".lc019-tmp/audio.mp3", language="zh", word_timestamps=True,
        vad_filter=vad, beam_size=5, condition_on_previous_text=False)
    print("=== vad_filter=%s ===" % vad)
    for s in segs:
        txt = s.text.strip()
        print("%.2f-%.2f | %s" % (s.start, s.end, txt[:60]))
print("DIAG_DONE")
