# R1907 close script (house convention: close scripts tracked as round evidence)
# Steps: 1) state.json update (tick/focus/log/ts/task)  2) export refresh via canonical
# writer (tech#70) with P-6 plain-language live lines  3) probe_capture run -> evidence file.
import json, subprocess, sys, io
from datetime import datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
STATE = ROOT + r"\src\os\state.json"
PATCH = ROOT + r"\.c3-tmp\r1907_export_patch.json"
PROBES = ROOT + r"\.c3-tmp\r1907_probes.txt"

now = datetime.now()
ts = now.strftime("%Y-%m-%d %H:%M:%S")
round_no = 1907

focus = ("R1908 快速路径首查（10-11 08:00 #112 城市口径判据窗届日即领〔城市源 ≥60 ≥2 件+tech#53 双新源流量首报同窗〕"
         "+GPU 窗 C-37 fresh 四腿判断+meme V1 成片查看位随轮盯+P-6 试点第 2 轮 live 大白话维持）")

log_line = (
    "2026-10-10 20:5x R1907: 生产轮·tech#73 硅基窗 v6.3 消费面复扫收口+P-6 提案起链试点首件执行"
    "（O-20261009-1246 取活·R1906 focus 指针兑现·两段制收账=交付段先行 commit 3f1b5011）——"
    "①轮首五查=HQ orders mtime 20:15:33 破 R1906 锚 20:08:26→尾读零新行=他窗就地状态编辑"
    "（O-1955 行 in-flight→executed·ad209fda1 已推=tech#73 gate 到达判据实锚）·余四查静"
    "（own orders 顶 O-20260908-1105 mtime==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0"
    "+group_scan 固定探针 truly_new=0 水位 131 维持+ledger @BigStream 4 行==值守锚·无 index.lock"
    "·树态=MV sprint 会话域在飞件零接触 R1745 承继）；"
    "②GPU 窗 C-37 fresh=NO-GO（pause_face clear 8/8=O-2006 算力解禁生效·vram_face free 452MB<9216 守卫"
    "=他 lane 合法并行满载）+ollama 探针 --ledger rc2 busy-contended gpu 100%/11830→四腿"
    "（MD-0002 剧本腿/DIGEST v17 M4.5·E4/F-170 S1/E4 v13）维持 fire-ready gated（材料 R1870/R1871/R1875 turnkey）；"
    "③#111/#115 查看位双路径并读=krea2 30s-reel-v1 零新到件（止于 DELIVERY-NOTE-v44 20:03:42==R1906 锚）"
    "+meme 正典域 spec 件 16:01-17:17=集团台账已承件·V1 成片 mp4 未到（TTS/装配在飞维持·O-2006 20:06 行「V1 生产在飞」对读）；"
    "④tech#73 交付（P2 队头·gate O-1955 收口已至）=复扫三面收口零新消费——generate.ps1 v6.3（752 行）六键集零漂移"
    "+canonical.html v6.3（1308 行）新渲染位（二级页 pg-lead L1184←s.now/游戏库←games_catalog）全 strings.json 策展层直供非 export"
    "+live 仍零看板路径（tech#72 定谳复证·shape 守卫分支不触发=零新面反膨胀律）·证据件 r1907_t73_consumer_evidence.txt；"
    "⑤副产出=§D P-6 提案起链+试点首件本尊执行（真发现：live 三行 OS 术语体 vs O-20261010-1955 大白话令"
    "·tech#73 实证 JSON 直读=唯一 CEO 可见路径）+tech#74 补货（三队补货步 ✓·连续 3 轮观察窗回读 ≤10-24）；"
    "⑥三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）"
    "0 发现/loop_health 2F+史实带内（两 outage 已裁定不重触发·r1907_probes.txt）；"
    "⑦例行件=10-10 日报在案不重跑（R1845 一份为真相）·W41 周审在案 W42 件 10-12 未到·GB §④ v1.3 下期 10-15 跳过"
    "·#112 城市口径判据窗 10-11 08:00 届日即领·#99 blocked-on-channel 维持（SLA ≤10-13）"
    "·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·tokens:local=0（纯只读复扫+工程台账零本地模型调用·P-54⑤ 计量律）"
    "——下轮=R1908 快速路径首查（10-11 08:00 #112 判据窗届日即领〔≥60 ≥2 件+tech#53 首报〕+GPU C-37 fresh+meme V1 成片查看位+P-6 第 2 轮维持）"
)

# fix the minute placeholder with real minute
log_line = log_line.replace("20:5x", ts[11:16])

with open(STATE, "r", encoding="utf-8") as f:
    state = json.load(f)
state["tick"] = round_no
state["focus"] = focus
# ts+task law: ts = close moment, task = first 60 chars of log line minus timestamp prefix
state["ts"] = ts
prefix = "2026-10-10 %s R1907: " % ts[11:16]
task_src = log_line[len("2026-10-10 ") + len(ts[11:16]) + len(" R1907: "):]
state["task"] = task_src[:60]
state["log"] = state.get("log", [])
state["log"].append(log_line)

with open(STATE, "w", encoding="utf-8", newline="\n") as f:
    json.dump(state, f, ensure_ascii=False, indent=1)
print("state.json: tick=%d ts=%s" % (round_no, ts))

# --- export refresh patch (P-6 pilot: plain-language live lines) ---
patch = {
    "do": "AI 媒体产线量产运转·OS 循环 R1907；硅基窗看板对接面查完（稳定不用改）；meme V1《慢慢踩》生产在飞；发布锁账号物理件",
    "live": [
        "当前活：把看板的数据对接面查了一遍，确认稳定不用改；新剧本、城市盘点卡、评审件、纪实篇四件活等显存腾出来就开工。",
        "最近实物：30 秒《爱在西元前》成片今晚 20:01 完成（带快慢变化的剪辑节奏）；本轮看板对接检查报告已入档。",
        "下个里程碑：明早 8 点验收雷达日报「城市热点版」第一份；显存一空四件活开工；《慢慢踩》短视频成片过完评审就呈你（最快明天）。"
    ]
}
with open(PATCH, "w", encoding="utf-8", newline="\n") as f:
    json.dump(patch, f, ensure_ascii=False, indent=1)

r = subprocess.run([sys.executable, ROOT + r"\src\os\export_refresh.py", "--patch", PATCH],
                   capture_output=True)
print("export_refresh rc=%d" % r.returncode)
sys.stdout.write(r.stdout.decode("utf-8", "replace"))
sys.stderr.write(r.stderr.decode("utf-8", "replace"))
if r.returncode != 0:
    print("FATAL: export refresh refused; aborting close before probes")
    sys.exit(2)

# --- probes (probe_capture compact consumption) ---
p = subprocess.run([sys.executable, ROOT + r"\src\os\probe_capture.py", "--out", PROBES],
                  capture_output=True)
sys.stdout.write(p.stdout.decode("utf-8", "replace"))
sys.stderr.write(p.stderr.decode("utf-8", "replace"))
print("probe_capture rc=%d -> %s" % (p.returncode, PROBES))
print("CLOSE-STEPS-OK")
