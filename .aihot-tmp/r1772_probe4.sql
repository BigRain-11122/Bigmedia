SELECT 'astate|' || processing_state || '|' || count(*) FROM articles GROUP BY processing_state ORDER BY 1;
SELECT 'rcpt_err|' || status || '|' || count(*) FROM receipt_attempts WHERE started_at > '2026-10-08 21:48:00' AND status <> 'received' GROUP BY status ORDER BY 1;
SELECT 'reports_cnt|' || count(*) FROM reports;
SELECT 'report_recent|' || id || '|' || kind || '|' || window_start || '|' || window_end || '|' || created_at FROM reports ORDER BY created_at DESC LIMIT 5;
SELECT 'jobs_recent|' || job || '|' || status || '|' || started_at || '|' || coalesce(error,'') FROM job_runs WHERE started_at > '2026-10-08 21:40:00' ORDER BY started_at DESC LIMIT 12;
