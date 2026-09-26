# -*- coding: utf-8 -*-
# R460 collect v2 (idempotent state guard + key-based results lookup)
import io, json, os, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
now = datetime.datetime.now()
TS = now.strftime("%Y-%m-%d %H:%M:%S")
ISO = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
HM = now.strftime("%H:%M")

LOG = (
    u"2026-09-27 " + HM + u" R460: 生产轮·#67 DIGEST 续件第四件《城市盘点 005·节目重制日数字盘点》全链走门毕"
    u"（R459 指针序首位领·claim 当轮闭环·P-20260926-11 史源）——"
    u"①轮首快速路径五查静（无新令 orders 顶=O-20260925-1931 已记账·ledger 五模式正典同法 29=锚零新转办〔r460_canon 复跑〕"
    u"·decisions 非空行 45=锚零新行·树净零锁 HEAD=9fabc28 R459 开轮实取）→非空转轮转全任务书认领 #67；"
    u"②史源核验=集团转办 P-20260926-11 节目质量整改令（CEO 原话 verbatim「可视化表现要注意页面统一和措辞简单易懂，"
    u"现在媒体公司的节目做的很不好，统一优化」evolution-ledger 正行+backlog #71 双源一致已核·P-51 送达链 git log grep "
    u"10 commits 含令号在案）=编年史 A 级未用事件+数字密度全在己仓可机核（1 句直评/4 维自审/2 律/4 件重制/S1 三连满分/"
    u"E4 8.0×4/297 测试）；③全链=bigstream-lcard-pipeline 技能产线第五用：M0 四维分 7/8 A 档（钩 2=1 句直评 vs 两日 "
    u"4 件全链重制收官=F-042 v2 对照结构同源第四证·四连母题）→M1 纪实数字汇编律复用六源指针逐条可机核→M2 出图 exit 0"
    u"+验图五检 5/5 一次过初稿即正字（转写先行十行全中+靶向空间复验六项全过·em 前置适配 h2_size 40=引文行 21.00em "
    u"margin +2.00em·44 档排除·subs 21.0em<24.21em·em-check-r460.txt+垂直栈 R381 断言 +21px=v4 同构七行 deck 初渲即过"
    u"零修参）→M3「城市盘点 005」四禁零中→M4 四检过（三重标注图内双落+来源双落+编辑价值递进链）→M4.5 七席 ≥9"
    u"（6×9.0+E7 N/A·评审单 review-20260927-mcdigest-v5.md）+E4 参考仪同轮回填 8.0（会停下来看+会保存并转发=三意愿"
    u"正面明说无条件式·DIGEST 带 v1 9.0 峰/v2-v5 8.0 带持平·旗①=CEO 直评句语境门槛扣 1〔verbatim 不可改写·F-042 v2 "
    u"同族·吸收位=M5〕·最弱=时间线紧凑被疑真实〔E4 事实面注记：令 09-26 晚→收官 09-27 凌晨≈30 小时=AI 公司机器速度"
    u"实况·10 commit 可证·吸收位=M5 图文页语境+系列语境·M6〕·净本 expert-verdicts/20260927-034634）→F-046 登记"
    u"（成品库第四十五件·L-卡 第三十四件·DIGEST 第五件）；台账=cards/README v5 行+finished.md F-046 块+station-reviews "
    u"R460 行+backlog #67 claim/交付毕双行；④例行件：日报 09-27+W39 周审在案不重跑（W40 周审明日开周·月度统计注记 "
    u"≤09-30 挂账）·global-benchmarks day3 ≤7 跳过（下期 ~10-01）·#63 CENSUS C-00030 锚轮首核仍不在位=supply-gated "
    u"照守·#59 REACT 09-27 窗已毕=09-28 窗明日·#70 OSS 下窗 09-29 21:40 后开·#72 素材消费面知悉挂账维持·T1 催办="
    u"已裁项停用口径·HQ-FEEDBACK 不写（无集团层新 open 问题·ledger/decisions 双锚静）·tokens:local=1（E4 参考仪 "
    u"qwen2.5:14b 一调热载快落 517 字·本地 Ollama 零 API token·P-54⑤ 计量律）。下轮=R461 生产轮序领（#59 REACT 09-28 "
    u"热点窗届日领→#67 DIGEST 编年史候选〔集团决策批 D-20260927-01~05 等 research §5 在册〕→#63 图鉴 C-00030 锚轮首核 "
    u"supply-gated）。收账显式列文件 commit+push。"
)
TASK = LOG.split("R460: ", 1)[1][:60]

# --- state.json (idempotent guard: skip if already tick 460)
sp = os.path.join(ROOT, "src", "os", "state.json")
st = json.load(io.open(sp, encoding="utf-8"))
if st.get("tick") == 459:
    st["tick"] = 460
    st["ts"] = TS
    st["task"] = TASK
    st["log"].append(LOG)
    json.dump(st, io.open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("state.json updated tick=460")
else:
    print("state.json already at tick %s - skipped" % st.get("tick"))

# --- status-export.json
ep = os.path.join(ROOT, "docs", "status-export.json")
se = json.load(io.open(ep, encoding="utf-8"))
se["export_ts"] = ISO

R460_TXT = (
    u"tick 460·R460（生产轮·#67 DIGEST 续件第四件《城市盘点 005·节目重制日数字盘点》全链走门毕·R459 指针序首位领·"
    u"claim 当轮闭环）——①轮首五查静（无新令·ledger 五模式 29=锚·decisions 非空行 45=锚·树净零锁 HEAD=9fabc28）→"
    u"非空转轮认领 #67；②史源=P-20260926-11 节目质量整改令（CEO 原话 verbatim evolution-ledger 正行+backlog #71 双源"
    u"一致已核·P-51 送达链 10 commits 含令号）=编年史 A 级未用事件+数字密度全在己仓可机核；③全链=bigstream-lcard-"
    u"pipeline 技能产线第五用：M0 7/8 A 档（钩 2=1 句直评 vs 两日 4 件全链重制收官=F-042 v2 同源第四证·四连母题）→"
    u"M1 纪实数字汇编律六源指针逐条可机核→M2 出图 exit 0+验图五检 5/5 一次过初稿即正字（转写先行十行全中+靶向空间"
    u"复验六项全过·h2_size 40=引文行 21.00em margin +2.00em·44 档排除·subs 21.0em<24.21em·em-check-r460.txt+垂直栈 "
    u"R381 断言 +21px）→M3「城市盘点 005」四禁零中→M4 四检过→M4.5 七席 ≥9（6×9.0+E7 N/A）+E4 参考仪同轮回填 8.0"
    u"（三意愿正面明说无条件式·DIGEST 带 v1 9.0 峰/v2-v5 8.0 带持平·旗①=CEO 直评句语境门槛扣 1〔verbatim 不可改写·"
    u"F-042 v2 同族·吸收位=M5〕·最弱=时间线紧凑被疑真实〔事实面=AI 机器速度实况≈30h·10 commit 可证·M5+系列语境吸收〕"
    u"·净本 expert-verdicts/20260927-034634）→F-046 登记（成品库第四十五件·L-卡 第三十四件·DIGEST 第五件）；台账="
    u"cards/README v5 行+finished.md F-046 块+station-reviews R460 行+backlog #67 双行；④例行件：日报 09-27+W39 周审"
    u"在案不重跑·global-benchmarks ≤7 跳过·#63 C-00030 锚不在位 supply-gated 照守·#59 REACT 09-28 窗明日·#70 OSS 下窗 "
    u"09-29 21:40 后开·tokens:local=1（E4 一调热载快落·本地 Ollama 零 API token）·发布锁=M5 账号物理件不变（未上线="
    u"未测量）——下轮 R461 序领 #59 REACT 09-28 窗/#67 DIGEST 编年史候选/#63 C-00030 锚首核"
)
prev = se["outs"][0][1]
se["outs"][0] = [u"OS 循环", R460_TXT, prev]

old = se["outs"][1][2]
new = old.replace(u"L-卡 三十三件 F-013~F-045（成品库四十四件", u"L-卡 三十四件 F-013~F-046（成品库四十五件")
assert new != old, "outs[1] count replace failed"
se["outs"][1][2] = new

for d in se["depts"]:
    if d["n"] == u"工程技术部":
        d["t"] = (u"OS 循环 R460（生产轮·#67 DIGEST 续件第四件《城市盘点 005·节目重制日数字盘点》全链走门毕=F-046 登记"
                  u"成品库第四十五件·L-卡 第三十四件·DIGEST 第五件：M0 7/8 A 档+M1 六源指针可机核+M2 验图 5/5 一次过"
                  u"〔h2_size 40·VERT +21px〕+M4.5 七席 ≥9+E4 8.0 同轮回填〔三意愿正面明说无条件式〕）·state.ts/task 心跳面刷新")
        d["s"] = (u"R460: #67 DIGEST 5th piece 'City Digest 005 program-remake day' full chain done "
                  u"(P-20260926-11 chronicle source, CEO verdict verbatim dual-source verified; frame-verify 5/5 "
                  u"first-pass h2=40 VERT+21px; M4.5 seven seats >=9; E4 8.0 in-round stop+save+share; "
                  u"F-046 registered = 45th finished piece)")

# results updates by key
def find_key(k):
    for i, r in enumerate(se["results"]):
        if r[0] == k:
            return i
    return -1

i459 = find_key(u"459")
assert i459 >= 0, "tick row not found"
se["results"][i459] = [u"460",
    u"R460 生产轮：#67 DIGEST 续件第四件《城市盘点 005·节目重制日数字盘点》全链走门毕（P-20260926-11 史源·CEO 原话 "
    u"verbatim 双源核·M0 7/8 A 档·验图 5/5 一次过·M4.5 七席 ≥9·E4 8.0 三意愿正面明说无条件式）·F-046 登记"
    u"（成品库第四十五件·L-卡 第三十四件·DIGEST 第五件）"]

i44 = find_key(u"44")
assert i44 >= 0, "finished-count row not found"
r3v = se["results"][i44][1]
r3v2 = r3v.replace(u"F-001~F-006+F-008~F-045（", u"F-001~F-006+F-008~F-046（")
assert r3v2 != r3v, "results F-range replace failed"
r3v2 += (u"；**F-046 DIGEST 盘点图文第五件=编年史事件随轮领第四件《城市盘点 005·节目重制日数字盘点》"
         u"〔P-20260926-11 节目质量整改令史源·CEO 原话 verbatim·E4 8.0 三意愿正面明说无条件式·L-卡 第三十四件·DIGEST 形态第五件〕**")
se["results"][i44] = [u"45", r3v2]

i297 = find_key(u"297")
if i297 >= 0:
    r2v = se["results"][i297][1]
    r2v2 = r2v.replace(u"R452-R457 零代码变更未重跑", u"R452-R460 零代码变更未重跑")
    if r2v2 != r2v:
        se["results"][i297][1] = r2v2

json.dump(se, io.open(ep, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("COLLECT OK ts=%s" % TS)
