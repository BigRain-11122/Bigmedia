# R1902 closing stage: state accounting + export refresh + embedded close commit.
# Family convention (tech#27 two-stage + tech#65 embedded commit). ASCII script
# body per the encoding rule; CJK only inside the data payloads below.
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "src" / "os" / "state.json"
EXPORT = ROOT / "docs" / "status-export.json"

NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

LOG = ("2026-10-10 19:2x R1902: 等待窗 P2 生产轮·tech#68 导出面契约守卫交付"
       "（O-20260909-1246 取活·R1901 focus 指针兑现·两段制收账=交付段先行 commit 39e15cb7）"
       "——①轮首五查 fresh 全静=own orders 顶 O-20261008-1105 mtime 12:08:14==R1733 锚零新令"
       "+origin_gap_check QUIET ahead0 behind0（R1500 前置位）+group_scan 固定探针三面静"
       "（decisions dnum 内容寻址差集 truly_new=0 水位 131 维持+ledger mtime 15:27:33=值守轮 15:07 "
       "记录面写入·@BigStream 4 行==值守锚零新转办+HQ orders mtime 18:54:32 破 R1901 锚 18:23:20"
       "→尾读新行全他域知悉 ack（BigLife 解冻令+O-1830 吸嘟嘟 GUI+2D 全面整改令+X2333/X2334 bm-a 回执"
       "=BigLife/MiniGame 域零本司份额）·新锚 18:54:32）+无 index.lock+树态=mv0001/mv001/whisper v3/"
       "drama_takt bm-a MV sprint 会话批域在飞件零接触（R1745 承继·tech#26 撞面维持）；"
       "②12:00 GPU 窗 C-37 fresh 判读=NO-GO 双面齐触（pause_face 任务态指纹 8/8 Disabled=CEO 让路令在役"
       "+vram_face free 3066MB<9216 守卫）→四腿（MD-0002 剧本腿/DIGEST v17 M4.5·E4/F-170 S1/"
       "tech#43 E4 v13）维持 fire-ready gated（材料 R1870/R1871/R1875 turnkey）+ollama 探针 --ledger="
       "rc0 GEN-OK face=ok gpu_util 81/gpu_mem 11886（服务健康·MV 会话生成满载窗=让路面维持）；"
       "③#111 查看位=krea2 30s-reel-v1 新到件批实录（R1898 锚 15:14 后：30s_reel_v4.mp4 18:23:58 成片"
       "+DELIVERY-QC-BOARD-v44+DELIVERY-NOTE-v44+CEO-DECISION-kf-5shot-stop-20261010.md+"
       "wave-c1793-harvest-qc.json=30s 成品出片+做旧克制档 CEO 终裁「其他都可以了」在案+成品 MV 五镜停手"
       "升级件〔KF1 火把/KF6 凿刻/KFT 金字/KF8 倒影/KF10 走远连摇不过线·四方向 A-D 待 CEO 定〕——"
       "CEO 过目位就绪·backlog #111 R1902 注记·MV 会话域零接触）；④#115 meme 查看位=outbound 零新到件"
       "（止于 15:41 narration.mp3==R1899 锚·成片未到=TTS/装配腿在飞维持）；"
       "⑤tech#68 交付=**export-face 检测面全落**（缺口锚=R1901 导出面 167KB 漂移 ~1700 轮零点名）——"
       "loop_health 新 classify_export_face 纯核（四面一 WARN 一面：do>120 字=export-do/outs 非 3 胞 "
       "[txt<=64,on|wait|off,tag<=24]=export-outs/results 非 [v<=16,k<=14] 短值键对=export-results/"
       "三列表超帽〔12/14/4〕=export-caps+解析坏=export-contract wholesale WARN·缺件静默=导出步自有面）"
       "+check_export_face 接线（例行探针消费即点名）·18 新测（ExportFaceTests：R1901 锚形四面复现点名"
       "+契约形零发现+边界/坏形/帽/CLI WARN 不破 FAIL/真仓净基线冒烟）·**730 全回归绿 99.7s SUITE_RC=0**"
       "（712+18·run_suite 正法）——判据双过=①锚形 fixture 四面全点名②真仓契约版零发现"
       "（新面首战静默 PASS·probe 消费 224 WARN==基线持平零新增）·C-20 v1.75；"
       "⑥真发现种子=export_ts 未来戳缺陷（export_ts 19:05:00 vs 件 mtime 18:49:42=写入时点未来 ~15min·"
       "R1901 刷新脚本 ts 取值面缺陷·本轮收账按真实钟勘正值+tech#69 补货守卫候选）；"
       "⑦三探针=probe_capture 单调消费（board 0 FAIL〔5 题 10 稿 5 in production〕/readiness 3 阻塞皆外部 "
       "CEO 面〔账号批次①+M4 GATE 6/10+#17 needs-CEO〕0 发现〔78 renders 全注账 unannot=0〕/"
       "loop_health 2F+224W 皆在案史实〔两 outage 09-26/09-28 已裁定不重触发·drift 17==R1865 基线 21 带内〕）；"
       "⑧例行件=10-10 日报在案不重跑（R1845 00:03 一份为真相）·W41 周审在案 W42 件 10-12 未到·"
       "GB §④ v1.3 下期 10-15 跳过·15:07 盘燃=R1825 已点名毕不重扫·krea2/H3 查看位=本轮实扫后禁重扫跳过·"
       "#99 blocked-on-channel 维持（SLA ≤10-13）·#112 判据窗 10-11 08:00 届日即领（tech#53 双新源流量首报同窗）"
       "·HQ-FEEDBACK 不写（HQ 新行全他域知悉类零集团层新 open 项零膨胀）·tokens:local=0（纯探针+工程+套件跑"
       "零本地模型产出调用·P-54⑤ 计量律）——下轮=R1903 快速路径首查（10-11 08:00 #112 城市口径判据窗验收"
       "〔城市源 ≥60 ≥2 件+tech#53 首报+failed 尾读数〕届日即领+GPU 窗 C-37 fresh 四腿判断+meme V1 成片/"
       "krea2 查看位随轮盯+P2 队头 tech#69 候选）")

FOCUS = ("R1903 快速路径首查（10-11 08:00 #112 城市口径判据窗届日即领+GPU 窗 C-37 fresh 四腿判断"
         "+meme V1 成片/krea2 查看位随轮盯+tech#69 P2 队头候选）")

# ---- state.json accounting -------------------------------------------------
state = json.loads(STATE.read_text(encoding="utf-8-sig"))
assert state["tick"] == 1901, "unexpected tick %r" % state.get("tick")
state["tick"] = 1902
state["focus"] = FOCUS
log = state["log"]
assert isinstance(log, list)
log.append(LOG)
state["log"] = log
state["ts"] = NOW
state["task"] = LOG.split("：", 1)[1][:60] if "：" in LOG else LOG[:60]
STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1) + "\n",
                 encoding="utf-8")

# ---- export refresh (P-61 step; fixes the R1901 future-stamped ts) --------
export = json.loads(EXPORT.read_text(encoding="utf-8-sig"))
export["export_ts"] = NOW  # real clock at write time (R1901 defect corrected)
export["do"] = ("AI 媒体产线量产开闸运转·OS 循环 R1902；meme V1《慢慢踩》生产在飞；"
                "MV 30s 成片 v4 CEO 终裁毕；发布锁账号物理件")
for dept in export["depts"]:
    if dept.get("n") == "工程技术部":
        dept["t"] = ("730 测试全绿（100s）；S2 三门机检+守卫面 21+ 在役（export-face 新）；"
                     "收账链 close_commit 内嵌（tech#65/67）")
export["outs"][0] = ["R1902 tech#68 export 契约守卫（730 测绿）", "on", "os-loop"]
for i, entry in enumerate(export["outs"]):
    if entry[2] == "mv0001" and "v4.3.1" in entry[0]:
        export["outs"][i] = ["MV 30s 成片 v4 做旧克制档 CEO 终裁放行", "on", "mv0001"]
for chip in export["chips"]:
    if chip[0] == "712 测绿":
        chip[0] = "730 测绿"
for res in export["results"]:
    if res[0] == "712":
        res[0] = "730"
    if res[0] == "1901":
        res[0] = "1902"
export["live"] = [
    "当前活：R1902 tech#68 export 契约守卫面交付（loop_health 四面 WARN+18 测·730 全回归绿 99.7s）"
    "+五查静（HQ 18:54:32 新行全他域 ack·decisions 水位 131 平）+GPU 窗 C-37 NO-GO 维持"
    "（pause 指纹 8/8+free 3066MB·四腿 fire-ready gated）+ollama GEN-OK 服务健康",
    "最近实物：src/os/loop_health.py export-face 检测面（commit 39e15cb7）+查看位：30s_reel_v4.mp4 "
    "成片（18:23·做旧克制档 CEO 终裁「其他都可以了」）+成品 MV 五镜停手升级件待 CEO 定方向"
    "（krea2/30s-reel-v1 批）+export_ts 未来戳缺陷勘正（tech#69 种子在册）",
    "下个里程碑：①10-11 08:00 #112 城市口径判据窗验收（城市源 ≥60 ≥2 件+tech#53 双新源流量首报）"
    "②GPU 窗 C-37 fresh（pause 解除即四腿开窗：MD-0002 剧本/DIGEST v17 M4.5·E4/F-170 S1/tech#43 E4 v13）"
    "③meme V1 成片到件随轮盯（#115）",
]
EXPORT.write_text(json.dumps(export, ensure_ascii=False, indent=1) + "\n",
                  encoding="utf-8")

# sanity: the new guard face must be silent on the refreshed export
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "os"))
import loop_health  # noqa: E402
data = json.loads(EXPORT.read_text(encoding="utf-8-sig"))
violations = loop_health.classify_export_face(data)
assert violations == [], "refreshed export violates contract: %r" % violations
print("state tick=1902 ts=%s" % NOW)
print("export contract: silent PASS (%d chars do)" % len(data["do"]))

# ---- embedded close commit (tech#65) ---------------------------------------
CLOSE_FILES = [
    "src/os/state.json",
    "docs/status-export.json",
    ".c3-tmp/r1902_group_scan.json",
    ".c3-tmp/r1902_probes.txt",
    ".c3-tmp/r1902_close.py",
]
CLOSE_MSG = ("R1902 closing: state tick 1902 + export refresh (ts future-stamp "
             "corrected) + probe evidence [via bm-a]")
proc = subprocess.run(
    [sys.executable, str(ROOT / "src" / "os" / "close_commit.py")]
    + ["--files"] + CLOSE_FILES + ["--message", CLOSE_MSG],
    cwd=str(ROOT), capture_output=True, timeout=300)
print(proc.stdout.decode("utf-8", "replace"))
if proc.returncode != 0:
    print(proc.stderr.decode("utf-8", "replace"))
    sys.exit(proc.returncode)
