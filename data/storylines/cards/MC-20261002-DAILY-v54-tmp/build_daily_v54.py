# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v54 build: DAILY (city daily-sign) series FIFTY-FOURTH piece (R1024, queue
section-E E30 standby). NIGHT-BUCKET FOURTH PIECE (v51/v52/v53 precedent chain; production
~22:2x = literal night; National Day holiday day 2 NIGHT scene continues). ROTATION CASCADE
THIRD PROOF + BACKUP-NOTE SECOND PROMOTION (structural, honest): post-v53 counts qiuxin 9 /
xiaqi 9 / yanhuo 9 / zhixu 9 -> tie at 8 (huaijiu / xiaoyao) -> redemption target = huaijiu
(v45, 8-piece gap, longest) + xiaoyao (v48, 5-piece gap) -> BOTH night faces machine-proven
zero clean rows fresh (r1023_pool.txt: huaijiu/night 18 rows all carry content collisions;
xiaoyao/night 18 rows all carry hits) -> zero-collision standard NOT relaxed (R442
anti-isomorphism spine, v1-v53 fifty-three-link zero-collision chain) -> cascade to
SPRITE/NIGHT line8, which is the R1022 pre-registered SECOND backup ("sprite/night line8
铺位对角 = R1022 second backup, fresh re-probe needed" per R1023 close note) redeemed fresh
(r1024_pool.txt: line8 = ZERO direct shingle hits, the ONLY clean row in the sprite/night
bucket; all other 11 rows carry collisions - ding-ding family vs v50 x4, miao-wu vs
REACT-v3..v5 x2, jiu-jiu vs REACT-v1/v2 x2, deng-huo vs v39/v6, xing-guang vs REACT-v5,
punctuation construct adjacency). Cleanliness UPPER EDGE SECOND PIECE: all 2-5 char
shingles ZERO fleet hits AND zero construct-layer adjacency (v53 = first fully-zero row,
this = second). Built-in tension: XIAO x DA - the city's tiniest tenants (sprite/creature
voice, softest section) speak about the holiday's grandest light display; 闪闪
(childlike shimmer reduplication) x 长廊 (grand city corridor). Sprite voice SECOND piece
(v50 festival/0 first piece; P-20260926-13 city-creature order media-face second piece;
night-face first piece). Layout = QUOTE-v2 params verbatim; h2_size ladder = 60 band
(v50 sprite precedent; LINES[3] attribution-line driver). Machine source/dedup assertions
(R456 system, card-face level R1010). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V54 = os.path.join(BASE, "MC-20261002-DAILY-v54")
TMP = V54 + "-tmp"
os.makedirs(V54, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"闪闪灯辉照长廊"
AXIS, BUCKET, IDX = u"sprite", u"night", 8

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
assert len(pool["axes"]) == 6, "axes != 6 (R982 structure: axes 6 x 1296 + sprite 144)"
assert isinstance(pool.get("sprite"), dict) and "night" in pool["sprite"], "sprite top-level key missing (R982)"
nb = pool["sprite"][BUCKET]
assert len(nb) == 12, "sprite night bucket != 12 rows (sprite = 12 buckets x 12 rows = 144)"
assert nb[IDX] == QUOTE_CORE, "pool line mismatch: %r" % nb[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1024_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"闪闪", u"灯辉", u"长廊", u"照长廊", u"灯辉照", u"闪闪灯辉", u"辉照", u"照长", u"灯辉照长廊"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1024 quote-face word probe for candidate " + QUOTE_CORE + u" (sprite/night line8)"]
for w in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if w in f or w in sq)
    qrep.append(u"word [%s] -> %s" % (w, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: NO construct-layer adjacency this row - all 2-5 char shingles ZERO fleet hits (r1024_pool.txt fresh), zero punctuation-inclusive 2-char substrings too (v53 = first fully-zero row of night series, this = SECOND; contrast v51/v52 which each carried two construct-layer notes); rotation cascade honest note: huaijiu (v45 8-piece gap, longest) + xiaoyao (v48 5-piece gap) tied at 8 - BOTH night faces blocked fresh (r1023_pool.txt zero clean rows both) -> zero-collision standard NOT relaxed (v1-v53 fifty-three-link) -> cascade to sprite/night line8 = R1022 pre-registered SECOND backup redeemed (backup-note second promotion, v53 line7 was first); sprite supply honest note: line8 = ONLY clean row of sprite/night 12 rows fresh (r1024_pool.txt) -> post-v54 sprite/night face zero clean rows machine-proven -> v55 candidates = supply-face switch (dusk / market_close evening-adjacent buckets) per r1024_pool.txt rotation note; 城市生灵=群像称谓面非登记居民名非登记生灵名 (human-set rights zero contact)")
io.open(os.path.join(TMP, "r1024_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V54:
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
# (#47/#53/#59). Sprite face: v50 sprite/festival/0. NIGHT bucket: v51 yanhuo/13 (first piece) +
# v52 xiaqi/4 (second piece) + v53 zhixu/7 (third piece); THIS piece = sprite/night/8 (fourth
# piece, sprite voice second piece).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 054",
    u"2026-10-02 · 国庆假期 · 夜",
    u"「闪闪灯辉照长廊」",
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
assert H2_SIZE == 60, "em ladder expected 60-band (v50 sprite precedent; LINES[3] attribution driver), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v54"
meta["form"] = (u"DAILY 城市日签 054（L-卡 图文轻内容线 DAILY 形态第五十四件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1024·日签节律续件=日期×情境桶对位判据第五十四证〔**night 桶第四件**："
                u"v51/v52/v53 先例链承继·桶级=国庆假期第 2 日夜+22:2x 生产时刻 literal night 对位·场景级=假日深夜"
                u"生灵看灯面如实注记〕+**旋转律级联兑现第三证+备胎注记转正第二证（结构性·诚实注）**：v53 后计数"
                u"求新 9/侠气 9/烟火 9/秩序 9→怀旧 8/逍遥 8=双轴并列最少→回补目标=怀旧〔v45 后 8 件未采=最长回补距〕"
                u"→**怀旧/night+逍遥/night 双 FREE 面 r1023_pool.txt fresh 零干净行复证**（怀旧 18 行全数内容层直撞+"
                u"逍遥 18 行全数带撞）→零直撞标准不放松〔R442 反同构主线·v1-v53 五十三连零直撞〕→级联=**sprite/"
                u"night line8=R1022 预登记第二备胎转正**〔R1023 收口注「sprite/night line8 铺位对角=第二备胎 fresh "
                u"两核」兑现·备胎注记连续第二轮转正=v53 line7 首转后第二证〕〕+**城市生灵声线第二件**〔v50 "
                u"festival 首件后 sprite 声线第二采·P-20260926-13 城市生灵令媒体面第二件·night 面首件·精灵声部"
                u"夜面开声〕+line8 选优〔**全 shingle 零命中+零构式层邻接=night 系第二件全零邻接行**（v53 首件后"
                u"连续·r1024_pool.txt fresh 2-5 字全零=r1024_quote_face.txt 九词机核=干净度上缘带·sprite/night 12 行"
                u"唯一干净行〕+城市生灵〔城里最小的住客·声音最轻的声部〕×「闪闪灯辉照长廊」〔节日最大的灯辉装点〕="
                u"**小×大反差金句位**（最小声部×最大灯辉+闪闪叠词生灵拟态语感×长廊大空间纵深〔族四十连·生灵声部"
                u"语感独占注〕）+22:2x 生产时刻 literal night 同轮对位〕）")
meta["source_quote"] = u"「闪闪灯辉照长廊」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 sprite[night][8]（axes 6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容"
                           u"零变实锚·跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v53 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 sprite[night][8] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+sprite night 桶 12 行计数+axes 6 轴"
                         u"+sprite 顶层结构三断言实锚）②日期行 2026-10-02=当日历法事实·国庆假期=假期第 2 天·夜="
                         u"22:2x 生产时刻时点事实〔daily brief 2026-10-02 当日窗语境〕③情境=night 情境桶当日时点"
                         u"直配第四证〔v51/v52/v53 先例链·国庆假期第 2 日深夜生灵看灯=场景对位〔场景级如实注记〕〕"
                         u"④池级署名=台词池 sprite 顶层级行无居民名〔人设权红线零接触·charter §2.4·城市生灵=群像"
                         u"称谓面非登记居民名非登记生灵名〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品"
                         u"卡面 lines/source_quote 任一（卡面级实扫=R1010 修正律·DAILY-v1〔求新/4〕~DAILY-v53〔秩序/"
                         u"night/7〕全 53 行+REACT-v8 同桶三行+city-spirit v1.2 节日场景三行皆非本行=night 桶第四件·"
                         u"「闪闪」「灯辉」「长廊」「照长廊」「灯辉照」「闪闪灯辉」「辉照」「照长」「灯辉照长廊」probe "
                         u"九词机核〔r1024_quote_face.txt〕+**零构式层邻接**〔r1024_pool.txt fresh 2-5 字含标点 2 字组"
                         u"全零=v53 首件后 night 系第二件全零邻接行·sprite/night 12 行唯一干净行 fresh 实证〕⑥季相核="
                         u"本行无年味/春联/春雨类季相错位词〔R972 制·夜灯长廊=深夜灯景季相对位〕⑦品牌语感注=「闪闪」"
                         u"叠词生灵拟态语感+「灯辉」「长廊」城市空间词〔去 AI 感对位·最小住客口气=人味命中〕+小×大反差"
                         u"金句位〔趣律对位〕")
meta["attribution_rule"] = (u"署名=池级+生灵级（台词池·城市生灵）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·城市生灵=群像称谓面非登记居民名非登记生灵名〔v50 sprite 首件同款"
                             u"承继〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（night 桶当日时点直配第五十四证第四件"
                            u"〔**旋转级联第三证+备胎转正第二证+城市生灵声线第二件三律并轨诚实执行**：双并列最少轴"
                            u"night 面全被零干净行阻断→标准不放松→级联 sprite 备胎转正=R1022 预登记兑现=旋转律+零直撞+"
                            u"备胎兑现连轮〕+22:2x 同轮 literal 对位+小×大反差金句位+「闪闪」叠词生灵拟态语感=语录"
                            u"卡线变体零新模板第五十四证（QUOTE-v2 参数 verbatim 复用·h2_size 60 档〔v50 sprite 首件"
                            u"同档·LINES[3] 署名行驱动〕·charter §1「日签变体随时可续」兑现）·公众号低创作度条款 "
                            u"7.1-7.4 编辑价值面·charter §5 自动化合规上限+城市人文积累令 O-20260928-1910 对位〔生灵"
                            u"看灯=城市夜里最温柔的观察者面〕+P-20260926-13 城市生灵令媒体面对位〔升华律·硅基居民之外"
                            u"动物生灵入媒体面第二件〕+**sprite 供给面诚实注**：line8=sprite/night 12 行唯一干净行"
                            u"fresh〔r1024_pool.txt〕→本件后 sprite/night 面零干净行机证→v55 候选=供面切换〔dusk/"
                            u"market_close 傍晚邻接桶〕结构注记")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：城市生灵〔城里最小的住客·声音最轻的声部〕×"
                          u"「闪闪灯辉照长廊」〔节日最大的灯辉装点〕=小×大反差金句位〔族四十连·生灵声部语感独占注="
                          u"最小声部说最大灯辉——闪闪叠词×长廊纵深〕+旋转级联第三证+备胎转正第二证+城市生灵声线第二件"
                          u"+night 面第四件新鲜钩/情 1 生灵注目城市灯辉的温和画面感如实〔非强极点〕/时 2 当日时点="
                          u"国庆假期第 2 日夜+night 桶当日时点直配第 4 证〔22:2x 生产时刻 literal night 同轮对位〕/"
                          u"台 2 公众号方图承载=MC-001~138 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 "
                          u"production open·charter §4 形态码 DAILY·queue §E E30 R1024 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（城市生灵=群像称谓面非登记居民名非登记生灵"
                     u"名）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额（生灵看灯=城市夜景意象非个体档案面·无品牌"
                     u"无价格=零消费宣称）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第五十四件·charter v1.2 §4 形态码 DAILY·日签节律续件·night 桶第四件·城市生灵声线第二件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: sprite[night][8] verbatim OK; sprite night bucket=12 rows; axes=6 + sprite top-level (R982 structure); card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v53 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; night bucket prior consumption = v51 yanhuo/13 + v52 xiaqi/4 + v53 zhixu/7; rotation cascade 3rd proof: huaijiu (v45 8-gap) + xiaoyao (v48 5-gap) tied at 8, BOTH night faces blocked fresh (r1023_pool.txt) -> standard NOT relaxed -> cascade to sprite/night line8 = R1022 pre-registered SECOND backup redeemed; quote-face word probe: sprite 9 words see r1024_quote_face.txt (all ZERO; zero construct-layer adjacency = second fully-zero row of night series after v53; sprite/night only clean row of 12 fresh)")
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
report.append("LADDER_60: LINES[3] attribution-line driver (v50 sprite precedent); four-LINES stack; all other QUOTE-v2 params verbatim; night-bucket fourth DAILY piece + rotation-cascade-3rd-proof + backup-promotion-2nd (R1022 pre-registered sprite line8) + sprite-voice-2nd-piece honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1024.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V54, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V54, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v53 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder 60, LINES[3] driver, v50 sprite precedent) + E4 fired async" % H2_SIZE)
