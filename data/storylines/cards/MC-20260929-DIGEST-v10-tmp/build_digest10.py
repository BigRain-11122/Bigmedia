# -*- coding: utf-8 -*-
"""MC-20260929-DIGEST-v10 build: DIGEST series 10th piece (R682, backlog #67 chronicle-event
claim, queue E2 batch pool per C-20260929-02 lane mandate R681). Cloud token saving mechanism
order numeric digest.
Facts from cph4/evolution-ledger.md L175 row P-2026-09-29-01 (CEO direct order verbatim:
"决策委员会去梳理一下，建立顶层节省云端token的机制" ~11:1x, ledger landing 11:21:09,
committee channel C-20260929-01 7/7 conditional-yes, token-economy.md v2.0 §8 four-clause
mechanism, rollback window to 10-06, revisit 10-07) + own-share R679 ack <=10min detection
after 11:21:09 ledger landing + R681 post-vote dispatch three-piece wiring (three-path gate
mandate + attribution mirror + weekly cloud line).
Em budget ladder machine check with ZERO-MARGIN EXCLUSION (R293/R310) + vertical stack
budget law (R381): stack bottom <= subs top - 20px.
Template = DIGEST v9 cards.json. All output UTF-8.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
V9 = os.path.join(BASE, "MC-20260928-DIGEST-v9")
V10 = os.path.join(BASE, "MC-20260929-DIGEST-v10")
TMP = V10 + "-tmp"
os.makedirs(V10, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

cfg = json.load(io.open(os.path.join(V9, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市盘点 010",
    u"云端 token 机制令 2026-09-29 落账 11:21:09",
    u"「决策委员会去梳理一下，建立顶层节省云端token的机制」",
    u"审计 5 日窗 206 计费任务 · 生成面 98% · 推理面零云",
    u"三缺口：记账无聚合 · 三径未升格 · 在册未在役",
    u"机制四款：记账律 · 三径闸 · 效率律 · 判据回访",
    u"委员会 7/7 有条件赞成 · 否决窗至 10-06",
    u"全司三径闸接线 · 本司 ack ≤10 分钟 · 回访 10-07",
]

SUBS_LINE = u"基于硅基城市真实事件（云端机制令台账档案）"

frame_w = cfg["video"]["width"]
h1_size = cfg["font"]["h1_size"]
subs_size = cfg["font"]["subs_size"]
LADDER = [50, 46, 44, 40, 36, 32, 28, 26, 24]
MARGIN_EM = 0.2  # zero-margin exclusion law (em-budget-ladder hard law; R293 pixel-overlap lesson)

# --- vertical stack budget (R381 hard law; model from measured v2/v3 bands)
H1_GAP = int(cfg["font"]["h1_gap"])          # 36
OPT_C = float(cfg["font"]["optical_center"])  # 0.24
SUBS_TOP = cfg["video"]["height"] - int(cfg["font"]["subs_bottom"])  # y=970
PITCH_F = 1.35   # conservative vs measured 1.318
GAP_MIN = 20     # px clearance to subs band


def stack_bottom(size, n):
    pitch = PITCH_F * size + 12
    h2_h = size + (n - 1) * pitch
    return cfg["video"]["height"] * OPT_C + H1_GAP + 1.5 * h2_h


def all_fit(size):
    budget = (frame_w - 160) / float(size)
    for ln in LINES[1:]:
        if _line_cost(ln) > budget - MARGIN_EM or len(wrap_for_width(ln, size, frame_w).split("\n")) != 1:
            return False
    return stack_bottom(size, len(LINES) - 1) <= SUBS_TOP - GAP_MIN


H2_SIZE = next(s for s in LADDER if all_fit(s))

meta = cfg["meta"]
meta["topic"] = "MC-20260929-DIGEST-v10"
meta["form"] = (u"DIGEST 盘点图文 010（hit-chain v1.0 全链审查留痕·P0 形态 DIGEST 续件第九件·"
                u"#67 触发律=ledger 新 CEO 令级事件落账随轮领+queue §E 批活池 E2 领做〔C-20260929-02 B 款 lane·R681 立池〕·"
                u"史源=P-2026-09-29-01 决策委员会云端 token 节省机制梳理案正行+本司 R679 ack+R681 票后派发三件落地双锚）")
meta["source_facts"] = (u"云端 token 机制令数字盘点八条："
                        u"①「云端 token 机制令 2026-09-29 落账 11:21:09」=cph4/evolution-ledger.md L175 P-2026-09-29-01 正行"
                        u"（CEO 直令原话 verbatim「决策委员会去梳理一下，建立顶层节省云端token的机制」~11:1x·T1 委员会通道·"
                        u"11:21:09 ledger 落账〔r679 探针 mtime 机证〕·委员会通道强制过会〔council §三①〕"
                        u"+同窗收口授权〔C-20260928-02 范式〕）／"
                        u"②引文行「决策委员会去梳理一下，建立顶层节省云端token的机制」=CEO 原话 verbatim 全句直引"
                        u"（正行原句零改字零重组·24 全角+5 拉丁=h2_size 32 档驱动行）／"
                        u"③「审计 5 日窗 206 计费任务 · 生成面 98% · 推理面零云」=正行消耗实况（P-09 executed·窗 09-23→09-27·±10）："
                        u"≈206 计费任务·生成面 98%（他司分布=批级知悉位不入卡面）·推理面零云（本地栈+U218 见效）——"
                        u"**用量细节脱敏处置**：配额 100/日·单日峰值 45-50·72 单待泄洪=token 用量细节仅档 source_facts 不入卡面"
                        u"（v9 GPU>70% 指标同型处置·206/98%/零云=治理审计读数入卡面分界）／"
                        u"④「三缺口：记账无聚合 · 三径未升格 · 在册未在役」=正行云端面三缺口短标签压缩"
                        u"（全称：①记账无集团聚合面②生成面三径未升格集团执法〔单日 45-50/100 常态化〕③正典在册≠机制在役）"
                        u"+CEO 五连令（09-23/24/25/27/28+本令）=实况优先信号／"
                        u"⑤「机制四款：记账律 · 三径闸 · 效率律 · 判据回访」=token-economy.md **v2.0 §八 云端节省机制** 四款"
                        u"（8.1 云端记账统一律/8.2 生成面三径闸升格/8.3 效率与后果/8.4 预注册判据 5 条·判据回访 10-07 治理日"
                        u"与 P-19 替代率首报同窗）／"
                        u"⑥「委员会 7/7 有条件赞成 · 否决窗至 10-06」=FluxGroup/docs/decisions.md C-20260929-01 记名归档行"
                        u"（七席独立意见 7/7 有条件赞成·全员附款随案生效·CEO 翻案权保留·否决窗至 10-06·跨仓只读）／"
                        u"⑦「全司三径闸接线 · 本司 ack ≤10 分钟 · 回访 10-07」=正行转办③@全司三件（三径闸 mandate 接线"
                        u"+attribution 单字段发射前必填+周轮云端行聚合=票后派发）+本司实况双锚：R679 ack 判读"
                        u"〔11:21:09 落账→轮首检出 ≤10 分钟·backlog #89〕+R681 票后派发三件落地〔iteration_prompt.txt "
                        u"Token 纪律行+data/cloud-attribution.json 本司份额镜像+weekly_report.py CLOUD_LINE 周报云端行聚合器〕"
                        u"+本司推理面零云实况〔TTS edge-tts 本地链+ASR faster-whisper+Ollama 评审席+FFmpeg 渲染全本地"
                        u"·P-20260925-12 回执「已是现状切换计划 N/A」在案〕／⑧底部行=虚实级+来源级标注")
meta["source_pointer"] = (u"cph4/evolution-ledger.md L175 P-2026-09-29-01 正行（集团进化台账·CEO 直令原话 verbatim+三缺口+"
                           u"消耗实况+机制四款+转办三件全录·跨仓只读）+FluxGroup/docs/decisions.md C-20260929-01 行"
                           u"（委员会记名归档 7/7 有条件赞成·token-economy v2.0 §八 立法面·跨仓只读）"
                           u"+cph4/council/C-20260929-01-bill.md（证据包·消耗实测窗与四款判据正源·跨仓只读）"
                           u"+src/os/backlog.md #89 行（本司 R679 收令+ack 判读 ≤10 分钟+R681 票后派发三件落地注记·P-51 送达链）"
                           u"+docs/self-improvement-queue.md §E 批活池 E2 行（lane 三验字段·C-20260929-02 B 款）"
                           u"+data/cloud-attribution.json（本司份额镜像·R681 落件）+src/os/state.json R679/R681 log"
                           u"+git commit cbb99dc（R681 收官 commit·P-51 送达判据链）——"
                           u"编年史 A 级史源（集团进化台账+集团决策正典+本司台账·charter §3 选题池多源）·一料多吃（charter §3）")
meta["attribution_rule"] = (u"署名=纪实线编年史档案级（charter §2.1 纪实线·无居民名面=零虚构署名·人设权红线照守；"
                             u"引文=CEO 原话 verbatim 全句〔「决策委员会去梳理一下，建立顶层节省云端token的机制」=正行原句零改字零重组·"
                             u"CEO 令全文 verbatim 入 source_facts〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「基于硅基城市真实事件（云端机制令台账档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"叙事包装=云端 token 机制令数字盘点档案体（1 句 CEO 直令 vs 当日委员会 7/7 过会+机制正典 v2.0 §八 "
                            u"四款落地+全司接线三件=「要节省」母题·审计三读数〔206 计费任务/98% 生成面/推理面零云〕=令的必要性证据位·"
                            u"三缺口→四款=「问题→立法」递进链·全司接线=落地兑现位·回访 10-07=悬念收束位·"
                            u"推理面零云=本地栈见效金句位；公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限）")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 数字反差链：1 句 CEO 直令 vs 当日委员会 7/7 过会+机制正典 v2.0 §八 "
                          u"四款+全司三径闸接线+本司 ack ≤10 分钟——F-042 v2 对照数字结构同源第九证·九连母题〔v2 开闸/v3 三线/"
                          u"v4 技能/v5 节目重制/v6 对账夜/v7 商业化定价日/v8 委员会成立日/v9 自驱力生态令/v10 云端 token 机制日〕"
                          u"+3 缺口/4 款/5 判据/7/7/≤10 分钟/10-07 六组数字/情 1 AI 自治省钱机制吃瓜温和如实非强极点"
                          u"〔G5 吃瓜未来党+G1 AI 效率实操党双群对位·云端节省=AI 公司自我治理叙事面〕/"
                          u"时 2 事件 2026-09-29 当日〔CEO 直令 ~11:1x→11:21:09 ledger 落账→本司轮首检出 ≤10 分钟 ack R679→"
                          u"12:00 委员会过会 C-20260929-01→本司 R681 票后派发三件落地→本件盘点〕/"
                          u"台 2 公众号方图承载=MC-001~055 S3 实证复用·盘点=公众号主流图文格式〔O-1327 research §2 #2 A 级通识〕）"
                          u"——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·R379 研究件 §5 判据锚定（编年史 A 级事件+数字密度）·"
                          u"#67 触发律=ledger 新 CEO 令级事件落账时随轮领+queue §E 批活池 E2（R681 立池·C-20260929-02 lane mandate）")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；脱敏律核=token 用量细节不入卡面"
                     u"（配额 100/日·单日峰值 45-50·72 单待泄洪=用量细节仅档 source_facts〔v9 GPU 指标同型处置〕·"
                     u"206 计费任务/98% 生成面/推理面零云=治理审计读数〔集团正典已落档口径〕入卡面分界）；"
                     u"P1 边界=本件=纪实档案非提案非表决（三径闸执行面=集团 mandate 接线纪实非本司自评宣传）；"
                     u"他司执行面细节不入卡面（生成面 98% 他司分布=批级知悉位·SDXL/Bonsai 本地产能件=他司执行细节不入）；"
                     u"成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DIGEST 形态第十件·charter v1.2 §4 形态码·编年史事件候选随轮领）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 3.0

# --- machine em check (R301-R313 precedent + R381 vertical law, renderer truth, assert-in-build)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append(u"H1 size %d budget %.2fem | H2 size %d budget %.2fem (ladder pick, zero-margin exclusion margin>=%.1fem)" % (h1_size, budget_h1, H2_SIZE, budget_h2, MARGIN_EM))
vb = stack_bottom(H2_SIZE, len(LINES) - 1)
report.append(u"VERT stack bottom est %.0fpx vs subs top %dpx gap %+.0fpx (need >=%dpx) (R381 vertical law)" % (vb, SUBS_TOP, SUBS_TOP - vb, GAP_MIN))
assert SUBS_TOP - vb >= GAP_MIN, "vertical stack budget FAIL"
for ln in LINES:
    cost = _line_cost(ln)
    size = h1_size if ln is LINES[0] else H2_SIZE
    budget = budget_h1 if ln is LINES[0] else budget_h2
    single = len(wrap_for_width(ln, size, frame_w).split("\n")) == 1
    margin = budget - cost
    fits = margin >= (0.0 if ln is LINES[0] else MARGIN_EM)
    ok = ok and single and fits
    report.append(u"%-6.2fem  budget %-6.2fem  margin %+-5.2fem  single=%s  %s" % (cost, budget, margin, single, ln))
subs_cost = _line_cost(SUBS_LINE)
subs_budget = (frame_w - 160) / float(subs_size)
report.append(u"subs   %-6.2fem  budget %-6.2fem  margin %+-5.2fem  %s" % (subs_cost, subs_budget, subs_budget - subs_cost, SUBS_LINE))
ok = ok and subs_cost <= subs_budget
report.append("EM_CHECK: " + ("ALL OK" if ok else "FAIL"))
io.open(os.path.join(TMP, "em-check-r682.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V10, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V10, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:03,000\n" + SUBS_LINE + "\n")
print("BUILD OK h2_size=%d" % H2_SIZE)
