# mv0001 V5.11 — FINAL QC station review (R2405, 2026-10-20)

Vehicle: orders 2026-10-20 00:32 row 636 (@bm-a BigStream-OSLoop,
lane=hq-central-night-gpu) — V5.11 detached 540P proxy re-render acceptance.

## What this round verified

The re-dispatch landed: `v56_v511_proxy` (23:06, 540P, PROXY-PASS by R2404 at
02:05) plus the production path `v56_v511_final` (02:24, all segments + G-blocks
rebuilt) and the 768P master `full_mv_v511.mp4` (02:27, 1338 MB, 5622 frames).

Machine checks re-run against the **768P master** (not the proxy):

- PTS: 5622 frames, 0 non-uniform steps -> PASS
- platform gate (B站): 16:9 / 234.25 s inside 180-900 s -> PASS
- audio: master true peak **+0.2 dBTP** fails the -1.0 gate ->
  delivery variant `full_mv_v511_n1.mp4` rebuilt (video stream copied, audio
  limiter -3.3 dB, 256k AAC) -> **-1.1 dBTP**, I = -14.1 LUFS -> PASS
- boards: XFS 14 cuts / 4 gap-1 splits / grade dual / 3-shot dense strips

## Boards

| file | content | read |
|---|---|---|
| `DENSE-3SHOT.jpg` | 3 shots x 12 consecutive frames | rows 1-2 clean progressive motion; row 3 crosses the designed 197.0 s cut |
| `XFS-CUT-BOARD.jpg` | 14 cut points +/-0.21 s (2 cols) | all coherent; row 12 = designed `fx_echo` overlay at 187.24 s |
| `SPLIT-DENSE-BOARD.jpg` | 4 gap-1 splits pre/cut/post | clean, unchanged from signed proxy review |
| `GRADE-DUAL-BOARD.jpg` | 3 amber + 3 cool samples | single warm envelope; cool zone not executed -> director note, no re-render |

Machine pack: `FINAL-QC-PACK.json`. Full verdict:
`cph4/fleet/mv0001-handover/outbound/krea2/30s-reel-v1/DIRECTOR-REVIEW-V511-FINAL-20261020.md`

## Open items carried to publish-prep

1. ~~AIGC badge overlay + VideoSeal invisible watermark (「大喵没鱼吃」) not applied.~~
   **RESOLVED 2026-10-20 R2410** — invisible VideoSeal watermark applied to the
   delivery variant: `full_mv_v511_wmvs.mp4` (917.6 MB, 31.1 Mbps, TP -1.1 dBFS,
   audio stream-copied, full-clip extract bit-accuracy 100 %). The visible AIGC
   badge was deliberately NOT burned in: CEO order 2026-10-17 removed the
   in-frame mark (`PUBLISH-CHECKLIST.md` §2), so Note 4 of the FINAL review is
   stale on that half. Evidence: `WATERMARK-R2410.md` + `WM-VIS-BOARD-VS.jpg`.
2. ~~Master bitrate 45.7 Mbps is spec-compliant but upload-heavy; delivery-size
   encode is a separate decision.~~ The watermarked delivery copy is 31.1 Mbps,
   so the upload-facing size question is closed for the publish copy; the
   archival master stays untouched as source of record.
3. R05_gold_threads verse split 5.40 s (beat-aligned, residual).

Tooling: `tools/v511_final_qc.py` (this repo) — PTS + four boards, read-only
against the media tree, boards land here.