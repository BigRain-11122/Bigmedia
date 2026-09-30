# -*- coding: utf-8 -*-
# R734 close script: LC-016 closeout ledgers + state.json + status-export.json
import io, json, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
def p(rel): return ROOT + "\\" + rel
ts_now = time.strftime("%Y-%m-%d %H:%M:%S")

LOG = ("2026-09-30 08:0x R734: 生产轮·LC-016 顾阿凤拆条收官腿毕=F-071 登记+冗余池第十三件落位（queue §E 批活池 E17 件收官·R733 指针①兑现·R726/R730 同型·实活轮·产品优先律对位=本轮实物增量=lc-016 成片 F-071 入成品库）——"
 "①轮首五查静（r694_probe 自跑 08:01：orders 顶 O-20260928-1910 42 件锚未动/ledger 六模式 CaseSensitive 41=锚零新 CEO 令级事件〔L189/L190=R698/R700 已收讫+L245 值守行位移非事件〕/decisions UTF8 非空行 75=锚零新行/production=open 自愈核在位 tick733/无 index.lock·树态=bm-a codex 批未闭让位维持〔README/city-humanities mtime 09-29 04:06 未动=#86 c+d 判据未达·两文件零接触〕+自产 tmp 族预期态）"
 "+三探针=board exit=0 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面+1 发现（render-unannot lc-016=在链预期红·R730 同型·F-071 登记+renders 行升成品即清）/loop_health 2 FAIL+81 WARN 皆在案史实类（2 outage 同事件足迹已裁定不重复触发·tick734 收账自平口径）；"
 "②ASR 终轨（R169 QC recipe medium-int8+beam5+noctx·HF_HUB_OFFLINE=1·07:56:59 与 E4 并飞双脱壳·12 cues 整轨一次过·asr-diff-r734.txt〔trad 归一 78 表复用·LC-016 run 零繁体输出=归一表缺口面零·对照 LC-014 首跑裸 53.8% 教训正面例〕）=20 sites/67 diff chars/209 字≈32.1% 字位=系列带内（LC-014 32.7 同位带·LC-015 43.2 峰下回落·沪语烟火词域件）：关键存活 21/40（顾阿凤/朱鸿奎净读+台风/这条街就是家/蒸笼/儿子在现实世界/每年来住半个月/第一口热乎气/比什么口号都金贵/每周三/信条/路过的都是客+数字形差值存活 ×3〔68 岁/4 点半/1992〕）+实质退化如实（hook 双损=系统日志→日制〔系列在案同音族〕+早班信使→信时/碳基→探机=物种行同位损族第十三证/脑环广场→老黄+粥铺→州部=专名损/灶上→早上=信条位核心字损/全档案→全答案=CTA 档案族第九发/转给惦记→转给电机=CTA 受众定位词损〔LC-007/008 损族同型复发〕/棋友→街友=互证拍词损）·字幕轨=edge-tts 直出 12/12 零损兜底→S2 9.0；"
 "③E4 参考仪同轮回填 8.0（e4_call.py 脱壳同窗落地·三意愿=会看完明说+点赞可能式+转发条件式〔朋友对人文故事兴趣〕=拆条带 8.0×10+8.5 峰+7.0×5 后 8.0 回稳位第二连·「温情和人文关怀·平凡人物在现代化城市中的独特存在」+「AI 生成内容与主题契合度」正面定性·旗①=「儿子在现实世界，每年来住半个月」设定突兀扣 1=锚经历字段 verbatim〔纪实线城市收留现实照片转生设定面〕·MC-003 语境门槛族经历字段变体·吸收位=M5 图文页语境+系列语境·最弱=创新性和故事独特性=温情故事常见型〔体裁面·M6 校准位〕·净本 expert-verdicts/20260930-075659-E4-audience+expert-calls 07:56 行）；"
 "④E8 评审单 review-20260930-lc016-v1.md（S1 10/10〔R731 十五连满分〕+S2 9.0+S3 9.0+S4 9.0+终审七席 E1/E2/E3/E5/E6/E7/E8 全 9.0·E3 席=CTA 受众定位词第四位+跨载体复用最厚位〔网文/有声/图鉴三载体已验→视频线第四载体〕+章尾钩兑现位·E6 席=产品优先律对位+b2/b3/b8 前置修=周全性预期律·E7 席=对位率 1.00 系列最高并列+零修红预防性落地·E8 席=前置预防通道连续第三件〔LC-014 b4+LC-015 b0/b2+LC-016 b2/b3/b8〕）→M4 完成态；"
 "⑤F-071 登记（成品库第七十一件·L-卡衍生视频线第十六件=拆条系列节律第十五续件=第八对人物链卡面双端互证件=章尾钩兑现位）+冗余池第十三件落位（release-schedule v2.8·视频号冗余弹药 13 件）+renders 行升成品+lc016 README 收口+station-reviews R734 行+queue §E E17 出池+E18 林之恒 C-00013 standby 入池（lane=E16+E18 ≥2 达标·选优=三源连接位〔C-00010×C-00013 双卡年轮互记+互聊台账 2 条 R512 在案=第九对人物链候选〕+档案记忆主题反差位·runner-up=沈佩兰 C-00012〔卡号序最前但零连接位〕/陈雅雯 C-00015〔REACT-v6 信条收束在案·量化近域〕注记·激活时选优门=档案馆区与 LC-002 同城区近域→拍稿须差异化角度位）；"
 "⑥例行件：日报 09-30 在案不重跑（R713 补产）/W40 周审在案（R576）/月度注记在案（R-20260928-03）/global-benchmarks day6 ≤7 跳过（下期 10-01=#80 并窗勿提前触碰）/#70 OSS 窗 2 切片=10-02 21:40 前随轮领（窗面义务足 R644）/#86 c+d 让位判据未达（codex mtime 04:06 未动）/T1 催办=已裁项停用口径/HQ-FEEDBACK 不写（双锚静零膨胀）·tokens:local=1（E4 qwen2.5:14b 本轮落地记账·本地 Ollama 零 API token·ASR=faster-whisper 本地·P-54⑤ 计量律如实记）"
 "——下轮=R735 可领序：①E16/E18 lane 选优起链（queue §E 拆条系列第十六续件·R731 同型）②#70 OSS 窗 2 切片（≤10-02 21:40）③#86 c+d 让位判据④global-benchmarks 10-01 刷新（#80 并窗）。收账显式列文件 commit+push")

FOCUS = ("R735: ①E16/E18 lane 选优起链（queue §E 拆条系列第十六续件·起链五腿=R731 同型·E16 激活选优门注记随行）②#70 OSS 窗 2 切片（≤10-02 21:40·切片 1 R644 在案）③#86 c+d 让位判据（bm-a codex 批闭 commit 落地）④global-benchmarks 10-01 刷新（#80 并窗）——五查锚=orders O-20260928-1910 42·ledger 41（L189/L190/L245 注）·decisions 75")

F071_ROW = ("- 2026-09-30: F-071 登记（R734）——**L-卡衍生视频线第十六件=拆条系列节律第十五续件=第八对人物链卡面双端互证件=章尾钩兑现位=跨载体复用最厚位（网文/有声/图鉴三载体已验→视频线第四载体）=冗余扩容位第十三件**（queue §E 批活池 E17 件收官）。"
 "**LC-016-v1-shipinhao-60s（拆条 016·源城市图鉴 001）全链走门全档**：源卡=CENSUS-v1 F-020《城市图鉴 001·顾阿凤》（R291 登记·CENSUS 形态立线首件）·素材正源=C-00010 手写展示锚（非荣誉席·跨仓只读·原型样板 P-0）。"
 "+R730 补池选优入池（E15 出池注记兑现·四胜位 over 周浩宇：前件点名兑现位+跨载体复用最厚位+题材零重复+源卡立线首件 PNG 在位核）+R731 起链（拍稿 v1 12 拍 ≈245 字·逐拍溯源对表·盲评律合规·b10 第八对人物链互证拍跨卡双源〔C-00010「棋友=朱鸿奎」×C-00011「棋友=顾阿凤」双端在册〕·SC-001-02 ch.2 章尾钩=拆条系列首个「章尾钩兑现位」）"
 "+S1 v1.5+L18-L20 门 **10/10 零违律一次过**（判词档 20260930-070337-S1-script=**拆条系列十五连满分**）+M1 v1 0F1W→v3 **0F0W**+空气预算两道机械裁链 v1 66.101→v2 62.110→**v3 57.638s 定稿入窗 2.362s 余量**（fleet 带内·LC-015 v3 同位带）+TTS light 定稿音轨（BGM-A 纯净）。"
 "+R733 渲染腿（F-020 派生源件 census-card-v1-vertical 13.000s+对位表 12/12 visual-ratio 1.00+**b2/b3/b8 前置几何修=R720 律预执行第三件**〔per-card size 48/46/56 verbatim 零字符·块顶 817/787/798 净距 50/20/31px〕+R-E shipinhao 12 段 11 柔 0 硬切+§4.5 三开关+S2 三门全绿+帧验三律全过+全卡几何审计 problems=NONE）。"
 "+R734 收官腿（**ASR 终轨**：R169 QC recipe medium-int8+beam5+noctx·HF_HUB_OFFLINE=1·07:56:59 与 E4 并飞双脱壳·12 cues 整轨一次过·asr-diff-r734.txt〔trad 归一 78 表复用·LC-016 run 零繁体输出=归一表缺口面零·对照 LC-014 首跑裸 53.8% 教训正面例〕=20 sites/67 diff chars/209 字≈**32.1% 字位=系列带内**〔LC-014 32.7 同位带·LC-015 43.2 峰下回落·沪语烟火词域件〕：**关键存活 21/40**〔顾阿凤/朱鸿奎净读+台风/这条街就是家/蒸笼/儿子在现实世界/每年来住半个月/第一口热乎气/比什么口号都金贵/每周三/信条/路过的都是客+数字形差值存活 ×3〔68 岁/4 点半/1992〕〕+实质退化如实〔hook 双损=系统日志→日制〔系列在案同音族〕+早班信使→信时/碳基→探机=物种行同位损族第十三证/脑环广场→老黄+粥铺→州部=专名损/灶上→早上=信条位核心字损/全档案→全答案=CTA 档案族第九发/转给惦记→转给电机=CTA 受众定位词损〔LC-007/008 损族同型复发〕/棋友→街友=互证拍词损〕·字幕轨=edge-tts 直出 12/12 零损兜底〕→S2 9.0；"
 "**E4 参考仪同轮回填 8.0**（e4_call.py 脱壳同窗落地·三意愿=会看完明说+点赞可能式+转发条件式〔朋友对人文故事兴趣〕=**拆条带 8.0×10+8.5 峰+7.0×5 后 8.0 回稳位第二连**·「温情和人文关怀·平凡人物在现代化城市中的独特存在」+「AI 生成内容与主题契合度」正面定性·旗①=「儿子在现实世界，每年来住半个月」设定突兀扣 1=锚经历字段 verbatim〔纪实线城市收留现实照片转生设定面〕·MC-003 语境门槛族经历字段变体·吸收位=M5 图文页语境+系列语境·最弱=创新性和故事独特性=温情故事常见型〔体裁面·M6 校准位〕·净本 expert-verdicts/20260930-075659-E4-audience+expert-calls 07:56 行）；"
 "+E8 终审七席全 9.0（review-20260930-lc016-v1.md·E3 席=CTA 受众定位词第四位+跨载体复用最厚位·E6 席=产品优先律对位+b2/b3/b8 前置修=周全性预期律·E7 席=对位率 1.00 系列最高并列+零修红预防性落地·E8 席=前置预防通道连续第三件）→M4 完成态。"
 "**冗余池第十三件落位**（release-schedule v2.8·视频号冗余弹药 13 件=LC-004 F-058~LC-016 F-071·M6 调仓弹药/30 天日更冗余·预产窗=开号前）+queue §E E17 出池+E18 林之恒 C-00013 standby 入池（lane=E16+E18 ≥2 达标）·发布锁=M5 账号物理件不变（未上线=未测量）。")

SR_ROW = ("| 2026-09-30 | **LC-016 顾阿凤拆条收官腿（E8 终审+ASR 终轨+E4 参考仪+M4→F-071 登记·冗余池第十三件落位·queue §E E17 件收官·实活轮）** | lc-016-v1-shipinhao-60s.mp4（57.638s·R733 渲染腿在案）+asr-check.srt+asr-diff-r734.txt | ASR 终轨（faster-whisper R169 QC recipe medium-int8+beam5+noctx·HF_HUB_OFFLINE=1·本地零云）+E4（Ollama qwen2.5:14b 本地·e4_call.py 脱壳 07:56:59 双飞窗同轮落地）+E8 评审单 | —（收官档） | "
 "ASR=20 sites/67 diff/209 字≈**32.1% 字位=系列带内**（LC-014 32.7 同位带·LC-015 43.2 峰下回落·沪语烟火词域件·trad 78 表复用·零繁体输出=归一缺口面零〔对照 LC-014 首跑裸 53.8% 教训正面例〕：关键存活 21/40〔顾阿凤/朱鸿奎净读+台风/这条街就是家/蒸笼/儿子在现实世界/每年来住半个月/第一口热乎气/比什么口号都金贵/每周三/信条/路过的都是客+数字形差值存活 ×3〕+实质退化如实〔hook 双损=系统日志→日制+早班信使→信时/碳基→探机=物种行损族第十三证/脑环广场→老黄+粥铺→州部=专名损/灶上→早上=信条位核心字损/全档案→全答案=CTA 档案族第九发/转给惦记→转给电机=受众定位词损〔LC-007/008 损族同型复发〕/棋友→街友=互证拍词损〕·字幕轨=edge-tts 直出 12/12 零损兜底）→S2 9.0"
 "+E4 同轮回填 8.0（三意愿=会看完明说+点赞可能式+转发条件式〔朋友对人文故事兴趣〕=拆条带 8.0×10+8.5 峰+7.0×5 后回稳位第二连·「温情和人文关怀·平凡人物在现代化城市中的独特存在」正面定性·旗①=「儿子在现实世界，每年来住半个月」设定突兀扣 1=锚经历字段 verbatim·MC-003 语境门槛族经历字段变体·吸收位=M5 图文页语境+系列语境·最弱=创新性和故事独特性=温情常见型体裁面·净本 expert-verdicts/20260930-075659-E4-audience+expert-calls 07:56 行）"
 "+E8 七席全 9.0（review-20260930-lc016-v1.md·S1 10/10 R731 十五连满分/S3 9.0/S4 9.0·E3=CTA 受众定位词第四位+跨载体复用最厚位·E6=产品优先律对位+b2/b3/b8 前置修=周全性预期律·E7=对位率 1.00 系列最高并列·E8=前置预防通道连续第三件）→M4 完成态→**F-071 登记**（成品库第七十一件·L-卡衍生视频线第十六件=拆条系列节律第十五续件=第八对人物链双端互证件=章尾钩兑现位）+冗余池第十三件落位（release-schedule v2.8·视频号冗余弹药 13 件）+queue §E E17 出池+E18 林之恒 C-00013 standby 入池（lane=E16+E18 ≥2 达标） | ")

E17_DONE = ("- 2026-09-30: **E17 收官毕（R734·F-071 登记=成品库第七十一件·冗余池第十三件落位 release-schedule v2.8·视频号冗余弹药 13 件·第八对人物链卡面双端互证件=章尾钩兑现位·跨载体复用最厚位〔三载体已验→视频线第四载体〕·收官=E8 七席 ≥9+E4 8.0 同轮回填〔旗①=经历字段「儿子在现实世界」语境门槛族变体〕+ASR 终轨 32.1% 字位带内〔trad 78 表复用·零繁体输出=归一缺口面零·CTA 档案族第九发+受众定位词损如实〕·字幕轨 edge-tts 12/12 零损兜底〕）→E17 出池（lane=E16 周浩宇 standby 单条<2·补池义务兑现=E18 林之恒 C-00013 standby 入池·续拆候选与 BS-007 稿集件随选优轮评估）**")

E18_ENTRY = ("- **E18 LC-017 林之恒拆条续投批 standby**（R734 补池入池·E17 出池注记兑现·三验字段：假设=拆条系列第十六续件候选+**第九对人物链候选=顾阿凤×林之恒摊头粢饭对**〔三源连接位：C-00010 年轮「与 C-00013 相遇：小林馆员照例来买粢饭」×C-00013 年轮「与 C-00010 相遇：顾阿姨在摊头问起新令牌」双卡互记+BigLife 互聊台账 2 条在案（R512·令牌号字面=verbatim 禁入面注记·拍稿选材排除）〕+**档案记忆主题=「城市不会忘记，除非我们偷懒。」手誊小史×git 全史活索引反差位**+同名混淆防核在案（归档者-07=C-00017 另卡·R294 口径）；消费面=视频号冗余扩容位+L-卡库存视频化通道；consumer_plan=全链 M0→F 本地执行零云端）：锚=C-00013（手写展示锚在位·非荣誉席）·源卡=CENSUS-v4 F-023 成品 PNG（R294 登记·E4 8.0 三意愿正面在案）——standby（E16 active 时待领·**激活时选优门**：档案馆区题材与 LC-002 归档者-07 同城区近域→拍稿须差异化角度位〔日常誊录防遗忘 vs 给失败立碑〕·runner-up 注记=沈佩兰 C-00012〔CENSUS-v3·卡号序最前但零连接位证据〕/陈雅雯 C-00015〔REACT-v6 信条收束在案·风控官主题=量化近域负担〕·BS-007 稿集件=顺位后置维持 R712 口径）")

RS_V28 = ("- v2.8 2026-09-30 R734：**冗余池扩容第十三件视频入池**（LC-016《城市图鉴 001·顾阿凤》拆条=F-071·成品库 70→71 件·L-卡衍生视频线第十六件=拆条系列节律第十五续件·**第八对人物链卡面双端互证件**〔C-00010「棋友=朱鸿奎」×C-00011「棋友=顾阿凤」双端在册〕+**章尾钩兑现位**〔SC-001-02 有声线 ch.2 章尾冲突钩「周三棋局」=拆条系列首个跨载体正典连接兑现〕+**跨载体复用最厚位**〔网文 SC-001-01 主角+有声 F-009 ch.1 主角+图鉴 CENSUS-v1 F-020+视频线=四载体·系列唯一〕·R730 补池选优入池〔四胜位 over 周浩宇〕→R731 起链〔S1 10/10 十五连满分〕→R732 定稿音轨〔两道裁链 57.638s 2.362s 余量〕→R733 渲染腿〔**b2/b3/b8 几何前置修=R720 律预执行第三件**·全卡几何审计 problems=NONE〕→R734 收官全链走门：ASR 终轨 32.1% 字位带内〔trad 78 表复用·零繁体输出=归一缺口面零·CTA 档案族第九发+受众定位词损如实〕+E4 8.0〔三意愿=会看完明说+点赞可能式+转发条件式·旗①=经历字段语境门槛族变体〕+七席 ≥9→M4）；§四 盘点行同步（视频号冗余弹药 12→13 件·M6 调仓/日更冗余预备·预产窗=开号前）。")

README_LINE = ("\n- [2026-09-30 08:0x R734 收官腿毕] ASR 终轨（R169 QC recipe·07:56:59 与 E4 双飞窗·12 cues 整轨一次过·asr-diff-r734.txt〔trad 78 表复用·零繁体输出=归一缺口面零〕=20 sites/67 diff/209 字≈**32.1% 字位带内**·关键存活 21/40〔顾阿凤/朱鸿奎净读+数字形差值存活 ×3〕+实质退化如实〔hook 双损+物种行第十三证+灶→早信条位族续+CTA 档案族第九发+受众定位词损复发〕·字幕轨=edge-tts 12/12 零损兜底）→S2 9.0+E4 同轮回填 8.0（三意愿=会看完明说+点赞可能式+转发条件式·旗①=经历字段「儿子在现实世界」语境门槛族变体·最弱=创新性=温情常见型体裁面·净本 expert-verdicts/20260930-075659-E4-audience+expert-calls 07:56 行）+E8 七席全 9.0（review-20260930-lc016-v1.md）→M4 完成态→**F-071 登记**（成品库第七十一件·L-卡衍生视频线第十六件=拆条系列节律第十五续件=第八对人物链双端互证件=章尾钩兑现位）+冗余池第十三件落位（release-schedule v2.8·视频号冗余弹药 13 件）+queue §E E17 出池+E18 林之恒 C-00013 standby 入池（lane=E16+E18 ≥2 达标）。")

def edit(path, fn):
    s = io.open(path, encoding="utf-8").read()
    s2 = fn(s)
    assert s2 is not None
    io.open(path, "w", encoding="utf-8", newline="\n").write(s2)
    return s2

def append_line(path, line):
    s = io.open(path, encoding="utf-8").read()
    if not s.endswith("\n"):
        s += "\n"
    s += line.rstrip("\n") + "\n"
    io.open(path, "w", encoding="utf-8", newline="\n").write(s)

# 1. finished.md F-071 row
append_line(p("output/finished.md"), F071_ROW)
# 2. renders README lc-016 row upgrade
REND_OLD = "**在链·渲染腿毕（R733）·收官腿=R734（E8 终审+ASR 终轨+E4+M4→F-071 登记→冗余池第十三件落位）·queue §E 批活池 E17 件·源卡=CENSUS-v1 F-020 顾阿凤（拆条系列=三载体已验后视频线第四载体·第八对人物链卡面双端互证·章尾钩兑现位）**"
REND_NEW = "**成品·落位件·冗余扩容位第十三件（F-071 登记 R734·queue §E 批活池 E17 件收官·源卡=CENSUS-v1 F-020 顾阿凤·R731 起链→R732 定稿音轨→R733 渲染腿→R734 收官全链走门毕：E8 七席 ≥9+ASR 终轨 32.1% 带内+E4 8.0+M4·第八对人物链卡面双端互证件=章尾钩兑现位=三载体已验后视频线第四载体）**"
def f_rend(s):
    assert s.count(REND_OLD) == 1, "renders anchor count=%d" % s.count(REND_OLD)
    return s.replace(REND_OLD, REND_NEW)
edit(p("output/renders/README.md"), f_rend)
# 3. station-reviews R734 row
append_line(p("docs/reviews/station-reviews.md"), SR_ROW)
# 4. release-schedule: inventory row + v2.8 row
RS_OLD = "）=视频号冗余弹药 12 件**=M6 调仓弹药"
RS_NEW = ("）+LC-016 拆条 F-071（R734·冗余池第十三件视频·顾阿凤《城市图鉴 001》·拆条系列节律第十五续件·**第八对人物链卡面双端互证件=章尾钩兑现位**〔C-00010×C-00011 棋友对双端+SC-001-02 ch.2 章尾钩〕+**跨载体复用最厚位**〔网文/有声/图鉴三载体已验→视频线第四载体〕·收官=E8 七席 ≥9+E4 8.0+ASR 终轨 32.1% 字位带内〔CTA 档案族第九发+受众定位词损如实〕）=视频号冗余弹药 13 件**=M6 调仓弹药")
def f_rs(s):
    assert s.count(RS_OLD) == 1, "rs anchor count=%d" % s.count(RS_OLD)
    s = s.replace(RS_OLD, RS_NEW)
    if not s.endswith("\n"):
        s += "\n"
    return s + RS_V28 + "\n"
edit(p("docs/release-schedule-v1.md"), f_rs)
# 5. queue: E17 done row + E18 standby entry before burn header
def f_q(s):
    anchor = "\n\n## burn 记录"
    assert s.count(anchor) == 1, "queue anchor count=%d" % s.count(anchor)
    return s.replace(anchor, "\n" + E17_DONE + "\n" + E18_ENTRY + "\n\n## burn 记录")
edit(p("docs/self-improvement-queue.md"), f_q)
# 6. lc016 README: gate-block close + R734 line
RM_OLD = "渲染腿/收官腿=后续轮领（R710/R725/R729 同型五步+全卡几何审计→E8+ASR+E4+M4→F-071 登记→冗余池第十三件落位→E17 出池）。发布锁=M5 账号物理件不变（未上线=未测量）。"
RM_NEW = "渲染腿毕（R733）+收官腿毕（R734·F-071 登记=冗余池第十三件落位 release-schedule v2.8·E17 出池+E18 林之恒 standby 入池）。发布锁=M5 账号物理件不变（未上线=未测量）。"
def f_rm(s):
    assert s.count(RM_OLD) == 1, "readme anchor count=%d" % s.count(RM_OLD)
    return s.replace(RM_OLD, RM_NEW)
edit(p("data/sources/lc016/README.md"), f_rm)
append_line(p("data/sources/lc016/README.md"), README_LINE.strip("\n"))

# 7. state.json
st = json.load(io.open(p("src/os/state.json"), encoding="utf-8"))
st["tick"] = 734
st["focus"] = FOCUS
st["log"].append(LOG)
st["ts"] = ts_now
st["task"] = LOG[:60]
io.open(p("src/os/state.json"), "w", encoding="utf-8", newline="\n").write(
    json.dumps(st, ensure_ascii=False, indent=1))

# 8. status-export.json
ex = json.load(io.open(p("docs/status-export.json"), encoding="utf-8"))
if "export_ts" in ex:
    ex["export_ts"] = ts_now
os_row = None
for row in ex.get("outs", []):
    if row and row[0] == "OS 循环":
        os_row = row
        break
assert os_row is not None
os_row[1] = ("tick 734，R734 生产轮·LC-016 顾阿凤拆条收官腿毕=F-071 登记+冗余池第十三件落位（queue §E 批活池 E17 件收官·实活轮·产品优先律对位=本轮实物增量=lc-016 成片 F-071 入成品库）：ASR 终轨 32.1% 字位带内（trad 78 表复用·零繁体输出=归一缺口面零·CTA 档案族第九发+受众定位词损如实·关键存活 21/40〔顾阿凤/朱鸿奎净读+数字形差值 ×3〕·字幕轨 edge-tts 12/12 零损兜底）→S2 9.0+E4 同轮回填 8.0（三意愿=会看完明说+点赞可能式+转发条件式·旗①=经历字段「儿子在现实世界」语境门槛族变体）+E8 七席 ≥9→M4 完成态→F-071 登记+冗余池 v2.8（视频号冗余弹药 13 件）→E17 出池+E18 林之恒 C-00013 standby 入池（lane=E16+E18 ≥2 达标）；下轮=R735 lane 选优起链（拆条第十六续件）/#70 OSS 窗 2/GB 10-01=#80 并窗")
res = ex.get("results", [])
prev_len = len(res)
res.insert(0, ["734", LOG])
while len(res) > prev_len:
    res.pop()
live = ex.get("live", [])
live[0][0] = "当前活：LC-016 顾阿凤拆条收官腿毕（R734·F-071 登记=成品库第七十一件·冗余池第十三件落位 release-schedule v2.8·E8 七席 ≥9+E4 8.0+ASR 终轨 32.1% 带内·E17 出池+E18 林之恒 standby 入池）"
live[1][0] = "最近实物：output/renders/lc-016-v1-shipinhao-60s.mp4（成品·拆条 016·源城市图鉴 001·57.638s）+docs/reviews/review-20260930-lc016-v1.md·" + ts_now
live[2][0] = "下个里程碑：E16/E18 lane 选优起链=拆条系列第十六续件（窗 ≤48h 即 2026-10-02 前）·#70 OSS 窗 2 切片 ≤10-02 21:40·global-benchmarks 7 日刷 10-01（#80 并窗）·C-20260928-02 义务窗=10-04 记忆 ≤10KB+10-05 C1 附款席6 司域保全确认"
io.open(p("docs/status-export.json"), "w", encoding="utf-8", newline="\n").write(
    json.dumps(ex, ensure_ascii=False, indent=1))

print("CLOSE_DONE ts=%s results_len=%d" % (ts_now, len(res)))
