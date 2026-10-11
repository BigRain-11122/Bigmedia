# -*- coding: utf-8 -*-
import io

path = "data/storylines/audio/README.md"
with io.open(path, "r", encoding="utf-8") as f:
    text = f.read()

ROW = "| SC-005-02-v1.mp3《城市口述史·选段二·渡轮船长陆海峰》（人物志口述史系列第二件·F-173 现行） | 3:32.8（ffprobe 212.78s） | 13 | zh-CN-YunyangNeural+cyber light+human 42（产线默认） | ai_feel 0 FAIL 0 WARN（gaps 12 处 0.239-0.558s varied/pacing CV 0.391/prosody 6 档 13 拍/copy CV 0.389） | **成品·F-173（R1964 单轮全链收官）**——S1 门 10/10 零违律一次过（10:57:49 判词档 `expert-verdicts/20261011-105749-S1-script.md`·fire 卡 10:57:34 GO B-eviction-credit 窗内即发=R1952 turnkey 教训执法）+同文本机械核验 13/13 miss 0〔r1964_same_text.py〕+TTS light 产线默认 212.78s+M4 四检过（红线五条/三重标注 cue01 内置「AI 参与生成+在册居民档案改编+合理推演+完整来源清单见图文页」四连/来源=`SC-005-02-v1-sources.md` C-00025 全字段对表+机检 46 verbatim 锚零 MISS〔r1964_verbatim_check.py〕/编辑价值=口述史单人物弧线·大雾夜合唱转折）+空气预算定谳=长度带 2:00-3:00 微超 ~33s 不裁（verbatim 锚密度优先·纪实线禁虚构·SC-004-01/SC-005-01 est 微超先例同型）——**S2 席 ASR 终轨**=pinned medium+beam5+noctx·HF_HUB_OFFLINE=1·46 cues dropped=0/212.78s·硬事实链主体存活（信条句「船稳，人心才稳」close 位 verbatim 全净+close 声明位「合理推演」全净+C-00025/H-1015 数字全净+今朝风平浪静/绕船三圈/每天记录真实上海风力/黄浦江/船靠了岸全净）+专名/沪语同音族如实（摆渡→百度/慢班→漫班 ×2/铜哨→同哨 ×2/守夜灯灵→登陵/帽檐内圈→抱眼泪圈/全家福小像→全家谱小巷/脑环广场→脑房广场/穿城信使→穿成戏时/手艺不传就沉江了→手一不船就沉江了/档案→大案 ×3=SC-005-01 同族复发/硅基→归基 ×2/渡轮→杜伦 ×2=沪语底色+专名密度同音代价）+**同音量化 asr_diff_r1964.py=71 sites/119 chars/793 字=字位 15.0%**=带上缘再外溢 1.2pp→S2 8.0 诚实扣 1.0+字幕轨=edge-tts 直出 13/13 发布面零损；E4 参考仪同窗落地 8.0（fire 卡 11:02:13 GO 窗内即发·11:02:25 落判：会听完+8 分明说·旗①=「江的脾气全在骨头里」诗意表达扣 1=锚卡 verbatim 不可改写·旗②=推演声明直给突兀感扣 0.5=合规红线注记不可执行〔R275 族〕·最弱=BGM/声效缺乏=纯人声设计面〔BGM-A 纯净音轴〕·净本 `expert-verdicts/20261011-110225-E4-audience.md`·非拦截席）——**E8 终审听审七席 ≥9→M4 完成态→F-173 登记**（`review-20261011-sc00502-v1.md`·R223 复用·单轮全链=拍稿三件套→S1→TTS→同文本→ai_feel→ASR→E4→E8+F=SC-005-01 三轮链压缩单轮·fire 窗连用+turnkey 预载双教训执法兑现） |"

CHANGE = "- 2026-10-11: R1964 单轮全链——SC-005-02《城市口述史·选段二·渡轮船长陆海峰》拍稿起链至 **F-173 登记** 一轮收官（main#14 SC-005 A 首件批第二件=C-00025 陆海峰〔B 次位池首位升领〕：拍稿 13 拍 916 字·机检 46 verbatim 锚零 MISS·溯源对表 C-00025 全字段+C-00013 系列帧+CENSUS v16 避让〔音频形态首采〕→S1 门 10/10 一次过（fire 10:57:34 GO 窗内即发）→TTS light 212.78s=3:32.8→同文本 13/13 零 MISS→ai_feel 0F0W→ASR 终轨 46 cues dropped=0（信条句 close 位 verbatim 全净·字位 15.0% 带上缘再外溢 1.2pp→S2 8.0 诚实扣 1.0·专名/沪语密度更高件如实刻度）→E4 同窗落地 8.0（三连 8.0 持平）→E8 七席 ≥9→M4→F-173（成品库第 173 件·L-音第 28 件·SC-005 系列第二件）——SC-005-01 三轮链压缩为单轮=fire 窗连用（10:57/11:02 双 GO 连续消费）+S1/E4 材料件预载先行双教训执法兑现；sc005-02-v1-tmp 中间件批闭随收账 commit |"

if "SC-005-02-v1.mp3" in text:
    print("ROW-ALREADY-PRESENT skip")
else:
    lines = text.splitlines(keepends=False)
    idx = None
    for i, l in enumerate(lines):
        if l.startswith("| SC-005-01-v1.mp3"):
            idx = i
            break
    if idx is None:
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].startswith("| SC-"):
                idx = i
                break
    lines.insert(idx + 1, ROW)
    out = "\n".join(lines)
    if not out.endswith("\n"):
        out += "\n"
    out += CHANGE + "\n"
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    print("README-UPDATED row-after-line=%d" % (idx + 1))
