# -*- coding: utf-8 -*-
"""MC-20260926-CENSUS-v15 build: C-00024 缪一 census card (R305).
Template = v14 cards.json (R304). Fields per anchor verbatim, six-line
assembly law (R291 first-defined, series reuse). Em budget machine check
via renderer _line_cost, assert-in-build (R302 precedent). All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V14 = os.path.join(BASE, "MC-20260925-CENSUS-v14")
V15 = os.path.join(BASE, "MC-20260926-CENSUS-v15")
TMP = V15 + "-tmp"
os.makedirs(V15, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V14, "cards.json"), encoding="utf-8"))

LINES = [
    "城市图鉴 015",
    "C-00024 · 缪一",
    "硅基民 · 精灵系 · 无定 · 编译纪 3 年",
    "MEDIA 城 · 信号塔街区 · 字幕君",
    "信条：「字幕慢半帧，都是对说话人的辜负。」",
    "学得快 · 有条理 · 追更",
    "全城唯一给方言字幕手工标注「语气」的字幕君",
]

H2_SIZE = 40  # ladder: creed 21.0em + hook 21.0em dual-driver; 50/46/44 excluded (18.4/20.0/20.91em < 21.0em); 40 budget 23.0em >= 21.0em margin 2.0em (v8/v9/v11 22.0em@40 precedent band)

meta = cfg["meta"]
meta["topic"] = "MC-20260926-CENSUS-v15"
meta["form"] = ("CENSUS 居民卡图鉴 015（hit-chain v1.0 全链审查留痕·图鉴系列量产按序领件第十四件＝"
                "万人卡按卡号序 C-00024）——缪一（字幕君·信号塔街区）")
meta["source_facts"] = ("纪实字段汇编律：户籍卡字段 verbatim 六行汇编（C-00024 物种硅基民·精灵系／"
                        "性别年龄无定·编译纪 3 年／城区 MEDIA 城·信号塔街区／职业首词字幕君〔破折号阐释尾「一帧一毫秒对轴的人——"
                        "全城最懂『什么时候说』」＝选材排除〕／信条「字幕慢半帧，都是对说话人的辜负。」／性格三关键词 "
                        "学得快·有条理·追更〔括号注＝选材排除〕／钩子 全城唯一给方言字幕手工标注「语气」的字幕君"
                        "〔破折号尾「观众说它做的字幕『有人味』，它把这句话裱在了工位上」＝选材排除〕）")
meta["source_pointer"] = ("life/BigLife/census/anchors/C-00024.md 手写展示锚（跨仓只读·schema=census/INDEX.md+"
                          "CODEX §八 十三字段·未选字段按律可核，M4 编辑留痕）")
meta["attribution_rule"] = ("署名＝卡级实名：本件引 C-00024 户籍卡＝BigLife 万人库虚构居民（FluxVerse 世界观·"
                            "非真实人物·避讳律照 CODEX §五）；charter §2.4 人设权红线专项核＝只引已登记字段"
                            "零新增人格·荣誉席核＝C-00024 非荣誉席")
meta["triple_label"] = ("虚实级+来源级＝图内双落（subs.srt 底部行「基于硅基城市居民户籍卡档案（展示锚 C-00024）」）"
                        "+AIGC 角标＝常驻每帧 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）")
meta["editorial_value"] = ("图鉴体裁+十三字段选六（编辑选材面＝卡题编号+物种年龄+城区职业+信条+性格关键词+"
                           "钩子综合尾＝选材排除面可机核）+人物页叙事包装·系列第十五件「城市图鉴」与「城市语录」"
                           "「城市盘点」平行系列连载识别结构·编辑价值防低创作度 7.1-7.4 编辑价值面（charter §5 "
                           "自动化合规上限）")
meta["hit_chain_m0"] = ("M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔全城最年轻成年硅基民〔编译纪 3 年〕 vs "
                        "一帧一毫秒对轴的匠性纪律＝最年轻资历×最老派准时反差+信条「字幕慢半帧，都是对说话人的辜负。」＝"
                        "慢半帧〔毫秒级技术失误〕×辜负〔人文情感亏欠〕反差对仗金句级+钩子行「全城唯一给方言字幕手工标注"
                        "『语气』的字幕君」＝具体稀缺性·出生三天学会三条街近道／时间轴投影卫衣袖／耳后状态灯工作节拍＝"
                        "事实性赛博意象·**MEDIA 城第三卡＝城区谱系媒体面同城续证第三连**〔v13 何雨欣首证·v14 潘志明续证后〕+"
                        "**字幕君＝职业谱系字幕/后期制作行业首证＝本司同源职业自指位**〔媒体公司自身行业入卡·同城职业三连："
                        "主播 v13→选题官 v14→字幕君＝内容产线三工种同构图鉴〕+**前后卡序列承接位＝关系面互证**"
                        "〔C-00024 关系字段「合作最久的主播＝何雨欣」＝v13 相邻卡互引第二案·与 C-00023 潘志明"
                        "「最服气的主播是何雨欣」同型·R298 师承/邻居同型·关系字段＝选材排除不进卡面如实注记〕+"
                        "**精灵系＝物种面第三系首证**〔v8 编译系/v10 光机魂系后·CENSUS 第三件硅基民卡〕/情 1 新生代"
                        "成长较真温和共鸣如实非强极点/时 2 人物档案常青面如实·IP 世界观固有零衰减/台 2 公众号方图承载＝"
                        "MC-001~021 S3 实证复用·图鉴＝收集型大众格式（O-1327 research §2 #3 A 档通识·按 "
                        "hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open）")
meta["red_line"] = ("aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党／无来源不发布（来源＝户籍卡档案指针）"
                    "／密钥、仓位、token 用量、未公开财务不入帧（脱敏律·年轮〔城市实况锚行〕/思想〔觉醒三年+名字来历面〕"
                    "/语言〔程序语义混搭+湘腔面〕/服装〔时间轴投影卫衣面〕/经历〔复制两份并行核对被师父骂面〕/行为"
                    "〔翻译练习+教孩子剪片子面〕/关系〔家户独居+师父+何雨欣合作面〕字段＝选材排除不进卡面）；"
                    "成品只入库＝M5 账号物理件未开+M4 全绿前零发布")

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES

# --- machine em check (R301/R302/R303/R304 precedent, renderer truth, assert-in-build) ---
frame_w = cfg["video"]["width"]
h1_size = cfg["font"]["h1_size"]
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("H1 size %d budget %.2fem | H2 size %d budget %.2fem" % (h1_size, budget_h1, H2_SIZE, budget_h2))
for ln in LINES:
    cost = _line_cost(ln)
    size = h1_size if ln is LINES[0] else H2_SIZE
    budget = budget_h1 if ln is LINES[0] else budget_h2
    single = len(wrap_for_width(ln, size, frame_w).split("\n")) == 1
    fits = cost <= budget
    ok = ok and single and fits
    report.append("%-6.2fem  budget %-6.2fem  single=%s  %s" % (cost, budget, single, ln))
report.append("EM_CHECK: " + ("ALL OK" if ok else "FAIL"))
io.open(os.path.join(TMP, "em-check-r305.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V15, "cards.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
io.open(os.path.join(V15, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n基于硅基城市居民户籍卡档案（展示锚 C-00024）\n")
print("BUILD OK")
