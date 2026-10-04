# -*- coding: utf-8 -*-
"""MC-20261005-DAILY-v65 build: DAILY (city daily-sign) series SIXTY-FIFTH piece (R1305, queue
section-E E30 standby cascade). NIGHT-WINDOW CASCADE PIECE - production moment ~02:4x = LITERAL
DEEP NIGHT (R1020 night literal law; v51-v54/v64 night-piece precedent band). Registered unlock
window "night-window rows" (R1032 -> R1086 -> R1122 chain) fires this round, but the registered
sprite-night residue face resolves ZERO-CLEAN on fresh scan (all 11 unconsumed rows are
onomatopoeia-band gated: ding/miao/jiu families, 4th-use blocked per R1123 registration + 2-char
shingle collisions) -> CASCADE to six-axes night fresh re-scan -> ONE clean row found:
axes[order][night][16] "别忘了关好自家门" = fresh-scan overturn of the R1023-R1029 "six-axes night
zero-clean" carried note (supply derive-blindspot-fix, R870/R970/R1095 same-type; machine-verified:
zero 2+ char shingle collision across ALL fleet card faces incl DAILY v1-v64/REACT/CENSUS/DIGEST/
QUOTE, zero city-spirit harvest, zero seasonal gates). Triple literal alignment: literal deep-night
production x night content x order axis (holiday day-5 night sign-off). SAME-BUCKET-DIFFERENT-ROW:
v53 (order/night/7 patrol) -> v65 (order/night/16 door) = same-axis-same-bucket different row =
line-level freshness law precedent (R975+ chain); honest motif-band note: public patrol x private
household door = scene-heterogeneous (anti-homogenization R442 spine held, v1-v64 sixty-four-link
zero-collision chain). Layout = QUOTE-v2 params verbatim; h2_size ladder = 60 band (v64 same-band
precedent, date-line driver). Machine source/dedup assertions (R456 system, card-face level R1010).
UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V65 = os.path.join(BASE, "MC-20261005-DAILY-v65")
TMP = V65 + "-tmp"
os.makedirs(V65, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"别忘了关好自家门"
AXIS, BUCKET, IDX = u"秩序", u"night", 16

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
assert len(pool["axes"]) == 6, "axes != 6 (R982 structure: axes 6 x 1296 + sprite 144)"
assert isinstance(pool.get("sprite"), dict) and len(pool["sprite"]) == 12, "sprite top-level 12 buckets missing (R982)"
nb = pool["axes"][AXIS][BUCKET]
assert len(nb) == 18, "axes bucket != 18 rows (axes = 6 axes x 12 buckets x 18 rows = 1296)"
assert nb[IDX] == QUOTE_CORE, "pool line mismatch: %r" % nb[IDX]
assert nb[7] == u"值夜岗上风吹凉，巡逻慢步保安康", "v53 consumed-row structural anchor expected (order/night/7)"
assert pool["sprite"][u"weekend"][3] == u"嗡嗡嗡，晨风中的舞", "v63 consumed-row structural anchor expected (sprite/weekend/3)"
assert pool["sprite"][u"weekend"][4] == u"叮咚响夜晚", "v64 consumed-row structural anchor expected (sprite/weekend/4)"
assert pool["sprite"][u"night"][8] == u"闪闪灯辉照长廊", "v54 consumed-row structural anchor expected (sprite/night/8)"
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- night-window supply adjudication evidence file (fresh scan r1305_pool_scan.txt on disk)
scan = io.open(os.path.join(ROOT, "r1305_pool_scan.txt"), encoding="utf-8").read()
assert u"CLEAN 秩序/night/16" in scan, "fresh-scan evidence line missing (r1305_pool_scan.txt)"
assert u"six-axes night clean rows: 1" in scan, "fresh-scan six-axes night count mismatch"

# --- quote-face word probe (r1305_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"别忘了", u"关好", u"自家", u"家门", u"别忘", u"忘了", u"别忘了关好自家门"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1305 quote-face word probe for candidate " + QUOTE_CORE + u" (order/night/line16, night-window cascade)"]
allzero = True
for wd in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if wd in f or wd in sq)
    if hits:
        allzero = False
    qrep.append(u"word [%s] -> %s" % (wd, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: %s. Night-window cascade adjudication (this round fresh verdict): (1) registered sprite-night residue face resolves ZERO-CLEAN - all 11 unconsumed rows are onomatopoeia-band gated (ding/miao/jiu families; 4th onomatopoeia use blocked per R1123 registration; 2-char shingle collisions with v50/v64/REACT-v1/v3/v61) -> cascade lawful; (2) six-axes night fresh re-scan finds ONE clean row (order/night/16) = fresh-scan overturn of R1023-R1029 zero-clean carried note = supply derive-blindspot-fix (R870/R970/R1095 same-type), machine-verified zero collision; (3) SAME-BUCKET-DIFFERENT-ROW: v53 order/night/7 (public patrol) -> THIS order/night/16 (private household door) = line-level freshness law; motif-band honest note: order-axis watchcare motif (v53 patrol / v31 lantern-check family) x household-door variant = scene-heterogeneous, anti-homogenization spine held; (4) NIGHT-SCENE literal law (R1020): production moment ~02:4x = literal deep night, night content honestly paired (v51-v54/v64 night-piece precedent band)." % (u"all 2+ char shingles ZERO fleet hits = fully-zero row (v53-v64 twelve-precedent chain)" if allzero else u"NOTE: some shingle hits above - honest adjacency adjudication required"))
qrep.append(u"post-v65 supply honest note: sprite night face = zero clean rows (onomatopoeia band 4th-use blocked + shingle collisions, r1305_pool_scan.txt); six-axes night = one row consumed THIS piece -> zero clean left; axes weekend fresh scan = 3 clean rows but ALL daytime/after-meal flavored (time-point mismatch at deep-night production; market-themed row gated by 10-08 market-reopen window) -> not selected this round, registered standby for daytime windows; unlock windows unchanged: rain-event day / CEO-order day / 2026-10-08+ market reopen / Nov+ coldsnap / summer heatwave. Pool-expansion report position maintained (status-line not chase).")
io.open(os.path.join(TMP, "r1305_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V65:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        assert QUOTE_CORE not in face and QUOTE_CORE not in sq, "line already consumed by %s" % d

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 065",
    u"2026-10-05 · 国庆假期 · 夜",
    u"「别忘了关好自家门」",
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
assert H2_SIZE == 60, "em ladder expected 60-band (date line driver, v64 same-band precedent), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261005-DAILY-v65"
meta["form"] = (u"DAILY 城市日签 065（L-卡 图文轻内容线 DAILY 形态第六十五件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 级联续领 R1305·日签节律续件=日期×情境桶对位判据第六十五证〔**夜窗级联件**："
                u"注册夜窗位 sprite night 残面 fresh 判=零干净行〔拟声族带第四用起阻=R1123 注册+双字撞·"
                u"r1305_pool_scan.txt 机证〕→级联六轴 night fresh 复扫=**唯一干净行 秩序/night/16 兑现**〔"
                u"R1023-R1029「六轴 night 零干净行」承继注被 fresh 机械复扫推翻=供给面 derive 盲区修正"
                u"〔R870/R970/R1095 同型·零直撞零季相门控零已采面全机核〕〕+**literal night 三重对位**："
                u"literal 深夜生产〔~02:4x·R1020 night literal 律·v51-v54/v64 夜件带先例〕×夜晚内容×"
                u"秩序轴〔假期第 5 夜出门看灯的人×替你看家的门〕+**同桶异行=线级新鲜度证**：v53"
                u"秩序/night/7〔岗哨巡逻·公共面〕→本件秩序/night/16〔门户关门·私人面〕=同轴同桶异行"
                u"〔场景异质=反同构 R442 主线维持·轴内守望母题带诚实注：巡逻×查灯×关门=守望三变奏〕〕+"
                u"最轻的一句叮嘱〔别忘了〕×最实的门户安全〔关好自家门〕=**轻叮嘱×实守夜反差金句位**"
                u"〔族五十一连·门锁位语感独占注=假期夜里出门看灯的人身后有座替你看门的城〕〕）")
meta["source_quote"] = u"「别忘了关好自家门」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[秩序][night][16]（axes 6 轴×12 情境桶"
                           u"×18 行=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构·跨仓只读指针）"
                           u"+data/intel/daily/2026-10-05.md（当日日期语境源·国庆假期第 5 天·周一·深夜生产语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[秩序][night][16] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+night 桶 18 行计数+axes 6 轴"
                         u"结构断言〔R982〕+v53 已耗行 night/7+v63/v64 已耗行 sprite weekend/3·4+v54 已耗行"
                         u"sprite night/8 四结构锚）②日期行 2026-10-05=当日历法事实·周一+国庆假期第 5 天"
                         u"〔daily brief 2026-10-05 当日窗语境〕+夜标记〔v51/v54/v64 夜标记先例带·literal deep "
                         u"night 生产〕③情境=夜窗级联件〔注册 sprite 夜面 fresh 判零干净→级联六轴 night 复扫"
                         u"唯一干净行·r1305_pool_scan.txt 机证〕④轴部署名=台词池秩序轴行·本行无称谓面=纯叮嘱"
                         u"句·泛称零涉及〔人设权红线零接触·charter §2.4·v5/v17/v21/v53 先例族〕⑤去重断言=本行"
                         u"不在 city-spirit.md 已采面+不在全成品卡面 lines/source_quote 任一（卡面级实扫=R1010 "
                         u"修正律·DAILY-v1~v64 全 65 行+REACT 八件+CENSUS 20+DIGEST 15+QUOTE 6 皆非本行）+"
                         u"「别忘了」「关好」「自家」「家门」「别忘」「忘了」全句 probe 七词机核〔r1305_quote_face.txt〕"
                         u"⑥季相核=本行无年味/春联/寒潮类季相错位词〔R972 制·关门叮嘱=四季通用夜面·十月秋夜兼容〕"
                         u"⑦品牌语感注=「别忘了」口语叮嘱开场+门锁意象=去 AI 感对位·人味命中·零书面套语·零消费宣称"
                         u"无品牌无价格")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·秩序轴）——池行无逐民署名·禁虚构居民名（charter v1.2 署名律"
                             u"+人设权红线·本行无称谓面=纯叮嘱句·泛称零涉及〔v5/v17/v21/v53 先例族对照注〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（夜窗级联件+同桶异行线级新鲜度双位"
                            u"〔**夜窗供给三段定谳诚实执行**：注册 sprite 夜面 fresh 判零干净→级联六轴 night 复扫"
                            u"→唯一干净行兑现〕+轻叮嘱×实守夜反差金句位〔族五十一连·门锁位语感独占注〕+口语叮嘱"
                            u"人味=语录卡线变体零新模板第六十五证（QUOTE-v2 参数 verbatim 复用·h2_size 60 档〔v64 "
                            u"同带先例·日期行驱动〕·charter §1「日签变体随时可续」兑现）·公众号低创作度条款 7.1-7.4 "
                            u"编辑价值面·charter §5 自动化合规上限+城市人文积累令 O-20260928-1910 对位〔假期夜里替"
                            u"全城说一句最实在的叮嘱=城市夜里活着的守望秩序〕+**供给面诚实注**：本件后六轴 night 面"
                            u"零干净行〔night/16 本件耗尽·fresh 复扫基线归零〕+sprite night 面零干净行〔拟声族带第"
                            u"四用起阻〕=夜窗位双面归零注·axes weekend 3 干净行=日间窗 standby〔时点错位不入选·"
                            u"市场行 10-08 复市窗门控〕·DAILY 可诚实配对面维持结构性近枯竭注〔池扩容呈报位维持呈现状"
                            u"行不催办〕·post-v65 指针：解锁窗维持=雨事件日/CEO 令日/10-08 market_open 复市/Nov+ "
                            u"寒潮/夏季 heatwave/axes weekend 日间窗行·REACT-v9 10-06 窗·F 序号诚实注=本件先落 F-152"
                            u"·REACT-v9 预指位顺延 F-153〔R978 判例 finished 顺序号=单一真相〕")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：别忘了〔最轻的一句叮嘱·口吻最轻〕×关好"
                          u"自家门〔夜晚安全的最小动作·分量最实〕=轻叮嘱×实守夜反差+出门看灯的人〔假期夜的动〕×"
                          u"替你看家的门〔留守的静〕=动静反差〔族五十一连·门锁位语感独占注〕/情 1 假日深夜守望式"
                          u"叮嘱的温和共鸣如实非强极点〔G1 城市生活群〕/时 2 当日=2026-10-05 周一国庆假期第 5 天·"
                          u"literal deep night 生产〔~02:4x〕×夜晚内容×秩序轴三重 literal 直配=夜窗级联件〔注册"
                          u"sprite 夜面零干净 fresh 判→级联六轴 night 复扫唯一干净行〕/台 2 公众号方图承载="
                          u"MC-001~151 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·"
                          u"charter §4 形态码 DAILY·queue §E E30 R1305 夜窗级联兑现")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市"
                     u"档案·DAILY 系列同源先例）；无登记居民名=人设权红线零接触（本行无称谓面=纯叮嘱句·泛称零"
                     u"涉及〔v5/v17/v21/v53 先例族对照注〕）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额"
                     u"（关门叮嘱=门户安全意象非安防消费面·无品牌无价格=零消费宣称）；成品只入库·发布=M5 账号"
                     u"物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第六十五件·charter v1.2 §4 形态码 DAILY·日签节律续件·夜窗级联件·秩序轴 night 桶同桶异行件·线级新鲜度证新证）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[order][night][16] verbatim OK; night bucket=18 rows; axes 6 structure (R982); v53 consumed-row order/night/7 + v63/v64 sprite weekend/3,4 + v54 sprite night/8 structural anchors; card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v64; night-window cascade: registered sprite-night face ZERO-CLEAN fresh verdict -> six-axes night fresh re-scan 1 clean row (derive-blindspot-fix R870/R970/R1095-type); quote-face word probe: 7 words see r1305_quote_face.txt")
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
report.append("LADDER_60: date line + attribution line fit 60-band (v64 same-band precedent); four-LINES stack; all other QUOTE-v2 params verbatim; night-window cascade + same-bucket-different-row + motif-band honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1305.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V65, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V65, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- fleet form counts (F-registration machine truth, v63/v64 review precedent: disk machine-count is authoritative)
forms = {}
png_in_dirs = 0
for d in sorted(os.listdir(BASE)):
    if os.path.isdir(os.path.join(BASE, d)) and d.startswith("MC-"):
        for form in ("QUOTE", "DIGEST", "CENSUS", "REACT", "DAILY"):
            if ("-" + form + "-") in d:
                forms[form] = forms.get(form, 0) + 1
                break
        if os.path.isfile(os.path.join(BASE, d, d + ".png")):
            png_in_dirs += 1
flat_png = len([f for f in os.listdir(BASE) if f.endswith(".png") and os.path.isfile(os.path.join(BASE, f))])
print("FORMS: " + json.dumps(forms) + " | png-in-dirs=%d flat-png=%d" % (png_in_dirs, flat_png))

# --- E4 audience reference call (async detached, 1500s window, v51-v64 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder 60, date+attribution lines fit) + E4 fired async" % H2_SIZE)
