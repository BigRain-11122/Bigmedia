SELECT 'rel_recent|' || an.relevance || '|' || count(*) FROM analyses an JOIN articles a ON a.id = an.article_id WHERE an.created_at > '2026-10-08 21:48:00' GROUP BY an.relevance;
SELECT 'an_recent_cnt|' || count(*) FROM analyses WHERE created_at > '2026-10-08 21:48:00';
SELECT 'pgboss_group|' || state || '|' || count(*) FROM pgboss.job WHERE name = 'group' GROUP BY state;
SELECT 'pgboss_analyze|' || state || '|' || count(*) FROM pgboss.job WHERE name LIKE '%analyze%' GROUP BY name, state;
