import io, json

p = 'docs/status-export.json'
lines = io.open(p, encoding='utf-8').read().split('\n')
assert 'OS' in lines[41] and 'R429' in lines[41], lines[41][:80]
new_t = ('   "t": "OS 循环 R430（生产轮·#68 P-2026-09-26-04 媒体文化区块块面调研件交付毕：'
         'docs/research/R-20260926-city-block-media.md v1.0 六必答 99 行·总规卡 7 槽位深化'
         '〔花瓣屏塔 5×5/光之街道素材实录面/滨水舞台广场/直播街区预留角位〕+plot 落位八条+器官司塔接口八行表·'
         '窗 ≤09-28 12:00 提前闭·送达三载体=本件+backlog done 行+commit 含令号·'
         '轮首五查 ledger 25=锚〔@八线全量第五模式首计漏=操作红当场修正〕·'
         '三探针 board 0 FAIL 5 题 10 稿/readiness 3 阻塞皆外部 CEO 面 0 发现/'
         'loop_health 1 FAIL 在案史实同事件足迹·state.json 尾逗号探针咬住即修=JSON 校验过）·state.ts/task 心跳面刷新",')
lines[41] = new_t
io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
d = json.load(io.open(p, encoding='utf-8'))
print('json_ok export_ts', d['export_ts'], '| dept41', d['depts'][7]['t'][:40])
