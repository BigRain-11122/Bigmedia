# R1903 closing stage: state accounting + export refresh + embedded close commit.
# Family convention (tech#27 two-stage + tech#65 embedded commit + tech#67 pycache
# purge step). ASCII script body per the encoding rule; CJK only in data payloads.
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "src" / "os" / "state.json"
EXPORT = ROOT / "docs" / "status-export.json"

NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

LOG = ("2026-10-10 19:3x R1903: 生产轮·tech#69 export_ts 时戳守卫交付（O-20261009-1246 取活·"
       "R1902 种子兑现·两段制收账=交付段先行 commit b671f974）"
       "——①轮首五查全静=own orders 顶 O-20260908-1105 mtime 12:08:14==R1733 锚零新令"
       "+origin_gap_check QUIET ahead0 behind0（R1500 前置位）+group_scan 固定探针三面静"
       "（decisions dnum 内容寻址差集 truly_new=0 水位 131 维持+ledger @BigStream 4 行==值守锚零新转办"
       "+HQ orders 18:54:32==R1902 消费锚零新行）+无 index.lock+树态=mv0001/mv001/whisper v3/drama_takt "
       "bm-a MV sprint 会话批域在飞件零接触（R1745 承继·tech#26 撞面维持）；"
       "②时间闸与窗=C-37 fresh 判读 NO-GO 双面齐触（pause_face 任务态指纹 8/8 Disabled=CEO 让路令在役"
       "+vram_face free 451MB<9216 守卫）→四腿（MD-0002 剧本腿/DIGEST v17 M4.5·E4/F-170 S1/"
       "tech#43 E4 v13）维持 fire-ready gated（材料 R1870/R1871/R1875 turnkey）+ollama 探针 --ledger="
       "rc2 TimeoutError face=busy-contended gpu_util 100/gpu_mem 11858（MV 会话生成满载窗=让路面判读"
       "·face 框架 tech#55 正用=不升级行）+#112 城市口径判据窗 10-11 08:00 未到（~13h）+"
       "#111/#115 查看位=R1902 锚（19:1x）三分钟前刚扫禁重扫跳过；"
       "③tech#69 交付=**export_ts 时戳守卫双候选腿全落**——〔腿一 ts 源考古定谳〕git show ccee6bfc:src/os/state.json"
       "+9e6a6516:docs/status-export.json 双证：R1901 close state.ts=18:58:00（真实钟）≠export_ts=19:05:00"
       "（写入时刻 18:49:42 未来 15min）→值既非取自 state 面亦非取自写入钟=**写入脚本预估值/硬编码面缺陷**"
       "（脚本已随清理钩删=durable 修法走守卫面·「根因未定位」勘正收口）；〔腿二守卫面〕loop_health 新 "
       "_export_ts_face 纯核三面（缺失/畸形/不可解析=export-ts WARN〔P-61 必填字段〕+未来戳=export-ts-future "
       "双比对〔vs 文件 mtime=任意后探针持久判 R1901 锚形+vs 探针钟 ±5min=cross_check state-ts 同法〕"
       "+滞后=export-ts-stale 双比对〔vs mtime >60min=写入器拷陈值+vs 钟超 24h=P-61 刷新律〕·一面一 WARN 顾问级）"
       "+classify_export_face 增 now/mtime 可选参（纯调缺省=零时钟比对·存量调用面零动）+check_export_face "
       "接线（datetime.now()+path.stat 双输入）·11 新测（ExportTsFaceTests：R1901 锚 mtime 复现点名+probe 钟面"
       "+±5min/60min/24h 三边界严格+陈值拷贝+24h 律+坏形四例+空白垫 strip 同 state-ts+纯调零时钟静默"
       "+check 面未来戳/缺 ts 双接线）+随批三测适配（CONTRACT_EXPORT 补 export_ts=契约正身+ANCHOR 注入 ts=实锚同构"
       "+真仓冒烟容差注=24h 律一面墙钟依赖归活探针）+首跑自检揭锚错位一轮内咬住（test_check_face_missing_ts_named "
       "CONTRACT_EXPORT 已含 ts=剥键复验）·**741 全回归绿 104.5s rc=0**（730+11·run_suite 正法）"
       "——判据双过=①R1901 锚形 fixture 复现点名（单测锁）②真仓零发现（probe_capture r1903_probes.txt "
       "零 export-* 行=新面首战静默 PASS）·C-20 v1.76；④队列补货步=tech#70 种子（tech#69 考古真发现="
       "导出刷新无单一真相写入器·ad-hoc 手搓世代〔r1876_export/r1902_close〕为 R1901 预估值缺陷生成土壤·"
       "候选=src/os/export_refresh.py 正典写入器 live-clock ts+写前契约自检）✓；⑤三探针=probe_capture "
       "单调消费（board 0 FAIL〔5 题 10 稿 5 in production〕/readiness 3 阻塞皆外部 CEO 面〔账号批次①+M4 GATE "
       "6/10+#17 needs-CEO〕0 发现〔78 renders 全注账 unannot=0〕/loop_health 2F+225W 皆在案史实"
       "〔两 outage 09-26/09-28 已裁定不重触发·drift +17==R1865 基线 21 带内〕）；⑥例行件=10-10 日报在案不重跑"
       "（R1845 00:03 一份为真相）·W41 周审在案 W42 件 10-12 未到·GB §④ v1.3 下期 10-15 跳过·#99 blocked-on-channel "
       "维持（SLA ≤10-13）·15:07 盘燃=R1825 已点名毕不重扫·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）"
       "·tokens:local=0（纯探针+工程+套件跑零本地模型产出调用·P-54⑤ 计量律）——下轮=R1904 快速路径首查"
       "（10-11 08:00 #112 城市口径判据窗届日即领〔城市源 ≥60 ≥2 件+tech#53 双新源流量首报+failed 尾读数〕"
       "+GPU 窗 C-37 fresh 四腿判断+meme V1 成片/krea2 查看位随轮盯+P2 队头 tech#70 候选）")

LOG_PREFIX = "2026-10-10 19:3x R1903: "

FOCUS = ("R1904 快速路径首查（10-11 08:00 #112 城市口径判据窗届日即领+GPU 窗 C-37 fresh 四腿判断"
         "+meme V1 成片/krea2 查看位随轮盯+tech#70 P2 队头候选）")

# ---- state.json accounting -------------------------------------------------
state = json.loads(STATE.read_text(encoding="utf-8-sig"))
assert state["tick"] == 1902, "unexpected tick %r" % state.get("tick")
state["tick"] = 1903
state["focus"] = FOCUS
log = state["log"]
assert isinstance(log, list)
log.append(LOG)
state["log"] = log
state["ts"] = NOW
state["task"] = LOG[len(LOG_PREFIX):][:60]
STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1) + "\n",
                 encoding="utf-8")

# ---- export refresh (P-61 step; live-clock ts per the tech#69 fix) -----------
export = json.loads(EXPORT.read_text(encoding="utf-8-sig"))
export["export_ts"] = NOW  # live clock at write time (R1901 estimate defect dead)
export["do"] = ("AI 媒体产线量产开闸运转·OS 循环 R1903；tech#69 export_ts 守卫交付；"
                "meme V1《慢慢踩》生产在飞；发布锁账号物理件")
for dept in export["depts"]:
    if dept.get("n") == "工程技术部":
        dept["t"] = ("741 测试全绿（105s）；S2 三门机检+守卫面族 20+ 在役（export-ts 新）；"
                     "收账链 close_commit 内嵌（tech#65/67）")
export["outs"][0] = ["R1903 tech#69 export_ts 守卫（741 测绿）", "on", "os-loop"]
if len(export["outs"]) > 1 and export["outs"][1][2] == "export-face":
    export["outs"][1] = ["导出面 v6.2 契约+export_ts 守卫在役（live 面双保险）",
                         "on", "export-face"]
for chip in export["chips"]:
    if chip[0] == "730 测绿":
        chip[0] = "741 测绿"
for res in export["results"]:
    if res[0] == "730":
        res[0] = "741"
    if res[0] == "1902":
        res[0] = "1903"
export["live"] = [
    "当前活：R1903 tech#69 export_ts 时戳守卫面交付（loop_health export-ts 三码+11 测·"
    "741 全回归绿 104.5s）+五查静（HQ 18:54:32 锚平·decisions 水位 131 平）+GPU 窗 C-37 NO-GO 维持"
    "（pause 指纹 8/8+free 451MB·四腿 fire-ready gated）",
    "最近实物：src/os/loop_health.py export-ts 检测面（commit b671f974）+R1901 ts 源考古定谳"
    "（state.ts 18:58:00≠export 19:05:00=写入器预估值·根因收口）+查看位：30s_reel_v4.mp4 成片"
    "（18:23·CEO 终裁毕·krea2/30s-reel-v1 批）+meme V1 生产在飞（#115）",
    "下个里程碑：①10-11 08:00 #112 城市口径判据窗验收（城市源 ≥60 ≥2 件+tech#53 双新源流量首报）"
    "②GPU 窗 C-37 fresh（pause 解除即四腿开窗：MD-0002 剧本/DIGEST v17 M4.5·E4/F-170 S1/tech#43 E4 v13）"
    "③meme V1 成片到件随轮盯（#115）",
]
EXPORT.write_text(json.dumps(export, ensure_ascii=False, indent=1) + "\n",
                  encoding="utf-8")

# sanity: the tech#68/#69 guard faces must be silent on the refreshed export
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "os"))
import loop_health  # noqa: E402
data = json.loads(EXPORT.read_text(encoding="utf-8-sig"))
violations = loop_health.classify_export_face(data)
assert violations == [], "refreshed export violates contract: %r" % violations
print("state tick=1903 ts=%s" % NOW)
print("export contract: silent PASS (%d chars do)" % len(data["do"]))

# ---- embedded close commit (tech#65) ---------------------------------------
CLOSE_FILES = [
    "src/os/state.json",
    "docs/status-export.json",
    ".c3-tmp/r1903_probes.txt",
    ".c3-tmp/r1903_suite.result",
    ".c3-tmp/r1903_close.py",
]
CLOSE_MSG = ("R1903 closing: state tick 1903 + export refresh (live-clock ts) + "
             "probe/suite evidence [via bm-a]")
proc = subprocess.run(
    [sys.executable, str(ROOT / "src" / "os" / "close_commit.py")]
    + ["--files"] + CLOSE_FILES + ["--message", CLOSE_MSG],
    cwd=str(ROOT), capture_output=True, timeout=300)
print(proc.stdout.decode("utf-8", "replace"))
if proc.returncode != 0:
    print(proc.stderr.decode("utf-8", "replace"))
    sys.exit(proc.returncode)
