# -*- coding: utf-8 -*-
"""R893: append delivery note to backlog item 86 (data-carrier for Chinese text)."""
import io

p = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\backlog.md"
t = io.open(p, encoding="utf-8").read()
anchor = "——ch1/ch2 v4 深采毕·c 腿供给面定谳=新章 ch6+/新锚卡 C-00030+（皆 supply-gated·r807_scan 复核 C-00030 present: False）；a 腿二批（台词池 469 候选余量）随轮领]"
note = "   **[R893 claim+交付毕 2026-10-01：a 腿二批——台词池扩充批二 +20 条入志（`city-spirit.md` v1.2·精神条 44→64）——R892 收口指针「#86 a 腿二批（台词池 469 候选余量·R633 注指针）」兑现·当轮闭环：①探针先行=r893_pool.py 现行 pools.json 全量走查（TOTAL_LINES 1440 与 R633 基线一致=池未扩容）+排除已采 #1-44 与 culture/humanities/residents 三志在册面→453 净候选（R633 基线 469−批一 18−跨志扣减）；②谚语级精选 20 条（#45-64·六轴各 3+像素灵 2·**节日/令件场景首采**=批一未触两桶补全场景面·池级署名+场景标注·尾句规范化沿批一制）；③机核 20/20 PASS=r893_verify.py 逐条对 pools.json verbatim+对 #1-44 零重+三志在册面零重（r893_verify.txt 证据件·轴面 7 位·场景面 9 位含节日/令件）；④d 腿随批并落=codex README §1 状态行 v1.2+§2 计数台账批 10 行+变更记录行；台词池供给面定谳=1440 行两轮筛毕（批一 18+批二 20=38 条谚语级在册·池级署名），下批 supply-gated 待 BigLife 池扩容（pools.json TOTAL_LINES 增量触发）——**#86 a 腿二批毕·#86 常设行维持开板**（c 腿供给面 supply-gated 同前·b 腿锚池在册毕同前）]**"
assert anchor in t, "anchor missing"
assert "R893 claim" not in t, "note already present"
t = t.replace(anchor, anchor + "\n" + note, 1)
io.open(p, "w", encoding="utf-8").write(t)
print("backlog note appended")
