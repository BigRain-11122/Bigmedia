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
2. ~~CosyVoice3 运行时装包→多角色配音首产~~（R1783-R1787 毕·短台词四路判负留痕+edge-tts 档位声直出收口）。
3. ~~T2I 腿→一致抽验~~（R1788-R1793 毕·SDXL 判负留痕→Qwen-2.1 升档→gate 9/9 PASS）。
4. ~~合成→S2 三门+帧验三律→E8→M4→F 登记~~（R1794 装配+三门毕·**R1795 E8 终审七席 ≥9→M4→F-168 登记=L-剧漫剧形态首件**·review-20261009-md0001-v1.md；E4 参考仪在飞·下轮回填）。
5. 迭代位（非阻断）：风格统一性（head 半写实漂移=Qwen-2.1 已知面）+27b 剧本 A/B+合集装配（M5 发布批位）。

## 合规

三重标注（AIGC 标识+档案改编声明+推演声明）片尾落位；人设权三角色非荣誉席；红线五条+真城真事律+脱敏律照守。
