# R300 amend: record 4th red-fix (R299 double-date log prefix) + probe summary into R300 log line and backlog #47.
import io, json

# ---- state.json R300 log line ----
sp = r"src\os\state.json"
d = json.load(io.open(sp, encoding="utf-8"))
assert d["log"][-1].startswith("2026-09-25 23:1"), "last log line is not R300"
line = d["log"][-1]
old3 = "③**随行补账与修红三件**：finished.md F-028 块级登记补块（R299 收账缺口·变更行在案不改写·R297 F-025 补账先例）+cards/README v9 表行补行（R299 同型缺口）+cards/README v6/v7 合并表行拆行修红（R297 插入缺换行致 v6 行缺 F-025 号并入 v7 行·补 F-025 号+拆行·原行分数史不改写）；"
new3 = "③**随行补账与修红四件**：finished.md F-028 块级登记补块（R299 收账缺口·变更行在案不改写·R297 F-025 补账先例）+cards/README v9 表行补行（R299 同型缺口）+cards/README v6/v7 合并表行拆行修红（R297 插入缺换行致 v6 行缺 F-025 号并入 v7 行·补 F-025 号+拆行·原行分数史不改写）+state.json R299 行双日期前缀规范化（上轮收账脚本缺陷「2026-09-25 2026-09-25 23:00:56 R299」=机读心跳面破坏·loop_health log-ts FAIL 揭·内容史实零改写仅前缀规范化·修后复跑 0 FAIL）；"
assert old3 in line, "log line seg3 anchor missing"
line = line.replace(old3, new3)
old4 = "④台账=F-029 登记（成品库第二十八件·L-卡 第十七件·图鉴系列量产第九件）+cards/README 台账两行+变更行+station-reviews R300 行+finished.md F-029 块+变更行+backlog #47 done+status-export 刷；"
new4 = "④台账=F-029 登记（成品库第二十八件·L-卡 第十七件·图鉴系列量产第九件）+cards/README 台账两行+变更行+station-reviews R300 行+finished.md F-029 块+变更行+backlog #47 done+status-export 刷；三探针=board 0 FAIL（5 题 10 稿 5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 面（账号批次①+6/10 GATE+#17）+0 发现（阻塞≠失败口径 exit 1）/loop_health 0 FAIL 19 WARN 皆在案史实（11 log-order+7 heartbeat-gap+account-ahead 瞬态=tick300 vs done299 轮内合法态·R288 同型）；"
assert old4 in line, "log line seg4 anchor missing"
line = line.replace(old4, new4)
d["log"][-1] = line
io.open(sp, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
print("STATE-LOG-AMENDED")

# ---- backlog #47 line ----
bp = r"src\os\backlog.md"
raw = io.open(bp, encoding="utf-8").read()
oldb = "**随行补账与修红**：①finished.md F-028 块级登记补块（R299 收账缺口·变更行在案不改写·R297 F-025 补账先例）②cards/README v9 表行补行（R299 同型缺口）③cards/README v6/v7 合并表行拆行修红（R297 插入缺换行致 v6 行缺 F 号并入 v7 行·补 F-025 号+拆行·原行分数史不改写）；发布锁"
newb = "**随行补账与修红四件**：①finished.md F-028 块级登记补块（R299 收账缺口·变更行在案不改写·R297 F-025 补账先例）②cards/README v9 表行补行（R299 同型缺口）③cards/README v6/v7 合并表行拆行修红（R297 插入缺换行致 v6 行缺 F 号并入 v7 行·补 F-025 号+拆行·原行分数史不改写）④state.json R299 行双日期前缀规范化（上轮收账脚本缺陷=机读心跳面破坏·loop_health log-ts FAIL 揭·内容史实零改写·修后复跑 0 FAIL）；发布锁"
assert raw.count(oldb) == 1, "backlog anchor count=%d" % raw.count(oldb)
io.open(bp, "w", encoding="utf-8", newline="\n").write(raw.replace(oldb, newb))
print("BACKLOG-AMENDED")
