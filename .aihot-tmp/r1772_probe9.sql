SELECT 'gstat|' || coalesce(grouping_status,'null') || '|' || count(*) FROM articles GROUP BY grouping_status;
SELECT 'gstat_scored|' || coalesce(a.grouping_status,'null') || '|seladd=' || coalesce(a.selection_adds_value::text,'null') || '|' || count(*) FROM articles a JOIN publications p ON p.article_id = a.id WHERE p.score IS NOT NULL GROUP BY a.grouping_status, a.selection_adds_value;
SELECT 'sav|' || coalesce(selection_adds_value::text,'null') || '|' || count(*) FROM articles GROUP BY selection_adds_value;
