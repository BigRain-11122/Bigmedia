# -*- coding: utf-8 -*-
"""R287: append station-reviews row (UTF-8 channel, per r278_append precedent)."""
import io

ROW = (
u"| 2026-09-25 | **M0-M6 全链站审+M4.5 终审+E4 回填·MC-20260925-QUOTE-v4 静态卡系列量产按序领件第二件（R287 同轮·追加制）** "
u"| MC-20260925-QUOTE-v4.png《城市语录 004·求新轴》（`docs/reviews/review-20260925-mc004-v1.md`） "
u"| hit-chain §8 站审 M0-M6 判据行全链留痕（M0 四维分 7/8=A 档·cards.json `meta.hit_chain_m0` 数据件自证·系列量产按序领件=六轴表格序第三条 L140）"
u"+七席 6×9.0+E7 N/A（MC-001 维度定标复用）+E4-audience（qwen2.5:14b 修正材料重跑→20:28:46 落地·热载快落·dept-review §6 双态制·盲评材料律合规零嵌审计史） "
u"| **8.0 会停下来看+倾向保存+可能转发（三意愿齐明说系列首件·F-016 登记·PASS 放行候选）** "
u"| **M1 verbatim 一字误写轮内拦下三重闭环**（初稿「更大」≠CODEX L140 原句「越大」·E2 对照原句当场定谳→修正重渲+复验〔转写先行无预期文本防偏〕+E4 首跑材料污染判无效重跑·首跑判词存档 `MC-20260925-QUOTE-v4-tmp/e4-result-a1-invalid.txt`=R184 audit2 无效审计同型处置·操作红如实入账零登记前漂移）；"
u"**零扣分旗**（Q2 明说「并没有一眼假或空洞套话的地方……没有必要扣分」=信任面五连·引文正面定性「寓意深刻·能引发读者的深思」）；"
u"最弱=来源行专业度（CODEX §八 对普通读者显专业·纪实律合规行不可删·吸收位=M5 图文页语境+系列语境）；验图复验 PASS=转写逐字对照原句零缺无损·全角标点齐全 "
u"| 评审单+净本 `expert-verdicts/20260925-202846-E4-audience.md`+cards/README 台账行 |\n"
)

PATH = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\docs\reviews\station-reviews.md"
with io.open(PATH, "a", encoding="utf-8") as f:
    f.write(ROW)
print("APPENDED-OK")
