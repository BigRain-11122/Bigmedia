# R1786 QC leg: R169 recipe ASR (medium int8 beam5 noctx) on narrator concat + 5 character wavs
# + trailing-silence detect on character wavs. ASCII law; Chinese only in data/outputs.
import os, subprocess, json

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
MD = os.path.join(BASE, "data", "storylines", "drama", "md0001", "tts")
SEG = os.path.join(MD, "segments")

targets = [("narrator", os.path.join(MD, "narrator", "audio.mp3"))]
for f in sorted(os.listdir(SEG)):
    if f.endswith(".wav"):
        targets.append((f, os.path.join(SEG, f)))

from faster_whisper import WhisperModel
wm = WhisperModel("medium", device="cpu", compute_type="int8")
out = {}
for name, path in targets:
    segs, info = wm.transcribe(path, beam_size=5, condition_on_previous_text=False, language="zh")
    txt = "".join(s.text for s in segs).replace(" ", "")
    out[name] = txt
    print("%s: %s" % (name, txt), flush=True)

json.dump(out, open(os.path.join(MD, "qc-r1786-asr-medium.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("--- silencedetect (tail silences >=0.4s) ---")
for f in sorted(os.listdir(SEG)):
    if not f.endswith(".wav"):
        continue
    r = subprocess.run(["ffmpeg", "-i", os.path.join(SEG, f), "-af",
                        "silencedetect=noise=-40dB:d=0.4", "-f", "null", "-"],
                       capture_output=True, text=True)
    for ln in r.stderr.splitlines():
        if "silence_" in ln:
            print(f, ln.strip())
print("QC-DONE")
