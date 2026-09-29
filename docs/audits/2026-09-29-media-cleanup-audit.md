# media/ 司域清理审计轮（P-20260929-13·72h 窗内领令清决）

- 日期：2026-09-29（R702）·执行体：BigStream-OSLoop [via bm-a]·令源=CEO 令 O-2026-0929-033（resource-chain §三§11 首批执法）·backlog #93
- **回执一行（对象/体积/判级）**：`_trash-20260928`（客户端已轮转删除暂存旧 auto-saves·1266 件 09-23~09-28）=**1.18GB·Class-A 直清已执行**；`output/renders` 历史档=**685MB·R3 清决建议（未执行·开闸批处置）**；auto-saves 活面=**453MB·水位线内零清对象**；bonsai=**6.1GB·冻结（10-09 判读窗）**；hf-cache=**1.46GB·在役冻结**

## 一、体积分层扫描（2026-09-29 20:14 实测）

- BigStream 仓=**10.0GB/10,756 件**：gitignored 9.0GB · tracked 519MB · untracked(未忽略) 9.7MB · `.git` 493MB；media 侧翼件 43MB（media/.codely-cli+两 md）
- 大件分布：`data/assets/bonsai` 6.1GB（27B GGUF+cudart/llama-bin·冻结见§二）·`output/renders` 1.2GB·`.codely-cli` 1.4GB（**清后 ≈248MB**）·`data/storylines/audio` 250MB（有声线 v4 在途 amb 中间件·冻结③）·`.bs*/.lc*-tmp` 批中间件族 ~350MB（声明行在案·随批次闭收账律）
- `.git` 493MB < 2GB 水位线（Biggame .git gc 项不适用本仓·git 历史零触碰）

## 二、R2 素材登记面（判级三问：②无云副本→R2 归档优先·③在途引用→冻结）

| 对象 | 体积 | 判级 | 处置 |
|---|---|---|---|
| `data/sources/footage`（实录源 28 件：citywatch/looplog/reviewsdoc/editgrid/biggame-cockpit 五源 raw+16x9+vertical+净裁系） | 35.2MB | **R2 源资产**（实录不可再生） | 已登记=renders README 声明行+对位表引用在案·云归档通道（TRANSFER manifest 判据）待开闸批 |
| `census-card-v*-vertical.mp4`（8 件·L 卡 PNG 派生源） | ~4.9MB | R3（PNG 可再生派生） | 产线活跃·冻结③ |
| `data/assets/piper-models`（huayan onnx 备份线） | 60.3MB | R2 | 在册（m2-local-stack §4） |
| `data/assets/bonsai`（Ternary-Bonsai-2-27B GGUF 5.5GB+cudart 373MB+llama-bin 245MB） | 6.1GB | **冻结③** | T-70 判读窗 10-09 联动（resource-chain 变更记录「Bonsai 冻结」）·清决随窗（CPH4 主责）·本司仓内代管 |
| `data/storylines/audio` sc001 v1-v4 tmp（amb beds 族） | 250MB | R3 中间件·在途③（有声线 v4 在产） | 随批次闭收账律 |

## 三、auto-saves 水位核验（@全司份额·水位线=30 天/500 件）

- repo `.codely-cli/auto-saves`：136 件 247.9MB（09-28 22:39 后活跃）·media/.codely-cli/auto-saves：7 件 43.0MB·FluxGroup/.codely-cli/auto-saves：78 件 162.6MB（组根·值守面）
- 全部 ≤30 天·各点 <500 件=**水位线内零超线零清对象（如实·不造清理动作）**
- 直清对象=已轮转进 `_trash-20260928` 的旧件（1266 件·09-23~09-28·客户端 09-28 自轮转删除暂存）——§11 Class-A 明列 auto-saves 类免隔离直清·活面 136 件零接触

## 四、过期导出清决（建议与执行分离·已登记成品零误清）

- 现行成品+在链件=37 件 499.9MB（F-001~F-006：v15 系×4+v14b-douyin+DD 200MB+BS-006+LC-001~008 拆条系+bs-005/005e 在链+C1 备件）——**保留**
- 历史档 mp4=37 件 685.1MB+辅助件 22.9MB（bs-001 v2~v14 系/live-A·B/voice 样件/bs-002~004 v1·v2·v2b 等·renders README 皆注「已被取代·盘上留档」）
- **清决建议**：R3 可再生（产线数据件全在 git 可重渲）·按 production-chain v2.0 §0 存量冻结律=**待开闸批「发布件替换清盘」统一处置**·本轮零执行（判级三问③ 台账引用在案）

## 五、HF 缓存消失事故根因面核验（R701 自愈后续）

- 时间线：09-24 锚 1.53GB 本地缓存（09-29 上午 R668 尚在役）→ R701 ASR offline 首飞 FAIL（缓存消失·本仓零删改记录）→ 网络双端探针（hf-mirror 0.56s/hf.co 0.92s）→ 重下 1.46GB @~48MBs → exit 0
- **根因=集团首夜清理波**（resource-chain 变更记录 2026-09-29：hf-cache 1.9GB Class-A 直清）波及本司 ASR 产线活跃模型 faster-whisper medium——集团动作按 §11 合法（hf-cache 明列 Class-A）·但撞上在途生产引用（判级三问③ 应冻结至结案）
- 处置：①已自愈（重下在位·newest 09-29 19:59）②**在役注记建议**：ASR 产线窗口期（拆条/深纵收官腿）hf-cache 为活跃依赖·值守轮周扫执法按③冻结——随本回执呈集团
- 影响面：一轮首飞 FAIL+1.46GB 重下带宽·零成品损失

## 六、集团面观察行（非本司份额·呈值守轮不清决·跨域不执行）

- 用户级 `.codely-cli/tmp` = **14.8GB**（hash 名会话工作目录族·最大单目录 3.8GB）——disk-sweep 嫌疑面候选
- 用户级 `.codely-cli` 总 14.9GB（tmp 14.8+cache 53MB+mcp 25MB）

## 七、判级台账小结

| 对象 | 体积 | 判级 | 本轮动作 |
|---|---|---|---|
| `_trash-20260928` | 1.18GB | Class-A（auto-saves 暂存） | **直清 ✅** |
| auto-saves 活面三点 | 453MB | Class-A 类·水位线内 | 零动作 |
| renders 历史档 | 708MB | R3 | 建议面（开闸批） |
| bonsai | 6.1GB | 冻结③ | 零动作（10-09 窗） |
| footage R2 源 | 35.2MB | R2 | **登记入册 ✅** |
| hf-cache | 1.46GB | R3·在役③ | 冻结建议 |
| `.git` | 493MB | R1 | 零触碰 |

**清理实绩：1.18GB 直清（media/ 10.2GB→~9.0GB）**·后续周扫=值守轮周日步（disk-sweep.ps1 口径）·本件=本司 72h 窗回执载体
