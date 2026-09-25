# -*- coding: utf-8 -*-
"""MC-20260926-REACT-v2 build: REACT series 2nd piece (R313, backlog #59 daily-hot claim).
Hot topic (zhihu hot list 2026-09-26 #5, verbatim relay, 71-yuan number fidelity) x
SiliconCity pool reactions (market_open bucket, single-bucket 3-axis mapping, R309 law
reuse) + census C-00016 canteen-creed wrap row (verbatim, job-level attribution).
Em budget ladder machine check, assert-in-build (R302/R312 precedent).
Template = REACT v1 cards.json. All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V1 = os.path.join(BASE, "MC-20260926-REACT-v1")
V2 = os.path.join(BASE, "MC-20260926-REACT-v2")
TMP = V2 + "-tmp"
os.makedirs(V2, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V1, "cards.json"), encoding="utf-8"))

LINES = [
    "城市速报 002",
    "今日热点 · 知乎热榜 2026-09-26",
    "全国牛肉批发均价涨至一公斤 71 元，创两年来新高，受哪些因素影响？",
    "烟火轴：「米价又涨了点，赶紧看看」",
    "侠气轴：「大风大浪见得多了，啥行情没经历过」",
    "像素灵池：「啾啾鸣叫行情起」",
    "QUANT 食堂信条：「行情再绿，汤是热的。」",
]

SUBS_LINE = "热点转述自知乎热榜·反应与信条皆取自虚构城市档案"

# --- em budget ladder (parametric pre-fit law; largest size where every h2 line is single-line fits) ---
frame_w = cfg["video"]["width"]
h1_size = cfg["font"]["h1_size"]
subs_size = cfg["font"]["subs_size"]
LADDER = [50, 46, 44, 40, 36, 32, 28, 26, 24]


def all_fit(size):
    budget = (frame_w - 160) / float(size)
    for ln in LINES[1:]:
        if _line_cost(ln) > budget or len(wrap_for_width(ln, size, frame_w).split("\n")) != 1:
            return False
    return True


H2_SIZE = next(s for s in LADDER if all_fit(s))

meta = cfg["meta"]
meta["topic"] = "MC-20260926-REACT-v2"
meta["form"] = ("REACT 热点城市反应版 002（L-卡 P0 形态第三位·L5 城市响应层媒体供给件·#59 按日热点随轮领"
                "首续件·R309 双律复用）——知乎热榜 2026-09-26 热点转述×硅基城市台词池反应×食堂信条收束")
meta["source_facts"] = ("热点转述律+反应抽取律 R309 双律复用：①热点行=知乎热榜 2026-09-26 第 5 条问题标题 verbatim "
                       "转述「全国牛肉批发均价涨至一公斤 71 元，创两年来新高，受哪些因素影响？」（来源="
                       "data/intel/daily/2026-09-26.md zhihu-hot·热度值 391 万与排名元数据不入卡面只入 README 记账·"
                       "71 元/两年新高数值保真转述）②反应行=BigLife 台词池 market_open 情境桶 verbatim 三条轴位映射"
                       "（烟火轴 market_open/7「米价又涨了点，赶紧看看」／侠气轴 market_open/5「大风大浪见得多了，"
                       "啥行情没经历过」／像素灵池 market_open/2「啾啾鸣叫行情起」——**单桶纪律**=涨价行情情境→"
                       "market_open 桶·编辑选材 3 轴位=轴位映射律）③收束行=万人卡 C-00016 徐根福信条 verbatim"
                       "「行情再绿，汤是热的。」（QUANT 食堂大厨·职业级署名不指名=REACT 署名律兼容·已登记字段 "
                       "verbatim 零新增人格·人设权红线照守）")
meta["source_pointer"] = ("data/intel/daily/2026-09-26.md（热点源·当日一份为真相）+life/BigLife/cognition/pools.json "
                          "台词池 market_open 桶（跨仓只读·池句=情境口气零事实）+life/BigLife/census/anchors/"
                          "C-00016.md 万人卡手写锚（跨仓只读·信条字段 verbatim·非荣誉席·CENSUS-v7 F-026 同源字段"
                          "跨形态复用）")
meta["attribution_rule"] = ("署名=轴级/池级/职业级（烟火轴/侠气轴/像素灵池/QUANT 食堂·charter v1.2 署名律禁虚构居民名·"
                            "人设权红线照守）；热点=平台热榜转述（知乎热榜 2026-09-26 第 5 条·转述面合规=逐条来源链+不标题党）")
meta["triple_label"] = ("虚实级+来源级＝图内双落（subs.srt 底部行「热点转述自知乎热榜·反应与信条皆取自虚构城市档案」——"
                        "热点=现实转述·反应与信条=虚构城市档案两态声明·池与户籍卡双虚构源并落）+AIGC 角标＝常驻每帧 "
                        "[AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）")
meta["editorial_value"] = ("速报体裁+轴位映射=编辑选材面（market_open 桶候选→3 轴位对位判断：烟火=民生涨价共鸣位"
                           "〔米价与牛肉价同频=菜篮子直感〕／侠气=老手定力 wink 位〔量化之城见惯行情的城格自嘲〕／"
                           "像素灵=城市自有灵物对行情的镜像反应位=IP 专属面）+食堂信条收束（牛肉涨价 71 元×「行情再绿，"
                           "汤是热的」=市场波动×人间恒暖反差对仗金句级收束+语录↔图鉴↔速报跨形态同句复用链）+系列"
                           "「城市速报」与「城市语录」「城市图鉴」「城市盘点」平行连载识别结构·编辑价值防低创作度 "
                           "7.1-7.4（charter §5 自动化合规上限）；热点择优判据留痕=映射对位优先于纯热度（#5 391 万 "
                           "market 桶位级直配入选·#3 食物 598 万未选=无专属情境桶跨桶弱对位·#9 呆毛 225 万未选=零映射桶"
                           "〔池探针 2 hits 皆寒潮误中〕·政治敏感面回避律照守=贸易休战/奥委会类不选·竞技面无映射桶"
                           "维持 R309 注记）")
meta["hit_chain_m0"] = ("M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔民生涨价痛点×量化之城见惯行情的定力反差+像素灵"
                        "「啾啾鸣叫行情起」城市自有灵物对行情的镜像反应+食堂信条「行情再绿，汤是热的」市场冷绿×人间"
                        "热汤对仗金句级收束·知乎热榜当日热议=具体稀缺性·market_open 行情桶/像素灵/QUANT 食堂=事实性"
                        "赛博意象〕/情 1 钱包共鸣温和如实非强极点〔G4 投资理财人群+G1 AI 效率实操党双群对位〕/时 2 "
                        "当日热点=速报时效本体〔热榜在飞·时效窗=本形态存在理由〕/台 2 公众号方图承载=MC-001~028 S3 "
                        "实证复用·速报=热点类大众流量面格式（O-1327 research §2 #4 A 档通识·按 hit-chain-mechanism "
                        "v1.0 §2/§9·D-BS-06 production open）")
meta["red_line"] = ("aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党〔热点行=平台问题标题 verbatim 转述"
                    "零改写零加感叹〕／无来源不发布〔热点=知乎热榜+日期图内行·反应=台词池指针·信条=户籍卡 C-00016 指针"
                    "README 双落〕／脱敏（热度值 391 万/平台排名等元数据不入卡面=README 记账·零仓位/密钥/token 量/"
                    "未公开财务面）；成品只入库＝M5 账号物理件未开+M4 全绿前零发布")
meta["line"] = "L-卡 图文轻内容线（REACT 形态第二件·charter v1.2 §4 形态码·#59 按日热点随轮领）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES

# --- machine em check (R301-R312 precedent, renderer truth, assert-in-build) ---
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("H1 size %d budget %.2fem | H2 size %d budget %.2fem (ladder pick)" % (h1_size, budget_h1, H2_SIZE, budget_h2))
for ln in LINES:
    cost = _line_cost(ln)
    size = h1_size if ln is LINES[0] else H2_SIZE
    budget = budget_h1 if ln is LINES[0] else budget_h2
    single = len(wrap_for_width(ln, size, frame_w).split("\n")) == 1
    fits = cost <= budget
    ok = ok and single and fits
    report.append("%-6.2fem  budget %-6.2fem  single=%s  %s" % (cost, budget, single, ln))
subs_cost = _line_cost(SUBS_LINE)
subs_budget = (frame_w - 160) / float(subs_size)
report.append("subs   %-6.2fem  budget %-6.2fem  fits=%s  %s" % (subs_cost, subs_budget, subs_cost <= subs_budget, SUBS_LINE))
ok = ok and subs_cost <= subs_budget
report.append("EM_CHECK: " + ("ALL OK" if ok else "FAIL"))
io.open(os.path.join(TMP, "em-check-r313.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V2, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V2, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d" % H2_SIZE)
