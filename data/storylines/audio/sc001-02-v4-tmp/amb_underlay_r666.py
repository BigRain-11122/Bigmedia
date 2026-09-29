# -*- coding: utf-8 -*-
# R666 ambience underlay mix for SC-001-02-v4 (R-20260928-bigstream-04 top1-benchmarks L53 recipe:
# low-level ambient layer ~-18dB under voice; product content layer, not BGM burn - D-BS-02 unaffected).
# Zero external assets: beds self-synthesized with ffmpeg lavfi (anoisesrc/sine) = no copyright surface.
# Full-day scene-arc design for ch2 benchmark (v4 TOP1 leg3 auto-inherit):
#   bed A = pre-dawn/night plaza (brown noise low band + faint 55Hz hum = tower hum + city rumble)
#   bed B = steamer warm bed (pink noise mid band + breathing tremolo = stove/fire strand)
#   arc = A (open, pre-dawn) --xf--> B (stove ignites "炉子点起来") --xf--> A (dusk/night "天擦黑")
import io, os, re, subprocess, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
TMP = HERE
VOICE = os.path.join(TMP, "audio.mp3")
SRT = os.path.join(TMP, "subs.srt")
BED_A1 = os.path.join(TMP, "amb-bedA1.wav")
BED_A2 = os.path.join(TMP, "amb-bedA2.wav")
BED_B = os.path.join(TMP, "amb-bedB.wav")
BED_X1 = os.path.join(TMP, "amb-bed-AB.wav")
BED_X = os.path.join(TMP, "amb-bed.wav")
OUT = os.path.join(ROOT, "data", "storylines", "audio", "SC-001-02-v4.mp3")

report = {}
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("FAIL cmd: %s" % " ".join(cmd))
        print(r.stderr[-1600:])
        sys.exit(1)
    return r

def probe_dur(path):
    r = run(["ffmpeg", "-i", path, "-f", "null", "-"])
    m = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        m2 = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", r.stderr)
        h, mi, s = m2.groups()
        return int(h) * 3600 + int(mi) * 60 + float(s)
    h, mi, s = m.groups()
    return int(h) * 3600 + int(mi) * 60 + float(s)

def mean_vol(path):
    r = run(["ffmpeg", "-i", path, "-af", "volumedetect", "-f", "null", "-"])
    m = re.search(r"mean_volume: (-?\d+\.?\d*) dB", r.stderr)
    return float(m.group(1))

def srt_time_to_s(t):
    h, m, rest = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(rest.replace(",", "."))

with io.open(SRT, encoding="utf-8") as f:
    srt = f.read()
blocks = re.split(r"\n\n+", srt.strip())
t1 = None  # stove-ignition turn cue
t2 = None  # dusk cue
for b in blocks:
    lines = b.splitlines()
    if len(lines) >= 3:
        body = "\n".join(lines[2:])
        if t1 is None and "炉子点起来" in body:
            t1 = srt_time_to_s(lines[1].split("-->")[0].strip())
        if t2 is None and "天擦黑" in body:
            t2 = srt_time_to_s(lines[1].split("-->")[0].strip())
assert t1 is not None, "stove-ignition cue not found in SRT"
assert t2 is not None, "dusk cue not found in SRT"
assert t2 > t1, "dusk cue must follow ignition cue"
report["ignition_cue_s"] = round(t1, 2)
report["dusk_cue_s"] = round(t2, 2)

dur = probe_dur(VOICE)
report["voice_dur_s"] = round(dur, 2)
xf = 3.0  # crossfade seconds
a1_dur = max(t1 + xf / 2, 2.0)
b_dur = max(t2 - t1 + xf, 2.0)
a2_dur = max(dur - t2 + xf / 2, 2.0)

def bed_cold(path, d):
    run(["ffmpeg", "-y",
         "-f", "lavfi", "-t", "%.3f" % d, "-i", "anoisesrc=colour=brown:sample_rate=44100:amplitude=0.5",
         "-f", "lavfi", "-t", "%.3f" % d, "-i", "sine=frequency=55:sample_rate=44100",
         "-filter_complex",
         "[0:a]highpass=f=35,lowpass=f=420,tremolo=f=0.22:d=0.25[n];"
         "[1:a]volume=0.06[s];"
         "[n][s]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.9[a]",
         "-map", "[a]", path])

def bed_warm(path, d):
    run(["ffmpeg", "-y",
         "-f", "lavfi", "-t", "%.3f" % d, "-i", "anoisesrc=colour=pink:sample_rate=44100:amplitude=0.4",
         "-f", "lavfi", "-t", "%.3f" % d, "-i", "anoisesrc=colour=brown:sample_rate=44100:amplitude=0.3",
         "-filter_complex",
         "[0:a]bandpass=f=900:width_type=h:width=1200,tremolo=f=0.14:d=0.35[p];"
         "[1:a]highpass=f=40,lowpass=f=300[b];"
         "[p][b]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.9[a]",
         "-map", "[a]", path])

bed_cold(BED_A1, a1_dur)
bed_warm(BED_B, b_dur)
bed_cold(BED_A2, a2_dur)
# chain crossfades: A1 -> B -> A2
run(["ffmpeg", "-y", "-i", BED_A1, "-i", BED_B,
     "-filter_complex", "acrossfade=d=%.2f:c1=tri:c2=tri[a]" % xf,
     "-map", "[a]", BED_X1])
run(["ffmpeg", "-y", "-i", BED_X1, "-i", BED_A2,
     "-filter_complex", "acrossfade=d=%.2f:c1=tri:c2=tri[a]" % xf,
     "-map", "[a]", BED_X])

# level: bed mean_volume ~= voice mean_volume - 18 dB (recipe quantified interpretation)
v_mv = mean_vol(VOICE)
b_mv = mean_vol(BED_X)
gain = (v_mv - 18.0) - b_mv
report["voice_mean_db"] = v_mv
report["bed_raw_mean_db"] = b_mv
report["bed_gain_db"] = round(gain, 1)
report["bed_target_mean_db"] = round(v_mv - 18.0, 1)

run(["ffmpeg", "-y", "-i", VOICE, "-i", BED_X,
     "-filter_complex",
     "[1:a]volume=%.1fdB,atrim=duration=%.3f,asetpts=N/SR/TB[b];"
     "[0:a][b]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,"
     "alimiter=limit=0.95[a]" % (gain, dur),
     "-map", "[a]", "-ar", "44100", OUT])

report["out_dur_s"] = round(probe_dur(OUT), 2)
report["out_mean_db"] = mean_vol(OUT)
with io.open(os.path.join(TMP, "amb-mix-r666.json"), "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=1)
print("OK ignition=%.2fs dusk=%.2fs voice=%.2fs bed_gain=%.1fdB out=%.2fs out_mean=%.1fdB" % (
    report["ignition_cue_s"], report["dusk_cue_s"], report["voice_dur_s"], report["bed_gain_db"],
    report["out_dur_s"], report["out_mean_db"]))
