# -*- coding: utf-8 -*-
# R970 E4 same-round backfill (landed 10:34:00 while round still open; R753/R872 correction
# precedent: registration pieces updated to real verdict, no pre-written score kept).
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, "data", "storylines", "cards", "MC-20261002-DAILY-v1-tmp")

r = json.load(io.open(os.path.join(TMP, "e4-result.json"), encoding="utf-8"))
assert r.get("verdict") and "TIMEOUT" not in r["verdict"], "E4 not landed: %r" % r.get("verdict")
ts = r["ts"]

E4ROW = (u"| E4 | 受众参考仪 | **8.0（%s 同轮回填·脱壳快落）** | 大概率会停下来看+打 8 分明说（国庆氛围+灯笼主题+"
         u"「AI 生成」好奇面吸引·节日气氛×文化内涵双正面）；三意愿=会停明说+保存/转发未明说如实（R293 型）；"
         u"旗①=「直播间都说」表述略显泛泛扣 1〔建议改写为观众留言体=池句 verbatim 不可改写·纪实律来源律·台词池行零改字；"
         u"E4 误读面=原句语境为做灯笼的师傅开直播间·非观众留言·吸收位=M5 图文页语境〔MC-003 语境门槛族变体〕〕；"
         u"最弱=互动参与感〔静态卡载体固有·M6 校准位〕·QUOTE 带 7.0-8.0 带内持平（F-013~F-018 同族） |" % ts)

p = os.path.join(ROOT, "docs", "reviews", "review-20261002-mcdaily-v1.md")
doc = io.open(p, encoding="utf-8").read()
old_row = u"| E4 | 受众参考仪 | 在飞 | 脱壳异步（1500s 窗·e4-result.json 轮间落地=追加制回填 R870→R871 先例·非拦截席） |"
assert old_row in doc, "E4 row anchor not found"
doc = doc.replace(old_row, E4ROW)
doc = doc.replace(u"（E4 回填=下轮追加制·假绿灯律：本单不预写 E4 分）",
                  u"（E4 同轮回填 8.0=%s 落判·脱壳快落·假绿灯律：本单未预写 E4 分·落判即校正）" % ts)
io.open(p, "w", encoding="utf-8").write(doc)

# finished.md append-only backfill line (追加制 R718 precedent)
with io.open(os.path.join(ROOT, "output", "finished.md"), "a", encoding="utf-8") as f:
    f.write(u"F-086 E4 回填（R970 同轮·追加制）——E4 参考仪 %s 落判 **8.0**（大概率会停下来看+打 8 分明说·"
            u"国庆氛围×灯笼主题×AI 生成好奇面三正面·三意愿=会停明说+保存/转发未明说如实〔R293 型〕·"
            u"旗①=「直播间都说」泛泛扣 1=池句 verbatim 不可改写·E4 误读面=原句为灯笼师傅开直播间非观众留言·"
            u"吸收位=M5 图文页语境·最弱=互动参与感〔静态载体固有·M6〕·净本 MC-20261002-DAILY-v1-tmp/e4-result.json）——"
            u"M4.5 七席终态=6×9.0+E4 8.0+E7 N/A 全 ≥8.0 PASS 维持（放行候选不变·发布锁不变）。\n" % ts)

# state.json: amend LOG E4 segment in place (honest same-round correction, R872 four-piece correction precedent)
sp = os.path.join(ROOT, "src", "os", "state.json")
st = json.load(io.open(sp, encoding="utf-8"))
last = st["log"][-1]
old_seg = u"+E4 参考仪**脱壳异步在飞**（PID 已发·1500s 窗·下轮追加制回填 R870→R871 先例·评审单不预写 E4 分=假绿灯律）"
new_seg = (u"+E4 参考仪**同轮回填 8.0**（%s 落判·脱壳快落·大概率会停+打 8 分明说·旗①=「直播间都说」泛泛扣 1="
           u"池句 verbatim 不可改写·最弱=互动感〔M6〕·QUOTE 带内持平·净本 e4-result.json·评审单不预写分=落判即校正"
           u"〔R872 四件校正先例〕）" % ts)
assert old_seg in last, "state LOG E4 segment anchor not found"
st["log"][-1] = last.replace(old_seg, new_seg)
st["log"][-1] = st["log"][-1].replace(u"⑥例行件：", u"⑥E4 同轮回填毕=七席终态 6×9.0+E4 8.0+E7 N/A 全 ≥8.0；例行件：")
json.dump(st, io.open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# export: outs line amendment
ep = os.path.join(ROOT, "docs", "status-export.json")
ex = json.load(io.open(ep, encoding="utf-8"))
ex["outs"][0][1] = ex["outs"][0][1].replace(u"E4 异步在飞下轮回填）", u"E4 同轮回填 8.0·七席全 ≥8.0）")
json.dump(ex, io.open(ep, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("E4 same-round backfill done: 8.0 @", ts)
