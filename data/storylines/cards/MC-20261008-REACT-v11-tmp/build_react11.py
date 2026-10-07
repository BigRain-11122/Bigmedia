# -*- coding: utf-8 -*-
"""build_react11.py - MC-20261008-REACT-v11 M1 build with machine assertions.

R1676 production round (day-boundary batch). REACT hot-city-reaction card 011.
Sources (verbatim, zero-rewrite):
  hot      : zhihu-hot #8 2026-10-08, single-row title (no comma split)
  reactions: BigLife pools.json coldsnap bucket, three distinct axes (first
             coldsnap card-face use in REACT series - fresh bucket)
  creed    : census anchor C-00016 (canteen chef) creed
Machine checks: pool/anchor/daily verbatim, fleet dedup (R1010 exact),
em pre-fit ladder (largest feasible h2_size, zero-margin exclusion),
VERT budget (R381).
"""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PIECE = HERE[:-4] if HERE.endswith("-tmp") else HERE
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(PIECE))))
POOL = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
ANCHOR = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00016.md"
DAILY = os.path.join(ROOT, "data", "intel", "daily", "2026-10-08.md")

HOT_FULL = u"世界上最宜居的城市是哪一座？"
HOT1 = HOT_FULL  # single-row title: no comma clause in verbatim source
R1 = u"街坊邻居得互相照应，这日子才过得多舒心"          # 侠气/coldsnap
R2 = u"早点摊上的粥，比啥都管用"                        # 烟火/coldsnap
R3 = u"热茶暖身又暖心，寒风中多一分闲适"                # 逍遥/coldsnap
CREED = u"行情再绿，汤是热的。"
SERIES = u"城市速报 011"
SRCROW = u"今日热点 · 知乎热榜 2026-10-08"
SUBS = u"热点转述自知乎热榜·反应与信条皆取自虚构城市档案"

# --- 1) source verbatim assertions
pools = json.load(io.open(POOL, encoding="utf-8"))
assert R1 in pools["axes"]["侠气"]["coldsnap"], "R1 not verbatim in 侠气/coldsnap"
assert R2 in pools["axes"]["烟火"]["coldsnap"], "R2 not verbatim in 烟火/coldsnap"
assert R3 in pools["axes"]["逍遥"]["coldsnap"], "R3 not verbatim in 逍遥/coldsnap"
anchor = io.open(ANCHOR, encoding="utf-8").read()
assert CREED in anchor, "creed not verbatim in C-00016"
daily = io.open(DAILY, encoding="utf-8").read()
assert HOT_FULL in daily, "hot title not verbatim in daily brief"

# --- 2) fleet dedup (R1010 exact-line; self dir excluded)
cards_dir = os.path.join(ROOT, "data", "storylines", "cards")
for d in sorted(os.listdir(cards_dir)):
    if not d.startswith("MC-") or d.endswith("-tmp"):
        continue
    cj = os.path.join(cards_dir, d, "cards.json")
    if not os.path.exists(cj):
        continue
    c = json.load(io.open(cj, encoding="utf-8"))
    for card in c.get("cards", []):
        for ln in card.get("lines", []):
            for cand, tag in [(R1, "R1"), (R2, "R2"), (R3, "R3")]:
                assert cand not in ln, "R1010 exact collision %s vs %s: %s" % (tag, d, ln)

# --- 3) em pre-fit (ladder: largest feasible, zero-margin exclusion)
def em_cost(ch):
    o = ord(ch)
    if o >= 0x2E80:
        return 1.0
    if ch in (" ", "\t"):
        return 0.5
    return 0.55

def width(s):
    return sum(em_cost(ch) for ch in s)

CANVAS = 1080
MARGINS = 160
AVAIL = CANVAS - MARGINS  # 920px
H1_SIZE = 84
H2_SIZE = 36               # selected ladder step (38 excluded by driver row)
SUBS_SIZE = 38
LINE_SPACING = 12
H1_GAP = 36
OPTICAL_CENTER = 0.24
SUBS_BOTTOM = 110

rows = [
    SRCROW,
    HOT1,
    u"侠气轴：「%s」" % R1,
    u"烟火轴：「%s」" % R2,
    u"逍遥轴：「%s」" % R3,
    u"食堂大厨信条：「%s」" % CREED,
]
h1_w = width(SERIES)
assert h1_w <= AVAIL / H1_SIZE, "H1 over budget"
budget38 = AVAIL / 38.0
driver_w = max(width(r) for r in rows)
assert driver_w == width(u"侠气轴：「%s」" % R1), "driver row is not R1 row"
assert width(u"侠气轴：「%s」" % R1) > budget38, "38-step not excluded: ladder selection broken"
budget = AVAIL / H2_SIZE
lines_out = ["em-check-r1676 (REACT-v11 M2 front-fit + VERT R381)"]
lines_out.append("h2_size=%g budget=%.2fem  H1=%.2fem" % (H2_SIZE, budget, h1_w))
for r in rows:
    w = width(r)
    assert w <= budget - 0.2, "zero-margin exclusion: %s (%.2fem)" % (r, w)
    lines_out.append("OK %.2fem margin +%.2f  %s" % (w, budget - w, r))
subs_w = width(SUBS)
subs_budget = AVAIL / float(SUBS_SIZE)
assert subs_w <= subs_budget, "subs row over budget"
lines_out.append("subs %.2fem < %.2fem budget OK" % (subs_w, subs_budget))
# VERT (R381): pitch = 1.35*size + spacing, stack bottom must clear subs top by >=20px
h1_block = 1.35 * H1_SIZE + H1_GAP
h2_pitch = 1.35 * H2_SIZE + LINE_SPACING
est_bottom = CANVAS * OPTICAL_CENTER + h1_block + len(rows) * h2_pitch
subs_top = CANVAS - SUBS_BOTTOM - SUBS_SIZE
gap = subs_top - est_bottom
assert gap >= 20, "VERT gap %d < 20px" % gap
lines_out.append("VERT: est bottom=%.0fpx subs_top=%dpx gap=%dpx OK (assert >=20)" % (est_bottom, subs_top, gap))
lines_out.append("ALL-HORIZ: PASS  VERT: PASS")

# --- 4) write piece files
meta = {
    "topic": "MC-20261008-REACT-v11",
    "line": u"L-卡 图文轻内容线（REACT 形态第十一件·charter v1.2 §4 形态码·#59 按日热点随轮领）",
    "form": u"REACT 热点城市反应版 011（L-卡 P0 形态·L5 城市响应层媒体供给件·#59 按日热点随轮领第十续件·R309 双律复用·热点择优判据第十一证=映射对位优先于纯热度·城市主题本司域直配位——知乎源线第 9 用）——知乎热榜热点转述×硅基城市台词池 coldsnap 情境桶反应（系列首用=四新鲜桶破一）×食堂大厨信条收束",
    "tool": "src/render/render_card_video.py --poster（C-27 静态帧路）",
    "source_facts": (u"热点转述律+反应抽取律 R309 双律复用：①热点行=知乎热榜 2026-10-08 第 8 条标题 verbatim 全题转述"
        u"（零裁零改字·单问句完整·全池唯一单行热点=短题不拆行设计〔v1-v10 跨两行排版为长题设计位·本件 15 字单行零折行〕）"
        u"·来源=data/intel/daily/2026-10-08.md zhihu-hot 第 8 条·知乎源线第 9 用"
        u"②反应行=BigLife 台词池 coldsnap 情境桶 verbatim 三条轴位映射（侠气「街坊邻居得互相照应，这日子才过得多舒心」"
        u"／烟火「早点摊上的粥，比啥都管用」／逍遥「热茶暖身又暖心，寒风中多一分闲适」——**coldsnap 桶=系列卡面首用"
        u"〔四新鲜桶 dusk/typhoon/coldsnap/ceo_order 破一·v1-v10 卡面实引账=rain/market_open/market_close/weekend×2/"
        u"morning×2/night/festival/heatwave（r1676_react_probe3.txt 机核）〕·单桶纪律=宜居之问→天冷试城情境〔编辑定谳="
        u"宜居不在天气在人心——寒流是宜居的试金石：榜上宜居城市多以气候宜人立论，寒流一来才见真宜居=街坊照应/热粥/"
        u"闲适三答案·映射对位判据=三轴一一对应宜居三面（社区互助面/日常温饱面/从容心境面）〕·三轴全 on-argument"
        u"·三句结构全异质（因果论证句/比较判断句/并列递进句·零人称口气句执行）·**三行全 CLEAN=R1010 卡面级"
        u" exact-line 探针零命中**〔build 断言·120 件全扫〕）③收束行=万人卡 C-00016 食堂大厨信条 verbatim"
        u"「行情再绿，汤是热的。」（食堂大厨·职业级署名=REACT 署名律兼容·已登记字段 verbatim 零新增人格·人设权红线照守"
        u"·温饱域=宜居答案同域锚〔题眼：宜居的终极答案不是气候不是收入，是无论世界怎么波动，城里那碗汤是热的="
        u"确定性温暖=宜居金标准〕·**信条速报形态复用链第六续件**〔v6 C-00015/v7 C-00013/v8 C-00028/v9 C-00010/"
        u"v10 C-00019 后第六续·C-00016 信条=REACT 收束位首用·CENSUS 互证位先例=v9 绿盘日免费例汤「给喝的」对应位"
        u"=跨形态信条复用链 by-design〕）④城志互证锚注记=C-00010 数据粥铺摊主（「灶上留一壶，路过的都是客」="
        u"灶火待客 warmth 族对应位·v9 收束位↔v11 互证位镜像对称·非收束位不引信条）"),
    "source_pointer": (u"data/intel/daily/2026-10-08.md（热点源·当日一份为真相）"
        u"+life/BigLife/cognition/pools.json 台词池 coldsnap 桶（跨仓只读·池句=情境口气零事实）"
        u"+life/BigLife/census/anchors/C-00016.md 万人卡手写锚（跨仓只读·信条字段 verbatim·非荣誉席）"),
    "attribution_rule": (u"署名=轴级/职业级（侠气轴/烟火轴/逍遥轴/食堂大厨·charter v1.2 署名律禁虚构居民名·人设权红线照守）；"
        u"热点=平台热榜转述（知乎热榜 2026-10-08 第 8 条·热度 322 万元数据只入 README 记账不入卡面·转述面合规="
        u"逐条来源链+不标题党+verbatim 全题零改字）"),
    "triple_label": (u"虚实级+来源级＝图内双落（subs.srt 底部行「热点转述自知乎热榜·反应与信条皆取自虚构城市档案」——"
        u"热点=现实转述·反应与信条=虚构城市档案两态声明·池与户籍卡双虚构源并落·R575 扩展版）"
        u"+AIGC 角标＝常驻每帧 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械方括号体）"),
    "editorial_value": (u"速报体裁+轴位映射=编辑选材面（coldsnap 桶候选→3 轴位对位判断：侠气=社区互助位直配"
        u"〔「街坊邻居得互相照应，这日子才过得多舒心」=「哪一座宜居」的社区软基建答案位·「舒心」=宜居市民语直配"
        u"·因果论证句结构〕／烟火=日常温饱位直配〔「早点摊上的粥，比啥都管用」=宜居的日常饮食暖答案位·「比啥都管用」="
        u"价值排序判断·比较判断句结构〕／逍遥=从容心境位直配〔「热茶暖身又暖心，寒风中多一分闲适」=宜居的精神从容"
        u"答案位·「闲适」=宜居同义词·并列递进句结构〕）+食堂大厨信条收束（宜居之问×「行情再绿，汤是热的。」="
        u"确定性温暖金句级收束〔题眼：宜居的终极答案不在气候榜在人心暖——外部世界怎么波动，城里那碗汤是热的〕"
        u"+跨形态信条复用链第六续件〔C-00016 温饱域=宜居答案同域居民档案〕+城志互证=C-00010 数据粥铺摊主"
        u"「灶上留一壶」warmth 族对应位）+系列「城市速报」与「城市语录」「城市图鉴」「城市盘点」「城市日签」平行"
        u"连载识别结构·编辑价值防低创作度 7.1-7.4（charter §5 自动化合规上限）；热点择优判据留痕=映射对位优先于"
        u"纯热度第十一证·**城市主题本司域直配位**（全池唯一「城市宜居」本域直问=硅基城市媒体身份的正主题）·"
        u"未选理由全量注记 19 条：**zhihu #1 孙颖莎 WTT 止步=具名当事人面回避〔零具名当事人律〕+体育赛果评论面**／"
        u"zhihu #2 C罗退出国家队=具名当事人面回避〔外国运动员·零具名律〕／zhihu #3 缅北电诈明珍珍死刑=政治敏感+"
        u"跨境执法面回避〔v9/v10 同族连三回避·判负留痕〕／zhihu #4 乒协赛场禁入名单=体育治理政策评论面回避〔v10 "
        u"教育部条同型·政策评论面〕／zhihu #5 余承东华为涨价=具名企业商务新闻面回避〔R909/R1299 具名企业口径维持·"
        u"v10 OPPO 同型〕／zhihu #6 俄罗斯鼠疫第二例死亡=健康宣称/疫情面回避〔健康宣称面回避律〕／zhihu #7 王星案"
        u"跨境人口贩卖=跨境犯罪敏感案件面+具名当事人面回避〔双回避〕／zhihu #9 清北牌子学术圈=具名机构+学术圈"
        u"评论面无桶〔教育评论面〕／zhihu #10 手性物质=硬核科普面无映射位〔无城市桶·R455 同型〕／bilibili #1/#5 "
        u"缅北电诈纪录片第三/二集=政治敏感面回避〔同 zhihu #3 族·双平台交叉不救敏感面〕／bilibili #2 改造善良老人"
        u"晚年=善意叙事内容面无城市事件锚〔vlog/纪实内容面〕／bilibili #3 道士下山上大学=宗教人物内容面回避〔宗教面〕／"
        u"bilibili #4 反向旅游陕西铜川=具名地区旅游内容面〔地区比较面风险+无事件锚·v10 树屋 vlog 同型〕／bilibili #6 "
        u"如来三界巡演 AI MV=具名宗教人物+音乐内容面〔R1030 音乐面+宗教面双回避〕／bilibili #7 少女前线2 PV=具名 IP "
        u"宣传面〔R909/R1030 影视/IP 宣传面族〕／bilibili #8 VCTCN 冠军赛单曲=音乐内容面〔R1030 注记维持〕／bilibili #9 "
        u"老师太显小=校园外貌内容面无事件锚／bilibili #10 马祖列岛旅行=涉台地域敏感面回避〔政治敏感面〕+旅游 vlog "
        u"无事件锚"),
    "hit_chain_m0": (u"M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔「世界上最宜居」=全球最高标准之问 vs 市民三答案="
        u"街坊照应/一碗热粥/一盏闲茶=最小日常答案·宏大之问×最小答案反差具象在场+「是哪一座」悬念缺口=给出非地理"
        u"答案的期待反转〕/情 1 温和共鸣非强极点〔G1 日常党+G5 城市生活家+安居乐业族直配对位〕/时 2 当日热点=速报"
        u"时效本体〔知乎热榜 2026-10-08 在飞〕/台 2 公众号方图承载=MC-001~158 S3 实证复用·速报=热点类大众流量面格式"
        u"（O-1327 research §2 #4 A 档通识·按 hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open）"),
    "aspect_note": u"1080×1080 公众号方图（S3 载体判断·规格窗随 M5 发布案复核）",
    "red_line": (u"aigc_notice 常驻每帧（CONSTITUTION S2-4）；红线律＝不标题党〔热点行=知乎热榜标题 verbatim 全题转述零改写"
        u"零加感叹〕／无来源不发布〔热点=知乎热榜+日期图内行·反应=台词池指针·信条=户籍卡 C-00016 指针 README 双落〕／"
        u"脱敏（热度 322 万元数据不入卡面=README 记账·零具名当事人·零仓位/密钥/token 量/未公开财务面）；政治敏感面回避律照守"
        u"（缅北电诈条×3/涉台马祖条/乒协政策条不选）；健康宣称面回避（鼠疫条不转述不背书）；成品只入库＝M5 账号物理件未开+M4 全绿前零发布"),
}

card = {
    "meta": meta,
    "video": {"width": 1080, "height": 1080, "fps": 30, "bg": "black"},
    "font": {
        "file": "C:/Windows/Fonts/msyh.ttc",
        "cards_size": 50,
        "subs_size": SUBS_SIZE,
        "subs_bottom": SUBS_BOTTOM,
        "aigc_size": 30,
        "line_spacing": LINE_SPACING,
        "h1_font": "C:/Windows/Fonts/msyhbd.ttc",
        "h1_size": H1_SIZE,
        "h1_color": "accent",
        "h2_size": H2_SIZE,
        "h2_color": "white",
        "h1_gap": H1_GAP,
        "optical_center": OPTICAL_CENTER,
    },
    "aigc_notice": "[AIGC·AI 生成内容]",
    "tail": 0.8,
    "cards": [
        {
            "start": 0.0,
            "end": 2.6,
            "lines": [SERIES, SRCROW, HOT1,
                      u"侠气轴：「%s」" % R1,
                      u"烟火轴：「%s」" % R2,
                      u"逍遥轴：「%s」" % R3,
                      u"食堂大厨信条：「%s」" % CREED],
        }
    ],
}

io.open(os.path.join(PIECE, "cards.json"), "w", encoding="utf-8").write(
    json.dumps(card, ensure_ascii=False, indent=1))
io.open(os.path.join(PIECE, "subs.srt"), "w", encoding="utf-8").write(
    u"1\n00:00:00,000 --> 00:00:02,600\n" + SUBS + u"\n")
io.open(os.path.join(PIECE, "em-check-r1676.txt"), "w", encoding="utf-8").write(
    "\n".join(lines_out) + "\n")
print("BUILD OK: cards.json + subs.srt + em-check-r1676.txt")
print("\n".join(lines_out))
