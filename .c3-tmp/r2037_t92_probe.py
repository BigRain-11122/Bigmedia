# -*- coding: utf-8 -*-
# R2037 tech#92 authoritative window read (10-12 08:00 production window).
# Pre-registered judgment (R1952 -> R1953 anchor-injection -> R1956 probe):
#   PASS = zhihu-hot head pieces >=3 with production score >=60 in this window
#          -> text-leg (anchor-injection) closes tech#92.
#   FAIL = threshold-layering fallback leg (city-source T1 60->55) per pre-registration.
# Channel: raw psql, zero SQL text functions on body_text (R1956 v3 / R1957 SOP).
# Also carries #112 light-read: processing states, failed pool, fetch rhythm.
import json
import os
import subprocess

PSQL = r"data\assets\aihot-poc\pg17\pgsql\bin\psql.exe"
ENV = {**os.environ, "PGPASSWORD": "", "PGCLIENTENCODING": "UTF8"}
CITY_SOURCES = ["json-zhihu-hot", "json-bilibili-tech", "json-bilibili-knowledge", "json-bilibili-popular"]


def q(sql):
    r = subprocess.run(
        [PSQL, "-h", "127.0.0.1", "-p", "55432", "-U", "aihot", "-d", "aihot", "-A", "-t",
         "-F", "\x01", "-c", sql],
        capture_output=True, env=ENV, timeout=60,
    )
    if r.returncode != 0:
        raise SystemExit("psql ERR: " + r.stderr.decode("utf-8", "replace").strip()[:300])
    return [ln.split("\x01") for ln in r.stdout.decode("utf-8", "replace").splitlines() if ln.strip()]


def main():
    out = {"ts_probe": "2026-10-12 08:0x", "gate": "tech#92 authoritative window 10-12 08:00"}

    # 1) today's daily report row (compose evidence + authoritative window bounds)
    rows = q("SELECT key, kind, window_start, window_end, generated_at, length(content::text) "
             "FROM reports WHERE kind='daily' ORDER BY key DESC LIMIT 2")
    out["recent_daily_reports"] = rows
    today = None
    for row in rows:
        if row[0] == "2026-10-12":
            today = row
    out["report_2026_10_12_present"] = bool(today)

    # selected/judged counts from today's report content if present
    if today:
        c = q("SELECT content FROM reports WHERE kind='daily' AND key='2026-10-12'")
        try:
            rep = json.loads(c[0][0])
            out["report_counts"] = {
                "judged": len(rep.get("judgedReports") or rep.get("judged") or []),
                "selected": len(rep.get("selectedReports") or rep.get("selected") or []),
                "sections": len(rep.get("sections") or []),
                "title": rep.get("title", ""),
            }
        except Exception as e:
            out["report_counts_error"] = repr(e)[:120]
        ws, we = today[2], today[3]
    else:
        ws, we = "2026-10-11 00:00:00+00", "2026-10-12 00:00:00+00"  # fallback bounds

    # 2) per-source scored band within the window (published_at inside report window)
    band = {}
    for s in CITY_SOURCES:
        w = q("SELECT count(*), max(score), "
              "sum(case when score>=60 then 1 else 0 end), "
              "sum(case when score>=55 then 1 else 0 end) "
              "FROM publications WHERE source_id='%s' AND backfill=false AND score IS NOT NULL "
              "AND published_at >= '%s' AND published_at < '%s'" % (s, ws, we))
        a = q("SELECT count(*), max(score), sum(case when score>=60 then 1 else 0 end) "
              "FROM publications WHERE source_id='%s' AND backfill=false AND score IS NOT NULL" % s)
        top = q("SELECT score, to_char(published_at,'MM-DD HH24:MI') "
                "FROM publications WHERE source_id='%s' AND backfill=false AND score IS NOT NULL "
                "ORDER BY score DESC LIMIT 8" % s)
        band[s] = {"window": w[0] if w else None, "all": a[0] if a else None,
                   "top8": [r[0] + "@" + (r[1] if len(r) > 1 else "?") for r in top]}
    out["scored_band"] = band

    # 3) judgment core: zhihu-hot in-window pieces >=60 (window + all-time views)
    zhihu_win = band["json-zhihu-hot"]["window"]
    zhihu_all = band["json-zhihu-hot"]["all"]
    ge60_win = int(zhihu_win[2]) if zhihu_win and zhihu_win[2] else 0
    ge60_all = int(zhihu_all[2]) if zhihu_all and zhihu_all[2] else 0
    out["judgment"] = {
        "criterion": "zhihu-hot head pieces >=3 with score>=60 in 10-12 08:00 window",
        "ge60_in_window": ge60_win,
        "ge60_all_time": ge60_all,
        "verdict_window": "PASS" if ge60_win >= 3 else "FAIL",
        "verdict_all_time": "PASS" if ge60_all >= 3 else "FAIL",
    }

    # 4) #112 light-read: processing states per city source + failed pool
    states = {}
    for s in CITY_SOURCES:
        st = q("SELECT processing_state, count(*) FROM articles WHERE source_id='%s' "
               "GROUP BY processing_state ORDER BY processing_state" % s)
        states[s] = {r[0]: r[1] for r in st}
    out["processing_states"] = states
    failed_pool = q("SELECT count(*) FROM articles WHERE processing_state='failed' "
                    "AND source_id IN (%s)" % ",".join("'%s'" % s for s in CITY_SOURCES))
    out["city_failed_pool"] = failed_pool[0][0] if failed_pool else None

    # 5) fetch rhythm (R1952 interval fix confirmation)
    src = q("SELECT id, interval_minutes, enabled, to_char(last_ok_at,'MM-DD HH24:MI'), "
            "to_char(next_fetch_at,'MM-DD HH24:MI') FROM sources WHERE id IN (%s) "
            "ORDER BY id" % ",".join("'%s'" % s for s in CITY_SOURCES))
    out["sources_rhythm"] = src

    with open(".c3-tmp/r2037_t92_readout.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
