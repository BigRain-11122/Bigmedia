# r481_account.py - R481 idle-fast accounting: state.json log/tick/ts/task/focus + status-export P-61 refresh
# v2 fix: last-array-element has NO trailing comma (R477 law) -> anchor includes prev element's
# closing quote and appends the inter-element comma; task regex eof-anchored.
# utf-8 no-PS-roundtrip; validate-before-write; eol-preserving; OUTP new evidence file
import io, json, datetime, re, sys

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = ROOT + r"\src\os\state.json"
SE = ROOT + r"\docs\status-export.json"
OUTP = ROOT + r"\.c3-tmp\r481_account.txt"

now = datetime.datetime.now()
ts = now.strftime("%Y-%m-%d %H:%M:%S")
iso = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")

BODY = ("idle-fast（快速路径·五静+探针定谳绿·不进开轮四步·并窗轮 1/6 不 commit）——"
"①无新令（orders 双 NONE=r481_check·锚=O-20260925-1931-HQ-C mtime 19:47:21·O- 34 件零新增零编辑·orders_edited_since_anchor NONE=D-20260927-05② 检测线绿）"
"+无新集团转办（ledger 五模式正典行数口径 29=锚零新行〔r481_canon.py=r462_canon 同法复算定谳·r481_check 首扫 occurrences 读数 41=行数 vs 出现次数计量口径偏差·多命中行膨胀坐实·R461 首扫 0/R475 四模式 28 同族·轮内即弃即正=假绿灯律自检闭环〕·内容寻址勿全文重读）"
"+无新决策行（decisions UTF8 非空行 45=锚·D-20260927-01~05 批后零新）·production=open 自愈核=在位零翻正（r481_check）；"
"②backlog 顶行不可认领（#74/#71/#73 done·#72 素材消费面知悉挂账〔BigLife 互聊台账 ≤09-28 12:00 到位前零动作〕·#59 REACT 09-27 窗已毕〔R456 F-045〕09-28 窗届日即领〔daily_brief 09-28 缺则先补产〕·#63 图鉴 C-00030/C-00031 锚正典位轮首核均不在位〔r481_check anchor False 双证·BigLife census/anchors 尾三止 C-00029〕supply-gated 维持·#70 OH 下窗 09-29 21:40 后开〔首窗三切片 R432/R458/R459 齐=窗面满〕·#57 替代率首报 10-07 挂账·W40 周自审 09-28 开周+月度统计注记首件 ≤09-30 随 W40 周审轮·#67 DIGEST 史源耗尽待 ledger 新 CEO 令级事件〔反膨胀律照守〕·自进池 open 项全门控〔B5 账号期站内采样/B3 周更 W40/C4 首进链件触发位〕）；"
"③树态=仅自产预期件（无 index.lock False 实证·开轮 git status 空输出=HEAD=897fd23 R480 batch 后净态·git log 零插队=无 bm-a 活跃写盘迹象·storylines 三子域 R480 收账后零新写盘 0/0/0=r481_check）；"
"④例行件：日报 09-27 在案不重跑（R443 补产件·09-28 件=明届日随窗补产）·W39 周审在案（W40 明日 09-28 开周）·global-benchmarks day3 ≤7 跳过（下期 ~10-01 并窗 M4/S4 门参数复核=R457 调研部首件选题窗）·T1 催办=已裁项停用口径·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀·ledger/decisions 双锚静）·tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（未上线=未测量）；"
"三探针定谳=board 0 FAIL（5 题 10 稿·5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现=阻塞≠失败口径 exit 1〔46 renders 全注账〕/loop_health 2 FAIL+21 WARN 全定谳在案类零新增（FAIL① heartbeat-outage 49min=R425 调度器漏触发同事件足迹 R426 已裁定不重复触发·FAIL② account-lag done481>tick480=+1 恒态足迹〔03-26 中断执行体 done-beat·R459/R462 在案·新断洞判据 lag ≥2·本轮 lag=+1 未破线零新断洞〕·21 WARN=13 log-order+8 heartbeat-gap 全 ≤09-27 03:15 史实零新增·backlog 75 项 61 done 81% 燃尽=R480 同读数）"
"——探针复制律第十八证（r481_check.py/r481_canon.py/r481_probes.py=write_file 新建+OUTP 改指·零 PS 往返零历史件覆写=R462 防再犯律+R466 write_file 预核 tracked 态律双守·本轮零操作红）；"
"一行收账即出（idle-fast 并窗轮 1/6〔窗 R481-R486 满 6 收账·跨日边界 09-28 00:00 先到即收〕·本轮不 commit·P-61 导出步照刷 export_ts+机读 tick 面对齐〔outs/results 480→481〕）。"
"下轮快速路径首查：#59 REACT 09-28 热点窗届日领（daily_brief 09-28 缺则先补产）/W40 周自审开周（09-28 起）+月度统计注记/C-00030 锚/新令/集团转办——全静即 idle-fast（2/6）。")

logline = ts + " R481: " + BODY
task = BODY[:60]

def must(cond, msg):
    if not cond:
        print("ABORT: " + msg)
        sys.exit(1)

# ---------- state.json (string surgery, eol-preserving, validate-before-write) ----------
raw = io.open(SP, encoding="utf-8", newline="").read()
eol = "\r\n" if "\r\n" in raw else "\n"

r2 = raw.replace('"tick": 480,', '"tick": 481,', 1)
must(r2 != raw, "tick anchor not found")

# last array element (R480) has NO trailing comma: anchor its closing quote, append inter-element comma
old_anchor = '"' + eol + ' ],' + eol + ' "ts": "2026-09-27 07:04:06",'
must(old_anchor in r2, "log-array/ts anchor not found")
new_text = ('",' + eol + '  ' + json.dumps(logline, ensure_ascii=False) + eol + ' ],'
            + eol + ' "ts": ' + json.dumps(ts, ensure_ascii=False) + ',')
r2 = r2.replace(old_anchor, new_text, 1)

# task: eof-anchored (last field before closing brace)
tpat = re.compile(r'"task": "[^"]*"' + re.escape(eol) + r'\}')
rm = tpat.search(r2)
must(rm is not None, "task field (eof-anchored) not found")
r2 = r2[:rm.start()] + '"task": ' + json.dumps(task, ensure_ascii=False) + eol + '}' + r2[rm.end():]

a4 = '"focus": "R481: #59 REACT'
must(a4 in r2, "focus round anchor not found")
r2 = r2.replace(a4, '"focus": "R482: #59 REACT', 1)
a5 = "全静即 idle-fast（并窗 6/6 窗满→R486 batch commit R481-R486·跨日边界 09-28 00:00 先到即收）"
must(a5 in r2, "focus window-note anchor not found")
r2 = r2.replace(a5, "全静即 idle-fast（并窗轮 2/6·窗 R481-R486 满 6 收账→R486 batch commit·跨日边界 09-28 00:00 先到即收）", 1)

st = json.loads(r2)
must(st["tick"] == 481, "tick validate failed")
must(st["production"] == "open", "production validate failed")
must(st["log"][-1] == logline, "log tail mismatch")
must(st["log"][-2].startswith("2026-09-27 07:04 R480:"), "log prev-tail mismatch")
must(st["task"] == task and st["ts"] == ts, "ts/task mismatch")
io.open(SP, "w", encoding="utf-8", newline="").write(r2)

# ---------- status-export.json (P-61: export_ts + outs/results derived, F3 no hardcode) ----------
seraw = io.open(SE, encoding="utf-8", newline="").read()
seeol = "\r\n" if "\r\n" in seraw else "\n"
se = json.loads(seraw)
se["export_ts"] = iso

r481_desc = ("tick 481·R481（idle-fast 空转快速路径轮·五静+探针定谳绿·零生产件·并窗轮 1/6 不 commit）——"
"①无新令（orders 顶=O-20260925-1931-HQ-C 零新增零编辑·O- 34 件）+无新集团转办（ledger 五模式正典行数口径 29=锚·r481_check occurrences 41 读数=计量口径偏差 r481_canon 轮内定谳）+无新决策行（decisions UTF8 非空行 45=锚）+production=open 在位零翻正；"
"②backlog 顶行不可认领（#74/#71/#73 done·#72 待 BigLife 台账 ≤09-28 12:00·#59 REACT 09-28 窗届日领〔daily_brief 09-28 缺则先补产〕·#63 C-00030/31 锚正典位不在位 supply-gated 照守·#70 OH 下窗 09-29 21:40·#57 替代率 10-07·W40 周自审 09-28 开周+月度统计注记 ≤09-30·#67 史源耗尽反膨胀律照守·自进池 open 全门控）；"
"③树态=仅并窗自产预期态（HEAD=897fd23 R480 batch 零插队·storylines R480 后零写盘=无 bm-a 迹象·无 index.lock）；"
"④三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面 0 发现/loop_health 2 FAIL+21 WARN 全定谳在案类零新增（49min 停跳=R425 足迹 R426 已裁定·account-lag +1=03-26 中断执行体 done-beat 恒态足迹·新断洞判据 lag ≥2 未破线）；例行件照旧（日报 09-27 在案·global-benchmarks day3 ≤7 跳过）·tokens:local=0·发布锁=M5 账号物理件不变（未上线=未测量）")

se["outs"][0] = [se["outs"][0][0], r481_desc, se["outs"][0][1]]
se["results"][0] = ["481",
    "R481 idle-fast 空转快速路径轮：五静（ledger 29=锚·正典行数口径〔r481_check occurrences 41 读数=计量口径偏差·r481_canon 轮内定谳〕/decisions 45=锚/orders 零新增零编辑）"
    "+三探针定谳（board 0 FAIL·readiness 3 皆外部 0 发现·loop_health 2 FAIL+21 WARN 皆在案类零新增）·零生产件（backlog 各窗未到全门控·#59 09-28 届日/W40 周自审+月度注记 09-28 起）·并窗轮 1/6 不 commit（窗 R481-R486 满 6 收账·跨日边界 09-28 00:00 先到即收）"]

dumped = json.dumps(se, ensure_ascii=False, indent=1)
if seeol == "\r\n":
    dumped = dumped.replace("\n", "\r\n")
trailing = seeol if seraw.endswith(seeol) else ""
io.open(SE, "w", encoding="utf-8", newline="").write(dumped + trailing)

# revalidate both files from disk
st2 = json.loads(io.open(SP, encoding="utf-8", newline="").read())
se2 = json.loads(io.open(SE, encoding="utf-8", newline="").read())
must(st2["tick"] == 481 and st2["log"][-1] == logline, "state revalidate failed")
must(se2["export_ts"] == iso and se2["results"][0][0] == "481", "export revalidate failed")

with io.open(OUTP, "w", encoding="utf-8") as f:
    f.write("ts=%s\ntick=481\ntask_len=%d\nstate=OK\nexport=OK\nv2 comma-law fix applied\n" % (ts, len(task)))
print("OK tick=481 ts=%s task_len=%d" % (ts, len(task)))
