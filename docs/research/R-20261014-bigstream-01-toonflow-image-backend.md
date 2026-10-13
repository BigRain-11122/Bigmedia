# R-20261014-bigstream-01：Toonflow 图像后端配置位调研（LEG-3 ②）

> 需求锚=backlog #110 收尾腿 tech#151 ②（R2204 LEG-2 收口后剩余面：①LLM 腿 VRAM 门控·②本件·③全链 1 帧测试）。
> 方法=app bundle 源级实读（C:\Users\sjs20\tools\ToonFlow\app\toonflow\Resources\app\ 全树 grep+精读）·零 CDP 零 GPU 零 token·2026-10-14 02:2x 夜窗执行。

## 一、内置媒体供应商盘点（providers/media/ 三件全读）

| 供应商 | 图像能力 | 端点可配性 | 定性 |
|---|---|---|---|
| tfRouter | doubao-seedream-5.0 Pro/Lite + 全能图片G-2.0/2.5（云模型） | **不可**（apiUrl 硬编码 api.toonflow.net/v1·仅 apiKey 输入） | 官方云中转·key=账号域 CEO 物理件 |
| apiMart | 视频系（seedance/wan）为主 | 不可（getBaseUrl 按 isOverseas 国内/海外双址切换） | 云市场·同上 |
| metaso | **无图像模型**（仅 MiniMax-H3 视频） | **唯一带 baseUrl rules 字段**（默认 metaso.cn/api/minimax）——但媒体供应商编辑界面只渲染 apiKey（类型契约原文「当前媒体供应商编辑界面只提供 API Key 输入」）→ baseUrl 字段 UI 可达性存疑，且模型表 video-only | 云中转·视频 |

**结论 A：内置三家全部云端、无本地图像通道；本地 ComfyUI 只能走自定义供应商路。**

## 二、自定义供应商路（正身=addCustomProviderDialog）

- **导入通道两条**：「文件导入 .ts → 添加」/「粘贴代码 → 添加」（对话内嵌助手提示词原文）→ **手写 .ts 文件导入=零 LLM 依赖零 GUI 多轮**（GUI 只 1-2 次点击，利于「人工干预点 ≤2/集」判据）。
- **ComfyUI 接入分支=厂商一等公民**（助手提示词专节）：要求=API 格式工作流 JSON（节点 id 为键·class_type/inputs）、服务端可达 HTTP(S) 地址（**不能固定写 localhost:8188——localhost 指 Toonflow 服务端机器**；本机单机部署下 127.0.0.1:8188 即同机=可达，但注释明示须按部署实况确认）、无鉴权服务跳过密钥、上传协议/输出节点映射/任务安全取消（禁用 /interrupt 与清队列误伤他任务）均须按实际资料实现。

## 三、适配文件开发契约（类型源=对话 bundle 内嵌 types.d.ts 全文实读）

1. `export default {...}` 对象字面量直出（禁变量中转/工厂/展开/计算属性）；文件名=供应商 id+.ts。
2. id 小驼峰 ≤96 字符（禁 con/prn/aux/nul/com1-9/lpt1-9 保留名）；version 首版 "2.0.0"；id/label/version/readme/models **全字面量**。
3. 服务端 Bun 环境：**禁 import/require/DOM/process/文件系统/全局 fetch/全局 Bun/FormData/File/WebSocket/crypto**；宿主供 `this.tool.fetch`（普通 async 方法经 this 取）/`this.tool.hash`/`this.tool.image`/`this.config`/`this.signal`/Buffer/URL/URLSearchParams/TextEncoder/Decoder/Blob/AbortController/AbortSignal/setTimeout。
4. **无鉴权本地 ComfyUI → `rules: []`**（不添 apiKey 项）；地址=公开资料直接写入适配器（媒体界面只有 apiKey 框）。
5. models 只声明真实能力（文本生图首发=单模型 `mode:["text"]`·imageSizes/imageRatios 按工作流真实档位）；generateImage 返回 `MediaAsset[]`（type:"url" 需 HTTP(S) 地址——ComfyUI `/view?filename=..` 直链即合法 url 型返回，最省转换）。
6. 长任务：轮询须响应取消+有限超时；错误抛中文可读；禁检查更新等无关行为。

## 四、本地可达性裁定（R1774「ComfyUI 网关=bm-c lane 预核」承接）

- **本机**：Toonflow 服务端与 ComfyUI 8188 同机（bm-a）→ 127.0.0.1:8188 可达性成立；**但 8188=MV 会话共享域（R2204 注·勿抢纪律）**——测试生成窗须避开 MV 活跃期（或 MV 收口后），队列共享期提交=抢队违例。
- **bm-c**：ComfyUI 只听 127.0.0.1（10-12 机队记忆·远程不可达）→ bm-c 图像后端路需其侧网关/放行=**bm-c owner 域动作，本司零代办**（预核结论维持 R1774 口径）。
- 当前窗（10-14 02:2x）：GPU free 311MB/util 98%=VRAM 饿空 → ①LLM 腿与③测试帧同 F 卡族 load-class 门（8704MB 档）结构性关窗；②调研=本件 CPU 面已毕。

## 五、下腿（tech#152 承载）

**手写 comfyui-local 适配 .ts**（CPU 面零 VRAM 零 LLM）：嵌 Qwen-Image-2.1 API 工作流（runner_r1792 谱系在册）+单 text 生图模型声明+`/prompt`→`/history` 轮询+`/view` url 返回+无鉴权 `rules: []`+唯一文件名防覆盖；判据=文件过契约自检（字面量/无 import/保留名/类型面）+Toonflow 导入成功+（VRAM/MV 窗开后）1 帧真实产出。导入+测窗=③全链收口位。
