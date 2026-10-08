SELECT 'jdetail|' || left(detail, 500) FROM job_runs WHERE job = 'reports.compose' AND started_at > '2026-10-08 21:50:00' ORDER BY started_at DESC LIMIT 2;
SELECT 'jerr|' || left(error, 300) FROM job_runs WHERE job = 'reports.compose' AND started_at > '2026-10-08 21:50:00' ORDER BY started_at DESC LIMIT 2;
SELECT 'selcols|' || string_agg(column_name, ',' ORDER BY ordinal_position) FROM information_schema.columns WHERE table_name='selected_state';
SELECT 'sel_rows|' || count(*) FROM selected_state;
