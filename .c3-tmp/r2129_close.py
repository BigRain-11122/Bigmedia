# -*- coding: utf-8 -*-
# R2129 close: state accounting via canonical single-writer (tech#76 finalize_state).
import sys

sys.path.insert(0, 'src/os')
from close_commit import finalize_state

LOG = (
    "2026-10-13 08:57 R2129: 实物=backlog #109 收口 [done]（下载+登记腿全链核毕：ollama list 四档活读在册"
    "〔qwen3.5:9b/9b-16k/27b-8k/14b-8k〕+pull log success 尾证+R1765/R1777/R1791 三轮回执链——"
    "27b 加载试跑=tech #1 A/B 承载〔GPU 独占窗〕+CosyVoice3 装包腿判负退役〔tech #2 R1828·资产转 dormant〕"
    "+bm-c 2.0 GGUF 腿已被 R1791 Qwen-Image-2.1 三件套演化收编·余活零）"
    "+#99 SLA ≤10-13 到期未达如实判读（腿② 通道探 10-13 08:5x 复测仍 No Unity Editor instances found"
    "=blocked-on-channel 维持+工作日零排单双卡·ETA 通道恢复后首个夜窗·HQ-FEEDBACK F-20261013-BS02 日清行已落）；"
    "五查静=own orders 锚 O-20261008-1105 维持+origin_gap QUIET ahead0 behind0（R1500 前置位）"
    "+group_scan fresh 08:43（DECISIONS truly_new=0 水位 154·LEDGER @BigStream 5==锚·ORDERS rows 341 tail '10-13 04:3x'==水位）"
    "+树=MV-lane 预期脏维持（mv0001/mv001 M+?? 承继 R1745 零接触）+无 index.lock；"
    "探针=board 0 FAIL（5 意 10 帖·5 in production）/readiness 3 blocker 全外部面（账号 11 平台+M4 6/10+#17 needs-CEO）"
    "+1 finding=render-unannot react-v16 预期红（F-183 登记即清维持）/loop_health 3F+286W 全历史 outage 实体+drift 18 已裁决维持；"
    "队列盘点=main 2 gated 前进（#7 手动窗+#27b GPU 车占位）/tech 1 gated（#126 tech#92 窗 10-14 08:00 锁）/explore 0"
    "/backlog claimable 9 逐项裁=全 gated 或他窗 lane（#111 MV 零接触/#112 tech#92 窗/#106 留痕行/#109 本轮 [done] 收口"
    "/#110 装机夜窗位〔#108 已收官条件已升〕/#70 72h 收获 10-12 已交下窗 ≤10-15/#59/#63/#67 fire 窗 F 票族/#31 render 窗/#15 陈案待裁）"
    "——工作日窗无可领活=等待态收轮（waiting: 工作日零排单窗+全队列 gated·ETA 10-14 00:00 夜窗〔撤 AIHOT 旗+main#21 重启"
    "+F-180~183 fire 接力+tech#126 校准〕/10-14 08:00〔tech#92/#126 权威窗〕）；"
    "export=skip（R2128 08:40 canonical writer 刷新龄 ~17min·无实况变化 ≤24h 律）；"
    "补货步=真无新种子如实注记（group 静+探针稳+提案轨 P-7 W42 在位·#99 SLA 逾期由 HQ 日清行承载非新队项）；tokens:local=0。"
)

FOCUS = (
    "工作日零排单窗等待态（08:00-23:59·O-20261012-1505）：下扫描点=10-14 夜窗 00:00"
    "（撤 AIHOT pause 旗+worker-restart main#21+F-180~183 fire 接力+tech#126 校准冒烟）"
    "+10-14 08:00 tech#92/#126 权威窗；#99 SC-003=通道仍断（10-13 08:5x 复测 No Unity Editor instances found）"
    "·SLA 逾期如实注+HQ F-20261013-BS02 已落·ETA 通道恢复后首个夜窗；#109 已 [done] 收口（余活=tech #1 A/B 承载）；"
    "main#28 DIGEST-v20 gated 维持；react-v16 unannot=F-183 登记即清；watermark 154/341 静；"
    "台词池 gate locked 复读 ≥10-17；close export 一律走 canonical writer/export 参（tech#148 强制律）"
)

if __name__ == '__main__':
    r = finalize_state(LOG, ts="2026-10-13 08:57:30", focus=FOCUS, tick=2129)
    print("FINALIZE_OK:", {k: r.get(k) for k in ("tick", "ts", "task")})
