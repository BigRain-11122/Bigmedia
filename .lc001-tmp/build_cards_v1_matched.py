# R511: build LC-001 cards-v1-matched.json (baseline TTS cards + per-beat visual declarations)
import json, io

SRC = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.lc001-tmp\cards.json"
DST = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\sources\lc001\cards-v1-matched.json"

with io.open(SRC, encoding="utf-8") as fh:
    j = json.load(fh)

CARD_SRC = "data/sources/footage/census-card-v7-vertical.mp4"
REV_SRC = "data/sources/footage/reviewsdoc-vertical.mp4"

REQS = [
    "源卡钩子行「全城唯一按涨跌调整菜谱的人」在帧（拆条形态=源卡即证据·F-026 成品卡 verbatim 行）",
    "源卡档案行 C-00016·徐根福/碳基市民·弄堂派·男·66 岁/QUANT 城·K线广场·食堂大厨在帧=居民档案面",
    "源卡在帧=被读档案（拍文=锚 C-00016 语言/性格字段「火候」展开·同源多用注记）",
    "源卡在帧=被读档案（拍文=锚 C-00016 行为/节律字段展开·同源多用注记）",
    "源卡钩子行「按涨跌调整菜谱」前提在帧（绿盘日菜单拍=钩子行展开）",
    "源卡钩子行前提在帧（红盘日菜单拍=钩子行展开）",
    "源卡在帧=被读档案（拍文=锚 C-00016 经历字段·1980 老照片展开·同源多用注记）",
    "源卡在帧=被读档案（拍文=锚 C-00016 起源字段展开·同源多用注记）",
    "源卡在帧=被读档案（拍文=锚 C-00016 思想字段展开·同源多用注记）",
    "Station Reviews 台账在帧=双日志入档直接证据（台账=档案实物面）",
    "源卡信条行「行情再绿，汤是热的。」在帧（verbatim 直引）",
    "源卡本体在帧=全档案面（底部档案行「基于硅基城市居民户籍卡档案（展示锚 C-00016）」在帧）",
]

cards = j["cards"]
assert len(cards) == 12, "expect 12 beats, got %d" % len(cards)
durs = []
for i, c in enumerate(cards):
    durs.append((i, round(c["end"] - c["start"], 2)))
    src = REV_SRC if i == 9 else CARD_SRC
    c["visual"] = {"source": src, "req": REQS[i]}

print("beat_durations", durs)
print("max_dur", max(d for _, d in durs))

j["meta"]["visual_spec"] = "docs/footage-matching-spec.md"
j["meta"]["storyboard"] = ("LC-001 拆条形态=源卡即证据：12 拍拍稿逐拍引源卡/锚卡 C-00016 字段，"
                           "画面=被读档案本体（F-026 成品卡 660px 上区+zoompan 微动）+b9 台账实物；"
                           "对位 12/12·同源多用逐拍注记")

with io.open(DST, "w", encoding="utf-8") as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print("written ->", DST)
