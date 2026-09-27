# r504_acct.py - R504 close-of-round accounting (json.load/dump full rewrite = trailing-comma family root fix)
# state.json: tick 503->504, focus->R505, log append, ts/task refresh
# status-export.json: export_ts, outs[0] rotate, results[0]/[1] refresh, depts[0].t append
import io, json, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
now = datetime.datetime.now()
ts = now.strftime("%Y-%m-%d %H:%M:%S")

LOG = (
 "2026-09-27 " + now.strftime("%H:%M") + " R504: O-1050 议程 1 收口轮·R-03 v1.0 毕（§8 四刀补采·实活轮触发收账）——"
 "①五查=无新令（orders 锚=O-1050 mtime 10:56:37=R503 回执行追加·35 件零新增零编辑）+ledger 五模式 30=锚零新转办"
 "+**decisions 锚定谳修正=R503 log「45→48」误记·实况 45**（r503_decisions_snapshot 与现文件尾行逐行一致=D-20260926-09/10/11 非新行系锚内既有·HQ 域零份额定谳维持·锚回正 45 零新行动作）"
 "+树态仅自产证据件+production open 自愈核在位；"
 "②议程 1 §8 四刀补采=**刀④ 公众号推荐规范 2026Q4 复扫成**（A 级直链现行在线·条款与在册快照逐段一致·动态文档条款→M5 前置复扫常设）"
 "+**刀① 抖音换刀 FAIL 定谳维持**（douyin.com/rules+creator.douyin.com 双新刀壳空·并档四通道全壳墙·零断言口径不变）"
 "+**刀② B站创作学院 FAIL 通道卡点**（help.bilibili.com 连接失败+公示页复扫在线壳空同 R19 定谳·B站面维持 in-册 A 级锚）"
 "+**刀③ 视频号创作者中心登录/JS 壳墙**（channels.weixin.qq.com→站内面开号后首读·账号域永不代办）"
 "——1 成 3 卡点皆通道型·fail 如实入件零编造·§六 30 天打法框架不因补采改动（卡点不改选型逻辑）；"
 "③R-20260927-bigstream-03 升 v1.0（§8 执行记录+§3 抖音行+变更行）+令文件 R504 收行追加=**议程 1 收口提前于窗 ≤09-28 10:50**（四议程实况：①done②done R503③未起 R505 起链④随窗）；"
 "④三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现（46 renders 全注账）"
 "/loop_health 2 FAIL+21 WARN 全在案定型零新增（FAIL① 49min=R425 足迹已裁定·FAIL② account-lag +1 done504>tick503=尾轮自beat 残差瞬态·lag ≥2 未破线·本轮收账 tick504 自然吸收）；"
 "⑤例行件：日报 09-27 在案不重跑（09-28 件=明届日随窗补产）·W39 周审在案（W40 明日 09-28 开周+月度统计注记）·global-benchmarks day3 ≤7 跳过（下期 ~10-01）·T1 催办=已裁项停用口径"
 "·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·tokens:local=0（零本地模型调用·四刀=web 采集通道非本地栈·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（未上线=未测量）；"
 "探针复制律第三十八证（r504_check.py/r504_urls.py/r504_acct.py=write_file 新建+OUTP 改指·零 PS 往返零历史件覆写=R462 防再犯律+R466 预核 tracked 态律双守·收账改 json.load/dump 全量写回=尾逗号坑族根治型）"
 "·随行操作红两件轮内闭环如实入账=①轮首 PS && 链 ParserError 零盘面副作用（R457/R471/R472 在案坑族·分跑即过）②inline python 正则转义坑即弃改脚本件法（编码律）。"
 "下轮=R505 议程 3 城市叙事首件样片脚本起链（≤09-29 10:50·先消费 charter 既有立法面）→议程 4 调研部首件选题随窗。"
)

FOCUS = (
 "R505: **O-1050 议程 3 城市叙事首件样片脚本起链**（≤09-29 10:50·先消费 charter 既有立法面=city-storylines-charter 真城真事律"
 "+city_time/节律/事件生灵窗面·派生非编造·U243 互聊台账 ≤09-28 12:00 到位后并入）"
 "→议程 4 调研部首件选题提前交卷（原 ≤10-01 提速随窗）→排期表 v1 缺口补件（视频号位拆条/稿集预产 ≥2 件）=预产窗随轮领候选；"
 "窗口件随查（#59 REACT 09-28 热点窗届日领·daily_brief 09-28 缺则先补产·W40 周自审 09-28 开周+月度统计注记 ≤09-30"
 "·#70 OH 下窗 09-29 21:40·#63 C-00030/31 锚 supply-gated 照守·#72 台账 ≤09-28 12:00）；"
 "探针执行注=loop_health account-lag +1 瞬态=尾轮自beat 残差既裁定型（lag ≥2 才=新断洞判据）；decisions 锚=45（R504 修正案）"
)

# ---- state.json ----
sp = ROOT + r"\src\os\state.json"
st = json.load(io.open(sp, encoding="utf-8"))
assert st["tick"] == 503, "tick drift: %s" % st["tick"]
st["tick"] = 504
st["focus"] = FOCUS
st["log"].append(LOG)
st["ts"] = ts
prefix_len = len("2026-09-27 " + now.strftime("%H:%M") + " ")
st["task"] = LOG[prefix_len:prefix_len + 60]
json.dump(st, io.open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("state ok tick=504 log_len=%d ts=%s" % (len(st["log"]), ts))

# ---- status-export.json ----
sep = ROOT + r"\docs\status-export.json"
se = json.load(io.open(sep, encoding="utf-8"))
se["export_ts"] = now.strftime("%Y-%m-%dT%H:%M:%S") + "+08:00"

OUT504 = (
 "tick 504，R504 实活轮·O-1050 议程 1 收口：**方向研究首件 R-03 升 v1.0**（§8 四刀补采执行毕：刀④ 公众号推荐规范 2026Q4 复扫成·"
 "A 级直链现行在线条款与快照一致+M5 前置复扫常设；刀①②③=抖音四通道壳墙/视频号登录壳墙/B站创作学院通道卡点=1 成 3 卡点 fail 如实入件零断言维持）"
 "·议程 1 提前于窗毕（≤09-28 10:50）·四议程=①done②done R503 ③R505 起链 ④随窗；"
 "**decisions 锚修正=R503「45→48」误记·实况 45**（snapshot 与现文件一致·D-09/10/11 系锚内既有非新行）；"
 "探针=board 0 FAIL/readiness 3 阻塞皆外部 0 发现/loop_health 2F+21W 在案定型零新增。"
)
o0 = se["outs"][0]
se["outs"][0] = [o0[0], OUT504, o0[1]]

se["results"][0] = ["504", (
 "R504 实活轮：O-1050 议程 1 收口（R-03 v1.0·四刀补采 1 成 3 卡点如实·提前于窗）·decisions 锚修正 45（R503 误记 48）。"
 "探针 board 0 FAIL/readiness 3 外部阻塞 0 发现/loop_health 2F+21W 在案。")]

old_r1 = se["results"][1]
se["results"][1] = ["35", old_r1[1].replace("34", "35", 1)
 + "·O-20260927-1050-HQ-C 自驱动员令在册（四议程：①方向研究 v1.0 done R504②排期表 v1 done R503③城市叙事脚本 ≤09-29 10:50④调研部首件随窗）"]

se["depts"][0]["t"] += "·O-20260927-1050-HQ-C 自驱动四议程收口面：①方向研究 R-03 v1.0 done（R504）②发布排期表 v1 done（R503）③城市叙事首件样片脚本 ≤09-29 10:50④调研部首件随窗。"

json.dump(se, io.open(sep, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("status-export ok export_ts=%s" % se["export_ts"])

# ---- verify both files parse back ----
json.load(io.open(sp, encoding="utf-8"))
json.load(io.open(sep, encoding="utf-8"))
print("verify ok: both json parse back clean")
