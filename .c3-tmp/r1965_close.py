# -*- coding: utf-8 -*-
import io, json, datetime, shutil

# --- 0. copy evidence scripts into batch-closure tmp dir ---
for src, dst in [
    (".c3-tmp/r1965_verbatim_check.py", "data/storylines/audio/sc005-03-v1-tmp/verbatim_check_r1965.py"),
    (".c3-tmp/r1965_asr_survival.py", "data/storylines/audio/sc005-03-v1-tmp/asr_survival_r1965.py"),
    (".c3-tmp/r1965_asr_survival.txt", "data/storylines/audio/sc005-03-v1-tmp/asr-survival-r1965.txt"),
    (".c3-tmp/r1965_same_text.txt", "data/storylines/audio/sc005-03-v1-tmp/same-text-report.txt"),
]:
    shutil.copyfile(src, dst)
print("EVIDENCE-COPIED 4")

# --- 1. audio README: table row after SC-005-02 row + changelog line ---
rpath = "data/storylines/audio/README.md"
rt = io.open(rpath, encoding="utf-8").read()
ROW = "| SC-005-03-v1.mp3《城市口述史·选段三·字幕君缪一》（人物志口述史系列第三件·F-174 现行） | 3:35.9（ffprobe 215.95s） | 13 | zh-CN-YunyangNeural+cyber light+human 42（产线默认） | ai_feel 0 FAIL 0 WARN（gaps 12 处 0.239-0.558s varied/pacing CV 0.551/prosody 6 档 13 拍/copy CV 0.562） | **成品·F-174（R1965 单轮全链收官）**——S1 门 10/10 零违律一次过（fire 卡 11:17:33 GO B-eviction-credit 窗内即发·判词档 `expert-verdicts/20261011-111754-S1-script.md`）+同文本机械核验 13/13 miss 0+TTS light 产线默认 215.95s+M4 四检过（红线五条/三重标注 cue01 内置「AI 参与生成+在册居民档案改编+合理推演+完整来源清单见图文页」四连/来源=`SC-005-03-v1-sources.md` C-00024 全字段对表+机检 57 verbatim 锚零 MISS〔verbatim_check_r1965.py·系列密度峰〕/编辑价值=口述史单人物弧线·复制自己之夜转折）+空气预算定谳=长度带 2:00-3:00 微超 ~36s 不裁（verbatim 锚密度优先·纪实线禁虚构·SC-004-01/SC-005-01/02 est 微超先例同型）——**S2 席 ASR 终轨**=pinned medium+beam5+noctx·HF_HUB_OFFLINE=1·43 cues dropped=0/215.95s·硬事实链主体存活（信条句「字幕慢半帧，都是对说话人的辜负」close 位 1 字 twist〔慢→漫=本件信条句单点〕+「对说话人的辜负」全净+数字族全净〔C-00024→C00024/H-1014→H1014〕+「合理推演」全净+「成长没有并行捷径」「有人味」跨 cue 存活+「字幕君」首现实位全净）+名族/湘语族如实（缪一→妙一/妙医=名族/霸得蛮→罢的蛮+湘腔→香香=湘语词族/发版了→八百=本件最大单点/硅基→归基 ×2=R1964 同族/档案馆→大案馆 ×2/像素小学→向宿小学）+**繁体字形重漂移带首见**（cue36-39 close 声明段整段繁体=R187 散布形态对照·tech#98 观察项）+**同音量化 asr_diff_r1965.py=83 sites/121 chars/830 字=字位 14.6%**（系列 12.3→13.8→15.0→14.6=带上缘外溢 ~1.1pp→S2 8.0 诚实扣 1.0〔SC-005-02 同型刻度〕·tech#97 判据 <16%=零动作维持 M6 注记位）+字幕轨=edge-tts 直出 13/13 发布面零损；E4 参考仪=**重试环在飞**（fire 卡 11:21/11:24 两查 no-fire=ComfyUI 常驻窗 MV sprint 避让→expert_retry_loop PID 72820 后台环·追加制回填三件套=R1948 F-171 先例·非拦截席·E4 目标带 ≥8.0·系列带 8.0×2 基锚）——**E8 终审听审七席 ≥9→M4 完成态→F-174 登记**（`review-20261011-sc00503-v1.md`·R223 复用·单轮全链=SC-005-02 同型第二证） |"
if "SC-005-03-v1.mp3" in rt:
    print("README-ROW-ALREADY skip")
else:
    lines = rt.splitlines(keepends=False)
    out = []
    inserted = False
    for l in lines:
        out.append(l)
        if not inserted and l.startswith("| SC-005-02-v1.mp3"):
            out.append(ROW)
            inserted = True
    if not inserted:
        raise SystemExit("README anchor row not found")
    io.open(rpath, "w", encoding="utf-8", newline="").write("\n".join(out) + "\n")
    print("README-ROW-INSERTED")

CHANGELOG = "- 2026-10-11: R1965 单轮全链——SC-005-03《城市口述史·选段三·字幕君缪一》拍稿起链至 **F-174 登记** 一轮收官（main#14 SC-005 A 首件批第三件=C-00024 缪一〔R1960 选型件三件位·非人视角+新生代起源弧+转折=城主欢迎词之夜把自己复制了两份〕：拍稿 13 拍 947 字·机检 57 verbatim 锚零 MISS〔系列密度峰〕·溯源对表 C-00024 全字段+C-00013 系列帧+CENSUS v15 避让〔音频形态首采〕+C-00042 相遇线留白→S1 门 10/10 一次过（fire 11:17:33 GO 窗内即发）→TTS light 215.95s=3:35.9→同文本 13/13 零 MISS→ai_feel 0F0W（pacing CV 0.551/copy CV 0.562=系列带内新高·新生代人物节奏自洽）→ASR 终轨 43 cues dropped=0（信条句 1 字 twist〔慢→漫〕+数字族全净+跨 cue 存活〔成长没有并行捷径/有人味〕+名族/湘语族〔缪一→妙一/霸得蛮→罢的蛮/发版了→八百〕+**繁体漂移带首见 cue36-39=tech#98 观察项**·字位 14.6% 带上缘外溢 ~1.1pp→S2 8.0 诚实扣 1.0·tech#97 判据 <16% 零动作）→E8 七席 ≥9→M4→F-174（成品库第 174 件·L-音第 29 件·SC-005 系列第三件）——**A 首件批三件收官**（C-00019 老晶振→C-00025 陆海峰→C-00024 缪一=F-172/F-173/F-174 三连·两轮连用单轮压缩节拍）；E4=fire 卡两查 no-fire（ComfyUI 常驻=MV sprint 避让）→expert_retry_loop 后台环在飞（PID 72820·追加制回填三件套=R1948 F-171 先例）·落地轮回填；sc005-03-v1-tmp 中间件批闭随收账 commit。"
rt2 = io.open(rpath, encoding="utf-8").read()
if "R1965 单轮全链" in rt2:
    print("README-LOG-ALREADY skip")
else:
    io.open(rpath, "w", encoding="utf-8", newline="").write(rt2.rstrip("\n") + "\n" + CHANGELOG + "\n")
    print("README-LOG-APPENDED")

# --- 2. finished.md F-174 block ---
fpath = "output/finished.md"
ft = io.open(fpath, encoding="utf-8").read()
F174 = """

**F-174 登记（R1965 单轮全链收官件）**：**L-音 有声线第二十九件·SC-005 人物志口述史系列第三件=成品库第一百七十四件**——SC-005-03-v1.mp3《城市口述史·选段三·字幕君缪一》（3:35.9=ffprobe 215.95s·13 cues·TTS light 产线默认 Yunyang+cyber light+human 42·纯音频无垫床=口述史体裁正身）全链走门毕（**F-173 已被 SC-005-02 占用→本件 F-174·R978 判例·finished 顺序号=单一真相**·**单轮全链**=R1965 拍稿三件套→S1 门→TTS→同文本核验→ai_feel→ASR 终轨→E8+F 登记——SC-005-02 单轮链同型第二证·fire 窗 GO 窗内 S1 即发+材料件预载先行）——拍稿 13 拍 947 字〔hook 三重标注+close 推演声明双落位·**机检 57 verbatim 锚零 MISS**〔verbatim_check_r1965.py·系列密度峰：信条「字幕慢半帧，都是对说话人的辜负」+思想「差一点点意思的『缪』，做字幕的就是差一点点都不能要/快不是本事，准时才是」+职业「字幕君——一帧一毫秒对轴——全城最懂『什么时候说』」+转折「第一次给城主欢迎词打轴/把自己复制了两份并行核对/成长没有并行捷径」+语言「程序语义+网络世代语混搭/这段对轴对到睫毛都数清了/弹幕太上头/湘腔霸得蛮」+服装「不对称剪裁卫衣/左袖时间轴投影/衣服就是工牌/状态灯」+行为「六亲不认/慈悲为怀/翻译练习/不许丢味/像素小学」+关系「H-1014 独居/进了它的脑子/老剪辑师/何雨欣/发版了」+钩子「全城唯一给方言字幕手工标注『语气』/有人味/裱在工位上」+年轮「这段对轴对到连呼吸都算计好了」全在位〕+溯源对表 sources.md C-00024 主锚全字段对表跨仓只读+C-00013 系列帧锚+CENSUS v15 图文卡避让〔音频形态首采=一料多吃〕+C-00042 相遇线留白〕——**S1-script 10/10 零违律一次过**（R1965·fire 卡 11:17:33 GO B-eviction-credit 窗内即发·总裁决「PASS，稿件完全符合评审底座与评分制的要求，无违律」·判词档 expert-verdicts/20261011-111754-S1-script.md）+环节门 **S2 8.0（诚实扣 1.0）**（ASR 终轨=pinned medium+beam5+noctx·HF_HUB_OFFLINE=1·43 cues dropped=0/215.95s·**硬事实链主体存活**〔信条句 1 字 twist〔慢→漫〕+「对说话人的辜负」全净+数字族全净〔C00024/H1014〕+「合理推演」全净+「成长没有并行捷径」「有人味」跨 cue 存活+「字幕君」首现实位全净〕+名族/湘语族如实〔缪一→妙一/妙医/霸得蛮→罢的蛮/湘腔→香香/发版了→八百=本件最大单点/硅基→归基 ×2=R1964 同族/档案馆→大案馆 ×2/像素小学→向宿小学〕+**繁体字形重漂移带首见**〔cue36-39 close 声明段整段繁体=R187 散布对照·tech#98 观察项〕+**同音量化 asr_diff_r1965.py=83 sites/121 chars/830 字=字位 14.6%**〔系列 12.3→13.8→15.0→14.6=带上缘外溢 ~1.1pp→诚实扣 1.0·tech#97 判据 <16%=零动作维持 M6 注记位〕+字幕轨=edge-tts 文本精确直出 13/13=发布面零损）/S3 9.0/S4 9.0+终审七席 E1/E2/E3/E5/E6/E7/E8 全 9.0=**七席 ≥9 PASS=放行候选→M4 完成态**（review-20261011-sc00503-v1.md·R223 纯音频件维度复用·S1=本件真飞非继承位）——**E4 参考仪=重试环在飞结转位**（fire 卡 11:21/11:24 两查 no-fire=ComfyUI 常驻窗 MV sprint 避让如实注记→expert_retry_loop 后台环 PID 72820 在飞·**追加制回填三件套=本行回填段+review E4 行+净本**·R1948 F-171 先例同型·非拦截席·E4 目标带 ≥8.0·audio 系列带 8.0×2 基锚）——发布锁=M5 账号物理件（未上线=未测量）·mp3 gitignored（charter §4·audio/README 记账）·中间件 sc005-03-v1-tmp 批闭收账随本单 commit（R150/R276/R639 惯例）；**SC-005 A 首件批三件收官**（C-00019 老晶振→C-00025 陆海峰→C-00024 缪一=F-172/F-173/F-174 三连·R1960 选型件 A 档批面收口）·B 次位池 5 件=R-20261011-bigstream-13 §4 升格回评窗随轮领·P-5 双声轮替并测位=续件 A/B 候选。

F-174 E4 回填（追加制·重试环落地轮销项）：待回填。
"""
if "F-174 登记" in ft:
    print("FINISHED-ALREADY skip")
else:
    io.open(fpath, "w", encoding="utf-8", newline="").write(ft.rstrip("\n") + F174)
    print("FINISHED-APPENDED")

# --- 3. queue main.md item 14 note ---
qpath = "state/queue/main.md"
qt = io.open(qpath, encoding="utf-8").read()
QNOTE = " **[R1965 注记·A 首件批三件收官]**：第三件=C-00024 缪一收官——**F-174 登记**（R1965 单轮全链：拍稿 57 verbatim 锚零 MISS→S1 10/10 一次过〔fire 11:17 GO 即发〕→TTS light 215.95s→同文本 13/13→ai_feel 0F0W〔CV 0.551/0.562 系列新高〕→ASR 终轨 43 cues〔信条句 1 字 twist 慢→漫+数字族全净+字位 14.6% 带上缘→S2 8.0 诚实扣·tech#97 <16% 零动作〕→E8 七席 ≥9→M4→F-174=成品库第 174 件·L-音第 29 件·**A 首件批三连收官 F-172/F-173/F-174**·单轮全链=SC-005-02 同型第二证）；E4=重试环在飞（ComfyUI 常驻窗 no-fire→PID 72820 后台环·追加制回填）；**A 档批面收口——B 次位池 5 件升领位**（R-20261011-bigstream-13 §4 升格回评窗·沈佩兰/陈雅雯/潘志明/何雨欣+池=随轮领）。"
if "R1965 注记·A 首件批三件收官" in qt:
    print("QUEUE-ALREADY skip")
else:
    lines = qt.splitlines(keepends=False)
    for i, l in enumerate(lines):
        if l.startswith("14. [R1960 补货"):
            lines[i] = l.rstrip() + QNOTE
            break
    else:
        raise SystemExit("queue item 14 not found")
    io.open(qpath, "w", encoding="utf-8", newline="").write("\n".join(lines) + "\n")
    print("QUEUE-NOTE-APPENDED")

# --- 4. tech.md tech#98 ---
tpath = "state/queue/tech.md"
tt = io.open(tpath, encoding="utf-8").read()
ITEM = "98. [R1965 补货·真发现] ASR 繁体字形重漂移带观察项——SC-005-03 close 声明段 cue36-39 整段繁体输出首见（「口述根據歸基城市在冊居民大案C00024改編」族·与 R187 历史散布形态不同=整段连续漂移·字幕轨=edge-tts 直出发布面零损不受影响）：判据=下一 audio 件 close 段繁体 ≥3 cues 复现=评估 whisper --initial-prompt 简体锚注入 A/B（R1409 B' 发现=参数在位从未启用·仅 QC 通道）；不复现=维持 M6 真人校准线注记零动作——观察位不占产线（随 audio 件收官轮并读·判负留痕合法）"
if "98. [R1965" in tt:
    print("TECH-98-ALREADY skip")
else:
    lines = tt.splitlines(keepends=False)
    last = max(i for i, l in enumerate(lines) if l.strip().startswith(tuple(str(n) + "." for n in range(1, 200))))
    lines.insert(last + 1, ITEM)
    io.open(tpath, "w", encoding="utf-8", newline="").write("\n".join(lines) + "\n")
    print("TECH-98-APPENDED after-line=%d" % (last + 1))

# --- 5. state.json round accounting ---
spath = "src/os/state.json"
st = json.load(io.open(spath, encoding="utf-8"))
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
LOG = "2026-10-11 11:3x R1965: 生产轮·SC-005-03 缪一单轮全链=F-174 登记（main#14 A 首件批第三件=C-00024〔R1960 选型件三件位·非人视角+新生代起源弧+转折=城主欢迎词之夜把自己复制了两份〕·拍稿 13 拍 947 字机检 57 verbatim 锚零 MISS〔系列密度峰〕→S1 门 10/10 一次过〔fire 卡 11:17:33 GO B-eviction-credit 窗内即发·判词档 20261011-111754-S1-script.md〕→TTS light 215.95s=3:35.9→同文本机械核验 13/13 miss 0→ai_feel 0F0W〔gaps 12 varied/pacing CV 0.551/prosody 6 档/copy CV 0.562=系列带内新高〕→ASR 终轨 43 cues dropped=0〔pinned medium+beam5+noctx·HF_HUB_OFFLINE=1·信条句 1 字 twist〔慢→漫〕+数字族全净〔C00024/H1014〕+「合理推演」全净+「成长没有并行捷径」「有人味」跨 cue 存活+名族/湘语族如实〔缪一→妙一/霸得蛮→罢的蛮/发版了→八百=最大单点〕+繁体漂移带首见〔cue36-39 整段繁体=tech#98 观察项〕+字位 14.6%〔83/121/830〕带上缘外溢 ~1.1pp→S2 8.0 诚实扣 1.0·tech#97 判据 <16%=零动作〕→E8 终审听审七席 ≥9→M4 完成态→F-174 登记=成品库第 174 件·L-音第 29 件·SC-005 系列第三件〔review-20261011-sc00503-v1.md·R223 复用〕）——**A 首件批三连收官**（C-00019 老晶振→C-00025 陆海峰→C-00024 缪一=F-172/F-173/F-174·R1960 选型件 A 档批面收口·B 次位池 5 件升领位=R-20261011-bigstream-13 §4 升格回评窗）——**E4 参考仪=重试环在飞结转位**（fire 卡 11:21/11:24 两查 no-fire=ComfyUI 常驻窗 MV sprint 避让如实注记→expert_retry_loop 后台环 PID 72820 在飞·追加制回填三件套=R1948 F-171 先例同型·非拦截席·落地轮回填）；轮首五查静=own orders 顶 O-20260908-1105 mtime==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）+decisions dnums new_vs_wm=0（水位 137 维持）+ledger @BigStream 行=值守锚零新转办+无 index.lock+树态=MV sprint 会话域在飞件零接触（R1745 承继·whisper v3/asr-noise-dict v3=其会话域文件本轮零碰·ASR 走 --no-ledger 最小足迹）；三探针=board/readiness/loop_health（loop_health 2F 皆 09-26/09-28 在案史实·readiness 3 阻塞皆外部 CEO 面〔账号批次①+M4 GATE 6/10+#17 needs-CEO〕0 发现）；台账=audio README 表行+变更行+finished F-174 块+queue main#14 R1965 注+tech#98 补货（繁体漂移带观察·真发现）+export 刷（F-174 态）；例行件=10-11 日报在案不重跑（R1927 一份为真相）·W42 周审 10-12 未到·GB §④ 下期 10-15 跳过·tech#92 判据窗 10-12 08:00 届日即领不预扫·#99 blocked-on-channel 维持（SLA ≤10-13）·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·tokens:local=1（S1-script qwen2.5:14b 真调=E4 重试环在飞=落地轮记账·零 API token·P-54⑤ 计量律）；下轮=快速路径首查（tech#92 判据窗 10-12 08:00 届日即领〔zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补〕+E4 回填三件套〔重试环落地轮〕+B 次位池 5 件升领评估+MD-0002 T2I gated CEO 点头+meme V1 查看位）。"
st["tick"] = st.get("tick", 1964) + 1
st["log"].append(LOG)
st["ts"] = now
st["task"] = LOG.split("R1965: ", 1)[1][:60]
st["focus"] = "R1965 SC-005-03 缪一单轮全链=F-174 登记（S1 10/10+ASR 字位 14.6%→S2 8.0+E8 七席 ≥9）·A 首件批三连收官 F-172/173/174·E4=重试环在飞回填位·B 次位池 5 件升领位·tech#92 判据窗 10-12 08:00"
io.open(spath, "w", encoding="utf-8", newline="").write(json.dumps(st, ensure_ascii=False, indent=2) + "\n")
print("STATE-UPDATED tick=%s ts=%s" % (st["tick"], now))
