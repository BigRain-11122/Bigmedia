SELECT 'jobs_distinct|' || job || '|cnt=' || count(*) FROM job_runs WHERE started_at > '2026-10-08 21:48:00' GROUP BY job ORDER BY 1;
SELECT 'jdetail|' || left(detail::text, 800) FROM job_runs WHERE job = 'reports.compose' AND started_at > '2026-10-08 21:50:00' ORDER BY started_at DESC LIMIT 1;
