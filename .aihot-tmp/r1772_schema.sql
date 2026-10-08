SELECT 'tbl|' || table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY 1;
SELECT 'acols|' || column_name FROM information_schema.columns WHERE table_name='articles' ORDER BY ordinal_position;
