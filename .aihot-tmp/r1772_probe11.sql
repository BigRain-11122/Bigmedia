SELECT 'gerr|' || left(grouping_error, 160) || '|cnt=' || count(*) FROM articles WHERE grouping_status = 'failed' AND grouping_error IS NOT NULL GROUP BY left(grouping_error, 160) ORDER BY count(*) DESC LIMIT 8;
SELECT 'gfail_recent|' || id || '|' || left(coalesce(grouping_error,'null'), 100) FROM articles WHERE grouping_status = 'failed' ORDER BY updated_at DESC LIMIT 5;
