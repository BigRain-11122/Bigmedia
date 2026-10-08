SELECT 'pub_sel|selected_true=' || count(*) FILTER (WHERE selected) || '|selected_false=' || count(*) FILTER (WHERE NOT selected) || '|scored_sel=' || count(*) FILTER (WHERE selected AND score IS NOT NULL) FROM publications;
SELECT 'pub_vis|' || visibility || '|' || count(*) FILTER (WHERE selected) || '/' || count(*) FROM publications GROUP BY visibility;
SELECT 'analyzed_states|' || processing_state || '|' || count(*) FROM articles WHERE processing_state = 'analyzed' GROUP BY processing_state;
SELECT 'facts_cnt|' || count(*) FROM facts;
SELECT 'stories_cnt|' || count(*) FROM stories;
SELECT 'story_status|' || coalesce(status::text,'null') || '|' || count(*) FROM stories GROUP BY 1;
