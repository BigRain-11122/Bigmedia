# -*- coding: utf-8 -*-
"""快速能量结构（whisper 未归时的科学替代：节拍+段落能量判据·秒级）"""
import json, subprocess, pathlib
import numpy as np

DST = pathlib.Path(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\sources\mv001")
WAV = DST / "ai-zai-xi-yuan-qian.wav"
r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(WAV), "-ac", "1", "-ar", "16000",
                    "-f", "s16le", "-"], capture_output=True)
pcm = np.frombuffer(r.stdout, dtype=np.int16).astype(np.float32) / 32768.0
sr = 16000
hop = int(0.05 * sr)
n = len(pcm) // hop
e = np.array([np.sqrt(np.mean(pcm[i*hop:(i+1)*hop]**2)) + 1e-9 for i in range(n)])
sm = np.convolve(20*np.log10(e), np.ones(6)/6, mode="same")
thr = np.percentile(sm, 62)
onset = (sm[1:-1] > sm[:-2]) & (sm[1:-1] > sm[2:]) & (sm[1:-1] > thr)
oi = np.where(onset)[0] * 0.05
d = np.diff(oi); d = d[(d > 0.28) & (d < 1.3)]
beat = float(np.median(d)) if len(d) else 0.5
w = int(4 / 0.05)
lo = np.convolve(sm, np.ones(w)/w, mode="same")
cuts, last, i = [0.0], 0, w
while i < n - w:
    if abs(lo[i] - lo[last]) > 3.0 and (i - last) * 0.05 > 8:
        cuts.append(round(i * 0.05, 2)); last = i
    i += w
cuts.append(round(len(pcm)/sr, 2))
secs = [{"s": cuts[j], "e": cuts[j+1], "db": round(float(np.mean(sm[int(cuts[j]/0.05):int(cuts[j+1]/0.05)])), 1)}
        for j in range(len(cuts)-1)]
out = {"duration": round(len(pcm)/sr, 2), "beat": round(beat, 3), "bpm": round(60/beat, 1),
       "sections": secs, "lines": [], "source": "energy-quick (whisper in flight)"}
(DST / "structure.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("BPM", out["bpm"], "| SECTIONS", [(s['s'], s['e'], s['db']) for s in secs])
