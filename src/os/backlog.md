# BigStream OS 循环任务板（backlog）

> 一行一任务，循环从上往下取第一条未完成项；完成=标 `[done YYYY-MM-DD]` 并 commit。新任务=追加到末尾；P1 级提案入板须标 `[needs-CEO]`。

1. [done 2026-09-23] 为 src/draft_lint.py 写最小测试件 tests/test_draft_lint.py（用临时夹具假稿，勿动 data/drafts 真稿）——落地=12 用例全绿 + tests/fixtures/ 10 假稿 + manifest.json（编码律：.py 纯 ASCII，中文只进数据件）；真稿回归 10 稿 0 FAIL
2. [done 2026-09-23] 建 docs/variant-templates.md——11 平台变体骨架模板（标题/画幅/字数/标签/封面提示规格骨架；模板非内容，不违反生产暂停令）
3. 选题库-台账一致性探针：校验 ideas.md 状态字段与 data/drafts 文件名前缀一一对应（可并入 draft_lint 或独立 src/board_check.py）
4. [needs-CEO] 生产暂停解除后的 M2 素材链路选型提案（TTS 音色/形象 prompt，按三案参数）
5. [blocked-by-pause] 视频号 4 稿口播实测 67-77s（draft_lint 实测·超 60s 规格）：恢复生产后统一裁至 ≤60s 或定快节奏读法
6. 自动周报生成器：src/os/state.json + git log → 周报 md（数据分析部归口·capabilities C-09）
