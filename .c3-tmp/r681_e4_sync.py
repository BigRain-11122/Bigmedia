# -*- coding: utf-8 -*-
# R681: sync E4 same-round backfill (8.0) across ledger rows
import io

FIX = [
    ("docs/reviews/review-20260929-lc002-v1.md",
     u"（E4 参考·非拦截·在飞=轮间异步回填）",
     u"（E4 参考·非拦截·8.0 同轮回填=v1.1）"),
    ("docs/reviews/review-20260929-lc002-v1.md",
     u"——E4 受众参考在飞（落地即回填）",
     u"——E4 受众参考已测（8.0·同轮回填）"),
    ("output/renders/README.md",
     u"·E4 参考仪在飞轮间回填）→M4 完成态",
     u"·E4 参考仪同轮回填 8.0=拆条带持平〔LC-001 8.0 对照〕）→M4 完成态"),
    ("docs/reviews/station-reviews.md",
     u"+E4 参考仪（e4_call.py 脱壳 PID 16116 起飞·轮间异步回填=R180/R187/R512 先例）",
     u"+E4 参考仪（e4_call.py 脱壳 PID 16116·**同轮回填 8.0**〔会看完+点赞明说+转发条件式=拆条带持平·净本 expert-verdicts/20260929120236〕）"),
    ("docs/reviews/station-reviews.md",
     u"（E4 在飞轮间回填）；F-055 登记",
     u"（E4 同轮回填 8.0）；F-055 登记"),
    ("src/os/backlog.md",
     u"·E4 参考仪在飞轮间异步回填=R180/R187/R512 先例）→M4 完成态",
     u"·E4 参考仪同轮回填 8.0=拆条带持平〔LC-001 8.0 对照·旗①镇田之宝句=verbatim 卡锚不可改写·吸收位 M5 图文页语境层·最弱受众窄=M6 校准线〕）→M4 完成态"),
    ("output/finished.md",
     u"·E4 参考仪在飞轮间异步回填=R180/R187/R512 先例〕",
     u"·E4 参考仪同轮回填 8.0=拆条带持平〔LC-001 8.0 对照·会看完+点赞明说+转发条件式·旗①镇田之宝句=MC-003 语境门槛族·吸收位 M5 图文页〕〕"),
    ("data/sources/lc002/README.md",
     u"·E4 参考仪在飞轮间异步回填=R180/R187/R512 先例）",
     u"·E4 参考仪同轮回填 8.0=拆条带持平〔会看完+点赞明说+转发条件式·净本 expert-verdicts/20260929120236〕）"),
]

for path, old, new in FIX:
    t = io.open(path, encoding="utf-8").read()
    if old in t:
        t = t.replace(old, new, 1)
        io.open(path, "w", encoding="utf-8").write(t)
        print("OK", path, old[:20])
    else:
        print("MISS", path, old[:20])
