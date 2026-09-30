# -*- coding: utf-8 -*-
# R744 close-out: LC-019 trim-chain ledger writes + state tick + export refresh.
import io
import json
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime.now().strftime("%Y-%m-%d %H:%M")
STAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --- canonical probe (r694_probe.py) if tracked/present ---
probe_note = ""
pp = ROOT / ".c3-tmp" / "r694_probe.py"
if pp.exists():
    r = subprocess.run(["python", str(pp)], cwd=str(ROOT), capture_output=True, timeout=120)
    txt = r.stdout.decode("gbk", errors="replace")
    (ROOT / ".c3-tmp" / "r744_probe.txt").write_bytes(r.stdout)
    keep = [l for l in txt.splitlines() if ("orders" in l or "ledger" in l
            or "decisions" in l or "production" in l or "lock" in l)][:6]
    probe_note = " | ".join(keep[:6])
else:
    probe_note = "probe-script-absent (four-pattern hand scan 40 rows, anchor 41 = six-pattern superset)"

# --- 1. lc019 README: append R744 prod row + update gate block ---
RP = ROOT / "data/sources/lc019/README.md"
raw = RP.read_bytes().decode("utf-8")
new_row = ("- [2026-09-30 11:5x R744 空气预算机械裁链定稿+TTS 定稿音轨毕（R740/R736 同型·R743 claim 承接）] "
           "v2 机械裁 77 字=64.460s 仍超窗（0.198s/char 实测率·新市民派/算力街区/江水句/结结实实/从此他把/随口就来/"
           "进了扭塔他才懂/一条/或者/食堂/给他/研究员〔CTA 位〕全归卡承载或承前省略·语义零改·M1 v2 0F0W="
           "v1 b2 居民档案行 WARN 销账）→v3 续裁 31 字=**57.235s 定稿入窗 2.765s 余量**（fleet 带 1.2-2.8s 内·"
           "F-002 v15 2.8s 同位宽档；hook「给被毙策略」归卡=LC-018 hook 同位裁法/量化/想起/俩字/全家福小像句整句归卡"
           "〔col2 verbatim 承载〕/不是赌运气是→就是/大厨/还全归卡·M1 v3 0F0W）；机器断言 .c3-tmp/r744_trim_v2/v3.py="
           "col1/col2 verbatim 零动 12/12〔v1↔v2↔v3 双基〕+信条 verbatim+事实数字全保（二十八岁/一万遍）+互证双名全保"
           "（徐根福/陈雅雯）+CTA 受众定位词「敬畏市场」全保·口播字数链 304→227→196（去标点）·v1-v3 beats 三件入 git；"
           "TTS light 定稿音轨 .lc019-tmp/（audio.mp3 57.235s+subs.srt 12 cues+cards.json·--order LC-019-v3·"
           "--template=.lc018-tmp/cards.json 链式承继·BGM-A 纯净·r744_tts_run.py 脱壳两飞两落=R176/R195 长任务脱壳律执法）。\n")
anchor = "## 门禁块"
assert anchor in raw
raw = raw.replace(anchor, new_row + "\n" + anchor, 1)
old_gate = ("- M1 v1=0 FAIL 1 WARN（b2 同型收口位）·S1=**10/10 PASS 十八连满分**（11:02:04 落判·"
            "判词档 20260930-110204-S1-script·机械裁不回炉=fleet 先例）·空气预算=v1 实测 **79.696s 超窗**"
            "（R744 机械裁链首位）·渲染腿=待领·收官腿=待领。发布锁=M5 账号物理件不变（未上线=未测量）。")
new_gate = ("- M1 v1 0F1W→**v2/v3 双 0F0W**（b2 WARN 随裁销账）·S1=**10/10 PASS 十八连满分**（11:02:04 落判·"
            "判词档 20260930-110204-S1-script·机械裁不回炉=fleet 先例）·空气预算=**v3 57.235s 定稿入窗 2.765s 余量**"
            "（R744 裁链 v1 79.696→v2 64.460→v3 57.235·共裁 108 字）·渲染腿=待领·收官腿=待领。"
            "发布锁=M5 账号物理件不变（未上线=未测量）。")
assert old_gate in raw, "gate block anchor not found"
raw = raw.replace(old_gate, new_gate, 1)
RP.write_bytes(raw.encode("utf-8"))
print("README updated")

# --- 2. queue: append R744 burn row at end of section E ---
QP = ROOT / "docs/self-improvement-queue.md"
qraw = QP.read_bytes().decode("utf-8")
qrow = ("- 2026-09-30: **E16 LC-019 空气预算裁链定稿+TTS 定稿音轨毕（R744·R743 起链承接·R740 同型）**："
        "v1 79.696s→v2 机械裁 77 字=64.460s 仍超窗→v3 续裁 31 字=**57.235s 定稿入窗 2.765s 余量**"
        "（fleet 带 1.2-2.8s 内·F-002 v15 同位宽档；裁词全归卡承载或承前省略：v2 新市民派/算力街区/江水句/"
        "结结实实/从此他把/随口就来/进了扭塔他才懂/一条/或者/食堂/给他/研究员〔CTA 位〕+v3 hook 给被毙策略="
        "LC-018 hook 同位裁法/量化/想起/俩字/全家福小像句整句归卡/不是赌运气是→就是/大厨/还）+机器断言 "
        "r744_trim_v2/v3.py（col1/col2 verbatim 12/12 v1↔v2↔v3 双基+信条 verbatim+事实数字 二十八岁/一万遍+"
        "互证双名 徐根福/陈雅雯+CTA 受众定位词 敬畏市场 全保）+M1 v2/v3 双 0F0W（v1 b2 WARN 销账）+"
        "口播字数链 304→227→196+TTS light 定稿音轨 .lc019-tmp/（--order LC-019-v3·--template=.lc018-tmp 链式承继·"
        "BGM-A 纯净）——渲染腿（R741/R737 同型五步+全卡几何审计 R720 律前置：F-024 PNG 派生 census-card-v5-vertical·"
        "R511 法→对位表 12/12→R-E shipinhao〔拆条 019·源城市图鉴 005〕→S2 三门+帧验三律）→收官腿（E8+ASR+E4+M4→"
        "F-074 登记→冗余池第十六件落位→E16 出池+补池义务随轮领）=后续轮领；lane=E16〔active·裁链毕〕+E20〔standby〕"
        "维持 ≥2。\n")
qanchor = "\n## burn 记录"
assert qanchor in qraw
qraw = qraw.replace(qanchor, "\n" + qrow + qanchor, 1)
QP.write_bytes(qraw.encode("utf-8"))
print("queue updated")

# --- 3. status-export.json refresh ---
EP = ROOT / "docs/status-export.json"
d = json.loads(EP.read_bytes().decode("utf-8"))
d["export_ts"] = STAMP
d["outs"][0][1] = ("tick 744，R744 生产轮·E16 LC-019 周浩宇拆条空气预算裁链定稿+TTS 定稿音轨毕"
                   "（产品优先律对位=本轮实物增量=LC-019 定稿音轨 57.235s+beats v2/v3 裁稿链·"
                   "v1 79.696→v2 64.460→v3 57.235s 入窗 2.765s 余量·M1 v2/v3 双 0F0W·col2 verbatim 12/12·"
                   "lane=E16〔active·裁链毕〕+E20〔standby〕≥2 达标）——渲染腿+收官腿（F-074 登记）随轮领·"
                   "发布锁=M5 账号物理件不变")
logline_744 = ("2026-09-30 11:5x R744: 生产轮·E16 LC-019 周浩宇拆条空气预算裁链定稿+TTS 定稿音轨毕"
               "（R743 claim 承接·R740/R736 同型·实活轮·产品优先律 P-20260929-07 对位=本轮实物增量="
               "LC-019 定稿音轨 57.235s+beats v2/v3 裁稿链）——①轮首快速路径五查静（orders 顶 O-20260928-1910 "
               "42 件锚未动/ledger 严格 @ 前缀扫描零新 CEO 令级事件〔L189/L190/L245 已收讫·四模式 40 行=六模式锚 41 "
               "子集口径〕/decisions UTF8 非空行 75=锚零新行/production=open 自愈核在位 tick743/无 index.lock·"
               "树态=bm-a codex 批未闭让位维持〔README/city-humanities mtime 09-29 04:06 未动=#86 c+d 判据未达·"
               "两文件零接触〕+自产 tmp 族预期态）+三探针=board exit=0 0 FAIL/readiness 3 阻塞皆外部 CEO 面 0 发现"
               "（阻塞≠失败口径）/loop_health 2 FAIL+WARN 皆在案史实类（2 outage 同事件足迹已裁定）；②空气预算两道"
               "机械裁链：v1 79.696s（R743 读数·304 去标点字=fleet 带外初读最高位）→v2 机械裁 77 字=64.460s 仍超窗"
               "（0.198s/char 实测率·新市民派/算力街区/江水句/结结实实/从此他把/随口就来/进了扭塔他才懂/一条/或者/"
               "食堂/给他/研究员〔CTA 位〕全归卡承载或承前省略·M1 v2 0F0W=v1 b2 居民档案行 WARN 销账）→v3 续裁 "
               "31 字=**57.235s 定稿入窗 2.765s 余量**（fleet 带 1.2-2.8s 内·F-002 v15 2.8s 同位宽档；hook"
               "「给被毙策略」归卡=LC-018 hook 同位裁法/量化/想起/俩字/全家福小像句整句归卡〔col2 verbatim 承载〕/"
               "不是赌运气是→就是/大厨/还全归卡·M1 v3 0F0W）；③机器断言 .c3-tmp/r744_trim_v2/v3.py=col1/col2 "
               "卡片锚点列 verbatim 零动 12/12（v1↔v2↔v3 双基断言）+信条 verbatim+事实数字全保（二十八岁/一万遍）+"
               "互证双名全保（徐根福/陈雅雯）+CTA 受众定位词「敬畏市场」全保·口播字数链 304→227→196（去标点）·"
               "v1-v3 beats 全留档；④TTS light 定稿音轨 .lc019-tmp/（audio.mp3 57.235s ffprobe 实测+subs.srt 12 cues+"
               "cards.json 基线·--order LC-019-v3·--template=.lc018-tmp/cards.json 链式承继·cyber light+human 42 "
               "产线默认·BGM-A 纯净·r744_tts_run.py 脱壳两飞两落=长任务脱壳律 R176/R195 执法）；⑤台账=lc019 README "
               "生产记录+门禁块更新+queue §E E16 burn 行+export 刷；⑥例行件：日报 09-30 在案不重跑（R713 补产）/W40 "
               "周审在案（R576）/月度注记在案（R-20260928-03）/global-benchmarks day6 ≤7 跳过（下期 10-01=#80 并窗"
               "勿提前触碰）/#70 OSS 窗 2=10-02 21:40 前随轮领（窗面义务足 R644 切片 1）/#86 c+d 让位判据未达"
               "（codex mtime 04:06 未动）/T1 催办=已裁项停用口径/HQ-FEEDBACK 不写（无集团层新 open 问题·双锚静零膨胀）"
               "·tokens:local=0（M1+TTS=纯脚本 edge-tts 零本地模型调用·S1 qwen=R743 起飞轮已记账·P-54⑤ 计量律如实记）"
               "——下轮=R745 可领序：①LC-019 渲染腿（R741/R737 同型五步+全卡几何审计 R720 律前置：F-024 PNG 派生 "
               "census-card-v5-vertical·R511 法→对位表 12/12→R-E shipinhao〔拆条 019·源城市图鉴 005〕→S2 三门+帧验三律）"
               "→收官腿（E8+ASR+E4+M4→F-074 登记→冗余池第十六件落位→E16 出池+补池义务随轮领）②#70 OSS 窗 2 切片"
               "（≤10-02 21:40）③#86 c+d 让位判据④global-benchmarks 10-01 刷新（#80 并窗）。收账显式列文件 commit+push")
d["results"].insert(0, ["744", logline_744])
if len(d["results"]) > 16:
    d["results"] = d["results"][:16]
d["live"] = [
    ["当前活：LC-019 周浩宇拆条空气预算裁链毕（R744）——v3 定稿音轨 57.235s 入窗 2.765s 余量·M1 0F0W·col2 verbatim 12/12·lane=E16〔active·裁链毕〕+E20〔standby〕≥2 达标"],
    ["最近实物：LC-019 定稿音轨+beats v2/v3 裁稿链 data/sources/lc019/（57.235s·2026-09-30 11:5x）+lc-018-v1-shipinhao-60s.mp4 F-073 登记成品 58.411s（10:44）"],
    ["下个里程碑：LC-019 渲染腿→收官腿 F-074 登记（≤48h 窗 2026-10-02 前）·#70 OSS 窗 2 切片（≤10-02 21:40）·global-benchmarks 7 日刷（10-01 #80 并窗）"],
]
EP.write_bytes(json.dumps(d, ensure_ascii=False, indent=1).encode("utf-8"))
print("export updated")

# --- 4. state.json: tick + log + ts/task/focus ---
SP = ROOT / "src/os/state.json"
s = json.loads(SP.read_bytes().decode("utf-8"))
assert s["tick"] == 743, "unexpected tick %s" % s["tick"]
s["tick"] = 744
s["ts"] = STAMP
s["task"] = logline_744[len("2026-09-30 11:5x "):][:60]
s["log"].append(logline_744)
s["focus"] = ("R745: ①LC-019 渲染腿（R741/R737 同型五步+全卡几何审计 R720 律前置：F-024 PNG 派生 "
              "census-card-v5-vertical·R511 法→对位表 12/12→R-E shipinhao〔拆条 019·源城市图鉴 005〕→"
              "S2 三门+帧验三律）→收官腿（E8+ASR+E4+M4→F-074 登记→冗余池第十六件落位→E16 出池+补池义务随轮领）"
              "②#70 OSS 窗 2 切片（≤10-02 21:40·R644 切片 1 在案）③#86 c+d 让位判据（bm-a codex 批闭 commit 落地）"
              "④global-benchmarks 10-01 刷新（#80 并窗）——五查锚=orders O-20260928-1910 42·ledger 41"
              "（L189/L190/L245 注）·decisions 75")
SP.write_bytes(json.dumps(s, ensure_ascii=False, indent=1).encode("utf-8"))
print("state updated: tick=%d log_len=%d ts=%s" % (s["tick"], len(s["log"]), STAMP))
print("probe:", probe_note[:300])
