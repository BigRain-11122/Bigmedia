# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v50 build: DAILY (city daily-sign) series FIFTIETH piece (R1019, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 evening (built
20:5x) -> festival bucket direct match (fiftieth same-day proof, bucket-level; scene face =
holiday nightfall city-in-festive-dress stroll, honestly noted; NON-LAMP-FACE variation
honest note: no lamp character in this line - 夜幕挂新装 = city festive-dress generic =
anti-isomorphism variation FIFTH proof, second consecutive non-lamp piece after v49 generic-
colors swing). SUPPLY-FACE SWITCH (structural, R1018 pre-registration honored): post-v49
rotation counts qiuxin 9 / huaijiu 8 / xiaqi 8 / yanhuo 8 / zhixu 8 / xiaoyao 8 -> five-axis
tie at 8, redemption target = yanhuo (longest gap: v44 then v45-v49 five other-axis pieces) ->
yanhuo/festival FREE face machine-proven ALL-WEAK with ZERO clean rows (r1019_pool.txt:
line8 灯挂得真高 = v12 five-char verbatim direct; line11 菜场->v19 + 阿姨->v13 + 灯串->v25/v43
triple; line15 挂上灯笼 = v21 four-char + 喜庆->v19; line16 包子->v32 + 热腾->v44 same-axis
double; line17 灯笼可真 = v23 four-char + 节日的灯->v4 + 这节日->v28/v30 + 漂亮->v26; line0/6/14
nian-wei seasonal wording R972 law exclusion three rows) -> per R1018 pre-registration
("sprite festival 12 lines next-supply candidate") the supply face switches to the BigLife
sprite top-level festival bucket = SPRITE-FACE FIRST DAILY PIECE (seventh voice family opens;
P-20260926-13 city-creature order echo; BigLife R982 sprite top-level key, read-only). Six-
axis rotation counts freeze honestly noted (yanhuo redemption suspended pending pool growth).
Within sprite face content-strength pick documented (r1019_pool.txt machine-proven):
line6/line10 zero-shingle rows but 叮叮作响/铃响庆佳节 near-isomorphic pair mutually exclusive
+ 庆佳节 slogan-face weak scene (R442); line4 灯满街 lamp-motif band (v47/v48 lamp then v49/v50
non-lamp = weaker); THIS line0 = '叮叮当，夜幕挂新装' = content shingles ALL ZERO (叮叮当/夜幕/
挂新装/新装 each ZERO fleet card-face hits; sole maximal probe hit = '，夜' punctuation
artifact vs REACT-v8 different continuation - non-content collision honest note) + nightfall-
city-dress double scene layer (R442 prescription band) + build-moment match (20:5x evening =
夜幕 literal same-round timing) + onomatopoeia-family freshness: 喵呜 family consumed by
REACT-v3/v4/v5, 啾啾 family by REACT-v1/v2, 叮叮 family = fleet-zero first open (voice-level
freshness). Honest adjacency notes carried: 夜幕 vs v43 夜空 = same 夜-character family,
different word different construction (motif-layer single adjacency); 非灯面变奏第五证.
Built-in tension: SHENG x SHENG voice-vs-city self-contrast: the smallest creatures' bell
chime keeps time for the whole city putting on its biggest festive dress - living-city proof
= a city whose smallest voices chime along when it dresses up for its holiday is a city
alive enough to be celebrated (city humane-accumulation order echo + P-20260926-13 creature
order echo). Quote verbatim + card framing (R285 QUOTE precedent). Layout = QUOTE-v2 params
verbatim; h2_size ladder returns 60 band (quote line 11.00em short-driver + attribution
13.65em (城市生灵 four-char face) both inside 60-band budget 15.33em = v1-v28 band return;
v29/v49 50-band were 17.00em quote-line drivers). Machine source/dedup assertions (R456
system, card-face level R1010). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V50 = os.path.join(BASE, "MC-20261002-DAILY-v50")
TMP = V50 + "-tmp"
os.makedirs(V50, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"叮叮当，夜幕挂新装"
FACE, BUCKET, IDX = u"sprite", u"festival", 0

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
assert len(pool["axes"]) == 6, "axes != 6 (R982 structure: axes 6 x 1296 + sprite 144)"
sprite = pool["sprite"]
fest = sprite[BUCKET]
assert len(fest) == 12, "sprite festival bucket != 12 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1019_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"叮叮当", u"夜幕", u"挂新装", u"新装", u"叮叮", u"叮当", u"夜幕挂"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1019 quote-face word probe for candidate " + QUOTE_CORE + u" (sprite festival line0)"]
for w in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if w in f or w in sq)
    qrep.append(u"word [%s] -> %s" % (w, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: sole maximal shingle hit = '，夜' punctuation artifact vs REACT-v8 (different continuation, non-content collision); 夜幕 vs v43 夜空 = same 夜-char family different word different construction (motif-layer single adjacency); 叮叮 onomatopoeia family fleet-zero first open (喵呜 family = REACT-v3/v4/v5 consumed, 啾啾 family = REACT-v1/v2 consumed); sprite-face first DAILY piece = voice-level freshness")
io.open(os.path.join(TMP, "r1019_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V50:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        # card-face-level scan (R1010 corrected law): lines + source_quote; whole-file meta
        # narrative false hits do NOT count as consumption.
        assert QUOTE_CORE not in face and QUOTE_CORE not in sq, "line already consumed by %s" % d
# consumed festival lines (documented not asserted): resident six-axis face - DAILY-v1 qiuxin/4 +
# DAILY-v2 huaijiu/0 + DAILY-v3 xiaqi/5 + DAILY-v4 yanhuo/4 + DAILY-v5 zhixu/4 + DAILY-v6
# xiaoyao/3 + DAILY-v7 qiuxin/7 + DAILY-v8 xiaqi/13 + DAILY-v9 qiuxin/12 + DAILY-v10 huaijiu/3 +
# DAILY-v11 yanhuo/13 + DAILY-v12 xiaoyao/15 + DAILY-v13 xiaqi/2 + DAILY-v14 qiuxin/3 +
# DAILY-v15 qiuxin/11 + DAILY-v16 huaijiu/1 + DAILY-v17 zhixu/12 + DAILY-v18 xiaoyao/1 +
# DAILY-v19 yanhuo/3 + DAILY-v20 xiaqi/1 + DAILY-v21 zhixu/6 + DAILY-v22 huaijiu/12 +
# DAILY-v23 qiuxin/13 + DAILY-v24 yanhuo/2 + DAILY-v25 huaijiu/17 + DAILY-v26 xiaqi/10 +
# DAILY-v27 yanhuo/7 + DAILY-v28 zhixu/9 + DAILY-v29 xiaoyao/2 + DAILY-v30 zhixu/2 +
# DAILY-v31 xiaoyao/4 + DAILY-v32 yanhuo/10 + DAILY-v33 huaijiu/4 + DAILY-v34 xiaqi/9 +
# DAILY-v35 zhixu/11 + DAILY-v36 xiaoyao/16 + DAILY-v37 qiuxin/5 + DAILY-v38 yanhuo/5 +
# DAILY-v39 huaijiu/5 + DAILY-v40 xiaqi/11 + DAILY-v41 zhixu/17 + DAILY-v42 xiaoyao/13 +
# DAILY-v43 qiuxin/9 + DAILY-v44 yanhuo/1 + DAILY-v45 huaijiu/16 + DAILY-v46 xiaqi/7 +
# DAILY-v47 zhixu/15 + DAILY-v48 xiaoyao/5 + DAILY-v49 qiuxin/2 + REACT-v8 xiaoyao/17 +
# yanhuo/12 + zhixu/14 (source_facts) + city-spirit v1.2 festival-scene trio zhixu/16 +
# qiuxin/14 + xiaqi/0 (#47/#53/#59). Sprite face: ZERO prior consumption (this piece = first).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 050",
    u"2026-10-02 · 国庆假期",
    u"「叮叮当，夜幕挂新装」",
    u"——硅基城市台词池 · 城市生灵",
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
assert H2_SIZE == 60, "em ladder expected 60-band return (quote 11.00em short-driver + attribution 13.65em both inside 60-band budget 15.33em = v1-v28 band; v29/v49 were 17.00em quote drivers at 50), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v50"
meta["form"] = (u"DAILY 城市日签 050（L-卡 图文轻内容线 DAILY 形态第五十件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1019·日签节律续件=日期×情境桶对位判据第五十证〔festival 桶当日"
                u"直配系列化·桶级=节日情境与当日唯一对位·10-02=国庆假期第 2 日·场景级=假日夜幕降临城市盛装面"
                u"如实注记·20:5x 生产时刻=夜幕 literal 同轮对位〕+**供给面切换定谳（结构性·R1018 预登记兑现）**："
                u"旋转律 v49 后五轴并列 8 采（求新 9 单最多）→回补目标=烟火〔v44 后 5 件未采=并列面最长回补距〕"
                u"→烟火 festival FREE 面机核全弱零干净行〔r1019_pool.txt：line8 灯挂得真高=v12 五字 verbatim 直撞/"
                u"line11 菜场 v19+阿姨 v13+灯串 v25/v43 三重/line15 挂上灯笼 v21 四字+喜庆 v19/line16 包子 v32+"
                u"热腾 v44 同轴双撞/line17 灯笼可真 v23 四字+节日的灯 v4+这节日 v28/v30+漂亮 v26/line0/6/14 年味"
                u"季相 R972 排除三行〕→**sprite festival 面首件=第七声部首开**〔R1018 预登记「sprite festival "
                u"12 lines next-supply candidate」兑现·P-20260926-13 城市生灵族令承接·BigLife R982 sprite 顶层键"
                u"跨仓只读〕——六轴计数冻结如实注（求新 9/怀旧 8/侠气 8/烟火 8/秩序 8/逍遥 8·烟火回补悬置待池扩容）"
                u"+sprite 面选优〔line6/line10 零命中行但叮叮作响/铃响庆佳节近同构互斥+庆佳节口号化弱场景 R442/"
                u"line4 灯满街=灯 motif 带（v47/v48 灯面后弱新鲜度）/本行 line0=**内容 shingle 全零**〔叮叮当/夜幕/"
                u"挂新装/新装 全 ZERO·唯一极大连通命中=「，夜」标点伪命中 vs REACT-v8 异续字=非内容碰撞如实注〕+"
                u"夜幕挂新装=夜幕降临×城市节日盛装双场景层〔R442 审计叙事弱点处方带〕+20:5x 生产时刻夜幕对位〕+"
                u"声部级新鲜度〔拟声族谱：喵呜族=REACT-v3/v4/v5 已采·啾啾族=REACT-v1/v2 已采·**叮叮族=fleet 零消费"
                u"首开**〕+夜字 motif 层单邻接诚实注〔v43 夜空（灯串比星）vs 本行 夜幕（夜降临城盛装）=同字族异词"
                u"异构式〕+**非灯面变奏第五证**〔本行无灯字·夜幕挂新装=城市盛装泛称=v49 泛色彩面后第二连〕〕）")
meta["source_quote"] = u"「叮叮当，夜幕挂新装」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 sprite[festival][0]（axes 6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容"
                           u"零变实锚·跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v49 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 sprite[festival][0] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+sprite 桶 12 行计数+axes 6 轴结构"
                         u"三断言实锚）②日期行 2026-10-02=当日历法事实·国庆假期=假期第 2 天（daily brief 2026-10-02 "
                         u"当日窗语境）③情境=festival 情境桶当日直配（12 桶中节日情境与当日唯一对位·DAILY-v1~v49 "
                         u"同桶直配第五十证=日签节律判据系列化·国庆假期第 2 日夜幕降临全城盛装=假日夜晚城市盛装面"
                         u"场景对位〔场景级如实注记〕）④池级署名=台词池 sprite 行无居民名〔人设权红线零接触·charter "
                         u"§2.4·城市生灵=群像称谓面非登记居民名〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在"
                         u"全成品卡面 lines/source_quote 任一（卡面级实扫=R1010 修正律·DAILY-v1〔求新/4〕~DAILY-v49"
                         u"〔求新/2〕全 49 行+REACT-v8 同桶三行+city-spirit v1.2 节日场景三行皆非本行=sprite 面首件="
                         u"声部级新鲜度〔叮叮族 fleet 零消费首开·喵呜族 REACT-v3/v4/v5·啾啾族 REACT-v1/v2 已采族"
                         u"对照〕·「叮叮当」「夜幕」「挂新装」「新装」「叮叮」「叮当」「夜幕挂」probe 七词机核"
                         u"〔r1019_quote_face.txt〕⑥季相核=本行无年味/春联/春雨类季相错位词〔R972 制·夜幕/新装="
                         u"节日盛装季相对位〕⑦品牌语感注=「叮叮当」拟声口语真感〔去 AI 感对位·生灵轻快铃语="
                         u"趣律对位〕+城市生灵〔最微小声部〕×「夜幕挂新装」〔全城最大盛装时刻〕=小×大反差金句位"
                         u"〔最微小的生灵给全城盛装时刻打拍子=城市人文积累令 O-20260928-1910 对位+P-20260926-13 "
                         u"城市生灵族令承接〕")
meta["attribution_rule"] = (u"署名=池级+生灵级（台词池·城市生灵）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·城市生灵=群像称谓面非登记居民名非登记生灵名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第五十证+**供给面"
                            u"切换=sprite 第七声部首件**〔旋转律烟火回补目标 FREE 面全弱零干净行机核定谳→R1018 预登记"
                            u"sprite 供给面兑现·六轴计数冻结如实注〕+sprite 面选优〔line6/line10 近同构互斥+line4 灯带"
                            u"弱新鲜度排除后 line0 内容 shingle 全零胜出+双场景层+同轮夜幕时刻对位〕+叮叮拟声族 "
                            u"fleet 首开〔声部级新鲜度〕+「叮叮当，夜幕挂新装」〔最微小的生灵给全城盛装时刻打拍子〕"
                            u"小×大反差金句位+假日夜幕城市盛装场景层=R442 审计处方带续证+语录卡线变体零新模板第"
                            u"五十证（QUOTE-v2 参数 verbatim 复用·h2_size 60 档回归〔引文 11.00em 短行+署名 13.65em "
                            u"双入 60 档预算 15.33em=v1-v28 带回归·v29/v49 50 档=17.00em 长行驱动带对照〕·charter §1"
                            u"「日签变体随时可续」兑现）·公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规"
                            u"上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：城市生灵〔最微小声部〕×「夜幕挂新装」〔全城"
                          u"最大盛装时刻〕=小×大反差金句位+第七声部首件新鲜钩/sprite 供给面切换结构性选材/情 1 生灵"
                          u"轻快铃语=趣律对位温和萌趣面如实注〔非强极点〕/时 2 当日时点=国庆假期第 2 日夜+festival "
                          u"情境桶直配第五十证〔桶级·场景级假日夜幕城市盛装面·20:5x 生产时刻夜幕同轮对位〕/台 2 "
                          u"公众号方图承载=MC-001~134 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 "
                          u"production open·charter §4 形态码 DAILY·queue §E E30 R1019 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（城市生灵=群像称谓面非登记居民名/生灵名）；"
                     u"脱敏律=池句无令牌号/无个体可识别面/零金钱数额（夜幕城市盛装=公共城市景观意象非个体档案面·"
                     u"无品牌无价格=零消费宣称）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第五十件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: sprite[festival][0] verbatim OK; sprite festival bucket=12 lines; axes=6 (R982 structure); card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v49 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; sprite face = ZERO prior consumption = first piece; voice-level freshness: ding-ding onomatopoeia family fleet-zero first open (miao-wu family = REACT-v3/v4/v5, jiu-jiu family = REACT-v1/v2); quote-face word probe: ding-ding-dang/ye-mu/gua-xin-zhuang/xin-zhuang/ding-ding/ding-dang/ye-mu-gua see r1019_quote_face.txt (content shingles all ZERO; sole maximal hit = comma-artifact vs REACT-v8 non-content); supply-face switch: yanhuo redemption target FREE face all-weak zero clean rows machine-proven (line8 v12 five-char verbatim + line11 triple + line15 four-char + line16 double + line17 multi + seasonal x3), sprite face per R1018 pre-registration; six-axis counts frozen qiuxin9/huaijiu8/xiaqi8/yanhuo8/zhixu8/xiaoyao8 honest note)")
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
report.append("LADDER_RETURN_60: quote line 11.00em short-driver + attribution 13.65em (cheng-shi-sheng-ling four-char face) both inside 60-band budget 15.33em = v1-v28 band return; v29/v49 were 50-band 17.00em quote drivers; four-LINES stack; all other QUOTE-v2 params verbatim; non-lamp-face variation fifth proof + supply-face-switch honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1019.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V50, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V50, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v48/v49 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder return 60, quote 11.00em short-driver) + E4 fired async" % H2_SIZE)
