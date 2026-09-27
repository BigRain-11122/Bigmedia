# r490_account.py - R490 idle-fast accounting: state.json (tick 489->490, log append, ts/task refresh, focus->R491) + status-export.json (export_ts, outs/results tick faces); json.load validation built in
import io, json, subprocess

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TS_LINE = "2026-09-27 08:50"
TS_FULL = "2026-09-27 08:50:00"

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

LOG_R490 = (
    "2026-09-27 08:50 R490: idle-fast（快速路径·五静+探针定谳绿·不进开轮四步·并窗轮 3/6 不 commit）——"
    "①无新令（orders 双 NONE=r490_check·锚=O-20260925-1931-HQ-C mtime 19:47:21·O- 34 件零新增零编辑）"
    "+无新集团转办（ledger 五模式正典行数口径 30=锚零新行·r490_check 行数口径直计·内容寻址勿全文重读）"
    "+无新决策行（decisions UTF8 非空行 45=锚·D-20260927-01~05 批后零新）·production=open 自愈核=在位零翻正（r490_check）；"
    "②backlog 顶行不可认领（#75/#74/#71/#73 done·#72 素材消费面知悉挂账〔BigLife 互聊台账 ≤09-28 12:00 到位前零动作〕"
    "·#59 REACT 09-27 窗已毕〔R456 F-045〕09-28 窗届日即领〔daily_brief 09-28 缺则先补产〕"
    "·#63 图鉴 C-00030/C-00031 锚正典位轮首核均不在位〔r490_check anchor False 双证·BigLife census/anchors 20 件尾三止 C-00029〕supply-gated 维持"
    "·#70 OH 下窗 09-29 21:40 后开〔首窗三切片 R432/R458/R459 齐=窗面满〕·#57 替代率首报 10-07 挂账"
    "·W40 周自审 09-28 开周+月度统计注记首件 ≤09-30 随 W40 周审轮·#67 DIGEST 史源耗尽待 ledger 新 CEO 令级事件〔反膨胀律照守〕"
    "·自进池 open 项全门控〔B5 账号期/B3 周更 W40/C4 首进链件触发位〕）；"
    "③树态=仅自产预期件（无 index.lock False 实证·M state.json+M status-export.json=R488/R489 idle-fast 自记账并窗预期态非 bm-a 迹象"
    "+untracked .c3-tmp r488~r490 证据件随并窗批 commit〔R150 先例〕·HEAD=d657506 R487 实活轮 commit 未变 git log 零插队=无 bm-a 活跃写盘迹象"
    "·storylines 三子域 R489 收账后零新写盘 0/0/0=r490_check）；"
    "④例行件：日报 09-27 在案不重跑（R443 补产件·09-28 件=明届日随窗补产）·W39 周审在案（W40 明日 09-28 开周）"
    "·global-benchmarks day3 ≤7 跳过（下期 ~10-01 并窗 M4/S4 门参数复核=R457 调研部首件选题窗）·T1 催办=已裁项停用口径"
    "·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀·mtime 08:14:55 未动）·tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）"
    "·发布锁=M5 账号物理件不变（未上线=未测量）；"
    "三探针定谳=board 0 FAIL（5 题 10 稿·5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现=阻塞≠失败口径 exit 1〔46 renders 全注账〕"
    "/loop_health 2 FAIL+21 WARN 全定谳在案类零新增（FAIL① heartbeat-outage 49min=R425 调度器漏触发同事件足迹 R426 已裁定不重复触发"
    "·FAIL② account-lag done490>tick489=+1 恒态足迹〔03-26 中断执行体 done-beat·R459/R462 在案·新断洞判据 lag ≥2 未破线·本轮收账 tick490 即平〕"
    "·21 WARN=13 log-order+8 heartbeat-gap 全 ≤09-27 03:15 史实零新增）"
    "——探针复制律第二十六证（r490_check.py/r490_probes.py=write_file 新建+OUTP 改指·零 PS 往返零历史件覆写=R462 防再犯律+R466 write_file 预核 tracked 态律双守·本轮零操作红）；"
    "一行收账即出（idle-fast 并窗轮 3/6〔窗 R488-R493 满 6 收账→R493 batch commit·跨日边界 09-28 00:00 先到即收〕·本轮不 commit·P-61 导出步照刷 export_ts+机读 tick 面对齐）。"
    "下轮=R491 快速路径首查（#59 REACT 09-28 热点窗届日领〔daily_brief 09-28 缺则先补产〕/W40 周自审开周+月度统计注记/新令/集团转办——全静即 idle-fast（并窗轮 4/6）。"
)

txt = sub1(txt, ' "tick": 489,', ' "tick": 490,')
txt = sub1(txt, '"focus": "R490: 快速路径首查', '"focus": "R491: 快速路径首查')
txt = sub1(txt, '全静即 idle-fast（并窗轮 3/6·窗 R488-R493 满 6 收账→R493 batch commit）",',
               '全静即 idle-fast（并窗轮 4/6·窗 R488-R493 满 6 收账→R493 batch commit）",')
txt = sub1(txt, NL + ' ],' + NL + ' "ts": "2026-09-27 08:36:00",',
               ',' + NL + '  "' + LOG_R490 + '"' + NL + ' ],' + NL + ' "ts": "' + TS_FULL + '",')
txt = sub1(txt, ' "task": "idle-fast（快速路径·五静+探针定谳绿·不进开轮四步·并窗轮 2/6 不 commit）——①无新令（order"',
               ' "task": "idle-fast（快速路径·五静+探针定谳绿·不进开轮四步·并窗轮 3/6 不 commit）——①无新令（order"')
st = json.loads(txt)
assert st["tick"] == 490 and st["production"] == "open" and st["ts"] == TS_FULL
assert st["log"][-1].startswith("2026-09-27 08:50 R490:")
assert st["focus"].startswith("R491:") and "并窗轮 4/6" in st["focus"]
save_text(sp, txt)
print("state.json OK: tick=490 ts=%s log_tail=R490 focus=R491" % TS_FULL)

# ---------- status-export.json ----------
sep = ROOT + r"\docs\status-export.json"
t2 = load_text(sep)
NL2 = "\r\n" if "\r\n" in t2 else "\n"

OUT_R490 = (
    "tick 490·R490（idle-fast 空转快速路径轮·五静+探针定谳绿·零生产件·并窗轮 3/6 不 commit）——"
    "①无新令（orders 顶=O-20260925-1931-HQ-C 零新增零编辑·O- 34 件·orders_edited_since_anchor NONE）"
    "+无新集团转办（ledger 五模式正典行数口径 30=锚〔R487 P-2026-09-27-02 收讫后新锚〕·r490_check 行数口径直计）"
    "+无新决策行（decisions UTF8 非空行 45=锚）+production=open 在位零翻正；"
    "②backlog 顶行不可认领（#75/#74/#71/#73 done·#72 待 BigLife 台账 ≤09-28 12:00·#59 REACT 09-28 窗届日领〔daily_brief 09-28 缺则先补产〕"
    "·#63 C-00030/31 锚正典位不在位 supply-gated 照守〔anchors 20 件尾三止 C-00029〕·#70 OH 下窗 09-29 21:40·#57 替代率 10-07"
    "·W40 周自审 09-28 开周+月度统计注记 ≤09-30·#67 史源耗尽反膨胀律照守·自进池 open 全门控）；"
    "③树态=仅自产预期态（HEAD=d657506 R487 实活轮 commit 后零插队·storylines R489 后零写盘=无 bm-a 迹象·无 index.lock）；"
    "④三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面 0 发现/loop_health 2 FAIL+21 WARN 全定谳在案类零新增"
    "（49min 停跳=R425 足迹 R426 已裁定·account-lag done490>tick489=+1 恒态足迹·新断洞判据 lag ≥2 未破线）；"
    "例行件照旧（日报 09-27 在案·global-benchmarks day3 ≤7 跳过）·tokens:local=0·发布锁=M5 账号物理件不变（未上线=未测量）"
)

OUT_R489_PRE = (
    "tick 489·R489（idle-fast 空转快速路径轮·五静+探针定谳绿·零生产件·并窗轮 2/6 不 commit·"
    "随行定谳=伤字残留疑云结案〔R488 修红描述文本自指=假阳性·R487 实伤已全复位·扫描判据=排除修法描述段〕）——"
)

RES_R490 = (
    "R490 idle-fast 空转快速路径轮：五静（ledger 30=锚/orders 零新增零编辑/decisions 45=锚）"
    "+三探针定谳绿（board 0 FAIL·readiness 3 皆外部 0 发现·loop_health 2 FAIL+21 WARN 皆在案类零新增）"
    "·零生产件（backlog 各窗未到全门控·#59 09-28 届日/W40 周自审+月度注记 09-28 起）"
    "·idle-fast 并窗轮 3/6 不 commit（窗 R488-R493 满 6 收账→R493 batch commit·跨日 09-28 00:00 先到即收）"
)

# 1) export_ts
t2 = sub1(t2, '"export_ts": "2026-09-27T08:36:00+08:00"', '"export_ts": "2026-09-27T08:50:00+08:00"')
# 2) outs[0][1]: full R489 string -> R490 full string
OLD_OUT_R489 = (
    "tick 489·R489（idle-fast 空转快速路径轮·五静+探针定谳绿·零生产件·并窗轮 2/6 不 commit）——"
    "①无新令（orders 顶=O-20260925-1931-HQ-C 零新增零编辑·O- 34 件·orders_edited_since_anchor NONE）"
    "+无新集团转办（ledger 五模式正典行数口径 30=锚〔R487 P-2026-09-27-02 收讫后新锚〕·r489_check 行数口径直计）"
    "+无新决策行（decisions UTF8 非空行 45=锚）+production=open 在位零翻正；"
    "②backlog 顶行不可认领（#75/#74/#71/#73 done·#72 待 BigLife 台账 ≤09-28 12:00·#59 REACT 09-28 窗届日领〔daily_brief 09-28 缺则先补产〕"
    "·#63 C-00030/31 锚正典位不在位 supply-gated 照守〔anchors 20 件尾三止 C-00029〕·#70 OH 下窗 09-29 21:40·#57 替代率 10-07"
    "·W40 周自审 09-28 开周+月度统计注记 ≤09-30·#67 史源耗尽反膨胀律照守·自进池 open 全门控）；"
    "③树态=仅自产预期态（HEAD=d657506 R487 实活轮 commit 后零插队·storylines R488 后零写盘=无 bm-a 迹象·无 index.lock）；"
    "④三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面 0 发现/loop_health 2 FAIL+21 WARN 全定谳在案类零新增"
    "（49min 停跳=R425 足迹 R426 已裁定·account-lag done489>tick488=+1 恒态足迹·新断洞判据 lag ≥2 未破线）；"
    "例行件照旧（日报 09-27 在案·global-benchmarks day3 ≤7 跳过）·tokens:local=0·发布锁=M5 账号物理件不变（未上线=未测量）"
    "·随行定谳=伤字残留疑云结案（R488 修红描述文本自指=假阳性·R487 实伤已全复位·扫描判据=排除修法描述段）"
)
t2 = sub1(t2, '"' + OLD_OUT_R489 + '"', '"' + OUT_R490 + '"')
# 3) outs[0][2]: prepend compressed R489 before compressed R488
t2 = sub1(t2, '"tick 488·R488（idle-fast 空转快速路径轮·五静+探针定谳绿·零生产件·并窗轮 1/6 不 commit·随行修红=R487 批 GBK 伤字复位）——tick 487·R487',
               '"' + OUT_R489_PRE + 'tick 488·R488（idle-fast 空转快速路径轮·五静+探针定谳绿·零生产件·并窗轮 1/6 不 commit·随行修红=R487 批 GBK 伤字复位）——tick 487·R487')
# 4) results[0]: tick number + text
t2 = sub1(t2, NL2 + '   "489",', NL2 + '   "490",')
OLD_RES_R489 = (
    "R489 idle-fast 空转快速路径轮：五静（ledger 30=锚/orders 零新增零编辑/decisions 45=锚）"
    "+三探针定谳绿（board 0 FAIL·readiness 3 皆外部 0 发现·loop_health 2 FAIL+21 WARN 皆在案类零新增）"
    "·零生产件（backlog 各窗未到全门控·#59 09-28 届日/W40 周自审+月度注记 09-28 起）"
    "·idle-fast 并窗轮 2/6 不 commit（窗 R488-R493·跨日 09-28 00:00 先到即收）"
    "+伤字残留疑云结案（R488 修红描述文本自指=假阳性·R487 实伤已全复位·扫描判据=排除修法描述段）"
)
t2 = sub1(t2, '"' + OLD_RES_R489 + '"', '"' + RES_R490 + '"')
se = json.loads(t2)
assert se["export_ts"] == "2026-09-27T08:50:00+08:00"
assert se["outs"][0][1].startswith("tick 490·R490")
assert se["outs"][0][2].startswith("tick 489·R489")
assert se["results"][0][0] == "490" and se["results"][0][1].startswith("R490")
save_text(sep, t2)
print("status-export.json OK: export_ts=08:50:00 outs=tick490 results=490")

# ---------- final verify: git status snapshot ----------
p = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
print("--- git status ---")
print(p.stdout.strip())
