# R1898 chronicle continuation batch 2: insert 10-10 row, bump counts, sync codex README + main queue note.
import io

CHRON = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines\codex\city-chronicle.md"
README = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines\codex\README.md"
MAINQ = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\state\queue\main.md"

ROW_1010 = (
    "| 10-10（第三周第四日） | **立线日**：**热点梗短视频账号+机队 AI 日产线令**"
    "（媒体司第二产品线立项：全网热点 AI 小剧场·日更 3 条·V1 尊界刹车片样片本窗直产"
    "·影射律成片零品牌名+转发引擎+评审授权=评审团 CERTIFIED 即产·账号名候选「梗闻联播」待 CEO 点）；"
    "**专家评审第二波扩席+经验积累令**（评审团六席→十三席：服化道/灯光/VFX/运镜/法务合规/平台运营六新席"
    "·判例册 EXPERIENCE-LEDGER+PROTOCOL v3+bigstream-expert-panel skill 正典三件套·每判例必须落闸）；"
    "CEO 用机让路修订（「本机不要占用算力」pause→修订二收窄授权面=本机金融回测+低清关键帧·机队满跑 MV）"
    "+**全片满跑放手令**（mv0001 机队一核满跑：bm-c 11 镜 i2v 全过〔int8 权重+768P〕+复古做旧 D 终版入链"
    "+女主年轻化终选板〔约二十岁锚〕·bm-a 装配终剪·13 席片闸 CERTIFIED 排 CEO）；"
    "**雷达双 greenlight**（D-08 雷达 MCP 端点 P1 裁定过〔本机研究面 7 tools〕"
    "+D-09 元宇宙「城市热点雷达」嵌入=快照生成器+首快照落件）"
    "+城市口径双换装激活（prefilter+selection-score 双换装+worker 重启激活+requeue 67·max 60 破 T1 首件"
    "·首份含城市源日报诚实空态定谳）；"
    "委员会全盘自查案开线（「好久没问了，最近为什么一直没有更新」）"
    "+软著全组合备齐令（32 款注册·A 机 14 款当日代码全量复跑）"
    "+P 系三基准设计令/填充批/U360 设计自查令（他司域）；"
    "jman LoRA 并行训练令（@bm-c 640px A/B）+lane 暂停让位修订；"
    "ollama wedged 服务级重启边界判例（F-03 收口→D-10 追认：blocker 亡+零活跃生成时重启属服务恢复=让路律条件失效面）"
    " | orders 10-10 批（O-20261010-0025/-0040/-1225/-1240/-1245/-1330+12:5x/13:1x/13:2x/13:3x 令行）"
    "+D-20261010-01~-10+C-20261010-01+MV/meme 窗台账 |"
)

# --- 1. chronicle: insert row after 10-09 row, bump footer ---
lines = io.open(CHRON, encoding="utf-8").read().splitlines()
assert not any("10-10（第三周" in l for l in lines), "10-10 row already present"
idx = None
for i, l in enumerate(lines):
    if l.startswith("| 10-09（第三周第三日）"):
        idx = i
        break
assert idx is not None, "10-09 anchor row not found"
lines.insert(idx + 1, ROW_1010)
out = []
for l in lines:
    if l.startswith("**计数**"):
        l = ("**计数**：立国周纪 14 项事件节点；大事记续表 09-29→10-10 续 12 日节点"
             "（2026-10-10 续采批二·loop R1898·历史事件 14→26）。"
             "来源清单：orders 台账全量/章件 ch1-v4/decisions 台账/capabilities 台账/station-reviews/state.json。")
    out.append(l)
io.open(CHRON, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("CHRON-OK rows+1 10-10 footer bumped")

# --- 2. README: status cell, ledger row, changelog row ---
txt = io.open(README, encoding="utf-8").read()
old_status = "| 历史 | `city-chronicle.md` | 编年史志（立国周纪·大事记·机制里程碑） | v1.1 续采批 |"
new_status = "| 历史 | `city-chronicle.md` | 编年史志（立国周纪·大事记·机制里程碑） | v1.2 续采批二 |"
assert old_status in txt, "chronicle status cell not found"
txt = txt.replace(old_status, new_status, 1)

anchor_ledger = ("| 台词池扩充批五 | 2026-10-10 | loop R1848 | +1（100→101） | 0 | 0 | 0 | 0 |")
assert anchor_ledger in txt, "ledger anchor not found"
ledger_row = (
    "| 编年史续采批二 | 2026-10-10 | loop R1898 | 0 | +1（25→26） | 0 | 0 | 0 | "
    "orders/decisions 台账只读消费（10-10「立线日」节点：热点梗短视频账号产线立项〔媒体司第二产品线〕"
    "+评审十三席扩容+经验册正典三件套+CEO 让路修订+全片满跑放手令+雷达双 greenlight"
    "+城市口径双换装激活+委员会全盘自查+软著全组合备齐·常态节律随轮续采首战） |"
)
# insert after the batch-5 ledger row line (find end of that line)
i = txt.index(anchor_ledger)
j = txt.index("\n", i)
txt = txt[: j + 1] + ledger_row + txt[j:]

changelog_anchor = "- 2026-10-10: 台词池扩充批五入账"
assert changelog_anchor in txt, "changelog anchor not found"
changelog_row = (
    "- 2026-10-10: 编年史续采批二入账（main#9 常态节律位·loop R1898 认领）"
    "——city-chronicle v1.2 大事记续表 10-10「立线日」节点续入（历史事件 25→26"
    "·常态节律首战：10-10 门控② 验收/meme 立线事件窗后随轮续兑现"
    "·下窗=10-11 门控②判据窗+meme V1 定版事件窗后随轮续）。\n"
)
txt = txt.replace(changelog_anchor, changelog_row + changelog_anchor, 1)
io.open(README, "w", encoding="utf-8", newline="\n").write(txt)
print("README-OK status+ledger+changelog")

# --- 3. main queue: note on item 9 ---
mq = io.open(MAINQ, encoding="utf-8").read()
mq_anchor = "常态节律=重大事件窗随轮续采（续采批在册·下窗=10-10 门控②/REACT-v13 事件窗后随轮续）"
assert mq_anchor in mq, "main#9 anchor not found"
mq_note = ("常态节律=重大事件窗随轮续采（续采批在册·下窗=10-10 门控②/REACT-v13 事件窗后随轮续）"
           "——**[R1898 续采批二 2026-10-10]**：10-10「立线日」节点续入（chronicle v1.2·历史事件 25→26"
           "·Meme 立线+全片满跑+雷达双 greenlight+评审十三席+城市口径激活五簇全录）"
           "——下窗=10-11 门控②判据窗+meme V1 定版事件窗后随轮续")
mq = mq.replace(mq_anchor, mq_note, 1)
io.open(MAINQ, "w", encoding="utf-8", newline="\n").write(mq)
print("MAINQ-OK item9 note")
print("ALL-OK")
