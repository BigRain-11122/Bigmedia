# -*- coding: utf-8 -*-
# R1686 ledger close: finished.md F-162 block + renders README row upgrade +
# release-schedule v3.10 + station-reviews row + bs014 README changelog + backlog #103 done
import io

def patch(path, pairs):
    t = io.open(path, encoding="utf-8").read()
    for old, new in pairs:
        assert t.count(old) == 1, "%s anchor not unique (%d): %r" % (path, t.count(old), old[:40])
        t = t.replace(old, new)
    io.open(path, "w", encoding="utf-8", newline="\n").write(t)

# ---------- 1) finished.md: append F-162 block at end ----------
f162 = (
"\n\n**F-162 登记（R1686 生产轮）**：**「板块十年」城市生长预演系列第三件·视频线新形态第三件（形态 C 图鉴语录卡×编年史混剪+城市年谱时间轴压条）=成品库第一百六十二件**——"
"BS-014《板块十年·这条街的口头禅》全链走门毕（backlog #103·lane 常备 ≥2 律备货位 1/2·R1684 起链→R1685 渲染→R1686 收官三轮链零断洞·**消费面双指名**="
"①本司视频线新形态〔真直切 A3 引擎在役·系列第三件〕②BigHouse P3 苏州吴中样板首件叙事规格候选〔R-20261001 §5 交付判据=BigHouse 侧引用 ≥1 处=全链走门留痕可达〕·"
"**前件章尾钩兑现位**=BS-013 cta「下集：这条街的口头禅」点名本件〔系列接力合法·钩兑现链第二证〕）——"
"①拍稿=Q8 题眼句「哪句口头禅，是从这条街传出去的？」+形态 C（语录库回放 b1→四句未消费信条 verbatim 逐拍 b2-b5〔v1 怀旧/v2 烟火/v3 秩序/v5 侠气·"
"四句全 fleet beats 反重复 grep 零命中=独占切面实证〕→时间轴压条 b6 turn 制式位→推演声明 b7 punch〔标签句 verbatim〕→传播面推演 b8"
"〔谁搬走谁顺路捎带新街坊接着教=census C-00022 对位〕→诚实交底 b9 proof→系列收束 b10 close〔Q8 答案落位=档案接着记+Q10 前置呼应+自指「还是我剪的」〕→"
"下集预告+评论区钩 cta b11〔《台风夜之后》点名+「报一句你街上的口头禅」=L14 互动钩新变体〕·§2.6 机器叙述者+系统日志体·黑话 12 词零命中·"
"一料多吃避让清单全执行〔v4/v6 口播零占用 lc010/lc003 已消费位·lc018 个人口头禅切面避让·lc006 共词族不同源双保〕）→"
"S1 v1.5 门 **10/10 一次过零违律**（R1684·判词档 20261008-014633-S1-script·**系列三连满分**〔BS-012/013/014 全 10/10〕）→"
"空气预算四道机械裁口 **v5=57.05s 定稿**（v1 74.84s→2.95s 余量·fleet 最宽位·卡片锚点列零动）→"
"②形态 C 视觉定谳（语录卡方图派生竖版评估=**弃用**〔卡面信条例文本带与成片 H1/H2 覆盖带同文双排=文本对撞非对位增益·在案源复用优先律〕+"
"**census-card-v13 图鉴拆条入混剪=形态 C 拆条面首证**〔C-00022 何雨欣新市民派=「新街坊接着教」对位判据·帧提取卡面核验实锚〕）→"
"对位表 cards-v1-matched 11/12=0.92（探针在案复用 R808/R188/R197）→R-E 渲染 bs-014-v1-shipinhao-60s.mp4（12 段 11 柔 0 硬切·9:16 1080×1920·57.05s·"
"**hits=[0] 单硬点克制档系列连三**·S5.5 角标 BigStream|BS-014 EP.14+§4.5 三开关·plan.series+s45_dials 入 plan.json）→"
"S2 三门全绿（ai_feel 0F0W〔gaps 11 处 0.220-0.558s varied·pacing CV 0.228·prosody 9 档·copy CV 0.235=bs012 copy-uniform 同位面本件净〕+"
"层 1.8 六面 PASS〔beat-align 11/11+camera 12 段全动+visual-ratio 0.92+share 1.00 无连排〕+spec 双 PASS 2.9s 余量）→"
"帧验三律全过（拍头 12/12+回环 b0 三帧净〔4.400s 穿越点 pre/x/post 全净·净源链继承〕+全分辨率零截断〔b8 拆条卡/b11 cta〕）→"
"③R1686 收官=ASR 终轨（R169 QC recipe medium-int8+beam5+noctx·16 cues/57.05s dropped=0 整轨一次过·"
"**题眼句 b0 100% 存活**+四句信条值全存活〔v5「桥上不问来路，落水都得拉一把」100% 全净〕+"
"**自指句「还是我剪的」/cta「下集台风夜之后」100% 全净**〔下集预告钩=系列第四件点名存活〕+六句计数+时间锚三年/十年/十年后全存活+"
"推演声明标签句值存活〔硅→归/档→大 承继族〕·实质退化如实 14 sites/20 chars〔hook 系列名 板块→反馈 R1683 族/b1 绘语路酷/浦→土/布→不/风→功/"
"先亮底→限量底/捎带→稍待/教→叫/诚实→城市 R1680 族变体/档案→大案 ×3 集中带/b10 尾「的」delete〕·"
"**9.8% 字位=BS 系带上缘外溢 0.7pp→S2 8.5 诚实扣**·字幕轨=edge-tts 直出 12/12 零损兜底=发布面零损）→"
"E8 评审单 review-20261008-bs014-v1.md（S1 10/10+S2 8.5+S3 9.0〔hits=[0] 系列连三+2.9s 余量系列最宽〕+S4 9.0+终审七席 E1/E2/E3/E5/E6/E7/E8 全 9.0）+"
"**E4 参考仪同轮回填 6.0**（02:12 Start-Process PID 1512 起飞与 ASR 并飞同窗 R809/R1680/R1683 同型→02:13:28 落判热载快落 ~1min·"
"会看完明说+点赞/转发条件式+**6 分明说=系列带最低读数**〔bs012 8.0/bs013 8.0/本件 6.0 如实入账·语录密度件理解成本上探·E4 材料面纯文本通道无卡面/系列语境注〕·"
"「结合 AI 科技与人文社会跨领域创意」正面定性·双旗=「数据是新黄浦江」比喻不直观+「风控做得好」意义不明确〔**双旗位皆 verbatim 信条例=CODEX §八 在册锚·来源律不可改写**·"
"MC-003 语境门槛族·吸收位=M5 图文页语境+系列语境〕·最弱=信息传达效率〔57s 短件固有·M6 校准位〕·净本 expert-verdicts/20261008-021328-E4-audience.md）→"
"M4 完成态——**F-162 登记**+冗余池第二十五件视频入池（release-schedule v3.10·件行落位）+backlog #103 done〔#104《台风夜之后》备位维持=lane 常备 ≥2 律〕；"
"**REACT-v12 顺延 F-163**（R978 判例·F-161 行预指 F-162 被本件占位=实际登记序单一真相）——"
"发布锁=M5 账号物理件（未上线=未测量）·未测面如实列（完播/互动实测=M6·M5 图文页语境层=E4 双旗+最弱吸收位·推演标注面挂账）\n")
p = "output/finished.md"
t = io.open(p, encoding="utf-8").read()
assert "F-162 登记" not in t, "F-162 already present"
if not t.endswith("\n"):
    t += "\n"
t += f162
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("OK finished.md F-162 appended")

# ---------- 2) renders README: bs-014 row upgrade ----------
patch(r"output\renders\README.md", [
    ("**在链·渲染腿毕（「板块十年」城市生长预演系列第三件·视频线新形态第三件·形态 C 图鉴语录卡混剪·#103 渲染腿=R1684 起链+S1 10/10 系列三连满分→R1685 渲染腿·**收官腿=E8→M4→F-162 登记=下轮**）**",
     "**成品·落位（F-162·「板块十年」城市生长预演系列第三件·视频线新形态第三件·形态 C 首件·#103 全链=R1684 起链+S1 10/10 系列三连满分→R1685 渲染腿→R1686 收官腿）**"),
    ("**收官腿=E8 终审〔ASR 终轨 R169 QC recipe+E4 参考仪〕→M4→F-162 登记=下轮**·tmp 批闭收账随收官轮 commit",
     "**收官腿毕=R1686**〔ASR 终轨 R169 QC recipe 16 cues/57.05s dropped=0·题眼句/自指句/cta 100% 存活+四句信条值全存活·9.8% 字位带上缘外溢 0.7pp=S2 8.5 诚实扣·字幕轨零损兜底+E4 6.0 同轮回填（系列带最低如实·双旗=verbatim 语境门槛族 M5 吸收位）+E8 评审单 review-20261008-bs014-v1.md 七席 ≥9→M4→**F-162 登记**〕·tmp 批闭收账随本轮 commit"),
])
print("OK renders README bs-014 row upgraded")

# ---------- 3) release-schedule v3.10 ----------
P = r"docs\release-schedule-v1.md"
t = io.open(P, encoding="utf-8").read()
# 3a) strip in-line note from BS-013 row tail (moves to new BS-014 row)
old_tail = "）；in-line 件行落位（R801/R804/R806/R809/R1683 修红律延续·视频号冗余弹药 23→24 件正字）。"
assert t.count(old_tail) == 1, "BS-013 row tail anchor not unique: %d" % t.count(old_tail)
t = t.replace(old_tail, "）；")
# 3b) insert BS-014 row after BS-013 row
row_bs014 = (
"+BS-014 板块十年件3 F-162（R1686·冗余池第二十五件视频·**「板块十年」城市生长预演系列第三件=视频线新形态第三件·形态 C 首件**〔形态 C 图鉴语录卡×编年史混剪+城市年谱时间轴压条·lane 常备 ≥2 律备货位 1/2·消费面双指名=本司视频线新形态+BigHouse P3 叙事规格候选·前件章尾钩兑现位=BS-013 cta 点名本件〕·R1684 起链〔S1 10/10 一次过=系列三连满分+四句未消费信条独占切面反重复 grep 零命中〕→R1685 渲染〔空气预算四道机械裁口 v5=57.05s 定稿 2.95s 余量·形态 C 拆条面首证 census-card-v13+对位 0.92+S2 三门全绿+帧验三律〕→R1686 收官〔ASR 终轨 16 cues dropped=0·**题眼句/自指句/cta 100% 存活**+四句信条值全存活·**9.8% 字位=带上缘外溢 0.7pp→S2 8.5 诚实扚**+E4 6.0 同轮回填（系列带最低如实·双旗=verbatim 语境门槛族）+七席 ≥9→M4〕）；in-line 件行落位（R801/R804/R806/R809/R1683/R1686 修红律延续·视频号冗余弹药 24→25 件正字）。\n"
)
anchor = "+BS-013 板块十年件2 F-161（R1683"
i = t.index(anchor)
line_end = t.index("\n", i)
t = t[:line_end] + "\n" + row_bs014 + t[line_end:]
# 3c) changelog v3.10 row
v310 = (
"- v3.10 2026-10-08 R1686：**冗余池扩容第二十五件视频入池**（BS-014《板块十年·这条街的口头禅》=F-162·成品库 161→162 件·**「板块十年」城市生长预演系列第三件·视频线新形态第三件·形态 C 首件**〔图鉴语录卡×编年史混剪+城市年谱时间轴压条·lane 常备 ≥2 律备货位 1/2·消费面双指名=本司视频线新形态+BigHouse P3 叙事规格候选·前件章尾钩兑现位=BS-013 cta 点名本件=钩兑现链第二证〕·R1684 起链〔S1 10/10 一次过=系列三连满分+四句未消费信条 verbatim 独占切面反重复 grep 零命中+一料多吃避让清单全执行〕→R1685 渲染〔空气预算四道机械裁口 v1 74.84s→v5 57.05s 定稿 2.95s 余量=fleet 最宽位·形态 C 视觉定谳=语录卡方图派生弃用+census-card-v13 图鉴拆条首证·对位 11/12=0.92 层 1.8 面上探五连+S2 三门全绿+帧验三律全过〕→R1686 收官〔ASR 终轨整轨一次过 16 cues dropped=0·题眼句/自指句/cta 100% 存活+四句信条值全存活〔v5 信条全净〕·9.8% 字位=带上缘外溢 0.7pp→S2 8.5 诚实扚（字幕轨=edge-tts 直出零损兜底）+E4 6.0 同轮回填（系列带最低读数如实·双旗=verbatim 语境门槛族·吸收位=M5 图文页语境+系列语境）+七席 ≥9→M4〕〕）；**in-line 盘点行计数 24→25 正字+BS-014 件行落位**（R801/R804/R806/R809/R1680/R1683/R1686 修红律延续）。\n"
)
t = t.rstrip("\n") + "\n" + v310
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("OK release-schedule v3.10 rows inserted")

# ---------- 4) station-reviews.md R1686 row ----------
sr_row = ("| 2026-10-08 | **E8 终审+M4+F 登记·BS-014《板块十年·这条街的口头禅》（R1686·backlog #103 收官腿·「板块十年」预演系列第三件·lane 常备 ≥2 律备货位 1/2·形态 C 首件）** | "
"bs-014-v1-shipinhao-60s.mp4+review-20261008-bs014-v1.md+asr-check.srt+asr-diff-r1686.txt | "
"E8 收官=ASR 终轨（R169 QC recipe·16 cues/57.05s dropped=0 整轨一次过·**题眼句 b0 100% 存活**+四句信条值全存活〔v5 侠气信条 100% 全净〕+**自指句/cta 100% 全净**〔下集预告钩=系列第四件点名存活〕+六句计数+时间锚全存活+推演标签句值存活〔硅→归/档→大 承继族〕·实质退化如实 14 sites/20 chars〔hook 系列名 板块→反馈 R1683 族/绘语路酷/浦→土/布→不/风→功/限量底/稍待/叫/城市/档案→大案 ×3〕·**9.8% 字位=带上缘外溢 0.7pp→S2 8.5 诚实扣**·字幕轨 edge-tts 12/12 零损兜底）"
"+评审单（S1 10/10〔R1684 系列三连满分〕+S2 8.5+S3 9.0〔hits=[0] 系列连三+2.9s 余量系列最宽〕+S4 9.0+终审七席 E1/E2/E3/E5/E6/E7/E8 全 9.0）"
"+E4 同轮回填 **6.0**（02:13:28 落判·会看完明说+点赞/转发条件式+**6 分明说=系列带最低读数**〔bs012 8.0/bs013 8.0/本件 6.0 如实入账〕·双旗=verbatim 信条例语境门槛族〔CODEX §八 在册锚不可改写〕·最弱=信息传达效率〔57s 固有·M6〕·净本 20261008-021328-E4-audience.md）"
"→M4 完成态→**F-162 登记**〔成品库第一百六十二件·形态 C 首件·冗余池第二十五件视频入池 v3.10〕+#103 done（lane 常备 1/2 收官·#104 备位维持）·REACT-v12 顺延 F-163〔R978 判例〕 |\n")
p = r"docs\reviews\station-reviews.md"
t = io.open(p, encoding="utf-8").read()
if sr_row.strip() in t:
    print("SKIP: station-reviews row already present")
else:
    if not t.endswith("\n"):
        t += "\n"
    t += sr_row
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("OK station-reviews R1686 row")

# ---------- 5) bs014 README changelog row ----------
readme_row = ("| 2026-10-08 | R1686 | 收官腿毕=ASR 终轨（R169 QC recipe 16 cues/57.05s dropped=0 整轨一次过·**题眼句 100% 存活**+四句信条值全存活〔v5 信条全净〕+自指句/cta 100% 全净·实质退化如实 14 sites/20 chars·**9.8% 字位=带上缘外溢 0.7pp=S2 8.5 诚实扣**·字幕轨零损兜底）+E4 6.0 同轮回填（系列带最低读数如实·双旗=verbatim 语境门槛族 M5 吸收位·净本 20261008-021328）+E8 评审单 review-20261008-bs014-v1.md（七席全 9.0）+M4+**F-162 登记**（成品库第一百六十二件·形态 C 首件·冗余池第二十五件 v3.10·lane 常备 1/2 收官·REACT-v12 顺延 F-163） |\n")
p = r"data\sources\bs014\README.md"
t = io.open(p, encoding="utf-8").read()
if readme_row.strip() in t:
    print("SKIP: bs014 README row already present")
else:
    if not t.endswith("\n"):
        t += "\n"
    t += readme_row
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("OK bs014 README R1686 row")

# ---------- 6) backlog #103 done + R1686 交付毕 note ----------
patch(r"src\os\backlog.md", [
    ("103. **「板块十年」城市生长预演系列·第三件《这条街的口头禅》全链起链**",
     "103. [done 2026-10-08] **「板块十年」城市生长预演系列·第三件《这条街的口头禅》全链起链**"),
    ("——余腿=E8 终审〔ASR 终轨 R169 QC recipe+E4 参考仪〕→M4→F-162 登记（下轮领）",
     "——余腿=E8 终审〔ASR 终轨 R169 QC recipe+E4 参考仪〕→M4→F-162 登记（下轮领）\n"
      "   **[R1686 交付毕 2026-10-08]**：收官腿=E8 终审〔ASR 终轨 R169 QC recipe 16 cues/57.05s dropped=0 整轨一次过·"
      "**题眼句 b0 100% 存活**+四句信条值全存活〔v5「桥上不问来路落水都得拉一把」100% 全净〕+"
      "**自指句/cta 100% 全净**〔下集预告钩=系列第四件《台风夜之后》点名存活〕+六句计数+时间锚全存活+推演标签句值存活·"
      "实质退化如实 14 sites/20 chars〔hook 系列名/绘语路酷/浦→土/布→不/风→功/限量底/稍待/叫城市/档案→大案 ×3〕·"
      "**9.8% 字位=带上缘外溢 0.7pp→S2 8.5 诚实扣**·字幕轨=edge-tts 直出 12/12 零损兜底〕"
      "+E4 参考仪同轮回填 **6.0**〔02:13:28 落判·会看完明说+6 分明说=**系列带最低读数如实入账**〔bs012 8.0/bs013 8.0/本件 6.0〕·"
      "双旗=verbatim 信条例语境门槛族〔CODEX §八 在册锚不可改写〕·吸收位=M5 图文页语境+系列语境·净本 20261008-021328-E4-audience〕"
      "+评审单 review-20261008-bs014-v1.md〔S1 10/10+S2 8.5+S3 9.0+S4 9.0+终审七席全 9.0〕"
      "→M4→**F-162 登记**（成品库第一百六十二件·「板块十年」系列第三件·视频线新形态第三件·**形态 C 首件**·"
      "冗余池第二十五件视频入池 v3.10）——**#103 全链收官**（R1684 起链→R1685 渲染→R1686 收官三轮链零断洞·"
      "lane 常备 1/2 收官·#104《台风夜之后》备位维持·REACT-v12 顺延 F-163）"),
])
print("OK backlog #103 done")
