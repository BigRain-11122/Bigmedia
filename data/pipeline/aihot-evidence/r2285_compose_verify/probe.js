const { Client } = require('C:/Users/sjs20/Desktop/FluxGroup/media/BigStream/data/assets/aihot-poc/AIHOT/node_modules/pg');
const c = new Client({ connectionString: 'postgres://aihot:2c8e31a57a7ce97681dd05ab1e37bc46@127.0.0.1:55432/aihot' });
(async () => {
  await c.connect();
  const q = async (sql) => (await c.query(sql)).rows;
  const cols = await q("select column_name from information_schema.columns where table_name='job' and table_schema='pgboss' order by ordinal_position");
  console.log('job cols:', cols.map(r => r.column_name).join(','));
  const jobs = await q("select name,state,created_on,started_on,completed_on,retry_count,start_after from pgboss.job where name='cron.reports.compose' order by created_on desc limit 3");
  for (const j of jobs) console.log(JSON.stringify(j));
  const daily = await q("select count(*)::int as n, max(window_start) as latest from reports where kind='daily' and window_start > now() - interval '2 days'");
  console.log('== recent daily reports ==', JSON.stringify(daily[0]));
  const jud = await q("select count(*)::int as n from analyses where created_at > '2026-10-15 08:00:00+08' and selection_score is not null");
  console.log('judged-since-0800:', JSON.stringify(jud[0]));
  await c.end();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
