# -*- coding: utf-8 -*-
"""MC-20260925-CENSUS-v12 build: C-00021 王多多 census card (R302).
Template = v11 cards.json (R301). Fields per anchor verbatim, six-line
assembly law (R291 first-defined, series reuse). Em budget machine check
via renderer _line_cost (R301 precedent). All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V11 = os.path.join(BASE, "MC-20260925-CENSUS-v11")
V12 = os.path.join(BASE, "MC-20260925-CENSUS-v12")
TMP = V12 + "-tmp"
os.makedirs(V12, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V11, "cards.json"), encoding="utf-8"))

LINES = [
    "城市图鉴 012",
    "C-00021 · 王多多",
    "碳基市民 · 原生代 · 男 · 11 岁",
    "GAME 城 · X026 城门区 · 像素小学学生",
    "信条：「放学别走，先把今天的谜想完。」",
    "好奇 · 学得快 · 嘴甜",
    "全城唯一能口哨唤来三只以上消息雀的孩子",
]

H2_SIZE = 46  # ladder: 50 budget 18.4em < max 19.0em -> excluded; 46 budget 20.0em >= 19.0em (R293 v3 precedent, same 19.0em driver)

meta = cfg["meta"]
meta["topic"] = "MC-20260925-CENSUS-v12"
meta["form"] = ("CENSUS 居民卡图鉴 012（hit-chain v1.0 全链审查留痕·图鉴系列量产按序领件第十一件＝"
                "万人卡按卡号序 C-00021）——王多多（像素小学学生·信使小跟班）")
meta["source_facts"] = ("纪实字段汇编律：户籍卡字段 verbatim 六行汇编（C-00021 物种碳基市民·原生代／"
                        "性别年龄男·11 岁／城区 GAME 城·X026 城门区／职业首词像素小学学生〔括号注信使小跟班＝"
                        "选材排除·随性格关键词括号注律〕／信条「放学别走，先把今天的谜想完。」／性格三关键词 "
                        "好奇·学得快·嘴甜〔括号注＝选材排除〕／钩子 全城唯一能口哨唤来三只以上消息雀的孩子"
                        "〔破折号尾＝选材排除〕）")
meta["source_pointer"] = ("life/BigLife/census/anchors/C-00021.md 手写展示锚（跨仓只读·schema=census/INDEX.md+"
                          "CODEX §八 十三字段·未选字段按律可核，M4 编辑留痕）")
meta["attribution_rule"] = ("署名＝卡级实名：本件引 C-00021 户籍卡＝BigLife 万人库虚构居民（FluxVerse 世界观·"
                            "非真实人物·避讳律照 CODEX §五）；charter §2.4 人设权红线专项核＝只引已登记字段"
                            "零新增人格·荣誉席核＝C-00021 非荣誉席")
meta["triple_label"] = ("虚实级+来源级＝图内双落（subs.srt 底部行「基于硅基城市居民户籍卡档案（展示锚 C-00021）」）"
                        "+AIGC 角标＝常驻每帧 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）")
meta["editorial_value"] = ("图鉴体裁+十三字段选六（编辑选材面＝卡题编号+物种年龄+城区职业+信条+性格关键词+"
                           "钩子综合尾＝选材排除面可机核）+人物页叙事包装·系列第十二件「城市图鉴」与「城市语录」"
                           "「城市盘点」平行系列连载识别结构·编辑价值防低创作度 7.1-7.4 编辑价值面（charter §5 "
                           "自动化合规上限）")
meta["hit_chain_m0"] = ("M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔11 岁像素小学学生 vs 全城唯一口哨唤来三只以上"
                        "消息雀＝最小年纪×最独特技能反差+信条「放学别走，先把今天的谜想完」＝学业纪律〔别走〕×"
                        "孩童好奇〔把谜想完〕反差对仗金句级+钩子行「全城唯一」＝具体稀缺性·commit 光点过江／驿站"
                        "加急件／消息雀口哨＝事实性赛博意象〕/情 1 网络世代孩童好奇温和共鸣如实非强极点/时 2 人物"
                        "档案常青面如实·IP 世界观固有零衰减/台 2 公众号方图承载＝MC-001~018 S3 实证复用·图鉴＝"
                        "空间序列叙事载体格式（O-1327 research §2 #3 A 档通识·按 hit-chain-mechanism v1.0 "
                        "§2/§9·D-BS-06 production open）")
meta["red_line"] = ("aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党／无来源不发布（来源＝户籍卡档案指针）"
                    "／密钥、仓位、token 用量、未公开财务不入帧（脱敏律·年轮〔含城市实况锚〕/思想/语言/服装/经历"
                    "〔含暗恋面〕/行为/关系字段＝选材排除不进卡面）；成品只入库＝M5 账号物理件未开+M4 全绿前零发布")

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES

# --- machine em check (R301 em_check precedent, renderer truth) ---
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
io.open(os.path.join(TMP, "em-check-r302.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V12, "cards.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
io.open(os.path.join(V12, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n基于硅基城市居民户籍卡档案（展示锚 C-00021）\n")
print("BUILD OK")
