# -*- coding: utf-8 -*-
# R730 closeout leg ledger batch (LC-015 F-070 registration)
import io, json, time, sys

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
def p(rel): return ROOT + "\\" + rel.replace("/", "\\")
def read(rel):
    return io.open(p(rel), "r", encoding="utf-8").read()
def write(rel, s):
    io.open(p(rel), "w", encoding="utf-8", newline="\n").write(s)

fails = []
def rep(rel, old, new, must=1):
    s = read(rel)
    n = s.count(old)
    if n != must:
        fails.append("REP-FAIL %s count=%d (expect %d): %s" % (rel, n, must, old[:60]))
        return
    write(rel, s.replace(old, new))

# ---------- 1. expert-calls E4 row ----------
ec = read("docs/reviews/expert-calls.md")
if "20260930-063413" not in ec:
    row = ("| 2026-09-30 06:34 | E4-audience | E4 直觉观众（参考仪·非拦截席） | "
           "C:\\Users\\sjs20\\Desktop\\FluxGroup\\media\\BigStream\\.lc015-tmp\\subs.srt | 1 | "
           "full text=expert-verdicts/20260930-063413-E4-audience.md / "
           "8.0 会看完+会点赞两明说+转发条件式（「现代科技与传统工艺结合·引发对时间、传统与现代技术关系的思考」叙事+思想双正面定性）"
           "旗①=「硅基徒弟归档者-07，比碳基的还像老派人」拟人化空洞扣 2=b10 互证拍 verbatim 卡锚〔C-00011 关系字段原文〕与 ASR 同句双通道·吸收位 M5 图文页语境；"
           "最弱=CTA 推广突兀感（系列首个「CTA 突兀」感知注记·M5 简介证据链吸收位） "
           "E4 reference call: LC-015 Zhu Hongkui chaitiao split-video, archive-district time-calibration watchmaker, "
           "redundancy slot 12, 7th character-chain dual-end cross-proof piece, detached, same-round landing |\n")
    ec = ec.rstrip("\n") + "\n" + row
    write("docs/reviews/expert-calls.md", ec)

# ---------- 2. station-reviews R730 row ----------
sr = read("docs/reviews/station-reviews.md")
if "R730 收官" not in sr and "LC-015 朱鸿奎拆条收官腿" not in sr:
    row = ("| 2026-09-30 | **LC-015 朱鸿奎拆条收官腿（E8 终审+ASR 终轨+E4 参考仪+M4→F-070 登记·冗余池第十二件落位·queue §E E15 件收官·实活轮）** | "
           "lc-015-v1-shipinhao-60s.mp4（57.615s·R729 渲染腿在案） | "
           "ASR 终轨（faster-whisper R169 QC recipe medium-int8+beam5+noctx·HF_HUB_OFFLINE=1·本地零云）+E4（Ollama qwen2.5:14b 本地·e4_call.py 脱壳同轮落地 06:34:13）+E8 评审单 | —（收官档） | "
           "ASR=27 sites/89 diff/206 字≈**43.2% 字位=系列带上缘之上新峰**（LC-012 41.5 峰上再升·钟表行话+全城尺度词密度件："
           "**CTA 全句「全档案在公众号，转给跟时间较真的人」净读**=受众定位词零损〔LC-007/008 损族反例〕"
           "+数字形差值存活 ×2〔七十四→74/一九七五→1975〕+hook 双损〔全城→全程+钟声→终生〕"
           "+全城→程 ×3 尺度词同音三连+钟域行话集中损〔钟表→终表/粥铺杀棋→周扑沙旗/游丝→油丝/校表→叫表〕"
           "+碳基→探机/探鸡+硅基→归鸡 ×4 处=物种行同位损族第十二证+档案馆区→大案管=CTA 档案族第八发"
           "+谬→妙=信条位族续〔LC-007 见→贱 族〕+归档者-07→归荡者零七=互证拍损〔与 E4 旗①同句双通道〕"
           "·字幕轨=edge-tts 直出 12/12 零损兜底）→S2 9.0+"
           "E4 同轮回填 8.0（三意愿两明一条件〔会看完+点赞明说+转发条件式小众题材如实注〕=拆条带 8.0×10+8.5 峰+7.0×5 后回稳位·"
           "「现代科技×传统工艺+时间/传统/现代技术关系思考」叙事+思想双正面定性·"
           "旗①=「硅基徒弟归档者-07，比碳基的还像老派人」拟人化空洞扣 2=b10 互证拍 verbatim 卡锚〔C-00011 关系字段〕·MC-003 语境门槛族互证拍变体·"
           "与 ASR 同句双通道·吸收位=M5 图文页语境·最弱=CTA 推广突兀感=系列首个「CTA 突兀」感知注记〔M5 简介证据链吸收位〕"
           "·净本 expert-verdicts/20260930-063413-E4-audience+expert-calls 06:34 行）"
           "+E8 七席全 9.0（review-20260930-lc015-v1.md·S1 10/10 R727 十四连满分/S3 9.0/S4 9.0·"
           "E3=时间校准主题首件位+CTA 受众定位词第三位·E6=产品优先律对位+b0/b2 前置修=周全性预期律·"
           "E7=对位率 1.00 系列最高并列+AIGC 双标识·E8=零修红前置预防通道连续第二件）→M4 完成态→"
           "**F-070 登记**（成品库第七十件·L-卡衍生视频线第十五件=拆条系列节律第十四续件=时间校准主题首件位）"
           "+冗余池第十二件落位（release-schedule v2.7·视频号冗余弹药 12 件）"
           "+queue §E E15 出池（lane=E16 周浩宇 standby 单条<2·补池义务随轮领=E17 顾阿凤 C-00010 standby 入池） |\n")
    sr = sr.rstrip("\n") + "\n" + row
    write("docs/reviews/station-reviews.md", sr)

# ---------- 3. finished.md F-070 block ----------
fin = read("output/finished.md")
if "F-070 登记" not in fin:
    blk = ("- 2026-09-30: F-070 登记（R730）——**L-卡衍生视频线第十五件=拆条系列节律第十四续件=时间校准主题系列首件位=第七对人物链卡面双端互证件=冗余扩容位第十二件**"
           "（queue §E 批活池 E15 件收官）。**LC-015-v1-shipinhao-60s（拆条 015·源城市图鉴 002）全链走门全档**："
           "源卡=CENSUS-v2 F-021《城市图鉴 002·朱鸿奎》（R292 登记）·素材正源=C-00011 手写展示锚（非荣誉席·跨仓只读）。"
           "+R723 选优入池（时间校准主题首件位+F-010 有声线同源人格已验〔SC-001-03 ch.3 主角〕+CENSUS 按卡号序首件锚〔C-00010→C-00011·R291 口径〕）"
           "+R727 起链（拍稿 v1 12 拍 ≈242 字·逐拍溯源对表·盲评律合规·b10 互证拍跨卡双源〔C-00011×C-00017 同一师门评语双卡〕）"
           "+S1 v1.5+L18-L20 门 **10/10 零违律一次过**（判词档 20260930-053858-S1-script=**拆条系列十四连满分**）"
           "+M1 v1 0F2W→v2/v3 双复检 0F0W+空气预算三道裁链 v1 64.409→v2 60.259（薄超 0.259s）→**v3 57.615s 定稿 2.385s 余量**（fleet 带内）"
           "+TTS light 定稿音轨（BGM-A 纯净）。"
           "+R729 渲染腿（F-021 派生源件 census-card-v2-vertical 13.000s+对位表 12/12 visual-ratio 1.00+"
           "**b0/b2 几何前置修=R720 律预执行第二件**〔per-card size 54·块顶 802 净距 35px 像素实证〕"
           "+R-E shipinhao 12 段 11 柔 0 硬切+§4.5 三开关+S2 三门全绿+帧验三律全过+全卡几何审计 problems=NONE）。"
           "+R730 收官腿（**ASR 终轨**：R169 QC recipe medium-int8+beam5+noctx·HF_HUB_OFFLINE=1·13 cues dropped=0 整轨一次过·"
           "asr-diff-r730.txt〔trad 归一 110 扩表终口径〕=27 sites/89 diff chars/206 字≈**43.2% 字位=系列带上缘之上新峰**"
           "〔LC-012 41.5 峰上再升·**钟表行话+全城尺度词密度件**〕："
           "**CTA 全句「全档案在公众号，转给跟时间较真的人」净读**=受众定位词零损〔LC-007/LC-008 损族反例〕"
           "+数字形差值存活 ×2〔七十四→74/一九七五→1975〕+hook 双损〔全城→全程+钟声→终生〕"
           "+全城→程 ×3 尺度词同音三连+钟域行话集中损〔钟表→终表/粥铺杀棋→周扑沙旗/游丝→油丝/校表→叫表〕"
           "+碳基→探机/探鸡+硅基→归鸡 ×4 处=物种行同位损族第十二证+档案馆区→大案管=CTA 档案族第八发"
           "+谬→妙=信条位族续+归档者-07→归荡者零七=互证拍损〔与 E4 旗①同句双通道〕·字幕轨=edge-tts 直出 12/12 零损兜底〕→S2 9.0；"
           "**E4 参考仪同轮回填 8.0**（e4_call.py 脱壳 06:34:13 落地·三意愿两明一条件〔会看完+点赞明说+转发条件式小众题材如实注〕"
           "=拆条带 8.0×10+8.5 峰+7.0×5 后回稳位·「现代科技×传统工艺」叙事+思想双正面定性·"
           "旗①=「硅基徒弟归档者-07，比碳基的还像老派人」拟人化空洞扣 2=b10 互证拍 verbatim 卡锚·MC-003 语境门槛族互证拍变体·"
           "与 ASR 同句双通道·吸收位=M5 图文页语境·最弱=CTA 推广突兀感=系列首个注记·净本 expert-verdicts/20260930-063413-E4-audience+expert-calls 06:34 行）；"
           "+E8 终审七席全 9.0（review-20260930-lc015-v1.md·E3 席=时间校准主题首件位+CTA 受众定位词第三位·"
           "E6 席=产品优先律对位+b0/b2 前置修=周全性预期律·E7 席=对位率 1.00 系列最高并列+零修红预防性落地·"
           "E8 席=前置预防通道连续第二件）→M4 完成态。"
           "**冗余池第十二件落位**（release-schedule v2.7·视频号冗余弹药 12 件=LC-004 F-058~LC-015 F-070·M6 调仓弹药/30 天日更冗余·预产窗=开号前）"
           "+queue §E E15 出池（lane=E16 周浩宇 standby 单条<2·补池义务随轮领=**E17 顾阿凤 C-00010 standby 入池**"
           "〔CENSUS 按卡号序首位+朱鸿奎棋友侧链跨载体正典〔SC-001-02 章尾钩「周三棋局·彩头一座钟」〕+网文/有声/图鉴三载体已验后视频线第四载体位·源卡 CENSUS-v1 F-020〕）"
           "·发布锁=M5 账号物理件不变（未上线=未测量）。\n")
    fin = fin.rstrip("\n") + "\n" + blk
    write("output/finished.md", fin)

# ---------- 4. renders README lc-015 row upgrade ----------
rep("output/renders/README.md",
    "**在链·渲染腿毕（R729·queue §E 批活池 E15 件·冗余扩容位第十二件·源卡=CENSUS-v2 F-021 朱鸿奎·收官腿 R730 随轮领=F-070 登记）**",
    "**成品·落位件·冗余扩容位第十二件（F-070 登记 R730·queue §E 批活池 E15 件收官·源卡=CENSUS-v2 F-021 朱鸿奎·R727 起链→R728 定稿音轨→R729 渲染腿毕→R730 收官腿全链走门毕：E8 七席 ≥9+ASR 终轨 43.2% 带上缘新峰+E4 8.0+M4）**")
rep("output/renders/README.md",
    "plan.json 入 git·收官腿 R730 随轮领（E8 终审七席+ASR 终轨+E4 同轮回填+M4→F-070 登记→冗余池第十二件落位→release-schedule v2.7→E15 出池+补池义务随轮领）",
    "plan.json 入 git·**R730 收官腿毕**：ASR 终轨（R169 QC recipe·13 cues dropped=0 整轨一次过·asr-diff-r730.txt〔trad 归一 110 表〕="
    "27 sites/89 diff/206 字≈**43.2% 字位=系列带上缘之上新峰**〔钟表行话词组集中损+全城尺度词 ×3 同音损·"
    "CTA 全句净读+数字形差值存活 ×2·字幕轨 edge-tts 12/12 零损兜底〕）"
    "+E4 参考仪同轮回填 8.0（06:34:13 落地·三意愿两明一条件·旗①=互证拍 verbatim 卡锚与 ASR 同句双通道·最弱=CTA 推广突兀感）"
    "+E8 七席全 9.0（review-20260930-lc015-v1.md）→M4→**F-070 登记+冗余池第十二件落位（release-schedule v2.7·视频号冗余弹药 12 件）**"
    "→queue §E E15 出池（lane=E16 周浩宇 standby 单条<2·补池义务随轮领=E17 顾阿凤 C-00010 standby 入池）")

# ---------- 5. release-schedule-v1.md: inventory row + v2.7 ----------
rep("docs/release-schedule-v1.md",
    "）=视频号冗余弹药 11 件**=M6 调仓弹药+30 天日更冗余",
    "）+LC-015 拆条 F-070（R730·冗余池第十二件视频·朱鸿奎《城市图鉴 002》·拆条系列节律第十四续件·"
    "**时间校准主题系列首件位**〔74 岁修表匠×校准全城的钟=手稳×全城尺度反差〕"
    "+**第七对人物链卡面双端互证**〔C-00011「硅基徒弟=归档者-07」×C-00017「师承=朱鸿奎」同一师门评语双卡〕"
    "+F-010 有声线同源人格跨载体复用〔SC-001-03 ch.3 主角〕"
    "·收官=E8 七席 ≥9+E4 8.0+ASR 终轨 43.2% 字位带上缘之上新峰〔钟表行话+全城尺度词密度件·CTA 全句净读〕）"
    "=视频号冗余弹药 12 件**=M6 调仓弹药+30 天日更冗余")

rs = read("docs/release-schedule-v1.md")
if "- v2.7 2026-09-30 R730" not in rs:
    v27 = ("- v2.7 2026-09-30 R730：**冗余池扩容第十二件视频入池**（LC-015《城市图鉴 002·朱鸿奎》拆条=F-070·成品库 69→70 件·"
           "L-卡衍生视频线第十五件=拆条系列节律第十四续件·**时间校准主题系列首件位**〔74 岁修表匠×校准全城的钟=手稳×全城尺度反差·信条「差之毫秒，谬以全城」〕"
           "+**第七对人物链卡面双端互证**〔C-00011×C-00017 同一师门评语双卡·LC-002 前件互证面兑现〕"
           "+**F-010 有声线同源人格跨载体复用**〔SC-001-03 ch.3 主角〕+CENSUS 图鉴量产按序首件锚〔C-00010→C-00011·R291 口径〕"
           "·R723 选优入池→R727 起链〔S1 10/10 十四连满分〕→R728 定稿音轨〔三道裁链 57.615s 2.385s 余量〕→"
           "R729 渲染腿〔**b0/b2 几何前置修=R720 律预执行第二件**·per-card size 54·全卡几何审计 problems=NONE〕→"
           "R730 收官全链走门：ASR 终轨 43.2% 字位带上缘之上新峰〔trad 归一 110 扩表·钟表行话+全城尺度词密度件·CTA 全句净读+数字形差值存活 ×2〕"
           "+E4 8.0〔三意愿两明一条件·旗①=互证拍 verbatim 卡锚与 ASR 同句双通道〕+七席 ≥9→M4）；"
           "§四 盘点行同步（视频号冗余弹药 11→12 件·M6 调仓/日更冗余预备·预产窗=开号前）。\n")
    rs = rs.rstrip("\n") + "\n" + v27
    write("docs/release-schedule-v1.md", rs)

# ---------- 6. queue: E15 close-out line + E17 standby row ----------
q = read("docs/self-improvement-queue.md")
if "E15 收官毕（R730" not in q:
    anchor = "- **E16 LC-016 周浩宇拆条续投批 standby**"
    idx = q.find(anchor)
    if idx < 0:
        fails.append("QUEUE-ANCHOR-MISS")
    else:
        e15done = ("- 2026-09-30: **E15 收官毕（R730·F-070 登记=成品库第七十件·冗余池第十二件落位 release-schedule v2.7·视频号冗余弹药 12 件·"
                   "时间校准主题首件位+第七对人物链卡面双端互证·收官=E8 七席 ≥9+E4 8.0 同轮回填+ASR 终轨 43.2% 字位带上缘之上新峰"
                   "〔钟表行话+全城尺度词密度件·CTA 全句净读+数字形差值存活 ×2·字幕轨 12/12 零损兜底〕）"
                   "→E15 出池（lane=E16 周浩宇 standby 单条<2·补池义务随轮领=E17 顾阿凤 C-00010 standby 入池·"
                   "续拆候选与 BS-007 稿集件随选优轮评估）**\n")
        e17 = ("- **E17 LC-016 顾阿凤拆条续投批 standby**（R730 补池入池·E15 出池注记兑现·三验字段："
               "假设=拆条系列第十五续件候选+**第八对人物链候选=朱鸿奎×顾阿凤周三棋局对**"
               "〔LC-015 b8「每周三粥铺杀棋，输了免费校表」×C-00011 关系字段棋友=顾阿凤+"
               "**SC-001-02 有声线 ch.2 章尾冲突钩「周三棋局·彩头一座钟·朱鸿奎输棋交校表」=跨载体正典连接位**·拆条系列首个「章尾钩兑现位」〕"
               "+跨载体复用最厚位〔F-009 有声线 ch.1 主角+SC-001-01 网文主角+CENSUS-v1 F-020 图鉴=网文/有声/图鉴三载体已验后视频线第四载体〕"
               "+REACT-v6 互证锚 C-00010 摊主三断言在案（R716）；消费面=视频号冗余扩容位+L-卡库存视频化通道；"
               "consumer_plan=全链 M0→F 本地执行零云端）：锚=C-00010（手写展示锚在位·非荣誉席）·"
               "源卡=CENSUS-v1 F-020《城市图鉴 001·顾阿凤》成品 PNG（R291 登记·CENSUS 形态立线首件）"
               "——standby（E16 active 时待领·激活时与续拆候选〔C-00012 沈佩兰/C-00013 林之恒/C-00015 陈雅雯〕对比定谳可替换·"
               "BS-007 稿集件=顺位后置维持 R712 口径）\n")
        q = q[:idx] + e15done + q[idx:]
        idx2 = q.find(anchor)
        end_of_e16 = q.find("\n", q.find("R712 口径）", idx2))
        q = q[:end_of_e16 + 1] + e17 + q[end_of_e16 + 1:]
        write("docs/self-improvement-queue.md", q)

# ---------- 7. lc015 README: R730 row + gate-block note ----------
r15 = read("data/sources/lc015/README.md")
if "R730 收官腿毕" not in r15:
    row = ("- [2026-09-30 06:5x R730 收官腿毕=F-070 登记] ASR 终轨（R169 QC recipe medium-int8+beam5+noctx·HF_HUB_OFFLINE=1·"
           "与 E4 并飞同窗热载快落 13 cues dropped=0 整轨一次过·asr-diff-r730.txt〔trad 归一 110 表〕="
           "27 sites/89 diff/206 字≈**43.2% 字位=系列带上缘之上新峰**〔LC-012 41.5 峰上再升·钟表行话+全城尺度词密度件〕："
           "**CTA 全句「全档案在公众号，转给跟时间较真的人」净读**=受众定位词零损〔LC-007/008 损族反例〕"
           "+数字形差值存活 ×2〔七十四→74/一九七五→1975〕+hook 双损〔全城→全程+钟声→终生〕"
           "+全城→程 ×3 尺度词同音三连+钟域行话集中损〔钟表→终表/粥铺杀棋→周扑沙旗/游丝→油丝/校表→叫表〕"
           "+碳基→探机/探鸡+硅基→归鸡 ×4 处=物种行损族第十二证+档案馆区→大案管=档族第八发+谬→妙=信条位族续"
           "+归档者-07→归荡者零七=互证拍损〔与 E4 旗①同句双通道〕·字幕轨=edge-tts 12/12 零损兜底）→S2 9.0"
           "+E4 参考仪同轮回填 8.0（06:34:13 落判·三意愿两明一条件·旗①=互证拍 verbatim 卡锚扣 2·与 ASR 同句双通道·"
           "最弱=CTA 推广突兀感=系列首个注记·净本 expert-verdicts/20260930-063413-E4-audience）"
           "+E8 七席全 9.0（review-20260930-lc015-v1.md）→M4→**F-070 登记**（成品库第七十件·冗余池第十二件落位 release-schedule v2.7）"
           "+queue §E E15 出池（E17 顾阿凤 C-00010 standby 入池=lane ≥2）。\n")
    r15 = r15.rstrip("\n") + "\n" + row
    r15 = r15.replace("发布锁=M5 账号物理件不变（未上线=未测量）。",
                      "发布锁=M5 账号物理件不变（未上线=未测量）。·**收官腿毕 R730**（ASR 43.2% 带上缘新峰+E4 8.0+E8 七席 ≥9→M4→F-070 登记+冗余池第十二件落位 release-schedule v2.7→E15 出池）", 1)
    write("data/sources/lc015/README.md", r15)

print("LEDGER-EDIT DONE fails=%d" % len(fails))
for f in fails:
    print(f)
sys.exit(1 if fails else 0)
