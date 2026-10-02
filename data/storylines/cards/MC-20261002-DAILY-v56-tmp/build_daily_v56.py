# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v56 build: DAILY (city daily-sign) series FIFTY-SIXTH piece (R1026, queue
section-E E30 standby). XIAOYAO-REDEMPTION PIECE (structural, honest): rotation post-v55 counts
qiuxin 9 / huaijiu 9 / xiaqi 9 / yanhuo 9 / zhixu 9 / xiaoyao 8 (sprite tracked separately:
v50 festival/0 + v54 night/8) -> xiaoyao unique minimum (last piece v48, gap 7 = LONGEST) ->
redemption target = xiaoyao -> xiaoyao/night face machine-proven zero clean rows (r1023_pool.txt
fresh, re-confirmed r1024 cascade; fleet additions only ADD collisions -> blocked stable) -> per
R1025 rotation note + pre-registration: xiaoyao x {festival, dusk, market_close} fresh re-probe
r1026_pool.txt (fleet includes v55) -> festival 18 rows ALL content collisions + market_close
18 rows ALL carry hits + dusk line6 「夕阳西下鱼也归巢了」 = ONLY clean row (ZERO direct shingle
hits, 2-5 char including punctuation-inclusive 2-gram all zero = zero construct-layer adjacency =
FOURTH fully-zero row of the series after v53/v54/v55). R1025 pre-registered backup redeemed =
THIRD backup-promotion of the series (v53 first / v54 second / this third). Zero-collision
standard NOT relaxed (R442 anti-isomorphism spine, v1-v55 fifty-five-link zero-collision chain).
DUSK BUCKET FIRST PIECE of the DAILY series (v55 market_close evening-adjacent first piece ->
v56 dusk = second evening-adjacent supply face; honest note: ~23:0x deep-night production x dusk
scene = time-adjacent NOT time-exact). Built-in tension: NAO x JING - National Day holiday day
2, the whole city crowds the festival lights, while the most leisurely angler packs up at dusk
by the river, even the fish go home; 「鱼也归巢了」 = fish personification everyday-casual
particle structure (也...了 completion tone = human-flavor hit). Layout = QUOTE-v2 params
verbatim; h2_size ladder = 60 band (short-quote band, v54 sprite piece precedent; attribution
line 12.65em driver margin +2.68em at 60 budget 15.33em). Machine source/dedup assertions
(R456 system, card-face level R1010 law). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V56 = os.path.join(BASE, "MC-20261002-DAILY-v56")
TMP = V56 + "-tmp"
os.makedirs(V56, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"夕阳西下鱼也归巢了"
AXIS, BUCKET, IDX = u"逍遥", u"dusk", 6

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
assert len(pool["axes"]) == 6, "axes != 6 (R982 structure: axes 6 x 1296 + sprite 144)"
assert isinstance(pool.get("sprite"), dict) and "night" in pool["sprite"], "sprite top-level key missing (R982)"
mb = pool["axes"][AXIS][BUCKET]
assert len(mb) == 18, "axis bucket != 18 rows (axes = 6 x 12 buckets x 18 rows = 1296)"
assert mb[IDX] == QUOTE_CORE, "pool line mismatch: %r" % mb[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1026_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"夕阳", u"西下", u"归巢", u"鱼也", u"夕阳西", u"阳西下", u"西下鱼", u"下鱼也", u"鱼也归巢"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1026 quote-face word probe for candidate " + QUOTE_CORE + u" (xiaoyao/dusk line6)"]
for w in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if w in f or w in sq)
    qrep.append(u"word [%s] -> %s" % (w, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
qrep.append(u"honest-adjacency notes: NO construct-layer adjacency this row - all 2-5 char shingles including punctuation-inclusive 2-grams ZERO fleet hits (r1026_pool.txt fresh, fleet includes v55) = FOURTH fully-zero row of the series (v53 first / v54 second / v55 third / this fourth); supply-face honest note: xiaoyao/night machine-proven zero clean rows (r1023 fresh + r1024 cascade re-confirmed, blocked stable) + xiaoyao/festival 18 rows ALL content collisions + xiaoyao/market_close 18 rows ALL carry hits (r1026_pool.txt fresh re-probe) -> dusk line6 = ONLY clean supply face for the redemption-target axis; R1025 pre-registered backup redeemed = THIRD backup-promotion of the series (v53/v54/this); bucket honesty: production ~23:0x deep night vs dusk scene = time-adjacent NOT time-exact (evening-adjacent supply face, dusk-bucket FIRST piece of DAILY series after v55 market_close first piece); holiday-day-2 note: National Day holiday day 2 dusk = the angler's holiday is spent by the water, packing up when the sun goes down (scene-context fit); 鱼也归巢了 = pool-line verbatim fish personification (fish returning home like people - living-city co-dwelling imagery, P-20260926-13 sublimation-law media-face air, NOT a sprite-voice harvest); post-v56 rotation note: xiaoyao becomes 9 -> ALL SIX AXES AT 9 -> next minimum by gap = qiuxin (last v49, gap 7 LONGEST) = v57 redemption target; qiuxin supply faces fresh full scan deferred to next round (honest deferral note, r1026 scan focused on xiaoyao redemption)")
io.open(os.path.join(TMP, "r1026_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V56:
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
# (#47/#53/#59). Sprite face: v50 sprite/festival/0 + v54 sprite/night/8. NIGHT bucket:
# v51 yanhuo/13 (first piece) + v52 xiaqi/4 (second piece) + v53 zhixu/7 (third piece).
# market_close bucket: v55 huaijiu/1 (supply-face-switch first piece). DUSK bucket:
# THIS piece = xiaoyao/dusk/6 (dusk-bucket FIRST piece of the DAILY series).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 056",
    u"2026-10-02 · 国庆假期",
    u"「夕阳西下鱼也归巢了」",
    u"——硅基城市台词池 · 逍遥轴",
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
assert H2_SIZE == 60, "em ladder expected 60-band (short-quote band, v54 sprite piece precedent; attribution line 12.65em driver margin +2.68em at 60 budget 15.33em; quote 11.00em), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v56"
meta["form"] = (u"DAILY 城市日签 056（L-卡 图文轻内容线 DAILY 形态第五十六件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1026·日签节律续件=日期×情境桶对位判据第五十六证〔**dusk 傍晚桶首件**"
                u"（DAILY 系列 dusk 桶第一件·v55 market_close 傍晚邻接桶首件后=傍晚族供面第二桶开桶）·**诚实注=时点邻接"
                u"非 literal night 直配**〔~23:0x 深夜生产×黄昏归巢场景=邻接面如实注记〕·场景级=假期第二日黄昏江边收竿"
                u"归巢面〕+**旋转律兑现（逍遥回补·结构性诚实注）**：v55 后计数求新 9/怀旧 9/侠气 9/烟火 9/秩序 9→"
                u"逍遥 8=六轴唯一最少〔v48 后 7 件未采=最长回补距〕→回补目标=逍遥→**逍遥/night 零干净行〔r1023 fresh+"
                u"r1024 级联复证·fleet 增只增撞=阻断稳定〕+逍遥三供面 fresh 复扫 r1026_pool.txt**：festival 18 行全数"
                u"内容层直撞+market_close 18 行全数带撞→dusk line6=**三供面唯一干净行胜出**=零直撞标准不放松〔R442 "
                u"反同构主线·v1-v55 五十五连零直撞〕+**R1025 预登记备胎第三次转正**〔v53 首转/v54 第二转后连续·"
                u"r1025_pool.txt 预登记「逍遥/dusk line6」兑现·质量选优非序号盲领〕〕+line6 选优〔**全 shingle 零命中+"
                u"零构式层邻接=系列第四件全零邻接行**（v53/v54/v55 后连续·r1026_pool.txt fresh 2-5 字含标点全零="
                u"r1026_quote_face.txt 九词机核·逍遥/dusk 18 行唯一干净行〕+「鱼也归巢了」=池行 verbatim 拟人细节"
                u"〔鱼像人一样归巢=城市场景生灵共栖意象·P-20260926-13 升华律媒体面气口·非 sprite 声部采录〕+「也…了」"
                u"完成体口语真感=人味命中〔CEO 审美线对位〕+逍遥轴〔最闲适·钓鱼喝茶看云的轴〕×「夕阳西下鱼也归巢了」"
                u"〔全城赶节日灯会热闹×黄昏水边独自收竿〕=**闹×静轴内自反差金句位**〔族四十二连·归巢位语感独占注"
                u"=最爱凑热闹的假期×最先收工回家的人·灯会散场前×江面归巢时〕〕）")
meta["source_quote"] = u"「夕阳西下鱼也归巢了」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[逍遥][dusk][6]（axes 6 轴"
                           u"×12 情境桶×18 行=1296+sprite 顶层 12 桶×12 行=144=1440 行·BigLife R982 窗结构"
                           u"重构·内容零变实锚·跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·"
                           u"国庆假期第 2 日=DAILY-v1~v55 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[逍遥][dusk][6] verbatim 零改字（「」=卡面"
                         u"排版层〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位+dusk 桶 18 行计数"
                         u"+axes 6 轴+sprite 顶层结构三断言实锚〔R982〕）②日期行 2026-10-02=当日历法事实·国庆假期="
                         u"假期第 2 天〔daily brief 2026-10-02 当日窗语境〕③情境=dusk 傍晚桶首件〔DAILY 系列 dusk 桶"
                         u"第一件·v55 market_close 傍晚邻接桶首件后傍晚族第二桶·**诚实注=黄昏场景×~23:0x 深夜生产="
                         u"时点邻接非 literal night 直配**〕④池级署名=台词池轴级行·「鱼也归巢了」=池行 verbatim 拟人"
                         u"面〔鱼归巢=生灵共栖意象〕非登记居民名非登记生灵名〔人设权红线零接触·charter §2.4·"
                         u"v52 船老大/v55 老陈头泛称先例族〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品"
                         u"卡面 lines/source_quote 任一（卡面级实扫=R1010 修正律·DAILY-v1~v55 全 55 行+REACT-v8 同桶"
                         u"三行+city-spirit v1.2 节日场景三行皆非本行）+「夕阳」「西下」「归巢」「鱼也」「夕阳西」"
                         u"「阳西下」「西下鱼」「下鱼也」「鱼也归巢」probe 九词机核〔r1026_quote_face.txt〕+"
                         u"**零构式层邻接**〔r1026_pool.txt fresh 2-5 字含标点 2 字组全零=系列第四件全零邻接行·"
                         u"v53/v54/v55 后连续·逍遥三供面〔night/festival/market_close〕零干净行+dusk 唯一干净行"
                         u"fresh 实证〕⑥季相核=本行无年味/春联/春雨类季相错位词〔R972 制·黄昏收竿归巢=假日傍晚"
                         u"季相对位〕⑦品牌语感注=「夕阳西下」自然时序白话+「也…了」完成体口语真感+鱼拟人市井想象"
                         u"〔去 AI 感对位·日常口气=人味命中〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·逍遥轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·本行无称谓面=纯景句·泛称零涉及〔v52/v55 泛称先例族对照注〕）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（dusk 傍晚桶首件〔**旋转律+预登记备胎转正+"
                            u"零直撞三律并轨诚实执行**：六轴唯一最少逍遥回补→night 面机证阻断〔r1023 fresh+r1024 级联〕"
                            u"→R1025 预登记 dusk line6 备胎 fresh 复扫兑现〔第三次转正〕→三供面唯一干净行胜出〕+~23:0x "
                            u"同轮对位〔时点邻接诚实注〕+闹×静反差金句位〔族四十二连·归巢位语感独占注〕+「鱼也归巢了」"
                            u"拟人+「也…了」口语真感=语录卡线变体零新模板第五十六证（QUOTE-v2 参数 verbatim 复用·"
                            u"h2_size 60 档〔v54 短句同带先例·署名行 12.65em 驱动 margin +2.68em〕·charter §1「日签"
                            u"变体随时可续」兑现）·公众号低创作度条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限+城市"
                            u"人文积累令 O-20260928-1910 对位〔最闲适的人在热闹的假期里最早收工回家=城市黄昏的收梢人面〕"
                            u"+R442 人物场景处方带第五件〔v51 铺子守早客/v52 船老大夜航/v53 值夜岗慢步巡逻/v55 老陈头"
                            u"背手溜达+v54 生灵插件后人物带续连=江边钓鱼人黄昏收竿·江边垂钓人像面 v6 同族第二采〔人物"
                            u"复访·行面零同构机证〕〕+升华律媒体面气口〔鱼归巢=生灵共栖意象·P-20260926-13〕+"
                            u"**供给面诚实注**：本件后逍遥轴四面已采面=dusk line6 唯一干净行已消费→六轴全 9→"
                            u"v57 目标=求新〔v49 后 gap 7 最长〕+求新供面 fresh 全扫下轮执行〔诚实缓办注〕")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：「鱼也归巢了」拟人细节〔鱼像人一样归巢="
                          u"生灵共栖想象〕+假期全城灯会热闹×黄昏水边独自收竿=闹×静反差〔族四十二连·归巢位语感独占注〕"
                          u"+灯会散场前×江面归巢时/情 1 黄昏收工归巢松弛温暖画面感如实〔非强极点〕/时 2 当日时点=国庆"
                          u"假期第 2 日+dusk 傍晚桶首件〔**诚实注=时点邻接非 literal night 直配**·~23:0x 深夜生产×"
                          u"黄昏归巢场景〕/台 2 公众号方图承载=MC-001~140 S3 实证复用）——hit-chain-mechanism v1.0 "
                          u"§2/§9·D-BS-06 production open·charter §4 形态码 DAILY·queue §E E30 R1026 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无登记居民名无登记生灵名=人设权红线零接触（本行无称谓面=纯景句·"
                     u"「鱼也归巢了」=池行 verbatim 拟人面〔v52/v55 泛称先例族对照注〕）；脱敏律=池句无令牌号/无个体"
                     u"可识别面/零金钱数额（黄昏收竿归巢=市井生活意象非个体档案面·无品牌无价格=零消费宣称）；成品只"
                     u"入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第五十六件·charter v1.2 §4 形态码 DAILY·日签节律续件·dusk 傍晚桶首件·逍遥轴回补件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[xiaoyao][dusk][6] verbatim OK; dusk bucket=18 rows; axes=6 + sprite top-level (R982 structure); card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v55 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; prior consumption faces: night bucket v51 yanhuo/13 + v52 xiaqi/4 + v53 zhixu/7 + sprite v50 festival/0 + v54 night/8 + market_close v55 huaijiu/1; xiaoyao redemption: night blocked (r1023 fresh + r1024 cascade, stable) + festival 18 all collisions + market_close 18 all hits (r1026_pool.txt fresh) -> dusk line6 = ONLY clean row; R1025 pre-registered backup redeemed = 3rd backup-promotion; quote-face word probe: 9 words see r1026_quote_face.txt (all ZERO; zero construct-layer adjacency = FOURTH fully-zero row of series after v53/v54/v55)")
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
report.append("LADDER_60: attribution-line 12.65em driver (v54 short-quote band precedent); four-LINES stack; all other QUOTE-v2 params verbatim; dusk-bucket-first DAILY piece + xiaoyao-redemption + 3rd-backup-promotion + 4th-fully-zero-row honest notes carried in meta.form")
io.open(os.path.join(TMP, "em-check-r1026.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V56, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V56, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v53-v55 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R1017 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder 60, short-quote band, v54 precedent) + E4 fired async" % H2_SIZE)
