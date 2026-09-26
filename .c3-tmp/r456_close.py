# -*- coding: utf-8 -*-
# r456 close: status-export.json programmatic refresh (P-61 export step).
# Defensive patches with per-patch FOUND/MISS report; ASCII console output only.
import io, json

P = "docs/status-export.json"
d = json.load(io.open(P, encoding="utf-8"))
rep = []
ok = True

d["export_ts"] = "2026-09-27T02:51:00+08:00"

# 1) dept Engineering/OS loop seat line
new_s = (u"R456: #59 REACT-v3 production chain closed same-round (MC-20260927-REACT-v3 F-045 = "
         u"library piece #44 / L-card #33 / REACT form #3: zhihu 09-27 #8 financial-freedom "
         u"verbatim relay x market_close single-bucket 3-axis [xiaoyao/8, yanhuo/12, sprite/5] "
         u"x C-00025 ferry-captain creed wrap row; M1 source machine-verify 4-asserts in build = "
         u"verbatim-chain mechanization first use [sprite two-level walker pit caught and "
         u"root-fixed in-round]; h2_size 44 zero-margin exclusion R380 precedent band; "
         u"frame-check 5/5 first-pass; seven seats >=9; E4 audience 7.0 same-round three-will "
         u"positive, honest band v1 7.0 / v2 8.0 / v3 7.0, flags = pool-line formulaic -2 / "
         u"sprite context -1; four ledgers updated; next queue = #73 research-dept receipt by "
         u"09-28 12:00, #70 OSS slice 2 by 09-29)")
hit = False
for dept in d["depts"]:
    if dept.get("n") == u"工程技术部":
        dept["s"] = new_s
        hit = True
rep.append("dept_s patched: %s" % hit)
ok = ok and hit

# 2) outs[0] OS loop current line
new_os = (u"tick 456·R456（生产轮·#59 REACT-v3《城市速报 003·财务自由》全链走门毕=F-045 成品库第四十四件·L-卡 第三十三件·"
          u"REACT 形态第三件）——①首核=C-00025 锚存在性+人设权红线过（信条「船稳，人心才稳。」verbatim·非荣誉席·R455 候选转正）"
          u"+M1 双律+**源机核四断言入 build=verbatim 链机核化首件**（日报热点行+锚信条字段+三池句递归 verbatim"
          u"〔逍遥 market_close/8+烟火 market_close/12+sprite market_close/5〕+桶索引回填·首渲踩坑 sprite 两层 walker "
          u"未命中→递归化根修轮内咬住·em-check-r456.txt m1-verify 段）；②M2 出图 exit 0+验图五检 5/5 一次过"
          u"（h2_size 44=反应行 20.00em 双行并列驱动·46 档零余量排除律执行 R293/R310/R380 判例复用·余量 0.91em"
          u"+热点行 12.00em 首见短热点标题型+垂直栈 R381 断言 gap +73px·REACT 零迭代第三连）；③M3 四禁零中+M4 四检过"
          u"+M4.5 七席 ≥9（6×9.0+E7 N/A·评审单 review-20260927-mcreact-v3.md）；④E4 参考仪同轮回填 7.0 三意愿正面明说"
          u"（REACT 带宽如实 v1 7.0/v2 8.0/v3 7.0·旗①=逍遥轴+烟火轴句套路化扣 2=机制反馈位第二现+旗②=像素灵句难懂扣 1"
          u"=v2 同位复发·最弱=像素灵句抽象·净本 20260927-024717）；⑤四台账落账（finished F-045+cards/README v3 行"
          u"+station-reviews R456 行+backlog #59 注·#59 维持开板）；三探针=board 0 FAIL/readiness 3 阻塞皆外部+0 发现"
          u"/loop_health 1 FAIL+20 WARN 皆在案史实；集团双锚静（ledger 五模式 28=锚·decisions 45=锚）；tokens:local=1"
          u"（E4 qwen 一判）；发布锁=M5 账号物理件不变（未上线=未测量）——下轮 R457 首位=#73 调研部回执件（≤09-28 12:00）")
hit = len(d["outs"]) > 0 and d["outs"][0][0] == u"OS 循环"
if hit:
    d["outs"][0][1] = new_os
rep.append("outs_os patched: %s" % hit)
ok = ok and hit

# 3) results[0] tick line
hit = len(d["results"]) > 0 and d["results"][0][0] == "455"
if hit:
    d["results"][0] = ["456", u"R456 生产轮：#59 REACT-v3《城市速报 003·财务自由》全链走门毕=F-045（成品库第四十四件·REACT 第三件·"
                              u"M1 源机核四断言首件+E4 同轮 7.0·七席 ≥9）"]
rep.append("results_tick patched: %s" % hit)
ok = ok and hit

# 4) results[3] F-count + F-range patches
def patch(s, old, new):
    if old in s:
        rep.append("patch FOUND: %s -> %s" % (old[:24], new[:24]))
        return s.replace(old, new), True
    rep.append("patch MISS : %s" % old[:40])
    return s, False

if len(d["results"]) > 3 and d["results"][3][0] == "43":
    d["results"][3][0] = "44"
    rep.append("results_f_count patched 43->44: True")
else:
    rep.append("results_f_count patched: MISS (found %s)" % (d["results"][3][0] if len(d["results"]) > 3 else "n/a",))
    ok = False
d["results"][3][1], h = patch(d["results"][3][1], u"F-008~F-044", u"F-008~F-045")
ok = ok and h

# 5) compliance dept t patch
for dept in d["depts"]:
    if dept.get("n") == u"合规审查部":
        dept["t"], h = patch(dept["t"], u"F-008~F-044 过门登记（四十三件）", u"F-008~F-045 过门登记（四十四件）")
        ok = ok and h

# 6) production line out patch
if len(d["outs"]) > 1:
    d["outs"][1][2], h = patch(d["outs"][1][2], u"L-卡 三十二件 F-013~F-044（成品库四十三件",
                              u"L-卡 三十三件 F-013~F-045（成品库四十四件")
    ok = ok and h

# 7) chips append (idempotent)
names = [c[0] for c in d["chips"]]
if u"M1 源机核 verbatim 断言" not in names:
    d["chips"].append([u"M1 源机核 verbatim 断言", "live"])
    rep.append("chip appended: True")
else:
    rep.append("chip appended: already-present")

json.dump(d, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.load(io.open(P, encoding="utf-8"))  # validity gate
io.open(".c3-tmp/r456_export_report.txt", "w", encoding="utf-8").write("\n".join(rep) + "\nRESULT: " + ("ALL OK" if ok else "HAS MISS"))
print("EXPORT REFRESH " + ("ALL OK" if ok else "HAS MISS"))
