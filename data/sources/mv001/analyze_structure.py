# -*- coding: utf-8 -*-
"""mv001 结构分析 v2：能量分帧→段落/节拍检测（纯本地·无模型）+ whisper 无VAD重对轴
输出 structure.json：{duration, beat_grid, sections[]（能量聚类段落）, lines[]（whisper 或能量近似）}"""
import json, subprocess, pathlib, sys
import numpy as np

DST = pathlib.Path(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\sources\mv001")
WAV = DST / "ai-zai-xi-yuan-qian.wav"

# 1) pcm 读入（ffmpeg → raw s16 mono 16k）
r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(WAV), "-ac", "1", "-ar", "16000",
                    "-f", "s16le", "-"], capture_output=True)
pcm = np.frombuffer(r.stdout, dtype=np.int16).astype(np.float32) / 32768.0
sr = 16000
dur = len(pcm) / sr
print("PCM", round(dur, 1), "s")

# 2) 分帧能量（50ms hop）
hop = int(0.05 * sr)
n = len(pcm) // hop
e = np.array([np.sqrt(np.mean(pcm[i*hop:(i+1)*hop]**2)) + 1e-9 for i in range(n)])
fe = 20 * np.log10(e)  # dB
# 平滑
k = 6
sm = np.convolve(fe, np.ones(k)/k, mode="same")

# 3) 节拍网格：能量峰（onset 近似）自相关估 BPM
thr = np.percentile(sm, 62)
onset = (sm[1:-1] > sm[:-2]) & (sm[1:-1] > sm[2:]) & (sm[1:-1] > thr)
oi = np.where(onset)[0] * 0.05
# 自相关求主周期（0.3-1.2s 即 50-200BPM）
lag_lo, lag_hi = int(0.3/0.05), int(1.2/0.05)
ac = np.array([np.mean(onset[i:i+200].astype(float) @ np.zeros(1) if False else 0) for i in []]) # placeholder
# 简化：直接统计相邻 onset 中位间隔
if len(oi) > 4:
    d = np.diff(oi)
    d = d[(d > 0.28) & (d < 1.3)]
    beat = float(np.median(d)) if len(d) else 0.5
else:
    beat = 0.5
bpm = 60.0 / beat
print("BEAT_EST", round(beat, 3), "s ≈", round(bpm, 1), "BPM")

# 4) 段落：能量长期包络变点（滑窗均值差 > 3dB 处切割·最小段 8s）
w = int(4 / 0.05)  # 4s 窗
lo = np.convolve(sm, np.ones(w)/w, mode="same")
cuts = [0.0]
i = w
last = 0
while i < n - w:
    if abs(lo[i] - lo[last]) > 3.0 and (i*0.05 - last*0.05) > 8:
        cuts.append(round(i*0.05, 2)); last = i
    i += w
cuts.append(round(dur, 2))
secs = [{"s": cuts[j], "e": cuts[j+1], "db": round(float(np.mean(sm[int(cuts[j]/0.05):int(cuts[j+1]/0.05)])), 1)}
        for j in range(len(cuts)-1)]
print("SECTIONS", len(secs))
for s in secs:
    print(f"  {s['s']:6.1f}-{s['e']:6.1f} {s['db']:5.1f}dB")

# 5) whisper 重对轴（无 VAD·word_timestamps 换行级）
lines = []
try:
    from faster_whisper import WhisperModel
    m = WhisperModel("medium", device="cpu", compute_type="int8")
    segs, info = m.transcribe(str(WAV), language="zh", beam_size=5, vad_filter=False,
                              condition_on_previous_text=False)
    lines = [{"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()} for s in segs if s.text.strip()]
    print("WHISPER_NOVAD_LINES", len(lines))
    for l in lines[:10]:
        print(f"  [{l['start']:7.2f}-{l['end']:7.2f}] {l['text'][:38]}")
except Exception as ex:
    print("WHISPER_FAIL", str(ex)[:200])

out = {"duration": round(dur, 2), "beat": round(beat, 3), "bpm": round(bpm, 1),
       "sections": secs, "lines": lines}
(DST / "structure.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("SAVED structure.json")
