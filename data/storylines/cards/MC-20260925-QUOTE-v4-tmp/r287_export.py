# -*- coding: utf-8 -*-
"""R287: refresh docs/status-export.json (P-61 export step, F3 derived-from-reality)."""
import io, json, time

P = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\docs\status-export.json"
d = json.load(io.open(P, encoding="utf-8"))
now = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
d["export_ts"] = now

def rep(s, old, new):
    assert old in s, "MISS: " + old[:40]
    return s.replace(old, new)

d["do"] = rep(d["do"],
    u"（R286 MC-003 秩序轴 F-015 全链留痕·余轴求新/侠气/逍遥按六轴表格序）",
    u"（R286 MC-003 秩序轴 F-015+R287 MC-004 求新轴 F-016 全链留痕〔一字误写轮内三重闭环+E4 8.0 三意愿齐明说〕·余轴侠气/逍遥按六轴表格序）")

for dep in d["depts"]:
    if dep["n"] == u"内容生产部":
        dep["t"] = rep(dep["t"],
            u"L-卡 三件 F-013/F-014/F-015（成品库十四件·R286 MC-003 秩序轴=系列量产按序领件首件）",
            u"L-卡 四件 F-013/F-014/F-015/F-016（成品库十五件·R286 MC-003 秩序轴+R287 MC-004 求新轴=系列量产按序领件前两件）")
    if dep["n"] == u"合规审查部":
        dep["t"] = rep(dep["t"],
            u"F-001~F-006+F-008~F-015 过门登记（十四件）",
            u"F-001~F-006+F-008~F-016 过门登记（十五件）")
    if dep["n"] == u"工程技术部":
        dep["t"] = (u"OS 循环 R287（L-卡 系列量产按序领件第二件=MC-20260925-QUOTE-v4 求新轴全链走门"
            u"【M0 四维分 7/8 A 档+M1 verbatim 一字误写〔更大→越大〕轮内拦下三重闭环+验图复验转写先行 PASS"
            u"+E4 同轮 8.0 三意愿齐明说=信任面五连+F-016】·前轮 R286 MC-003 秩序轴在案"
            u"·R283 素材窗复核〔D-BS-08 弃件态维持〕+自进 B2 done 维持在案）·state.ts/task 心跳面刷新")

for row in d["outs"]:
    if row[0] == u"OS 循环":
        row[2] = (u"tick 287·R287（生产轮——L-卡 系列量产按序领件第二件=MC-20260925-QUOTE-v4《城市语录 004·求新轴》"
            u"hit-chain §8 全链留痕：M0 四维分 7/8 A 档+M1 verbatim 一字误写轮内拦下三重闭环+验图复验 PASS+七席 ≥9"
            u"+E4 同轮 8.0〔三意愿齐明说系列首件·零扣分旗·信任面五连〕+F-016 登记=成品库十五件；backlog #34 留痕行 done"
            u"；余轴侠气 L142/逍遥 L143 按六轴表格序随轮领；生产线无在途件=N=6 毕+ch.5 v3 稿未落〔bm-a 面〕）")
    if row[0] == u"量产产线":
        row[2] = rep(row[2],
            u"L-卡 三件 F-013/F-014/F-015（成品库十四件·R286 MC-003 秩序轴按序领件毕）",
            u"L-卡 四件 F-013/F-014/F-015/F-016（成品库十五件·R286 MC-003+R287 MC-004 求新轴按序领件毕）")

for row in d["results"]:
    if row[1] == u"OS 轮次":
        row[0] = u"287"
    if row[1].startswith(u"回归测试绿"):
        row[1] = u"回归测试绿（R287 零代码变更·纯数据件+台账轮·维持）"
    if row[1].startswith(u"成品库登记件"):
        row[0] = u"15"
        row[1] = (u"成品库登记件 F-001~F-006+F-008~F-016（短产线 N6 收官+有声五件〔ch.1-ch.4 四件 v3 现行=产线默认〕"
            u"+图文卡四件〔F-013 首件+F-014 hit-chain 首件实证件+F-015 系列量产按序领件首件+F-016 求新轴按序领件第二件〕"
            u"；F-007=BS-005e 预留位=D-BS-08 弃件处置毕·复活条款挂账）")

io.open(P, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2) + u"\n")
print("EXPORT-OK ts=" + now)
