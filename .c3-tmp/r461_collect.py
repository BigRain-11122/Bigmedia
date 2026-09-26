# -*- coding: utf-8 -*-
# R461 collect (idempotent state guard + key-based results lookup, r460 pattern)
import io, json, os, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
now = datetime.datetime.now()
TS = now.strftime("%Y-%m-%d %H:%M:%S")
ISO = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
HM = now.strftime("%H:%M")

LOG = (
    u"2026-09-27 " + HM + u" R461: 生产轮·#67 DIGEST 续件第五件《城市盘点 006·深夜决策批数字盘点》全链走门毕"
    u"（R460 指针序首位领·claim 当轮闭环·D-20260927-01~05 史源）——"
    u"①轮首快速路径五查静（无新令 orders 双 NONE=r461_check/ledger 五模式正典同法 29=锚零新转办〔r461_check 首扫 0=口径偏离 r460_canon 正法当场定谳复跑 29〕"
    u"/decisions UTF8 非空行 45=锚零新行/树净零锁 HEAD=9627775 R460 收账开轮实取·无 bm-a 活跃写盘迹象"
    u"/日报 09-27 在案不重跑/C-00030 锚仍不在位 supply-gated 照守/storylines 三子域 09-27 零新写盘=bm-a 面）"
    u"→backlog 顶行序判：#59 REACT 09-28 窗未到/#63 锚不在位/#70 下窗 09-29 21:40 后开/#72 待 BigLife 台账"
    u"=R460 指针首位 #67 DIGEST 候选〔集团决策批 D-20260927-01~05〕成立非硬造→转全任务书认领；"
    u"②史源核验=深夜决策批五行 00:05 落档（FluxGroup/docs/decisions.md 跨仓只读·R444 收讫窗内回执）"
    u"+核心故事双源 verbatim：D-01⑦「技能动员令计数修正 5/8」（点名）vs 本仓 F-20260927-01「技能动员令计数应 6/8」"
    u"（自证·证据 9 件链）=编年史 A 级事件+数字密度（5 决/10 点/0 驳回/2 份额/9 证据/3 司）；"
    u"③全链=bigstream-lcard-pipeline 技能产线第六用：M0 四维分 7/8 A 档（钩 2 数字反差链 5/8 vs 6/8"
    u"=F-042 v2 对照结构同源第五证·五连母题〔v2 开闸/v3 三线/v4 技能/v5 节目重制/v6 对账夜〕）"
    u"→M1 纪实数字汇编律复用五源指针逐条可机核（引文双源 verbatim 对读=对账对话零改写）"
    u"→M2 出图 exit 0+验图五检 5/5 一次过初稿即正字（转写先行十行全中+靶向空间复验六项全过·"
    u"em 前置适配 h2_size 40=最长行 18.30em margin +4.70em〔44 档排除=垂直栈预算律驱动选档·VERT 律正用〕"
    u"·subs 19.0em<24.21em·em-check-r461.txt+垂直栈 R381 断言 +21px=v4/v5 同构七行 deck 初渲即过零修参）"
    u"→M3「城市盘点 006」四禁零中→M4 四检过（三重标注图内双落+来源双落+编辑价值递进链"
    u"+他司执行面细节不入卡面〔D-02/D-04=批级知悉位〕）"
    u"→M4.5 七席 ≥9（6×9.0+E7 N/A·评审单 review-20260927-mcdigest-v6.md）"
    u"+E4 参考仪同轮回填 8.0（会停下来看+打 8 分·保存/转发=倾向式如实记非无条件式"
    u"·「真实且独特信息+AI 内部决策流程即视感」双正面定性〔DIGEST 带 v1 9.0 峰/v2-v6 8.0=带持平五连〕"
    u"·旗①=批级三数行语境门槛扣 1〔verbatim 不可改写·MC-003 族数字压缩变体·吸收位=M5+系列语境〕"
    u"·最弱=5/8→6/8 对账段技术性〔同段双读数=透明自纠机制正面定性并录·M5 图文页展开+系列语境吸收·M6〕"
    u"·净本 expert-verdicts/20260927-035639-E4-audience.md·起飞 03:56:12 热载快落）"
    u"→F-047 登记（成品库第四十六件·L-卡 第三十五件·DIGEST 形态第六件）；"
    u"台账=cards/README v6 行+finished.md F-047 块+station-reviews R461 行+backlog #67 claim/交付毕双行；"
    u"④例行件：日报 09-27+W39 周审在案不重跑（W40 周审明日开周·月度统计注记 ≤09-30 挂账）"
    u"·global-benchmarks day3 ≤7 跳过（下期 ~10-01）·#63 CENSUS C-00030 锚轮首核仍不在位=supply-gated 照守"
    u"·#59 REACT 09-28 窗明日·#70 OSS 下窗 09-29 21:40 后开·#72 素材消费面知悉挂账维持"
    u"·T1 催办=已裁项停用口径·HQ-FEEDBACK 不写（无集团层新 open 问题·双锚静）"
    u"·tokens:local=1（E4 参考仪 qwen2.5:14b 一调热载快落·本地 Ollama 零 API token·P-54⑤ 计量律）"
    u"·发布锁=M5 账号物理件不变（未上线=未测量）；⑤悬置进程核验=PID 61696=ComfyUI 用户自有件良性零接触。"
    u"下轮=R462 生产轮序领（#59 REACT 09-28 热点窗届日领→#63 图鉴 C-00030 锚轮首核 supply-gated"
    u"→#70 OSS 下窗 09-29 21:40 后开）。收账显式列文件 commit+push。"
)
TASK = LOG.split(u"R461: ", 1)[1][:60]

# --- state.json (idempotent guard: only bump if still at tick 460)
sp = os.path.join(ROOT, "src", "os", "state.json")
st = json.load(io.open(sp, encoding="utf-8"))
if st.get("tick") == 460:
    st["tick"] = 461
    st["ts"] = TS
    st["task"] = TASK
    st["focus"] = (u"R461: #59 REACT 09-28 热点窗届日领（M0 择优→全链·B站源线随系列第 2+ 件按需）→#63 图鉴 C-00030 锚轮首核"
                   u"（supply-gated 照守·锚落即领）→#70 OH 下窗 09-29 21:40 后开（切片 4 换刀=ffmpeg drawtext cjk/awesome-tts "
                   u"生态/Ollama library 预检·礼貌节流单窗 ≤3 刀）→#72 素材消费面知悉挂账（BigLife 互聊台账到位前零动作）"
                   u"→#57 替代率首报 10-07 挂账；月度统计注记首件 ≤09-30（调研部章程 §二.2·随 W40 周审轮）"
                   u"·W40 周自审开周（周一 09-28 起·docs/audits/2026-W40-self-audit.md 缺任意轮补产）"
                   u"·#67 DIGEST 续件=ledger 新 CEO 令级事件落账时随轮领（research §5 在册史源全耗尽·反膨胀律照守）"
                   u"；新令/集团转办/探针红出现即优先；全静即 idle-fast（并窗 0/6）。")
    st["log"].append(LOG)
    json.dump(st, io.open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("state.json updated tick=461")
else:
    print("state.json already at tick %s - skipped" % st.get("tick"))

# --- status-export.json
ep = os.path.join(ROOT, "docs", "status-export.json")
se = json.load(io.open(ep, encoding="utf-8"))
se["export_ts"] = ISO

R461_TXT = (
    u"tick 461·R461（生产轮·#67 DIGEST 续件第五件《城市盘点 006·深夜决策批数字盘点》全链走门毕·R460 指针序首位领·"
    u"claim 当轮闭环）——①轮首五查静（无新令·ledger 五模式 29=锚·decisions 非空行 45=锚·树净零锁 HEAD=9627775）"
    u"→backlog 序判=其余量产线各窗未到（#59 09-28/#63 锚不在位/#70 下窗 09-29）→R460 指针首位 #67 DIGEST 候选成立；"
    u"②史源=集团决策批 D-20260927-01~05 五行 00:05 落档（跨仓只读）+核心故事双源 verbatim：D-01⑦「技能动员令计数修正 5/8」"
    u"vs 本仓 F-20260927-01「技能动员令计数应 6/8」（自证证据 9 件链）=编年史 A 级+数字密度；"
    u"③全链=bigstream-lcard-pipeline 技能产线第六用：M0 7/8 A 档（钩 2=5/8 vs 6/8 对照结构同源第五证·五连母题）"
    u"→M1 五源指针逐条可机核（引文双源 verbatim 对读）→M2 出图 exit 0+验图五检 5/5 一次过初稿即正字"
    u"（h2_size 40=最长行 18.30em margin +4.70em〔44 档排除=垂直栈预算律驱动选档〕·subs 19.0em<24.21em·"
    u"em-check-r461.txt+垂直栈 R381 断言 +21px）→M3 四禁零中→M4 四检过（含他司执行面细节不入卡面=批级知悉位纪律）"
    u"→M4.5 七席 ≥9（6×9.0+E7 N/A）+E4 参考仪同轮回填 8.0（会停下来看+打 8 分·保存/转发=倾向式如实记非无条件式"
    u"·「真实且独特信息+AI 内部决策流程即视感」双正面定性〔DIGEST 带 v1 9.0 峰/v2-v6 8.0=带持平五连〕"
    u"·旗①=批级三数行语境门槛扣 1〔verbatim 不可改写·吸收位=M5+系列语境〕·最弱=5/8→6/8 对账段技术性"
    u"〔同段双读数=透明自纠机制正面定性并录·M5 图文页展开+系列语境吸收·M6〕·净本 expert-verdicts/20260927-035639）"
    u"→F-047 登记（成品库第四十六件·L-卡 第三十五件·DIGEST 形态第六件）；④例行件：日报 09-27 在案·global-benchmarks ≤7 跳过"
    u"·#63 supply-gated 照守·#59 09-28 窗明日·#70 下窗 09-29 21:40 后开·tokens:local=1（E4 一调·本地 Ollama 零 API token）"
    u"·发布锁=M5 账号物理件不变（未上线=未测量）——下轮 R462 序领 #59 REACT 09-28 热点窗/#63 C-00030 锚首核 supply-gated/"
    u"#70 OSS 下窗 09-29 21:40 后开/W40 周审开周（09-28 起）"
)
prev = se["outs"][0][1]
se["outs"][0] = [u"OS 循环", R461_TXT, prev]

old = se["outs"][1][2]
new = old.replace(u"L-卡 三十四件 F-013~F-046（成品库四十五件", u"L-卡 三十五件 F-013~F-047（成品库四十六件")
assert new != old, "outs[1] count replace failed"
se["outs"][1][2] = new

for d in se["depts"]:
    if d["n"] == u"工程技术部":
        d["t"] = (u"OS 循环 R461（生产轮·#67 DIGEST 续件第五件《城市盘点 006·深夜决策批数字盘点》全链走门毕=F-047 登记"
                  u"成品库第四十六件·L-卡 第三十五件·DIGEST 形态第六件：M0 7/8 A 档〔钩 2=总部计数 5/8 vs 本仓台账 6/8"
                  u"五连母题〕+M1 五源指针可机核〔引文双源 verbatim 对读〕+M2 验图 5/5 一次过〔h2=40·VERT +21px〕"
                  u"+M4.5 七席 ≥9+E4 8.0 同轮回填〔倾向式如实记〕）·state.ts/task 心跳面刷新")
        d["s"] = (u"R461: #67 DIGEST 6th piece 'City Digest 006 midnight decision batch' full chain done "
                  u"(D-20260927-01~05 chronicle source, dual-verbatim 5/8-vs-6/8 reconciliation story, "
                  u"9-evidence chain; frame-verify 5/5 first-pass h2=40 VERT+21px; M4.5 seven seats >=9; "
                  u"E4 8.0 in-round stop+8pts; F-047 registered = 46th finished piece)")

# results updates by key
def find_key(k):
    for i, r in enumerate(se["results"]):
        if r[0] == k:
            return i
    return -1

i460 = find_key(u"460")
assert i460 >= 0, "tick row not found"
se["results"][i460] = [u"461",
    u"R461 生产轮：#67 DIGEST 续件第五件《城市盘点 006·深夜决策批数字盘点》全链走门毕（D-20260927-01~05 深夜决策批史源"
    u"·引文双源 verbatim 对读=D-01⑦「计数修正 5/8」点名 vs F-20260927-01「计数应 6/8」自证·证据 9 件链·M0 7/8 A 档"
    u"·验图 5/5 一次过·M4.5 七席 ≥9·E4 8.0 同轮回填）·F-047 登记（成品库第四十六件·L-卡 第三十五件·DIGEST 形态第六件）"]

i45 = find_key(u"45")
assert i45 >= 0, "finished-count row not found"
r3v = se["results"][i45][1]
r3v2 = r3v.replace(u"F-001~F-006+F-008~F-046（", u"F-001~F-006+F-008~F-047（")
assert r3v2 != r3v, "results F-range replace failed"
r3v2 += (u"；**F-047 DIGEST 盘点图文第六件=编年史事件随轮领第五件《城市盘点 006·深夜决策批数字盘点》"
         u"〔D-20260927-01~05 集团决策批史源·引文双源 verbatim 对读=计数 5/8→6/8 对账故事·E4 8.0 倾向式三意愿"
         u"·L-卡 第三十五件·DIGEST 形态第六件〕**")
se["results"][i45] = [u"46", r3v2]

i297 = find_key(u"297")
if i297 >= 0:
    r2v = se["results"][i297][1]
    r2v2 = r2v.replace(u"R452-R460 零代码变更未重跑", u"R452-R461 零代码变更未重跑")
    if r2v2 != r2v:
        se["results"][i297][1] = r2v2

json.dump(se, io.open(ep, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("COLLECT OK ts=%s" % TS)
