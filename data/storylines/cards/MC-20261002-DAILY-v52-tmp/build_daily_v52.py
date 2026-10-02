# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v52 build: DAILY (city daily-sign) series FIFTY-SECOND piece (R1022, queue
section-E E30 standby). NIGHT-BUCKET SECOND PIECE (v51 first-piece precedent; production ~22:0x
= literal night; National Day holiday day 2 NIGHT scene continues). ROTATION CASCADE (structural,
honest): post-v51 counts qiuxin 9 / yanhuo 9 / huaijiu 8 / xiaqi 8 / zhixu 8 / xiaoyao 8 ->
four-way tie at 8 -> redemption target = huaijiu (v45, 6-piece gap, longest) -> huaijiu/night
FREE face machine-proves ZERO clean rows (r1022_pool.txt fresh: all 18 rows carry content-layer
collisions - laojiu dengguang vs REACT-v7 6-char shingles, dangan->v10/v45, xiushanpu->v22,
laokele->v33, zheizhandeng->REACT-v8, etc.) -> zero-collision standard NOT relaxed (R442
anti-isomorphism spine, v1-v51 fifty-one-link zero-collision chain) -> cascade to next-longest
gap = XIAQI (v46, 5-piece gap) -> xiaqi/night line4 DIRECT pick: distinctive shingles
chuanlaoda/heshang/yexing/zuishi-changkuai ALL ZERO (r1022_pool.txt + r1022_quote_face.txt
machine-proven); sole adjacency = construct-layer function hits only: ",zhe"->v10/v2
(demonstrative+comma, v51 "zhege"->DIGEST-v11 same law) + "shuo,"->DIGEST-v3/v1 (speech-attribution
verb+comma construct) = two construct-layer hits, same count and same law as v51's accepted
"zhe,"/("zhege") pair - clean row per v51 precedent. Backup rows documented: zhixu/night line7
(zero-hit row, next-face v53 redemption candidate gap 4) + sprite/night line8 (zero-hit row).
Built-in tension: NAO x KUANG (crowd x open-water) - the loudest, crowd-loving, tavern-home axis
finds its peak joy in the quietest open river at night. Layout = QUOTE-v2 params verbatim; h2_size
ladder = 50 band (quote 16.00em driver, margin +2.40em = v40 exact-band precedent; 60-band budget
15.33em excluded). Machine source/dedup assertions (R456 system, card-face level R1010). All
output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V52 = os.path.join(BASE, "MC-20261002-DAILY-v52")
TMP = V52 + "-tmp"
os.makedirs(V52, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"船老大说，这河上夜行最是畅快"
AXIS, BUCKET, IDX = u"侠气", u"night", 4

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
assert len(pool["axes"]) == 6, "axes != 6 (R982 structure: axes 6 x 1296 + sprite 144)"
assert isinstance(pool.get("sprite"), dict) and "night" in pool["sprite"], "sprite top-level key missing (R982)"
nb = pool["axes"][AXIS][BUCKET]
assert len(nb) == 18, "night bucket != 18 rows"
assert nb[IDX] == QUOTE_CORE, "pool line mismatch: %r" % nb[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1022_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"船老大", u"河上", u"夜行", u"最是", u"畅快", u"河上夜行", u"最是畅快", u"老大"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1022 quote-face word probe for candidate " + QUOTE_CORE + u" (xiaqi/night line4)"]
for w in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if w in f or w in sq)
    qrep.append(u"word [%s] -> %s" % (w, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: ，这->DAILY-v10/v2 = demonstrative+comma construct layer (v51 这个->DIGEST-v11 same law, non-content); 说，->DIGEST-v3/DAILY-v1 = speech-attribution verb+comma construct layer (non-content); distinctive shingles 船老大/河上/夜行/最是/畅快/河上夜行/最是畅快/老大 ALL ZERO = zero-collision row per v1-v51 chain standard (v51 two-construct-hit accepted-row precedent); rotation cascade honest note: huaijiu redemption (v45 6-piece gap) blocked - huaijiu/night all 18 rows carry content collisions (r1022_pool.txt) -> zero-collision standard NOT relaxed -> cascade to xiaqi (v46 5-piece gap); backups: zhixu/night line7 (zero-hit, v53 redemption candidate), sprite/night line8 (zero-hit); 船老大=occupation generic title, not a registered resident name (船长 2-char collides CENSUS-v16 card face while 船老大 3-char=fleet ZERO=word-form distinctness positive case)")
io.open(os.path.join(TMP, "r1022_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V52:
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
# (#47/#53/#59). Sprite face: v50 sprite/festival/0. NIGHT bucket: v51 yanhuo/13 (first piece);
# THIS piece = xiaqi/4 (second piece).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 052",
    u"2026-10-02 · 国庆假期 · 夜",
    u"「船老大说，这河上夜行最是畅快」",
    u"——硅基城市台词池 · 侠气轴",
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
assert H2_SIZE == 50, "em ladder expected 50-band (quote 16.00em driver margin +2.40em = v40 exact-band precedent; 60-band budget 15.33em excluded), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v52"
meta["form"] = (u"DAILY 城市日签 052（L-卡 图文轻内容线 DAILY 形态第五十二件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1022·日签节律续件=日期×情境桶对位判据第五十二证〔**night 桶第二件**："
                u"v51 首件先例承继·桶级=国庆假期第 2 日夜+22:0x 生产时刻 literal night 对位·场景级=假日深夜河上"
                u"夜航面如实注记〕+**旋转律级联兑现（结构性·诚实注）**：v51 后计数求新 9/烟火 9/怀旧 8/侠气 8/"
                u"秩序 8/逍遥 8=四轴并列最少→回补目标=怀旧〔v45 后 6 件未采=并列面最长回补距〕→**怀旧/night "
                u"FREE 面机核零干净行定谳**〔r1022_pool.txt fresh：18 行全数内容层直撞——line3 老街的灯光照亮了"
                u"我半辈子=REACT-v7 6 字 shingle 全撞/line2 里藏着的 v10+档案 v10+故事 v45 三撞/line8 夜深了，"
                u"REACT-v7+修伞铺 v22+着灯 v18/line11 老克勒 v33 直撞/line14 这盏灯 REACT-v8+年，/line1 伞的"
                u"REACT-v1+手艺 CENSUS-v20+v23/line0 夜市 city-spirit/line16 故事 v45+藏着 v10/v45/line17 "
                u"city-spirit 慢工出细活 11 字带〕→零直撞标准不放松〔R442 反同构主线·v1-v51 五十一连零直撞〕→"
                u"级联次长距=**侠气回补**〔v46 后 5 件未采〕→night 面 line4 直接兑现〕+line4 选优〔distinctive "
                u"shingles 船老大/河上/夜行/最是畅快 全 ZERO·r1022_pool.txt+r1022_quote_face.txt 机核·仅 ，这→"
                u"v10/v2 指示代词构式+说，→DIGEST-v3/v1 言说动词逗号构式两处功能词构式层邻接诚实注=v51 着，/这个"
                u"两构式判例同律+备胎注记〔秩序/night line7 值夜岗零命中行=v53 秩序赎回首选面·sprite/night "
                u"line8 闪闪灯辉零命中行〕+船老大=职业群像称谓面〔船长 2 字直撞 CENSUS-v16 卡面而 船老大 3 字="
                u"fleet 零命中=词形区分正面例·人设权零接触〕〕+侠气轴〔最豪爽·嗓门最大·情义至重·酒馆是主场·"
                u"人堆里凑热闹的轴〕×河上夜行最是畅快〔最开阔最清静的独航之乐〕=闹×旷轴内自反差金句位+「船老大」"
                u"「最是畅快」豪爽口语真感=人味对位+22:0x 生产时刻 literal night 同轮对位〕）")
meta["source_quote"] = u"「船老大说，这河上夜行最是畅快」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[侠气][night][4]（axes 6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容"
                           u"零变实锚·跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v51 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[侠气][night][4] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+night 桶 18 行计数+axes 6 轴结构"
                         u"三断言实锚）②日期行 2026-10-02=当日历法事实·国庆假期=假期第 2 天·夜=22:0x 生产时刻时点"
                         u"事实〔daily brief 2026-10-02 当日窗语境〕③情境=night 情境桶当日时点直配第二证〔v51 首件"
                         u"先例·国庆假期第 2 日深夜河上夜航=场景对位〔场景级如实注记〕〕④池级署名=台词池轴级行无"
                         u"居民名〔人设权红线零接触·charter §2.4·船老大=职业群像称谓面非登记居民名〕⑤去重断言=本行"
                         u"不在 city-spirit.md 64 条已采面+不在全成品卡面 lines/source_quote 任一（卡面级实扫=R1010 "
                         u"修正律·DAILY-v1〔求新/4〕~DAILY-v51〔烟火/night/13〕全 51 行+REACT-v8 同桶三行+city-"
                         u"spirit v1.2 节日场景三行皆非本行=night 桶第二件·「船老大」「河上」「夜行」「最是」"
                         u"「畅快」「河上夜行」「最是畅快」「老大」probe 八词机核〔r1022_quote_face.txt〕+，这/说，"
                         u"两处功能词构式层邻接诚实注〔v51 着，/这个同律〕⑥季相核=本行无年味/春联/春雨类季相"
                         u"错位词〔R972 制·河上夜航=深夜夜航季相对位〕⑦品牌语感注=「船老大」「最是畅快」豪爽口语"
                         u"真感〔去 AI 感对位·江上人家口气=人味命中〕+侠气轴〔酒馆是主场的豪爽轴〕×「河上夜行"
                         u"最是畅快」〔最爱热闹的轴在深夜空河上说出最畅快〕=闹×旷反差金句位〔趣律对位〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·侠气轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·船老大=职业群像称谓面非登记居民名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（night 桶当日时点直配第五十二证第二件"
                            u"〔**旋转律级联兑现**：怀旧回补被 night 面零干净行阻断→标准不放松→级联侠气回补="
                            u"旋转律+零直撞双律并轨诚实执行〕+line4 舟位人物场景处方带〔船老大深夜河上夜航="
                            u"R442 审计叙事弱点正面处方带续证·v20 船上信使=同域异面（信使忙不停送信面 vs 船老大"
                            u"夜行畅快面）·v12 看得见星星=夜空仰望面 vs 本行=河面夜航面〕+22:0x 同轮 literal 对位+"
                            u"闹×旷反差金句位+「船老大」「最是畅快」豪爽口语真感=语录卡线变体零新模板第五十二证"
                            u"（QUOTE-v2 参数 verbatim 复用·h2_size 50 档〔引文 16.00em 驱动 margin +2.40em=v40 "
                            u"同带先例·60 档预算 15.33em 排除〕·charter §1「日签变体随时可续」兑现）·公众号低"
                            u"创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：侠气轴〔最豪爽·酒馆是主场·人堆里凑热闹的轴〕"
                          u"×「河上夜行最是畅快」〔最开阔最清静的独航之乐〕=闹×旷轴内自反差金句位〔族三十八连·"
                          u"舟位语感独占注=把酒馆当家的人才说得出把深夜空河的夜航说成最畅快〕+侠气回补级联兑现+"
                          u"night 面第二件新鲜钩/情 1 深夜河上独航温和共鸣如实〔非强极点〕/时 2 当日时点=国庆假期"
                          u"第 2 日夜+night 桶当日时点直配第二证〔22:0x 生产时刻 literal night 同轮对位〕/台 2 "
                          u"公众号方图承载=MC-001~136 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 "
                          u"production open·charter §4 形态码 DAILY·queue §E E30 R1022 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（船老大=职业群像称谓面非登记居民名）；"
                     u"脱敏律=池句无令牌号/无个体可识别面/零金钱数额（河上夜航=江上劳作意象非个体档案面·"
                     u"无品牌无价格=零消费宣称）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第五十二件·charter v1.2 §4 形态码 DAILY·日签节律续件·night 桶第二件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[xiaqi][night][4] verbatim OK; night bucket=18 rows; axes=6 + sprite top-level (R982 structure); card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v51 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; night bucket prior consumption = v51 yanhuo/13 only; rotation cascade: huaijiu redemption (v45 6-gap) blocked by zero clean rows on night face (r1022_pool.txt) -> standard NOT relaxed -> cascade to xiaqi (v46 5-gap); quote-face word probe: 船老大/河上/夜行/最是/畅快/河上夜行/最是畅快/老大 see r1022_quote_face.txt (content shingles all ZERO; sole adjacency ，这->v10/v2 demonstrative + 说，->DIGEST-v3/v1 speech-verb-comma = construct-layer honest notes, v51 two-construct-hit precedent)")
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
report.append("LADDER_50: quote line 16.00em driver margin +2.40em (v40 exact-band precedent; 60-band budget 15.33em excluded); four-LINES stack; all other QUOTE-v2 params verbatim; night-bucket second DAILY piece + rotation-cascade (huaijiu blocked -> xiaqi) honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1022.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V52, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V52, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v51 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder 50, quote 16.00em driver +2.40em = v40 band) + E4 fired async" % H2_SIZE)
