# BigStream 发布准备度报告（Readiness Probe）

> 生成：{GEN_TS}｜探针：`src/readiness.py`（平台运营部归口·纯只读·重跑即刷新）
> 口径：距离首发＝批次①账号亮灯＋10 稿 M4 门全绿＋测试件纪律零发现；未上线＝未测量；阻塞≠失败（发布前诚实态）。

## ① 账号亮灯（{ACC_N} 平台·状态流：{ACC_FLOW}）

| 平台 | 状态 | 备注 |
|---|---|---|
{ACC_ROWS}

## ② 稿件 GATE 态（{DRAFT_N} 稿）

| 稿件 | GATE |
|---|---|
{GATE_ROWS}

## ③ 产线测试件（`output/renders/`·{RENDER_N} 件·标注核验「测试件·非成品」）

| 文件 | 标注 |
|---|---|
{RENDER_ROWS}

## ④ 待 CEO 决策与暂缓项（backlog 标记）

**[needs-CEO]（{NEEDS_N} 项）**

{NEEDS_LIST}

**[suspended]（{SUSP_N} 项）**

{SUSP_LIST}

## 距离首发的阻塞清单（{BLOCKER_N} 项）

{BLOCKERS_LIST}

## 探针发现项（findings·机器纪律核验）

{FINDINGS_LIST}
