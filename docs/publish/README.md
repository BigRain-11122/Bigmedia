# 发布文案目录（docs/publish/）

发布面文案 = 账号开到即可复制粘贴的成品件。账号未开不影响起草（未上线=未测量）。

## 索引

| 文件 | 内容 | 状态 |
|---|---|---|
| `mv0001-v511/BILIBILI-DESC.md` | B站标题（A/B）+ 简介 + 置顶评论 + 封面前置 + 对表 | 起草毕·待账号 |
| `mv0001-v511/YOUTUBE-DESC.md` | YouTube 中英标题 + description + 合成内容开关四项 + 对表 | 起草毕·待账号 |
| `mv0001-v511/AIGC-DECLARATION.md` | AIGC 声明四句式 + 放置规则表 + 不可删律 + 验收判据 | 起草毕·随发布执行 |
| `mv0001-v511/PUBLISH-COPY-V511.json` | 机器可读全量（标题/文案/信用/前置件/黑名单裁定） | 机读正身 |

## 两条口径（跨件一致）

1. **署名四件套 vs 人名黑名单**：CEO 令 2026-10-18 的「专辑名+作词+作曲+导演」只管**署名行与标题**；`PUBLISH-CHECKLIST` 2026-10-10 的人名黑名单继续管**宣传语/话题标签/置顶评论**（禁人名 hashtag、禁撞脸钩）。裁定与依据见 `PUBLISH-COPY-V511.json.copy_blacklist_resolution`。
2. **导演归属 = C 级**：邝盛（jaychou.wiki + newton 三源一致，未取得官方职员字卡）。发布前未核到官方字卡 → 用 fallback 标题变体（`bilibili_director_unverified_variant`），不硬写推测。

## 发布日操作顺序

1. 取 `PUBLISH-COPY-V511.json` → 按平台取标题/简介/置顶评论
2. 平台 AIGC 声明开关按其 `platform_switches` 勾选
3. 封面帧 = KFT（禁自动首帧）
4. 发布后 24h：把播放/完播/转粉读数登记进 station-reviews 与 `docs/status-export.json`
5. 发布页截图 → `qa/publish/`（声明开关状态留档）