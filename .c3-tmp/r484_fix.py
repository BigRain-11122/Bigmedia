# r484_fix.py - R484 idle-fast closeout: state.json surgery + status-export P-61 refresh
# (utf-8 string surgery, no reformat; json.load verify gate before+after write; evidence to r484_fix.txt)
import io, os, re, json, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = os.path.join(ROOT, "src", "os", "state.json")
XP = os.path.join(ROOT, "docs", "status-export.json")
OUTP = os.path.join(ROOT, ".c3-tmp", "r484_fix.txt")

now = datetime.datetime.now()
TS = now.strftime("%Y-%m-%d %H:%M:%S")
STAMP = now.strftime("%Y-%m-%d %H:%M")
ISO = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")

LOG = (STAMP + " R484: idle-fast（快速路径·五静+探针定谳绿·不进开轮四步·并窗轮 4/6 不 commit）——"
 "①无新令（orders 双 NONE=r484_check·锚=O-20260925-1931-HQ-C mtime 19:47:21·O- 34 件零新增零编辑·orders_edited_since_anchor NONE=D-20260927-05② 检测线绿）"
 "+无新集团转办（ledger 五模式正典行数口径 29=锚零新行·r484_check 行数口径直计·内容寻址勿全文重读）"
 "+无新决策行（decisions UTF8 非空行 45=锚·D-20260927-01~05 批后零新）·production=open 自愈核=在位零翻正（r484_check）；"
 "②backlog 顶行不可认领（#74/#71/#73/#21/#64 done·#72 素材消费面知悉挂账〔BigLife 互聊台账 ≤09-28 12:00 到位前零动作〕"
 "·#59 REACT 09-27 窗已毕〔R456 F-045〕09-28 窗届日即领〔daily_brief 09-28 缺则先补产〕"
 "·#63 图鉴 C-00030/C-00031 锚正典位轮首核均不在位〔r484_check anchor False 双证·BigLife census/anchors 20 件尾三止 C-00029〕supply-gated 维持"
 "·#70 OH 下窗 09-29 21:40 后开〔首窗三切片 R432/R458/R459 齐=窗面满〕·#57 替代率首报 10-07 挂账"
 "·W40 周自审 09-28 开周+月度统计注记首件 ≤09-30 随 W40 周审轮·#67 DIGEST 史源耗尽待 ledger 新 CEO 令级事件〔反膨胀律照守〕"
 "·自进池 open 项全门控〔B5 账号期站内采样/B3 周更 W40/C4 首进链件触发位〕）；"
 "③树态=仅自产预期件（无 index.lock False 实证·树态=M state.json+M status-export.json=R481~R483 idle-fast 自记账并窗预期态非 bm-a 迹象"
 "+untracked .c3-tmp r481~r484 探针证据件随并窗批 commit〔R150 先例〕·HEAD=897fd23 R480 batch 未变 git log 零插队=无 bm-a 活跃写盘迹象"
 "·storylines 三子域 R483 收账后零新写盘 0/0/0=r484_check）；"
 "④例行件：日报 09-27 在案不重跑（R443 补产件·09-28 件=明届日随窗补产）·W39 周审在案（W40 明日 09-28 开周）"
 "·global-benchmarks day3 ≤7 跳过（下期 ~10-01 并窗 M4/S4 门参数复核=R457 调研部首件选题窗）·T1 催办=已裁项停用口径"
 "·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀·ledger/decisions 双锚静）·tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）"
 "·发布锁=M5 账号物理件不变（未上线=未测量）；"
 "三探针定谳=board 0 FAIL（5 题 10 稿·5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现=阻塞≠失败口径 exit 1〔46 renders 全注账〕"
 "/loop_health 2 FAIL+21 WARN 全定谳在案类零新增（FAIL① heartbeat-outage 49min=R425 调度器漏触发同事件足迹 R426 已裁定不重复触发"
 "·FAIL② account-lag done484>tick483=+1 恒态足迹〔03-26 中断执行体 done-beat·R459/R462 在案·新断洞判据 lag ≥2 未破线零新断洞〕"
 "·21 WARN=13 log-order+8 heartbeat-gap 全 ≤09-27 03:15 史实零新增·backlog 75 项 61 done 81% 燃尽=R483 同读数）"
 "——探针复制律第二十一证（r484_check.py/r484_probes.py=write_file 新建+OUTP 改指·零 PS 往返零历史件覆写=R462 防再犯律+R466 write_file 预核 tracked 态律双守·本轮零操作红）；"
 "一行收账即出（idle-fast 并窗轮 4/6〔窗 R481-R486 满 6 收账→R486 batch commit·跨日边界 09-28 00:00 先到即收〕·本轮不 commit·P-61 导出步照刷 export_ts 轻量+机读 tick 面 484 对齐〔F3 律〕）。"
 "下轮快速路径首查：#59 REACT 09-28 热点窗届日领（daily_brief 09-28 缺则先补产）/W40 周自审开周（09-28 起·docs/audits/2026-W40-self-audit.md 缺任意轮补产）+月度统计注记/图鉴 C-00030 锚/新令/集团转办——全静即 idle-fast（5/6）。")

FOCUS = ("R485: #59 REACT 09-28 热点窗届日领（M0 择优→全链·daily_brief 09-28 缺则先补产·B站源线随系列第 2+ 件按需）"
 "→W40 周自审开周（周一 09-28 起·docs/audits/2026-W40-self-audit.md 缺任意轮补产）+月度统计注记首件 ≤09-30（调研部章程 §二.2·随 W40 周审轮）"
 "→#63 图鉴 C-00030 锚轮首核（supply-gated 照守·锚落即领）→#70 OH 下窗 09-29 21:40 后开→#72 素材消费面知悉挂账（BigLife 互聊台账到位前零动作）→#57 替代率首报 10-07 挂账；"
 "#67 DIGEST 续件=ledger 新 CEO 令级事件落账时随轮领（史源耗尽·反膨胀律照守）；自进清单 open 项全门控（B5 账号期/B3 周更 W40/C4 首进链件触发位）；"
 "探针执法注记=loop_health account-lag +1 恒态=03-26 中断执行体 done-beat 足迹（R459 在案·新断洞判据 lag ≥2）"
 "+探针跨轮复制律（python utf-8 改写/write_file·禁 PS Get-Content 往返·字节拷贝须 OUTP 改指）+write_file 预核 tracked 态律（R466）；"
 "新令/集团转办/探针红出现即优先；全静即 idle-fast（并窗轮 5/6·窗 R481-R486 满 6 收账→R486 batch commit·跨日边界 09-28 00:00 先到即收）")

R484_OUTS = ("tick 484·R484（idle-fast 空转快速路径轮·五静+探针定谳绿·零生产件·并窗轮 4/6 不 commit）——"
 "①无新令（orders 顶=O-20260925-1931-HQ-C 零新增零编辑·O- 34 件·orders_edited_since_anchor NONE）"
 "+无新集团转办（ledger 五模式正典行数口径 29=锚·r484_check 行数口径直计）+无新决策行（decisions UTF8 非空行 45=锚）+production=open 在位零翻正；"
 "②backlog 顶行不可认领（#74/#71/#73 done·#72 待 BigLife 台账 ≤09-28 12:00·#59 REACT 09-28 窗届日领〔daily_brief 09-28 缺则先补产〕"
 "·#63 C-00030/31 锚正典位不在位 supply-gated 照守〔anchors 20 件尾三止 C-00029〕·#70 OH 下窗 09-29 21:40·#57 替代率 10-07"
 "·W40 周自审 09-28 开周+月度统计注记 ≤09-30·#67 史源耗尽反膨胀律照守·自进池 open 全门控）；"
 "③树态=仅并窗自产预期态（HEAD=897fd23 R480 batch 零插队·storylines R483 后零写盘=无 bm-a 迹象·无 index.lock）；"
 "④三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面 0 发现/loop_health 2 FAIL+21 WARN 全定谳在案类零新增"
 "（49min 停跳=R425 足迹 R426 已裁定·account-lag done484>tick483=+1 在飞恒态足迹·新断洞判据 lag ≥2 未破线）；"
 "例行件照旧（日报 09-27 在案·global-benchmarks day3 ≤7 跳过）·tokens:local=0·发布锁=M5 账号物理件不变（未上线=未测量）")

R484_RESULT = ("R484 idle-fast 空转快速路径轮：五静（ledger 29=锚·正典行数口径直计/decisions 45=锚/orders 零新增零编辑）"
 "+三探针定谳（board 0 FAIL·readiness 3 皆外部 0 发现·loop_health 2 FAIL+21 WARN 皆在案类零新增）"
 "·零生产件（backlog 各窗未到全门控·#59 09-28 届日/W40 周自审+月度注记 09-28 起）"
 "·并窗轮 4/6 不 commit（窗 R481-R486 满 6 收账·跨日边界 09-28 00:00 先到即收）")

TASK = re.sub(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2} R\d+: ', '', LOG)[:60]

E = []
def w(t):
    E.append(str(t))

# ---------- state.json string surgery ----------
s = io.open(SP, encoding="utf-8").read()
NL = "\r\n" if "\r\n" in s else "\n"

assert s.count('"tick": 483,') == 1, "tick anchor not unique"
s = s.replace('"tick": 483,', '"tick": 484,')

m = re.search(r'"focus": "R483:[^"]*",', s)
assert m, "focus R483 anchor not found"
s = s[:m.start()] + '"focus": "' + FOCUS + '",' + s[m.end():]

seam = NL + " ],"
i = s.rindex(seam)
s = s[:i] + "," + NL + " " + json.dumps(LOG, ensure_ascii=False) + s[i:]

s = re.sub(r'"ts": "[^"]*"', lambda _: '"ts": ' + json.dumps(TS, ensure_ascii=False), s, count=1)
s = re.sub(r'"task": "[^"]*"', lambda _: '"task": ' + json.dumps(TASK, ensure_ascii=False), s, count=1)

json.loads(s)  # verify gate (R477)
io.open(SP, "w", encoding="utf-8", newline="").write(s)
json.loads(io.open(SP, encoding="utf-8").read())  # post-write verify
w("state.json OK tick=484 log_append=R484 ts=" + TS)
w("task=" + TASK)

# ---------- status-export.json P-61 refresh ----------
t = io.open(XP, encoding="utf-8").read()
x = json.loads(t)
assert x["outs"][0][0] == "OS 循环" and len(x["outs"][0]) == 3, "outs[0] shape unexpected"
assert x["results"][0][0] == "483", "results[0] anchor unexpected"

dump_check = json.dumps(x, indent=1, ensure_ascii=False)
trail = "\n" if t.endswith("\n") else ""
if dump_check + trail == t:
    r483_entry = x["outs"][0][1]
    x["outs"][0][1] = R484_OUTS
    x["outs"][0][2] = r483_entry
    x["results"][0] = ["484", R484_RESULT]
    x["export_ts"] = ISO
    out = json.dumps(x, indent=1, ensure_ascii=False) + trail
    json.loads(out)
    io.open(XP, "w", encoding="utf-8", newline="").write(out)
    w("status-export OK path=json fidelity=yes export_ts=" + ISO)
else:
    NLX = "\r\n" if "\r\n" in t else "\n"
    r483_entry = x["outs"][0][1]
    r482_entry = x["outs"][0][2]
    assert t.count(r483_entry) == 1 and t.count(r482_entry) == 1, "outs entries not unique"
    t = t.replace(r483_entry, R484_OUTS)
    t = t.replace(r482_entry, r483_entry)
    r0 = x["results"][0][1]
    assert t.count(r0) == 1, "results[0][1] not unique"
    t = t.replace(r0, R484_RESULT)
    assert t.count('"483",') == 1, "results tick string not unique"
    t = t.replace('"483",', '"484",')
    t = re.sub(r'"export_ts": "[^"]*"', lambda _: '"export_ts": ' + json.dumps(ISO, ensure_ascii=False), t, count=1)
    json.loads(t)
    io.open(XP, "w", encoding="utf-8", newline="").write(t)
    w("status-export OK path=string fidelity=no export_ts=" + ISO)

io.open(OUTP, "w", encoding="utf-8").write("\n".join(E) + "\n")
print("R484_FIX_OK")
