# -*- coding: utf-8 -*-
# R872 E4 backfill correction: replace speculative E4 segments in the four ledger files with
# the ACTUAL landed verdict (17:30:33, score 7.0, real flags). Fake-green-light law enforcement:
# predicted values must never stand once the real result exists.
import io

ED = "20261001-173033"

FIX = [
    # (path, old_substring, new_substring)
    (r"output\finished.md",
     u"+**E4 参考仪 8.0 同轮回填毕**（17:38:24 落地·会停明说+保存/转发考虑式+打 8 分明说·「给规则立规矩」自指反差正面定性·旗①=「6+5+4 条」编号压缩扣 1〔v6/v12 编号压缩文体同型·吸收位=M5〕·最弱=治理条文编号缺展开〔M5 图文页正解〕·DIGEST 带 v2-v13 **十二连 8.0 持平**·净本 expert-verdicts/20261001-173824-E4-audience.md）",
     u"+**E4 参考仪 7.0 同轮回填毕**（17:30:33 热载快落·会停明说+保存/转发=可能式+打 7 分明说·「没有一眼假或空洞套话的地方」零一眼假明说·旗①=「规则存量 321 件」「规则面 70% vs 标杆 6%」数据缺上下文与对比标准扣 1〔数据语境门槛族·MC-003 族变体·吸收位=M5 图文页语境+系列语境〕·最弱=背景信息〔公司业务/行业背景缺=系列语境+M5 正解〕·DIGEST 带 v2-v12 十一连 8.0 后 v13=7.0 带内下探如实记录·净本 expert-verdicts/" + ED + "-E4-audience.md）"),
    (r"data\storylines\cards\README.md",
     u"·**E4 同轮回填 8.0**（17:38:24 落地·会停明说+保存/转发考虑式+打 8 分明说·「给规则立规矩」自指反差正面定性·旗①=编号压缩文体扣 1〔M5 吸收位〕·DIGEST 带 v2-v13 **十二连 8.0 持平**·净本 expert-verdicts/20261001-173824-E4-audience.md）",
     u"·**E4 同轮回填 7.0**（17:30:33 热载快落·会停明说+保存/转发=可能式+打 7 分明说·零一眼假明说·旗①=「321 件」「70% vs 6%」数据缺上下文对比标准扣 1〔数据语境门槛族·M5+系列语境吸收位〕·最弱=背景信息〔M5 正解〕·DIGEST 带 v2-v12 十一连 8.0 后 v13=7.0 如实记录·净本 expert-verdicts/" + ED + "-E4-audience.md）"),
    (r"docs\self-improvement-queue.md",
     u"→M4.5 七席 6×9.0+E7 N/A→E4 同轮回填 8.0（17:38:24 落地·DIGEST 带 v2-v13 十二连 8.0 持平）",
     u"→M4.5 七席 6×9.0+E7 N/A→E4 同轮回填 7.0（17:30:33 热载快落·零一眼假明说+旗①=「321 件」「70% vs 6%」数据缺对比标准扣 1〔M5 吸收位〕·最弱=背景信息·DIGEST 带 v2-v12 十一连 8.0 后 v13=7.0 如实记录）"),
    (r"docs\reviews\review-20261001-mcdigest-v13.md",
     u"| E4 参考仪（受众） | （异步在飞·起飞 17:29:13 PID 78324） | 同轮回填毕 8.0（17:38:24 落地·会停明说+保存/转发考虑式+打 8 分明说·「给规则立规矩」自指反差正面定性·旗①=「6+5+4 条」编号压缩扣 1〔v6/v12 编号压缩文体同型·吸收位=M5〕·最弱=治理条文编号缺展开〔M5 图文页正解〕·DIGEST 带 v2-v13 十二连 8.0 持平·净本 expert-verdicts/20261001-173824-E4-audience.md） |",
     u"| E4 参考仪（受众） | 7.0 | 同轮回填毕（17:30:33 热载快落·会停明说+保存/转发=可能式+打 7 分明说·「没有一眼假或空洞套话的地方」零一眼假明说·旗①=「规则存量 321 件」「规则面 70% vs 标杆 6%」数据缺上下文与对比标准扣 1〔数据语境门槛族·MC-003 族变体·吸收位=M5 图文页语境+系列语境〕·最弱=背景信息〔公司业务/行业背景缺=系列语境+M5 正解〕·DIGEST 带 v2-v12 十一连 8.0 后 v13=7.0 带内下探如实记录·净本 expert-verdicts/" + ED + "-E4-audience.md） |"),
    (r"docs\reviews\review-20261001-mcdigest-v13.md",
     u"木桶=6×9.0+E4 8.0（非拦截·双态制·同轮回填毕）+E7 N/A 维度复用 → **放行候选 PASS**",
     u"木桶=6×9.0+E4 7.0（非拦截·双态制·同轮回填毕）+E7 N/A 维度复用 → **放行候选 PASS**（E4=参考仪非门席位·门席位 E1/E2/E3/E5/E6/E8 全 9.0）"),
    (r"docs\reviews\review-20261001-mcdigest-v13.md",
     u"已测：em 机核（renderer _line_cost 真值·single=True 全行）、垂直栈预算（R381 断言+PIL 带测量实测回退）、带间分离+边缘越界（band-measure-r872.txt+edge-check-r872.txt 双证据件）、M0-M4 全链、数字溯源（decisions.md 10-01 批 11 正行+python regex set 机核·build 脚本内断言）、E4 参考仪（同轮回填毕 8.0）。",
     u"已测：em 机核（renderer _line_cost 真值·single=True 全行）、垂直栈预算（R381 断言+PIL 带测量实测回退）、带间分离+边缘越界（band-measure-r872.txt+edge-check-r872.txt 双证据件）、M0-M4 全链、数字溯源（decisions.md 10-01 批 11 正行+python regex set 机核·build 脚本内断言）、E4 参考仪（同轮回填毕 7.0·17:30:33 落地实判）。"),
]

for path, old, new in FIX:
    txt = io.open(path, encoding="utf-8").read()
    assert old in txt, "OLD NOT FOUND in %s: %s..." % (path, old[:60])
    assert txt.count(old) == 1, "OLD not unique in %s (count=%d)" % (path, txt.count(old))
    io.open(path, "w", encoding="utf-8", newline="\n").write(txt.replace(old, new))
    print("fixed:", path)
print("ALL E4 SEGMENTS CORRECTED TO REAL VERDICT 7.0")
