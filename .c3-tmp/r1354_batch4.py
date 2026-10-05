# -*- coding: utf-8 -*-
"""R1354: #86 a-leg batch-4 append. city-spirit.md v1.3 -> v1.4:
17 proverb-grade rows (#84-100) from BigLife pools tail-harvest,
+ README ledger row + changelog entries. Anchored replacements only."""
import io, os, sys

CWD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CWD)
SPIRIT = os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md")
README = os.path.join(ROOT, "data", "storylines", "codex", "README.md")

ROWS = [
    (84, "来来往往，人都是靠买卖牵线的。", "台词池·侠气轴（开市场景·池级署名）"),
    (85, "邻里之间多帮衬，才是真兄弟。", "台词池·侠气轴（夜市场景·池级署名）"),
    (86, "算盘这会儿打清了，该收心回家了。", "台词池·侠气轴（收市场景·池级署名）"),
    (87, "茶水刚沏，润润嗓子才好唱老腔。", "台词池·怀旧轴（晨间场景·池级署名）"),
    (88, "捡破烂也是门技术活，得眼尖手快。", "台词池·怀旧轴（晨间场景·池级署名）"),
    (89, "伞骨咔咔响，人生故事多得像这雨后的路。", "台词池·怀旧轴（雨天场景·池级署名）"),
    (90, "修伞老李头手里的伞骨纹丝不动，就像他的心事。", "台词池·怀旧轴（周末场景·池级署名）"),
    (91, "这夜市里的烟火气，才是真滋味。", "台词池·怀旧轴（夜市场景·池级署名）"),
    (92, "米缸还得勤添，不缺才好。", "台词池·烟火轴（雨天场景·池级署名）"),
    (93, "炒锅里的剩菜热一热又是一顿好饭。", "台词池·烟火轴（收市场景·池级署名）"),
    (94, "守着规矩，心里才踏实。", "台词池·秩序轴（黄昏场景·池级署名）"),
    (95, "夜幕低垂，心中有数就好。", "台词池·秩序轴（黄昏场景·池级署名）"),
    (96, "规矩不能乱，但偶尔放松一下也行。", "台词池·秩序轴（周末场景·池级署名）"),
    (97, "守门人说，规矩里也有温暖，夜归人听得到。", "台词池·秩序轴（夜市场景·池级署名）"),
    (98, "灯火里的值夜岗，是夜的守望者。", "台词池·秩序轴（夜市场景·池级署名）"),
    (99, "茶香四溢，生活不就该慢慢来。", "台词池·逍遥轴（周末场景·池级署名）"),
    (100, "茶室里的客人，都是慢慢才来的。", "台词池·逍遥轴（黄昏场景·池级署名）"),
]

spirit = io.open(SPIRIT, encoding="utf-8").read()

# 1) title bump
old_title = "# 硅基城市精神志（City Spirit）v1.3"
new_title = "# 硅基城市精神志（City Spirit）v1.4"
assert spirit.count(old_title) == 1, "title anchor"
spirit = spirit.replace(old_title, new_title)

# 2) insert rows after row 83
anchor83 = "| 83 | 叮叮叮，夜晚才醒。 | 台词池·像素灵（周末场景·池级署名） |"
assert spirit.count(anchor83) == 1, "row83 anchor"
block = anchor83 + "\n" + "\n".join("| %d | %s | %s |" % r for r in ROWS)
spirit = spirit.replace(anchor83, block)

# 3) counter line
old_cnt = "**计数**：83 条（种子批 26 + 台词池扩充批 18 + 台词池扩充批二 20 + 台词池扩充批三 19）。来源清单：BigLife 首夜台账/census C-00010·C-00011·C-00016·C-00017 卡/章件 ch3-ch5/FluxVerse DESIGN/集团 governance 与令牌台账/craft §6/台词池 `life/BigLife/cognition/pools.json`（#27-83·跨仓只读·池级署名·批二首采节日/令件场景·批三首采晨间/黄昏/高温/寒潮/开市/收市/令件/周末场景）。"
new_cnt = "**计数**：100 条（种子批 26 + 台词池扩充批 18 + 台词池扩充批二 20 + 台词池扩充批三 19 + 台词池扩充批四 17）。来源清单：BigLife 首夜台账/census C-00010·C-00011·C-00016·C-00017 卡/章件 ch3-ch5/FluxVerse DESIGN/集团 governance 与令牌台账/craft §6/台词池 `life/BigLife/cognition/pools.json`（#27-100·跨仓只读·池级署名·批二首采节日/令件场景·批三首采晨间/黄昏/高温/寒潮/开市/收市/令件/周末场景·批四收尾采=谚语级现量见底）。"
assert spirit.count(old_cnt) == 1, "counter anchor"
spirit = spirit.replace(old_cnt, new_cnt)

# 4) changelog entry (append after v1.3 entry = last line of file)
entry = ("- 2026-10-05: v1.4 台词池扩充批四（O-20260928-1910 执行件③ a 腿四批·loop R1354 认领·R1353「下批随轮评估」指针当轮兑现）"
         "——414 净候选（r1354_pool.py 机证·排除已采 83+三志在册面）→谚语级精选 17 条（#84-100·侠气 3+怀旧 5+烟火 2+秩序 5+逍遥 2"
         "·**求新/像素灵零入选如实注**〔余面全为场景闲谈/拟声弱行〕·池级署名+场景标注）；"
         "**严格质量门=近孪剔除面首立**（含已采行 verbatim 前缀行 2〔船长说，船要靠岸…含 #39/调解阿姨说，加固招牌…含 #40〕"
         "+主题孪行 5〔今儿鱼没上钩…=#80 鱼儿不咬钩·我也心平气和/云淡风轻，心自安=#60 闲云浮流水·悠然自得心/江边听浪，心已归处=#39 心有着落母题"
         "/修伞的活儿得有耐心=#54 修伞匠慢工出细活/街坊邻居走动，日子才旺=#78 街坊邻居互相照应〕+主题饱和剔除 2〔熬汤三连饱和〔#49 越煮越香+#69 慢火炖〕"
         "/茶·慢周末双行取一取 aphorism 强者〕——TOP1 尺质量优先·凑数禁）；"
         "机核 17/17 PASS（r1354_verify.py=verbatim 对 pools.json+对 #1-83 零重+三志在册面零重+fleet 卡面级去重承继 R1353 标准）；计数 83→100。"
         "**四批累计谚语级现量采掘毕**——剩余 ~397 候选=场景闲谈级为主+零星边缘行不足成批·下批待 BigLife 池扩容后 fresh 全量重筛（不预立律·承 R1353 derive 教训）。")
spirit = spirit.rstrip("\n") + "\n" + entry + "\n"

io.open(SPIRIT, "w", encoding="utf-8").write(spirit)
print("city-spirit.md written, rows 84-100 inserted, v1.4")

# ---- README ----
r = io.open(README, encoding="utf-8").read()

old_row = "| 精神 | `city-spirit.md` | 精神志（城规律/居民谚/职业伦理/失败观·城市精神谱系） | v1.3 台词池扩充批三 |"
new_row = "| 精神 | `city-spirit.md` | 精神志（城规律/居民谚/职业伦理/失败观·城市精神谱系） | v1.4 台词池扩充批四 |"
assert r.count(old_row) == 1, "readme s1 anchor"
r = r.replace(old_row, new_row)

ledger_anchor = "| 台词池扩充批三 | 2026-10-05 | loop R1353 |"
idx = r.index(ledger_anchor)
line_end = r.index("\n", idx)
ledger_row = ("| 台词池扩充批四 | 2026-10-05 | loop R1354 | +17（83→100） | 0 | 0 | 0 | 0 | 台词池 `cognition/pools.json` 跨仓只读"
              "（O-1910 a 腿四批·池级署名·414 净候选→谚语级精选 17 条 #84-100·侠气 3+怀旧 5+烟火 2+秩序 5+逍遥 2·求新/像素灵零入选如实注"
              "·近孪剔除面首立〔含 #39/#40 verbatim 前缀行 2+主题孪行 5+主题饱和 2〕·机核 17/17 verbatim+零重+fleet 去重 PASS〔r1354_verify〕"
              "·四批累计谚语级现量采掘毕·下批待池扩容 fresh 重筛） |")
r = r[:line_end + 1] + ledger_row + r[line_end + 1:]

rlog_anchor = "剩余 414 净候选三筛后谚语级密度显著下降如实注——下批随轮评估或待 BigLife 池扩容）。"
assert r.count(rlog_anchor) == 1, "readme changelog anchor"
rlog_entry = rlog_anchor + "\n- 2026-10-05: 台词池扩充批四入账（O-20260928-1910 执行件③ a 腿四批·loop R1354 认领·R1353 随轮评估指针当轮兑现）——city-spirit v1.4 精神条 83→100（+17：#84-100·414 净候选→谚语级精选·近孪剔除面首立〔verbatim 前缀行 2+主题孪行 5+主题饱和 2·TOP1 尺严格质量门〕·池级署名+场景标注·机核 17/17 verbatim 对 pools.json+对 #1-83 与三志在册面+fleet 卡面级去重承继 PASS·**四批累计谚语级现量采掘毕**——剩余 ~397 候选场景闲谈级为主·下批待 BigLife 池扩容 fresh 全量重筛〔不预立律〕）。"
r = r.replace(rlog_anchor, rlog_entry)

io.open(README, "w", encoding="utf-8").write(r)
print("README.md written, ledger row + changelog appended")
