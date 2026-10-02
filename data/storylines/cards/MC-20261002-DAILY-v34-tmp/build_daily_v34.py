# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v34 build: DAILY (city daily-sign) series THIRTY-FOURTH piece (R1003, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 -> festival
bucket direct match (thirty-fourth same-day proof). Axis pick = xiaqi (loyalty-and-brotherhood
residents)/festival/9: rotation law = post-v33 DAILY counts qiuxin 6 / yanhuo 6 / huaijiu 6 /
xiaqi 5 / zhixu 5 / xiaoyao 5 -> three-way tie at five consumptions -> within-tie
longest-unconsumed redemption = xiaqi last picked v26, seven pieces ago (v27-v33 all other
axes) vs zhixu v30 / xiaoyao v31 recent picks avoided. Within xiaqi FREE face
content-strength pick documented (weakness notes: line17 'jianghu yiqi' word-level repeat of
consumed v3 line5, line14 star motif near-duplicate of consumed v12 line15, line11+line12
'ye dei' clause near-duplicate of consumed v32 line10, line7 labor-x-joy structural slot same
as v32 (R442 serial-isomorphism face), line3 'jieri fenwei' word repeat of consumed v28 line9,
line4 'chuanshang' word repeat of consumed v20 line1 plus labor-x-joy third consecutive risk,
line6/line8 'nianwei' wording season-law avoid (R972, October timepoint, R988 precedent),
line15 lantern-hang pattern family saturation (v21/v26/v30 lantern-joy band), line16
'xinqing feiyang' bookish cliched register weak on colloquial authenticity; THIS line9 =
chuanmen (door-to-door visiting) slot brand-new series theme family zero prior consumption +
National Day holiday custom direct match (zou-qin-fang-you) + doubled-verb 'chuanchuanmen'
+ trailing clipped one-word exclaim 'renaao' (series-first clipped ending) + 'jiefang linli'
folk doubled-synonym compound = top colloquial authenticity). Mild adjacency documented
honestly: 'linli' two-char word also in consumed v13 line2 (different collocation: linli-jian
dispute-gone vs jiefang-linli visiting, theme families distinct); trailing 'renao' word also
in consumed v22 (verb-object 'cou ge renao' vs clipped standalone exclaim, different
construction, series-first). This line zero fleet consumption (city-spirit NOT_IN pre-check +
all cards.json scan asserted; consumed festival lines for xiaqi axis = DAILY-v3 line5 +
DAILY-v8 line13 + DAILY-v13 line2 + DAILY-v20 line1 + DAILY-v26 line10 + city-spirit v1.2
line0 -> line9 fresh). Built-in tension:
街坊邻里都来串串门，热闹 (the residents who prize loyalty-and-brotherhood above all, in the
end, spend the festival on the humblest of all rituals - knocking on the neighbor's door =
grand loyalty lands in the smallest walk = yi x lin)
= 义×邻 axis-internal self-contrast (v15 screen-x-real / v16 past-x-present / v17 rule-x-
joy / v18 bustle-x-ease / v19 plain-x-festival / v20 rest-x-busy / v21 joy-x-steady /
v22 old-x-bustle / v23 new-x-craft / v24 bustle-x-heart / v25 new-season-x-old-time /
v26 hard-x-soft / v27 bustle-x-homecoming / v28 joy-x-maintain / v29 ease-x-bustle /
v30 dress-x-proper / v31 dance-x-furnace / v32 labor-x-joy / v33 style-x-small = same
structural gold-sentence family, twentieth consecutive variant). Axis-exclusive register
note: only a resident whose loyalty-ethos lives in open doors and loud greetings says the
festival as 'come over for a visit' - the trend-chasers and the rule-keepers cannot say
this line = axis-exclusive register slot. Scene layer: National Day holiday evening,
festival lamps strung, every street door standing open, neighbors moving door-to-door, the
loudest-voiced loyalty residents hailing each other across doorways = concrete
people-in-motion visiting scene (R442 audit weakness prescription band; v13 street-corner
auntie sibling scene noted; chuanmen slot = brand-new theme family). Plain speech
(doubled-verb chuanchuanmen + clipped one-word exclaim renao = colloquial authenticity) =
anti-AI-flavor authenticity. Living-city proof = the festival that turns neighbors into
visiting relatives = the city's human bonds are alive (city humane-accumulation order
echo). Line-level freshness thirty-first proof = same-axis-different-line twenty-ninth
proof. Quote verbatim + card framing (R285 QUOTE precedent). Layout = QUOTE-v2 params
verbatim; h2_size ladder returns to notch 60 (quote line 14.00em fits 15.33em budget with
+1.33em margin, four-line stack VERT +229px = v17/v22 same-structure notch band; step-up
from v33 46-notch short-line step-down, ladder length-driven law). Machine source/dedup
assertions (R456 system). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V34 = os.path.join(BASE, "MC-20261002-DAILY-v34")
TMP = V34 + "-tmp"
os.makedirs(V34, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"街坊邻里都来串串门，热闹"
AXIS, BUCKET, IDX = u"侠气", u"festival", 9

# --- machine source assertions (R456: pool verbatim + fleet-wide dedup)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"
for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V34:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        assert QUOTE_CORE not in io.open(cj, encoding="utf-8").read(), "line already consumed by %s" % d
# consumed festival lines (documented not asserted): DAILY-v1 qiuxin/festival/4 +
# DAILY-v2 huaijiu/festival/0 + DAILY-v3 xiaqi/festival/5 + DAILY-v4 yanhuo/festival/4 +
# DAILY-v5 zhixu/festival/4 + DAILY-v6 xiaoyao/festival/3 + DAILY-v7 qiuxin/festival/7 +
# DAILY-v8 xiaqi/festival/13 + DAILY-v9 qiuxin/festival/12 + DAILY-v10 huaijiu/festival/3 +
# DAILY-v11 yanhuo/festival/13 + DAILY-v12 xiaoyao/festival/15 + DAILY-v13 xiaqi/festival/2 +
# DAILY-v14 qiuxin/festival/3 + DAILY-v15 qiuxin/festival/11 + DAILY-v16 huaijiu/festival/1 +
# DAILY-v17 zhixu/festival/12 + DAILY-v18 xiaoyao/festival/1 + DAILY-v19 yanhuo/festival/3 +
# DAILY-v20 xiaqi/festival/1 + DAILY-v21 zhixu/festival/6 + DAILY-v22 huaijiu/festival/12 +
# DAILY-v23 qiuxin/festival/13 + DAILY-v24 yanhuo/festival/2 + DAILY-v25 huaijiu/festival/17 +
# DAILY-v26 xiaqi/festival/10 + DAILY-v27 yanhuo/festival/7 + DAILY-v28 zhixu/festival/9 +
# DAILY-v29 xiaoyao/festival/2 + DAILY-v30 zhixu/festival/2 + DAILY-v31 xiaoyao/festival/4 +
# DAILY-v32 yanhuo/festival/10 + DAILY-v33 huaijiu/festival/4 + REACT-v8 xiaoyao/festival/17 +
# yanhuo/festival/12 + zhixu/festival/14 (source_facts) + city-spirit v1.2 festival-scene trio
# zhixu/festival/16 + qiuxin/festival/14 + xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 034",
    u"2026-10-02 · 国庆假期",
    u"「街坊邻里都来串串门，热闹」",
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
assert H2_SIZE == 60, "em ladder front-fit: quote line 14.00em fits 15.33em budget at 60 with margin +1.33em (four-line stack VERT +229px = v17/v22 same-structure notch band; step-up from v33 46-notch, ladder length-driven law), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v34"
meta["form"] = (u"DAILY 城市日签 034（L-卡 图文轻内容线 DAILY 形态第三十四件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1003·日签节律续件=日期×情境桶对位判据第三十四证〔festival 桶当日"
                u"直配系列化·10-02=国庆假期第 2 日〕+六轴收官后线级新鲜度第三十一证=同轴异行第二十九证〔侠气轴 "
                u"DAILY-v3〔line5〕+DAILY-v8〔line13〕+DAILY-v13〔line2〕+DAILY-v20〔line1〕+DAILY-v26〔line10〕"
                u"之外线级新鲜行 line9·轴面 v6 收官耗尽后线级新鲜度=唯一面〔R975 收口注承接〕·旋转律兑现=v33 后"
                u"计数求新 6/烟火 6/怀旧 6/侠气 5/秩序 5/逍遥 5=三轴并列最少 5 采·并列面内最久未采回补=侠气"
                u"v26 后 7 件首回〔v27-v33 七件皆他轴〕·v30 秩序/v31 逍遥两最近采避开=轮换多样性维持·并列面内"
                u"内容强度择优如实注记〔侠气 FREE 面弱项：line17「江湖义气」词面重复已采 v3 line5+line14 星星 "
                u"motif 近重复已采 v12 line15+line11/line12「也得」句式连件近重复已采 v32 line10+line7 劳×欢"
                u"结构同构 v32〔R442 系列同构面〕+line3「节日氛围」词面重复已采 v28 line9+line4「船上」词面"
                u"重复已采 v20 line1 且劳×欢结构三连+line6/line8「年味」措辞季相律回避〔10 月秋时点·R972 制·"
                u"R988 同型先例〕+line15 灯笼一挂主题族饱和〔v21/v26/v30 灯喜带〕+line16「心情飞扬」书面套语"
                u"感口语真感弱；本行=串门位系列全新主题族零前采+叠动词「串串门」+截断式单叹「热闹」收尾=系列"
                u"首见截断式收尾+「街坊邻里」双近义民间复合词·轻度邻接如实注记：「邻里」二字亦在已采 v13 "
                u"line2〔不同搭配 邻里间纠纷 vs 街坊邻里·主题族 纠纷和解 vs 串门=异质〕+尾词「热闹」亦在已采 "
                u"v22〔动词宾语凑个热闹 vs 截断式单叹=不同构式·系列首见〕〕〕+侠气轴〔最豪爽嗓门最大·情义至重·"
                u"把街坊当兄弟的居民〕×「街坊邻里都来串串门，热闹」（最讲义气的人把节日过成最家常的串门=大"
                u"情义落进小走动）=义×邻轴内自反差金句位〔v15 屏×真/v16 往×今/v17 规×情/v18 闹×闲/v19 "
                u"平实×节日/v20 歇×忙/v21 喜×稳/v22 旧×闹/v23 新×手艺/v24 闹×心/v25 新时×旧光/v26 硬×软/v27 "
                u"闹×归/v28 喜×护/v29 闲×喧/v30 装×妥/v31 舞×炉/v32 劳×欢/v33 派×小=族二十连·串门位语感"
                u"独占注=把情义过成串门·讲规矩的人和赶新潮的人说不出这句=轴语感独占位〕〕）")
meta["source_quote"] = u"「街坊邻里都来串串门，热闹」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[侠气][festival][9]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v33 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[侠气][festival][9] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·单行短句排版=v19/v22/v28 设计排版先例·build 脚本内断言=池行"
                         u"逐字在位实锚）②日期行 2026-10-02=当日历法事实·国庆假期=假期第 2 天（daily brief "
                         u"2026-10-02 当日窗语境）③情境=festival 情境桶当日直配（12 桶中节日情境与当日唯一对位"
                         u"·DAILY-v1~v33 同桶直配第三十四证=日签节律判据系列化）④池级署名=台词池行无居民名〔人设权"
                         u"红线零接触·charter §2.4〕⑤去重断言=本行不在 city-spirit.md 64 条已采面+不在全成品 "
                         u"cards.json 任一（build 脚本 fleet 级扫描实锚·DAILY-v1〔求新/4〕+DAILY-v2〔怀旧/0〕+"
                         u"DAILY-v3〔侠气/5〕+DAILY-v4〔烟火/4〕+DAILY-v5〔秩序/4〕+DAILY-v6〔逍遥/3〕+DAILY-v7"
                         u"〔求新/7〕+DAILY-v8〔侠气/13〕+DAILY-v9〔求新/12〕+DAILY-v10〔怀旧/3〕+DAILY-v11〔烟火"
                         u"/13〕+DAILY-v12〔逍遥/15〕+DAILY-v13〔侠气/2〕+DAILY-v14〔求新/3〕+DAILY-v15〔求新/11〕"
                         u"+DAILY-v16〔怀旧/1〕+DAILY-v17〔秩序/12〕+DAILY-v18〔逍遥/1〕+DAILY-v19〔烟火/3〕+"
                         u"DAILY-v20〔侠气/1〕+DAILY-v21〔秩序/6〕+DAILY-v22〔怀旧/12〕+DAILY-v23〔求新/13〕+"
                         u"DAILY-v24〔烟火/2〕+DAILY-v25〔怀旧/17〕+DAILY-v26〔侠气/10〕+DAILY-v27〔烟火/7〕+"
                         u"DAILY-v28〔秩序/9〕+DAILY-v29〔逍遥/2〕+DAILY-v30〔秩序/2〕+DAILY-v31〔逍遥/4〕+"
                         u"DAILY-v32〔烟火/10〕+DAILY-v33〔怀旧/4〕+REACT-v8 同桶三行〔逍遥/17+烟火/12+秩序/14〕+"
                         u"city-spirit v1.2 节日场景三行〔秩序/16+求新/14+侠气/0〕皆非本行=线级新鲜度第三十一证·"
                         u"本行=侠气轴 line9 非 DAILY-v3 line5 非 DAILY-v8 line13 非 DAILY-v13 line2 非 "
                         u"DAILY-v20 line1 非 DAILY-v26 line10 非 city-spirit v1.2 line0=同轴异行第二十九证"
                         u"〔六轴收官后侠气轴第六采·轮前 city-spirit NOT_IN 预检复证=r1003_pool_scan.txt 全桶"
                         u"预检 FREE 52 行=R978 拦截教训执行·v33 行已 USED 复核〕⑥季相核=本行无「年味」措辞亦无"
                         u"春雨/春联类季相错位词（R972 制·侠气面 line6/line8 年味行已按季相律回避·串门/热闹="
                         u"全季相公共节日社交措辞与国庆走亲访友时点对位）⑦品牌语感注=「串串门」叠动词+收尾截断式"
                         u"单叹「热闹」+「街坊邻里」双近义民间复合词=街坊嘴里的口气·口语真感顶档〔去 AI 感/制作感"
                         u"双对位·CEO 趣律缺趣=不合格对位〕+侠气轴〔把情义看得最重·把街坊当兄弟〕×串门〔最日常"
                         u"的人情走动〕=义×邻金句位（最讲义气的人把节日过成最家常的串门=大情义落进小走动）+"
                         u"国庆假期傍晚满街节日灯下街坊家门敞开邻里互相串门=串门场景层=具体人群×具体动作场景面"
                         u"〔R442 审计叙事弱点处方带续证·v13 街角阿姨同族异质行注·串门位=系列全新主题族零前采〕+"
                         u"真城生命感方向对位=假期把邻居走成亲戚=城市人情活着的证据〔城市人文积累令 O-20260928-1910 "
                         u"对位〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·侠气轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·街坊邻里=人群称谓群像面非登记居民名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第三十四证+三轴"
                            u"并列最少 5 采内最久未采回补〔侠气 v26 后 7 件首回·并列面内容强度择优弱项注记后本行"
                            u"胜出·串门位=系列全新主题族·R442 具体人物场景处方+叠动词截断式收尾双命中〕+"
                            u"「街坊邻里都来串串门，热闹」〔最讲义气的人把节日过成最家常的串门=义×邻〕义×邻轴内"
                            u"自反差金句位〔族二十连·串门位语感独占注〕+串门场景层=R442 审计处方带续证+「串串门」"
                            u"叠动词+「热闹」截断式单叹=口语真感=人味命中〔CEO 审美线对位·国庆走亲访友习俗直配〕"
                            u"+假期把邻居走成亲戚=城市人文积累令对位〔真城生命感〕）+语录卡线变体零新模板第三十"
                            u"四证（QUOTE-v2 参数 verbatim 复用·h2_size 梯档回 60=14.00em 行长驱动〔v33 46 档带后"
                            u"回档·60 档预算 15.33em margin +1.33em·四行栈 VERT +229px=v17/v22 同构档·R293 零余量"
                            u"排除+R301-313 梯档律〕·charter §1「日签变体随时可续」兑现）·公众号低创作度条款 "
                            u"7.1-7.4 编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：侠气轴〔最豪爽嗓门最大·情义至重·把街坊当"
                          u"兄弟〕×串门〔最日常的人情走动〕=义×邻轴内自反差金句位〔族二十连·串门位语感独占注〕+"
                          u"国庆假期傍晚满街灯下街坊家门敞开邻里互相串门=串门场景层+「串串门」叠动词+「热闹」"
                          u"截断式单叹=街坊口气口语真感/情 1 人情温度温和共鸣如实非强极点/时 2 当日时点=国庆"
                          u"假期第 2 日走亲访友=串门习俗当日对位+festival 情境桶直配第三十四证+池句节日语气常青/"
                          u"台 2 公众号方图承载=MC-001~118 S3 实证复用）——hit-chain-mechanism v1.0 §2/§9·D-BS-06 "
                          u"production open·charter §4 形态码 DAILY·queue §E E30 R1003 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（街坊邻里=人群称谓群像面非登记居民名）；"
                     u"脱敏律=池句无令牌号/无个体可识别面/零金钱数额（串门=节日社交习俗面非个体档案面）；"
                     u"成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第三十四件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[xiaqi][festival][9] verbatim OK; festival bucket=18 lines; fleet dedup OK (city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v33 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness thirty-first proof: xiaqi line9 != DAILY-v3 line5 != DAILY-v8 line13 != DAILY-v13 line2 != DAILY-v20 line1 != DAILY-v26 line10 != city-spirit v1.2 line0 = same-axis-different-line twenty-ninth proof")
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
report.append("LADDER_STEP_UP: quote line 14.00em fits 15.33em budget at 60 with margin +1.33em -> returns to notch 60 (four-line stack VERT +229px = v17/v22 same-structure band; step-up from v33 46-notch short-line step-down, ladder length-driven law); zero-new-template law maintained on all other QUOTE-v2 params")
io.open(os.path.join(TMP, "em-check-r1003.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V34, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V34, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v8/v13/v15-v33 pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder step-up back to 60 notch, from v33 46-notch band) + E4 fired async" % H2_SIZE)
