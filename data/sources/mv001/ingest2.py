# -*- coding: utf-8 -*-
"""mv001 音频入库 v2（路径修正:media/MUSIC/jay 子目录）+ whisper 歌词对轴（本地 faster-whisper·R169 QC recipe）"""
import pathlib, shutil, subprocess, json, sys

SRC = pathlib.Path(r"C:\Users\sjs20\Desktop\FluxGroup\media\MUSIC\jay")
DST = pathlib.Path(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\sources\mv001")
DST.mkdir(parents=True, exist_ok=True)

songs = sorted(SRC.rglob("*.ape")) + sorted(SRC.rglob("*.mp3"))
print("LIBRARY_COUNT", len(songs))

target = next((f for f in songs if "爱在西元前" in f.name), None)
assert target is not None, "target not found in rglob"
copy = DST / target.name
if not copy.exists():
    shutil.copy2(target, copy)

wav = DST / "ai-zai-xi-yuan-qian.wav"
if not wav.exists():
    r = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                        "-i", str(copy), "-ar", "44100", "-ac", "2", str(wav)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("FFMPEG_FAIL", r.stderr[-400:]); sys.exit(1)

probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                       "-of", "json", str(wav)], capture_output=True, text=True,
                      encoding="utf-8", errors="replace")
dur = float(json.loads(probe.stdout)["format"]["duration"])
print("DURATION", round(dur, 2), "s =", f"{int(dur//60)}:{dur%60:04.1f}")

# 全库登记（路径含 jay 子目录如实注记）
cat = pathlib.Path(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\MUSIC-CATALOG.md")
lines = ["# CEO 歌曲资源库登记（media/MUSIC/jay/<专辑>/·2026-10-08 物理件到位·内部草稿用面）", "",
         "> 版权边界=商用发布前逐曲走 JVR 词曲授权（MV 改编发布面清污门）；格式=.ape 无损为主。", ""]
lines += [f"- {f.relative_to(f.parents[1]).as_posix()}（{round(f.stat().st_size/1048576,1)}MB）" for f in songs]
cat.write_text("\n".join(lines), encoding="utf-8")
print("CATALOG", len(songs))

# whisper 歌词对轴（CPU int8·medium·beam5·noctx=R169 QC recipe·不占 CEO 桌面 GPU）
from faster_whisper import WhisperModel
model = WhisperModel("medium", device="cpu", compute_type="int8")
segs, info = model.transcribe(str(wav), language="zh", beam_size=5, vad_filter=True)
rows = [{"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()} for s in segs]
(DST / "whisper_lines.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
srt = "\n".join(f"{i+1}\n{r['start']:0>8.2f}".replace(".", ",") + " --> " +
                f"{r['end']:0>8.2f}".replace(".", ",") + f"\n{r['text']}\n"
                for i, r in enumerate(rows))
(DST / "lyrics-draft.srt").write_text(srt, encoding="utf-8")
print("WHISPER_LINES", len(rows), "| lang", info.language, "| dur", round(info.duration, 1))
for r in rows[:6]:
    print(f"  [{r['start']:7.2f}-{r['end']:7.2f}] {r['text'][:36]}")
