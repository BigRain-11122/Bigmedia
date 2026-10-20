# mv0001 V5.11 — AIGC implicit metadata pass (R2413, 2026-10-20)

Vehicle: the last open copy-side blocker in `DELIVERY-PACK-V511.json`
("GB 45438-2025 metadata fields in the media file"). Executed by BigStream
OS loop R2413 on the mv0001 lane, on top of the R2410 watermark pass and the
R2411/R2412 delivery + publish-copy packs.

## Why this is legal to do before accounts open

《人工智能生成合成内容标识办法》第五条 / GB 45438-2025 put the implicit-label
(metadata) duty on the **generation service provider**, not on the publishing
user; the publishing user's duty is the 第十条 declaration (already carried by
`docs/publish/mv0001-v511/AIGC-DECLARATION.md`). Writing the tag is therefore a
**voluntary compliance enhancement on the delivery file**, not a publish action:
nothing is uploaded, no account is touched, and the M5 gate stays closed.

## Field source (in-repo canon, not invented)

`docs/research/R-20260927-bigstream-04-aigc-labeling-recsys-weekly-scan.md`
§10.1 (v1.2) records TC260-PG-20257A V1.0-202508 appendix E verbatim:

    {"Label","ContentProducer","ProduceID","ReservedCode1",
     "ContentPropagator","PropagateID","ReservedCode2"}

Storage: `moov.udta.meta` (keys key=`AIGC`, ilst value=JSON). ffmpeg form:
`-metadata AIGC='<json>' -movflags use_metadata_tags -c copy`.

## Input / output

| role | file | size |
|---|---|---|
| input | `cph4/fleet/mv0001-handover/outbound/krea2/30s-reel-v1/full_mv_v511_wmvs.mp4` | 917,565,589 B |
| output | same dir, `full_mv_v511_wmvs_aigc.mp4` | 917,566,040 B (+451 B of metadata box) |

Tool: `src/aigc_metadata.py` (new, reusable; `--in/--out` embed, `--verify`
readback gate; same ASCII/exit-code conventions as the other `src/*_check.py`
gates). Payload written:

    {"Label":"AIGC","ContentProducer":"FluxGroup BigStream",
     "ProduceID":"BS-MV0001-V511-20261020","ReservedCode1":"",
     "ContentPropagator":"","PropagateID":"","ReservedCode2":""}

`ContentPropagator` / `PropagateID` are intentionally empty: per the standard
they are filled by the **propagating platform** at distribution time, so a
publisher-side file cannot pre-empt them. `ReservedCode1/2` stay empty
(reserved fields, no assigned meaning for this line yet).

## Machine evidence (measured this round)

| item | measured | gate | result |
|---|---|---|---|
| readback | `ffprobe` shows tag `AIGC` with all 7 fields, JSON parses | 7/7 present, Label/ContentProducer/ProduceID non-empty | PASS |
| video stream MD5 | `e2760d2ca2b2fbff0f909038a2021021` (in == out) | stream copy, must be bit-identical | PASS |
| audio stream MD5 | `1ed2f4d5e62e538c7cf5571e9460a5b9` (in == out) | stream copy, must be bit-identical | PASS |
| duration / frames | 234.253 s / 5622 frames / 24 fps | = signed master | PASS |
| platform gate (B站) | 1344x768 = 16:9, 234.25 s in 180-900 s | `src/platform_spec_check.py` | PASS |

Bit-identical video and audio streams mean the R2410 VideoSeal payload and the
R2405 audio gate readings (`TP -1.1 dBTP`, `I -14.1 LUFS`) carry over unchanged —
a remux cannot alter them, and this is proven, not assumed.

Verification commands reproducible as:

    python src/aigc_metadata.py --verify "…/full_mv_v511_wmvs_aigc.mp4"
    ffmpeg -v error -i FILE -map 0:v -c copy -f md5 -   # same on both files
    ffmpeg -v error -i FILE -map 0:a -c copy -f md5 -

## Effect on the publish checklist

- `DELIVERY-PACK-V511.json` — `delivery_file` now points at the `_aigc` variant;
  the metadata blocker moves from `open_blockers` to a closed `aigc_metadata`
  block with the measured values.
- `docs/publish/mv0001-v511/AIGC-DECLARATION.md` §四 — "尚未补写" is now stale;
  replaced with the closed state + this file as the evidence pointer.
- `docs/publish/mv0001-v511/BILIBILI-DESC.md` §五 — metadata checkbox ticked;
  the upload-body line now names the `_aigc` file.

## Remaining publish-side blockers (unchanged, not ours to close)

1. Platform accounts not open — CEO physical item (`docs/accounts.md`).
2. M4 gates: 6/10 drafts not GATE PASS (see `readiness.py` section 2).
3. 原曲授权口径 (清单 §一-1) — CEO channel decision.