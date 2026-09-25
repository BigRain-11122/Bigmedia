## BS-001 v15-douyin | ai_feel | rc=0
[PASS] gaps: 11 gaps, 0.220-0.558s (varied)
[PASS] pacing: cue duration CV 0.185
[PASS] prosody: 9 distinct profiles across 12 beats
[PASS] copy: sentence-length CV 0.204
SUMMARY: 0 FAIL 0 WARN -> pass

## BS-001 v15-douyin | edit_craft_l18 | rc=0
[PASS] beat-align: 11/11 boundaries on cue edges (+-0.25s)
[PASS] camera: all 12 segments move (flat/ken_in/ken_out/punch)
[PASS] visual-ratio: per-beat matched footage 0.83 (10/12 beats)
[PASS] flash: 6 hit flash(es) on-profile
[PASS] transition-share: 7 transitions / 4 cuts (share 0.64)
[PASS] transition-variety: 7 transitions, no back-to-back repeat
[PASS] timeline: durations satisfy the run algebra (fade chains + true-splice cuts, beats fixed)
SUMMARY: 0 FAIL 0 WARN -> pass

## BS-001 v15-douyin | platform_spec | rc=0
[PASS] aspect: 1080x1920 = 9:16
[PASS] duration: 57.39s within 15-60s window (2.6s headroom)
SUMMARY: 抖音 -> pass

## BS-001 v15-douyin | ffprobe: 1080,1920,1721 | 57.388000

## ramp algebra report
ramp_beats: [0, 2, 3, 4, 5, 7]
seg 0 dur 5.300s span_frames+1=160 blocks=4 sum_out=160 speeds=1.0000,1.1429,1.6000,2.6667
seg 2 dur 3.387s span_frames+1=103 blocks=4 sum_out=103 speeds=1.0000,1.1429,1.6000,2.6667
seg 3 dur 5.300s span_frames+1=160 blocks=4 sum_out=160 speeds=1.0000,1.1429,1.6000,2.6667
seg 4 dur 6.820s span_frames+1=206 blocks=4 sum_out=206 speeds=1.0000,1.1429,1.6000,2.6667
seg 5 dur 5.067s span_frames+1=153 blocks=4 sum_out=153 speeds=1.0000,1.1429,1.6000,2.6667
seg 7 dur 4.587s span_frames+1=139 blocks=4 sum_out=139 speeds=1.0000,1.1429,1.6000,2.6667

## ramp continuity probe: 54 frames -> .bs001-dy-tmp\probe-r316\tile-r316.png
