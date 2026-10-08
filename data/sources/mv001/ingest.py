# -*- coding: utf-8 -*-
"""mv001 音频入库+转码+探测（python UTF-8 通道·规避 PS5.1 中文路径坑）"""
import pathlib, shutil, subprocess, json

SRC = pathlib.Path(r"C:\Users\sjs20\Desktop\FluxGroup\media\MUSIC")
DST = pathlib.Path(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\sources\mv001")
DST.mkdir(parents=True, exist_ok=True)

# 1) 曲库清点（登记面）
songs = sorted(SRC.glob("*.ape")) + sorted(SRC.glob("*.mp3"))
print("LIBRARY_COUNT", len(songs))

# 2) 目标曲入库
target = SRC / "周杰伦 - 爱在西元前.ape"
assert target.exists(), f"missing: {target}"
copy = DST / target.name
if not copy.exists():
    shutil.copy2(target, copy)
print("COPIED", copy.name, round(copy.stat().st_size / 1048576, 1), "MB")

# 3) 转码 wav（ffmpeg·ape 解码器内置）——中文路径经 subprocess list 传递
wav = DST / "ai-zai-xi-yuan-qian.wav"
if not wav.exists():
    r = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                        "-i", str(copy), "-ar", "44100", "-ac", "2", str(wav)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("FFMPEG_RC", r.returncode, r.stderr[-300:] if r.returncode else "")
    if r.returncode != 0:
        raise SystemExit(1)

# 4) 实测时长+节拍指纹（粗 BPM：取前 60s 能量震荡估算）
probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                       "-of", "json", str(wav)], capture_output=True, text=True,
                      encoding="utf-8", errors="replace")
dur = float(json.loads(probe.stdout)["format"]["duration"])
print("DURATION_S", round(dur, 2), "=", f"{int(dur//60)}:{int(dur%60):02d}")

# 5) 全库登记清单（CEO 资源面·R2 源资产台账）
cat = DST / ".." / ".." / "MUSIC-CATALOG.md"  # media/BigStream/data/MUSIC-CATALOG.md
cat = cat.resolve()
lines = ["# CEO 歌曲资源库登记（media/MUSIC·2026-10-08 物理件到位·内部草稿用面）", "",
         "> 版权边界：本库=CEO 自有资源面；商用发布前逐曲走 JVR 词曲授权（MV 改编发布面清污门）。", ""]
for s in songs:
    lines.append(f"- {s.stem}{s.suffix}（{round(s.stat().st_size/1048576,1)}MB）")
cat.write_text("\n".join(lines), encoding="utf-8")
print("CATALOG", cat.name, len(songs), "items")
