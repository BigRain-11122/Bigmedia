SELECT 'acols|' || string_agg(column_name, ',' ORDER BY ordinal_position) FROM information_schema.columns WHERE table_name='articles';
SELECT 'reports_recent|' || id || '|' || created_at || '|' || coalesce(status,'') FROM reports ORDER BY created_at DESC LIMIT 3;
SELECT 'jobs_recent|' || name || '|' || status || '|' || started_at FROM job_runs ORDER BY started_at DESC LIMIT 8;
SELECT 'rcpt_14b|' || count(*) || '|err=' || count(*) FILTER (WHERE status <> 'received') FROM receipt_attempts WHERE started_at > '2026-10-08 21:48:00';
SELECT 'rcpt_model|' || model || '|' || count(*) FROM receipt_attempts WHERE started_at > '2026-10-08 21:48:00' GROUP BY model;
