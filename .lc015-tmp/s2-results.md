[ffprobe] width=1080 | height=1920 | duration=57.615000 |

=== gate1_ai_feel exit=0 ===
[PASS] gaps: 11 gaps, 0.220-0.558s (varied)
[PASS] pacing: cue duration CV 0.255
[PASS] prosody: 9 distinct profiles across 12 beats
[PASS] copy: sentence-length CV 0.287
SUMMARY: 0 FAIL 0 WARN -> pass

=== gate2_platform_spec exit=0 ===
[PASS] aspect: 1080x1920 = 9:16
[PASS] duration: 57.62s within 30-60s window (2.4s headroom)
SUMMARY: 微信视频号 -> pass

=== gate3_edit_craft_1p8 exit=0 ===
[PASS] beat-align: 11/11 boundaries on cue edges (+-0.25s)
[PASS] camera: all 12 segments move (ken_in/ken_out/punch)
[PASS] visual-ratio: per-beat matched footage 1.00 (12/12 beats)
[PASS] transition-share: 11 transitions / 0 cuts (share 1.00)
[PASS] transition-variety: 11 transitions, no back-to-back repeat
[PASS] timeline: durations satisfy the run algebra (fade chains + true-splice cuts, beats fixed)
SUMMARY: 0 FAIL 0 WARN -> pass

