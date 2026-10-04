# r1302 P-2 pilot leg 1: download faster-whisper medium via the production
# self-heal path (HF cache empty = 6th sweep incident, real-time gap anchor),
# then report the snapshot dir path for the pinned-copy step.
import faster_whisper.utils as u

p = u.download_model("medium")
print("DL_PATH:" + p)
