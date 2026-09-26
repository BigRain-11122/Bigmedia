---
name: bigstream-lcard-pipeline
description: BigStream 硅基城市 L-卡（静态图文卡）四形态全链量产工艺：城市语录 QUOTE / 城市盘点 DIGEST / 城市图鉴 CENSUS / 城市速报 REACT。Use when producing, auditing, or resuming any BigStream 静态图文卡 based on BigLife 户籍卡手写锚 / CODEX 六轴信条例 / 编年史台账 / 当日热榜 — covers supply-gate anchor check, M0 hit-chain 四维分, M1 verbatim 纪实抽取律, M2 --poster 渲染 + em 预算前置适配 + 验图五检, M3 标题四禁, M4 四检, M4.5 七席评审 + E4 参考仪回填, F 成品登记.
---

# BigStream L-卡全链工艺（QUOTE / DIGEST / CENSUS / REACT）

四形态同一渲染引擎（`src/render/render_card_video.py --poster`），差别只在 M1 素材抽取律。
判据单一真相（本件不复制细节，只导航）：`docs/hit-chain-mechanism.md`（M0 四维分/M6）、`docs/city-storylines-charter.md` §5（门禁/三重标注）、`docs/dept-review-mechanism.md` §6（评审席位）、`CONSTITUTION.md`（红线）。

## 0. 供给门锚核（先于一切）

- **CENSUS（图鉴）**：按卡号序领件；**只查 `life/BigLife/census/anchors/C-XXXXX.md`**（正典位）——`census/registry/` 生成卡 ≠ 手写锚（R316 误判撤领教训）。锚不在位 = supply-gated：退领零产出、如实留痕、不等待不催办。
- **QUOTE（语录）**：BigLife CODEX §八 六轴信条例按表格序领；**轴级署名，禁虚构居民名**；引文逐字 verbatim。
- **DIGEST（盘点）**：编年史 A 级史源 + 逐条数字溯源（一料多吃，零改写零编造）。
- **REACT（速报）**：当日日报热榜择优；**映射对位优先于纯热度** + 政治敏感面回避律 + 轴位映射律/热点转述律（R309 双律）；热度元数据脱敏不入卡面。

## 1. M0 选题四维分（≥6=A 档才进 M1）

钩子强度 / 情绪势能 / 时效窗 / 平台适配度，各 0-2 分；判据正典=`docs/hit-chain-mechanism.md` §2。
四维分与总分写入 `cards.json` 的 `meta.hit_chain_m0`（数据件自证）。未过 A 档=不产。

## 2. M1 verbatim 纪实抽取（红线位）

- CENSUS = **纪实字段汇编律**（R291 首定）：六行逐条溯手写锚 verbatim——卡题行+编号 / 物种行 / 性别·年龄行（verbatim 合并）/ 城区·职业行（两级选材）/ 信条 / 性格三关键词 / 钩子首句。**字段内括号注与破折号阐释尾 = 选材排除，不进卡面**。零改写、零新增人格、逐行可机核。
- **人设权红线**：只引已登记字段；荣誉席三卡只引不增；非荣誉席核验后才用。
- **脱敏律**：年轮 / 思想 / 语言 / 服装 / 经历 / 行为 / 关系字段 = 选材排除，不进卡面（含令牌号/财务/隐私面）。
- QUOTE/DIGEST/REACT 同律：引文逐字、数字逐条溯源、转述不加工、来源行闭合。

## 3. M2 渲染 + em 预算 + 验图

- 出图：`python src/render/render_card_video.py --cards <cards.json> --poster <out.png>`（1080×1080；副产 mp4 gitignored 入 tmp）。
- **em 预算前置适配律**（出图前先算行宽再选档，判例库见 [references/em-budget-ladder.md](references/em-budget-ladder.md)）：全角 1.0em、ASCII≈0.55em；h2_size 梯档 28-50 选最大可行档；**零余量档排除**；折行孤尾（orphan-tail <2 字）禁；renderer `_em_cost` 机核断言留档（`em-check-rNNN.txt` 惯例）。
- **验图五检**（转写先行防偏=先多模态转写卡面文字，再逐字对照，禁凭眼直判）：
  1. 逐字对照全中；2. 零重叠零越界零截断；3. 全行单行零折行；4. 来源行闭合；5. AIGC 角标清晰 + 层级留白明确。
  任一不过=修参重渲复验（文本 verbatim 零动；盲改无效参数面=R293 教训）。

## 4. M3 标题四禁

不标题党（标题=内容即承诺）；不无来源；不虚构宣称；AIGC 依法标注位在图。系列编号连载识别（「城市语录/盘点/图鉴/速报 NNN」）。

## 5. M4 四检

红线五条 / 三重标注图内双落（AIGC 角标 + 底部来源行；REACT=热点现实转述×反应虚构两态声明）/ 来源双落（图内+台账）/ 编辑价值（体裁+选材+叙事包装）。

## 6. M4.5 七席 ≥9 木桶 + E4 参考仪

- 站审 M0-M6 判据行全链留痕 = `docs/reviews/review-<date>-<id>.md`（hit-chain §8 承接口径）；七席 ≥9 放行候选。
- E4 参考仪回填 = dept-review §6 双态制席位；wrapper = tmp 件 `e4_call.py` 复用改源（Start-Process 脱壳·1500s 窗·落地回填追加制·非拦截）。
- **假绿灯律**：评审单如实列已测面+未测面；未测维度的 PASS 是无依据宣称。

## 7. F 登记

`output/finished.md` 成品库块（F-XXX）+ `data/storylines/cards/README.md` 台账行 + 变更行。
**成品入库不入发布队列**（发布锁 = M5 账号物理件 + M4 全绿 + AIGC 显著标识；未上线=未测量）。
