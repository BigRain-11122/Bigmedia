# -*- coding: utf-8 -*-
# R382 P-61 export step: docs/status-export.json refresh (export_ts + depts/outs/results derived)
import io, json, time

P = r"docs\status-export.json"
d = json.load(io.open(P, encoding="utf-8"))

d["export_ts"] = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")

for dep in d["depts"]:
    if dep["n"] == u"工程技术部":
        dep["t"] = (u"OS 循环 R382（生产轮·#67 DIGEST 续件第三件全链走门毕=MC-20260926-DIGEST-v4 F-044〔技能动员 P-20260926-01 史源·四源指针逐条可机核·"
                    u"**垂直栈预算律 R381 复用首证**〔VERT 断言过+PIL 实测间隙 29px·新律下首件初渲即过零修参〕·E4 同轮回填 8.0 三意愿正面+零一眼假明说〕"
                    u"+随行 E4 v3 第二飞回填毕〔R381 首飞未落实证→R180/R181 重飞先例→8.0 三意愿正面·review v1.1+净本存档+F-043/README 回填段〕"
                    u"·research §5 在册三候选耗尽注记〔开闸/三线/技能动员=本日三件全制毕·下件候选=新 CEO 令级事件落 ledger 即入池〕"
                    u"·产线 supply-gated 照守=图鉴 C-00030 锚不在位+REACT 新热点窗 09-27+#21 周日件 09-27 届日）·state.ts/task 心跳面刷新")
    if dep["n"] == u"合规审查部":
        dep["t"] = dep["t"].replace(u"F-001~F-006+F-008~F-043 过门登记（四十二件）", u"F-001~F-006+F-008~F-044 过门登记（四十三件）")

for row in d["outs"]:
    if row[0] == u"OS 循环":
        row[2] = (u"tick 382·R382（生产轮·#67 DIGEST 续件第三件全链走门毕：MC-20260926-DIGEST-v4《城市盘点 004·技能动员日数字盘点》F-044=成品库第四十三件·"
                  u"L-卡 第三十二件·DIGEST 形态第四件〔R381 focus 候选序首位领做·M0 7/8 A 档+四源指针逐条可机核〔ledger L116 CEO 原话 verbatim+#65+README Skills 节+C-32〕"
                  u"+验图 5/5 一次过+**垂直栈预算律 R381 复用首证**〔VERT 断言+PIL 实测 10 带全分离间隙 29px·新律下首件初渲即过零修参〕+七席 ≥9+E4 同轮回填 8.0 三意愿正面+零一眼假明说〕"
                  u"+随行 E4 v3 第二飞回填毕〔R381 首飞未落实证→重飞 13:23:29 落地 8.0·review v1.1+净本+F-043/README 回填〕·backlog #67 留痕行维持开板+station-reviews R382 行"
                  u"+cards/README v4 行+finished F-044 行级登记·三探针全绿·实活轮收账 commit）")
    if row[0] == u"量产产线":
        row[2] = row[2].replace(u"L-卡 三十件 F-013~F-042（成品库四十一件·", u"L-卡 三十二件 F-013~F-044（成品库四十三件·")
        row[2] = row[2] + (u"；**R382 MC-DIGEST-v4《城市盘点 004·技能动员日数字盘点》=DIGEST 形态第四件（F-044 成品库第四十三件·L-卡 第三十二件·"
                          u"技能动员 P-20260926-01 史源·四源指针逐条可机核·垂直栈预算律 R381 复用首证〔VERT 断言+PIL 实测间隙 29px·初渲即过零修参〕"
                          u"·E4 8.0 三意愿正面+「没有一眼假或空洞套话」明说·research §5 在册三候选〔开闸/三线/技能动员〕本日全制毕）**")

for chip in d["chips"]:
    pass
if not any(c[0] == u"垂直栈预算律" for c in d["chips"]):
    d["chips"].append([u"垂直栈预算律", u"live"])

for row in d["results"]:
    if row[0] == u"381":
        row[0] = u"382"
    if row[0] == u"42" and row[1].startswith(u"成品库登记件"):
        row[0] = u"43"
        row[1] = row[1].replace(u"F-001~F-006+F-008~F-043", u"F-001~F-006+F-008~F-044")
        row[1] = row[1] + u"+**F-044 DIGEST 形态第四件=R382 技能动员日数字盘点〔垂直栈预算律复用首证·E4 8.0 同轮回填〕**"

json.dump(d, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("EXPORT OK ts=%s chips=%d" % (d["export_ts"], len(d["chips"])))
