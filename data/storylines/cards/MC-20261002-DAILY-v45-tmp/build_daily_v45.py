# -*- coding: utf-8 -*-
"""MC-20261002-DAILY-v45 build: DAILY (city daily-sign) series FORTY-FIFTH piece (R1014, queue
section-E E30 standby). Day context 2026-10-02 = National Day holiday day 2 -> festival
bucket direct match (forty-fifth same-day proof, bucket-level; scene face = holiday at-home
rummaging old-objects honestly noted, second non-lamp face after v44 morning-market face =
anti-homogenization variation continuation). Axis pick = huaijiu (most nostalgic, old-times
lover) /festival/16: rotation law = post-v44 DAILY counts qiuxin 8 / huaijiu 7 / xiaqi 7 /
yanhuo 8 / zhixu 7 / xiaoyao 7 = FOUR axes tied at minimum (huaijiu/xiaqi/zhixu/xiaoyao)
-> tie-break by longest-since-last-pick redemption = huaijiu (first re-pick since v39;
v40-v44 five pieces all other axes = longest redemption distance in the tie). Within
huaijiu FREE face content-strength pick documented (card-face-level law R1010 corrected
scanning; r1014_pool.txt FREE-face precheck + r1014_quote_face.txt word-face machine
probe): line6/8/15 nian-wei seasonal rows -> R972 EXCLUDED three rows (+line8/15
guashang-denglong / denglong-yi-gua four-char collisions v21 + deng-long eight-piece
saturation); line7 'jiu san shang napa you ge xiao podong, ye zhe de zhu chunyu' =
chunyu seasonal + umbrella family v22 double interception (R1008 note carried); line13
'nian-nian gua deng, nian-nian you yu' = new-year-blessing nian-wei adjacency (R1002
note carried); line2 'xiu san de shouyi huor, rujin ke zhen shi shao le' = umbrella
v22 + shouyi-huor v23 double word-face collision + zero festival hook; line9 'zhe bu
deng de shouyi, chuan le ji beizi' = shouyi v23 + generational-passing v14 double
adjacency (R1008 note carried) + lamp-face regression = anti-homogenization backstab;
line10 'kan zhe hongtongtong de, xinli ye nuanhe' = xinli-nuanhe v24 direct collision =
lamp->warmth causation strongest repeat face (R1008 note carried); line11 'ji de lao
dang'an li xie de guadeng xisu' = archive family v10 + slogan-ish zero-scene R442;
line14 'zhe jieri deng yi gua, ganjue rizi you tashi le jifen' = lamp x settled-days
isomorph v21 strongest (R1008 note carried) + lamp face. THIS line16 = 'lao wujian li
cangzhe gushi' = the ONLY FREE row with ZERO machine word-face flag on probe words
(lao-wujian/cangzhe/gushi; r1014_quote_face.txt) and ZERO seasonal wording and ZERO
four-char collision and NON-lamp face (second non-lamp after v44 = anti-homogenization
variation continuation). Honest notes carried: 'cangzhe' = v10 'dang'anguan li
CANGZHE de' same-axis same-bucket two-char construct-layer adjacency (v10 =
institutional-cabinet face vs THIS = personal-object face = same-family different-scene
row; nostalgia-axis memory-carrier band third face: v10 archive-house + v39 lamp-sea +
THIS old-objects); gazing-face abstractness note ('gushi' general-word = weaker concrete
scene than v44 breakfast face, R1008 v39 gazing-face same-type honest note); zero
explicit festival word = festival bucket catalog = holiday generic face (v38/v44
precedent), day-match compensation = date line '2026-10-02 - National Day holiday' +
holiday at-home rummaging scene framing. Scene layer: National-Day day-2 holiday at
home, nostalgic residents rummage bottom-of-trunk old objects, palm-rubbing and
saying old-objects-hold-stories = holiday at-home memory scene (R442 weakness
prescription band; second non-lamp face of the series run). Built-in tension: WU x SHI
axis-internal self-contrast (thirty-first consecutive variant): the most nostalgic
residents locate the city's living stories not in archives or lamp seas but in the
oldest palm-worn objects they keep = the oldest container holds the liveliest story
(carrier-register exclusive note: the archive locks memory in cabinets, the lamp sea
acts the old days out on streets - only the nostalgic knows stories also sit quietly
in every palm-polished old object). Living-city proof = a city that keeps its old
objects is a city whose stories stay touchable (city humane-accumulation order echo).
Line-level freshness forty-second proof = same-axis-different-line fortieth proof.
Quote verbatim + card framing (R285 QUOTE precedent). Layout = QUOTE-v2 params
verbatim; h2_size stays 60 zero-template default (quote line 10.00em into 60-band
budget 15.33em margin +5.33em = v42 10.40em +4.93em same-band precedent). Machine
source/dedup assertions (R456 system, card-face level R1010). All output UTF-8.
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src", "render"))
from render_card_video import _line_cost, wrap_for_width  # noqa: E402

BASE = os.path.join(ROOT, "data", "storylines", "cards")
QV2 = os.path.join(BASE, "MC-20260925-QUOTE-v2")
V45 = os.path.join(BASE, "MC-20261002-DAILY-v45")
TMP = V45 + "-tmp"
os.makedirs(V45, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

QUOTE_CORE = u"老物件里藏着故事"
AXIS, BUCKET, IDX = u"怀旧", u"festival", 16

# --- machine source assertions (R456: pool verbatim + card-face-level fleet dedup R1010 law)
pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
fest = pool["axes"][AXIS][BUCKET]
assert len(fest) == 18, "festival bucket != 18 lines"
assert fest[IDX] == QUOTE_CORE, "pool line mismatch: %r" % fest[IDX]
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
assert QUOTE_CORE not in spirit, "line already consumed by city-spirit harvest"

# --- quote-face word probe (r1014_quote_face.txt evidence file; honest-adjacency law)
probe_words = [u"老物件", u"藏着", u"故事"]
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg2 = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg2.get("cards", []))
        sq = cfg2.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
qrep = [u"r1014 quote-face word probe for candidate " + QUOTE_CORE]
for w in probe_words:
    hits = sorted(d for d, (f, sq) in faces.items() if w in f or w in sq)
    qrep.append(u"word [%s] -> %s" % (w, u",".join(hits) if hits else u"ZERO fleet card-face hits"))
io.open(os.path.join(TMP, "r1014_quote_face.txt"), "w", encoding="utf-8").write(u"\n".join(qrep))

for d in sorted(os.listdir(BASE)):
    if os.path.join(BASE, d) == V45:
        continue  # self-exclusion: current piece's own cards.json (re-runnability)
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        # card-face-level scan (R1010 corrected law): lines + source_quote; whole-file meta
        # narrative false hits do NOT count as consumption.
        assert QUOTE_CORE not in face and QUOTE_CORE not in sq, "line already consumed by %s" % d
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
# DAILY-v32 yanhuo/festival/10 + DAILY-v33 huaijiu/festival/4 + DAILY-v34 xiaqi/festival/9 +
# DAILY-v35 zhixu/festival/11 + DAILY-v36 xiaoyao/festival/16 + DAILY-v37 qiuxin/festival/5 +
# DAILY-v38 yanhuo/festival/5 + DAILY-v39 huaijiu/festival/5 + DAILY-v40 xiaqi/festival/11 +
# DAILY-v41 zhixu/festival/17 + DAILY-v42 xiaoyao/festival/13 + DAILY-v43 qiuxin/festival/9 +
# DAILY-v44 yanhuo/festival/1 + REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 +
# zhixu/festival/14 (source_facts) + city-spirit v1.2 festival-scene trio zhixu/festival/16 +
# qiuxin/festival/14 + xiaqi/festival/0 (#47/#53/#59).

cfg = json.load(io.open(os.path.join(QV2, "cards.json"), encoding="utf-8"))

LINES = [
    u"城市日签 045",
    u"2026-10-02 · 国庆假期",
    u"「老物件里藏着故事」",
    u"——硅基城市台词池 · 怀旧轴",
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
assert H2_SIZE == 60, "em ladder expected 60-band zero-template default (quote line 10.00em into 60-band budget 15.33em margin +5.33em = v42 10.40em +4.93em same-band precedent), got %d" % H2_SIZE

meta = cfg["meta"]
meta["topic"] = "MC-20261002-DAILY-v45"
meta["form"] = (u"DAILY 城市日签 045（L-卡 图文轻内容线 DAILY 形态第四十五件·charter v1.2 §4 形态码 DAILY·"
                u"queue §E E30 standby 续领 R1014·日签节律续件=日期×情境桶对位判据第四十五证〔festival 桶当日"
                u"直配系列化·桶级=节日情境与当日唯一对位·10-02=国庆假期第 2 日·场景级=假日居家翻检老物件面如实"
                u"注记〔灯面之外的假日记忆面·v44 早市晨面后第二件非灯面=反同构变奏续证·R442 系列同构弱点正面处方"
                u"·日期行「2026-10-02 · 国庆假期」承节日面〕〕+六轴收官后线级新鲜度第四十二证=同轴异行第四十证"
                u"〔怀旧轴 DAILY-v2〔line0〕+DAILY-v10〔line3〕+DAILY-v16〔line1〕+DAILY-v22〔line12〕+DAILY-v25"
                u"〔line17〕+DAILY-v33〔line4〕+DAILY-v39〔line5〕之外线级新鲜行 line16·轮前 r1014_pool.txt "
                u"怀旧桶 FREE 行预检=R978 拦截教训执行·v39 行已 USED 复核〕+旋转律兑现=v44 后计数求新 8/怀旧 7/"
                u"侠气 7/烟火 8/秩序 7/逍遥 7=四轴并列最少（怀旧/侠气/秩序/逍遥）→并列面最久未采回补=怀旧〔v39 "
                u"后 5 件未采·v40-v44 五件皆他轴=并列轴中最长回补距〕·FREE 面内容强度择优如实注记〔怀旧 FREE 面"
                u"逐行机核排除：line6/8/15=年味措辞三行 R972 季相排除〔+line8/15 挂上灯笼/灯笼一挂 v21 四字直撞"
                u"+灯笼八件饱和〕/line13「年年挂灯，年年有余」=过年祝福族年味邻接回避〔R1002 注记承继〕/line7"
                u"「旧伞上哪怕有个小破洞，也遮得住春雨」=春雨季相+伞族 v22 双拦截〔R1008 注记承继〕/line2「修伞"
                u"的手艺活儿，如今可真是少了」=伞 v22+手艺活儿 v23 双词面直撞+零节日钩/line9「这布灯的手艺，传了"
                u"几辈子」=手艺 v23+传代 v14 双邻接〔R1008 注记承继〕+灯面回归=反同构背刺/line10「看这红彤彤的，"
                u"心里也暖和」=心里也暖和 v24 词面直撞=灯→心暖 causation 最强重复面〔R1008 注记承继〕/line11"
                u"「记得老档案里写的挂灯习俗」=档案族 v10+口号化零场景 R442/line14「这节日灯一挂，感觉日子又踏实"
                u"了几分」=挂灯×日子踏实 v21 同构=最强同构面〔R1008 注记承继〕+灯面；本行 line16=「老物件里藏着"
                u"故事」=FREE 面唯一零机核词面旗行〔老物件/藏着/故事=fleet 卡面+source_quote 扫描·probe 词面"
                u"r1014_quote_face.txt 机核〕+零季相词+零四字直撞+非灯面〔v44 后第二件非灯面=反同构变奏续证〕+"
                u"「藏着」诚实邻接注记=v10「档案馆里藏着」同轴同桶两字构式层邻接〔R1012「星星」两字 motif 邻接"
                u"同律=构式层如实注记非主题族重复·v10=机构柜存面 vs 本行=随身物件面=同族异质行·怀旧轴记忆载体"
                u"带第三面〔v10 档案馆面+v39 灯火面+本行=老物件面〕〕+凝视面抽象度诚实注记=「故事」泛化词"
                u"具象场景弱于 v44 早市面〔R1008 v39 凝视面同型注记·M6 校准位〕+零显性节日钩〔festival 桶编目="
                u"节日通用面·v38/v44 零节日钩先例·假日居家翻箱记忆面场景补偿〕〕）")
meta["source_quote"] = u"「老物件里藏着故事」"
meta["source_pointer"] = (u"life/BigLife/cognition/pools.json 台词池 axes[怀旧][festival][16]（6 轴×12 情境桶×18 行"
                           u"=1296+sprite 顶层 144=1440 行·BigLife R982 窗结构重构 sprite 轴移顶层·内容零变实锚·"
                           u"跨仓只读指针）+data/intel/daily/2026-10-02.md（当日日期语境源·国庆假期第 2 日="
                           u"DAILY-v1~v44 当日件同窗语境）")
meta["source_facts"] = (u"日签纪实抽取律：①引文=台词池 axes[怀旧][festival][16] verbatim 零改字（「」=卡面排版层"
                         u"〔R285 QUOTE v2 先例〕·build 脚本内断言=池行逐字在位实锚）②日期行 2026-10-02=当日"
                         u"历法事实·国庆假期=假期第 2 天（daily brief 2026-10-02 当日窗语境）③情境=festival 情境"
                         u"桶当日直配（12 桶中节日情境与当日唯一对位·DAILY-v1~v44 同桶直配第四十五证=日签节律判据"
                         u"系列化·国庆假期第 2 日居家翻检老物件=假日记忆面场景对位〔场景级如实注记：灯面之外的"
                         u"假日居家物件面〕）④池级署名=台词池行无居民名〔人设权红线零接触·charter §2.4〕⑤去重"
                         u"断言=本行不在 city-spirit.md 64 条已采面+不在全成品卡面 lines/source_quote 任一（卡面级"
                         u"实扫=R1010 修正律·DAILY-v1〔求新/4〕+DAILY-v2〔怀旧/0〕+DAILY-v3〔侠气/5〕+DAILY-v4"
                         u"〔烟火/4〕+DAILY-v5〔秩序/4〕+DAILY-v6〔逍遥/3〕+DAILY-v7〔求新/7〕+DAILY-v8〔侠气/13〕+"
                         u"DAILY-v9〔求新/12〕+DAILY-v10〔怀旧/3〕+DAILY-v11〔烟火/13〕+DAILY-v12〔逍遥/15〕+"
                         u"DAILY-v13〔侠气/2〕+DAILY-v14〔求新/3〕+DAILY-v15〔求新/11〕+DAILY-v16〔怀旧/1〕+"
                         u"DAILY-v17〔秩序/12〕+DAILY-v18〔逍遥/1〕+DAILY-v19〔烟火/3〕+DAILY-v20〔侠气/1〕+"
                         u"DAILY-v21〔秩序/6〕+DAILY-v22〔怀旧/12〕+DAILY-v23〔求新/13〕+DAILY-v24〔烟火/2〕+"
                         u"DAILY-v25〔怀旧/17〕+DAILY-v26〔侠气/10〕+DAILY-v27〔烟火/7〕+DAILY-v28〔秩序/9〕+"
                         u"DAILY-v29〔逍遥/2〕+DAILY-v30〔秩序/2〕+DAILY-v31〔逍遥/4〕+DAILY-v32〔烟火/10〕+"
                         u"DAILY-v33〔怀旧/4〕+DAILY-v34〔侠气/9〕+DAILY-v35〔秩序/11〕+DAILY-v36〔逍遥/16〕+"
                         u"DAILY-v37〔求新/5〕+DAILY-v38〔烟火/5〕+DAILY-v39〔怀旧/5〕+DAILY-v40〔侠气/11〕+"
                         u"DAILY-v41〔秩序/17〕+DAILY-v42〔逍遥/13〕+DAILY-v43〔求新/9〕+DAILY-v44〔烟火/1〕+"
                         u"REACT-v8 同桶三行〔逍遥/17+烟火/12+秩序/14〕+city-spirit v1.2 节日场景三行〔秩序/16+"
                         u"求新/14+侠气/0〕皆非本行=线级新鲜度第四十二证·本行=怀旧轴 line16 非 DAILY-v2 line0 非 "
                         u"DAILY-v10 line3 非 DAILY-v16 line1 非 DAILY-v22 line12 非 DAILY-v25 line17 非 DAILY-v33 "
                         u"line4 非 DAILY-v39 line5=同轴异行第四十证〔六轴收官后怀旧轴第八采·轮前 r1014_pool.txt "
                         u"怀旧桶 FREE 行预检=R978 拦截教训执行〕+「老物件」「藏着」「故事」probe 词面机核"
                         u"〔r1014_quote_face.txt〕⑥季相核=本行无年味/春联/春雨类季相错位词〔R972 制·怀旧面 line6/8/13/"
                         u"15 年味行已按季相律排除·老物件=全季相公共记忆措辞与国庆假日时点对位〕⑦品牌语感注="
                         u"「藏着」大众口语动词真感〔去 AI 感对位〕+怀旧轴〔最爱念旧·最爱往年时光〕×老物件藏着"
                         u"故事〔最念旧的人把城市的活故事寄存在最旧的物件里〕=物×事金句位+国庆假期第 2 日居家"
                         u"翻检老物件场景层〔R442 审计叙事弱点处方带·v44 晨市面后第二件非灯面=反同构续证〕")
meta["attribution_rule"] = (u"署名=池级+轴级（台词池·怀旧轴）——池行无逐民署名·禁虚构居民名（charter v1.2 "
                             u"署名律+人设权红线·翻检老物件的怀旧轴居民=群像称谓面非登记居民名）")
meta["triple_label"] = (u"虚实级+来源级=图内底部行（subs.srt 烧录）「引文取自硅基城市台词池（虚构城市档案）」；"
                         u"AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）")
meta["editorial_value"] = (u"日签形态=日期戳+当日情境+池句三件编辑选材面（festival 桶当日直配第四十五证+四轴"
                            u"并列最少最久未采回补=怀旧赎回〔v39 后 5 件首回〕+FREE 面逐行机核排除注记后本行胜出"
                            u"〔唯一零机核词面旗行·「藏着」v10 构式层诚实邻接注〕+「老物件里藏着故事」〔最旧的东西"
                            u"里装着最活的故事〕物×事轴内自反差金句位〔族三十一连·载体语感独占注：档案馆把记忆锁"
                            u"进柜子、灯海把当年演在街上——只有最爱念旧的人知道，最旧的老物件不声不响，里面揣着"
                            u"最活的故事〕+假日居家翻检老物件场景层=R442 审计处方带续证+v44 后第二件非灯面=反同构"
                            u"变奏续证+「藏着」大众口语动词=人味命中〔CEO 审美线对位·城市人文积累令对位·故事摸得"
                            u"着=城市记忆可触摸面〕）+语录卡线变体零新模板第四十五证（QUOTE-v2 参数 verbatim 复用·"
                            u"h2_size 60 零模板默认档直配〔10.00em 引文行入 60 档预算 15.33em margin +5.33em="
                            u"v42 10.40em +4.93em 同档先例〕·charter §1「日签变体随时可续」兑现）·公众号低创作度"
                            u"条款 7.1-7.4 编辑价值面·charter §5 自动化合规上限")
meta["hit_chain_m0"] = (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链：怀旧轴〔最爱念旧·最爱往年时光〕×老物件"
                          u"藏着故事〔最念旧的人把城市的活故事寄存在最旧的物件里〕=物×事轴内自反差金句位〔族"
                          u"三十一连〕+国庆假期第 2 日居家翻检老物件场景层+「藏着」口语动词真感/情 1 假日念旧温情"
                          u"共鸣如实非强极点/时 2 当日时点=国庆假期第 2 日居家记忆面直配+festival 情境桶直配第"
                          u"四十五证〔桶级·场景级假日物件面注记〕/台 2 公众号方图承载=MC-001~129 S3 实证复用）"
                          u"——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·charter §4 形态码 DAILY·"
                          u"queue §E E30 R1014 续领")
meta["red_line"] = (u"aigc_notice 烧录每帧（CONSTITUTION S2-4）；池句=情境口气零事实宣称（台词池=虚构城市档案·"
                     u"REACT 系列同源先例）；无居民名=人设权红线零接触（翻检老物件的怀旧轴居民=群像称谓面非登记"
                     u"居民名）；脱敏律=池句无令牌号/无个体可识别面/零金钱数额（老物件=公共记忆意象非个体档案面·"
                     u"无品牌无价格=零消费宣称）；成品只入库·发布=M5 账号物理件+M4 全绿")
meta["line"] = u"L-卡 图文轻内容线（DAILY 形态第四十五件·charter v1.2 §4 形态码 DAILY·日签节律续件）"

cfg["font"]["h2_size"] = H2_SIZE
cfg["cards"][0]["lines"] = LINES
cfg["cards"][0]["start"] = 0.0
cfg["cards"][0]["end"] = 2.6

# --- machine em check (R301-R313 precedent + R381 vertical law)
report = []
ok = True
budget_h1 = (frame_w - 160) / float(h1_size)
budget_h2 = (frame_w - 160) / float(H2_SIZE)
report.append("pool assert: axes[huaijiu][festival][16] verbatim OK; festival bucket=18 lines; card-face-level fleet dedup OK (R1010 law: lines+source_quote scan; city-spirit NOT_IN pre-check + all cards.json incl DAILY-v1..v44 + REACT-v8 same-bucket trio + city-spirit v1.2 festival trio; line-level freshness forty-second proof: huaijiu line16 != DAILY-v2 line0 != DAILY-v10 line3 != DAILY-v16 line1 != DAILY-v22 line12 != DAILY-v25 line17 != DAILY-v33 line4 != DAILY-v39 line5 = same-axis-different-line fortieth proof; quote-face word probe: lao-wujian/cangzhe/gushi see r1014_quote_face.txt; strongest-exclusion rows machine-proven: line6/8/15 nian-wei seasonal (R972); line8/15 guashang-denglong 4-char v21; line13 nian-nian-you-yu nian-wei adjacency; line7 chunyu seasonal + san v22; line2 san v22 + shouyi-huor v23; line9 shouyi v23 + generational v14; line10 xinli-nuanhe v24; line11 archive v10; line14 lamp-x-tashi isomorph v21")
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
report.append("LADDER_STAY_60: quote line 10.00em into 60-band budget 15.33em margin +5.33em (v42 10.40em +4.93em same-band precedent); all other QUOTE-v2 params verbatim")
io.open(os.path.join(TMP, "em-check-r1014.txt"), "w", encoding="utf-8").write("\n".join(report))
assert ok, "em budget FAIL - see report"

json.dump(cfg, io.open(os.path.join(V45, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
io.open(os.path.join(V45, "subs.srt"), "w", encoding="utf-8", newline="\n").write(
    "1\n00:00:00,000 --> 00:00:02,600\n" + SUBS_LINE + "\n")

# --- E4 audience reference call (async detached, 1500s window, v44 same-round pattern; fired at
# --- build time so a hot-loaded model can land same round; backfill per R870->R871 precedent)
subprocess.Popen(["python", os.path.join(TMP, "e4_call.py")], cwd=TMP,
                 creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("BUILD OK h2_size=%d (ladder stay 60 zero-template default, quote 10.00em driver) + E4 fired async" % H2_SIZE)
