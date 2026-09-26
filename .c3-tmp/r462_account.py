# r462 accounting: surgical state.json edits + status-export.json derived refresh
# encoding-safe: this script itself is UTF-8 on disk, read/written via python io only
import io, json, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = ROOT + r"\src\os\state.json"
XP = ROOT + r"\docs\status-export.json"

now = datetime.datetime.now()
stamp = now.strftime("%Y-%m-%d %H:%M")
ts = now.strftime("%Y-%m-%d %H:%M:%S")
export_ts = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")

logline = (
    stamp + " R462: 空转快速路径轮·五静+探针定谳+探针复制操作红轮内闭环（零生产件·backlog 各窗未到全门控·异常触发实活收账）——"
    "①轮首五查静：无新令（orders 双 NONE=r462_check）/ledger 五模式正典 29=锚零新转办/decisions UTF8 非空行 45=锚零新行/树净零锁 HEAD=d481db0 R461 收账/无 bm-a 迹象（storylines 09-27 零写盘 0/0/0）·例行件=日报 09-27+W39 周审在案不重跑·global-benchmarks day3 ≤7 跳过（下期 ~10-01）·C-00030/C-00031 锚仍不在位 supply-gated 照守（anchors 止 C-00029）→backlog 顶行序判无可领件：#59 REACT 09-28 窗未到/#63 锚门/#70 OH 下窗 09-29 21:40 后开/#72 待 BigLife 互聊台账/#57 替代率 10-07/月度统计注记 ≤09-30 随 W40 周审轮/W40 周自审开周 09-28 起/自进清单 open 项全门控（B5 账号期站内采样·B3 周更 W40·C4 首进链件触发位）/#67 史源耗尽待 ledger 新 CEO 令级事件（反膨胀律照守）→三探针照跑；"
    "②探针读数=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现（46 renders 全注账）/loop_health 2 FAIL+21 WARN 全定谳在案类零新增：FAIL① 49min 停跳=R425 调度器漏触发同事件足迹 R426 已裁定不重复触发·FAIL② account-lag（done beats 462>tick 461）=03:26:43 中断执行体 done-beat 恒久 +1 足迹（R459 首见记「收账即平」——本轮心跳尾 14 行实证该平仅瞬时态：收账后 D-T 复位 0·执行体退出即复 +1·R459 起每轮恒态非新断洞·证据件 r462_beats_tail.txt·**新断洞判据=lag ≥2**）·21 WARN=13 log-order 叙事时间戳+8 heartbeat-gap 长轮间隙合法违例（清单 r462_lh_warns.txt·全部 ≤09-27 03:15 史实）；"
    "③操作红一件轮内闭环（如实入账）：本轮探针复制走 PS Get-Content 无 -Encoding 往返→UTF-8 正则中文五模式 GBK 损坏（七线全司→涓冪嚎鍏ㄥ徃 等）→ledger 假读数 20=仅 @BigStream ASCII 子集——正法双通道复算 29=锚（r462_canon 直扫+方法 A/B 对照 r462_debug 双 29·零分隔符伪差）+损坏复现件 r462X_repro 稳定复演 20=根因坐实（PS5.1 编码律已知坑族第三证=R461「首扫 0 口径偏离」+R459「PS 计数 29 控制台误读」同族）；随行第二红=shutil.copy 字节拷贝保留原 OUTP→r461_check.txt 历史证据件被覆写→git checkout HEAD 恢复（d481db0）+r462_check.py 改 OUTP 重跑出正确证据件（ledger 29）——**防再犯律一条：探针跨轮复制一律 python utf-8 读改写或 write_file·禁 PS Get-Content/Set-Content 往返·字节拷贝须 OUTP 改指（编码律+证据件防覆写双面）**；"
    "④收账=idle-fast 并窗律不适用（异常触发实活收账·并窗重置 0/6）·ts+task 刷新·status-export 刷（export_ts+工程技术部 t/s+OS 循环 outs+results 派生·F3 律）·tokens:local=0（本轮零本地模型调用·P-54⑤ 计量律）·发布锁=M5 账号物理件不变（未上线=未测量）·HQ-FEEDBACK 不写（无集团层新 open 问题·双锚静）。下轮=R463 快速路径首查→#59 REACT 09-28 热点窗届日领→W40 周自审+月度统计注记（09-28 起）→#63/#70/#72 各窗随轮。收账显式列文件 commit+push。"
)

focus_new = (
    "R463: #59 REACT 09-28 热点窗届日领（M0 择优→全链·B站源线随系列第 2+ 件按需）→W40 周自审开周（周一 09-28 起·docs/audits/2026-W40-self-audit.md 缺任意轮补产）+月度统计注记首件 ≤09-30（调研部章程 §二.2·随 W40 周审轮）→#63 图鉴 C-00030 锚轮首核（supply-gated 照守·锚落即领）→#70 OH 下窗 09-29 21:40 后开→#72 素材消费面知悉挂账（BigLife 互聊台账到位前零动作）→#57 替代率首报 10-07 挂账；#67 DIGEST 续件=ledger 新 CEO 令级事件落账时随轮领（史源耗尽·反膨胀律照守）；自进清单 open 项全门控（B5 账号期/B3 周更 W40/C4 首进链件触发位）；探针执法注记=loop_health account-lag +1 恒态=03-26 中断执行体 done-beat 足迹（R459 在案·新断洞判据 lag ≥2）+探针跨轮复制律（python utf-8 改写/write_file·禁 PS Get-Content 往返·字节拷贝须 OUTP 改指）；新令/集团转办/探针红出现即优先；全静即 idle-fast（并窗 0/6·R462 异常触发已收账重置）。"
)

task_new = logline.split("R462: ", 1)[1][:60]

# ---------- state.json surgical edits ----------
raw = io.open(SP, encoding="utf-8").read()

def sub1(text, old, new, label):
    n = text.count(old)
    assert n == 1, "anchor not unique (%d): %s" % (n, label)
    return text.replace(old, new, 1)

raw = sub1(raw, '"tick": 461,', '"tick": 462,', "tick")

old_focus_prefix = '"focus": "R461: #59 REACT 09-28 热点窗届日领（M0 择优→全链·B站源线随系列第 2+ 件按需）'
i = raw.index(old_focus_prefix)
j = raw.index('",', i)
old_focus_full = raw[i:j + 2]
assert "全静即 idle-fast（并窗 0/6）。" in old_focus_full
new_focus_full = '"focus": "' + focus_new + '",'
raw = raw[:i] + new_focus_full + raw[j + 2:]

tail_anchor = '\n ],\n "ts": "2026-09-27 03:59:22",'
new_tail = ',\n  "' + logline + '"\n ],\n "ts": "' + ts + '",'
raw = sub1(raw, tail_anchor, new_tail, "log-append-tail")

old_task = '"task": "生产轮·#67 DIGEST 续件第五件《城市盘点 006·深夜决策批数字盘点》全链走门毕（R460 指针序首位领·cl"'
new_task = '"task": "' + task_new + '"'
raw = sub1(raw, old_task, new_task, "task")

json.loads(raw)  # validity gate before write
io.open(SP, "w", encoding="utf-8", newline="\n").write(raw)
print("state.json updated: tick=462 ts=%s" % ts)

# ---------- status-export.json derived refresh (P-61, F3 derive-on-write) ----------
se = json.load(io.open(XP, encoding="utf-8"))
se["export_ts"] = export_ts

eng_t = (
    "OS 循环 R462（空转快速路径轮·五静+探针定谳·零生产件：backlog 各窗未到全门控）——loop_health 2 FAIL 定谳在案类"
    "（49min 停跳=R425 裁定项+account-lag +1=03-26 中断执行体 done-beat 恒久足迹〔R459 在案·新断洞判据 lag ≥2〕+21 WARN 全史实零新增）"
    "+探针复制操作红轮内闭环（PS Get-Content 往返 GBK 损坏正则→ledger 假读数 20→正法复算 29=锚+复现坐实+shutil OUTP 覆写 r461_check.txt→git HEAD 恢复）"
    "+防再犯律（探针跨轮复制一律 python utf-8 改写/write_file·禁 PS 往返·字节拷贝须 OUTP 改指）·state.ts/task 心跳面刷新"
)
eng_s = (
    "R462 fast-path round: five-checks quiet (ledger 29=anchor, decisions 45=anchor), no claimable backlog (all windows/gates not reached); "
    "loop_health 2 FAIL adjudicated in-case (49min outage R425 + account-lag +1 = 03:26 interrupted-entity done-beat permanent footprint, new-break threshold lag>=2); "
    "probe-copy op-red closed in-round (PS Get-Content roundtrip GBK-corrupted Chinese regex -> false ledger 20, canonical rescan 29=anchor + repro seated; "
    "shutil byte-copy OUTP clobbered r461_check.txt -> restored from git HEAD d481db0); law: cross-round probe copies via python utf-8 or write_file only"
)
for d in se["depts"]:
    if d.get("n") == "工程技术部":
        d["t"] = eng_t
        d["s"] = eng_s
        break
else:
    raise SystemExit("dept not found")

r462_out = (
    "tick 462·R462（空转快速路径轮·五静+探针定谳+探针复制操作红轮内闭环·零生产件）——①五查静（无新令·ledger 29=锚·decisions 45=锚·树净零锁 HEAD=d481db0）"
    "→backlog 序判无可领件（#59 09-28 窗/#63 锚门/#70 下窗 09-29/#72 待台账/W40 周自审+月度注记 09-28 起/自进清单 open 全门控）；"
    "②三探针=board 0 FAIL/readiness 3 阻塞皆外部+0 发现/loop_health 2 FAIL+21 WARN 全定谳在案类（49min 停跳 R425 裁定项"
    "+account-lag +1=03-26 中断执行体 done-beat 恒久足迹·R459 在案·新断洞判据 lag ≥2·21 WARN 全 ≤09-27 03:15 史实零新增）；"
    "③操作红轮内闭环=PS Get-Content 往返损坏探针正则（GBK）→ledger 假读数 20→正法双通道复算 29=锚+复现件坐实（PS5.1 编码律坑族第三证）"
    "+shutil OUTP 覆写 r461_check.txt→git HEAD 恢复+防再犯律（python utf-8 改写/write_file·禁 PS 往返·字节拷贝须 OUTP 改指）；"
    "④异常触发实活收账（并窗重置 0/6）·tokens:local=0·发布锁不变——下轮 R463 序领 #59 REACT 09-28 热点窗/W40 周自审+月度统计注记/#63/#70 各窗"
)
osrow = se["outs"][0]
se["outs"][0] = [osrow[0], r462_out, osrow[1]]

se["results"][0] = [
    "462",
    "R462 空转快速路径轮：五静（ledger 29=锚/decisions 45=锚/树净零锁）+三探针定谳（board 0 FAIL·readiness 3 皆外部 0 发现"
    "·loop_health 2 FAIL+21 WARN 全在案类零新增）+探针复制操作红轮内闭环（PS 往返 GBK 损坏正则→ledger 假读数 20→正法复算 29=锚"
    "+复现坐实+r461_check.txt git 恢复）·零生产件（backlog 各窗未到全门控）·异常触发实活收账",
]

se_txt = json.dumps(se, ensure_ascii=False, indent=1)
orig = io.open(XP, encoding="utf-8").read()
nl = "\n" if orig.endswith("\n") else ""
io.open(XP, "w", encoding="utf-8", newline="\n").write(se_txt + nl)
json.loads(io.open(XP, encoding="utf-8").read())
print("status-export.json refreshed: export_ts=%s" % export_ts)
print("task=%s" % task_new)
