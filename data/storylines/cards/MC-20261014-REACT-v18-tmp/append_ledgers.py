# -*- coding: utf-8 -*-
"""R2254 ledger appends: cards README + renders README + finished.md F-186."""
import io, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

cards_row = "- 2026-10-14: MC-20261014-REACT-v18 F-186 登记（R2254 起链+登记同轮全链·REACT 形态第十八件·成品库第186件·L-卡 第一百三十四件·《城市速报 018·PS5 底层漏洞之问》）——素材源=知乎热榜 2026-10-14 第 5 条全题 verbatim 跨两行（116 万热度元数据脱敏·#4=v17 已消费·同窗零重复执法）+BigLife 台词池 typhoon 桶三轴位 verbatim（秩序[17]/求新[12]/侠气[17]·**typhoon 桶=REACT 卡面首用**〔v1-v17 十一桶后第十二桶·bucket 轮换律〕·三行与 v1-v17 全卡面零冲突机核）+收束行 C-00012 晨操领队沈佩兰信条 verbatim「队形不能乱，人心更不能散。」（非荣誉席·带队十九年散伙重组亲历者=「生态阵型」原生权威岗·主机生态冲击之问×队形/人心双受力面题眼级直配·收束位轮换律=v1-v17 全未用）——M0 6/8 A 档（热点择优留痕第十八证·未选理由 19 条全量注记·PS5=GAME 城邻面承接 v17 留痕位）·M1 六断言（m1-assert-r2254.txt）·M2 em 32 档执法（驱动行 26.00em>25.56 排除 36 档·余量 +2.75em）+验图五检 5/5（多模态转写逐字全中零截断零重叠）·M3 四禁零中·M4 四检过——M4.5 七席=4×9+3 N/A 维度复用=PASS 放行候选（评审单 docs/reviews/review-20261014-mcreact-v18.md·desk-audit）·E4 参考仪 **CPU 车道已起飞在飞**（fire_consume --cpu-lane rc0 PID 33936·21:12:11·探针 8.89 tok/s ETA 775s·追加回填制 R176→R177 先例·双态制非拦截席）——成品入库不入发布队列（发布锁=M5 账号物理件+M4 全绿+AIGC 显著标识·未上线=未测量）\n"

renders_row = "| mc-20261014-react-v18-card.mp4 | **测试件·非成品（L-卡 REACT 形态第十八件《城市速报 018·PS5 底层漏洞之问》·R2254 渲染腿产物·M1 六断言+em-check-r2254.txt 全绿在案·M4.5 七席 4×9+3N/A PASS〔E4 参考仪 CPU 车道在飞·非拦截席·双态制〕·F-186 已登记）** | **spec probe 实测**：1080×1080·30fps·**3.40s ffprobe 实测**（2.6s 卡+0.8s tail 与 cards.json 逐项吻合·cover frame t=0.150s·115KB）·纯视频零音轨=静态帧路（C-27 --poster）·帧验=M2 验图五检全绿在案（多模态转写逐字对照全中零截断零乱码·AIGC 角标清晰）·PNG 正身=data/storylines/cards/MC-20261014-REACT-v18/MC-20261014-REACT-v18.png·评审单=review-20261014-mcreact-v18.md·发布锁=M5 账号物理件未开·未上线=未测量 |\n"

fin_block = """
**F-186 登记（R2254）**：**L-卡 REACT 城市速报系列第十八件=成品库第一百八十六件·L-卡 第一百三十四件**——MC-20261014-REACT-v18《城市速报 018·PS5 底层漏洞之问》静态热点反应卡（#59 按日热点随轮领第十七续件·R2254 起链+登记同轮·bigstream-lcard-pipeline 技能产线第三十用）——素材源=知乎热榜 2026-10-14 第 5 条全题 verbatim 跨两行（116 万热度元数据脱敏·#4=v17 已消费零重复）+BigLife 台词池 typhoon 桶三轴位 verbatim（秩序「别看外面风平浪静，加固招牌不能马虎」/求新「天气预报说台风凶猛，咱们得给招牌加个保险」/侠气「船长们都加固了锚，咱们也得紧绷着」·**typhoon 桶 REACT 首用=bucket 轮换律**·风暴三面镜像链=漏洞面/预警面/生态面一一对应）+收束行 C-00012 晨操领队信条 verbatim「队形不能乱，人心更不能散。」（非荣誉席·生态冲击双受力面题眼级直配·收束位轮换律）——M0 6/8 A 档（热点择优留痕第十八证）·M1 六断言（m1-assert-r2254.txt）·M2 em 32 档执法+验图五检 5/5（em-check-r2254.txt·多模态转写逐字全中）·M3 四禁零中·M4 四检过——M4.5 七席=4×9+3 N/A 维度复用=PASS 放行候选（评审单 review-20261014-mcreact-v18.md·desk-audit）·E4 参考仪 CPU 车道在飞（PID 33936·追加回填制·双态制非拦截席）；F 号连续性=R2239 收官批 F-181..185 后首件·零顺延积压；发布锁=M5 账号物理件未开+未上线=未测量。
"""

p = os.path.join(ROOT, 'data', 'storylines', 'cards', 'README.md')
t = io.open(p, encoding='utf-8').read()
assert 'REACT-v18' not in t, 'v18 row already present'
io.open(p, 'a', encoding='utf-8').write(cards_row)

p = os.path.join(ROOT, 'output', 'renders', 'README.md')
t = io.open(p, encoding='utf-8').read()
assert 'react-v18-card' not in t, 'renders row already present'
io.open(p, 'a', encoding='utf-8').write(renders_row)

p = os.path.join(ROOT, 'output', 'finished.md')
t = io.open(p, encoding='utf-8').read()
assert 'F-186' not in t, 'F-186 already present'
io.open(p, 'a', encoding='utf-8').write(fin_block)

print('LEDGERS OK')
