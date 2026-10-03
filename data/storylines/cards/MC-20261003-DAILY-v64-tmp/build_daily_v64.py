# -*- coding: utf-8 -*-
"""MC-20261003-DAILY-v64 build: DAILY (city daily-sign) series SIXTY-FOURTH piece (R1123 night-window
round, queue section-E E30 night unlock). NIGHT-WINDOW UNLOCK PIECE - the pre-registered night line
sprite/weekend/4 "叮咚响夜晚" fires THIS round: triple chain of custody (R1032 unlock-window
registration "night-window rows (sprite/weekend/4 + night-bucket residue)" -> R1086 post-v63 supply
note "sprite weekend face remainder = weekend/4 night content (night-window only)" -> R1122
night-window candidate registration). Sunset ~17:37, render moment past sunset = LITERAL NIGHT
(R1020 night-content literal law; v51-v54 night-piece precedent band). Triple literal alignment:
literal-night production x night content x weekend bucket (Saturday + national-holiday day-3
evening). ONOMATOPOEIA BAND THIRD-USE FRESH VERDICT (R1122 registered discretion): v50 叮叮当 (bell,
festival night dress-up) + v63 嗡嗡嗡 (hum, morning dance) + THIS 叮咚 (doorbell, holiday night
visits) = three distinct sounds x three distinct scenes x three distinct buckets = third use LEGAL
per R1062 angling-band precedent (third use legal, fourth use blocked) -> post-v64 onomatopoeia 4th
use registered blocked. WEEKEND BUCKET: v63+v64 = new-run 2-link (four-peat law far). SPRITE VOICE
5th piece, weekend bucket 2nd within voice = the 4-distinct-bucket streak ends (v50/v54/v61/v63),
honest weaker-form registration (legal, no voice-repeat blocking law). Six-axes daytime depletion
carried (R1032/R1086); night-face residue honest note (six-axes night faces zero-clean per
R1023-R1029 scans; sprite night face residue = night-window position). Single shared char 叮 with
v50 叮叮当 = family/band layer adjacency, NOT a 2+ char shingle collision (honest note).
Zero-collision standard NOT relaxed (R442 spine, v1-v63 sixty-three-link chain). Layout =
QUOTE-v2 params verbatim; h2_size ladder = 60 band (v63 same-band precedent, date-line driver).
Machine source/dedup assertions (R456 system, card-face level R1010 law). UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V64 = os.path.join(BASE, "MC-20261003-DAILY-v64")
TMP = V64 + "-tmp"
os.makedirs(V64, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"叮咚响夜晚"
VOICE, BUCKET, IDX = u"sprite", u"weekend", 4

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
assert len(pool["axes"]) == 6, "axes != 6 (R982 structure: axes 6 x 1296 + sprite 144)"
assert isinstance(pool.get("sprite"), dict) and len(pool["sprite"]) == 12, "sprite top-level 12 buckets missing (R982)"
wb = pool["sprite"][BUCKET]
assert len(wb) == 12, "sprite bucket != 12 rows (sprite = 12 buckets x 12 rows = 144)"
assert wb[IDX] == QUOTE_CORE, "pool line mismatch: %r" % wb[IDX]
assert wb[3] == u"嗡嗡嗡，晨风中的舞", "v63 consumed-row structural anchor expected (sprite/weekend/3)"
assert pool["sprite"][u"night"][8] == u"闪闪灯辉照长廊", "v54 consumed-row structural anchor expected (sprite/night/8)"
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1123_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"叮咚", u"响夜", u"夜晚", u"叮咚响", u"响夜晚", u"叮咚响夜晚"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1123 quote-face word probe for candidate " + QUOTE_CORE + u" (sprite/weekend line4, night-window)"]
allzero = True
for wd in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if wd in f or wd in sq)
    if hits:
        allzero = False
    qrep.append(u"word [%s] -> %s" % (wd, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: %s. Facet-band honest registrations (single-char/family layer, NOT card-face collisions): (1) SPRITE VOICE 5th piece - weekend bucket 2nd within voice (v50 festival / v54 night / v61 market_close / v63 weekend / THIS weekend-2) = the 4-distinct-bucket streak ends, honest weaker-form note, legal (no voice-repeat blocking law; four-peat law far: v63+v64 = new-run 2-link); (2) ONOMATOPOEIA band THIRD USE fresh verdict (R1122 registered discretion, THIS round): v50 叮叮当 [bell/festival-night-dress] + v63 嗡嗡嗡 [hum/morning-dance] + THIS 叮咚 [doorbell/holiday-night-visits] = three distinct sounds x three distinct scenes x three distinct buckets -> third use LEGAL per R1062 angling-band precedent (third use legal, fourth use blocked) -> POST-v64 REGISTRATION: onomatopoeia 4th use future-blocked; single shared char 叮 with v50 叮叮当 = family-layer band adjacency, not a 2+ char shingle collision (叮叮 vs 叮咚 differ at 2nd char); (3) NIGHT-SCENE literal law (R1020): production moment past sunset ~17:37 = literal night, night content honestly paired (v51-v54 night-piece precedent band)." % (u"all 2+ char shingles ZERO fleet hits = TWELFTH fully-zero row of the series (v53-v63 eleven precedents)" if allzero else u"NOTE: some shingle hits above - honest adjacency adjudication required, see word lines"))
qrep.append(u"night-window unlock note: triple chain of custody (R1032 unlock-window registration -> R1086 post-v63 supply note -> R1122 night-window candidate registration). Triple literal alignment: literal-night production x night content (叮咚响夜晚) x weekend bucket (Saturday + national holiday day-3 evening). Six-axes daytime depletion carried (R1032/R1086); night-face residue: six-axes night faces zero-clean per R1023-R1029 scans (v51/v52/v53 consumed the only three clean night rows), sprite night face = v54 consumed night/8, remaining night rows = night-window position honest note.")
qrep.append(u"supply-face honest note post-v64: sprite weekend face = zero clean rows left (weekend/3 v63 + weekend/4 THIS consumed; other 10 rows collision/context-gated per R1032 scan); six axes remain R1032-depletion state; onomatopoeia band 3-link formed -> 4th use future-blocked registration; unlock windows unchanged: rain-event day / CEO-order day / 2026-10-08+ market reopen / Nov+ coldsnap / summer heatwave / sprite-night residue rows (night-window). Pool-expansion report position maintained (status-line not chase).")
io.open(os.path.join(TMP, "r1123_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V64:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        assert QUOTE_CORE not in face and QUOTE_CORE not in sq, "line already consumed by %s" % d

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 064",
    u"2026-10-03 · 国庆假期 · 夜",
    u"「叮咚响夜晚」",
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
assert H2_SIZE == 60, "em ladder expected 60-band (date line + 城市生灵 attribution line fits, v63 same-band precedent), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261003-DAILY-v64"
meta["form"] = (u"DAILY 城市日签 064（L-卡 图文轻内容线 DAILY 形态第六十四件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 夜窗解锁兑现 R1123·日签节律续件=日期×情境桶对位判据第六十四证〔**sprite 声部第五件+"
                u"weekend 桶新跑第二件**〔声部五件内 weekend 二采=四件四桶零重复最强形（v50/v54/v61/v63）终结·"
                u"诚实弱形注册·四连律远（v63+v64=新跑二连）〕+**夜窗 literal 对位**：literal night 生产〔日落 "
                u"~17:37 后·R1020 night literal 律〕×夜晚内容×weekend 假日桶（周六+国庆假期第 3 日夜）三重 "
                u"literal〔v51-v54 夜件带先例·邻接升档带 v55/v57 时点邻接→v62/v63 literal→本件 literal "
                u"night〕+**夜窗预登记链兑现**：R1032 解锁窗「night-window rows（sprite/weekend/4+night-bucket "
                u"residue）」→R1086 post-v63 供给注「sprite weekend face remainder=weekend/4 夜内容（night-"
                u"window only）」→R1122 夜窗候选注册=三重链兑现件〕+**拟声族带第三用定谳（R1122 注册裁量位·"
                u"本轮 fresh 判）**：v50 叮叮当〔铃铛·festival 夜换装〕+v63 嗡嗡嗡〔蜂鸣·晨舞〕+本件 叮咚〔门铃·"
                u"假日夜访〕=三声各异×三景各异×三桶各异=**第三用合法判例=R1062 垂钓族带同律**〔三连同构律字面"
                u"第四用起阻〕→post-v64 拟声族带第四用起阻注册+叮单字族带层邻接诚实注〔叮叮≠叮咚=非 2+ 字 "
                u"shingle 撞·族带层注〕〕+六轴日间枯竭态承继〔R1032/R1086·夜面残行=六轴 night R1023-R1029 扫描"
                u"零干净行承继+sprite night 残行夜窗位〕+门铃〔一家一户的最小问候〕×满城之夜〔最大的安静回响"
                u"舞台〕=**最小问候×最大夜幕反差金句位**〔族五十连·门铃位语感独占注=假期夜里串门的脚步声都"
                u"藏在门铃里〕〕）")
meta["source_quote"] = u"「叮咚响夜晚」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 sprite[weekend][4]（axes 6 轴×12 情境桶"
                           u"×18 行=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构·跨仓只读指针）"
                           u"+data/intel/daily/2026-10-03.md（当日日期语境源·国庆假期第 3 日+周六·夜窗生产语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 sprite[weekend][4] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+weekend 桶 12 行计数+sprite "
                         u"顶层 12 桶结构断言〔R982〕+v63 已耗行 weekend/3 结构锚+v54 已耗行 night/8 结构锚）"
                         u"②日期行 2026-10-03=当日历法事实·周六+国庆假期第 3 天〔daily brief 2026-10-03 当日窗"
                         u"语境〕+夜标记〔v51/v54 夜标记先例带·literal night 生产〕③情境=夜窗解锁件〔三重 "
                         u"literal 对位=literal night 生产时刻×夜晚内容×weekend 假日桶·R1032→R1086→R1122 三重"
                         u"预登记链〕④声部署名=台词池城市生灵声部行·本行无称谓面=纯景句·泛称零涉及〔人设权红"
                         u"线零接触·charter §2.4·v50/v54/v61/v63 先例族〕⑤去重断言=本行不在 city-spirit.md 已采"
                         u"面+不在全成品卡面 lines/source_quote 任一（卡面级实扫=R1010 修正律·DAILY-v1~v63 全 "
                         u"64 行+REACT-v8 同桶三行+city-spirit 节日场景三行皆非本行）+「叮咚」「响夜」「夜晚」"
                         u"「叮咚响」「响夜晚」全句 probe 六词机核〔r1123_quote_face.txt〕+**叮单字族带层邻接"
                         u"=v50 叮叮当族带注**〔非 2+ 字 shingle 卡面撞·拟声族带三连注册内〕⑥季相核=本行无年味/"
                         u"春联/春雨/寒潮类季相错位词〔R972 制·夜晚=四季通用夜面·十月秋夜兼容〕⑦品牌语感注="
                         u"「叮咚响夜晚」拟声开场+假日夜访场景=去 AI 感对位·人味命中·零书面套语·零消费宣称"
                         u"无品牌无价格")
meta["attribution_rule"] = (u"署名=池级+声部级（台词池·城市生灵声部）——池行无逐民署名·禁虚构居民名/生灵名"
                             u"（charter v1.2 署名律+人设权红线·本行无称谓面=纯景句·泛称零涉及〔v50/v54/v61/"
                             u"v63 先例族对照注〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（sprite 声部第五件+夜窗解锁件双位"
                            u"〔**夜窗预登记链兑现+拟声族带第三用定谳+零直撞三律并轨诚实执行**：六轴日间枯竭承继"
                            u"→夜窗解锁→sprite/weekend/4 唯一预登记夜行兑现〕+最小问候×最大夜幕反差金句位〔族"
                            u"五十连·门铃位语感独占注〕+拟声开场人味=语录卡线变体零新模板第六十四证（QUOTE-v2 "
                            u"参数 verbatim 复用·h2_size 60 档〔v63 同带先例·日期行驱动〕·charter §1「日签变体"
                            u"随时可续」兑现）·公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限+"
                            u"城市人文积累令 O-2026-09-28-1910 对位〔假期夜里串门声此起彼伏=城市夜里活着的邻里"
                            u"往来·城市生灵令 P-2026-09-26-13 媒体面第五采〕+**供给面诚实注**：本件后 sprite "
                            u"weekend 面零干净行〔weekend/3+4 双耗尽·余 10 行撞/门控〕+六轴维持 R1032 枯竭注+"
                            u"拟声族带三连成形→第四用起阻注册=DAILY 可诚实配对面维持结构性近枯竭注〔R1030 "
                            u"REACT 判负+R1032 零判负+R1086 唯一行解锁窗兑现+本件夜窗兑现四信号族·池扩容呈报"
                            u"位维持呈现状行不催办〕·post-v64 指针：解锁窗维持=雨事件日/CEO 令日/10-08 "
                            u"market_open 复市/Nov+ 寒潮/夏季 heatwave/夜窗行（sprite night 残面）·REACT-v9 "
                            u"10-04 窗·F 序号诚实注=本件先落 F-150·REACT-v9 10-04 预指位顺延 F-151〔R978 判例 "
                            u"finished 顺序号=单一真相〕")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：叮咚〔一记门铃·一家一户的最小问候·全城"
                          u"最小的一声问候〕×响夜晚〔满城之夜=最大的安静回响舞台〕=最小问候×最大夜幕反差+门铃"
                          u"声〔动的问候〕×夜〔静的背景〕=动静反差〔族五十连〕/情 1 假日夜里街坊串门的烟火温情"
                          u"共鸣温和如实非强极点〔G5 生灵/宠物群+G1 城市生活群〕/时 2 当日=2026-10-03 周六国庆"
                          u"假期第 3 日·literal night 生产〔日落 ~17:37 后〕×夜晚内容×weekend 假日桶三重 "
                          u"literal 直配=夜窗解锁件〔R1032→R1086→R1122 三重预登记链兑现〕/台 2 公众号方图"
                          u"承载=MC-001~149 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production "
                          u"open·charter §4 形态码 DAILY·queue §E E30 R1123 夜窗兑现")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市"
                     u"档案·DAILY 系列同源先例）；无登记居民名无登记生灵名=人设权红线零接触（本行无称谓面="
                     u"纯景句·泛称零涉及〔v50/v54/v61/v63 先例族对照注〕）；脱敏律=池句无令牌号/无个体可识别面/零"
                     u"金钱数额（叮咚响夜晚=假日夜访门铃意象非商业面·无品牌无价格=零消费宣称）；成品只入库·"
                     u"发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第六十四件·charter v1.2 §4 形态码 DAILY·日签节律续件·sprite 声部第五件·weekend 桶新跑第二件·夜窗 literal 对位件·拟声族带第三用注册件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: sprite[weekend][4] verbatim OK; weekend bucket=12 rows; sprite top-level 12 buckets (R982 structure); v63 consumed-row weekend/3 + v54 consumed-row night/8 structural anchors; card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v63; night-window unlock: triple chain R1032->R1086->R1122; onomatopoeia 3rd-use fresh verdict LEGAL per R1062 precedent -> post-v64 4th-use blocked registered; quote-face word probe: 6 words see r1123_quote_face.txt")
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
report.append("LADDER_60: date line + attribution line fit 60-band (v63 same-band precedent); four-LINES stack; all other QUOTE-v2 params verbatim; night-window unlock + onomatopoeia 3rd-use verdict + sprite-voice-5th honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1123.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V64, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V64, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- fleet form counts (F-registration machine truth, v63 review precedent: disk machine-count is authoritative)
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

# --- E4 audience reference call (async detached, 1500s window, v51-v63 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder 60, date+attribution lines fit) + E4 fired async" % H2_SIZE)
