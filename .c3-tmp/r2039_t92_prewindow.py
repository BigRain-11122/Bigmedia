# -*- coding: utf-8 -*-
# R2039 tech#92 pre-window verify: score/structure receipt resume after worker restart 08:16:37
# Precheck for the 10-13 08:00 re-judge window (R2038 next-step pointer).
# Channel: raw psql (R1957 SOP; no SQL text functions on body_text).
import json
import os
import subprocess

PSQL = r"data\assets\aihot-poc\pg17\pgsql\bin\psql.exe"
ENV = {**os.environ, "PGPASSWORD": "", "PGCLIENTENCODING": "UTF8"}
RESTART = "2026-10-12 08:16:37"


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
    out = {"probe": "r2039_t92_prewindow", "restart_anchor": RESTART}

    # 1) pgboss queue shape per name/state
    rows = q("SELECT name, state, count(*) FROM pgboss.job GROUP BY name, state ORDER BY name, state")
    queues = {}
    for name, state, cnt in rows:
        queues.setdefault(name, {})[state] = cnt
    out["pgboss_queues"] = queues

    # 2) receipts since restart: per model+status (resume-flow core check)
    rows = q("SELECT model, status, count(*) FROM receipts WHERE created_at >= '" + RESTART +
             "' GROUP BY model, status ORDER BY model, status")
    out["receipts_since_restart"] = rows

    # 3) score/structure flow detail with first/last ts
    rows = q("SELECT model, status, min(created_at), max(created_at), count(*) FROM receipts "
             "WHERE created_at >= '" + RESTART + "' AND (model LIKE 'selection-score%' "
             "OR model LIKE 'structure%' OR model LIKE 'prefilter%') GROUP BY model, status ORDER BY model")
    out["score_struct_flow"] = rows

    # 4) receipts freshness (worker liveness proxy)
    rows = q("SELECT max(created_at) FROM receipts")
    out["receipts_max_ts"] = rows[0][0]

    # 5) stale active slots created before restart (R2038: 6 old stale pending maintenance)
    rows = q("SELECT count(*) FROM pgboss.job WHERE state='active' AND created_on < '" + RESTART + "'")
    out["stale_active_pre_restart"] = rows[0][0]

    # 6) non-backfill >=60 accumulation (re-judge window reading)
    rows = q("SELECT count(*), max(p.score) FROM publications p JOIN articles a ON a.id=p.article_id "
             "WHERE p.score IS NOT NULL AND p.backfill=false AND p.score >= 60")
    out["nonbf_ge60"] = rows[0]

    rows = q("SELECT count(*) FROM publications p JOIN articles a ON a.id=p.article_id "
             "WHERE p.score IS NOT NULL AND p.backfill=false")
    out["nonbf_scored_total"] = rows[0][0]

    # 7) articles processing mix
    rows = q("SELECT processing_state, count(*) FROM articles GROUP BY processing_state")
    out["articles_states"] = rows

    # 8) per-source non-backfill ceiling band
    rows = q("SELECT s.id, count(*), max(p.score) FROM publications p JOIN articles a ON a.id=p.article_id "
             "JOIN sources s ON s.id=a.source_id WHERE p.score IS NOT NULL AND p.backfill=false "
             "GROUP BY s.id ORDER BY 3 DESC NULLS LAST LIMIT 8")
    out["src_score_ceiling"] = rows

    # 9) fetch rhythm (R2037 open issue: interval 180min not persisted)
    rows = q("SELECT max(finished_at), count(*) FROM fetch_runs WHERE finished_at >= '2026-10-12 06:00'")
    out["fetch_since_0600"] = rows[0]

    with open(r".c3-tmp/r2039_t92_readout.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
