# -*- coding: utf-8 -*-
"""R2204 close: dead-attempt resume round. Toonflow #110 LEG-2 closed (provider
Ollama Local + 3 models via CDP automation), ollama serve restored, fire
carried (card no-go: mv-active + VRAM class), driver promoted to
tools/toonflow_cdp.ts, r2204/r2203 debris cleaned."""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join("src", "os"))
import close_commit as cc  # noqa: E402
import group_scan  # noqa: E402

# ---------- 1) backlog #110 progress note (insert before "112." item) ----------
BL = os.path.join("src", "os", "backlog.md")
with open(BL, "r", encoding="utf-8") as f:
    bl = f.read()

NOTE = (
    "\n   **[R2204 进展 2026-10-14]**：**LEG-2 UI 端点配置收口**（前 R2204 实体 23:28-23:34 死于 CDP 中途·"
    "tick 停 2203·本实体重开续跑同轮号）——①死因修复实录：r2204_cdp.ts evalfile 路径 `const mode` 重赋值炸（改 let）"
    "+模型勾选 pick.js 从未执行（写盘 23:34:30 死于 run 前·结果文件 mtime 23:33:11 早锚）；"
    "②Toonflow app+CDP 9222 跨进程存活（launcher+bun 23:29 起）→续流程=勾选 3 模型→确定添加供应商→"
    "card 落位 Ollama Local/ollama（0 个模型）→编辑框核验端点 http://localhost:11434/v1 保存正确→"
    "「获取模型列表」二跑报 Unable to connect（Ollama serve 母进程 23:49 后死·两 runner 孤儿·11434 空听）→"
    "改走「手动添加模型」三行（qwen2.5:14b-8k/qwen3.5:9b-16k/qwen3.8:27b-8k）+删空行+保存修改→"
    "**card=Ollama Local/ollama·3 个模型=配置面毕**（端点连通证据=23:33 首取 10 模型在案〔前实体 LEG-1〕）；"
    "③ollama serve 已复活（Start-Process hidden·/v1/models HTTP 200·10 模型=零 VRAM 监听面·夜窗 fire F-180 "
    "LLM 栈依赖位+LEG-3 依赖位就绪）·孤儿 runner×2（23:48:42/59 派生·母 PID 123396 已死）不杀=他窗产物零接触注记；"
    "④**剩余=LEG-3 漫画工作台全链实测**（需 ollama 模型加载过 VRAM 门+图像后端配置〔ComfyUI 网关=R1774 bm-c lane "
    "预核注记·本机 8188=MV 会话共享域勿抢〕）+驱动正身升格 tools/toonflow_cdp.ts（LEG-3 复用面·"
    "CDP 自动化替代一次性人工预言点·app 存活中 CDP 9222 可直连）——夜窗装机器位继续按认领制随轮领做\n"
)

anchor = "\n112. **雷达日报"
assert anchor in bl, "backlog anchor (112 radar item) not found"
if "R2204 进展 2026-10-14" not in bl:
    bl = bl.replace(anchor, NOTE + anchor, 1)
    with open(BL, "w", encoding="utf-8", newline="") as f:
        f.write(bl)
    print("backlog note inserted")

# ---------- 2) tech queue replenish (tech#151) ----------
TQ = os.path.join("state", "queue", "tech.md")
with open(TQ, "r", encoding="utf-8") as f:
    tq = f.read()
ITEM = (
    "\n\n151. [R2204 补货·真种子] **Toonflow LEG-3：漫画工作台全链实测**（backlog #110 收尾腿·夜窗机器位线）："
    "①Toonflow 内新建项目选 Ollama Local 供应商跑一次剧本/分镜生成（LLM 腿端到端·模型加载过 VRAM 门=" 
    "fire_consume load-class 同门）②图像后端配置位调研（ComfyUI 网关=bm-c lane 预核·本机 8188=MV 会话共享域勿抢）"
    "③全链 1 条测试出片——判据=LLM 脚本生成返回非空+至少 1 帧图像产出；图像后端缺口=如实记录位不清零"
    "——驱动正身=tools/toonflow_cdp.ts（R2204 升格·app 存活 CDP 9222 可直连·若 app 已死按工具头注释重启带 CDP）"
    "——晨窗 08:00 CEO 复机前 LEG-3 未毕=回滚序注记收 app 窗口位\n"
)
if "tech#151" not in tq and "Toonflow LEG-3" not in tq:
    if not tq.endswith("\n"):
        tq += "\n"
    tq += ITEM
    with open(TQ, "w", encoding="utf-8", newline="") as f:
        f.write(tq)
    print("tech queue item appended")

# ---------- 3) debris cleanup (cleanup hook) ----------
DEBRIS = [
    ".c3-tmp/r2204_cdp.ts", ".c3-tmp/r2204_pick.js", ".c3-tmp/r2204_t110_cdp.py",
    ".c3-tmp/r2204_cdp_result.txt", ".c3-tmp/r2204_cdp_http.txt",
    ".c3-tmp/r2204_out.txt", ".c3-tmp/r2204_ollama_probe.json",
    ".c3-tmp/r2203_close.py",
]
removed = []
for d in DEBRIS:
    if os.path.exists(d):
        os.remove(d)
        removed.append(os.path.basename(d))
print("debris removed:", removed)

# ---------- 4) state finalize ----------
LOG = (
    "2026-10-14 00:1x R2204: 死轮重开+夜窗实件轮（前 R2204 实体 23:28-23:34 死于 #110 CDP 中途·"
    "tick 停 2203·本实体重执同轮号）——①五查静=group_scan fresh 23:50 全静（DECISIONS truly_new=0 水位 155 维持"
    "+ORDERS rows=381 tail==stored+LEDGER @BigStream 5 行值守锚零新转办+DIGEST-SUPPLY advisory 1 age0d 已裁决面维持"
    "+ORIGIN-DELTA delta=0）+origin_gap_check QUIET ahead0 behind0+own orders 锚维持；"
    "②取活=backlog #110 Toonflow LEG-2 续作（R2200 起夜窗装机器位·前实体遗留活）=死轮现场复活实录："
    "app+CDP 9222 跨进程存活（launcher+bun 23:29 起）·前实体死因实证=cdp 驱动 evalfile 路径 const 重赋值炸（改 let 修）"
    "+pick.js 写盘后死于 run 前（mtime 锚证）→本实体续跑=勾选 3 模型→确定添加供应商→card 落位但 0 模型→"
    "编辑框核验端点 http://localhost:11434/v1 保存正确→获取模型列表二跑 Unable to connect"
    "（ollama serve 母进程 23:49 后死·两 runner 孤儿·11434 空听）→改走手动添加模型三行"
    "（qwen2.5:14b-8k/qwen3.5:9b-16k/qwen3.8:27b-8k）+删空行+保存修改→**card=Ollama Local/ollama·3 个模型="
    "LEG-2 UI 端点配置毕（R1774 一次性人工预言点全自动化落账·端点连通 10 模型证据在案）**；"
    "③服务面=ollama serve 复活（Start-Process hidden·HTTP 200·10 模型·零 VRAM 监听面=夜窗 fire F-180 LLM 栈依赖位"
    "+LEG-3 依赖位就绪）·孤儿 runner×2（23:48:42/59 派生·母 PID 123396 已死）不杀=他窗产物零接触注记；"
    "④fire 面=fire_window_card 00:0x 读数 reasons=mv-active+load-class free_for_class=512MB ok=False"
    "（MV sprint 会话 00:0x 复活中·newest_age 2.8min+GPU 已载）=双门 no-go 正确侧→"
    "fire_consume 收据 rc1 card-no-fire: mv-active·F-180~183+DIGEST-v20 fire-ready carried"
    "（真窗=card 唯一仲裁面）·下轮 mv 静+VRAM 门开即接力；⑤三探针=board 0 FAIL（5 题 10 稿 5 in production）/"
    "readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）+1 发现 react-v16 unannot=F-183 夜窗登记即清"
    "（R2118 维持）/loop_health 3F+293W 皆在案史实（state-ts-stale 项本轮收账 ts 刷新即清）；"
    "⑥例行=10-13 日报在案不重跑（R2086 一份为真相）·W42 周审在案（R2011）·GB §④ 10-15 ≤7d 跳过"
    "+export=实况变化（LEG-2 实物收口）走 tech#148 正身刷新·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）"
    "·tokens:local=0（探针/CDP 驱动/serve 复活=零本地模型产出调用·P-54⑤ 计量律）；"
    "⑦补货步=tech 队 +1 真种子（tech#151 Toonflow LEG-3 工作台全链实测+图像后端配置位）"
    "+临时件清理钩=r2204_* 七件+r2203_close.py 前轮残件轮末删净+CDP 驱动升格 tools/toonflow_cdp.ts"
    "（LEG-3 复用正身·入账收口）——下轮=MV 让位即 fire 接力（F-180~183+DIGEST-v20 产线）"
    "+10-14 08:00 tech#92/#126 权威窗读数+晨窗 08:00 回滚序（re-enable MiniGameOllama 双任务+LEG-3 未毕收 app 窗口位）"
)

FOCUS = ("MV-yield fire relay (F-180~183 + DIGEST-v20 line) + 10-14 08:00 tech#92/#126 "
         "authoritative window read + morning rollback (re-enable MiniGameOllama tasks; "
         "close Toonflow app window if LEG-3 not done) + Toonflow #110 LEG-3 workbench "
         "full-chain test (GPU/VRAM-gated)")

EXPORT_PATCH = {
    "do": ("R2204 夜窗实件轮：Toonflow #110 LEG-2 收口——本地 Ollama 供应商+3 模型经 CDP 全自动化配置落位"
           "（一次性 UI 人工预言点自动化·端点连通 10 模型在案）；ollama serve 复活（夜窗 fire F-180 LLM 栈依赖就绪）；"
           "fire 四件候 MV sprint 让位（card 双门 no-go）。"),
    "live": [
        "当前活：夜窗装机器位——Toonflow #110 LEG-2 收口（供应商+3 模型落位）；L 卡四件 fire 候 MV sprint 让位（双门 no-go）。",
        "最近实物：tools/toonflow_cdp.ts（CDP 自动化驱动正身·10-14 00:1x）+ Toonflow 供应商配置落位（Ollama Local·3 模型·ollama serve HTTP 200）。",
        "下个里程碑：MV 让位后 F-180~183 fire 接力+DIGEST-v20（窗 ≤10-15）；10-14 08:00 tech#92/#126 权威窗读数。",
    ],
}

MESSAGE = ("R2204: resume dead-attempt round -- Toonflow #110 LEG-2 closed (provider "
           "Ollama Local + 3 models qwen2.5:14b-8k/qwen3.5:9b-16k/qwen3.8:27b-8k configured "
           "via CDP automation, one-time UI manual point now automated+audited, endpoint "
           "connectivity 10-model fetch banked); fixed prior attempt driver const-reassign "
           "bug; ollama serve restored (HTTP 200, zero-VRAM listener, fire F-180 dep ready); "
           "fire no-fire rc1 card-no-fire mv-active + VRAM class gate 512MB (F-180~183 "
           "carried, card sole arbiter); driver promoted tools/toonflow_cdp.ts; tech#151 "
           "LEG-3 queue seed; r2204/r2203 debris cleaned; next: MV-yield fire relay + "
           "08:00 tech#92/#126 window + morning rollback [via bm-a]")

FILES = ["src/os/state.json", "src/os/backlog.md", "state/queue/tech.md",
         "tools/toonflow_cdp.ts", "data/pipeline/fire-consume-ledger.jsonl"]

sumry = cc.finalize_state(LOG, ts="2026-10-14 00:19:00", focus=FOCUS,
                          orders_watermark=group_scan.current_orders_watermark())
print("finalize:", sumry)

rc, lines = cc.run_close_commit(FILES, MESSAGE, export_patch=EXPORT_PATCH)
for l in lines:
    print(l)
print("close rc:", rc)

# self-cleanup last (post-commit; not in FILES)
try:
    os.remove(__file__)
    print("close script self-removed")
except OSError as e:
    print("self-remove skipped:", e)
sys.exit(rc)
