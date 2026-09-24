## bs-005-v1 | ai_feel | rc=0
[PASS] gaps: 11 gaps, 0.220-0.558s (varied)
[PASS] pacing: cue duration CV 0.219
[PASS] prosody: 9 distinct profiles across 12 beats
[PASS] copy: sentence-length CV 0.231
SUMMARY: 0 FAIL 0 WARN -> pass

## bs-005-v1 | edit_craft_l18 | rc=1
[PASS] beat-align: 11/11 boundaries on cue edges (+-0.25s)
[PASS] camera: all 12 segments move (flat/ken_in/ken_out)
[FAIL] visual-ratio: matched-beat ratio 0.17 < 0.80: too many cards-only beats
[PASS] transition-share: 11 transitions / 0 cuts (share 1.00)
[PASS] transition-variety: 11 transitions, no back-to-back repeat
[PASS] timeline: durations satisfy the run algebra (fade chains + true-splice cuts, beats fixed)
SUMMARY: 1 FAIL 0 WARN -> exit 1

## bs-005-v1 | platform_spec | rc=0
[PASS] aspect: 1080x1920 = 9:16
[PASS] duration: 58.41s within 30-60s window (1.6s headroom)
SUMMARY: ΢����Ƶ�� -> pass

