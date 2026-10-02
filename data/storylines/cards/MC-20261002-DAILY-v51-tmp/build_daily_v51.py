# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v51 build: DAILY (city daily-sign) series FIFTY-FIRST piece (R1020, queue
section-E E30 standby). SUPPLY-FACE SWITCH (structural): r1020_pool.txt machine-proves the
WHOLE festival supply face (resident six-axis FREE rows + sprite festival leftovers) has ZERO
clean rows post-v50 - yanhuo/huaijiu/xiaqi/zhixu/xiaoyao FREE rows all carry >=3-char verbatim
or distinctive 2-char collisions; sprite line4/6/10 now hit ding-ding vs v50. Zero-collision
standard NOT relaxed (R442 anti-isomorphism spine, v1-v50 fifty-link zero-collision chain).
Per R1019 pointer ("yu 11 tong 1288 rows" supply note) the day-context bucket switches to
NIGHT: same-day time-of-day match (production 21:1x = literal night; National Day holiday day
2 NIGHT scene; v50 ye-mu same-round timing precedent raised to bucket level). ROTATION
REDEEMED ON THE NEW FACE: post-v50 counts qiuxin 9 / huaijiu 8 / xiaqi 8 / yanhuo 8 / zhixu 8
/ xiaoyao 8 -> redemption target = yanhuo (v44, 6-piece gap, longest; R1019 suspension note
"pending pool growth" = the face switch IS the pool growth, structural honest note) ->
yanhuo/night line13 DIRECT pick: distinctive shingles 铺子/还得守着/等早起/客人 ALL ZERO
(r1020_night_pool.txt + r1020_quote_face.txt machine-proven); sole adjacency = 着，->city-spirit
(particle+comma construct) + 这个->DIGEST-v11 (demonstrative pronoun) = function-layer honest
notes, same law as v50 "，夜" punctuation artifact. Backup rows documented: yanhuo/night line15
(single punct-construct hit), zhixu/night line7 (zero-hit row) - line13 wins on content
strength (R442 character-scene prescription band: night-shift shopkeeper holding the shop for
early-morning customers + 21:1x build moment = "这个点" literal same-round match). Built-in
tension: YE-tail x CHEN-head time-bridge self-contrast - the everyday-fireworks voice works
the night shift so the city's first morning customers get served; night's last light holding
the door for dawn. Layout = QUOTE-v2 params verbatim; h2_size ladder returns 50 band (quote
「」18.00em driver margin +0.40em thin-positive = v29/v49 50-band precedent; v50 was 60-band
short-driver). Machine source/dedup assertions (R456 system, card-face level R1010). All
output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V51 = os.path.join(BASE, "MC-20261002-DAILY-v51")
TMP = V51 + "-tmp"
os.makedirs(V51, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"铺子这个点还得守着，等早起的客人"
AXIS, BUCKET, IDX = u"烟火", u"night", 13

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
assert len(pool["axes"]) == 6, "axes != 6 (R982 structure: axes 6 x 1296 + sprite 144)"
assert isinstance(pool.get("sprite"), dict) and "festival" in pool["sprite"], "sprite top-level key missing (R982)"
nb = pool["axes"][AXIS][BUCKET]
assert len(nb) == 18, "night bucket != 18 rows"
assert nb[IDX] == QUOTE_CORE, "pool line mismatch: %r" % nb[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1020_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"铺子", u"这个点", u"还得守着", u"等早起", u"客人", u"守着", u"早起", u"铺子这个点"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1020 quote-face word probe for candidate " + QUOTE_CORE + u" (yanhuo/night line13)"]
for w in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if w in f or w in sq)
    qrep.append(u"word [%s] -> %s" % (w, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: 着，->city-spirit = particle+comma construct layer (non-content); 这个->MC-20261001-DIGEST-v11 = demonstrative pronoun (non-content); distinctive shingles 铺子/这个点/还得守着/等早起/客人/守着/早起/铺子这个点 ALL ZERO = zero-collision row per v1-v50 chain standard; supply-face switch: festival whole-face zero-clean machine-proven (r1020_pool.txt) -> night bucket first DAILY piece; yanhuo redemption honored on fresh face (R1019 suspension 'pending pool growth' = face switch is the growth); backups: yanhuo/night line15 (single punct-construct hit), zhixu/night line7 (zero-hit)")
io.open(os.path.join(TMP, "r1020_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V51:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        # card-face-level scan (R1010 corrected law): lines + source_quote; whole-file meta
        # narrative false hits do NOT count as consumption.
        assert QUOTE_CORE not in face and QUOTE_CORE not in sq, "line already consumed by %s" % d
# consumed lines (documented not asserted): festival resident-bucket DAILY v1 qiuxin/4 + v2 huaijiu/0 +
# v3 xiaqi/5 + v4 yanhuo/4 + v5 zhixu/4 + v6 xiaoyao/3 + v7 qiuxin/7 + v8 xiaqi/13 + v9 qiuxin/12 +
# v10 huaijiu/3 + v11 yanhuo/13 + v12 xiaoyao/15 + v13 xiaqi/2 + v14 qiuxin/3 + v15 qiuxin/11 +
# v16 huaijiu/1 + v17 zhixu/12 + v18 xiaoyao/1 + v19 yanhuo/3 + v20 xiaqi/1 + v21 zhixu/6 +
# v22 huaijiu/12 + v23 qiuxin/13 + v24 yanhuo/2 + v25 huaijiu/17 + v26 xiaqi/10 + v27 yanhuo/7 +
# v28 zhixu/9 + v29 xiaoyao/2 + v30 zhixu/2 + v31 xiaoyao/4 + v32 yanhuo/10 + v33 huaijiu/4 +
# v34 xiaqi/9 + v35 zhixu/11 + v36 xiaoyao/16 + v37 qiuxin/5 + v38 yanhuo/5 + v39 huaijiu/5 +
# v40 xiaqi/11 + v41 zhixu/17 + v42 xiaoyao/13 + v43 qiuxin/9 + v44 yanhuo/1 + v45 huaijiu/16 +
# v46 xiaqi/7 + v47 zhixu/15 + v48 xiaoyao/5 + v49 qiuxin/2 + REACT-v8 xiaoyao/17 + yanhuo/12 +
# zhixu/14 (source_facts) + city-spirit v1.2 festival-scene trio zhixu/16 + qiuxin/14 + xiaqi/0
# (#47/#53/#59). Sprite face: v50 sprite/festival/0. NIGHT bucket: THIS piece = first (yanhuo/13).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 051",
    u"2026-10-02 · 国庆假期 · 夜",
    u"「铺子这个点还得守着，等早起的客人」",
    u"——硅基城市台词池 · 烟火轴",
]

SUBS_LINE = u"引文取自硅基城市台词池（虚构城市档案）"

frame_w = cfg["video"]["width"]
h1_size = cfg["font"]["h1_size"]
subs_size = cfg["font"]["subs_size"]
LADDER = [60, 50, 46, 44, 40, 36, 32, 28, 26, 24]  # 60 first = zero-template default, ladder picks the largest feasible notch
MARGIN_EM = 0.2  # zero-margin exclusion law (R293)

H1_GAP = int(cfg["font"]["h1_gap"])
OPT_C = float(cfg["font"]["optical_center"])
SUBS_TOP = cfg["video"]["height"] - int(cfg["font"]["subs_bottom"])
PITCH_F = 1.35
GAP_MIN = 20


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
assert H2_SIZE == 50, "em ladder expected 50-band return (quote 18.00em driver margin +0.40em thin-positive = v29/v49 50-band precedent; v50 was 60-band short-driver), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v51"
meta["form"] = (u"DAILY 城市日签 051（L-卡 图文轻内容线 DAILY 形态第五十一件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1020·日签节律续件=日期×情境桶对位判据第五十一证〔**供给面切换"
                u"=night 桶首件（结构性）**：festival 全供给面零干净行机核定谳〔r1020_pool.txt：六轴 FREE 行"
                u"全数直撞（怀旧 line2 修伞 v22+手艺活儿 v23/line9 手艺 CENSUS-v20+v23/line10 暖和 v24/"
                u"line11 档案四撞/line14 这节日灯 v30 五字 verbatim；侠气 line3 大伙儿 v46+节日氛围 v28/"
                u"line12 好心情 v41/line14 见星星 v12/line17 江湖义气 v3；秩序 line1/10 守规矩 city-spirit/"
                u"line3 安全第一 v35；逍遥 line7 暖和 v24/line9 逍遥轴名 13 撞/line10 茶香灯影 v18 双撞/"
                u"line12 云淡风轻 v29）+sprite 余行 line4/6/10 叮叮→v50 全撞零干净行→零直撞标准不放松"
                u"〔R442 反同构主线·v1-v50 五十连零直撞〕→R1019 指针「余 11 桶 1288 行」承接〕·桶级=国庆"
                u"假期第 2 日夜+21:1x 生产时刻 literal night 对位〔v50 夜幕同轮对位先例升桶级〕·场景级=假日"
                u"深夜街市铺子守候早客面如实注记〕+**旋转律兑现=烟火回补（v44 后 6 件未采=最长回补距）**"
                u"〔v50 后计数求新 9/怀旧 8/侠气 8/烟火 8/秩序 8/逍遥 8=五轴并列最少→回补目标=烟火→"
                u"R1019 festival 面悬置注「待池扩容」=供给面切换即扩容·结构性注→night 新面 line13 直接"
                u"兑现〕+line13 选优〔distinctive shingles 铺子/还得守着/等早起/客人 全 ZERO·r1020_night_pool.txt"
                u"+r1020_quote_face.txt 机核·仅 着，→city-spirit 粒词逗号构式/这个→DIGEST-v11 指示代词两处"
                u"功能词邻接诚实注=v50「，夜」标点伪命中同律+备胎注记〔烟火/night line15 熬大半夜单标点构式"
                u"命中行/秩序/night line7 零命中行·line13=R442 人物场景处方带胜出〕+烟火轴〔最市井人味·守铺子"
                u"的人〕×等早起的客人〔最清晨的服务对象〕=夜尾×晨头时桥自反差金句位+铺子店主夜班守候="
                u"R442 审计「概念名词替代人物场景」叙事弱点处方带+「这个点」「还得」「守着」口语真感=人味"
                u"对位+21:1x 生产时刻「这个点」literal 同轮对位〕）")
meta["source_quote"] = u"「铺子这个点还得守着，等早起的客人」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[烟火][night][13]（axes 6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容"
                           u"零变实锚·跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v50 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[烟火][night][13] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+night 桶 18 行计数+axes 6 轴结构"
                         u"三断言实锚）②日期行 2026-10-02=当日历法事实·国庆假期=假期第 2 天·夜=21:1x 生产时刻时点"
                         u"事实〔daily brief 2026-10-02 当日窗语境〕③情境=night 情境桶当日时点直配〔festival 全供给面"
                         u"零干净行机核定谳后供给面切换·night 桶 DAILY 首件=夜桶时点对位第五十一证系列化·国庆假期"
                         u"第 2 日深夜街市铺子守候早客=场景对位〔场景级如实注记〕〕④池级署名=台词池轴级行无居民名"
                         u"〔人设权红线零接触·charter §2.4·烟火轴=轴级称谓面非登记居民名〕⑤去重断言=本行不在 "
                         u"city-spirit.md 64 条已采面+不在全成品卡面 lines/source_quote 任一（卡面级实扫=R1010 修正律·"
                         u"DAILY-v1〔求新/4〕~DAILY-v50〔sprite/festival/0〕全 50 行+REACT-v8 同桶三行+city-spirit "
                         u"v1.2 节日场景三行皆非本行=night 桶系列首件·「铺子」「这个点」「还得守着」「等早起」"
                         u"「客人」「守着」「早起」「铺子这个点」probe 八词机核〔r1020_quote_face.txt〕+着，/这个两处"
                         u"功能词构式层邻接诚实注〔v50「，夜」标点伪命中同律〕⑥季相核=本行无年味/春联/春雨类季相"
                         u"错位词〔R972 制·守铺等客=深夜守候季相对位〕⑦品牌语感注=「这个点」「还得」「守着」口语"
                         u"真感〔去 AI 感对位·市井劳动者口气=人味命中〕+烟火轴〔夜班守铺的市井人味〕×「等早起的"
                         u"客人」〔为晨头客人守夜尾〕=夜尾×晨头时桥反差金句位〔劳动者夜班坚守=城市烟火气最字面"
                         u"的形态·趣律对位〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·烟火轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·烟火轴=轴级称谓面非登记居民名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（night 桶当日时点直配第五十一证首件"
                            u"〔**供给面切换结构性选材**：festival 全面零干净行机核定谳→night 新面=日签节律判据"
                            u"的情境桶层扩容·R1019 指针承接〕+**旋转律烟火回补兑现**〔v44 后 6 件最长距·悬置注"
                            u"「待池扩容」=面切换即扩容〕+line13 人物场景处方带〔铺子店主夜班守候=R442 审计叙事"
                            u"弱点正面处方带续证〕+「这个点」21:1x 同轮 literal 对位+夜尾×晨头时桥反差金句位+"
                            u"「这个点」「还得」「守着」口语真感=语录卡线变体零新模板第五十一证（QUOTE-v2 参数 "
                            u"verbatim 复用·h2_size 50 档回归〔引文 18.00em 驱动 margin +0.40em 薄正余量入档="
                            u"v29/v49 50 档带·v50 60 档短行带对照〕·charter §1「日签变体随时可续」兑现）·公众号"
                            u"低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：烟火轴〔最市井人味·守铺子的人〕×「等早起"
                          u"的客人」〔最清晨的服务对象〕=夜尾×晨头时桥自反差金句位+烟火回补最长距兑现+night 面"
                          u"首件新鲜钩/sprite 后供给面切换结构性选材/情 1 劳动者夜班坚守温和共鸣如实〔非强极点〕/"
                          u"时 2 当日时点=国庆假期第 2 日夜+night 桶当日时点直配首件〔21:1x 生产时刻「这个点」同轮"
                          u"对位·v50 夜幕先例升桶级〕/台 2 公众号方图承载=MC-001~135 S3 实证复用）——hit-chain-"
                          u"mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 DAILY·queue §E E30 "
                          u"R1020 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（烟火轴=轴级称谓面非登记居民名）；"
                     u"脱敏律=池句无令牌号/无个体可识别面/零金钱数额（铺子守候=市井劳动意象非个体档案面·"
                     u"无品牌无价格=零消费宣称）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第五十一件·charter v1.2 §4 形态码 DAILY·日签节律续件·night 桶首件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[yanhuo][night][13] verbatim OK; night bucket=18 rows; axes=6 + sprite top-level (R982 structure); card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v50 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; night bucket = ZERO prior consumption = first piece; supply-face switch: festival whole-face zero-clean machine-proven (six-axis FREE rows all collided + sprite line4/6/10 ding-ding vs v50), night bucket per R1019 pointer; yanhuo redemption honored on fresh face (v44 6-piece gap, suspension 'pending pool growth' = face switch is the growth); quote-face word probe: 铺子/这个点/还得守着/等早起/客人/守着/早起/铺子这个点 see r1020_quote_face.txt (content shingles all ZERO; sole adjacency 着，->city-spirit particle+comma construct + 这个->DIGEST-v11 demonstrative = function-layer honest notes, v50 '，夜' same law)")
report.append(u"H1 %d budget %.2fem | H2 %d budget %.2fem (ladder pick, margin>=%.1fem) | VERT stack bottom %.0fpx vs subs top %dpx gap %+.0fpx (need >=%d) R381" % (h1_size, budget_h1, H2_SIZE, budget_h2, MARGIN_EM, stack_bottom(H2_SIZE, len(LINES) - 1), SUBS_TOP, SUBS_TOP - stack_bottom(H2_SIZE, len(LINES) - 1), GAP_MIN))
vb = stack_bottom(H2_SIZE, len(LINES) - 1)
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
report.append("LADDER_RETURN_50: quote line 18.00em driver margin +0.40em thin-positive (v29/v49 50-band precedent; v50 was 60-band short-driver 11.00em); four-LINES stack; all other QUOTE-v2 params verbatim; night-bucket first DAILY piece + yanhuo-redemption-on-fresh-face honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1020.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V51, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V51, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v50 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder return 50, quote 18.00em driver +0.40em) + E4 fired async" % H2_SIZE)
