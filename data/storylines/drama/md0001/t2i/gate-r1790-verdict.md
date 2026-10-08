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
