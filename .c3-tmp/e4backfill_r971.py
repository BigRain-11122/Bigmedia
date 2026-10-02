# -*- coding: utf-8 -*-
# R971 E4 same-round backfill (landed 10:45:52 while round still open; R970/R753/R872
# correction precedent: registration pieces updated to real verdict, no pre-written score).
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, "data", "storylines", "cards", "MC-20261002-DAILY-v2-tmp")

r = json.load(io.open(os.path.join(TMP, "e4-result.json"), encoding="utf-8"))
assert r.get("verdict") and "TIMEOUT" not in r["verdict"], "E4 not landed: %r" % r.get("verdict")
ts = r["ts"]

E4ROW = (u"| E4 | 受众参考仪 | **7.0（%s 同轮回填·build 早发热载快落）** | 会停下来看明说+打 7 分（节日氛围×"
         u"怀旧情怀×虚构城市设定新颖性三正面）；三意愿=会停明说+保存/转发未明说如实（R293 型）；"
         u"旗①=底部来源行「引文取自硅基城市台词池（虚构城市档案）」正式官方、缺互动引导元素扣 1"
         u"〔三重标注合规红线行不可删改·吸收位=M5 图文页语境+系列语境〕；最弱=互动性与具体性〔静态卡载体固有·"
         u"M6 校准位〕·QUOTE/DAILY 带 7.0-8.0 带内下缘如实（DAILY-v1 8.0 对照·REACT v1/v5 7.0 同位）·"
         u"非拦截席=MC-001 定标口径 |" % ts)

p = os.path.join(ROOT, "docs", "reviews", "review-20261002-mcdaily-v2.md")
doc = io.open(p, encoding="utf-8").read()
old_row = u"| E4 | 受众参考仪 | 在飞 | 脱壳异步（1500s 窗·e4-result.json 轮间落地=追加制回填 R870→R871 先例·非拦截席） |"
assert old_row in doc, "E4 row anchor not found"
doc = doc.replace(old_row, E4ROW)
doc = doc.replace(u"（E4 回填=同轮或下轮追加制·假绿灯律：本单不预写 E4 分）",
                  u"（E4 同轮回填 7.0=%s 落判·脱壳快落·假绿灯律：本单未预写 E4 分·落判即校正）" % ts)
io.open(p, "w", encoding="utf-8").write(doc)

# finished.md append-only backfill line (追加制 R718/R970 precedent)
with io.open(os.path.join(ROOT, "output", "finished.md"), "a", encoding="utf-8") as f:
    f.write(u"F-087 E4 回填（R971 同轮·追加制）——E4 参考仪 %s 落判 **7.0**（会停下来看明说+打 7 分·"
            u"节日氛围×怀旧情怀×虚构城市设定新颖性三正面·三意愿=会停明说+保存/转发未明说如实〔R293 型〕·"
            u"旗①=底部来源行「引文取自硅基城市台词池（虚构城市档案）」正式官方缺互动引导扣 1=三重标注合规行"
            u"不可删改·吸收位=M5 图文页语境+系列语境·最弱=互动性与具体性〔静态卡载体固有·M6〕·"
            u"QUOTE/DAILY 带 7.0-8.0 带内下缘如实〔DAILY-v1 8.0 对照〕·净本 MC-20261002-DAILY-v2-tmp/e4-result.json）——"
            u"M4.5 七席终态=6×9.0+E4 7.0+E7 N/A（E4 参考仪非拦截席=MC-001 定标口径·REACT v1/v5 7.0 F 登记先例）"
            u"PASS 维持（放行候选不变·发布锁不变）。\n" % ts)

# state.json: amend LOG E4 segment in place (honest same-round correction, R872 precedent)
sp = os.path.join(ROOT, "src", "os", "state.json")
st = json.load(io.open(sp, encoding="utf-8"))
last = st["log"][-1]
old_seg = u"+E4 参考仪脱壳异步起飞（build 时点早发·1500s 窗·同轮回填或下轮追加制 R870→R871 先例·非拦截席）"
new_seg = (u"+E4 参考仪**同轮回填 7.0**（%s 落判·build 早发热载快落·会停明说+打 7 分·节日氛围×怀旧×虚构设定三正面·"
           u"三意愿保存/转发未明说如实·旗①=底部来源行正式官方扣 1=合规行不可改·吸收位=M5+系列语境·"
           u"最弱=互动性〔M6〕·带内下缘 v1 8.0 对照·非拦截席=MC-001 定标·净本 e4-result.json·"
           u"评审单不预写分=落判即校正〔R872 四件校正先例〕）" % ts)
assert old_seg in last, "state LOG E4 segment anchor not found"
st["log"][-1] = last.replace(old_seg, new_seg)
st["log"][-1] = st["log"][-1].replace(u"⑥例行件：", u"⑥E4 同轮回填毕=七席终态 6×9.0+E4 7.0+E7 N/A（E4 参考仪非拦截席·带内下缘如实）；例行件：")
st["log"][-1] = st["log"][-1].replace(u"tokens:local=1（E4 qwen2.5:14b 本轮起飞=同轮或落地轮记账", u"tokens:local=1（E4 qwen2.5:14b 本轮起飞+同轮落地记账")
st["ts"] = ts
st["task"] = u"生产轮·E30 DAILY 续件 v2=F-087 登记+E4 同轮回填 7.0（台词池怀旧/festival/0 verbatim"
json.dump(st, io.open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# export: outs line amendment
ep = os.path.join(ROOT, "docs", "status-export.json")
ex = json.load(io.open(ep, encoding="utf-8"))
ex["outs"][0][1] = ex["outs"][0][1].replace(u"验图 5/5·E4 异步在飞）", u"验图 5/5·E4 同轮回填 7.0〔带内下缘·非拦截席〕）")
ex["export_ts"] = ts
json.dump(ex, io.open(ep, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("E4 same-round backfill done: 7.0 @", ts)
