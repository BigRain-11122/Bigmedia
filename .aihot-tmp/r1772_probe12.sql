SELECT 'grp_done_recent|' || count(*) FROM articles WHERE grouping_status = 'complete' AND grouped_at > '2026-10-08 21:48:00';
SELECT 'grp_done_total|' || count(*) || '|last=' || coalesce(max(grouped_at)::text,'null') FROM articles WHERE grouping_status = 'complete';
SELECT 'grp_fail_recent|' || count(*) FROM articles WHERE grouping_status = 'failed' AND updated_at > '2026-10-08 21:48:00';
SELECT 'rcpt_purpose|' || purpose || '|' || status || '|' || count(*) FROM receipt_attempts WHERE started_at > '2026-10-08 21:48:00' GROUP BY purpose, status ORDER BY 1;
