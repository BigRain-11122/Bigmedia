# -*- coding: utf-8 -*-
# r631_verify.py -- R631 close-out verification (digit-expectation checklist law, R618/R619)
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
res = []
ok = True

def chk(name, cond, detail):
    global ok
    ok = ok and bool(cond)
    res.append("%s %s %s" % ("PASS" if cond else "FAIL", name, detail))

sp = os.path.join(ROOT, "src", "os", "state.json")
st = json.load(io.open(sp, encoding="utf-8"))
chk("VERIFY_R631", st["tick"] == 631, "tick=%s" % st["tick"])
chk("TS", st["ts"].startswith("2026-09-28 09:38"), "ts=%s" % st["ts"])
chk("TASK", st["task"].startswith("R631:") and len(st["task"]) <= 60, "task=%r len=%d" % (st["task"], len(st["task"])))
log_tail = st["log"][-1]
chk("LOG_TAIL", log_tail.startswith("2026-09-28 09:38") and " R631: " in log_tail, "tail head=%r" % log_tail[:40])
chk("LOG_COUNT", len(st["log"]) > 643, "log=%d" % len(st["log"]))
chk("FOCUS_R632", st["focus"].startswith("R632:") and "r631_lednew5" in st["focus"], "focus head=%r" % st["focus"][:24])
chk("STATE_PROD", st["production"] == "open", st["production"])

xp = json.load(io.open(os.path.join(ROOT, "docs", "status-export.json"), encoding="utf-8"))
chk("EXPORT_TS", xp["export_ts"].startswith("2026-09-28T09:38"), "export_ts=%s" % xp["export_ts"])
chk("EXPORT_R631", xp["results"][0][0] == u"631" and u"F-053" in xp["results"][0][1], "results[0] tick=%s" % xp["results"][0][0])

fin = io.open(os.path.join(ROOT, "output", "finished.md"), encoding="utf-8").read()
chk("FIN_F053", u"F-053 登记（R631）" in fin and u"自驱力生态令数字盘点" in fin, "F-053 row")
cr = io.open(os.path.join(ROOT, "data", "storylines", "cards", "README.md"), encoding="utf-8").read()
chk("CARDS_V9", u"MC-20260928-DIGEST-v9 登记（R631" in cr, "cards README v9 row")
sr = io.open(os.path.join(ROOT, "docs", "reviews", "station-reviews.md"), encoding="utf-8").read()
chk("STATION_R631", u"mc-digest-v9" in sr and u"R631" in sr, "station row")
bl = io.open(os.path.join(ROOT, "src", "os", "backlog.md"), encoding="utf-8").read()
chk("BACKLOG_R631", u"R631 claim+交付毕 2026-09-28" in bl, "backlog R631 delivered line")
chk("REVIEW_FILE", os.path.exists(os.path.join(ROOT, "docs", "reviews", "review-20260928-mcdigest-v9.md")), "review v9 exists")
chk("PNG", os.path.exists(os.path.join(ROOT, "data", "storylines", "cards", "MC-20260928-DIGEST-v9", "MC-20260928-DIGEST-v9.png")), "png exists")

out = "\n".join(res)
io.open(os.path.join(ROOT, ".c3-tmp", "r631_verify.txt"), "w", encoding="utf-8").write(out + "\n")
print(out if all(ord(c) < 128 for c in out) else ("ALL_PASS" if ok else "HAS_FAIL"))
