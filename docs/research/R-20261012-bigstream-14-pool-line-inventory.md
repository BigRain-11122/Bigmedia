# R-20261012-bigstream-14 台词池 REACT 直配行消费盘点读数 v1.0

> 溯源：tech#117（R2009 补货·缺口锚=R1030/R1160 两窗判负实锚「直配行消耗殆尽结构性信号」在案+REACT 15 件消费后读数缺口=桶行消费无盘点面）·消费侧=BigLife 台词池 `life/BigLife/cognition/pools.json`（跨仓只读·R1031 台词池扩容承接面）·盘点窗=2026-10-12 00:5x R2010。
> 判据（tech#117 预注册）：盘点件落位+预警三态注+BigLife 池扩容触发判据预注册。

## 一、池结构实测（1296+144=1440 行）

- **六轴**（烟火/秩序/求新/怀旧/侠气/逍遥）× **12 桶**（morning/dusk/night/weekend/rain/typhoon/heatwave/coldsnap/market_open/market_close/ceo_order/festival）= **72 桶位**，每桶位 **18 行**（实测全矩阵 18/18 均一·零空位）= **1296 轴行**。
- **sprite 池**（像素灵拟声族·`sprite` 键）12 桶 × 12 行 = **144 行**。
- **池总行数=1440**——tech#117 种子「行数 >1440」触发线=池总行数实测精确值（种子 72×20 估算勘正：实为 72×18+144=1440·触发线数值不受影响）。
- 全 1440 行归一化（去空白/标点）后唯一——零重复行。

## 二、15 卡消费读数（REACT v1~v15·发布面 verbatim 对账）

扫描法=cards.json+subs.srt 全字符串归一化逐行包含匹配（发布面正身）·m1-assert 面交叉核（v13/v14/v15 三件零差·双扫描读数一致）；脚本证据=.c3-tmp/r2010_consume_scan2.txt（+r2010_pool_matrix.txt 结构面）。

**总读数：51/1440 行已消费（45 轴+6 sprite）=3.5%**·逐卡计数：v1~v5/v7~v9/v11~v13/v15=3 行/卡·v6/v14=4 行/卡·v10=7 行/卡（多桶卡·dusk/heatwave/morning×3/ceo_order）·**零跨卡行复用**（51 行全部单次使用）。

| 桶 | 轴消费/108 | 剩余% | sprite/12 | 消费卡 |
|---|---|---|---|---|
| market_open | 8 | 92.6% | 1 | v2/v13/v15 |
| night | 7 | 93.5% | 0 | v7/v14 |
| morning | 6 | 94.4% | 1 | v6/v10 |
| weekend | 4 | 96.3% | 2 | v4/v5 |
| heatwave | 4 | 96.3% | 0 | v9/v10 |
| ceo_order | 4 | 96.3% | 0 | v10/v12 |
| coldsnap | 3 | 97.2% | 0 | v11 |
| festival | 3 | 97.2% | 0 | v8 |
| dusk | 2 | 98.1% | 0 | v10 |
| rain | 2 | 98.1% | 1 | v1 |
| market_close | 2 | 98.1% | 1 | v3 |
| typhoon | 0 | 100% | 0 | （零用） |

- 桶位级最高消费=2/18（七桶位：烟火×market_open/秩序×night/秩序×weekend/求新×market_open/侠气×morning/侠气×market_open/侠气×ceo_order·剩余 89%）。
- typhoon 桶零消费维持（explore#13 候选位在册：下一个台风日热点窗直配位照旧）；dusk 桶 v10 首用勘正 explore#13「dusk 零用」注（该注=v3 时点读数·已被 v10 消费 superseded）。

## 三、预警三态注（<20% 剩余=RED·<40%=AMBER·其余 GREEN）

**全 12 桶 GREEN（RED=0·AMBER=0）**——桶级最低剩余 92.6%（market_open）·桶位级最低剩余 89%（七桶位 2/18）·sprite 级最低剩余 83.3%（weekend 2/12）。按现节奏（≈3.4 行/卡·单桶重度 ≈8 行/15 卡）外推：market_open 首达 AMBER 需再消费 ~53 行 ≈ 100+ 卡——**字面耗尽在现产线节律下不可达**。

## 四、R1030/R1160「直配行消耗殆尽结构性信号」勘正定谳

两窗判负的「supply-exhaustion structural signal」实锚=**M0 全池探针对当日热榜逐条不匹配**（热点-池行适配面枯竭·R1030 20/20 law-excluded/R1160 二连窗）非字面行库耗尽——本盘点实测 15 卡仅耗 3.5% 且零复用证明行库存量充裕；**瓶颈=热点↔桶行匹配面（编辑选材带宽）非库存深度**。池扩容（BigLife 域）若发生应扩**热点适配带宽**（新桶型/新轴位）而非加深现有桶位——本定谳供 BigLife 侧扩容设计参考（跨仓只读呈报位）。

## 五、BigLife 池扩容触发判据（预注册·R1848 判据族复用）

- **触发①**：pools.json 总行数 >1440（=BigLife 加行·任何桶位加深或新桶型）；
- **触发②**：工作树 vs HEAD 行集差非空（行集=归一化行全集合；改动无行数变化时此臂兜底·R1848 行集差判据族复用）；
- 任一触发=REACT 直配行续供窗重开评估（读数件复读+桶适配面重评）；零触发=库存面维持现判（GREEN·无需扩容）。

## 六、复读点位（预注册）

- **点位①**：REACT-v20 收官轮并读（本盘点+5 卡后复算三态·tech#118 到点执行位）；
- **点位②**：任一桶触 AMBER（<40% 剩余）即提前复读（点位①不必等）；
- 复读法=.c3-tmp/r2010_consume_scan2.py 重跑（证据件 committed·零新工具=反膨胀律·效率平衡校准：现节律下 AMBER 不可达·禁为不可达场景预建常设 CLI）。

## 七、验证声明

本件全部数字=脚本实测（非估算）·双扫描（含/不含 m1-assert 面）读数一致 51/51·扫描脚本与证据件=.c3-tmp/r2010_pool_inspect.py/r2010_pool_matrix.py/r2010_consume_scan.py/r2010_consume_scan2.py/r2010_v14_diff.py/r2010_v13v15_diff.py+对应 .txt 证据件（随轮收账入 git）。池=BigLife 仓跨仓只读零写接触。
