# GitHub 工具普查与安装台账 v1.0（github tooling survey）

> CEO 令 O-20260928-18XX：「去github去找你公司能用到的所有环境，工具，skills，mcp等等，全面安装」。
> 纪律=`docs/research-protocol.md`（源分级/零断言/台账）；安全律=只装可溯源官方源（modelcontextprotocol/anthropics/comfyanonymous 等）+许可证面人工核；科学判断闸=「能用到的」=按公司产线缺口选型·禁虚荣安装。
> 环境实测（2026-09-28）：Windows·Python 3.14.4·git 2.55·node 24.16·uvx 0.12.19·盘余 906GB·RTX 4070S 12GB。

## §1 选型决策表

| 类 | 项 | 来源（可溯源） | 决策 | 依据 |
|---|---|---|---|---|
| MCP | Fetch/Everything/Git/Memory/SequentialThinking/Time | github.com/modelcontextprotocol/servers（官方参考七件） | **不装** | 与 Codely 内建能力全量冗余（web_fetch/文件工具/git shell/结构化记忆）——MCP 每件都对全会话征 token 税·冗余件=负收益 |
| MCP | **Playwright MCP** | github.com/microsoft/playwright-mcp（微软官方） | **装** | 真实缺口：账号期平台数据采集/页面自动化（P-76 粉丝经营采集架构的执行底座）+截图取证；微软官方源·npx 即用 |
| Skill | **docx/pdf/pptx/xlsx 文档四件** | github.com/anthropics/skills（Anthropic 官方） | **装** | 公众号图文→docx 导出/调研 PDF 提取/汇报 pptx/数据 xlsx——媒体公司运营面真实需求；标准 SKILL.md 结构=Codely 原生兼容 |
| 工具 | **funasr**（pip） | github.com/modelscope/FunASR（阿里达摩院） | **装** | 中文 ASR 升级件——S2 门在案痛点=whisper 同音错字（13.07%→5.53% 已用模型档位调优·funasr ParaFormer 为 zh 原生更优解·S2 QC 双轨候选） |
| 工具 | **jieba**（pip） | github.com/fxsjy/jieba | **装** | 中文分词——网文线文本分析底件（词频/句长分布/金句检测机检候选） |
| 工具 | **yt-dlp**（pip） | github.com/yt-dlp/yt-dlp | **装** | 对标采样器——B3 池（B站热门结构拆解）需要真实样本源；用途=公司内部对标研究·合规注在案 |
| 环境 | **ComfyUI** | github.com/comfyanonymous/ComfyUI | **装 ✓（09-28 落地）** | C-11 文生图位既定缺口（m2-local-stack §1 画面后置升级·原记 C-16 为撞号误指 09-28 更正）——漫画/图文卡线的本地批量图像生成位（云通道已定栈·本地位=零边际成本批量+显存分时）；uv venv 锁 Python 3.12（3.14 兼容未证） |
| TTS 栈 | GPT-SoVITS/CosyVoice/IndexTTS/F5-TTS | 各官方仓 | **缓装（候选台账）** | 有声线多声线本地化=真实远期需求·但多 GB 级安装+商用许可面须专项核+与 Ollama/ComfyUI 显存分时冲突须排程——盲装=坏工程；专项评估后再定（§3 台账） |
| 工具 | whisperX/moviepy/pysubs2 等 | — | **不装** | faster-whisper+FFmpeg 既有链覆盖；无新缺口不装（禁虚荣安装） |

## §2 安装实况（2026-09-28 17:4X-17:5X）

| 批 | 项 | 结果 |
|---|---|---|
| pip 三件 | funasr 1.4.16 / jieba / yt-dlp 2026.08.19 | ✅ 全装·import 验证过（funasr 模型首用时自动下载=显存分时排程注记在案） |
| 技能七件 | docx/pdf/pptx/xlsx/doc-coauthoring/canvas-design/mcp-builder（anthropics/skills·user scope=`~/.codely-cli/skills/`） | ✅ 全装成功（四件为覆装=此前已有）；brand-guidelines 装后即卸（Anthropic 自家品牌色与我司黑白品牌冲突） |
| 既有技能盘点 | capcut-edit（剪映工程编辑·字幕/卡点/切片）/algorithmic-art/dispatching-parallel-agents 等 | 在册（此前未知资产·capcut-edit=视频线相关） |
| MCP 配置 | Playwright（microsoft/playwright-mcp 0.0.82·`npx -y @playwright/mcp@latest`·media/.codely-cli/settings.json workspace 级） | ✅ 实跑验证过；生效=新会话起（MCP 随会话启动加载） |
| Node 环境 | v24.19.0 已装（C:\Program Files\nodejs·系统级 Machine PATH 在位） | ✅ 核验完成（本会话陈旧 PATH 曾误导·已排除） |
| ComfyUI | C:\Agent\ComfyUI·uv venv py3.12.14·torch 2.14.0+cu126 | ✅ **装毕双验证（09-28）**：`torch.cuda.is_available()=True`（cuda:0 RTX 4070S 12GB）+`main.py --quick-test` 启动绿（v0.37.0·DynamicVRAM enabled·exit 0）；🟡 诚实注记=cu126 下 comfy_kitchen 优化 CUDA 后端 disabled（上游建议 cu130+·现走 eager 后端=可用非最优·升级与否挂显存排程专项） |
| MCP 官方七件 | Fetch/Everything/Git/Memory/SequentialThinking/Time/Filesystem | ❌ 判不装（与 Codely 内建能力全量冗余·每件对全会话征 token 税=负收益）——决策依据在 §1 |
| **DDG 搜索 MCP**（v1.1 增采） | nickclyde/duckduckgo-mcp-server（uvx·`DDGSearch`） | ✅ 采纳自集团调研 R-20260928-gh-install-mcp（「Codely 无搜索工具的真空白」——**历次调研件「无搜索通道」卡点（U6-U8 同族）的解药**）；uvx 实跑验证过（初始化成功·限速策略自报） |
| **Playwright 配置修正**（v1.1） | settings.json 改 `cmd /c npx` 包裹 | ✅ 采纳集团调研「Windows 须 cmd /c 包裹律」——原直配 npx 会在 stdio 启动失败；npx.cmd 实跑 0.082 验证过·node 24.19 系统 PATH 在位 |
| **Agent-Reach CLI**（v1.1 增采） | Panniantong/Agent-Reach（uv tool·`C:\Users\sjs20\.local\bin\agent-reach.exe`·集团调研指派本司内容调研面） | ✅ CLI 装毕验证过（list/install/doctor 面）；渠道实装 **rss ✓（feedparser）+ youtube ✓（复用 yt-dlp）**；**bilibili 渠道=上游 PyPI 版未含（master 在案·发版后升级）**——B站免登录采集挂账待上游；cookie 平台（XHS/Twitter/Reddit）=专用小号原则·账号期待办 |

## §3 候选缓装台账

| # | 项 | 缓装理由 | 解锁条件 |
|---|---|---|---|
| D1 | GPT-SoVITS | 多 GB+商用模型许可专项核+显存排程 | 有声线声线多样化专项（音色合规审后） |
| D2 | CosyVoice/IndexTTS | 同上 | 同上（对比测评后择一） |
| D3 | F5-TTS | torch 环境共享方案先定（ComfyUI venv 复用评估） | ComfyUI 装毕后——**触发条件已满足（09-28 装毕）**·待有声线专项启动 |
| D4 | 社区 MCP（MCP Registry） | 无搜索通道逐个溯源+供应链安全审查成本高 | 逐个专项核（账号期采集需求触发） |

## 结论应用表

| 结论 | 落点 | 状态 |
|---|---|---|
| 选型决策表（七不装+四装+三缓） | 本件=公司工具面正典 | 已闭环 |
| pip 三件+技能四件+Playwright MCP+ComfyUI | 安装实况（§2） | **已闭环（09-28）**——全部项装毕验证过（Playwright/DDGSearch MCP 生效=新会话起） |
| 缓装台账 D1-D4 | ①任务单=专项评估触发制 | 接线中 |

## 变更记录
- 2026-09-28: v1.0 首版（CEO GitHub 全面安装令·bm-a 会话）——普查+选型+安装台账。
- 2026-09-28: v1.1 集团调研对齐增补——采 DDG 搜索 MCP（真空白·历次卡点解药）+Playwright 配置修正（cmd /c 包裹律）+Agent-Reach CLI（rss/youtube 渠道实装·bilibili 待上游发版）；交叉引用=`cph4/research/R-20260928-gh-install-mcp.md`（集团 MCP 普查正典·姊妹件分工：集团=全注册表面·本件=本司决策面）；本司相关的集团他件指派照旧（unity-mcp→Biggame/comfy-mcp→bm-c/github-mcp→CPH4·非本司份额）。
- 2026-09-28: v1.2 ComfyUI 收口——后台安装毕·双验证绿（torch cuda True+quick-test 启动 v0.37.0）；🟡 cu126 优化后端 disabled 注记入案；结论应用表全闭环（安装面毕·MCP 双件新会话生效·缓装台账转入触发待命态）；GitHub 全面安装令主体执行完毕。
