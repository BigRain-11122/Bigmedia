SELECT 'astate|' || processing_state || '|' || count(*) FROM articles GROUP BY processing_state ORDER BY 2;
SELECT 'rcols|' || string_agg(column_name, ',' ORDER BY ordinal_position) FROM information_schema.columns WHERE table_name='reports';
SELECT 'jcols|' || string_agg(column_name, ',' ORDER BY ordinal_position) FROM information_schema.columns WHERE table_name='job_runs';
SELECT 'rcpt_err|' || status || '|' || count(*) FROM receipt_attempts WHERE started_at > '2026-10-08 21:48:00' AND status <> 'received' GROUP BY status ORDER BY 2;
SELECT 'rcpt_ok_latency|count=' || count(*) || '|avg_ms=' || round(avg(latency_ms)) FROM receipt_attempts WHERE started_at > '2026-10-08 21:48:00' AND status = 'received' AND model = 'qwen2.5:14b-8k';
