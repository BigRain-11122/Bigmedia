# -*- coding: utf-8 -*-
# R1689 BS-015 matched-cards builder (bs014 build_matched.py same-type, form-C three-perspective strip face)
import json, io

def read(p):
    return io.open(p, encoding="utf-8").read()

def write(p, s):
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)

c = json.loads(read(".bs015-tmp/cards.json"))
assert len(c["cards"]) == 12, len(c["cards"])

VIS = [
 ("data/sources/footage/citywatch-vertical.mp4", "城市观测终端在帧（CityWatch 观城台=题眼问句的城市观测面·第四问观测台位·BS-012/013/014 b0 同位·意象对位声明）"),
 ("data/sources/footage/looplog-vertical.mp4", "系统事件日志在帧（系统回事件档案=日志字面直证·b1 日志动词骨架位·系统日志体·意象对位声明）"),
 ("data/sources/footage/census-card-v19-vertical.mp4", "图鉴拆条卡在帧（灯视角直接证据=C-00028 十四号路灯卡·台风梅花留补丁源卡·形态 C 三视角拆条混剪·R1685 v13 先例扩三卡面·本轮 probe-r1689 三时点全分辨率核验=静态零录穿）"),
 ("data/sources/footage/census-card-v18-vertical.mp4", "图鉴拆条卡在帧（塔视角直接证据=C-00027 感知塔站值守员邓建国卡·守到风停源卡·形态 C 三视角拆条混剪·同源多用注记见 b4）"),
 ("data/sources/footage/census-card-v18-vertical.mp4", "图鉴拆条卡在帧（塔起名 wink=C-00027 钩子字段尾段「播报员说比编号好记」verbatim 源卡·同源多用注记·lc007 未消费切面独占·形态 C 拆条混剪）"),
 ("data/sources/footage/census-card-v20-vertical.mp4", "图鉴拆条卡在帧（猫视角直接证据=C-00029 咪喱卡·口信一家一家送到源卡·形态 C 三视角拆条混剪·本轮 probe-r1689 三时点全分辨率核验=静态零录穿）"),
 ("data/sources/footage/editgrid-vertical.mp4", "剪辑时间网格在帧（时间轴压条=形态 C 制式位·BS-012/013/014 b6 同位·自产字卡网格）"),
 ("data/sources/footage/reviewsdoc-vertical.mp4", "档案载体在帧（推演声明基于真实档案=档案载体直证·BS-012/013/014 b7 同位·意象对位声明）"),
 ("data/sources/footage/reviewsdoc-vertical.mp4", "档案载体在帧（三样在册对账=灯/塔/猫三视角收束归纳面·同源多用注记·意象对位声明）"),
 ("data/sources/footage/looplog-vertical.mp4", "系统日志在帧（真话在册=诚实交底日志台账字面·同源多用注记·意象对位声明）"),
 ("data/sources/footage/editgrid-vertical.mp4", "剪辑网格在帧（还是我剪的自指拍=剪辑台面直证·BS-012/013/014 b10 同位·自产字卡网格）"),
]
for i, (src, req) in enumerate(VIS):
    c["cards"][i]["visual"] = {"source": src, "req": req}
c["cards"][11]["visual"] = {"cards-only": True, "reason": "CTA 导流拍常规纯字卡（footage-matching-spec §1·F-004 v15/BS-012/013/014 b11 同拍位先例）"}

c["meta"]["order"] = "BS-015-v6"
c["meta"]["visual_spec"] = "docs/footage-matching-spec.md"
c["meta"]["storyboard"] = (
    "BS-015 板块十年第四件视觉=台风梅花同夜三视角档案回放+十年推演（形态 C·源=C-00027 邓建国/C-00028 十四号路灯/C-00029 咪喱 三手写锚在册+R-20261001 选题框架·R1687 M0 定谳）——"
    "三视角拆条混剪=形态 C 拆条面第二证（R1685 bs014 单卡 v13 首证→本件 v18/v19/v20 三卡直接证据面·灯 b2=v19/塔 b3+b4=v18 同源多用/猫 b5=v20）——"
    "citywatch（观城台=题眼观测面）×1+looplog（系统事件日志=系统回档案/真话在册）×2+"
    "reviewsdoc（档案载体=推演声明/三样在册对账）×2+editgrid（时间轴压条=形态 C 制式位/自指拍）×2+"
    "census-card-v18/v19/v20（三视角拆条=直接证据面）×4+cards-only×1（CTA 拍）·"
    "对位 11/12=0.92（层 1.8 ≥0.80 面·BS-012/013/014 同位带）·"
    "素材探针=census v18/v19/v20=本轮 probe-r1689 三时点多模态核验（13s 全静态·零录穿零隐私·全分辨率二验 v18=C-00027 邓建国感知塔站值守员/v20=C-00029 咪喱·tile 低清首读名称误判定谳=读数手段问题如实注记·正典锚=BigLife census/anchors C-00027/28/29 一致）+"
    "looplog/reviewsdoc/editgrid 三源三时点零录穿=R808 probe-r808 在案证据复用（反重复律）+"
    "citywatch 源裁净窗 4.400s 全程净=R188/R197 修红链实证（裁后任意拍任意 offset 全程净窗·拍长于源走 stream_loop 回环=帧验回环边界律覆盖）"
)
write("data/sources/bs015/cards-v1-matched.json", json.dumps(c, ensure_ascii=False, indent=2))
m = json.loads(read("data/sources/bs015/cards-v1-matched.json"))
n_vis = sum(1 for x in m["cards"] if "visual" in x)
print("OK matched cards=12 visual=%d ratio=%.3f order=%s" % (n_vis, n_vis / 12.0, m["meta"]["order"]))
