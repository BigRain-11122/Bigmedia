# BigStream 周报（{WEEK_LABEL}）

> 自动生成件（C-09 周报生成器·数据分析部归口）——生成时间 {GEN_TS}
> 本件=公司运营周报（L3 台账·非内容成品）；数据源=src/os/state.json + git log + src/os/backlog.md + orders/（四个机器源·无人工编辑）
> 诚实纪律：未上线=未测量（PLAN §5）——平台与内容数据在账号开通前一律「未测量」；本件可重跑覆盖（重生成=最新真相）

- 周期：{SINCE} ~ {UNTIL}（ISO 周 {WEEK_LABEL}）
- 轮次：本周 {ROUNDS} 轮（当前 tick={TICK}·idle {IDLE} 轮·其他账目 {OTHER} 条）
- 交付：{COMMITS_N} commits
- 任务板：本周完成 {DONE_N} 项·未完成 {OPEN_N} 项
- 令牌：本周 CEO 令 {ORDERS_N} 条

## 1 轮次实录（state.json）

{ROUNDS_LOG}

## 2 交付账（git log·{COMMITS_N} 条）

{COMMITS_LOG}

## 3 任务板燃尽（backlog.md）

### 本周完成（{DONE_N} 项）

{DONE_LOG}

### 未完成（{OPEN_N} 项）

{OPEN_LOG}

## 4 令牌账（orders/·本周 {ORDERS_N} 条）

{ORDERS_LOG}

## 5 度量（诚实纪律）

- 平台数据（涨粉/播放/互动率/完播率）：未测量——未上线（账号批次① 待 CEO 物理件·`output/analytics.md` 对账制已立）
- 内容发布：0——M5 闸不变；产线测试件（渲染试跑/TTS 试录/字幕对轴）=「测试件·非成品」不入发布队列（O-20260923-1756-bm-a）
- 循环健康：心跳与 tick 序列详见 `src/os/state.json`——未发生=未测量
