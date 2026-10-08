SELECT 'pgboss_names|' || name || '|' || state || '|' || count(*) FROM pgboss.job GROUP BY name, state ORDER BY 1;
