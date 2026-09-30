# -*- coding: utf-8 -*-
# R761: archive E4 verdict netcopy (verbatim from e4-result.json) + append expert-calls row
import io, json

d = json.load(io.open(r".bs007-tmp/e4-result.json", encoding="utf-8"))
verdict = d["verdict"]
ts = d["ts"]  # 2026-09-30 17:34:31 (call start; landed 17:39:26)

hdr = (
    "# E4 直觉观众 · 参考仪判词（非拦截席）· BS-007《三颗心脏》稿集件2\n\n"
    "> 调用=e4_call.py 脱壳（qwen2.5:14b·UTF-8 stdin 管道·ANSI/盲文清洗·1500s 窗）·材料=.bs007-tmp/voiceover.txt（口播全文+画面/声线语境头）。\n"
    "> 起飞 17:34:31 · 落地 17:39:26（≈5min 满载机面慢落·R743 4.5min 同型带）·exit=DONE。\n"
    "> 读数=**7.0**（会看完明说+点赞可能式+不转发=三意愿一明一条件·机制哲学件受众窄位带）。\n\n---\n\n"
)
io.open(r"docs/reviews/expert-verdicts/20260930-173431-E4-audience.md", "w", encoding="utf-8").write(hdr + verdict + "\n")

row = (
    "| 2026-09-30 17:34 | E4-audience | E4 直觉观众（参考仪·非拦截席） | C:\\Users\\sjs20\\Desktop\\FluxGroup\\media\\BigStream\\.bs007-tmp\\voiceover.txt | 1 | "
    "full text=expert-verdicts/20260930-173431-E4-audience.md / **7.0 三意愿一明一条件**（会看完明说+点赞可能式+不转发=机制哲学件受众窄位带如实注〔LC-007/009/012/013/014/017 同位族〕·「创意独特·现代科技×公司管理类比」正面定性·旗①=b10「电脑空闲才干活，无人值守，但不无礼」被旗空洞套话扣 2=verbatim 卡锚〔无人值守=OS 循环空闲窗实况·不无礼=留窗收尾缓释设计·E4 盲评面看不到证据链〕·MC-003 语境门槛族 wink 位变体·吸收位=M5 图文页语境+系列语境·最弱=内容的实用性和普及性〔57s 比喻密度接收难度=机制哲学件固有·M6 校准位〕） |\n"
)
with io.open(r"docs/reviews/expert-calls.md", "a", encoding="utf-8") as f:
    f.write(row)
print("E4 ARCHIVED + CALL ROW APPENDED")
