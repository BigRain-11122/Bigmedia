# -*- coding: utf-8 -*-
# r1409_oss_blades.py - OSS harvest window 4 slice 1 (P-2026-09-26-08; opens 21:40 10-05)
# blade faces: (1) audio loudness face per R1034 next-window pointer (predicted no-workstation);
# (2) ASR proper-noun hotword face - real recurring in-case flag (M6 calibration-line annotations);
# profit lens wired per P-2026-10-04-02 (3-type benefit tagging + monetizable upweight + toy downweight)
# ASCII source per encoding law; output UTF-8
import json, time, urllib.request, io, inspect

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = io.open(repo + r"\.c3-tmp\r1409_oss_blades.txt", "w", encoding="utf-8")
w = out.write

def get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "bigstream-oss-harvest",
        "Accept": "application/vnd.github+json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except Exception as e:
        return {"ERROR": str(e)}

def blade(tag, url):
    d = get(url)
    w("== %s ==\n" % tag)
    if "ERROR" in d:
        w("ERROR " + d["ERROR"] + "\n")
        return
    items = d.get("items", [])
    w("total_count=%s\n" % d.get("total_count"))
    for it in items[:6]:
        lic = (it.get("license") or {}).get("spdx_id")
        w("%s | lic=%s | stars=%s | push=%s | arch=%s | lang=%s | %s\n" % (
            it.get("full_name"), lic, it.get("stargazers_count"),
            it.get("pushed_at"), it.get("archived"), it.get("language"),
            (it.get("description") or "")[:110]))
    time.sleep(1)

# blade 1: audio loudness face (R1034 pointer prediction: no workstation)
blade("blade1 ffmpeg loudnorm python", "https://api.github.com/search/repositories?q=ffmpeg+loudnorm+python&sort=stars&per_page=6")

# direct fetch: pyloudnorm (known EBU R128 loudness measurement lib)
d = get("https://api.github.com/repos/csteinmetz1/pyloudnorm")
w("== direct csteinmetz1/pyloudnorm ==\n")
if "ERROR" in d:
    w("ERROR " + d["ERROR"] + "\n")
else:
    lic = (d.get("license") or {}).get("spdx_id")
    w("lic=%s stars=%s forks=%s push=%s arch=%s lang=%s desc=%s\n" % (
        lic, d.get("stargazers_count"), d.get("forks_count"),
        d.get("pushed_at"), d.get("archived"), d.get("language"),
        (d.get("description") or "")[:140]))
time.sleep(1)

# blade 2: ASR hotword face (whisper hotwords/initial-prompt biasing ecosystem)
blade("blade2 whisper hotwords", "https://api.github.com/search/repositories?q=whisper+hotwords&sort=stars&per_page=6")

# blade 3 (local stack inspection, zero-network): installed faster-whisper version + hotwords param support
w("== local faster-whisper inspection ==\n")
try:
    import faster_whisper
    w("faster_whisper_version=%s\n" % getattr(faster_whisper, "__version__", "unknown"))
    from faster_whisper import WhisperModel
    params = list(inspect.signature(WhisperModel.transcribe).parameters)
    w("transcribe_has_hotwords=%s\n" % ("hotwords" in params))
    w("transcribe_has_initial_prompt=%s\n" % ("initial_prompt" in params))
except Exception as e:
    w("local_inspection_exc=%s %s\n" % (type(e).__name__, str(e)[:200]))

# local evidence: ffmpeg loudnorm filter built-in (anti-repeat gate evidence)
import subprocess
try:
    p = subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True, timeout=60)
    txt = (p.stdout or b"").decode("utf-8", "replace")
    w("ffmpeg_loudnorm_filter_present=%s\n" % ("loudnorm" in txt))
except Exception as e:
    w("ffmpeg_check_exc=%s\n" % type(e).__name__)

out.close()
print("done")
