# -*- coding: utf-8 -*-
"""MC-20260926-CENSUS-v17 build: C-00026 高小满 census card (R308).
Template = v16 cards.json (R306). Fields per anchor verbatim, six-line
assembly law (R291 first-defined, series reuse). Em budget machine check
via renderer _line_cost, assert-in-build (R302 precedent). All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V16 = os.path.join(BASE, "MC-20260926-CENSUS-v16")
V17 = os.path.join(BASE, "MC-20260926-CENSUS-v17")
TMP = V17 + "-tmp"
os.makedirs(V17, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V16, "cards.json"), encoding="utf-8"))

LINES = [
    "城市图鉴 017",
    "C-00026 · 高小满",
    "碳基市民 · 新市民派 · 女 · 22 岁",
    "江面与光桥 · 光桥市集 · 穿城信使",
    "信条：「急件不急，稳到才算到。」",
    "勤快 · 直性子 · 随缘",
    "全城唯一给每单写「一句话交货注脚」的信使",
]

H2_SIZE = 44  # ladder: hook line 20.0em single longest driver; 50/46 excluded (18.4/20.0em < or == 20.0em; zero-margin law per R293), 44 budget 20.91em margin 0.91em (v13/v5 precedent band)

meta = cfg["meta"]
meta["topic"] = "MC-20260926-CENSUS-v17"
meta["form"] = ("CENSUS 居民卡图鉴 017（hit-chain v1.0 全链审查留痕·图鉴系列量产按序领件第十六件＝"
                "万人卡按卡号序 C-00026）——高小满（穿城信使·光桥市集）")
meta["source_facts"] = ("纪实字段汇编律：户籍卡字段 verbatim 六行汇编（C-00026 物种碳基市民·新市民派／"
                        "性别年龄女·22 岁／城区 江面与光桥·光桥市集／职业首词穿城信使〔破折号阐释尾「全城急件的摆渡人——"
                        "光桥和渡轮是她家走廊」＝选材排除〕／信条「急件不急，稳到才算到。」／性格三关键词 "
                        "勤快·直性子·随缘〔括号注＝选材排除〕／钩子 全城唯一给每单写「一句话交货注脚」的信使"
                        "〔破折号尾「『今夜风大，交到本人手里』这样的字条，档案馆的年轻人专门收藏了一沓」＝选材排除〕）")
meta["source_pointer"] = ("life/BigLife/census/anchors/C-00026.md 手写展示锚（跨仓只读·schema=census/INDEX.md+"
                          "CODEX §八 十三字段·未选字段按律可核，M4 编辑留痕）")
meta["attribution_rule"] = ("署名＝卡级实名：本件引 C-00026 户籍卡＝BigLife 万人库虚构居民（FluxVerse 世界观·"
                            "非真实人物·避讳律照 CODEX §五）；charter §2.4 人设权红线专项核＝只引已登记字段"
                            "零新增人格·荣誉席核＝C-00026 非荣誉席")
meta["triple_label"] = ("虚实级+来源级＝图内双落（subs.srt 底部行「基于硅基城市居民户籍卡档案（展示锚 C-00026）」）"
                        "+AIGC 角标＝常驻每帧 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）")
meta["editorial_value"] = ("图鉴体裁+十三字段选六（编辑选材面＝卡题编号+物种年龄+城区职业+信条+性格关键词+"
                           "钩子综合尾＝选材排除面可机核）+人物页叙事包装·系列第十七张「城市图鉴」与「城市语录」"
                           "「城市盘点」平行系列连载识别结构·编辑价值防低创作度 7.1-7.4 编辑价值面（charter §5 "
                           "自动化合规上限）")
meta["hit_chain_m0"] = ("M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔22 岁穿城信使 vs 信条「急件不急，稳到才算到。」＝"
                        "最急职业〔急件摆渡人〕×最慢纪律〔稳到才算到〕反差+信条「急件不急，稳到才算到。」＝"
                        "急件〔时效催逼〕×稳到〔交付确定〕反差对仗金句级+钩子行「全城唯一给每单写『一句话交货注脚』的信使」＝"
                        "具体稀缺性·一句话交货注脚「今夜风大，交到本人手里」／全城口哨打得最响的姑娘／"
                        "包底永远有一把伞「桥上常有人淋着」／光桥和渡轮是她家走廊＝事实性赛博意象·"
                        "**穿城信使＝职业谱系快递/配送物流行业首证**+**江面与光桥＝同城第二卡**〔v16 陆海峰渡轮航道后"
                        "光桥市集续证·v13-v15 MEDIA 三连同型〕+**前后卡序列承接位＝关系面互证第三案**"
                        "〔C-00026 关系字段「忘年交＝渡轮船长陆海峰」＝v16 相邻卡互引·与 C-00025 关系字段「徒弟高小满」"
                        "双向对位＝首件互指闭合对+行为字段「休息日去江边教王多多认近道」＝v12 C-00021 互引·"
                        "关系/行为字段＝选材排除不进卡面如实注记〕·高小满＝万人卡新面孔〔无有声线前史·"
                        "novel/音频线 rg 零出场实证·非跨载体复用如实注记〕/情 1 江淮进城青年自食其力温和共鸣如实非强极点/"
                        "时 2 人物档案常青面如实·IP 世界观固有零衰减/台 2 公众号方图承载＝MC-001~023 S3 实证复用·"
                        "图鉴＝收集型大众格式（O-1327 research §2 #3 A 档通识·按 hit-chain-mechanism v1.0 "
                        "§2/§9·D-BS-06 production open）")
meta["red_line"] = ("aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党／无来源不发布（来源＝户籍卡档案指针）"
                    "／密钥、仓位、token 用量、未公开财务不入帧（脱敏律·年轮〔城市实况锚行〕/思想〔光桥市集摆摊卖家乡酱菜+"
                    "驿站招信使+「多谢」比酱菜好卖面〕/语言〔江淮官话「搞快点」「不存在」「多大事」+行话「接单」「跨江」"
                    "「妥投」+全城口哨打得最响面〕/服装〔工装夹克运动鞋+双肩包徽章+包底一把伞「桥上常有人淋着」面〕/"
                    "经历〔头一单加急送药立规矩+驿站金牌信使+「小满站」开店攒钱面〕/行为〔雨声加班费+心里「收到了」+"
                    "教王多多认近道面〕/关系〔H-1016 室友合租+师父驿站老板娘+忘年交陆海峰面〕字段＝选材排除不进卡面）；"
                    "成品只入库＝M5 账号物理件未开+M4 全绿前零发布")

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES

# --- machine em check (R301-R306 precedent, renderer truth, assert-in-build) ---
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
io.open(os.path.join(TMP, "em-check-r308.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V17, "cards.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
io.open(os.path.join(V17, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n基于硅基城市居民户籍卡档案（展示锚 C-00026）\n")
print("BUILD OK")
