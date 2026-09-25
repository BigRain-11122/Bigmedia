# -*- coding: utf-8 -*-
"""MC-20260926-CENSUS-v20 build: C-00029 咪喱 census card (R312).
Template = v19 cards.json (R311). Fields per anchor verbatim, six-line
assembly law (R291 first-defined, series reuse). Em budget machine check
via renderer _line_cost, assert-in-build (R302 precedent). All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V19 = os.path.join(BASE, "MC-20260926-CENSUS-v19")
V20 = os.path.join(BASE, "MC-20260926-CENSUS-v20")
TMP = V20 + "-tmp"
os.makedirs(V20, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V19, "cards.json"), encoding="utf-8"))

LINES = [
    "城市图鉴 020",
    "C-00029 · 咪喱",
    "像素灵 · radiocat · 无定 · 第 19 数据季",
    "GAME 城 · 像素匠人巷 · 伴居灵",
    "信条：「蹭饭是门艺术，报恩是门手艺。」",
    "好奇 · 追光 · 嘴甜",
    "全城唯一拥有「巷志」的猫",
]

H2_SIZE = 44  # ladder: species line ~20.15em single longest driver (radiocat latin 8ch vs nightlamp 9ch = v19 20.70em minus 0.55em); 46 excluded (budget 20.0em < 20.15em per v19 same-type precedent), 44 budget 20.91em margin ~0.76em positive (R293 zero-margin law not triggered)

meta = cfg["meta"]
meta["topic"] = "MC-20260926-CENSUS-v20"
meta["form"] = ("CENSUS 居民卡图鉴 020（hit-chain v1.0 全链审查留痕·图鉴系列量产按序领件第十九件＝"
                "万人卡按卡号序 C-00029）——咪喱（伴居灵·像素匠人巷·GAME 城·像素灵 radiocat）")
meta["source_facts"] = ("纪实字段汇编律：户籍卡字段 verbatim 六行汇编（C-00029 物种像素灵·radiocat／"
                        "性别年龄无定 · 第 19 数据季／城区 GAME 城·像素匠人巷／职业首词伴居灵〔破折号阐释尾"
                        "「弄堂与三城屋顶的伴居者——尾巴天线永远对准最热闹的方向」＝选材排除〕／信条"
                        "「蹭饭是门艺术，报恩是门手艺。」／性格三关键词 好奇·追光·嘴甜〔括号注＝选材排除〕／"
                        "钩子 全城唯一拥有「巷志」的猫〔破折号尾「罗大壮按月给它画像记录体形与光纹变化，"
                        "档案馆破例收了副本，题名《咪喱巷志》」＝选材排除〕）")
meta["source_pointer"] = ("life/BigLife/census/anchors/C-00029.md 手写展示锚（跨仓只读·schema=census/INDEX.md+"
                          "CODEX §八 十三字段·未选字段按律可核，M4 编辑留痕）")
meta["attribution_rule"] = ("署名＝卡级实名：本件引 C-00029 户籍卡＝BigLife 万人库虚构居民（FluxVerse 世界观·"
                            "非真实人物·避讳律照 CODEX §五）；charter §2.4 人设权红线专项核＝只引已登记字段"
                            "零新增人格·荣誉席核＝C-00029 非荣誉席")
meta["triple_label"] = ("虚实级+来源级＝图内双落（subs.srt 底部行「基于硅基城市居民户籍卡档案（展示锚 C-00029）」）"
                        "+AIGC 角标＝常驻每帧 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）")
meta["editorial_value"] = ("图鉴体裁+十三字段选六（编辑选材面＝卡题编号+物种年龄+城区职业+信条+性格关键词+"
                           "钩子综合尾＝选材排除面可机核）+人物页叙事包装·系列第二十张「城市图鉴」与「城市语录」"
                           "「城市盘点」「城市速报」平行系列连载识别结构·编辑价值防低创作度 7.1-7.4 编辑价值面（charter §5 "
                           "自动化合规上限）")
meta["hit_chain_m0"] = ("M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔伴居灵＝全巷公共宠物的最会蹭饭职业 vs "
                        "信条「蹭饭是门艺术，报恩是门手艺。」＝蹭饭〔白吃行为〕×报恩〔手艺化偿还〕反差对仗金句级+"
                        "钩子行「全城唯一拥有「巷志」的猫」＝具体稀缺性·尾巴天线永远对准最热闹的方向／喵语七八种音调"
                        "巷子里人人听得懂个大概／高兴时踩的步子像小碎鼓／生气时把耳朵拍得啪啪响全巷小孩都会学／"
                        "柔光绒羽奶牛猫配色（它自己选的「接地气」）／左耳缺口为救卡在管线里的小消息雀留下"
                        "不许说是「英勇」「就是耳朵痒」／台风「梅花」夜全巷通讯中断一趟一趟把口信叼到位"
                        "第二天早饭吃了七家／匠人巷编外巷长（自封）办公室＝罗家窗台＝事实性赛博意象·"
                        "**伴居灵＝职业谱系宠物/社区伴居服务行业首证**+**radiocat＝像素灵亚型第二证**"
                        "〔v19 nightlamp 首证后第二亚型〕+**像素灵＝物种面第三物种类第二件**〔v19 首证后第二件像素灵卡〕+"
                        "**前后卡序列承接位＝关系面互证第五案＝多卡互指网首证**〔最投缘＝王多多＝v12 C-00021 口哨召消息雀跨卡对位·"
                        "收编人类三户＝粥铺阿凤（管布头）＝C-00010 v1 顾阿凤+回测田那位＝C-00017 v8 归档者-07+"
                        "画匠家（管毛线）＝C-00018 v9 罗大壮三卡互引·经历字段「画匠把它画进了那天的门脸像里」＝v9 钩子"
                        "「每月给老城门画门脸像」同场事件双档·台风「梅花」＝v18 邓建国+v19 十四号路灯同场台风三卡共时〕·"
                        "咪喱＝万人卡新面孔〔无有声线前史·git grep 零出场实证·非跨载体复用如实注记〕/"
                        "情 1 巷弄烟火里被一只猫收编全巷的温和笑点共鸣如实/时 2 人物档案常青面如实·IP 世界观固有零衰减/"
                        "台 2 公众号方图承载＝MC-001~027 S3 实证复用·图鉴＝收集型大众格式（O-1327 research §2 #3 A 档通识·"
                        "按 hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open）")
meta["red_line"] = ("aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党／无来源不发布（来源＝户籍卡档案指针）"
                    "／密钥、仓位、token 用量、未公开财务不入帧（脱敏律·年轮〔城市实况锚行〕/思想〔全巷公共宠物定位+"
                    "耳朵借给对人好的人面〕/语言〔喵语音调+小碎鼓+拍耳朵面〕/服装〔柔光绒羽奶牛猫配色+左耳缺口面〕/"
                    "经历〔雨季首场雨诞生+台风夜口信+编外巷长现状面〕/行为〔巡视全巷+报喜绕梁三圈+雨天蒸笼边面〕/"
                    "关系〔灵群 L-02 电波猫群九只老大+恩人名单+王多多投缘面〕字段＝选材排除不进卡面）；"
                    "成品只入库＝M5 账号物理件未开+M4 全绿前零发布")

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES

# --- machine em check (R301-R311 precedent, renderer truth, assert-in-build) ---
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
io.open(os.path.join(TMP, "em-check-r312.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V20, "cards.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
io.open(os.path.join(V20, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n基于硅基城市居民户籍卡档案（展示锚 C-00029）\n")
print("BUILD OK")
