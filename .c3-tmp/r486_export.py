# r486_export.py - json re-validation gate + status-export refresh (P-61; F3-law derived, no hardcode)
import io, os, json, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r486_export.txt")
L = []
def w(s):
    L.append(str(s))

# 1) state.json json.load re-validation gate (R477/R483 law)
sp = os.path.join(ROOT, "src", "os", "state.json")
with io.open(sp, "r", encoding="utf-8") as f:
    st = json.load(f)
w("state_json_valid=True tick=%d log_entries=%d ts=%s" % (st["tick"], len(st["log"]), st["ts"]))
w("log_tail_head=%s" % st["log"][-1][:40])
w("task_prefix60=%s" % st["task"][:20])

# 2) status-export.json refresh (export_ts + outs OS-loop lines + results tick line)
xp = os.path.join(ROOT, "docs", "status-export.json")
with io.open(xp, "r", encoding="utf-8") as f:
    ex = json.load(f)
now = datetime.datetime.now()
new_ts = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
ex["export_ts"] = new_ts

r486_out = "tick 486·R486（idle-fast 空转快速路径轮·五静+探针定谳绿·零生产件·并窗 6/6 满=本窗 batch commit R481-R486）——①无新令（orders 顶=O-20260925-1931-HQ-C 零新增零编辑·O- 34 件·orders_edited_since_anchor NONE）+无新集团转办（ledger 五模式正典行数口径 29=锚·r486_check 行数口径直计）+无新决策行（decisions UTF8 非空行 45=锚）+production=open 在位零翻正；②backlog 顶行不可认领（#74/#71/#73 done·#72 待 BigLife 台账 ≤09-28 12:00·#59 REACT 09-28 窗届日领〔daily_brief 09-28 缺则先补产〕·#63 C-00030/31 锚正典位不在位 supply-gated 照守〔anchors 20 件尾三止 C-00029〕·#70 OH 下窗 09-29 21:40·#57 替代率 10-07·W40 周自审 09-28 开周+月度统计注记 ≤09-30·#67 史源耗尽反膨胀律照守·自进池 open 全门控）；③树态=仅并窗自产预期态（HEAD=897fd23 R480 batch 零插队·storylines R485 后零写盘=无 bm-a 迹象·无 index.lock）；④三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面 0 发现/loop_health 2 FAIL+21 WARN 全定谳在案类零新增（49min 停跳=R425 足迹 R426 已裁定·account-lag done486>tick485=+1 在飞恒态足迹·新断洞判据 lag ≥2 未破线）；例行件照旧（日报 09-27 在案·global-benchmarks day3 ≤7 跳过）·tokens:local=0·发布锁=M5 账号物理件不变（未上线=未测量）·窗满 6 轮触发=batch commit R481-R486（os-protocol §6·commit 注区间·窗重置 1/6 新窗 R487-R492）"

# outs[0] = ["OS 循环", <R486>, <R485>] (drop oldest R484, keep 2 newest)
old_os = ex["outs"][0]
w("outs0_before=%s" % [x[:24] for x in old_os])
ex["outs"][0] = [old_os[0], r486_out, old_os[1]]
w("outs0_after=%s" % [x[:24] for x in ex["outs"][0]])

# results[0] = ["486", <R486 desc>]
ex["results"][0] = ["486", "R486 idle-fast 空转快速路径轮：五静（ledger 29=锚·正典行数口径直计/decisions 45=锚/orders 零新增零编辑）+三探针定谳（board 0 FAIL·readiness 3 皆外部 0 发现·loop_health 2 FAIL+21 WARN 皆在案类零新增）·零生产件（backlog 各窗未到全门控·#59 09-28 届日/W40 周自审+月度注记 09-28 起）·并窗 6/6 满=batch commit R481-R486（commit 注区间·窗重置 1/6·新窗 R487-R492）"]

with io.open(xp, "w", encoding="utf-8") as f:
    json.dump(ex, f, ensure_ascii=False, indent=1)
    f.write("\n")

# 3) re-validate export json
with io.open(xp, "r", encoding="utf-8") as f:
    ex2 = json.load(f)
w("export_json_valid=True export_ts=%s" % ex2["export_ts"])
w("export_outs0_ticks=%s" % [x[:12] for x in ex2["outs"][0]])
w("export_results0=%s" % ex2["results"][0][0])

with io.open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("\n".join(L))
