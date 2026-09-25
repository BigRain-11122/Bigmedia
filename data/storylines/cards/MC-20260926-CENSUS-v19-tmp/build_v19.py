# -*- coding: utf-8 -*-
"""MC-20260926-CENSUS-v19 build: C-00028 十四号路灯 census card (R311).
Template = v18 cards.json (R310). Fields per anchor verbatim, six-line
assembly law (R291 first-defined, series reuse). Em budget machine check
via renderer _line_cost, assert-in-build (R302 precedent). All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V18 = os.path.join(BASE, "MC-20260926-CENSUS-v18")
V19 = os.path.join(BASE, "MC-20260926-CENSUS-v19")
TMP = V19 + "-tmp"
os.makedirs(V19, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V18, "cards.json"), encoding="utf-8"))

LINES = [
    "城市图鉴 019",
    "C-00028 · 十四号路灯",
    "像素灵 · nightlamp · 无定 · 第 41 数据季",
    "外环感知网 · 边缘街区 · 夜灯员",
    "信条：「灯不问来路，只管照路。」",
    "稳 · 随缘 · 热肠",
    "全城唯一在台风夜把自己亮度开满格的灯灵",
]

H2_SIZE = 44  # ladder: species line 20.70em single longest driver (nightlamp latin 9ch + "41" digits); 50/46 excluded (18.4/20.0em < 20.70em per v3 precedent), 44 budget 20.91em margin 0.21em positive (R293 zero-margin law not triggered)

meta = cfg["meta"]
meta["topic"] = "MC-20260926-CENSUS-v19"
meta["form"] = ("CENSUS 居民卡图鉴 019（hit-chain v1.0 全链审查留痕·图鉴系列量产按序领件第十八件＝"
                "万人卡按卡号序 C-00028）——十四号路灯（夜灯员·外环感知网·边缘街区·像素灵 nightlamp）")
meta["source_facts"] = ("纪实字段汇编律：户籍卡字段 verbatim 六行汇编（C-00028 物种像素灵·nightlamp／"
                        "性别年龄无定 · 第 41 数据季／城区 外环感知网·边缘街区／职业首词夜灯员〔破折号阐释尾「夜城照明与独行客的护送者——"
                        "执灯照径，天亮交晨」＝选材排除〕／信条「灯不问来路，只管照路。」／性格三关键词 "
                        "稳·随缘·热肠〔括号注＝选材排除〕／钩子 全城唯一在台风夜把自己亮度开满格的灯灵"
                        "〔破折号尾「那晚它把外环一段路照成了白昼，检修日志写：超载运行，无损耗，原因不明。它自己说：知道原因，不能说」＝选材排除〕）")
meta["source_pointer"] = ("life/BigLife/census/anchors/C-00028.md 手写展示锚（跨仓只读·schema=census/INDEX.md+"
                          "CODEX §八 十三字段·未选字段按律可核，M4 编辑留痕）")
meta["attribution_rule"] = ("署名＝卡级实名：本件引 C-00028 户籍卡＝BigLife 万人库虚构居民（FluxVerse 世界观·"
                            "非真实人物·避讳律照 CODEX §五）；charter §2.4 人设权红线专项核＝只引已登记字段"
                            "零新增人格·荣誉席核＝C-00028 非荣誉席")
meta["triple_label"] = ("虚实级+来源级＝图内双落（subs.srt 底部行「基于硅基城市居民户籍卡档案（展示锚 C-00028）」）"
                        "+AIGC 角标＝常驻每帧 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）")
meta["editorial_value"] = ("图鉴体裁+十三字段选六（编辑选材面＝卡题编号+物种年龄+城区职业+信条+性格关键词+"
                           "钩子综合尾＝选材排除面可机核）+人物页叙事包装·系列第十九张「城市图鉴」与「城市语录」"
                           "「城市盘点」「城市速报」平行系列连载识别结构·编辑价值防低创作度 7.1-7.4 编辑价值面（charter §5 "
                           "自动化合规上限）")
meta["hit_chain_m0"] = ("M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔夜灯员＝城市照明基础设施的最无声物性 vs "
                        "谁夜里哭过灯知道但灯不说＝最人文护送温度＝基础设施物性×人文温度反差+信条「灯不问来路，只管照路。」＝"
                        "灯〔照明技术职能〕×不问来路只管照路〔无条件护送伦理〕反差对仗金句级+钩子行「全城唯一在台风夜把自己亮度开满格的灯灵」＝"
                        "具体稀缺性·全城对频那一秒在塔尖亮起/「多亮一档」打招呼/暖黄平常心橙红遇上事＝光的颜色是它自己的情绪表/"
                        "台风「梅花」灯罩补丁不许修「疤是资历」/「交晨」＝它发明的词/路过夜宵摊多亮半档「让摊主知道有人看见他的辛苦」/"
                        "雾天跟渡轮船长的铜哨对暗号两长一短「这段有我」＝事实性赛博意象·**夜灯员＝职业谱系市政照明/夜间公共服务行业首证**+"
                        "**像素灵＝CENSUS 物种面第三物种类首证**〔v1-v18 碳基市民+硅基民双面后像素灵面展开首证〕+"
                        "**nightlamp＝像素灵亚型首证**+**前后卡序列承接位＝关系面互证第四案＝三卡互指链首证**"
                        "〔老友＝渡轮船长陆海峰＝v16 铜哨暗号对传三十年+v16 意象「守夜灯灵十四号路灯」提前点名双向对位·"
                        "最惦记高小满＝v17「跑夜单，伞永远在包里却永远不撑」＝v17 行为字段「包底永远有一把伞」跨卡对位·"
                        "塔站的值守员说它比仪器可靠＝v18 互证·台风「梅花」＝v18 邓建国守一宿同场台风跨卡共时首证〕·"
                        "十四号路灯＝万人卡新面孔〔无有声线前史·novel/音频线 rg 零出场实证·非跨载体复用如实注记〕/"
                        "情 1 夜路独行客被无声守护的温和共鸣如实非强极点/时 2 人物档案常青面如实·IP 世界观固有零衰减/"
                        "台 2 公众号方图承载＝MC-001~025 S3 实证复用·图鉴＝收集型大众格式（O-1327 research §2 #3 A 档通识·"
                        "按 hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open）")
meta["red_line"] = ("aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党／无来源不发布（来源＝户籍卡档案指针）"
                    "／密钥、仓位、token 用量、未公开财务不入帧（脱敏律·年轮〔城市实况锚行〕/思想〔对频夜出生+记性是光+"
                    "最懂外环的夜面〕/语言〔光语+铜哨暗号面〕/服装〔暖光外衣颜色情绪表+梅花补丁面〕/经历〔调试夜所生+"
                    "桥上哭的年轻人鞠躬+守夜路现状面〕/行为〔交晨+恒定步频+夜宵摊半档面〕/关系〔灵群 L-01 五盏老大+"
                    "老友陆海峰+惦记高小满面〕字段＝选材排除不进卡面）；成品只入库＝M5 账号物理件未开+M4 全绿前零发布")

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES

# --- machine em check (R301-R310 precedent, renderer truth, assert-in-build) ---
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
io.open(os.path.join(TMP, "em-check-r311.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V19, "cards.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
io.open(os.path.join(V19, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n基于硅基城市居民户籍卡档案（展示锚 C-00028）\n")
print("BUILD OK")
