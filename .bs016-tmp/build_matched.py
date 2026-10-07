# -*- coding: utf-8 -*-
# R1692 BS-016 matched-cards builder (bs012 same-anchor loopback reuse + bs015/bs014 same-slot precedents)
import json, io

def read(p):
    return io.open(p, encoding="utf-8").read()

def write(p, s):
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)

c = json.loads(read(".bs016-tmp/cards.json"))
assert len(c["cards"]) == 12, len(c["cards"])

VIS = [
 ("data/sources/footage/citywatch-vertical.mp4", "城市观测终端在帧（CityWatch 观城台=题眼问句的城市观测面·第五问/终问观测台位·BS-012/013/014/015 b0 同位·意象对位声明）"),
 ("data/sources/footage/looplog-vertical.mp4", "系统事件日志在帧（系统回城市档案=日志字面直证·BS-015 b1 系统回事件档案同位制式·系统日志体·意象对位声明）"),
 ("data/sources/footage/looplog-vertical.mp4", "系统日志终端在帧（砖一·指令 14:50=第一指令档案直证·BS-012 b1 同锚回环引用位〔十问结构律·首问立记忆〕·同源多用注记）"),
 ("data/sources/footage/reviewsdoc-vertical.mp4", "档案台账在帧（砖二·名字 23:42 一万零三落库=名字过三道校验台账直证·BS-012 b3 同锚回环引用位·Rollout Review Ledger 载体）"),
 ("data/sources/footage/citywatch-vertical.mp4", "城市观测台在帧（砖三·光 04:30 蒸笼发光塔顶纯白=全城唯一发光观测位·BS-012 b5 同锚回环引用位·拍长 4.54s>源净窗 4.400s 走 stream_loop 回环=帧验回环边界律覆盖·R188/R197 净源链继承）"),
 ("data/sources/footage/reviewsdoc-vertical.mp4", "档案载体在帧（问档案一翻就到=检索意象档案实体直证·同源多用注记·意象对位声明）"),
 ("data/sources/footage/editgrid-vertical.mp4", "剪辑时间网格在帧（时间轴倒放=bs012 b6 正放镜像回环·十问结构律「首问立记忆、尾问回收记忆」倒放收束位·自产字卡网格·BS-012/013/014/015 b6 同位）"),
 ("data/sources/footage/reviewsdoc-vertical.mp4", "档案载体在帧（推演声明·基于真实档案=档案载体直证·BS-012/013/014/015 b7 同位·同源多用注记·意象对位声明）"),
 ("data/sources/footage/census-card-v13-vertical.mp4", "图鉴拆条卡在帧（谁砌的都有名有姓=名字在册直接证据·C-00022 新市民派登记面·BS-014 b8 同位先例·R1685 probe 帧提取卡面内容核验实锚）"),
 ("data/sources/footage/reviewsdoc-vertical.mp4", "台账在目在帧（砖是比喻档案是真的=台账真实直证·BS-012 b9 诚实交底同位·同源多用注记·意象对位声明）"),
 ("data/sources/footage/editgrid-vertical.mp4", "剪辑网格在帧（还是我剪的自指拍=剪辑台面直证·BS-012/013/014/015 b10 同位·系列第五件承接·同源多用注记·自产字卡网格）"),
]
for i, (src, req) in enumerate(VIS):
    c["cards"][i]["visual"] = {"source": src, "req": req}
c["cards"][11]["visual"] = {"cards-only": True, "reason": "CTA 收官导流拍常规纯字卡（footage-matching-spec §1·F-004 v15/BS-012/013/014/015 b11 同拍位先例·五问收官位）"}

c["meta"]["order"] = "BS-016-v3"
c["meta"]["visual_spec"] = "docs/footage-matching-spec.md"
c["meta"]["storyboard"] = (
    "BS-016 板块十年终件视觉=第一块砖档案检索回放+十年推演（形态 A+C·源=SC-001-01-v4 立国日档+city-chronicle 立国周纪+BigLife census INDEX·R-20261001 选题框架·R1691 M0 定谳）——"
    "同锚回环引用位=bs012 b1/b3/b5（指令 14:50/名字 23:42/光 04:30 三锚·十问结构律「首问立记忆、尾问回收记忆」收束设计面）+bs012 b6 正放镜像=本件 b6 倒放——"
    "citywatch（观城台=题眼观测面/全城唯一发光观测位）×2+looplog（系统日志=档案回放/第一指令档案）×2+"
    "reviewsdoc（档案载体=名字校验台账/检索意象/推演声明/台账真实）×4+editgrid（时间轴压条倒放/自指拍）×2+"
    "census-card-v13（名字在册=有名有姓直证·BS-014 b8 同位先例）×1+cards-only×1（CTA 收官拍）·"
    "对位 11/12=0.92（层 1.8 ≥0.80 面·BS-012/013/014/015 同位带）·"
    "素材探针=在案证据复用（反重复律）：looplog/reviewsdoc/editgrid 三源三时点零录穿=R808 probe-r808 在案+"
    "citywatch 源裁净窗 4.400s 全程净=R188/R197 修红链实证（b4 拍长 4.54s>源净窗走 stream_loop 回环=帧验回环边界律覆盖）+"
    "census-card-v13=R1685 probe 帧提取卡面内容核验实锚（bs014 b8 拆条面首证同卡）"
)
write("data/sources/bs016/cards-v1-matched.json", json.dumps(c, ensure_ascii=False, indent=2))
m = json.loads(read("data/sources/bs016/cards-v1-matched.json"))
n_vis = sum(1 for x in m["cards"] if "visual" in x)
print("OK matched cards=12 visual=%d ratio=%.3f order=%s" % (n_vis, n_vis / 12.0, m["meta"]["order"]))
