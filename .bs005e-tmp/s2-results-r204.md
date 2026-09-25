# BS-005e v1 S2 三门读数（R204 循环独立执法·2026-09-25）

对象=bs-005e-v1-shipinhao-60s.mp4（R-E shipinhao·9:16 1080×1920·ffprobe 58.07s·12 段 11 柔转场 0 硬切·hits=[]）
拍稿=data/sources/bs005e/voiceover-v3.beats.txt（S1 v1 材料判 10/10 PASS 054444·v2/v3=机械窗预算裁·卡片行零动·语义零改）

## ① ai_feel_check.py --beats v3.beats --srt subs.srt
[PASS] gaps: 11 gaps, 0.220-0.558s (varied)
[PASS] pacing: cue duration CV 0.144
[PASS] prosody: 9 distinct profiles across 12 beats
[PASS] copy: sentence-length CV 0.180
SUMMARY: 0 FAIL 0 WARN -> pass

## ② edit_craft_check.py --plan bs-005e-v1-shipinhao-60s.mp4.plan.json --srt subs.srt --profile shipinhao
[PASS] beat-align: 11/11 boundaries on cue edges (+-0.25s)
[PASS] camera: all 12 segments move (flat/ken_in/ken_out)
[FAIL] visual-ratio: matched-beat ratio 0.17 < 0.80: too many cards-only beats
[PASS] transition-share: 11 transitions / 0 cuts (share 1.00)
[PASS] transition-variety: 11 transitions, no back-to-back repeat
[PASS] timeline: durations satisfy the run algebra (fade chains + true-splice cuts, beats fixed)
SUMMARY: 1 FAIL 0 WARN -> exit 1
（FAIL=README 素材预判声明预期态：b1/b2/b3/b6 引擎编辑器面板=开窗实录批待录；b5 总控+b7 像素小镇=cockpit 在位直接源同源多用=诚实对位上限 2/12=0.17；与 BS-005 原版同读数；门线 0.80 不动·利益回避）

## ③ platform_spec_check.py --video bs-005e-v1-shipinhao-60s.mp4 --platform 微信视频号
[PASS] aspect: 1080x1920 = 9:16
[PASS] duration: 58.07s within 30-60s window (1.9s headroom)
SUMMARY: 微信视频号 -> pass
（spec 门经 python exec 包装 \u 转义+__file__ 补定义=R173/R147 在案坑预防；SUMMARY 平台名控制台显示乱码=已知显示面非检查面）

## 空气预算链（TTS light·--cyber light --human 42·--template bs004 cards-v1-matched）
- v1 65.68s 超窗 → v2 机械裁 30 字符=59.05s（余量 0.95s 薄于 fleet 同族线 ≥1.2s）→ v3 再裁 4 字符=**58.05s 定稿（1.95s 余量·fleet 同族线内）**
- 裁口全卡锚承载面：b1「游戏」/b3「不做广告词」/b4「版权证书一沓」/b6「三端模块配齐」/b11「过程如实播报」/b5「一台」/b9「工程」——事实数字 8/0/1.10.3/12 与六标记位零动
- 音轨=.bs005e-tmp/audio.mp3 58.07s（含 room tone）+subs.srt 12 cues+cards.json 基线（v14 批口径模板）

## 处置
S2 visual-ratio FAIL-blocked 维持（声明预期态·门线不动）→ E8/M4/F-007 冻结待开窗实录批（与 BS-005 原版共享解锁面·素材采集线候选呈报=现状行不催办）；S1/空气预算/TTS/对位表/渲染腿全毕=素材窗一开即续链闭环。
