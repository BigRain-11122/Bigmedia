---
name: bigstream-s2-probes
description: BigStream S2 机检三门 + 验图采样面三律执法组合（层 1.8）。Use when verifying, 补账, or gating any BigStream rendered piece（成片 / 重渲件 / 在途批核验 / 渲染件收口 / 纯音频件）: run the three S2 machine gates — ai_feel_check（拍稿↔SRT）、platform_spec_check（画幅+时长窗）、edit_craft_check（层 1.8 六/七面·visual-ratio ≥0.80）— plus frame-sampling verification（拍头/段中尾/回环边界三律）, record PASS/FAIL honestly into station-reviews + renders ledgers, never silently patch in-flight batches.
---

# BigStream S2 三门 + 验图采样面

零 token 纯脚本执法面。判读正典（本件不复制细节）：`docs/production-chain.md`（S2 环节门）、`docs/footage-matching-spec.md` v1.1（采样面三律）、`docs/dept-review-mechanism.md`（席位）。
结果一律入账：`docs/reviews/station-reviews.md` + `output/renders/README.md`（或对应台账行）。

## 1. 三门命令（成片核验必跑齐）

```
python src/ai_feel_check.py --beats <拍稿.beats.txt> --srt <tmp>/subs.srt             # 门线: 0 FAIL 0 WARN（gaps/pacing CV/prosody 档/copy CV 读数入账）
python src/platform_spec_check.py --video <mp4> --platform <平台键>                    # 门线: 双 PASS（画幅+时长窗·headroom 余量入账）
python src/edit_craft_check.py --plan <mp4同名>.plan.json --srt <subs> --profile <平台>  # 层 1.8 门线: 六/七面 PASS·visual-ratio ≥0.80
```

- 纯音频件：spec = 时长 ffprobe 实测注记；层 1.8 = N/A（无剪辑面）。
- 同音轨重渲件读数应与前件逐项一致（同音轴确定性）；不一致=新账须查因。

## 2. 验图采样面三律（footage-matching-spec v1.1）

每素材拍按三采样面抽帧 + 多模态验图：

- **拍头帧**：每拍首帧语义对位（声画对位核——画面必须是当下文案的证据）。
- **段中尾帧**：每拍中点 + 尾帧（防段内录穿；R186 单时点探针假绿灯教训）。
- **回环边界帧**：`stream_loop` 源拍于 beat 相对 =（源长 − src_off）±0.1s 抽 pre/x/post 三帧（回环穿越区必采；R196 假绿灯第二案）。

手段纪律：全分辨率复核；tile 缩采样失读 = 读数手段问题非画面问题（R189 定谳）。
脱敏四查在帧：密钥 / 聊天 / 财务 / 隐私零在帧（含标题栏/任务管理器/编辑器层级条带录穿）。

## 3. FAIL 处置律

- FAIL 如实入账（station-reviews + renders 台账行），**不自行修改在途批**（认领制·待其闭环）。
- 门线不动（利益回避：在途件门线校准须升裁或决策件，禁自降门线凑过）。
- 结构性 FAIL（如素材源池缺口致 visual-ratio 诚实上限 < 门线）= 定谳 + 路线自决呈报（D-BS-08 先例）；禁硬贴错位素材凑数（数字错位避用律）。

## 4. 计量

三门 + 验图 = 纯脚本 + 会话内建工具，零 API token；`state.json` tokens:local 如实记账（本地模型调用另计）。
