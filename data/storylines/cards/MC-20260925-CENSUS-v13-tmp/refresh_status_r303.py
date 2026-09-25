# -*- coding: utf-8 -*-
"""status-export refresh for R303 (P-61 export step, F3 law: derive from live state)."""
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
    "tick 303·R303（生产轮——图鉴系列量产按序领件第十二件=MC-20260925-CENSUS-v13《城市图鉴 013·何雨欣》"
    "hit-chain §8 全链留痕：M0 四维分 7/8 A 档〔钩 2 反差链：25 岁最流量化职业主播 vs 信条「流量像潮水，我是灯塔不是渔船。」"
    "灯塔定力宣言=最追流量职业×最反流量纪律反差+信条句=潮水×灯塔反差对仗金句级·**信条句=F-018 城市语录 006·逍遥轴信条例逐字同句="
    "语录↔图鉴同句跨形态双档第二证**〔首证=罗大壮 v9 求新轴 F-016↔C-00018〕·**系列首件 MEDIA 城卡**〔城区谱系媒体面展开首证+"
    "主播=职业谱系直播行业首证·何雨欣=万人卡新面孔〕〕+M1 纪实字段汇编律系列化复用〔六行逐条溯 BigLife 手写展示锚 C-00022 verbatim "
    "零新增人格·职业首词主播〔破折号阐释尾=选材排除〕·人设权红线专项核过·脱敏律核=年轮〔含 CEO 令令牌号锚行〕/思想/语言/服装/经历/"
    "行为/关系字段选材排除〕+验图 5/5 一次过=h2_size 44 前置适配系列化第十件=信条/钩子双 20.0em 并列最长驱动型〔50 档排除 20.0em>18.4em·"
    "**46 档排除=20.0em==预算零余量**〔R293 像素级重叠教训〕·44 档 20.91em 余量 0.91em·binding 行=MEDIA 城 · 七段街区 · 主播 "
    "13.35em〔MEDIA 拉丁段〕+物种行 16.25em 同帧单行入窗·em 预算 renderer _em_cost 机核断言入构建脚本·初稿即正字系列化第十二连〕+"
    "七席 ≥9+E4 同轮 8.0 会停下来看+会保存并转发给朋友=三意愿正面明说（「细节描写非常生动·吸引深入了解背景故事」=正面读数·"
    "「没有明显一眼假或空洞套话」正面明说=信任面续证·旗①=信条对不熟悉直播行业者难理解扣 1〔卡面文字旗=信条字段档案 verbatim "
    "不可改写·MC-003 族·吸收位 M5 图文页〕）+F-032 登记=成品库第三十一件·图鉴系列量产第十二件；backlog #50 留痕行 done；"
    "图鉴续件=万人卡按卡号序随轮领〔C-00023 起·锚存在性轮首核〕·L-卡 P0 形态余项=热点速报城市反应版（第三位）·待随轮认领；"
    "ch.5 v3 稿未落〔bm-a 面·稿落即认领·音频线优先口径维持〕）"
)

# --- 量产产线 out (index 1) ---
t1 = j["outs"][1][2]
t1, r = rep(t1, "L-卡 十九件 F-013~F-031（成品库三十件", "L-卡 二十件 F-013~F-032（成品库三十一件", "out1-count")
ok_all = ok_all and r
t1, r = rep(t1, "·E4 8.0 三意愿正面明说〕〕；BS-005/bs005e 视频线",
    "·E4 8.0 三意愿正面明说〕+**R303 MC-CENSUS-v13 图鉴系列量产第十二件**〔C-00022 何雨欣=万人卡新面孔+"
    "**系列首件 MEDIA 城卡**〔城区谱系媒体面首证+主播=职业谱系直播行业首证〕+**信条句=F-018 逍遥轴语录逐字同句="
    "语录↔图鉴同句跨形态双档第二证**·h2_size 44 信条/钩子双 20.0em 并列最长驱动〔**46 档零余量排除新判例**〕·"
    "E4 8.0 三意愿正面明说〕〕；BS-005/bs005e 视频线", "out1-v13")
ok_all = ok_all and r
j["outs"][1][2] = t1

# --- results: tick 302->303, warehouse 30->31 ---
j["results"][0][0] = "303"
t5 = j["results"][4][1]
t5, r = rep(t5, "成品库登记件 F-001~F-006+F-008~F-031", "成品库登记件 F-001~F-006+F-008~F-032", "res4-frange")
ok_all = ok_all and r
t5, r = rep(t5, "+图文卡十九件〔", "+图文卡二十件〔", "res4-cards")
ok_all = ok_all and r
t5, r = rep(t5, "·E4 8.0 三意愿正面明说〕**〕；F-007=BS-005e 预留位",
    "·E4 8.0 三意愿正面明说〕**+**F-032 图鉴系列量产第十二件=按卡号序续领·何雨欣〔万人卡新面孔+系列首件 MEDIA 城卡+"
    "信条句=F-018 逍遥轴同句=语录↔图鉴跨形态双档第二证·h2_size 44 信条/钩子双 20.0em 驱动=46 档零余量排除新判例·"
    "E4 8.0 三意愿正面明说〕**〕；F-007=BS-005e 预留位", "res4-v13")
ok_all = ok_all and r
if '"30",\n' in t5:
    t5 = t5.replace('"30",\n', '"31",\n', 1)
    print("OK: res4-warehouse-count")
else:
    print("SKIP: res4-warehouse-count pattern absent")
j["results"][4][1] = t5

# --- 内容生产部 dept text: prepend v13 ---
for d in j["depts"]:
    if d["n"] == "内容生产部":
        old = "R302 MC-CENSUS-v12 王多多（图鉴系列量产第十一件·F-031·系列首件儿童居民卡）"
        new = ("R303 MC-CENSUS-v13 何雨欣（图鉴系列量产第十二件·F-032·系列首件 MEDIA 城卡+主播职业首证）+"
               "R302 MC-CENSUS-v12 王多多（图鉴系列量产第十一件·F-031·系列首件儿童居民卡）")
        if old in d["t"]:
            d["t"] = d["t"].replace(old, new, 1)
            print("OK: dept-v13")
        else:
            d["t"] = d["t"] + "+R303 MC-CENSUS-v13 何雨欣（图鉴系列量产第十二件·F-032·系列首件 MEDIA 城卡）"
            print("APPEND: dept-v13")
        break

json.dump(j, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.load(io.open(P, encoding="utf-8"))
print("EXPORT OK", j["export_ts"], "ALL-REPLACES:", ok_all)
