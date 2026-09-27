# r500_account.py - R500 idle-fast accounting: state.json (tick 499->500, log append, ts/task refresh, focus->R501 2/6 window R500-R505) + status-export.json (export_ts, outs/results tick faces); json.load validation built in
import io, json, subprocess, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"

now = datetime.datetime.now()
TS_MIN = now.strftime("%Y-%m-%d %H:%M")
TS_FULL = TS_MIN + ":00"
TS_ISO = now.strftime("%Y-%m-%dT%H:%M") + ":00+08:00"

def load_text(p):
    with io.open(p, "r", encoding="utf-8", newline="") as f:
        return f.read()

def save_text(p, t):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(t)

def sub1(t, old, new):
    n = t.count(old)
    assert n == 1, "anchor not unique (%d): %r" % (n, old[:80])
    return t.replace(old, new)

# ---------- state.json ----------
sp = ROOT + r"\src\os\state.json"
txt = load_text(sp)
NL = "\r\n" if "\r\n" in txt else "\n"
st_old = json.loads(txt)
old_task = st_old["task"]
old_ts = st_old["ts"]
assert st_old["tick"] == 499 and st_old["production"] == "open" and old_ts == "2026-09-27 10:13:00"

LOG_R500 = (
    TS_MIN + " R500: idle-fast（快速路径·五静+探针定谳绿·不进开轮四步·并窗轮 1/6 不 commit）——"
    "①无新令（orders 双 NONE=r500_check·锚=O-20260925-1931-HQ-C mtime 19:47:21·O- 34 件零新增零编辑·orders_edited_since_anchor NONE）"
    "+无新集团转办（ledger 五模式正典行数口径 30=锚零新行·r500_check 行数口径直计·内容寻址勿全文重读）"
    "+无新决策行（decisions UTF8 非空行 45=锚·D-20260927-01~05 批后零新）·production=open 自愈核=在位零翻正（r500_check）；"
    "②backlog 顶行不可认领（#75/#74/#71/#73 done·#72 素材消费面知悉挂账〔BigLife 互聊台账 ≤09-28 12:00 未到位·r500_check os.walk 探针 0 命中〕"
    "·#59 REACT 09-27 窗已毕〔R456 F-045〕09-28 窗届日即领〔daily_brief 09-28 缺则先补产〕"
    "·#63 图鉴 C-00030/C-00031 锚正典位轮首核均不在位〔r500_check anchor False 双证·BigLife census/anchors 20 件尾三止 C-00029〕supply-gated 维持"
    "·#70 OH 下窗 09-29 21:40 后开〔首窗三切片 R432/R458/R459 齐=窗面满〕·#57 替代率首报 10-07 挂账"
    "·W40 周自审 09-28 开周+月度统计注记首件 ≤09-30 随 W40 周审轮·#67 DIGEST 史源耗尽待 ledger 新 CEO 令级事件〔反膨胀律照守〕"
    "·自进池 open 项全门控〔B5 账号期/B3 周更 W40/C4 首进链件触发位〕）；"
    "③树态=仅自产预期件（无 index.lock False 实证·untracked .c3-tmp r500 探针证据件随并窗批 commit〔R150 先例〕"
    "·HEAD=8001641 R494-R499 batch commit 未变 git log 零插队=无 bm-a 活跃写盘迹象"
    "·storylines 三子域 R499 收账后零新写盘 0/0/0=r500_check·state mtime 10:13=R499 自记账足迹〔ts 10:13:00 一致〕）；"
    "④例行件：日报 09-27 在案不重跑（09-28 件=明届日随窗补产）·W39 周审在案（W40 明日 09-28 开周）"
    "·global-benchmarks day3 ≤7 跳过（下期 ~10-01 并窗 M4/S4 门参数复核=R457 调研部首件选题窗）·T1 催办=已裁项停用口径"
    "·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀·mtime 08:14:55 未动）·tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）"
    "·发布锁=M5 账号物理件不变（未上线=未测量）；"
    "三探针定谳=board 0 FAIL（5 题 10 稿·5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现 exit 1〔账号批次①+6/10 GATE+#17〕"
    "/loop_health 2 FAIL+21 WARN 全定谳在案类零新增（FAIL① heartbeat-outage 49min=R425 调度器漏触发同事件足迹 R426 已裁定不重复触发"
    "·FAIL② account-lag done500>tick499=本轮在飞 done-beat 先行于收账 tick 瞬态 +1〔03-26 中断执行体 done-beat 恒态·R459/R462 在案·新断洞判据 lag ≥2 未破线·本轮收账 tick500 即平〕"
    "·21 WARN=13 log-order+8 heartbeat-gap 全 ≤09-27 03:15 史实零新增）"
    "——探针复制律第三十六证（r500_check.py/r500_probes.py=write_file 新建+OUTP 改指·零 PS 往返零历史件覆写=R462 防再犯律+R466 write_file 预核 tracked 态律双守）"
    "·随行注记=轮首 PS &&/& 链 ParserError 两跑零盘面副作用（R457/R471/R472 在案坑族）→分跑+glob 工具替代即过·无操作红入账；"
    "一行收账即出（idle-fast 并窗轮 1/6〔窗 R500-R505 满 6 收账→R505 batch commit·跨日边界 09-28 00:00 先到即收〕·本轮不 commit·P-61 导出步照刷 export_ts+机读 tick 面对齐）。"
    "下轮=R501 快速路径首查（#59 REACT 09-28 热点窗届日领〔daily_brief 09-28 缺则先补产〕/W40 周自审开周+月度统计注记首件/新令/集团转办——全静即 idle-fast（并窗轮 2/6）。"
)

new_task = LOG_R500.split("R500: ", 1)[1][:60]

txt = sub1(txt, ' "tick": 499,', ' "tick": 500,')
txt = sub1(txt, '"focus": "R500: 快速路径首查', '"focus": "R501: 快速路径首查')
txt = sub1(txt, '全静即 idle-fast（并窗轮 1/6·新窗 R500-R505 满 6 收账→R505 batch commit·跨日边界 09-28 00:00 先到即收）",',
               '全静即 idle-fast（并窗轮 2/6·窗 R500-R505 满 6 收账→R505 batch commit·跨日边界 09-28 00:00 先到即收）",')
txt = sub1(txt, NL + ' ],' + NL + ' "ts": "' + old_ts + '",',
               ',' + NL + '  "' + LOG_R500 + '"' + NL + ' ],' + NL + ' "ts": "' + TS_FULL + '",')
txt = sub1(txt, '"task": "' + old_task + '"', '"task": "' + new_task + '"')
st = json.loads(txt)
assert st["tick"] == 500 and st["production"] == "open" and st["ts"] == TS_FULL
assert st["log"][-1].startswith(TS_MIN + " R500:")
assert st["task"] == new_task and len(new_task) == 60
assert st["focus"].startswith("R501:") and "并窗轮 2/6" in st["focus"] and "并窗轮 1/6" not in st["focus"]
save_text(sp, txt)
print("state.json OK: tick=500 ts=%s task_len=%d log_tail=R500 focus=R501 2/6" % (TS_FULL, len(new_task)))

# ---------- status-export.json ----------
sep = ROOT + r"\docs\status-export.json"
t2 = load_text(sep)
NL2 = "\r\n" if "\r\n" in t2 else "\n"

OLD_OUT_R499 = (
    "tick 499·R499（idle-fast 空转快速路径轮·五静+探针定谳绿·零生产件·并窗 6/6 满=本窗 batch commit R494-R499）——"
    "①无新令（orders 顶=O-20260925-1931-HQ-C 零新增零编辑·O- 34 件·orders_edited_since_anchor NONE）"
    "+无新集团转办（ledger 五模式正典行数口径 30=锚〔R487 P-2026-09-27-02 收讫后新锚〕·r499_check 行数口径直计）"
    "+无新决策行（decisions UTF8 非空行 45=锚）+production=open 在位零翻正；"
    "②backlog 顶行不可认领（#75/#74/#71/#73 done·#72 待 BigLife 互聊台账 ≤09-28 12:00〔r499 探针 0 命中未到位〕·#59 REACT 09-28 窗届日领〔daily_brief 09-28 缺则先补产〕"
    "·#63 C-00030/31 锚正典位不在位 supply-gated 照守〔anchors 20 件尾三止 C-00029〕·#70 OH 下窗 09-29 21:40·#57 替代率 10-07"
    "·W40 周自审 09-28 开周+月度统计注记 ≤09-30·#67 史源耗尽反膨胀律照守·自进池 open 全门控）；"
    "③树态=仅自产预期态（HEAD=634e873 R488-R493 batch commit 后零插队·storylines R498 后零写盘=无 bm-a 迹象·无 index.lock）；"
    "④三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面 0 发现/loop_health 2 FAIL+21 WARN 全定谳在案类零新增"
    "（49min 停跳=R425 足迹 R426 已裁定·account-lag done499>tick498=+1 恒态足迹·新断洞判据 lag ≥2 未破线）；"
    "例行件照旧（日报 09-27 在案·global-benchmarks day3 ≤7 跳过）·tokens:local=0·发布锁=M5 账号物理件不变（未上线=未测量）"
)
OUT_R499_PRE = (
    "tick 499·R499（idle-fast 空转快速路径轮·五静+探针定谳绿·零生产件·并窗 6/6 满=本窗 batch commit R494-R499）——"
)
OLD_RES_R499 = (
    "R499 idle-fast 空转快速路径轮：五静（ledger 30=锚/orders 零新增零编辑/decisions 45=锚）"
    "+三探针定谳绿（board 0 FAIL·readiness 3 皆外部 0 发现·loop_health 2 FAIL+21 WARN 皆在案类零新增）"
    "·零生产件（backlog 各窗未到全门控·#59 09-28 届日/W40 周自审+月度注记 09-28 起）"
    "·idle-fast 并窗 6/6 满=本窗 batch commit R494-R499（os-protocol §6 并窗律·窗重置 1/6）"
)

OUT_R500 = (
    "tick 500·R500（idle-fast 空转快速路径轮·五静+探针定谳绿·零生产件·并窗轮 1/6 不 commit）——"
    "①无新令（orders 顶=O-20260925-1931-HQ-C 零新增零编辑·O- 34 件·orders_edited_since_anchor NONE）"
    "+无新集团转办（ledger 五模式正典行数口径 30=锚〔R487 P-2026-09-27-02 收讫后新锚〕·r500_check 行数口径直计）"
    "+无新决策行（decisions UTF8 非空行 45=锚）+production=open 在位零翻正；"
    "②backlog 顶行不可认领（#75/#74/#71/#73 done·#72 待 BigLife 互聊台账 ≤09-28 12:00〔r500 探针 0 命中未到位〕·#59 REACT 09-28 窗届日领〔daily_brief 09-28 缺则先补产〕"
    "·#63 C-00030/31 锚正典位不在位 supply-gated 照守〔anchors 20 件尾三止 C-00029〕·#70 OH 下窗 09-29 21:40·#57 替代率 10-07"
    "·W40 周自审 09-28 开周+月度统计注记 ≤09-30·#67 史源耗尽反膨胀律照守·自进池 open 全门控）；"
    "③树态=仅自产预期态（HEAD=8001641 R494-R499 batch commit 后零插队·storylines R499 后零写盘=无 bm-a 迹象·无 index.lock）；"
    "④三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面 0 发现/loop_health 2 FAIL+21 WARN 全定谳在案类零新增"
    "（49min 停跳=R425 足迹 R426 已裁定·account-lag done500>tick499=+1 瞬态足迹·新断洞判据 lag ≥2 未破线）；"
    "例行件照旧（日报 09-27 在案·global-benchmarks day3 ≤7 跳过）·tokens:local=0·发布锁=M5 账号物理件不变（未上线=未测量）"
)
RES_R500 = (
    "R500 idle-fast 空转快速路径轮：五静（ledger 30=锚/orders 零新增零编辑/decisions 45=锚）"
    "+三探针定谳绿（board 0 FAIL·readiness 3 皆外部 0 发现·loop_health 2 FAIL+21 WARN 皆在案类零新增）"
    "·零生产件（backlog 各窗未到全门控·#59 09-28 届日/W40 周自审+月度注记 09-28 起）"
    "·idle-fast 并窗轮 1/6 不 commit（窗 R500-R505 满 6 收账→R505 batch commit·跨日 09-28 00:00 先到即收）"
)

# 1) export_ts
t2 = sub1(t2, '"export_ts": "2026-09-27T10:13:00+08:00"', '"export_ts": "' + TS_ISO + '"')
# 2) outs[0][1]: full R499 string -> R500 full string
t2 = sub1(t2, '"' + OLD_OUT_R499 + '"', '"' + OUT_R500 + '"')
# 3) outs[0][2]: prepend compressed R499 before compressed R498
t2 = sub1(t2, '"tick 498·R498（', '"' + OUT_R499_PRE + 'tick 498·R498（')
# 4) results[0]: tick number + text
t2 = sub1(t2, NL2 + '   "499",', NL2 + '   "500",')
t2 = sub1(t2, '"' + OLD_RES_R499 + '"', '"' + RES_R500 + '"')
se = json.loads(t2)
assert se["export_ts"] == TS_ISO
assert se["outs"][0][1].startswith("tick 500·R500")
assert se["outs"][0][2].startswith("tick 499·R499") and "tick 498·R498" in se["outs"][0][2]
assert se["results"][0][0] == "500" and se["results"][0][1].startswith("R500")
save_text(sep, t2)
print("status-export.json OK: export_ts=%s outs=tick500 results=500" % TS_ISO)

# ---------- final verify: git status snapshot ----------
p = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
print("--- git status (M count / head) ---")
lines = [ln for ln in (p.stdout or "").splitlines() if ln.strip()]
print("lines=%d head=%s" % (len(lines), lines[0] if lines else "CLEAN"))
