# -*- coding: utf-8 -*-
# R2212 close: tech#152 Toonflow ComfyUI adapter leg delivered (contract self-check + bun smoke + app import).
# finalize_state (tech#76/tech#149 single-writer law) + run_close_commit (tech#65) with tech#148 export writer.
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src", "os"))
# repo-root relative for direct run: .c3-tmp/ -> repo root is two levels up
sys.path.insert(0, r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os")

import close_commit

LOG_LINE = (
    "2026-10-14 03:15 R2212: 实活轮（夜窗 00:00-08:00·CPU 面）——tech#152 Toonflow ComfyUI 适配 .ts 手写腿当轮双达成"
    "（R2211 下轮指针兑现）：①正身落 tools/toonflow/comfyuiLocal.ts（10,125B·Qwen-Image-2.1 API 工作流全嵌〔runner_r1792 谱系〕"
    "+单模型 mode:[text]+imageRatios 五档 16:9→1216×688+/prompt→/history 轮询〔AbortSignal.any 20min 总超时+取消仅 /queue delete "
    "自家 promptId 禁 interrupt 禁清队〕+/view url 返回+rules:[] 无鉴权+127.0.0.1:8188 字面量+中文可读错误全抛）"
    "——判据①契约自检 33/33 PASS（字符串感知注释剥离检查器：字面量/无 import/无禁全局/保留名/方法 this 绑定/文件名=id+.ts）"
    "+Bun 原生解析冒烟形状全对（id=comfyuiLocal/version=2.0.0/rules=[]/单模型/generateImage=function）；"
    "②导入成功=设置→模型→媒体模型→添加自定义供应商→「粘贴代码」通道 CDP 全自动（填充 10,125 字符回读一致→确定→"
    "卡落位「ComfyUI 本地（Qwen-Image-2.1）/comfyuiLocal.ts/v2.0.0/1 个模型」·抽屉关开重进复核持久化在位）"
    "——同名双按钮勘定：语言模型段表单流〔LEG-2 族〕vs 媒体模型段 .ts 导入流=判据② 正身通道；"
    "③1 帧真实产出=VRAM/MV 窗后·归 tech#151 ③ 全链腿承载（判据同面不双记）；"
    "④轮首五查全静=group_scan 六面 fresh 02:33 全静（DECISIONS truly_new=0 水位 155+LEDGER @BigStream 5 行值守锚零新转办"
    "+ORDERS rows=382 tail '10-13 23:5x'==stored+ORIGIN-DELTA delta=0+DIGEST-SUPPLY quiet）+origin_gap_check QUIET ahead0 behind0"
    "+own orders 锚 O-20260908-1105 mtime 10-08 12:08 维持+树=MV-lane 预期脏面零锁（R1745 零接触承继）；"
    "⑤三探针带内=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）"
    "+2 发现 react-v16/digest-v20 unannot=F-183/184 fire 窗登记即清预期态（R2118 裁定维持）/loop_health 3F+296W 皆在案史实"
    "（三 outage 窗+drift 20≤21 adjudicated）；⑥fire_consume --launch sc005-07 s1_call.py --ledger=no-fire rc1 "
    "reason=card-no-fire: gate-credit-no-go;util-face: worst-case util 97%>gate 80%（03:0x 收据·ledger 行随本 commit 入账）"
    "→F-180 SC-005-07 flight-4+F-181 REACT-v15+F-182 DIGEST-v19+F-183 REACT-v16+F-184 DIGEST-v20 五件 fire-ready carried"
    "（真窗=util/VRAM 门开·fire_window_card 唯一仲裁面）；⑦main#32 守望=V3 成片未落位维持（本轮零重扫=fire 卡自带 mv probe 面）；"
    "⑧例行件=10-14 日报在案不重跑（R2205 补产·一份为真相）·W42 周审在案（R2011）·GB §④ 下期 10-15 ≤7d 跳过"
    "+export=本轮实物交付走 tech#148 canonical writer 正身刷（do/results/live 三面·新实物=适配器+导入落位）"
    "·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·T1 催办无超线项（账号物理件=呈现状行不催办）"
    "·tokens:local=0（契约检查/CDP 驱动/bun 冒烟=档案读写+UI 自动化零本地模型产出调用·P-54⑤ 计量律）；"
    "⑨队列补货步=tech#153 真种子 1 条（toonflow_cdp import 子命令固化·R2212 导入工艺散化真发现驱动）"
    "·临时件清理钩=r2212_* 五件轮末删净+close 脚本 tech#81 自含律随 manifest——"
    "下轮=main#32 守望续+fire 接力（F-180→184·util/VRAM 门开即发）+08:00 tech#92/#126 权威窗读数"
    "+晨窗回滚序（re-enable MiniGameOllama 双任务+LEG-3 未毕收 app 窗口位）"
)

FOCUS = "tech#153 cdp import cmd + 08:00 tech#92/#126 window + fire relay on util/VRAM open (R2212)"

close_commit.finalize_state(LOG_LINE, ts="2026-10-14 03:15:00", focus=FOCUS)

EXPORT_PATCH = {
    "do": "R2212 夜窗实活轮：tech#152 Toonflow ComfyUI 适配器手写+导入双达成（tools/toonflow/comfyuiLocal.ts v2.0.0·Toonflow 媒体供应商卡落位）——LEG-3 剩 LLM 腿+测试帧双 VRAM 门控；F-180~184 结转",
    "results": [
        ["comfyui adapter imported", "r2212"],
        ["r977 viewlog ok", "r2206"],
        ["v20 CPU leg done", "r2205"],
        ["fire no-fire x5", "f180"],
        ["row 382 ack", "orders"],
    ],
    "live": [
        "当前活：Toonflow 本地画图链适配毕（comfyuiLocal.ts 已入 Toonflow 供应商库）；夜窗算力让路中，fire 五件候门",
        "最近实物：tools/toonflow/comfyuiLocal.ts（Qwen-Image-2.1 文生图适配器·Toonflow 导入 v2.0.0 卡在位·契约自检 33/33）2026-10-14 03:1x",
        "下个里程碑：明早八点读城市日报评分结果（tech#92/#126 权威窗）；util/VRAM 门开后 Toonflow 全链 1 帧实测出片",
    ],
}

FILES = [
    "tools/toonflow/comfyuiLocal.ts",
    "state/queue/tech.md",
    "src/os/backlog.md",
    "src/os/state.json",
    "docs/status-export.json",
    "data/pipeline/fire-consume-ledger.jsonl",
    "data/pipeline/aihot-watchdog-ledger.jsonl",
    "data/pipeline/aihot-watchdog-state.json",
]

rc, lines = close_commit.run_close_commit(
    FILES,
    "R2212 tech#152: comfyuiLocal.ts adapter delivered (contract 33/33, bun smoke OK, Toonflow import persisted) [via bm-a]",
    export_patch=EXPORT_PATCH,
)
for ln in lines:
    print(ln)
print("RC=%d" % rc)
