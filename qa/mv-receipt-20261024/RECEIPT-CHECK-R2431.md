# MV V5 re-run receipt check — R2431 (2026-10-24 06:2x)

Decision: D-20261024-06 (回执判据收紧·三件齐才计 receipt, 缺一即判未回执).
Window: dispatcher row 2026-10-23 23:25 + 24h = 2026-10-24 23:25. Not due yet.

## Verdict: ABSENT (0/3 pieces)

| Piece | Requirement | Machine reading |
|---|---|---|
| (a) 17 shots | `bmc/i2v/v5redo/` holds all 17 re-rendered shot ids | no shot folder at `outbound/bmc/i2v/v5redo` |
| (b) edit grammar | hard-cut 54 / dissolve 7 / defocus 2 / deep-slow 3 | no v7 edit-grammar reading on disk |
| (c) director gate | `DIRECTOR-REVIEW-V5-PASS` (or explicit failure list + re-shoot order) | no such file |

Command (canonical, one row appended to `data/pipeline/mv-receipt-check.jsonl`):

    python src/os/mv_receipt_check.py

Exit 2 = receipt absent, window still open. A rendered `full_mv_v7xx.mp4` is
never accepted as a receipt (D-20261024-06 ②, and the five `.repair.json`
twins show a repair loop still writing).

Numbering note: D-20261024-06 says "17 镜", while the edit-grammar table in
the same row totals 54+7+2+3 = 66 cuts over those shots — a shot may contain
several cuts. Criterion (a) therefore counts shot ids (>= 17), not cut count.

## Next check

Re-run at/after 2026-10-24 23:25. Still ABSENT then = 夜轮 03:07 names one row
(not E1). RECEIVED requires all three statuses `present` in the same run.