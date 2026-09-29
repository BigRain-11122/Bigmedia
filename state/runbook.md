# BigStream runbook（Executive Protocol·state/runbook.md·<2KB 启动读面·2026-09-29 R681 建面）

- 定位：FLUX 集团 AI 媒体公司 BigStream（硅基城市多线内容：短视频/L-卡/网文/有声/漫画）
- 执行体：OSLoop 循环（L0）+ bm-a 会话（内容线）·计划任务 BigStream-OSLoop ~15min 节律
- 启动序：快速判定五查（state log 尾+backlog 顶+orders 顶+git status+集团转办两件头 ledger/decisions 内容寻址）→五静全静跑三探针→按序取活（backlog 顶行→self-improvement-queue 顶项→创新提案轨→declared-idle 一行声明）；任一异常=全任务书 src/os/iteration_prompt.txt
- 量产态：production open（D-BS-06·拍稿压缩→TTS light→对位表素材探针先行→R-E 三 profile 渲染→S2 三门→E8 终审 ≥9→M4 四检→F 登记成品库）；发布锁=M5 账号物理件（CEO 面·未上线=未测量）
- 台账：src/os/state.json（tick+log+ts/task 机读面）·backlog.md 认领制·output/finished.md 成品库·renders/station-reviews 台账
- 探针：board_check/readiness/loop_health 每轮照跑（例行=脚本零 token·判断=模型）
- 例行件：情报日报 data/intel/daily/<日期>.md（当日缺=先补产再干别的）·周自审 docs/audits/<ISO 周>（缺=任意轮补）·global-benchmarks 7 天刷新（下期 10-01）·HQ-FEEDBACK 日清（无集团层 open 问题=零膨胀）
- 专家面：python src/call_expert.py --expert <id> --material <件>（名册 docs/expert-roster.md·本地 Ollama·按需调用）
- 收账：tick+1+log 行+ts/task 刷新→status-export 刷→显式列文件 git add→commit（英文一行 ≤500 字符·[via bm-a] 尾标）→push；并窗律=os-protocol §6（窗满 6/跨日/异常/实活即收）
- 红线：不标题党/无来源不发布/AIGC 依法显著标识/脱敏律（仓位密钥 token 禁入素材）/账号域永不代办/跨仓写禁令（只写本仓）/同仓退避（index.lock 或他执行体写盘=只读）/P1 面只提案 [needs-CEO]
