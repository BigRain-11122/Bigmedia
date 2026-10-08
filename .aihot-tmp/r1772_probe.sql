SELECT 'articles|' || state || '|' || count(*) FROM articles GROUP BY state ORDER BY 2;
SELECT 'pubs|total=' || count(*) || '|scored=' || count(score) || '|ge60=' || count(*) FILTER (WHERE score >= 60) || '|ge65=' || count(*) FILTER (WHERE score >= 65) || '|ge76=' || count(*) FILTER (WHERE score >= 76) FROM publications;
SELECT 'scored_minmax|min=' || min(score)::numeric(5,1) || '|max=' || max(score)::numeric(5,1) || '|avg=' || round(avg(score),1) FROM publications WHERE score IS NOT NULL;
SELECT 'stories|' || count(*) FROM stories;
SELECT 'scored_recent5|' || id || '|' || score FROM publications WHERE score IS NOT NULL ORDER BY id DESC LIMIT 5;
