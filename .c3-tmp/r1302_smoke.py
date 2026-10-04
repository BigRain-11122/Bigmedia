# r1302 P-2 judgment smoke: judgment-1 (cleared-cache simulation) +
# judgment-2 (offline + pinned load). HF_HOME points at an empty temp
# dir = the hf-cache state right after a disk sweep; the pinned copy
# must load with zero hub contact and transcribe the QC-recipe way.
import os
import sys
import tempfile

os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["HF_HOME"] = tempfile.mkdtemp(prefix="bs-empty-hf-")  # simulated 7th sweep

sys.path.insert(0, "src/render")
import whisper_to_srt as w2s  # noqa: E402

audio = sys.argv[1]
resolved = w2s.resolve_model("medium")
print("RESOLVED_MODEL: " + resolved)
assert os.path.isdir(resolved) and resolved.endswith("faster-whisper-medium"), \
    "resolver did not pick the pinned dir"

cues, dropped, dur = w2s.transcribe_to_cues(
    audio, "medium", beam_size=5, condition_on_previous_text=False)
print("SMOKE_OK cues=%d dropped=%d audio_dur=%.2fs" % (len(cues), dropped, dur))
print("FIRST_CUE: " + cues[0][2][:50])
