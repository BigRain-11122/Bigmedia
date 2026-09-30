# -*- coding: utf-8 -*-
"""R659 close: declared-idle accounting (state.json + status-export.json refresh, window 1/6, no commit)."""
import io, json, os, datetime, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

now = datetime.datetime.now()
ts_line = now.strftime("%Y-%m-%d %H:%M")
ts_field = now.strftime("%Y-%m-%d %H:%M:%S")
export_ts = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")

LOG = (
    "2026-09-29 " + now.strftime("%H:%M") + " R659: declared-idle 空轮判定（五静+探针绿+可领序尽·P-2026-09-28-02 ②④序·"
    "新窗 1/6=R659-R664 本窗不 commit〔满 6 或跨日 09-30 00:00 先到即 batch commit〕）——"
    "①五查静：无新令（orders 顶=O-20260928-1910 19:12:33 锚未动·41 O-件）+无新集团转办（ledger 严格 @ 前缀 34 行=锚·"
    "rowdiff vs r644_lednew5 基线〔L 前缀剥离正法〕NEW=0 GONE=0=零新 CEO 令级事件〔#67 触发律不解锁〕）+无新决策行"
    "（集团 decisions UTF8 非空行 68=锚·mtime 03:20:29 未动）+production=open 自愈核在位零翻正+无 index.lock；"
    "②树态=bm-a codex 批未闭（README staged+3+city-humanities 双 M·mtime 04:06·HEAD b8344d0 R658 05:56 后零新 commit）"
    "=五维计数台账共享面让位维持（R651 裁定）+untracked 全属 .sc003-tmp（09-27 史实批 41 件+新列 audio/s1/probe 族同批）"
    "/.sc003-v3-tmp/本轮 .c3-tmp 探针族零外族路径；"
    "③供给面专项核验（轮首 pools.json 1626 原始行读数触发深查·三源定谳全负如实入账）：a 腿=pools.json 06:06:02 重写"
    "但叶数 1440=1440 零增量（1626=原始行数≠叶行数·r633/r659 双探针同读数·r659_pool.txt 证据件）=台词池源闭零新谚语料；"
    "b 腿/#63=BigLife registry 万人卡 ~9503 张落位（GM 2801/MD 1998/NS 1204/OR 1002/QT 2498·顶 C-10036·09-28 23:41）"
    "但 R316 在案裁定 registry 生成批次 P-0 登记卡≠手写展示锚·供给门正典位=census/anchors/ 仍 20 卡止 C-00029=supply-gated "
    "照守〔R316 误判重蹈险本轮探针拦住·C-00030/31 实存位=registry/OR 非锚〕；c 腿=锚池 C-00022/23/25 内容改写（09-28/29）"
    "微增量·二轮深采 R650 已毕+目标文件 city-humanities=bm-a 让位区；"
    "④可领序尽=#86 四腿全 gated（a 腿源闭/b 腿锚止 C-00029/c 腿让位/d 腿=README 让位面）/#70 窗 2=09-29 21:40 后开未到"
    "〔切片 1 已毕 R644=窗面义务足〕/#67 零新事件/#63 供给门闭/#59 REACT v6 挂 09-30 窗/#31 ch5 稿未落 supply-gated/"
    "#78 素材门 blocked/#66 CEO 物理件/queue 顶项全 gated（B5 账号期·C4 触发位）+W40 窗提案 P-1 已交（试点 1/2 毕·终判挂 "
    "REACT v6）=保护态豁免面在案（门控型/素材窗 blocked/bm-a 在途批/CEO 物理件待开）→declared-idle 一行声明收轮合法；"
    "⑤三探针=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现〔阻塞≠失败口径〕/"
    "loop_health FAIL+WARN 全在案类零新增（outage 49min+609min=同事件足迹裁定不重复触发·account-lag beat659>tick658=轮内瞬态"
    " tick659 收账自平 R615-R657 先例连）；例行件：日报 09-29 在案不重跑（R637 补产）·W40 周审在案（R576）·W41 周报=10-05 后"
    "首个周轮·global-benchmarks ≤7 跳过（下期 10-01=#80 并窗）·T1 催办=已裁项停用口径·当日无集团层新 open 问题=HQ-FEEDBACK "
    "不写〔零膨胀〕·tokens:local=0〔探针+核验纯脚本零本地模型调用·P-54⑤ 计量律如实记〕·发布锁=M5 账号物理件不变（未上线未测量）"
    "——下轮=R660 可领序=①#86 codex 续采（让位解除判据=bm-a 批闭 commit 落地·a 腿源闭注记）②#70 下窗切片 2（21:40 后）"
    "③#67 编年史事件候选（触发律）——五查锚不变（orders O-1910/ledger 34/decisions 68）。"
)

FOCUS = (
    "R660: 空轮判定路径开轮——可领序=①#86 codex 续采余量（让位解除判据=bm-a 批闭 commit 落地·四腿态：a 腿源闭"
    "〔pools.json 叶数 1440 零增量·06:06 重写非增长〕/b 腿锚止 C-00029 supply-gated〔registry ~9503 张=R316 裁定生成卡非手写锚"
    "勿重蹈·C-00030/31 实存位=registry/OR〕/c 腿 city-humanities=bm-a 在途批让位/d 腿=README 让位面）②#70 OSS 下窗切片 2"
    "（09-29 21:40 后开·OH-20260929-bigstream.md 续写·实搜面 ≥2+候选 ≥1 五门评估）③#67 编年史事件候选（ledger 新 CEO 令级事件"
    "落账触发律·反膨胀律照守）——W40 窗提案 P-1 已交（试点 1/2 判读毕·终判挂 REACT v6=09-30 热点窗）·#82 已毕——五查锚=orders 顶 "
    "O-20260928-1910 19:12:33·ledger 34（rowdiff 基线=.c3-tmp/r644_lednew5.txt·L 前缀剥离正法）·decisions 68——R659 "
    "declared-idle 窗 1/6=R659-R664（满 6 或跨日 09-30 00:00 batch commit·commit 注区间）"
)

# --- state.json ---
sp = os.path.join("src", "os", "state.json")
d = json.load(io.open(sp, encoding="utf-8"))
assert d["tick"] == 658, "tick baseline drift: %s" % d["tick"]
assert d["production"] == "open", "production not open!"
d["tick"] = 659
d["log"].append(LOG)
d["ts"] = ts_field
task_src = LOG.split(" ", 2)[2]  # drop date + time
d["task"] = task_src[:60]
d["focus"] = FOCUS
io.open(sp, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))

# --- status-export.json ---
ep = os.path.join("docs", "status-export.json")
e = json.load(io.open(ep, encoding="utf-8"))
e["export_ts"] = export_ts
res = e.get("results", [])
res.append(["659", "R659 declared-idle 空轮判定（五静+探针绿+可领序尽·窗 1/6）：五查锚静（orders O-1910/ledger 34 rowdiff 0/decisions 68）·bm-a codex 批未闭让位维持·供给面专项核验三源全负定谳（a 腿 pools.json 叶数 1440=1440 零增量源闭/b 腿 registry ~9503 张=R316 裁定非手写锚·anchors 止 C-00029 supply-gated 照守/c 腿让位+二轮深采毕）·可领序尽（#86 四腿 gated/#70 未到窗/#67 零新事件/queue gated/W40 提案已交）=保护态豁免面在案·三探针 board 0F/readiness 3 外部 0 发现/loop 在案类·tokens:local=0·下轮可领序 #86 让位判据/#70 21:40/#67 触发律"])
# trim to last 8 rows like prior exports
if len(res) > 8:
    e["results"] = res[-8:]
else:
    e["results"] = res
# OS row update
osrow = None
for row in e.get("outs", []):
    if row and row[0] == "OS 循环":
        osrow = row
        break
if osrow is not None:
    osrow[1] = "tick 659：R659 declared-idle 空轮判定（五静+探针绿+可领序尽·P-02 ②④序·窗 1/6=R659-R664）：供给面三源核验全负（a 腿源闭 1440=1440/b 腿 registry 9503 张 R316 裁定非手写锚·anchors 止 C-00029/c 腿让位）·bm-a codex 批未闭让位维持·三探针 board 0F/readiness 3 皆外部/loop 在案类·tokens:local=0——下轮 R660 可领序=①#86（bm-a 批闭判据）②#70 切片 2（21:40 后）③#67 触发律"
io.open(ep, "w", encoding="utf-8").write(json.dumps(e, ensure_ascii=False, indent=2))

# --- verify (R615 verify 生成律: numbers expected synced) ---
d2 = json.load(io.open(sp, encoding="utf-8"))
e2 = json.load(io.open(ep, encoding="utf-8"))
checks = {
    "tick659": d2["tick"] == 659,
    "prod_open": d2["production"] == "open",
    "log_tail_r659": d2["log"][-1].startswith("2026-09-29") and "R659:" in d2["log"][-1][:40],
    "ts_field": d2["ts"] == ts_field,
    "task_60": d2["task"] == task_src[:60] and len(d2["task"]) <= 60,
    "focus_r660": d2["focus"].startswith("R660:"),
    "export_ts_fresh": e2["export_ts"] == export_ts,
    "results_has_659": any(r[0] == "659" for r in e2["results"]),
    "os_row_tick659": any(r[0] == "OS 循环" and "tick 659" in r[1] for r in e2["outs"]),
}
out = io.open(os.path.join(".c3-tmp", "r659_verify.txt"), "w", encoding="utf-8")
allok = True
for k, v in checks.items():
    out.write("%s %s\n" % (k, "PASS" if v else "FAIL"))
    allok = allok and v
out.write("ALL_PASS %s\n" % allok)
out.close()
print("tick", d2["tick"], "| ts", ts_field, "| ALL_PASS", allok)
if not allok:
    sys.exit(1)
