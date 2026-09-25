# -*- coding: utf-8 -*-
"""MC-20260925-CENSUS-v14 build: C-00023 潘志明 census card (R304).
Template = v13 cards.json (R303). Fields per anchor verbatim, six-line
assembly law (R291 first-defined, series reuse). Em budget machine check
via renderer _line_cost, assert-in-build (R302 precedent). All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V13 = os.path.join(BASE, "MC-20260925-CENSUS-v13")
V14 = os.path.join(BASE, "MC-20260925-CENSUS-v14")
TMP = V14 + "-tmp"
os.makedirs(V14, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V13, "cards.json"), encoding="utf-8"))

LINES = [
    "城市图鉴 014",
    "C-00023 · 潘志明",
    "碳基市民 · 原生代 · 男 · 47 岁",
    "MEDIA 城 · 选题馆街区 · 选题官",
    "信条：「毙稿不毙人，选题选良心。」",
    "记性好 · 端水 · 较真",
    "全城唯一保留「毙稿理由档案」的选题官",
]

H2_SIZE = 50  # ladder: hook 18 fullwidth = 18.0em; 50 budget 18.4em >= 18.0em margin 0.4em (positive margin -> admitted; zero-margin rule R293/R313 not triggered; v6 25.0em@36 margin 0.6em precedent band; 19.0em+ would exclude 50)

meta = cfg["meta"]
meta["topic"] = "MC-20260925-CENSUS-v14"
meta["form"] = ("CENSUS 居民卡图鉴 014（hit-chain v1.0 全链审查留痕·图鉴系列量产按序领件第十三件＝"
                "万人卡按卡号序 C-00023）——潘志明（选题官·选题馆街区）")
meta["source_facts"] = ("纪实字段汇编律：户籍卡字段 verbatim 六行汇编（C-00023 物种碳基市民·原生代／"
                        "性别年龄男·47 岁／城区 MEDIA 城·选题馆街区／职业首词选题官〔破折号阐释尾「选题馆的守门人——"
                        "留言墙的真实来信都汇到他案头」＝选材排除〕／信条「毙稿不毙人，选题选良心。」／性格三关键词 "
                        "记性好·端水·较真〔括号注＝选材排除〕／钩子 全城唯一保留「毙稿理由档案」的选题官"
                        "〔破折号尾「二十年每条毙稿一行理由，年轻人都说那是选题馆的『镇馆之宝』」＝选材排除〕）")
meta["source_pointer"] = ("life/BigLife/census/anchors/C-00023.md 手写展示锚（跨仓只读·schema=census/INDEX.md+"
                          "CODEX §八 十三字段·未选字段按律可核，M4 编辑留痕）")
meta["attribution_rule"] = ("署名＝卡级实名：本件引 C-00023 户籍卡＝BigLife 万人库虚构居民（FluxVerse 世界观·"
                            "非真实人物·避讳律照 CODEX §五）；charter §2.4 人设权红线专项核＝只引已登记字段"
                            "零新增人格·荣誉席核＝C-00023 非荣誉席")
meta["triple_label"] = ("虚实级+来源级＝图内双落（subs.srt 底部行「基于硅基城市居民户籍卡档案（展示锚 C-00023）」）"
                        "+AIGC 角标＝常驻每帧 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）")
meta["editorial_value"] = ("图鉴体裁+十三字段选六（编辑选材面＝卡题编号+物种年龄+城区职业+信条+性格关键词+"
                           "钩子综合尾＝选材排除面可机核）+人物页叙事包装·系列第十四件「城市图鉴」与「城市语录」"
                           "「城市盘点」平行系列连载识别结构·编辑价值防低创作度 7.1-7.4 编辑价值面（charter §5 "
                           "自动化合规上限）")
meta["hit_chain_m0"] = ("M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔47 岁选题馆守门人 vs 信条「毙稿不毙人，"
                        "选题选良心。」＝毙稿〔最否定行为〕×不毙人〔最人文温度〕反差对仗金句级+钩子行「全城唯一保留"
                        "『毙稿理由档案』的选题官」＝具体稀缺性·每天毙稿三十留下三个／留言墙亲手拆信／深夜地标灯＝"
                        "事实性赛博意象·**MEDIA 城第二卡＝城区谱系媒体面同城续证**〔v13 何雨欣首证后同城承接〕+"
                        "**选题官＝职业谱系内容选题行业首证＝本司同源职业自指位**〔媒体公司自身行业入卡〕+"
                        "**前后卡序列承接位＝关系面互证**〔C-00023 关系字段「最服气的主播是何雨欣」＝v13 相邻卡互引·"
                        "R298 师承朱鸿奎／邻居徐根福同型·关系字段＝选材排除不进卡面如实注记〕/情 1 守门人较真与笔不认"
                        "人情温和共鸣如实非强极点/时 2 人物档案常青面如实·IP 世界观固有零衰减/台 2 公众号方图承载＝"
                        "MC-001~020 S3 实证复用·图鉴＝收集型大众格式（O-1327 research §2 #3 A 档通识·按 "
                        "hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open）")
meta["red_line"] = ("aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党／无来源不发布（来源＝户籍卡档案指针）"
                    "／密钥、仓位、token 用量、未公开财务不入帧（脱敏律·年轮〔城市实况锚行〕/思想〔心电图室+追稿三个月"
                    "面〕/语言〔改稿术语+口头禅+红笔面〕/服装〔三色笔马甲+黑白小屏面〕/经历〔人情稿撤稿转折面〕/行为"
                    "〔毙稿三十留三+留言墙值班+地标灯面〕/关系〔家户三代同堂+何雨欣互证面〕字段＝选材排除不进卡面）；"
                    "成品只入库＝M5 账号物理件未开+M4 全绿前零发布")

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES

# --- machine em check (R301/R302/R303 precedent, renderer truth, assert-in-build) ---
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
io.open(os.path.join(TMP, "em-check-r304.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V14, "cards.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
io.open(os.path.join(V14, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n基于硅基城市居民户籍卡档案（展示锚 C-00023）\n")
print("BUILD OK")
