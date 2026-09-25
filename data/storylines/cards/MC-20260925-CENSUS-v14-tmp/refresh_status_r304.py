# -*- coding: utf-8 -*-
"""status-export refresh for R304 (P-61 export step, F3 law: derive from live state).
Includes drift fix: results[4][0] count stale 29 (R301-era, R302/R303 count pattern
broke) -> 32; dept 合规审查部 F-range/card-count stale sync."""
import io, json, datetime

P = "docs/status-export.json"
j = json.load(io.open(P, encoding="utf-8"))

now = datetime.datetime.now()
j["export_ts"] = now.strftime("%Y-%m-%dT%H:%M:%S") + "+08:00"

def rep(s, old, new, tag):
    if old not in s:
        print("MISS:", tag)
        return s, False
    if s.count(old) != 1:
        print("AMBIG:", tag, s.count(old))
        return s, False
    print("OK:", tag)
    return s.replace(old, new), True

ok_all = True

# --- OS 循环 out (index 0): full refresh ---
j["outs"][0][2] = (
    "tick 304·R304（生产轮——图鉴系列量产按序领件第十三件=MC-20260925-CENSUS-v14《城市图鉴 014·潘志明》"
    "hit-chain §8 全链留痕：M0 四维分 7/8 A 档〔钩 2 反差链：47 岁选题馆守门人 vs 信条「毙稿不毙人，选题选良心。」"
    "毙稿〔最否定行为〕×不毙人〔最人文温度〕反差对仗金句级+钩子行「全城唯一保留『毙稿理由档案』的选题官」=具体稀缺性·"
    "每天毙稿三十留下三个/留言墙亲手拆信/深夜地标灯=事实性赛博意象·**MEDIA 城第二卡=同城续证**〔v13 何雨欣首证后〕+"
    "**选题官=职业谱系内容选题行业首证=本司同源职业自指位**+**前后卡承接位=C-00023 关系字段「最服气的主播是何雨欣」="
    "v13 相邻卡互证**〔R298 师承/邻居同型·关系字段=选材排除不进卡面〕·潘志明=万人卡新面孔〕〕+M1 纪实字段汇编律系列化复用"
    "〔六行逐条溯 BigLife 手写展示锚 C-00023 verbatim 零新增人格·职业首词选题官〔破折号阐释尾=选材排除〕·人设权红线专项核过·"
    "脱敏律核=年轮/思想/语言/服装/经历/行为/关系字段选材排除〕+验图 5/5 一次过=h2_size 50 前置适配系列化第十一件=钩子 18.0em "
    "单行驱动回摆型〔50 档 budget 18.4em≥18.0em 余量 0.4em=**正余量入档·零余量排除律不触发**〔v13 46 档 20.0==20.0 对照〕·"
    "19.0em 起才排除 50 档〔v3 判例〕=前置适配带两端判例补全·信条 17.0em+binding 行 15.35em〔MEDIA 拉丁段〕+物种行 15.25em 同帧"
    "单行入窗·em 预算 renderer _em_cost 机核断言入构建脚本·初稿即正字系列化第十三连〕+七席 ≥9+E4 同轮 8.0 会停下来看+会保存并"
    "转发给朋友=三意愿正面明说（「创意、细节和叙事上都做得很好」=正面读数·「似乎没有明显的空洞套话的地方」=信任面续证·"
    "旗①=信条过于理想化扣 1〔卡面文字旗=verbatim 不可改写·吸收位 M5 图文页〕+旗②=深夜地标灯语境段扣 0.5〔非卡面=材料语境段旗·"
    "行为字段=选材排除〕〕+F-033 登记=成品库第三十二件·图鉴系列量产第十三件；backlog #51 留痕行 done；"
    "图鉴续件=万人卡按卡号序随轮领〔C-00024 起·锚存在性轮首核〕·L-卡 P0 形态余项=热点速报城市反应版（第三位）·待随轮认领；"
    "ch.5 v3 稿未落〔bm-a 面·稿落即认领·音频线优先口径维持〕；随行修红=status-export results[4] 计数陈账 29→32（R302/R303 "
    "刷新脚本计数 pattern 断链·文本面 F 系已对·纯计数位滞后两轮如实入账）+合规审查部 F 系/卡系数陈账同步（F-030→F-033·"
    "C-00020→C-00023）+工程技术部 OS 循环节陈账同步（R301→R304））"
)

# --- 量产产线 out (index 1) ---
t1 = j["outs"][1][2]
t1, r = rep(t1, "L-卡 二十件 F-013~F-032（成品库三十一件", "L-卡 二十一件 F-013~F-033（成品库三十二件", "out1-count")
ok_all = ok_all and r
t1, r = rep(t1, "·E4 8.0 三意愿正面明说〕〕；BS-005/bs005e 视频线",
    "·E4 8.0 三意愿正面明说〕+**R304 MC-CENSUS-v14 图鉴系列量产第十三件**〔C-00023 潘志明=万人卡新面孔+"
    "**MEDIA 城第二卡同城续证**+选题官=职业谱系内容选题行业首证=本司同源职业自指位+**前后卡承接位=v13 何雨欣关系面互证**〔"
    "选材排除注记〕·h2_size 50 回摆适配=钩子 18.0em 正余量 0.4em=前置适配带两端判例补全·E4 8.0 三意愿正面明说〕〕；"
    "BS-005/bs005e 视频线", "out1-v14")
ok_all = ok_all and r
j["outs"][1][2] = t1

# --- results: tick 303->304, warehouse count drift fix 29->32, F range -> F-033 ---
j["results"][0][0] = "304"
t5 = j["results"][4][1]
t5, r = rep(t5, "成品库登记件 F-001~F-006+F-008~F-032", "成品库登记件 F-001~F-006+F-008~F-033", "res4-frange")
ok_all = ok_all and r
t5, r = rep(t5, "+图文卡二十件〔", "+图文卡二十一件〔", "res4-cards")
ok_all = ok_all and r
t5, r = rep(t5, "E4 8.0 三意愿正面明说〕**〕；F-007=BS-005e 预留位",
    "E4 8.0 三意愿正面明说〕**+**F-033 图鉴系列量产第十三件=按卡号序续领·潘志明〔万人卡新面孔+**MEDIA 城第二卡同城续证**+"
    "选题官=职业谱系内容选题行业首证=本司同源职业自指位+**前后卡承接位=v13 何雨欣关系面互证**〔选材排除注记〕·"
    "h2_size 50 回摆适配=钩子 18.0em 正余量 0.4em=前置适配带两端判例补全·E4 8.0 三意愿正面明说〕**〕；F-007=BS-005e 预留位",
    "res4-v14")
ok_all = ok_all and r
j["results"][4][1] = t5
if j["results"][4][0] == "29":
    j["results"][4][0] = "32"
    print("OK: res4-warehouse-count drift fix 29->32")
else:
    print("UNEXPECTED res4 count:", j["results"][4][0])
    j["results"][4][0] = "32"

# --- 回归测试 line: R298 -> R304 (this round also zero code change) ---
t2 = j["results"][2][1]
t2, r = rep(t2, "（R298 零代码变更·纯数据件+台账轮·维持）", "（R304 零代码变更·纯数据件+台账轮·维持）", "res2-tests")
ok_all = ok_all and r
j["results"][2][1] = t2

# --- 内容生产部 dept text: prepend v14 ---
for d in j["depts"]:
    if d["n"] == "内容生产部":
        old = "R303 MC-CENSUS-v13 何雨欣（图鉴系列量产第十二件·F-032·系列首件 MEDIA 城卡+主播职业首证）"
        new = ("R304 MC-CENSUS-v14 潘志明（图鉴系列量产第十三件·F-033·MEDIA 城第二卡+选题官职业首证=本司同源职业自指位）+"
               "R303 MC-CENSUS-v13 何雨欣（图鉴系列量产第十二件·F-032·系列首件 MEDIA 城卡+主播职业首证）")
        if old in d["t"]:
            d["t"] = d["t"].replace(old, new, 1)
            print("OK: dept-v14")
        else:
            d["t"] = d["t"] + "+R304 MC-CENSUS-v14 潘志明（图鉴系列量产第十三件·F-033·MEDIA 城第二卡）"
            print("APPEND: dept-v14")
        break

# --- 合规审查部 dept text: stale F-range/card-count sync (R301-era -> live) ---
for d in j["depts"]:
    if d["n"] == "合规审查部":
        old = "F-001~F-006+F-008~F-030 过门登记（二十九件）"
        new = "F-001~F-006+F-008~F-033 过门登记（三十二件）"
        if old in d["t"]:
            d["t"] = d["t"].replace(old, new, 1)
            print("OK: dept-compliance-frange")
        else:
            print("MISS: dept-compliance-frange")
        old2 = "CENSUS 形态=C-00010~C-00020 十一卡非荣誉席"
        new2 = "CENSUS 形态=C-00010~C-00023 十四卡非荣誉席"
        if old2 in d["t"]:
            d["t"] = d["t"].replace(old2, new2, 1)
            print("OK: dept-compliance-cards")
        else:
            print("MISS: dept-compliance-cards")
        break

# --- 工程技术部 dept text: OS loop line refresh (R301-era -> R304) ---
for d in j["depts"]:
    if d["n"] == "工程技术部":
        d["t"] = ("OS 循环 R304（图鉴系列量产按序领件第十三件=MC-20260925-CENSUS-v14 潘志明居民图鉴全链走门"
                  "【M0 四维分 7/8 A 档+纪实字段汇编律系列化复用+h2_size 50 前置适配系列化第十一件=钩子 18.0em 单行驱动回摆型"
                  "（50 档 budget 18.4em≥18.0em 余量 0.4em 正余量入档·零余量排除律不触发·信条 17.0em+binding 行 15.35em 同帧"
                  "单行入窗·em 预算 renderer _em_cost 机核断言化）·验图 5/5 一次过+E4 同轮 8.0 三意愿正面明说+F-033·按卡号序"
                  "续领第十三件】·前轮 R303 MC-CENSUS-v13 在案）·state.ts/task 心跳面刷新")
        print("OK: dept-eng-loop-refresh")
        break

json.dump(j, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.load(io.open(P, encoding="utf-8"))
print("EXPORT OK", j["export_ts"], "ALL-REPLACES:", ok_all)
