# -*- coding: utf-8 -*-
# r1967 E4 same-round backfill: review/finished/README/backlog/state log fix
import io, json, os, datetime

E4 = ('**E4 参考仪同窗落地 7.0**（tech#91 expert_retry_loop CLI 第二生产用例：首 DEFER 45s 后第二发 11:51:51 落判·'
      '净本 expert-verdicts/20261011-115151-E4-audience.md）——会看完明说+点赞转发条件式（「如果我对此类话题感兴趣，我可能会点赞和转发」）'
      '+保存条件式+7 分明说·旗①=侠气轴「值夜岗上风凉快，但别忘了巡逻」被旗「为配合热点强行套用·缺乏真实感和深度」扣分'
      '=池句 verbatim 不可改写〔v13 老货郎旗族续·吸收位=M5+系列语境+M6 池句选优回访锚〕·最弱=虚构城市反应融入度'
      '——REACT 带读数 v11 7.0→v12 8.0→v13 8.0→v14 7.0=带内下缘如实·非拦截席·七席 ≥9 PASS 维持')

# 1. review file: E4 row + strike 未测面
p = 'docs/reviews/review-20261011-mcreact-v14.md'
t = io.open(p, encoding='utf-8').read()
old_e4 = ('- E4 参考仪（受众反应面）：**异步重试环在飞**（tech#91 expert_retry_loop CLI·PID 35632·fire 窗 defer 自动重试至落地'
          '·追加制回填三件套=本评审单 E4 行+净本 expert-verdicts+finished 回填段·R1938 v13 E4 三飞回填先例同型）。')
new_e4 = '- ~~E4 参考仪（受众反应面）：异步重试环在飞~~ → **同轮回填毕（11:51:51 落判）**：' + E4 + '。'
assert old_e4 in t
t = t.replace(old_e4, new_e4)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('review E4 backfilled')

# 2. finished.md F-175 E4 clause
p = 'output/finished.md'
t = io.open(p, encoding='utf-8').read()
old_c = ('E4 参考仪=异步重试环在飞（tech#91 expert_retry_loop PID 35632·追加制回填三件套·非拦截席）')
new_c = ('E4 参考仪**同轮回填毕 7.0**（tech#91 expert_retry_loop 第二生产用例：首 DEFER 后第二发 11:51:51 落判·会看完+点赞转发条件式+7 分明说·'
         '旗①=侠气轴池句被旗强套感=verbatim 不可改写〔v13 旗族续·吸收位=M5+系列语境+M6〕·最弱=虚构反应融入度·REACT 带下缘如实·'
         '净本 expert-verdicts/20261011-115151-E4-audience.md·非拦截席）')
assert old_c in t
t = t.replace(old_c, new_c)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('finished F-175 E4 clause updated')

# 3. cards README row E4 clause
p = 'data/storylines/cards/README.md'
t = io.open(p, encoding='utf-8').read()
old_c = '·E4 异步在飞（tech#91 重试环）'
new_c = '·E4 同轮回填毕 7.0（tech#91 第二用例·净本 20261011-115151-E4-audience.md·带内下缘如实·非拦截席）'
assert old_c in t
t = t.replace(old_c, new_c)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('cards README E4 clause updated')

# 4. backlog #59 note E4 clause
p = 'src/os/backlog.md'
t = io.open(p, encoding='utf-8').read()
old_c = '·E4 异步重试环在飞（tech#91 PID 35632·追加制回填）——#59 维持开板'
new_c = ('·E4 同轮回填毕 7.0（tech#91 第二用例·首 DEFER 后第二发 11:51 落判·净本 20261011-115151·REACT 带下缘·非拦截席）——#59 维持开板')
assert old_c in t
t = t.replace(old_c, new_c)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('backlog #59 E4 clause updated')

# 5. state.json: rewrite last log line + task/focus/ts
p = 'src/os/state.json'
st = json.load(io.open(p, encoding='utf-8'))
NOW = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
LOG = st['log'][-1]
LOG = LOG.replace('——E4 异步重试环在飞〔tech#91 expert_retry_loop PID 35632·追加制回填三件套〕',
                   '——E4 参考仪**同窗落地 7.0**〔tech#91 expert_retry_loop 第二生产用例：首 DEFER 45s 后第二发 11:51:51 落判·会看完+点赞转发条件式+7 分明说·旗①=侠气轴池句被旗强套感=verbatim 不可改写〔v13 旗族续·吸收位=M5+系列语境+M6〕·最弱=虚构反应融入度·REACT 带 v11 7.0→v12 8.0→v13 8.0→v14 7.0 带内下缘如实·净本 expert-verdicts/20261011-115151-E4-audience.md·非拦截席·重试环 log 回调 GBK 崩=显示面 op-red 如实注记（调用与台账全落地）〕')
LOG = LOG.replace('tokens:local=0（本轮零本地模型调用·E4 在飞未落=落地轮记账·P-54⑤ 计量律如实记）',
                  'tokens:local=1（E4 qwen2.5:14b 本轮落地记账·本地 Ollama 零 API token·P-54⑤ 计量律如实记）')
LOG = LOG.replace('——下轮=R1968 E4 回填三件套+SC-005-04 何雨欣起链〔F-176〕/tech#92 判据窗 10-12 08:00。',
                   '——E4 回填三件套同轮销项毕（review E4 行+净本+finished 回填段）·下轮=R1968 SC-005-04 何雨欣起链〔F-176〕/REACT-v15 10-12 窗/tech#92 判据窗 10-12 08:00。')
st['log'][-1] = LOG
st['task'] = LOG.split('R1967: ', 1)[1][:60]
st['focus'] = 'R1967 REACT-v14 F-175+E4 7.0 同轮毕·R1968=SC-005-04 何雨欣领起位（F-176）+REACT-v15 10-12 窗·tech#92 判据窗 10-12 08:00'
st['ts'] = NOW
with io.open(p, 'w', encoding='utf-8', newline='') as f:
    json.dump(st, f, ensure_ascii=False, indent=2)
    f.write('\n')
print('state.json log/task/focus/ts finalized ts=%s' % NOW)

# 6. cleanup retry middleware (E4 landed)
for f in ['.c3-tmp/r1967_e4_retry.log', '.c3-tmp/r1967_e4_retry.err']:
    if os.path.exists(f):
        os.remove(f)
        print('deleted', f)
print('E4 BACKFILL DONE')
