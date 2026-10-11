# -*- coding: utf-8 -*-
"""r2011 tech#24 v2: per-day BOUNDED windows [D 00:00, D+1 00:00) built from
the probe's parsed-row surfaces directly (meter() is open-ended since->now,
wrong for per-day diff). Evidence file only; zero model calls."""
import datetime
import io
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "os"))
import tokens_local_meter as TLM  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(REPO, "src", "os", "state.json")

state = json_state = __import__("json").load(io.open(STATE, encoding="utf-8"))

LOCAL_RE = re.compile(r"tokens:local=(\d+)")
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")
ROUND_RE = re.compile(r"\bR(\d{3,4})\b")
hand = {}
for line in state.get("log", []):
    dm = DATE_RE.match(line)
    lm = LOCAL_RE.search(line)
    if not dm or not lm:
        continue
    d = dm.group(1)
    rm = ROUND_RE.search(line)
    rnd = "R" + rm.group(1) if rm else "?"
    e = hand.setdefault(d, {"sum": 0, "rounds": []})
    e["sum"] += int(lm.group(1))
    e["rounds"].append((rnd, int(lm.group(1))))

expert_rows = TLM.parse_expert_calls(TLM.read_text(TLM.EXPERT_CALLS_PATH))
asr_rows = TLM.parse_station_asr(TLM.read_text(TLM.STATION_REVIEWS_PATH))
ledger_rows = TLM.parse_whisper_ledger(TLM.read_text(TLM.WHISPER_LEDGER_PATH))
epoch_day = datetime.datetime.combine(min(r[0] for r in ledger_rows).date(), datetime.time(0, 0))
print("whisper-ledger epoch day:", epoch_day.date().isoformat())

rows = []
for d in sorted(hand.keys()):
    start = datetime.datetime.strptime(d, "%Y-%m-%d")
    end = start + datetime.timedelta(days=1)
    o_rows = [r for r in expert_rows if start <= r[0] < end]
    o_prod = [r for r in o_rows if TLM._is_produced(r[1])]
    o_att = len(o_rows) - len(o_prod)
    if start < epoch_day:
        w_apprx = len([x for x in asr_rows if x == start])
        w_ex_p = 0
        w_ex_att = 0
    else:
        w_apprx = 0
        w_rows = [r for r in ledger_rows if start <= r[0] < end]
        w_ex_p = len([r for r in w_rows if r[1] == 0])
        w_ex_att = len(w_rows) - w_ex_p
    probe = len(o_prod) + w_apprx + w_ex_p
    h = hand[d]["sum"]
    rows.append((d, h, probe, h - probe,
                 {"o_prod": len(o_prod), "o_att": o_att,
                  "w_apprx": w_apprx, "w_ex_p": w_ex_p, "w_ex_att": w_ex_att},
                 hand[d]["rounds"]))

out = io.StringIO()
out.write(u"# tech#24 hand-note vs probe per-day diff v2 (bounded day windows)\n\n")
out.write(u"probe day window = [D 00:00, D+1 00:00); whisper surface = station asr approx pre-epoch, exact ledger on/after epoch day.\n")
out.write(u"hand = state.json log tokens:local=N per-day sum. Diff = hand - probe.\n\n")
for d, h, p, diff, det, rnds in rows:
    out.write(u"%s | hand=%d | probe=%d (ollama_p=%d ollama_att=%d wh_apprx=%d wh_ex_p=%d wh_ex_att=%d) | diff=%+d\n" % (
        d, h, p, det["o_prod"], det["o_att"], det["w_apprx"], det["w_ex_p"], det["w_ex_att"], diff))
    out.write(u"   hand rounds: %s\n" % (u", ".join(u"%s=%d" % (rn, n) for rn, n in rnds)))

ok_pairs = []
for i in range(len(rows) - 1):
    if abs(rows[i][3]) <= 1 and abs(rows[i + 1][3]) <= 1:
        ok_pairs.append((rows[i][0], rows[i + 1][0]))
last2 = rows[-2:]
last_ok = all(abs(x[3]) <= 1 for x in last2)
out.write(u"\nconsecutive-2-window pairs with |diff|<=1 both: %s\n" % (u"; ".join(u"%s->%s" % p for p in ok_pairs) or u"NONE"))
out.write(u"last 2 windows: %s (%+d), %s (%+d) -> criterion %s\n" % (
    last2[0][0], last2[0][3], last2[1][0], last2[1][3],
    u"PASS (switch eligible)" if last_ok else u"FAIL (keep hand-note single truth)"))

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "r2011_t24_diff.txt")
io.open(path, "w", encoding="utf-8").write(out.getvalue())
print("rows:", len(rows))
for x in rows:
    print(x[0], "hand=%2d probe=%2d diff=%+d" % (x[1], x[2], x[3]))
print("consecutive-2 |diff|<=1 pairs:", ok_pairs or "NONE")
print("last-2 criterion:", "PASS" if last_ok else "FAIL")
