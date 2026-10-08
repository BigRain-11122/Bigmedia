# MD-0001《台风梅花夜》· L-剧 漫剧 PoC 首件（#108）

> CEO 令 P-2026-10-08-02·D-BS-20261008-09 立项批执行件③。登记位：drama/ 路径（MV-0001 同目录族）。形态=漫剧（分镜剧本→T2I 多格→多角色 TTS→FFmpeg 动效合成）。判据窗 72h（立项 10-08）：同角色 10 镜一致抽验 ≥8 + M4 全绿 + 盲评过线。

## 选题

纪实改编「台风梅花夜」——编年史 A 级事件，同夜三视角：灯（C-00028 十四号路灯）/塔（C-00027 邓建国）/猫（C-00029 咪喱）。溯源对表=sources.md。

## 生产记录

- **R1782 2026-10-09（起链腿）**
  - 范围：剧本+分镜表一体化首产（模型腿）+ schema v0.1 + 溯源对表。
  - 模型：qwen3.5:9b-16k（#109 模型位·think=false·temperature 0.8）——本地推理零 API token（C-20260929-01 A 款本地先试）。
  - GPU 让路纪律：nvidia-smi 实测 7b keep-warm 5.1GB 驻留、AIHOT 14b-8k 未载（静磨态·08:00 compose 前 7h 零冲突窗）→ 9b 独跑合法。
  - 产物：prompt-script-v1.txt / gen-script-v1.py / script-raw-v1.txt / script-content-v1.json / script-validate-v1.txt / SCRIPT-v1.md。
  - 判据读数：见 script-validate-v1.txt（schema 无效率机检）+ SCRIPT-v1.md QC 节（verbatim 锚抽验）。

## 余链（后续轮领·拆细）

1. 模型 A/B 位：9b vs 27b-8k 剧本重档对打（27b 试跑=AIHOT 08:00 收官独占窗·R1777 锚）。
2. CosyVoice3 运行时装包（核心件已下 R1776/R1777·data/assets/model-pulls/）→ 多角色配音首产（主声线守 light 赛博定档）。
3. T2I 腿：分镜表交 bm-c ComfyUI（参照卡制锚三角色一致性）→ 同角色 10 镜一致抽验判据。
4. FFmpeg 动效合成（Ken Burns/转场/字幕/AIGC 烧录）→ S2 三门+帧验三律 → E8（盲评七席 ≥9+E4 参考仪）→ M4 → F 登记（drama/ 路径+三重标注）。

## 合规

三重标注（AIGC 标识+档案改编声明+推演声明）片尾落位；人设权三角色非荣誉席；红线五条+真城真事律+脱敏律照守。
