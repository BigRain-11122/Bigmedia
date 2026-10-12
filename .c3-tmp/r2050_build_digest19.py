# -*- coding: utf-8 -*-
"""MC-20261012-DIGEST-v19 build (顶层梳理日数字盘点).

Pre-stage leg (R2050, CPU face, CEO-pause window take per O-20261012-1115 CPU duty +
O-20261009-1246 item c waiting-window take): machine-verify the 10-11 evening -> 10-12
noon order-cluster anchors (22 new rows, v18 史源窗之后), emit cards.json + subs.srt.
M2 poster render + 验图 same round (CPU). M4.5 + E4 + F-182 登记 stay gated for the
GPU fire window (R1871->R1938 / R1985->R2002 precedent).
Assertion families (v18 build precedent):
  A1 twelve 10-12-cluster order labels present in HQ orders.md
  A1b/A1c row counts: 10-11 == 23 (13 v18-era + 10 evening backfill), 10-12 == 12 -> 22 new
  A2 CEO verbatim quotes present verbatim; deck quote == continuous substring
  A3 canonical artifacts on disk (bill + PREPRO-MASTER + AUDIENCE-VOICE + DIRECTOR-RULING)
  A4 C-20261012-01 in group decisions.md; F-179 tail registration in finished.md
  A5 deck em costs fit budget at h2_size 40 (23.0em), h1 fits 10.95em
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, "src/render")
from render_card_video import _line_cost  # noqa: E402

ORDERS = r"C:\Users\sjs20\Desktop\FluxGroup\docs\orders.md"
DECISIONS = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
FINISHED = r"output\finished.md"
OUT_DIR = r"data\storylines\cards\MC-20261012-DIGEST-v19"
TMP_DIR = OUT_DIR + "-tmp"

# A1: twelve order labels of the 10-12 cluster (10-11 19:3x -> 10-12 12:3x window)
LABELS = [
    "三车道排产政策令",
    "零卡点流线令",
    "否决窗制度废止令",
    "调色师席介入令",
    "服装师席介入令",
    "歌词意象转化令",
    "全面开工令+MV 专家审查团令",
    "顶层梳理执行令",
    "年代 MV 拍摄语法深研令",
    "CEO 用机让路令+机队满负荷令",
    "MV 全方面预研总纲令",
    "导演拍板权令+机队满负荷令",
    "用户之声采集-筛选-升华令",
    "全并行+云端算力续工强化令",
]
# A2: CEO verbatim quotes (continuous substrings of the cluster rows)
Q_DIRECTOR = "导演拍板，不要都来问我，我看到问题自然会说，没说你们就自己推进"
Q_TOP = "好好从顶层开始梳理规则制度流程，工作流，资源分配等等，建立合理计划，逐步推进，高效落实"
Q_WORK = "我要工作了，本机算力资源腾出来，云端继续，机队其他机器满负荷去做"
Q_PARALLEL = "项目全面开工继续啊！所有的并行！云端"

H1 = "城市盘点 019"
LINES = [
    H1,
    "顶层梳理日（10-12 · 两日 22 行令批）",
    "「" + "，".join(Q_DIRECTOR.split("，")[:2]) + "，",
    "，".join(Q_DIRECTOR.split("，")[2:]) + "」",
    "顶层梳理案同窗收口 · 票档 7/7 · 判据 6 条",
    "四阶段推进 · 盘点 瘦身 治理 常态",
    "法熵守恒 · 新增 ≤3 节 · 退役并档 ≥3 处",
    "三席定律成形 · 道具 调色 服装 三签字闸",
]
H2_SIZE = 40  # v17 band (23.0em budget; longest deck line ~21em driver)
H1_SIZE = 84
BUDGET_H2 = (1080 - 160) / float(H2_SIZE)  # 23.0em
BUDGET_H1 = (1080 - 160) / float(H1_SIZE)  # ~10.95em

orders_txt = io.open(ORDERS, encoding="utf-8").read()
dec_txt = io.open(DECISIONS, encoding="utf-8").read()
fin_txt = io.open(FINISHED, encoding="utf-8").read()

results = []
results.append(("A1 fourteen cluster order labels", all(lb in orders_txt for lb in LABELS)))
n_1011ev = len([l for l in orders_txt.splitlines() if re.match(r"^\|\s*10-11\s+(19|2[0-3])", l)])
n_1012 = len([l for l in orders_txt.splitlines() if re.match(r"^\|\s*10-12\s", l)])
results.append(("A1b 10-11 evening rows (19:xx-23:xx) == 10", n_1011ev == 10))
results.append(("A1c 10-12 rows total 12", n_1012 == 12))
results.append(("A1d cluster total == 22 (10 evening + 12 day)", n_1011ev + n_1012 == 22))
results.append(("A2a quote 11:3x director verbatim", Q_DIRECTOR in orders_txt))
results.append(("A2b quote 09:2x top-level verbatim", Q_TOP in orders_txt))
results.append(("A2c quote 11:1x ceo-work verbatim", Q_WORK in orders_txt))
results.append(("A2d quote 12:3x parallel verbatim", Q_PARALLEL in orders_txt))
quote_join = (LINES[2] + LINES[3]).strip("「」")
results.append(("A2g deck quote == verbatim", quote_join == Q_DIRECTOR))
P_BILL = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\council\C-20261012-01-bill.md"
P_PREPRO = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\fleet\mv-album-001-jay\MV-PREPRO-MASTER-v1.md"
P_VOICE = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\fleet\mv-album-001-jay\AUDIENCE-VOICE-v1.md"
P_RULING = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\fleet\mv0001-handover\canon\DIRECTOR-RULING-20261012.md"
results.append(("A3a C-20261012-01 bill present", os.path.exists(P_BILL)))
results.append(("A3b MV-PREPRO-MASTER present", os.path.exists(P_PREPRO)))
results.append(("A3c AUDIENCE-VOICE present", os.path.exists(P_VOICE)))
results.append(("A3d DIRECTOR-RULING present", os.path.exists(P_RULING)))
results.append(("A4a C-20261012-01 in decisions", "C-20261012-01" in dec_txt))
results.append(("A4b F-179 tail registration", "F-179" in fin_txt))
h1_ok = _line_cost(LINES[0]) <= BUDGET_H1
costs = [_line_cost(s) for s in LINES[1:]]
results.append(("A5a h1 fits budget", h1_ok))
results.append(("A5b h2 lines fit budget", all(c <= BUDGET_H2 for c in costs)))
results.append(("A5c deck line count == 7 (v18 parity)", len(LINES) - 1 == 7))

fail = [name for name, ok in results if not ok]
em_report = []
for name, ok in results:
    print(("PASS " if ok else "FAIL ") + name)
    em_report.append(("PASS " if ok else "FAIL ") + name)
print("em costs: " + ", ".join("%.2f" % c for c in costs) + " budget %.2f" % BUDGET_H2)
em_report.append("em costs: " + ", ".join("%.2f" % c for c in costs) + " budget %.2f" % BUDGET_H2)
if fail:
    print("ASSERTIONS FAILED: %s" % fail)
    sys.exit(1)

meta = {
    "topic": "MC-20261012-DIGEST-v19",
    "line": "L-卡 图文轻内容线（DIGEST 形态第十九件·charter v1.2 §4 形态码·#67 触发律=新令级事件簇随轮领〔R2050 预置腿·CEO pause 窗 CPU 面·R1871/R1985 范式〕）",
    "form": "DIGEST 盘点图文 019（P0 形态 DIGEST 续件第十八件·史源=10-11 晚→10-12 午 22 行令级事件簇=v18〔10-11 全曲冲刺日〕后新落令批·#67 触发律直领）",
    "tool": "src/render/render_card_video.py --poster（静态帧路·v17/v18 同链）",
    "source_facts": "顶层梳理日数字盘点八条：①「顶层梳理日（10-12 · 两日 22 行令批）」=FluxGroup/docs/orders.md 10-11 晚 19:3x→23:5x 十行+10-12 00:0x→12:3x 十二行=两日 22 行令批（build_digest19.py 断言 A1b/A1c/A1d 实锚·v18〔全曲冲刺日〕史源窗后新落令级事件簇）／②引文两行「导演拍板，不要都来问我，」「我看到问题自然会说，没说你们就自己推进。」=10-12 11:3x 导演拍板权令 CEO 原话 verbatim 连续子串跨两行设计排版（v5/v12/v14/v15/v16/v17/v18 先例同型·断言 A2a/A2g 零改字）／③「顶层梳理案同窗收口 · 票档 7/7 · 判据 6 条」=10-12 09:2x 顶层梳理执行令（CEO 原话 verbatim「好好从顶层开始梳理规则制度流程，工作流，资源分配等等，建立合理计划，逐步推进，高效落实」·断言 A2b）+C-20261012-01 集团顶层梳理执行案同窗收口票档 7/7 PASS+预注册判据 6 条（断言 A4a decisions 行+A3a 案卷宗正典 cph4/council/C-20261012-01-bill.md）／④「四阶段推进 · 盘点 瘦身 治理 常态」=执行案四阶段=Phase0 盘点 10-13 交→Phase1 瘦身批+修法包 10-13/15→Phase2 治理窗 10-16→Phase3 常态+四标首报 10-30（令行 09:2x 原文）／⑤「法熵守恒 · 新增 ≤3 节 · 退役并档 ≥3 处」=执行案定位节原文（立法观察期内零新顶层法条·结构修法全部押后 Phase 1 修法包过会·新增 ≤3 节·退役/并档 ≥3 处）／⑥「三席定律成形 · 道具 调色 服装 三签字闸」=10-11 22:3x 道具席令 J-20+10-11 23:5x 调色师席介入令 J-21+10-12 00:0x 服装师席介入令 J-22（帧批三签字闸=BigStream 产线长期律·令行台账）／⑦同簇资源令两行台账位=10-12 11:1x CEO 用机让路令（CEO 原话 verbatim 断言 A2c「我要工作了，本机算力资源腾出来，云端继续，机队其他机器满负荷去做」·本司当窗 pause 执法承其令）+10-12 12:3x 全并行+云端算力续工强化令（CEO 原话 verbatim 断言 A2d「项目全面开工继续啊！所有的并行！云端」）——两行不进卡面·source_facts 承载／⑧MV 域创作类令（反韩化重制/剧本 v5 穿越/拍摄语法深研/全方面预研总纲/用户之声采集）=MV sprint 会话域在执·本卡只入令批计数不采创作细节（他司执行面细节不入卡面分界·v18 同型）——卡面数字 22/7/6/4/3/3 全台账可溯",
    "source_pointer": "FluxGroup/docs/orders.md 10-11 晚→10-12 午令批台账（跨仓只读·本机即集团仓宿主机直读正典零 git 操作零写接触）+FluxGroup/docs/decisions.md C-20261012-01 行+cph4/council/C-20261012-01-bill.md（案卷宗正典）+cph4/fleet/mv-album-001-jay/{MV-PREPRO-MASTER-v1,AUDIENCE-VOICE-v1}.md+cph4/fleet/mv0001-handover/canon/DIRECTOR-RULING-20261012.md（导演拍板权正典·断言 A3d）+本司 output/finished.md F-179 尾位登记（断言 A4b）——编年史 A 级史源（顶层梳理日令批台账·charter §3 一料多吃）",
    "attribution_rule": "署名=纪实线编年史档案级（charter §2.1 纪实线·零虚构居民名·人设权红线照守；引文=CEO 原话 verbatim 连续子串零改字〔11:3x 令逗号子句拆行=排版设计非改字·v18 同型〕）",
    "triple_label": "虚实级+来源级=图内底部行（subs.srt 烧录）「基于硅基城市真实事件（顶层梳理日令批台账档案）」；AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）",
    "editorial_value": "叙事包装=顶层梳理日数字盘点档案体（1 句「没说你们就自己推进」放权令 vs 两日 22 行令批+一案四阶段+7/7 票档+6 判据+三席定律=「一句话 vs 一套机制」母题·F-042 v2 对照数字结构同源第十八证·十九连母题续〔v19 顶层梳理日〕·令→案→票→阶段→定律=「梳理令→执行案→委员会票档→四阶段→产线定律」递进链·CEO 放权+机制接棒=信任面叙事位·v14 集团令批日/v16 首报直投日/v17 审查执法双日/v18 全曲冲刺日同型=令批盘点先例承继第六件；公众号低创作度条款 7.1-7.4 编辑价值面）",
    "hit_chain_m0": "M0 选题四维分 7/8=A 档进 M1（钩 2 数字反差链：1 句「没说你们就自己推进」放权令 vs 两日 22 行令批+票档 7/7+判据 6 条+四阶段+三席+法熵 ≤3/≥3——七组数字反差·F-042 v2 对照数字结构同源第十八证·十九连母题续/情 1 CEO 放权+机器接棒=信任面温和如实非强极点〔G5 吃瓜未来党+G1 信任党双群对位〕/时 2 事件 10-11 晚 19:3x→10-12 午 12:3x 当日窗/台 2 公众号方图承载=MC-001~179 S3 实证复用·盘点=公众号主流图文格式〔O-1327 research §2 #2 A 级通识〕）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·R379 研究件 §5 判据锚定（编年史 A 级事件+数字密度）·#67 触发律=新令级事件簇落账随轮领〔R2050 预置腿·CEO pause 窗 CPU 面·O-20261012-1115 让路执法窗取活〕",
    "aspect_note": "1080×1080 方图=公众号图文通用（S3 载体面·系列 S3 实证复用·平台规格窗随 M5 发布案复核）",
    "red_line": "aigc_notice 烧录每帧（CONSTITUTION S2-4）；脱敏律核=全部数字为令批台账读数（令行数/票档数/判据数/阶段数/席数/法熵节段数=非 token 用量细节非财务非持仓面）；CEO 指令原文 verbatim 纪实照录；P1 边界=本件=纪实档案非提案非表决（MV 域创作类令细节〔反韩化/剧本 v5/拍摄语法/预研总纲/用户之声〕不入卡面只入令批计数=v18 同型分界·他司执行面细节不入卡面·批级行计数合法）；成品只入库·发布=M5 账号物理件+M4 全绿",
}
cards = {
    "meta": meta,
    "video": {"width": 1080, "height": 1080, "fps": 30, "bg": "black"},
    "font": {
        "file": "C:/Windows/Fonts/msyh.ttc",
        "cards_size": 50, "subs_size": 38, "subs_bottom": 110,
        "aigc_size": 30, "line_spacing": 12,
        "h1_font": "C:/Windows/Fonts/msyhbd.ttc",
        "h1_size": 84, "h1_color": "accent",
        "h2_size": H2_SIZE, "h2_color": "white",
        "h1_gap": 36, "optical_center": 0.24,
    },
    "aigc_notice": "[AIGC·AI 生成内容]",
    "tail": 0.8,
    "cards": [{
        "start": 0.0, "end": 3.0,
        "lines": LINES,
    }],
}
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)
with io.open(OUT_DIR + r"\cards.json", "w", encoding="utf-8") as f:
    json.dump(cards, f, ensure_ascii=False, indent=1)
subs = """1
00:00:00,000 --> 00:00:03,000
基于硅基城市真实事件（顶层梳理日令批台账档案）

"""
with io.open(OUT_DIR + r"\subs.srt", "w", encoding="utf-8") as f:
    f.write(subs)
with io.open(TMP_DIR + r"\em-check-r2050.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(em_report) + "\n")
print("WROTE %s\\cards.json + subs.srt" % OUT_DIR)
print("ALL ASSERTIONS GREEN")
