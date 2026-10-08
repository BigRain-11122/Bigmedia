# MD 分镜表 Schema v0.1（#108 漫剧 PoC·T2I/TTS 双消费端规格）

> 剧本与分镜表一体化：一次模型产出的 JSON 同时是「剧本」（台词/时长/角色）与「分镜表」（逐镜视觉指示）。判据=**schema 无效率 ≤5%**（无效镜数/总镜数·#108 立项条款）。

## 顶层字段

| 字段 | 类型 | 约束 |
|---|---|---|
| title | string | ≤12 字 |
| logline | string | ≤30 字 |
| total_seconds | number | =sum(shots.seconds)·60-90 |
| characters | array | ≥3 项·见下 |
| shots | array | 10-14 项·见下 |

## characters 项

| 字段 | 类型 | 约束 | 消费端 |
|---|---|---|---|
| id | string | narrator/lamp/tower/cat（本件） | 全链主键 |
| name | string | 档案名 verbatim | 字幕/角标 |
| voice | string | 声线档描述 | CosyVoice3 多角色 TTS（声纹选档·D-BS/O-2136 主声线定档不变·配角多声纹=声音档位非人格新增） |

## shots 项

| 字段 | 类型 | 约束 | 消费端 |
|---|---|---|---|
| id | number | 1..N 连续 | 装配序 |
| scene | enum | open/lamp/tower/cat/close（幕序锁定） | 剪辑段 |
| seconds | number | 3-12·整数优先 | 时长轴（Σ=60-90） |
| visual | string | 主体/环境/光线/构图·具体可画 | T2I（bm-c ComfyUI·参照卡锚角色一致性） |
| camera | string | 镜头语言（远景/中景/特写/慢推…） | T2I+动效（Ken Burns 参数位） |
| speaker | enum | =characters.id | TTS 声道分配 |
| line | string | ≤40 字·引号金句=档案 verbatim | TTS 文本+字幕 |

## 无效率判据（机检口径）

- 无效镜 = 缺任一必填字段 / scene 越枚举 / speaker 未登记 / seconds 出界 / line 超长，任一即整镜计无效。
- 无效率 = 无效镜数 / 总镜数 ≤ 5%（10-14 镜容差 = 0 无效镜）。
- 顶层问题（镜数越界/总时长出界/声明 total ≠ Σ）= 整件 FAIL 不进无效率分母。

## 后续扩展位（v0.2 候选·本版不立）

- t2i 字段：prompt 种子/负面词/参照卡 ref id/风格档（T2I 腿实弹后按 bm-c 回执定形）
- tts 字段：韵律提示/emotion tag（CosyVoice3 装包后按实测定形）
