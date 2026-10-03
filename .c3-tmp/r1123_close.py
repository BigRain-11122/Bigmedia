# -*- coding: utf-8 -*-
# R1123 real-work night-window close: window closes (real work appeared), F-150 registrations + state + export
import io, json, os, datetime

root = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
now = datetime.datetime.now()
ts = now.strftime("%Y-%m-%d %H:%M:%S")

# --- 0) machine PNG/dir counts (F-150 disk-truth, v63 precedent)
BASE = os.path.join(root, "data", "storylines", "cards")
forms = {}
png_in_dirs = 0
dirs_by_form = 0
for d in sorted(os.listdir(BASE)):
    if os.path.isdir(os.path.join(BASE, d)) and d.startswith("MC-") and not d.endswith("-tmp"):
        for form in ("QUOTE", "DIGEST", "CENSUS", "REACT", "DAILY"):
            if ("-" + form + "-") in d:
                forms[form] = forms.get(form, 0) + 1
                dirs_by_form += 1
                break
        if os.path.isfile(os.path.join(BASE, d, d + ".png")):
            png_in_dirs += 1
flat_png = len([f for f in os.listdir(BASE) if f.endswith(".png") and os.path.isfile(os.path.join(BASE, f))])
lc_total = sum(forms.values())
print("FORMS %s lc=%d png_in=%d flat=%d png_total=%d" % (json.dumps(forms), lc_total, png_in_dirs, flat_png, png_in_dirs + flat_png))
assert lc_total == 112 and png_in_dirs + flat_png == 112, "disk count drift - see review F line"

V64 = os.path.join(BASE, "MC-20261003-DAILY-v64")
png = os.path.join(V64, "MC-20261003-DAILY-v64.png")
print("v64 png exists=%s size=%dB" % (os.path.exists(png), os.path.getsize(png) if os.path.exists(png) else -1))

# --- 1) finished.md F-150 block append
fin_p = os.path.join(root, "output", "finished.md")
f150 = (
u"\n**F-150 登记（R1123 夜窗生产轮）**——**L-卡 DAILY 城市日签系列第六十四件=成品库第一百五十件**："
u"MC-20261003-DAILY-v64《城市日签 064》全链走毕（queue §E E30 夜窗解锁兑现 R1123·声明窗 R1120-R1122 "
u"实活出现即收卷入本 commit〔os-protocol §6〕·产品优先律对位=2 分位实物=夜窗成品卡入库·24h 判负钟销账："
u"最后 2 分实物 R1095 F-149 13:0x→本件 17:37=4.5h）。素材源=BigLife 台词池 sprite[weekend][4] verbatim"
u"（引文「叮咚响夜晚」·**sprite 声部第五件+weekend 桶新跑第二件**〔声部五件内 weekend 二采=四件四桶零重复"
u"最强形（v50/v54/v61/v63）终结·诚实弱形注册·四连律远〕+**夜窗预登记链三重兑现**〔R1032 解锁窗「night-"
u"window rows（sprite/weekend/4+night-bucket residue）」→R1086 post-v63 供给注→R1122 夜窗候选注册〕+"
u"**夜窗 literal 对位**：日落 ~17:37 线后紧贴生产〔E4 fire 锚 17:37:00+渲染紧随=夜幕初上起点时刻·诚实注="
u"非深夜带（v51-v54 对照）〕×夜晚内容×weekend 假日桶（周六+国庆假期第 3 日夜）三重 literal〔R1020 night "
u"律〕+**拟声族带第三用定谳（R1122 注册裁量位·本轮 fresh 判）**：v50 叮叮当〔铃铛〕+v63 嗡嗡嗡〔蜂鸣〕+"
u"本件 叮咚〔门铃〕=三声三景三桶各异=第三用合法〔R1062 垂钓族带判例·三连同构律第四用起阻〕→post-v64 "
u"拟声族带第四用起阻注册+叮单字族带层邻接诚实注〔非 2+ 字 shingle 撞〕+六轴日间枯竭态承继〔R1032/R1086〕"
u"——build_daily_v64.py 机核断言全过（池行 verbatim+weekend 桶 12 行+sprite 12 桶结构〔R982〕+v63/v54 "
u"双结构锚+fleet 卡面级去重 R1010+city-spirit NOT_IN）+六词 probe 全零=r1123_quote_face.txt 系列第十二件"
u"全零邻接行。**MC-20261003-DAILY-v64.png（1080×1080 静态卡）全链走门全档**：M2 --poster exit 0+"
u"h2_size 60 档〔日期行 13.60em +1.73em 驱动·城市生灵署名行 13.65em +1.68em=v63 同带先例·em-check-"
u"r1123.txt 全行 OK·VERT gap +229px R381〕+验图五检 5/5 一次过（多模态转写六带逐字全中+五问全过）→M3"
u"「城市日签 064」四禁零中→M4 四检过（红线五条/三重标注图内双落/来源双落/编辑价值+人设权零接触=纯景句"
u"泛称零涉及+脱敏=无金钱无隐私无品牌）→M4.5 七席 6×9.0+E7 N/A（review-20261003-mcdaily-v64.md）——"
u"F-150=成品库第一百五十件·L-卡 第一百一十二件〔盘上机核单一真相：QUOTE 6+DIGEST 14+CENSUS 20+REACT 8+"
u"DAILY 64=112·PNG 实存 105+7 平置=112 全实存·F-149 行「114」=历史台账漂移承继 v63 判例如实注记〕·DAILY "
u"形态第六十四件·sprite 声部第五件——成品只入库不入发布队列（发布锁=M5 账号物理件+M4 全绿+AIGC 显著标"
u"识·未上线=未测量）。\n"
u"\nF-150 E4 回填（R1123 同轮回填追加制）：E4 参考仪 build 早发当轮落地 2026-10-03 17:37:00 **8.0**"
u"（会停明说〔设计与内容吸引人·节日气氛+城市生活+独特魅力正面〕+可能会保存或转发明说〔条件式〕+**打 8 分"
u"明说**；旗①=「一记门铃（最小问候）对上整座城的夜晚（最大回响舞台）」诗意刻意扣 1=**wrapper 背景段措辞"
u"位旗非卡面旗**〔卡面仅五字引文+署名行·旗句出自 wrapper 解读段=R231 ch.5 wrapper 措辞面先例·吸收位="
u"wrapper 校准位〕·最弱=虚构背景真实性〔合规行旗族=合规红线件不可删·吸收位=M5+系列语境〕·**DAILY 带读数"
u"注=v61/v62/v63/v64=8.0 四连企稳**·判词净本 expert-verdicts/20261003-173700-E4-audience.md·M4.5 七席"
u"终态=6×9.0+E4 8.0+E7 N/A·E4 参考仪非拦截席=MC-001 定标口径·带内候选维持）。\n"
)
with io.open(fin_p, "a", encoding="utf-8") as f:
    f.write(f150)
print("finished.md F-150 appended")

# --- 2) cards/README.md row append
cr_p = os.path.join(root, "data", "storylines", "cards", "README.md")
crow = (
u"\n- 2026-10-03: MC-20261003-DAILY-v64 登记（R1123·queue §E E30 夜窗解锁兑现·DAILY 形态第六十四件=日签节"
u"律续件=日期×情境桶对位判据第六十四证）——素材源=BigLife 台词池 sprite[weekend][4] verbatim（引文「叮咚响"
u"夜晚」·**sprite 声部第五件**〔城市生灵令 P-20260926-13 媒体面第五采·v50/v54/v61/v63 后第五采·**weekend "
u"桶声部内二采=四件四桶零重复最强形终结·诚实弱形注册**〕+**夜窗预登记链三重兑现**〔R1032 解锁窗→R1086 "
u"post-v63 供给注→R1122 夜窗候选注册〕+**夜窗 literal 对位**〔日落 ~17:37 线后生产×夜晚内容×weekend 假日"
u"桶三重 literal·夜幕初上起点时刻诚实注〕+**拟声族带第三用定谳合法**〔v50 叮叮当+v63 嗡嗡嗡+本件 叮咚=三"
u"声三景三桶各异·R1062 垂钓族带判例·post-v64 第四用起阻注册〕+六词 probe 全零=系列第十二件全零邻接行"
u"〔r1123_quote_face.txt〕+h2_size 60 档〔日期行驱动·em-check-r1123.txt〕+验图五检 5/5 一次过+M4.5 七席 "
u"6×9.0+E4 8.0 同轮回填〔wrapper 措辞位旗·DAILY 带四连企稳〕+**供给面诚实注**：sprite weekend 面零干净"
u"行耗尽〔weekend/3+4 双耗〕+六轴 R1032 枯竭注维持+post-v64 解锁窗=雨事件日/CEO 令日/10-08 复市/Nov+ 寒潮"
u"/夏季 heatwave/夜窗 sprite night 残面）→F-150（成品库第一百五十件·L-卡 第一百一十二件盘上机核）\n"
)
with io.open(cr_p, "a", encoding="utf-8") as f:
    f.write(crow)
print("cards README row appended")

# --- 3) queue section-E note append
q_p = os.path.join(root, "docs", "self-improvement-queue.md")
qrow = (
u"\n- 2026-10-03: **R1123 E30 夜窗解锁兑现=DAILY v64《城市日签 064》=F-150 登记（夜窗实活轮·声明窗 "
u"R1120-R1122 实活出现即收卷入·产品优先律对位=2 分位实物）**——sprite/weekend/4「叮咚响夜晚」三重预登记链"
u"兑现（R1032 解锁窗→R1086 供给注→R1122 夜窗候选注册）+两裁量 fresh 判=①literal-night 闸过（日落 ~17:37 "
u"线后生产·E4 锚 17:37:00）②拟声族带第三用合法（v50 叮叮当+v63 嗡嗡嗡+叮咚三声三景三桶各异=R1062 判例）"
u"→post-v64 拟声第四用起阻注册+sprite weekend 面零干净行耗尽注+六词 probe 全零（系列第十二件全零邻接行）"
u"+h2_size 60 档+验图 5/5+七席 6×9.0+E4 8.0 同轮回填（旗①=wrapper 措辞位非卡面·DAILY 带 v61-v64 四连企稳"
u"）——**随行 10-03 批 DIGEST v15 day-close 定谳=判负留痕**（orders L274-276 三行 CEO 派单全他司面 in-"
u"formation 未闭环+零 BS 份额+r1123 fresh 扫描 ledger mtime 15:15:33 冻结零新 BS 事件→非 A 级 BS 史源·池维"
u"持空·P-2026-09-28-02 判负留痕合法）——post-v64 指针：解锁窗维持=雨事件日/CEO 令日/10-08 market_open 复市"
u"/Nov+ 寒潮/夏季 heatwave/夜窗行（sprite night 残面 fresh scan）·E31 REACT-v9=10-04 日界轮（日报先补产·F "
u"预指位顺延 F-151·R978 判例 finished 顺序号=单一真相）/10-04 日界三件组（+#94 记忆梳理）/#70 OSS 窗 4="
u"10-05 21:40 开/W41 周轮件 10-05。\n"
)
with io.open(q_p, "a", encoding="utf-8") as f:
    f.write(qrow)
print("queue note appended")

# --- 4) E4 clean verdict archive
ev_dir = os.path.join(root, "expert-verdicts")
ev_p = os.path.join(ev_dir, "20261003-173700-E4-audience.md")
res = json.load(io.open(os.path.join(V64 + "-tmp", "e4-result.json"), encoding="utf-8"))
ev = (
u"# E4 参考仪判词净本 · MC-20261003-DAILY-v64《城市日签 064》（受众席·qwen2.5:14b·本地 Ollama 零 API token）\n\n"
u"> 起飞=build 早发（R1017 追加制先例·e4_call.py wrapper 复用改源）·落地 ts=" + res.get("ts", "") + u"\n"
u"> 材料=" + res.get("material", "") + u"\n\n## 判词（清洗后全文）\n\n"
+ res.get("verdict", "").strip() + u"\n\n## 台账读数\n\n8.0（会停明说+可能保存/转发条件式+打 8 分明说·"
u"旗①=wrapper 背景段措辞位旗非卡面旗〔R231 先例〕·最弱=虚构背景真实性=合规行旗族·DAILY 带 v61-v64 8.0 "
u"四连企稳·非拦截席=MC-001 定标口径）\n"
)
io.open(ev_p, "w", encoding="utf-8").write(ev)
print("E4 verdict archive written")

# --- 5) state.json close
P = os.path.join(root, "src", "os", "state.json")
line = (
u"2026-10-03 17:5x R1123: 生产轮·E30 夜窗解锁兑现 DAILY v64《城市日签 064》全链走门毕=F-150 登记（实活轮·"
u"声明窗 R1120-R1122 卷入本 commit 收窗〔os-protocol §6 实活轮出现即收〕·产品优先律对位=2 分位实物=夜窗成"
u"品卡入库·24h 判负钟销账：最后 2 分实物 R1095 F-149 13:0x→本件 17:37=4.5h）——①轮首五查静（fresh "
u"r1123_check.txt 17:35：orders 顶=O-20260928-1910 未动零新令/集团 orders mtime 12:39:57 冻结/ledger "
u"mtime 15:15:33 冻结零新转办/decisions 131==131 NEW=[]/无 index.lock/production=open/#86 三腿 "
u"supply-gated 持平〔pools 1440/interchat 22/C-00030 absent fresh 机证〕/GB 闸 10-01 ≤7 跳过/日报 10-03 "
u"在案不重跑）+三探针基线平（board 0 FAIL 5 题 10 稿/readiness 3 阻塞皆外部 CEO 面 0 findings/loop 3 "
u"FAIL+127 WARN 皆在案史实零新增〔account-lag beats1126>tick1122=+4 恒差承继·tick1123 收账自平口径〕）+"
u"**夜窗闸至=日落 ~17:37 线后生产（R1122 指针「literal night 至=夜窗轮 E30 DAILY v64 实活先至即收」兑现）**；"
u"②E30 夜窗候选 sprite/weekend/4「叮咚响夜晚」三重预登记链兑现（R1032 解锁窗→R1086 供给注→R1122 夜窗候选注"
u"册）+两裁量 fresh 判=literal-night 闸过（E4 fire 锚 17:37:00+渲染紧随=夜幕初上起点时刻·诚实注=非深夜带"
u"〔v51-v54 对照〕）+拟声族带第三用合法（v50 叮叮当+v63 嗡嗡嗡+叮咚=三声三景三桶各异=R1062 垂钓族带判例→"
u"post-v64 第四用起阻注册）+声部第五件 weekend 二采弱形诚实注+六词 probe 全零（系列第十二件全零邻接行·"
u"r1123_quote_face.txt）+build 机核断言全过（池行 verbatim+weekend 桶 12 行+sprite 12 桶〔R982〕+v63/"
u"v54 双结构锚+fleet 去重 R1010+city-spirit NOT_IN）；③M2 --poster exit 0（PNG 1080×1080+副产 mp4 69KB "
u"落 v64-tmp=R985 律）+h2_size 60 档（日期行 13.60em +1.73em 驱动·em-check-r1123.txt 全行 OK·VERT "
u"+229px R381）+验图五检 5/5 一次过（多模态转写六带逐字全中+零重叠零越界零截断/全行单行/来源行闭合/AIGC "
u"清晰/大留白分层）→M3「城市日签 064」四禁零中→M4 四检过→M4.5 七席 6×9.0+E7 N/A（review-20261003-"
u"mcdaily-v64.md）+**E4 参考仪 8.0 同轮回填**（17:37:00 热载快落·会停明说+可能保存/转发条件式+8 分明说·旗①="
u"wrapper 背景段措辞位非卡面〔R231 先例〕·最弱=虚构背景=合规行旗族·DAILY 带 v61-v64 四连企稳·净本 "
u"expert-verdicts/20261003-173700-E4-audience.md）→**F-150 登记**（成品库第一百五十件·L-卡 第一百一十二"
u"件盘上机核〔QUOTE 6+DIGEST 14+CENSUS 20+REACT 8+DAILY 64=112·PNG 105+7 平置=112 全实存·F-149 行 114="
u"历史台账漂移承继 v63 判例注〕）；④随行 day-close 定谳=10-03 批 DIGEST v15 候选判负留痕（orders L274-276 "
u"全他司 in-formation+零 BS 份额+ledger 冻结→非 A 级 BS 史源·池维持空·判负留痕合法·queue §E R1123 行）；"
u"⑤台账=review+finished F-150 两行+cards/README v64 行+queue §E R1123 行+status-export 刷（实况变化=新实"
u"物 F-150）+窗证据件 r1120-r1123 卷入；例行件：W40 周审在案·HQ-FEEDBACK 不写（无集团层本司 open 项·零膨"
u"胀）·tokens:local=1（E4 qwen2.5:14b=夜窗件受众参考仪·本地 Ollama 零 API token·P-54⑤ 计量律）。下轮=10-04 "
u"日界三件组（10-04 日报先补产→E31 REACT-v9 F-151+#94 记忆梳理）+夜窗续位（sprite night 残面 fresh "
u"scan）+W41 周轮件 10-05。收账显式列文件 commit+push。"
)
s = json.load(io.open(P, encoding="utf-8"))
s["tick"] = int(s.get("tick", 0)) + 1
s["ts"] = ts
s["task"] = ("R1123: " + line.split("R1123: ", 1)[1])[:60]
s.setdefault("log", []).append(line)
io.open(P, "w", encoding="utf-8").write(json.dumps(s, ensure_ascii=False, indent=2))
print("state updated tick=%s ts=%s" % (s["tick"], ts))

# --- 6) status-export refresh (P-61: real change = new artifact F-150)
E = os.path.join(root, "docs", "status-export.json")
ex = json.load(io.open(E, encoding="utf-8"))
ex["export_ts"] = ts
ex["outs"][0][1] = (
u"tick 1123，R1123=夜窗实活轮=E30 DAILY v64 夜窗解锁兑现 F-150 登记（三重预登记链+拟声第三用定谳+验图 "
u"5/5+七席 6×9.0+E4 8.0·声明窗 R1120-R1122 卷入收窗·并窗重置 0/6）。随行=10-03 批 DIGEST v15 day-close "
u"定谳判负留痕。下轮=10-04 日界三件组（REACT-v9 F-151 顺延+10-04 日报补产+#94 记忆梳理）+夜窗续位"
u"（sprite night 残面）+W41 周轮件 10-05。真发布=blocked-on-CEO 账号物理件·发布锁=M5 不变"
)
rkey = None
for k, v in ex.items():
    if isinstance(v, list) and v and isinstance(v[-1], list) and str(v[-1][0]) == "1119":
        rkey = k
        break
assert rkey, "results key not found"
ex[rkey].append(["1123",
    u"2026-10-03 17:5x R1123: 生产轮·E30 夜窗解锁兑现 DAILY v64《城市日签 064》全链走门毕=F-150 登记（实活"
    u"轮·声明窗 R1120-R1122 卷入 commit 收窗·产品优先律对位=2 分位实物·24h 判负钟销账 4.5h）——三重预登记链"
    u"兑现+两裁量 fresh 判（literal-night 闸过+拟声族带第三用合法 R1062 判例）+六词 probe 全零系列第十二件全"
    u"零邻接行+h2_size 60 档+验图 5/5+七席 6×9.0+E4 8.0 同轮回填+随行 10-03 批 DIGEST v15 day-close 定谳判负"
    u"留痕——详见 state.json log R1123 行"
])
ex["live"] = [
    [u"当前活：R1123 夜窗实活轮 commit 收窗（E30 DAILY v64 夜窗解锁兑现 F-150·声明窗 R1120-R1122 卷入）（%s）" % ts],
    [u"最近实物：data/storylines/cards/MC-20261003-DAILY-v64/MC-20261003-DAILY-v64.png（成品卡 F-150·L-卡 第一百一十二件·DAILY 形态第六十四件·sprite 声部第五件·2026-10-03 17:37）"],
    [u"下个里程碑：10-04 日界三件组（10-04 日报补产+E31 REACT-v9 F-151+#94 记忆梳理）+夜窗续位（sprite night 残面 fresh scan）+W41 周轮件 10-05——窗 ≤48h"],
]
io.open(E, "w", encoding="utf-8").write(json.dumps(ex, ensure_ascii=False, indent=1))
print("status-export refreshed (results key=%s)" % rkey)
print("CLOSE DONE")
