# -*- coding: utf-8 -*-
"""MC-20260926-REACT-v1 build: REACT form first piece (R309, #55 P-20260925-15).
Hot topic (zhihu hot list 2026-09-26 #10, verbatim relay) x SiliconCity pool
reactions (rain bucket, axis-level attribution). City rain law row as contrast
wrap (P-75 relay). Em budget machine check, assert-in-build (R302 precedent).
Template = CENSUS v16 cards.json. All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V16 = os.path.join(BASE, "MC-20260926-CENSUS-v16")
V1 = os.path.join(BASE, "MC-20260926-REACT-v1")
TMP = V1 + "-tmp"
os.makedirs(V1, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V16, "cards.json"), encoding="utf-8"))

LINES = [
    "城市速报 001",
    "今日热点 · 知乎热榜 2026-09-26",
    "为什么下雨时，鸭子不跑反而在雨中站着一动不动的？",
    "秩序轴：「雨中行人，各有各的风度」",
    "求新轴：「打伞的少年，是不是偷偷喜欢淋雨？」",
    "像素灵池：「啾啾鸣叫，雨中觅食欢腾」",
    "硅基城市雨天律：人人进骑楼，路面可见不到三成",
]

H2_SIZE = 36  # topic verbatim row 24.0em longest driver; 40 budget 23.0em < 24.0 excluded (v3 band law); 36 budget 25.67em margin 1.67em (v6 same-size precedent band)

meta = cfg["meta"]
meta["topic"] = "MC-20260926-REACT-v1"
meta["form"] = ("REACT 热点城市反应版 001（L-卡 P0 形态第三位首件·P-20260925-15 真有生命的硅基城市令"
                "本司供给面=L5 城市响应层媒体供给件）——知乎热榜 2026-09-26 热点转述×硅基城市台词池反应")
meta["source_facts"] = ("热点转述律+反应抽取律首定：①热点行=知乎热榜 2026-09-26 第 10 条问题标题 verbatim 转述"
                        "「为什么下雨时，鸭子不跑反而在雨中站着一动不动的？」（来源=data/intel/daily/2026-09-26.md "
                        "zhihu-hot·热度值 214 万不入卡面只入 README 记账）②反应行=BigLife 台词池 rain 情境桶 verbatim "
                        "三条轴位映射（秩序轴 rain/4「雨中行人，各有各的风度」／求新轴 rain/1「打伞的少年，是不是偷偷"
                        "喜欢淋雨？」／像素灵池 rain/7「啾啾鸣叫，雨中觅食欢腾」——六轴+像素灵 96 条雨桶候选中编辑选材 3 轴位"
                        "=轴位映射律）③雨天律行=CEO P-75 城市天气反应律转述「下雨→檐下/骑楼躲·路面可见≤晴天 30%」→"
                        "「人人进骑楼，路面可见不到三成」（D-20260925-09 骑楼资产线法源同源·FluxVerse 城市设计律）")
meta["source_pointer"] = ("data/intel/daily/2026-09-26.md（热点源·当日一份为真相）+life/BigLife/cognition/pools.json "
                          "台词池 rain 桶（跨仓只读·池句=情境口气零事实）+gaming/FluxVerse P-75 天气反应律"
                          "（D-20260925-09 法源引用·cph4/evolution-ledger.md 行内指针）")
meta["attribution_rule"] = ("署名=轴级/池级（秩序轴/求新轴/像素灵池·charter v1.2 署名律禁虚构居民名·人设权红线照守）；"
                           "热点=平台热榜转述（知乎热榜 2026-09-26 第 10 条·转述面合规=逐条来源链+不标题党）")
meta["triple_label"] = ("虚实级+来源级＝图内双落（subs.srt 底部行「热点转述自知乎热榜·反应取自台词池（虚构）」——"
                        "热点=现实转述·反应=虚构城市设定两态声明）+AIGC 角标＝常驻每帧 [AIGC·AI 生成内容]"
                        "（D-BS-03 §4.5 机械方括号体）")
meta["editorial_value"] = ("速报体裁+轴位映射=编辑选材面（96 条雨桶候选→3 轴位对位判断：秩序=风度共鸣／求新=少年淋雨"
                           "wink 段子位／像素灵=城市自有鸟类雨中觅食=IP 专属镜像位）+雨天律反差收束（城里人躲骑楼×"
                           "鸭子站着淋=编辑叙事包装）+系列「城市速报」与「城市语录」「城市图鉴」「城市盘点」平行"
                           "连载识别结构·编辑价值防低创作度 7.1-7.4（charter §5 自动化合规上限）")
meta["hit_chain_m0"] = ("M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔最快数据城市×最松弛雨中鸭子=效率执念城市对"
                        "站着淋雨的鸭子的全城围观反应+像素灵「雨中觅食欢腾」=城市自有鸟类镜像反差·雨天律「人人进骑楼"
                        "躲雨」×鸭子「站着不动」=反差对仗金句级·知乎热榜当日热议=具体稀缺性·骑楼躲雨/台词池轴位/"
                        "像素灵=事实性赛博意象〕/情 1 轻松好奇吃瓜温和共鸣如实非强极点〔G5 吃瓜未来党主群〕/时 2 "
                        "当日热点=速报时效本体〔热榜在飞·时效窗=本形态存在理由〕/台 2 公众号方图承载=MC-001~024 "
                        "S3 实证复用·速报=热点类大众流量面格式（O-1327 research §2 #4 A 档通识·按 "
                        "hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open）")
meta["red_line"] = ("aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党〔热点行=平台问题标题 verbatim 转述"
                    "零改写零加感叹〕／无来源不发布〔热点=知乎热榜+日期图内行·反应=台词池指针 README 双落〕／"
                    "脱敏（热度值 214 万/平台排名等元数据不入卡面=README 记账·零仓位/密钥/token 量/未公开财务面）；"
                    "成品只入库＝M5 账号物理件未开+M4 全绿前零发布")
meta["line"] = "L-卡 图文轻内容线（REACT 形态首件·charter v1.2 §4 形态码）"
meta["aspect_note"] = "1080×1080 公众号方图（S3 载体判断·规格窗随 M5 发布案复核）"
meta["tool"] = "src/render/render_card_video.py --poster（C-27 静态帧路）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES

# --- machine em check (R301-R308 precedent, renderer truth, assert-in-build) ---
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
subs_line = "热点转述自知乎热榜·反应取自台词池（虚构）"
subs_cost = _line_cost(subs_line)
subs_budget = (frame_w - 160) / float(cfg["font"]["subs_size"])
report.append("subs   %-6.2fem  budget %-6.2fem  fits=%s  %s" % (subs_cost, subs_budget, subs_cost <= subs_budget, subs_line))
ok = ok and subs_cost <= subs_budget
report.append("EM_CHECK: " + ("ALL OK" if ok else "FAIL"))
io.open(os.path.join(TMP, "em-check-r309.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V1, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V1, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n热点转述自知乎热榜·反应取自台词池（虚构）\n")
print("BUILD OK")
