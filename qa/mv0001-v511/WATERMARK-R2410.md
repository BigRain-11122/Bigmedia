# mv0001 V5.11 — invisible watermark pass (R2410, 2026-10-20)

Vehicle: publish-prep open item 1 of `README.md` in this directory
("AIGC badge overlay + VideoSeal invisible watermark not applied").
Executed by BigStream OS loop R2410, mv0001 lane (owner: this loop since
R2403; signed V5.11 FINAL review is R2405).

## Scope decision (before any encode)

The V5.11 FINAL review Note 4 bundles two different things:

1. **Visible in-frame AIGC badge overlay** — REMOVED by CEO order 2026-10-17
   and stays removed. `PUBLISH-CHECKLIST.md` §2 records it verbatim:
   "片内正式标识 (CEO 已删动态) / 按 CEO 令 2026-10-17, AIGC 标识去除, 全删
   (V5.4 起) ... 商业化触发时合规席恢复全检". Burning `aigc_badge.png` into
   the picture now would contradict that order, so it was **not** applied.
   Note 4 is therefore stale on that half; the correction is recorded here
   instead of editing the signed review (append-only evidence face).
2. **Invisible VideoSeal watermark** — required by the same checklist item
   暗水印出库闸 (CEO 2026-10-17 11:0x): apply before any release. This is
   what this round executed.

## Input / output

| role | file | size | note |
|---|---|---|---|
| input (delivery variant) | `cph4/fleet/mv0001-handover/outbound/krea2/30s-reel-v1/full_mv_v511_n1.mp4` | 1,340,088,152 B | audio already under N1 gate |
| output (watermarked delivery) | same dir, `full_mv_v511_wmvs.mp4` | 917,565,589 B | SHA256 `134C980EF147AC5D4341466B74FC33CEC684B07CB7CC799D7E1F5D2C7DB7D685`, MD5 `CCF476441B7185D3FE934B4A5FCEABDC` |

Tool: `mv_videoseal_wm_r1017.py embed <in> <out> 18 fast`
(VideoSeal v1.0.1, Meta MIT, 256-bit embed, 120-bit payload
`大喵没鱼吃` utf-8, 16-frame blocks, `lowres_attenuation=True`, GPU).

## Machine evidence (measured this round)

| item | measured | gate | result |
|---|---|---|---|
| container duration | 234.25 s (00:03:54.25) | = master 234.253 s | PASS |
| video | h264 High, 1344x768, 24 fps, 31.1 Mbps | 768P production | PASS |
| audio | AAC LC 44.1 kHz stereo 262 kbps | stream-copied from `_n1` (bit-identical audio path) | PASS |
| loudness | I = -14.1 LUFS, LRA 5.6 LU | -14 LUFS | PASS |
| true peak | **-1.1 dBFS** (TPK) | <= -1.0 (N1 gate) | PASS (unchanged: audio copied) |
| watermark extraction | **bit-accuracy 100.0 %**, payload `大喵没鱼吃` | full-clip extract 100 % | PASS |
| invisibility (PSNR vs input) | frames 13 samples: min 32.54 / avg 35.73 dB | no visible artifact | PASS (see board) |
| embed wall time | 149 s (37 fps, 5622 frames) | - | - |
| extract wall time | ~85 s (GPU, full clip) | - | - |

## Board read (multimodal, this round)

`WM-VIS-BOARD-VS.jpg` = 3 rows x [original | watermarked | x24 amplified diff],
frames 1200 / 2400 / 3600.

- Left vs middle: indistinguishable at 1:1 — no color cast, no blur, no black
  lift, no ringing on subtitle glyphs, brick/stele texture equally crisp.
- Amplified diff column: diffuse full-frame dither speckle, **no 8x8/16x16
  block structure, no banding, no macroblock grid**. Residual is faintly
  content-correlated (perceptual masking) and non-zero in flat dark areas —
  cosmetic at this amplitude.
- No quality defect found in the watermarked column.

## Carried notes

- The watermark encode is a second generation (crf18 fast, 45.7 -> 31.1 Mbps),
  so the master `full_mv_v511.mp4` stays the archival source of record. The
  `_wmvs` file is the publish-facing copy, matching the existing line
  (`full_mv_v57_wmvs.mp4` / `_v58_wmvs` / `_v59_wmvs` / `_v51_proxy_wmvs`).
- The visible badge question reopens only on a commercialization trigger
  (compliance seat restores the full checklist), per CEO 2026-10-17.
- Still open from `README.md`: original-song licensing / platform account
  (CEO physical items), and director notes 1-3 of the FINAL review.

## Repro

```
$PY = C:\Users\sjs20\comfyui-krea\ComfyUI_windows_portable\python_embeded\python.exe
& $PY mv_videoseal_wm_r1017.py embed  full_mv_v511_n1.mp4 full_mv_v511_wmvs.mp4 18 fast
& $PY mv_videoseal_wm_r1017.py extract full_mv_v511_wmvs.mp4          # expect bit-acc 100%
& $PY mv_videoseal_wm_r1017.py psnr   full_mv_v511_n1.mp4 full_mv_v511_wmvs.mp4
& $PY mv_videoseal_wm_r1017.py board  full_mv_v511_n1.mp4 full_mv_v511_wmvs.mp4 1200,2400,3600
```

Logs: `v511_wm_embed.log` (+ `.err` = ffmpeg progress), `v511_wm_extract.log`.