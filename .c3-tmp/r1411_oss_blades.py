# -*- coding: utf-8 -*-
# r1411_oss_blades.py - OSS harvest window 4 slice 2 (P-2026-09-26-08; remaining-slice honest close)
# blade faces: (1) zh text auto-correction lib face (predicted design-level reject: QC honesty law);
# (2) ASR alignment metric lib face (predicted reject: in-house asr-diff in service, no flag);
# (3) local zero-API: w2 parked dual-track reopen-condition recheck (whisper.cpp env axis + SenseVoice zh axis)
# API budget: 2 calls this slice -> window total 4+2=6 <= 6 cap (politeness law)
# ASCII source per encoding law; output UTF-8
import json, time, urllib.request, io, os, glob, re

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = io.open(repo + r"\.c3-tmp\r1411_oss_blades.txt", "w", encoding="utf-8")
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

# blade 1 (API call 1 of 2): zh text auto-correction face
blade("blade1 chinese text correction python", "https://api.github.com/search/repositories?q=chinese+text+correction+python&sort=stars&per_page=6")

# blade 2 (API call 2 of 2): ASR alignment metric lib face (jiwer canonical)
blade("blade2 jiwer wer cer", "https://api.github.com/search/repositories?q=jiwer&sort=stars&per_page=6")

# blade 3 (local, zero API): w2 parked dual-track reopen-condition recheck
w("== local parked recheck ==\n")
# whisper.cpp env axis: reopen = HF-hub-type blockage recurs AND HF_HUB_OFFLINE=1 mitigation fails
# evidence: R1410 P-3 A/B ran 4 transcriptions pinned+HF_HUB_OFFLINE=1 zero hub contact (state log R1410)
mdl = repo + r"\data\assets\models\faster-whisper-medium"
w("pinned_medium_model_exists=%s files=%s\n" % (os.path.exists(mdl), len(glob.glob(mdl + r"\*")) if os.path.exists(mdl) else 0))
p3 = repo + r"\.c3-tmp\r1410_p3_ab.txt"
if os.path.exists(p3):
    t = io.open(p3, encoding="utf-8").read()
    rates = re.findall(r"noise_rate[^\d]*([\d.]+)", t)
    w("p3_noise_rates=%s (SenseVoice trigger-A line = >=40pct diff x2 consecutive; in-band = untriggered)\n" % rates[:8])
else:
    w("p3_evidence_file=MISSING\n")
# SenseVoice trigger-B evidence: homophone adjudication never >0.5 round budget (in-round log lines; no bottleneck flag in state log tail)
st = json.load(io.open(repo + r"\src\os\state.json", encoding="utf-8"))
tail = "\n".join(st.get("log", [])[-6:])
w("state_log_tail_mentions_bottleneck=%s\n" % ("瓶颈" in tail))
w("hf_hub_blockage_recent=%s (R1410 four transcriptions zero hub contact per log)\n" % ("HF hub" in tail))

out.close()
print("done")
