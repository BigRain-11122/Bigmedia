# edge-tts 情感参数实验（C3·人味链 v2 输入）edge-tts-emotion-dial v1.0

> 自进清单 C3 顶项（CEO 常态令 O-20260924-2118「学习各种技能」·技能学习池·产线全 supply-gated 轮领取）。
> 纪律：`docs/research-protocol.md` v2.0（指针声明 v2.0：调研「行程标准+结论应用律」正典=`cph4/research-protocol.md` v1.0·T2 否决窗至 2026-10-01）。源分级：**A 级=本机工具一手实测**（edge-tts 云端免费接口〔产线默认〕+ffmpeg 9.0.1.26〔本机在役〕·测量件=`.c3-tmp/c3_matrix.py`+`corpus.txt`+`c3-results.txt` 盘上可复跑）。
> 语料=机器叙述者语域两句（S1 短句/S2 含逗号长句·`corpus.txt`）·voice=zh-CN-YunyangNeural（产线默认）·对照制=同文本变单轴。

## §1 实验设计（五轴一引用）

| 轴 | 方法 | 度量 |
|---|---|---|
| A0 PROFILES 落地性 | hook(-8%/-3Hz)/punch(+6%/+3Hz)/body(0/0) 同文本三合成 | 时长（率代理）+频谱质心（音高代理） |
| A1 率轴 | rate -14%/0/+8% | 时长 |
| A2 音高轴 | pitch -12/0/+12Hz | 质心+时长（时间线安全判据） |
| A3 音量轴 | volume -50%/0/+50% | volumedetect mean/max（**产线零使用轴**） |
| A4 light 链存活 | A2 两极件过 CYBER_CHAINS["light"]（emotive_tts.py 同参） | 质心 pre→post（「light 保留抑扬顿挫」宣称实测） |
| A5 拍内阶梯音高 | S2 逗号拆两半（头 0Hz/尾 -8Hz）合成+concat | 两半时长代数+整体 RMS |
| SSML 面 | 不重跑——R10 已定谳（`research/local-stack-research-v1.md` §1.1：edge-tts SSML 收紧仅剩单 voice+单 prosody·express-as 情感样式不可用） | 引案（反重复律） |

质心法=ffmpeg `aspectralstats=measure=centroid` 逐帧均值（**≥50Hz 有声帧滤静音**·静音帧质心≈1Hz）；质心≠基频（F0）=**音高方向的代理量非绝对音高**——单调性与相对差有效，绝对值不作断言。

## §2 读数表（16 行·`.c3-tmp/c3-results.txt` verbatim）

```
A0 profile=hook | dur=3.384s centroid=2837.4
A0 profile=punch | dur=2.928s centroid=2957.4
A0 profile=body | dur=3.120s centroid=2895.4
A1 rate_m14 | dur=3.600s
A1 rate_0 | dur=3.120s
A1 rate_p8 | dur=2.880s
A2 pitch_m12 | dur=3.120s centroid=2708.7
A2 pitch_0 | dur=3.120s centroid=2907.8
A2 pitch_p12 | dur=3.120s centroid=3045.3
A3 vol_m50 | mean=-34.7dB max=-13.1dB dur=3.120s
A3 vol_0 | mean=-28.7dB max=-7.1dB dur=3.120s
A3 vol_p50 | mean=-25.2dB max=-5.0dB dur=3.120s
A4 light pitch_m12 | centroid 2708.7 -> 2212.9 (delta=-495.8 Hz)
A4 light pitch_p12 | centroid 3045.3 -> 2353.0 (delta=-692.3 Hz)
A5 stepped halves | durA=2.952s durB=2.136s concat=5.088s (sum=5.088 padding=0.000s) centroidA=2810.9 centroidB=2948.1
A5 stepped whole | mean=-26.6dB max=-3.3dB
```

## §3 定谳（逐轴）

1. **A0=PROFILES 表实测落地**：同文本下 hook 3.384s/2837.4（慢且低）vs punch 2.928s/2957.4（快且高）vs body 3.120s/2895.4（中位）——产线拍型双轴（率+音高）设计意图在合成输出中真实成立〔A 级实测·O-1918 立制面首件量化核验〕。
2. **A1=率轴单调可靠**：-14%→3.600s / 0→3.120s / +8%→2.880s（同文本 span 25%）——率档与时长严格单调，时间线预算换算可依赖。
3. **A2=音高轴单调落地+时长零漂移**：质心 2708.7→2907.8→3045.3 随 ±12Hz 设置单调（设置位差 336.6Hz）；三态时长逐毫秒同（3.120s）——**音高调节不伤 SRT/卡片时间线**（机核判据：漂移 0.000s）。
4. **A3=音量轴=产线零使用的可用新轴**：edge-tts 接受 `--volume` 且单调（-50% 档 mean -34.7dB/0 档 -28.7dB/+50% 档 -25.2dB·时长零漂移）——现行 emotive_tts.py 无 volume 档位=**人味链 v2 候选新轴**（强调拍抬升/收束拍压低的动态对比面）。
5. **A4=light 链旋律存活率 42%**：±12Hz 两极件过 light 赛博链后质心 2212.9/2353.0——跨度 336.6Hz→140.1Hz=**旋律未清零但压缩至 ~42%**。「light=保留抑扬顿挫加机器质感」（emotive_tts.py 设计宣称/O-2136 CEO 定档）实测=**部分成立**：拍型对比可感知但被纹理链压低过半。v2 候选：PROFILES 音高档位加宽补偿（如 ±3Hz→±5Hz）或接受现状——待人耳 A/B 裁。
6. **A5=拍内阶梯音高机械可行**：两半 concat 时长代数精确（2.952+2.136=5.088s·padding 0.000s）+整体 max -3.3dB 无削顶——**长拍拆分阶梯 pitch 技术路成立**（句内音高曲线=edge-tts 单 prosody 限制下的曲线近似法）；感知面（接缝可闻度/自然度）**待人耳**。两半质心 2810.9 vs 2948.1 不可作音高效验读数（跨半文本异质——同文本效验已由 A2 承担）。

## §4 诚实边界（待核验面）

- 质心=频谱能量重心（F0 方向代理）非基频测量——单调性结论有效，绝对音高值零断言。
- 语料=两句短样本·单 voice（Yunyang）——档位读数不外推其他 voice（v8 评测在案的 full 档伤词面即跨档差异例证）。
- A4 存活率=单链单音高对（±12Hz×light）——mid/full 链与产线真实 ±3Hz 档位的压缩率未测（设计值更窄·存活绝对量更小·方向性推论=观察级）。
- A5 接缝感知质量与阶梯自然度=**人耳位待验**（#8 CEO 听感先例同口径）；max_volume 两跑 -3.5→-3.3dB 微差=轮间变动面（未做逐字节核验·零断言·R18 确定性结论或有时点漂移）。
- 全部读数=2026-09-26 时点服务行为（edge-tts 免费端点无 SLA·R18 403 风控史在案）。

## §5 对位应用（消费方指认）

1. **C-21 人味链 v2 备件位三候选**（消费方=`docs/human-feel-spec.md` 升级面）：①volume 强调轴（punch/wink +15~25% vs beat/close -10~15% 动态对比）②PROFILES 音高档加宽（对冲 light 链 42% 旋律压缩）③长拍句内阶梯 pitch（turn/close 下坠尾=「陈述判定式」语气的声学落地）。**启用前置=同稿 A/B 干净样片呈 CEO 听感（#8 先例）+ai_feel 门+E8 席——本件只立备件不立法**（无实证不立法律·零 A/B 零人耳零升档）。
2. **emotive_tts.py 工程注记**：A2/A3 双轴「时长零漂移」实测=volume/pitch 档可入 PROFILES 表而不破 SRT/卡片时间线（机核前置已过）；A5 拆分法若采=beat 内 cue 仍单条（卡片切点在拍边界·句内拆分不进 cards 时间线=时间线面零成本）。
3. **SSML 面**：维持 R10 定谳（单 voice 单 prosody）——本件 A5 拆分法=该限制下的工程绕行位·非 SSML 解锁。
4. **量化基线入档**：本件读数=v2 改造前后对照的「前基线」（后续任何 PROFILES 改档复跑本矩阵即可得对照 delta）。

## 变更记录

- 2026-09-26 v1.0：R317 首版（自进清单 C3·产线全 supply-gated 轮）——五轴 16 读数+SSML 引案+light 链旋律存活率 42% 定谳+人味链 v2 备件三候选立位（待人耳 A/B 不立法）。
