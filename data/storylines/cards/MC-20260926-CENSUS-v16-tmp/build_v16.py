# -*- coding: utf-8 -*-
"""MC-20260926-CENSUS-v16 build: C-00025 陆海峰 census card (R306).
Template = v15 cards.json (R305). Fields per anchor verbatim, six-line
assembly law (R291 first-defined, series reuse). Em budget machine check
via renderer _line_cost, assert-in-build (R302 precedent). All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V15 = os.path.join(BASE, "MC-20260926-CENSUS-v15")
V16 = os.path.join(BASE, "MC-20260926-CENSUS-v16")
TMP = V16 + "-tmp"
os.makedirs(V16, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V15, "cards.json"), encoding="utf-8"))

LINES = [
    "城市图鉴 016",
    "C-00025 · 陆海峰",
    "碳基市民 · 弄堂派 · 男 · 52 岁",
    "江面与光桥 · 渡轮航道 · 渡轮船长",
    "信条：「船稳，人心才稳。」",
    "稳 · 直性子 · 记性好",
    "全城唯一保留「慢班渡轮」的船长",
]

H2_SIZE = 50  # ladder: district/career line 16.10em single longest driver; 50 budget 18.4em margin 2.3em (v14 18.0em@50 precedent band); 19.0em+ excludes 50 (v3 precedent)

meta = cfg["meta"]
meta["topic"] = "MC-20260926-CENSUS-v16"
meta["form"] = ("CENSUS 居民卡图鉴 016（hit-chain v1.0 全链审查留痕·图鉴系列量产按序领件第十五件＝"
                "万人卡按卡号序 C-00025）——陆海峰（渡轮船长·渡轮航道）")
meta["source_facts"] = ("纪实字段汇编律：户籍卡字段 verbatim 六行汇编（C-00025 物种碳基市民·弄堂派／"
                        "性别年龄男·52 岁／城区 江面与光桥·渡轮航道／职业首词渡轮船长〔破折号阐释尾「江上摆渡人——"
                        "三流数据道的活船老大」＝选材排除〕／信条「船稳，人心才稳。」／性格三关键词 "
                        "稳·直性子·记性好〔括号注＝选材排除〕／钩子 全城唯一保留「慢班渡轮」的船长"
                        "〔破折号尾「不为生意，只为给想慢慢看江的人留一趟船，船票恒价：一句『多谢』」＝选材排除〕）")
meta["source_pointer"] = ("life/BigLife/census/anchors/C-00025.md 手写展示锚（跨仓只读·schema=census/INDEX.md+"
                          "CODEX §八 十三字段·未选字段按律可核，M4 编辑留痕）")
meta["attribution_rule"] = ("署名＝卡级实名：本件引 C-00025 户籍卡＝BigLife 万人库虚构居民（FluxVerse 世界观·"
                            "非真实人物·避讳律照 CODEX §五）；charter §2.4 人设权红线专项核＝只引已登记字段"
                            "零新增人格·荣誉席核＝C-00025 非荣誉席")
meta["triple_label"] = ("虚实级+来源级＝图内双落（subs.srt 底部行「基于硅基城市居民户籍卡档案（展示锚 C-00025）」）"
                        "+AIGC 角标＝常驻每帧 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）")
meta["editorial_value"] = ("图鉴体裁+十三字段选六（编辑选材面＝卡题编号+物种年龄+城区职业+信条+性格关键词+"
                           "钩子综合尾＝选材排除面可机核）+人物页叙事包装·系列第十六张「城市图鉴」与「城市语录」"
                           "「城市盘点」平行系列连载识别结构·编辑价值防低创作度 7.1-7.4 编辑价值面（charter §5 "
                           "自动化合规上限）")
meta["hit_chain_m0"] = ("M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔52 岁渡轮船长 vs 数据道再快永远留着慢班＝"
                        "最快数据城市×最慢班次反差+信条「船稳，人心才稳。」＝船稳〔航行技术〕×人心稳〔群体情感〕"
                        "反差对仗金句级+钩子行「全城唯一保留『慢班渡轮』的船长」＝具体稀缺性·三流数据道／慢班渡轮／"
                        "雾天铜哨对暗号／守夜灯灵十四号路灯＝事实性赛博意象·**江面与光桥＝城区谱系江面水域面首证**"
                        "〔v1-v15 城区谱系：老城厢弄堂/编年史馆区/QUANT/GAME/MEDIA 后水域航道面展开首证〕+"
                        "**渡轮船长＝职业谱系水上交通/航运行业首证**·陆海峰＝万人卡新面孔〔无有声线前史·"
                        "novel 全文零出场 grep 实证·非跨载体复用如实注记〕/情 1 弄堂派老船工温和共鸣如实非强极点/"
                        "时 2 人物档案常青面如实·IP 世界观固有零衰减/台 2 公众号方图承载＝MC-001~022 S3 实证复用·"
                        "图鉴＝收集型大众格式（O-1327 research §2 #3 A 档通识·按 hit-chain-mechanism v1.0 "
                        "§2/§9·D-BS-06 production open）")
meta["red_line"] = ("aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党／无来源不发布（来源＝户籍卡档案指针）"
                    "／密钥、仓位、token 用量、未公开财务不入帧（脱敏律·年轮〔城市实况锚行〕/思想〔父亲轮渡船长+"
                    "大雾夜全船合唱面〕/语言〔上海话底色+报站腔面〕/服装〔藏青盘扣外套+船帽+铜哨面〕/经历〔家谱数据线+"
                    "教徒弟手艺面〕/行为〔绕船三圈+记录真实风力+退潮慢船面〕/关系〔老伴小卖部+徒弟高小满+守夜灯灵老友面〕"
                    "字段＝选材排除不进卡面）；成品只入库＝M5 账号物理件未开+M4 全绿前零发布")

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES

# --- machine em check (R301-R305 precedent, renderer truth, assert-in-build) ---
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
io.open(os.path.join(TMP, "em-check-r306.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V16, "cards.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
io.open(os.path.join(V16, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n基于硅基城市居民户籍卡档案（展示锚 C-00025）\n")
print("BUILD OK")
