# -*- coding: utf-8 -*-
# R632 verify (digit-expectation checklist per R615/R618 law; every number hand-updated per round)
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ok = []
def chk(name, cond):
    ok.append((name, bool(cond)))

st = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
chk("TICK==632", st["tick"] == 632)
chk("task R632:", st["task"].startswith(u"R632:"))
chk("log tail R632:", u" R632: " in st["log"][-1])
chk("focus next R633:", st["focus"].startswith(u"R633:"))
chk("focus baseline r632_lednew5", u"r632_lednew5.txt" in st["focus"])
chk("LOG_COUNT>=643", len(st["log"]) >= 643)
chk("ts fresh today", st["ts"].startswith("2026-09-28 "))

xp = json.load(io.open(os.path.join(ROOT, "docs", "status-export.json"), encoding="utf-8"))
chk("export_ts fresh", xp["export_ts"].startswith("2026-09-28T09:5"))
chk("OS row tick 632", any(r[0] == u"OS 循环" and u"tick 632" in r[1] for r in xp["outs"]))
chk("results[0]=632", xp["results"][0][0] == u"632")

sr = io.open(os.path.join(ROOT, "docs", "reviews", "station-reviews.md"), encoding="utf-8").read()
chk("station R632 row", u"R631 起飞 R632 落判" in sr)

ev = os.path.join(ROOT, "docs", "reviews", "expert-verdicts")
v928 = [f for f in os.listdir(ev) if f.startswith("20260928")]
chk("VERDICTS_0928_COUNT==3", len(v928) == 3)
chk("verdict 093647 present", "20260928-093647-E4-audience.md" in v928)

fin = io.open(os.path.join(ROOT, "output", "finished.md"), encoding="utf-8").read()
chk("F-053 backfill seg", u"E4 R632 回填毕" in fin and u"20260928-093647-E4-audience.md" in fin)

cards = io.open(os.path.join(ROOT, "data", "storylines", "cards", "README.md"), encoding="utf-8").read()
chk("cards v9 backfill seg", u"E4 R632 回填毕" in cards)

rv = io.open(os.path.join(ROOT, "docs", "reviews", "review-20260928-mcdigest-v9.md"), encoding="utf-8").read()
chk("review v1.1 E4 section", u"R632 回填毕" in rv and u"v1.1（R632·E4 参考仪回填追加制" in rv)

chk("ledger baseline file exists", os.path.exists(os.path.join(ROOT, ".c3-tmp", "r632_lednew5.txt")))

fails = [n for n, c in ok if not c]
with io.open(os.path.join(ROOT, ".c3-tmp", "r632_verify.txt"), "w", encoding="utf-8") as fh:
    for n, c in ok:
        fh.write(("PASS " if c else "FAIL ") + n + "\n")
    fh.write(("ALL_PASS" if not fails else "HAS_FAIL: " + ",".join(fails)) + "\n")
print("ALL_PASS" if not fails else "HAS_FAIL: " + ",".join(fails))
