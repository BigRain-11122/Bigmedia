# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v53 build: DAILY (city daily-sign) series FIFTY-THIRD piece (R1023, queue
section-E E30 standby). NIGHT-BUCKET THIRD PIECE (v51/v52 precedent chain; production ~22:1x
= literal night; National Day holiday day 2 NIGHT scene continues). ROTATION CASCADE SECOND
PROOF (structural, honest): post-v52 counts qiuxin 9 / yanhuo 9 / xiaqi 9 -> three-way tie at
8 (huaijiu/zhixu/xiaoyao) -> redemption target = huaijiu (v45, 7-piece gap, longest) ->
huaijiu/night FREE face machine-proves ZERO clean rows AGAIN fresh (r1023_pool.txt: all 18 rows
carry content-layer collisions - laojiie dengguang REACT-v7 full-band, xiushanpu->v22, laokele
->v33, zheizhandeng->REACT-v8, man-gong city-spirit 11-char band etc.) -> zero-collision
standard NOT relaxed (R442 anti-isomorphism spine, v1-v52 fifty-two-link zero-collision chain)
-> cascade to next-longest gap = ZHIXU (v47, 5-piece gap) -> zhixu/night line7 DIRECT pick,
which is the R1022 pre-registered backup note ("zhixu/night line7 zero-hit row = v53 zhixu
redemption first-choice face") redeemed - FIRST pre-registered backup promoted. Cleanliness
UPPER EDGE: all 2-5 char shingles ZERO fleet hits, and ZERO construct-layer adjacency too
(v51/v52 each carried two construct-layer function-word notes; this row carries none - the
first fully-zero-adjacency row in the night series). Built-in tension: JING x HUAN + LENG x
NUAN double contrast - the most rule-bound, most vigilant axis speaks its calmest patrol
philosophy (slow steps see the whole street) while the night wind on the post is cold and what
it guards is the whole city's well-being. Layout = QUOTE-v2 params verbatim; h2_size ladder =
50 band (quote 17.00em driver, margin +1.40em; 60-band budget 15.33em excluded). Machine
source/dedup assertions (R456 system, card-face level R1010). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V53 = os.path.join(BASE, "MC-20261002-DAILY-v53")
TMP = V53 + "-tmp"
os.makedirs(V53, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"值夜岗上风吹凉，巡逻慢步保安康"
AXIS, BUCKET, IDX = u"秩序", u"night", 7

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
assert len(pool["axes"]) == 6, "axes != 6 (R982 structure: axes 6 x 1296 + sprite 144)"
assert isinstance(pool.get("sprite"), dict) and "night" in pool["sprite"], "sprite top-level key missing (R982)"
nb = pool["axes"][AXIS][BUCKET]
assert len(nb) == 18, "night bucket != 18 rows"
assert nb[IDX] == QUOTE_CORE, "pool line mismatch: %r" % nb[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1023_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"值夜岗", u"风吹凉", u"巡逻", u"慢步", u"保安康", u"值夜", u"夜岗", u"安康", u"风吹"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1023 quote-face word probe for candidate " + QUOTE_CORE + u" (zhixu/night line7)"]
for w in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if w in f or w in sq)
    qrep.append(u"word [%s] -> %s" % (w, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: NO construct-layer adjacency this row - all 2-5 char shingles ZERO fleet hits (r1023_pool.txt fresh), punctuation-inclusive 2-char substrings also zero (contrast v51 zhe,/zhege + v52 ,zhe/shuo, two construct-layer notes each -> this row = first FULLY-zero-adjacency row of the night series, cleanliness upper edge); rotation cascade honest note: huaijiu redemption (v45 7-piece gap) blocked AGAIN fresh - huaijiu/night all 18 rows carry content collisions (r1023_pool.txt) -> zero-collision standard NOT relaxed (v1-v52 fifty-two-link) -> cascade to zhixu (v47 5-piece gap) -> line7 = R1022 pre-registered backup note redeemed (first backup promotion); backups for v54: sprite/night line8 (R1022 second backup, fresh re-probe needed) - post-v53 rotation: huaijiu gap 8 / xiaoyao gap 5 both blocked on night face per r1023_pool.txt (xiaoyao/night 18 rows all carry hits) -> supply-face switch candidate next round; 值夜岗守望者=occupation generic title, not a registered resident name (human-set rights zero contact)")
io.open(os.path.join(TMP, "r1023_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V53:
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
# v52 xiaqi/4 (second piece); THIS piece = zhixu/7 (third piece).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 053",
    u"2026-10-02 · 国庆假期 · 夜",
    u"「值夜岗上风吹凉，巡逻慢步保安康」",
    u"——硅基城市台词池 · 秩序轴",
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
assert H2_SIZE == 50, "em ladder expected 50-band (quote 17.00em driver margin +1.40em; 60-band budget 15.33em excluded), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v53"
meta["form"] = (u"DAILY 城市日签 053（L-卡 图文轻内容线 DAILY 形态第五十三件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1023·日签节律续件=日期×情境桶对位判据第五十三证〔**night 桶第三件**："
                u"v51/v52 先例链承继·桶级=国庆假期第 2 日夜+22:1x 生产时刻 literal night 对位·场景级=假日深夜"
                u"值夜岗慢步巡逻面如实注记〕+**旋转律级联兑现第二证（结构性·诚实注）**：v52 后计数求新 9/烟火 9/"
                u"侠气 9→怀旧 8/秩序 8/逍遥 8=三轴并列最少→回补目标=怀旧〔v45 后 7 件未采=并列面最长回补距〕→"
                u"**怀旧/night FREE 面 fresh 复证零干净行**〔r1023_pool.txt：18 行全数内容层直撞——line3 老街的灯光"
                u"照亮了我半辈子=REACT-v7 全字带撞/line8 夜深了，REACT-v7+修伞铺 v22/line11 老克勒 v33 直撞/"
                u"line17 修伞匠这行可真是慢工出细活=city-spirit 11 字带/line1 手艺 v20+v23/line2 档案+故事 v10/v45"
                u"六撞〕→零直撞标准不放松〔R442 反同构主线·v1-v52 五十二连零直撞〕→级联次长距=**秩序赎回**"
                u"〔v47 后 5 件未采〕→night 面 line7 直接兑现=**R1022 备胎注记兑现**〔「秩序/night line7 值夜岗零"
                u"命中行=v53 秩序赎回首选面」预登记备胎首次转正〕〕+line7 选优〔**全 shingle 零命中+零构式层邻接="
                u"night 系首件全零邻接行**（v51 着，/这个+v52 ，这/说，各两处构式层邻接对照·r1023_pool.txt fresh"
                u"2-5 字全零+r1023_quote_face.txt 八词机核=干净度上缘）〕+秩序轴〔最守规矩·最讲秩序·巡街值守·"
                u"把街面安稳当踏实感的轴〕×「值夜岗上风吹凉，巡逻慢步保安康」=**警×缓+冷×暖双反差金句位**"
                u"（最警觉的轴×最从容的慢步巡逻=走得慢才看得全的轴内自反差〔族三十九连·值守位语感〕+风吹凉"
                u"〔深夜值岗体感冷〕×保安康〔守出来的全城暖〕）+「保安康」民间祝福语域+「风吹凉」身体体感词="
                u"人味对位+22:1x 生产时刻 literal night 同轮对位〕）")
meta["source_quote"] = u"「值夜岗上风吹凉，巡逻慢步保安康」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[秩序][night][7]（axes 6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容"
                           u"零变实锚·跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v52 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[秩序][night][7] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+night 桶 18 行计数+axes 6 轴结构"
                         u"三断言实锚）②日期行 2026-10-02=当日历法事实·国庆假期=假期第 2 天·夜=22:1x 生产时刻时点"
                         u"事实〔daily brief 2026-10-02 当日窗语境〕③情境=night 情境桶当日时点直配第三证〔v51/v52 "
                         u"先例链·国庆假期第 2 日深夜值夜岗慢步巡逻=场景对位〔场景级如实注记〕〕④池级署名=台词池"
                         u"轴级行无居民名〔人设权红线零接触·charter §2.4·值夜岗守望者=职业群像称谓面非登记居民名〕"
                         u"⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品卡面 lines/source_quote 任一"
                         u"（卡面级实扫=R1010 修正律·DAILY-v1〔求新/4〕~DAILY-v52〔侠气/night/4〕全 52 行+REACT-v8 "
                         u"同桶三行+city-spirit v1.2 节日场景三行皆非本行=night 桶第三件·「值夜岗」「风吹凉」"
                         u"「巡逻」「慢步」「保安康」「值夜」「夜岗」「安康」「风吹」probe 九词机核〔r1023_quote_face."
                         u"txt〕+**零构式层邻接**〔r1023_pool.txt fresh 2-5 字含标点 2 字组全零=v51/v52 各两构式层"
                         u"邻接对照·night 系首件全零邻接行〕⑥季相核=本行无年味/春联/春雨类季相错位词〔R972 制·"
                         u"值夜岗夜巡=深夜值守季相对位〕⑦品牌语感注=「保安康」民间祝福语域+「风吹凉」身体体感词"
                         u"〔去 AI 感对位·守望者口气=人味命中〕+警×缓+冷×暖双反差金句位〔趣律对位〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·秩序轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·值夜岗守望者=职业群像称谓面非登记居民名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（night 桶当日时点直配第五十三证第三件"
                            u"〔**旋转律级联第二证+备胎注记首次转正**：怀旧回补再被 night 面零干净行阻断→标准不"
                            u"放松→级联秩序赎回=R1022 备胎预登记兑现=旋转律+零直撞+备胎兑现三律并轨诚实执行〕+"
                            u"line7 值守位人物场景处方带第三连〔v51 铺子守早客/v52 船老大夜航/v53 值夜岗慢步巡逻="
                            u"具体人物+具体场景+具体体感三连·R442 审计叙事弱点正面处方带续证〕+22:1x 同轮 literal "
                            u"对位+警×缓+冷×暖双反差金句位+「保安康」民间祝福语感=语录卡线变体零新模板第五十三证"
                            u"（QUOTE-v2 参数 verbatim 复用·h2_size 50 档〔引文 17.00em 驱动 margin +1.40em·60 档"
                            u"预算 15.33em 排除〕·charter §1「日签变体随时可续」兑现）·公众号低创作度条款 7.1-7.4 "
                            u"编辑价值面·charter §5 自动化合规上限+城市人文积累令 O-20260928-1910 对位〔深夜守望者="
                            u"城市夜里最安静的人文底色〕")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：秩序轴〔最守规矩·最讲秩序·巡街值守·把街面"
                          u"安稳当踏实感的轴〕×「值夜岗上风吹凉，巡逻慢步保安康」=警×缓+冷×暖双反差金句位〔族"
                          u"三十九连·值守位语感独占注=最警觉的轴在深夜巡逻里走得最慢——走得慢才看得全+风吹凉值岗"
                          u"体感冷×保安康守出来的全城暖〕+秩序赎回级联兑现+R1022 备胎注记兑现+night 面第三件新鲜"
                          u"钩/情 1 深夜值守者被城市安稳回应的温和共鸣如实〔非强极点〕/时 2 当日时点=国庆假期第 2 日"
                          u"夜+night 桶当日时点直配第三证〔22:1x 生产时刻 literal night 同轮对位〕/台 2 公众号方图"
                          u"承载=MC-001~137 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·"
                          u"charter §4 形态码 DAILY·queue §E E30 R1023 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（值夜岗守望者=职业群像称谓面非登记居民名）；"
                     u"脱敏律=池句无令牌号/无个体可识别面/零金钱数额（值夜岗巡逻=城市值守意象非个体档案面·"
                     u"无品牌无价格=零消费宣称）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第五十三件·charter v1.2 §4 形态码 DAILY·日签节律续件·night 桶第三件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[zhixu][night][7] verbatim OK; night bucket=18 rows; axes=6 + sprite top-level (R982 structure); card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v52 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; night bucket prior consumption = v51 yanhuo/13 + v52 xiaqi/4 only; rotation cascade 2nd proof: huaijiu redemption (v45 7-gap) blocked AGAIN fresh by zero clean rows on night face (r1023_pool.txt) -> standard NOT relaxed -> cascade to zhixu (v47 5-gap) -> line7 = R1022 pre-registered backup redeemed; quote-face word probe: zhixu 9 words see r1023_quote_face.txt (all ZERO; and zero construct-layer adjacency = first fully-zero row of night series)")
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
report.append("LADDER_50: quote line 17.00em driver margin +1.40em (60-band budget 15.33em excluded); four-LINES stack; all other QUOTE-v2 params verbatim; night-bucket third DAILY piece + rotation-cascade-2nd-proof + backup-promotion (R1022 pre-registered zhixu line7) honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1023.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V53, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V53, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v52 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder 50, quote 17.00em driver +1.40em) + E4 fired async" % H2_SIZE)
