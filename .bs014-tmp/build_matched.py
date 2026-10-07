# -*- coding: utf-8 -*-
# R1685 BS-014 matched-cards builder (bs013 build_matched.py same-type, form-C adjudication)
import json, io

def read(p):
    return io.open(p, encoding="utf-8").read()

def write(p, s):
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)

c = json.loads(read(".bs014-tmp/cards.json"))
assert len(c["cards"]) == 12, len(c["cards"])

VIS = [
 ("data/sources/footage/citywatch-vertical.mp4", "城市观测终端在帧（CityWatch 观城台=题眼问句的城市观测面·第三问观测台位·BS-012/013 b0 同位·意象对位声明）"),
 ("data/sources/footage/looplog-vertical.mp4", "系统指令日志在帧（系统回语录库=库回放的日志字面·系统日志体直证·意象对位声明）"),
 ("data/sources/footage/reviewsdoc-vertical.mp4", "档案载体在帧（信条例在册档案=语录库条目载体·怀旧轴信条溯源面·意象对位声明）"),
 ("data/sources/footage/editgrid-vertical.mp4", "剪辑字卡网格在帧（信条字面陈列形态·自产字卡网格非实盘素材·意象对位声明）"),
 ("data/sources/footage/reviewsdoc-vertical.mp4", "台账档案在帧（在册对账=秩序轴信条在册面·同源多用注记·意象对位声明）"),
 ("data/sources/footage/citywatch-vertical.mp4", "城市观测面在帧（观城台守望位=桥面值守观测呼应·同源多用注记·意象对位声明）"),
 ("data/sources/footage/editgrid-vertical.mp4", "剪辑时间网格在帧（时间轴压条=形态 C 制式位·BS-012/013 b6 同位·自产字卡网格）"),
 ("data/sources/footage/reviewsdoc-vertical.mp4", "档案载体在帧（推演声明基于真实档案=档案载体直证·BS-012/013 b7 同位·意象对位声明）"),
 ("data/sources/footage/census-card-v13-vertical.mp4", "图鉴拆条卡在帧（新市民派登记面=新街坊接着教的登记形态·C-00022 何雨欣卡=形态 C 图鉴语录卡混剪拆条面首证·自产拆条卡零录穿面·卡面 v6 信条陈列=QUOTE 卡 verbatim 面合法位·M0 避让注记）"),
 ("data/sources/footage/looplog-vertical.mp4", "系统日志在帧（真话在册=日志台账字面·同源多用注记·意象对位声明）"),
 ("data/sources/footage/editgrid-vertical.mp4", "剪辑网格在帧（还是我剪的自指拍=剪辑台面直证·BS-012/013 b10 同位·自产字卡网格）"),
]
for i, (src, req) in enumerate(VIS):
    c["cards"][i]["visual"] = {"source": src, "req": req}
c["cards"][11]["visual"] = {"cards-only": True, "reason": "CTA 导流拍常规纯字卡（footage-matching-spec §1·F-004 v15/BS-012/013 b11 同拍位先例）"}

c["meta"]["order"] = "BS-014-v5"
c["meta"]["visual_spec"] = "docs/footage-matching-spec.md"
c["meta"]["storyboard"] = (
    "BS-014 板块十年第三件视觉=六轴信条语录回放+十年传播推演（形态 C·源=QUOTE-v1~v6 六轴信条例在册+R-20261001 选题框架·R1684 M0 定谳）——"
    "语录卡方图派生竖版评估=渲染腿定谳弃用（卡面信条例与成片 H2 卡锚同文双排=文本对撞非对位增益·在案源复用优先律）——"
    "citywatch（观城台=题眼观测面/守望位=桥面呼应）×2+looplog（系统日志=库回放/真话在册）×3+"
    "reviewsdoc（档案载体=信条在册/推演声明）×3+editgrid（字卡网格=信条陈列/时间轴压条=形态 C 制式位/自指拍）×3+"
    "census-card-v13（图鉴拆条=新市民派登记面=形态 C 拆条混剪首证·C-00022 何雨欣卡）×1+cards-only×1（CTA 拍）·"
    "对位 11/12=0.92（层 1.8 ≥0.80 面·BS-012/013/009/010/011 同位带）·"
    "素材探针=在案证据复用（反重复律）：looplog/reviewsdoc/editgrid 三源三时点多模态零录穿=R808 probe-r808（bs011/012/013 同源同窗）+"
    "citywatch 源裁净窗 4.400s 全程净=R188/R197 修红链实证（裁后任意拍任意 offset 全程净窗·拍长于源走 stream_loop 回环=帧验回环边界律覆盖）+"
    "census-card-v13=自产拆条卡（render_card_video 产物·零录穿面·本轮帧提取卡面内容核验=C-00022 新市民派 对位判据实锚）"
)
write("data/sources/bs014/cards-v1-matched.json", json.dumps(c, ensure_ascii=False, indent=2))
m = json.loads(read("data/sources/bs014/cards-v1-matched.json"))
n_vis = sum(1 for x in m["cards"] if "visual" in x)
print("OK matched cards=12 visual=%d ratio=%.3f order=%s" % (n_vis, n_vis / 12.0, m["meta"]["order"]))
