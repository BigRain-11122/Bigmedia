# MD-0001 T2I 一致门 R1790 判定书（gate verdict·判据窗内迭代记录）

**判据**：同角色镜一致抽验 ≥8（#108 charter；角色镜 9 面=lamp 2/3/4/12·tower 6/7·cat 9/10/11）vs census 参照卡 v19/v18/v20 多模态并排逐特征核对。

**正式读数**：R1789 12/12 出图后首轮正式核对 = **4/9 PASS → FAIL**
- lamp：shot02 PASS · shot03 FAIL（补丁未主体化+写实漂移） · shot04 PASS · shot12 PASS
- tower：shot06 FAIL（大檐帽+制服+打盹不明） · shot07 FAIL（帽+室外漂移+琥珀屏光缺失）
- cat：shot09 PASS（弱·尾天线不可证） · shot10 FAIL（耳缺口/舔爪/看镜头三项失） · shot11 FAIL（猫本体崩坏+七盘/吃食未达）

**迭代一**（reroll_r1790.py·prompt 修复+负锁强化·5 镜）：tower 2/2 修复过（去帽/工装/室内锚/打盹姿态/琥珀屏光全落）→ 累计 **6/9**。shot03/10/11 仍 FAIL。

**迭代二**（reroll2_r1790.py·主体化重写）：三镜仍 FAIL（shot03 补丁仍非主体·shot10 耳缺口+舔爪缺失·shot11 猫完全缺席+丢像素感）。

**迭代三 best-of-N**（reroll3_r1790.py·每镜 3 seed=9 候选）：shot03 三候选全无补丁（NONE·两候选漂移成抽象/城市）·shot10 最优 B=2/4（无缺口无舔爪无像素感）·shot11 最优 D=2/4（白灰猫+多盘√·非吃食无天线）。最优候选 D 已换入 frames/shot11.png（优于迭代二的零猫帧）。

**定谳**：17 张生成证据（12 首批+5 迭代一+3 迭代二+9 候选去重）收敛于同一结论=**SDXL base 1.0 草稿档在细粒度特征面（歪斜补丁主体化/左耳缺口/舔爪吃食交互动作/像素方感）的天花板**，prompt-only 迭代边际收益归零。gate 终读数 **6/9 = FAIL（判据 ≥8）**，如实入账不宣称通过。

**frames/ 现态**：12 帧全在位=装配链可用的最优草稿档（tower 2 帧已达正典锚·shot11=最优候选 D）。v1 原帧存 frames-v1/（FAIL 证据保全）。

**下轮升档路径**（O-2126 科学决策授权·判据窗 72h 至 ~10-11 带内）：
1. **Qwen-Image-2.0 GGUF A/B**（PACK 升档位既定·#109 模型位并行）——中文指令遵循+细节控制强项直面三个残余镜；
2. 备选=ComfyUI img2img/inpaint 路线（shot03 现灯头帧局部补丁植入·shot10 耳缺口局部修）；
3. 装配腿不阻塞可并行启动（12 帧草稿档+13 段音轨已齐·KB 动效参数在 PACK）——但 **M4 前须 gate 复核 ≥8/9** 方可呈 CEO。

**证据件**：gate-r1790-{lamp,tower,cat}.png（首轮）·gate-r1790-reroll-*.png（迭代一/二）·gate-r1790-pick-*.png（择优）·reroll{,2,3}-r1790.log+status.json·reroll3-candidates/ 9 候选。

---

## R1793 复核（Qwen-Image-2.1 全量重 roll frames-r1792/ 正式 gate）

**首轮读数**：lamp 3/4（shot02/03/04 PASS·shot12 远景灯成光点锚不可辨 FAIL）/ tower 1/2（shot06 PASS·shot07 判 FAIL）/ cat 2/3（shot10/11 PASS·shot09 天线错位头顶+缺口不可见+毛色漂移 FAIL）= **6/9**。

**勘误（如实入账）**：shot07 的 FAIL 系 gate 指令错置预期——PACK 正典 shot07=resolute side profile+琥珀屏光（非打盹镜；打盹镜=shot06「curled up asleep」且已 PASS），多模态确认 shot07 ①②③④⑥全命中=tower 实为 **2/2**。修正后真实读数 **7/9**，真残余=shot09+shot12 两镜。

**迭代（reroll_r1793.py·定向 best-of-N 3 seed×2 镜·负锁加 antenna on head）**：
- shot09：s19019/s19120 天线仍长头顶淘汰；**s19221=4/5 BEST**（尾尖金属天线正位唯一候选+纸条+灰白像素感+占比大；左耳 V 缺口侧跑角度被耳型遮挡不醒目=弱过注记·R1790「PASS 弱·不可证」同口径）→ 换入 frames-r1792/shot09.png。
- shot12：**s13013=6/6 全中**（歪斜灯罩+暖光勾出补丁+同款悬臂灯+塔剪影+柱脚蜷猫+近黑收尾）→ 换入 frames-r1792/shot12.png；s13114=5/6 备选（塔剪影过暗）；s13215 灯型漂移弃用。

**终读数：lamp 4/4 + tower 2/2 + cat 3/3 = 9/9 ≥8 = GATE PASS**（shot09 弱过注记：耳缺口角度遮·装配腿可选补耳部特写/转身镜强化该锚）。

**证据件（R1793）**：gate-r1792-{lamp,tower,cat}.png（首轮三并排）·gate-r1792-reroll-{cat09,lamp12}.png（择优并排）·reroll_r1793.py+reroll-r1793.log+status.json+reroll-r1793/（6 候选+2 prev-fail 保全）。

**装配腿解锁**（判据窗 72h 至 ~10-11 带内）：12 帧正档=frames-r1792/（9 角色镜全过+shot01/05/08 非角色镜）；13 段音轨+KB 参数在 PACK → 装配→S2 三门+帧验三律→E8→M4→F 登记。

