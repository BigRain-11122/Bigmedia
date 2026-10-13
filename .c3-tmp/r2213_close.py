# -*- coding: utf-8 -*-
"""R2213 accounting close (tech#149 finalize_state + tech#148 export writer)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "src", "os"))
from close_commit import finalize_state, run_close_commit

LOG_LINE = (
    "2026-10-14 03:1x R2213: 实活轮（夜窗 00:00-08:00·CPU 面）：tech#153 交付——tools/toonflow_cdp.ts 新增 import 子命令"
    "（R2212 五步散化面工艺沉淀为一命令复用）：陈旧对话框先关〔防上次残窗〕+幂等前置查〔供应商 list 含 <id>.ts 即 no-op〕"
    "→添加自定义供应商→粘贴代码通道→textarea 原生 setter+input 事件填装→确定→面板回读 12×500ms 轮询；"
    "+--dry 旗〔全机械链跑至填装后点取消=机制验证零安装〕；实测三绿=①幂等路 import comfyuiLocal.ts→"
    "「no-op: comfyuiLocal already installed」（回归复测同判）②dry 路 cdpDryRunTest 改名副本→「DRY-OK: filled 10126 chars, "
    "canceled before confirm」（对话框开/粘贴通道/填装/取消全链）③终态核验=对话框关+cdpDryRunTest 未入册+四供应商卡在位零污染；"
    "坑入账=python text 模式写盘 Windows 侧 \\n→\\r\\n 翻译+bun readFileSync 保留 \\r+浏览器 textarea 填装 CRLF→LF 规范化"
    "=字符数比对必炸（237 行差）→工具内 readFileSync 后统一 replace(/\\r\\n/g,/\\n/) 根修（与 R2212 手动装结果同态）；"
    "bun 非本机 PATH（ToonFlow 捆绑位 bin/bun.exe）=工具头注释已记；tech#154 补货（Toonflow 媒体模型选择器自动化·LEG-3 ③前置位）；"
    "六面静=own orders 锚 O-20260908-1105 mtime 10-08 12:08 维持+origin_gap_check QUIET ahead0 behind0"
    "+group_scan 模块 fresh 03:0x 全静〔DECISIONS truly_new=0 水位 155 维持+LEDGER @BigStream 5 行值锚零转办"
    "+ORDERS rows=382 tail '10-13 23:5x'==stored+DIGEST-SUPPLY quiet+ORDERS-ORIGIN-DELTA delta=0〕；"
    "实况=MV-lane 预期静默态 bm-a 写盘维持（R1745 接触器判 bm-a 活跃写盘迹象·写区零接触）；"
    "三探针=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）"
    "+2 发现 react-v16/digest-v20 unannot=F-183/184 fire-ready 预期态（R2118 判定维持）/loop_health 3F+297W 皆在案史实"
    "（outage adjudicated 域+drift 20↔21 adjudicated+新 1=密集窗 20-35min gap 同族）；"
    "fire 门=VRAM 饿空维持关（03:0x 实测 free ~530MB<guard 2048+util 100%）→F-180 SC-005-07 flight-4+F-181 REACT-v15"
    "+F-182 DIGEST-v19+F-183 REACT-v16+F-184 DIGEST-v20 五件 fire-ready carried 维持（fire_window_card 唯一插部位）；"
    "main#32 议题=V3 成片仍未到位维持（kf-demo 顶记录 23:57 r977 fix3 维持·查看位接触维持）；"
    "例行件=10-14 GB 基准刷新在案（R2205 席位）+W42 周审在案（R2011）"
    "+export=实况变化 canonical writer 刷新（live/do/results 面·tech#148 强制律如实执·本轮交付件入 results）"
    "+HQ-FEEDBACK 不写（无集团层 open 问题）+T1 催办剔除维持（账号物理件=呈现状行不催办）"
    "+tokens:local=0（CDP 探针/直调=纯本地面板不算计量·P-54⑤ 计量律如实记）；"
    "临时件清理=r2213_dry_adapter.ts/r2213_cdp_check.txt/toonflow_cdp_result.txt 轮末删净（实测归零）+r2212_close.py 删除收口维持；"
    "下一锚=08:00 tech#92/#126 权重窗开（夜窗 gated 解除）+fire relay on util/VRAM 开+恢复回滚 re-enable MiniGameOllama 双任务"
    "+LEG-3 未毕收 app 窗口位"
)
summary = finalize_state(
    LOG_LINE,
    focus=("08:00 tech#92/#126 window + fire relay on util/VRAM open + "
           "main#32 follow + rollback re-enable at 08:00 (R2213)"),
)
print(summary)

EXPORT_PATCH = {
    "live": [
        "当前活：夜窗收尾，Toonflow 适配器 import 子命令已固化（幂等+--dry 三绿），候 08:00 权重窗/VRAM 开窗接力。",
        "最近实物：tools/toonflow_cdp.ts import 模式（对已装适配器 no-op 幂等·--dry 机制链 10126 字符实测），2026-10-14 03:1x。",
        "下个里程碑：08:00 tech#92/#126 权重窗执行；fire 五件 F-180~184 候 util/VRAM 开窗发射；V3 成片 main#32 跟进。",
    ],
}
EXPORT_DO = ("R2213 夜窗实活轮：tech#153 交付 toonflow_cdp.ts import 子命令（幂等 no-op+--dry 机制链三绿+终态零污染"
             "+CRLF 规范化坑根修）；tech#154 补货（模型选择器自动化）；fire 门 VRAM 饿空维持 F-180~184 carried；"
             "main#32 未落维持；六面静。")

rc, lines = run_close_commit(
    files=["src/os/state.json",
           "tools/toonflow_cdp.ts",
           "state/queue/tech.md",
           ".c3-tmp/r2213_close.py"],
    message=(
        "R2213: active round - tech#153 delivered: toonflow_cdp.ts import "
        "subcommand mechanizes the custom-provider install (idempotent no-op "
        "on installed adapter, --dry mechanics chain validated DRY-OK 10126 "
        "chars canceled-before-confirm, app state clean zero pollution; "
        "CRLF textarea-normalization pit root-fixed via readFileSync "
        "normalize; bundled-bun path noted in header); tech#154 seeded "
        "(media model picker automation, LEG-3 precondition); six faces "
        "quiet; VRAM starved (free ~530MB, util 100%) F-180..184 carried; "
        "main#32 film still not landed; next=08:00 tech#92/#126 window + "
        "fire relay on util/VRAM open [via bm-a]"
    ),
    export_patch=EXPORT_PATCH,
    export_do=EXPORT_DO,
)
for line in lines:
    print(line)
print("RC=%d" % rc)
sys.exit(rc)
