# R514: build BS-006 cards-v1-matched.json (baseline TTS cards + per-beat visual declarations)
# probe-informed honest mapping (probe-src-tile.png): looplog=BS-loop.log terminal w/ state+health
# readouts; reviewsdoc=Station Reviews ledger table (verdict/evidence cols); editgrid=self-made
# chapter frame grid; citywatch=city dashboard (no honest face for this topic -> not used)
import json, io

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SRC = ROOT + r"\.bs006-tmp\cards.json"
DST = ROOT + r"\data\sources\bs006\cards-v1-matched.json"

with io.open(SRC, encoding="utf-8") as fh:
    j = json.load(fh)

LOOP = "data/sources/footage/looplog-vertical.mp4"
REV = "data/sources/footage/reviewsdoc-vertical.mp4"
GRID = "data/sources/footage/editgrid-vertical.mp4"

# (source|None, req|reason)
MAP = [
    (LOOP, "系统日志本体在帧（BS-loop.log 终端=state+心跳台账实况·拍文「系统日志」字面直证·开业时点公司实况）"),
    (LOOP, "循环日志台账在帧（一切落库·每分钟轮询审计的运行实况·同源多用注记）"),
    (None, "规矩宣示拍：上线状态判定无专属画面可证（账号面=台账非画面素材·探针证实日志无「未上线」字样），字卡即门牌"),
    (REV, "Station Reviews 台账表格在帧（证据材料列=来源审查留痕·「无来源不发布」的执行记录）"),
    (GRID, "剪辑验图帧网格在帧（本片同族章节帧=标题承诺的内容交付实物·自指注记）"),
    (GRID, "自产帧网格=AI 生成内容本体在帧；成片全帧由 renderer 常驻烧录 [AIGC·AI 生成内容] 标识=依法标识在位直证（自指素材·标识位随成片验图复核）"),
    (REV, "站审台账 verdict 行在帧（同一道门过站留痕=标题党/来源/脱敏审查执行面·同源多用注记）"),
    (LOOP, "循环日志健康对账读数在帧（Loop health 行=定期对表实况·「每周对表」节律直证·同源多用注记）"),
    (LOOP, "台账实况读数在帧（只记实测数字·愿景数字不进账·「不发愿景数字」的反面证据面·同源多用注记）"),
    (LOOP, "循环机制本体在运转（state+心跳台账=「这套机制本身」直证·同源多用注记）"),
    (REV, "门禁台账在帧（不过站不流转留痕=「门不过字不出」执行记录·同源多用注记）"),
    (None, "CTA 常规拍（完整实录指引·F-001 v15 b11 同位惯例·字卡收尾）"),
]

cards = j["cards"]
assert len(cards) == 12 and len(MAP) == 12
n_vis = 0
for i, (c, (src, req)) in enumerate(zip(cards, MAP)):
    if src:
        c["visual"] = {"source": src, "req": req}
        n_vis += 1
    else:
        c["visual"] = {"cards-only": True, "reason": req}

j["meta"]["visual_spec"] = "docs/footage-matching-spec.md"
j["meta"]["storyboard"] = ("BS-006 编辑诚实机制件：题材对位=台账/审计面——looplog（BS-loop.log 系统日志终端）×5"
                           "+reviewsdoc（Station Reviews 站审台账）×3+editgrid（本片自产章节帧网格）×2+cards-only×2；"
                           "对位 10/12=0.83·同源多用逐拍注记·素材探针先行定谳（probe-src-tile.png）")

with io.open(DST, "w", encoding="utf-8") as fh:
    json.dump(j, fh, ensure_ascii=False, indent=1)
print("visual_beats:", n_vis, "of", len(cards))
print("written ->", DST)
