# DIRECTOR REVIEW — V5.11 DELIVERY ADDENDUM (publish copy signoff)

- Date: 2026-10-20 (BigStream OS loop R2411)
- Parent verdict: `cph4/fleet/mv0001-handover/outbound/krea2/30s-reel-v1/DIRECTOR-REVIEW-V511-FINAL-20261020.md` (R2405, PASS)
- Addendum scope: sign the **watermarked delivery copy** and refresh the one
  stale carried note. No picture change, no re-render.
- Repo note: this file lives in the BigStream repo (write boundary); the review
  it amends lives in the group MV canon directory (read-only from here).

## Delivery copy under review

`cph4/fleet/mv0001-handover/outbound/krea2/30s-reel-v1/full_mv_v511_wmvs.mp4`

| item | measured this round | expected | result |
|---|---|---|---|
| container | 234.253 s / 917,565,589 B | 234.25 s target | PASS |
| video | h264 1344x768 24/1, **5622 frames**, 31.10 Mbps | 768P production | PASS |
| audio | AAC 2ch 262 kbps, stream-copied from `full_mv_v511_n1.mp4` | copy, no re-encode | PASS |
| true peak | **-1.1 dBTP** (ffmpeg ebur128, this round) | <= -1.0 | PASS |
| loudness | **I = -14.1 LUFS / LRA 5.6 LU** | -14 LUFS | PASS |
| invisible watermark | VideoSeal embed 149 s / 37 fps / 5622 frames; extract bit-accuracy **100.0 %** (`v511_wm_extract.log`) | payload survives full clip | PASS |
| platform gate B站 | 16:9 PASS / 234.25 s inside 180-900 s | 16:9 · 3-15 min | PASS |
| platform gate YouTube | 16:9 PASS / duration unchecked (no range in playbook) | 16:9 | PASS |

Re-run commands (this round, BigStream repo):

```
python src/platform_spec_check.py --video <wmvs> --platform B站
python src/platform_spec_check.py --video <wmvs> --platform YouTube
```

Note: 9:16 short-video platforms (视频号/抖音/快手/TikTok/小红书) are **out of
window for this cut** — the piece is a 234 s 16:9 MV, so a vertical derivative
is a separate deliverable, not a spec failure of this one.

## Note 4 refresh (supersedes the stale half, not the verdict)

The FINAL review Note 4 said "AIGC badge overlay + VideoSeal invisible watermark
are NOT yet applied". Both halves are now resolved for the delivery copy:

1. **Invisible watermark — APPLIED** (`full_mv_v511_wmvs.mp4`), evidence
   `qa/mv0001-v511/WATERMARK-R2410.md` + `WM-VIS-BOARD-VS.jpg`.
2. **Visible in-frame AIGC badge — deliberately NOT burned in**, per CEO order
   2026-10-17 (`PUBLISH-CHECKLIST.md` §2 removes the in-frame mark). The AIGC
   declaration travels as platform-level labelling + description copy at publish
   time, which is still a hard precondition (AIGC 显著标识 = 硬法).

The archival master `full_mv_v511.mp4` (45.7 Mbps) stays untouched as source of
record; it is not the upload artifact.

## Carried notes unchanged

Notes 1-3 of the FINAL review still stand (R05 verse split 5.40 s; 3.5-4.4 s
verse band list; master bitrate is archival-only, now superseded by the 31.1
Mbps delivery copy).

## Disposition

**Delivery copy accepted for publish-prep.** Publish (M5) remains blocked on the
unchanged externals: platform accounts (CEO physical item) and per-platform
description/declaration copy. Machine-readable pack:
`qa/mv0001-v511/DELIVERY-PACK-V511.json`.

Signed: BigStream OS loop R2411 (independent re-measure) / director seat (accept).