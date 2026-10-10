# -*- coding: utf-8 -*-
"""R1922 close: waiting-round accounting (tech#75 data point + state tick + probes evidence)."""
import json, io, os, subprocess, datetime, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
os.chdir(ROOT)

now = datetime.datetime.now()
ts = now.strftime("%Y-%m-%d %HH:%M:%S").replace(" ", " ", 1)
ts = now.strftime("%Y-%m-%d %H:%M:%S")
log_min = now.strftime("%H:%M")

# ---------- 1) tech.md #75 row: append data point ----------
tech_path = os.path.join("state", "queue", "tech.md")
with io.open(tech_path, "r", encoding="utf-8") as f:
    tech_lines = f.read().split("\n")
idx = None
for i, ln in enumerate(tech_lines):
    if ln.startswith("75."):
        idx = i
        break
assert idx is not None, "tech#75 row not found"
row = tech_lines[idx]
if "[R1922 判断位照正法执行" in row:
    print("tech.md #75 data point already appended (skip)")
else:
    assert "[R1921 判断位照正法执行=稳态饱和域清洁 NO-GO]" in row, "R1921 anchor missing in tech#75 row"
    dp = ("——**[R1922 判断位照正法执行=稳态饱和域 NO-GO 延续]**：23:12 ollama 探针 GEN-ERROR transport=TimeoutError face=busy-contended"
          "+gate --samples 4 worst-case free 738MB/band 356/util 100=稳态饱和域（band 356 非振荡·advisory 未现）"
          "·frames_full N03_goddess_pass.png 23:08:37 新落帧=全曲 KF 批本机在产互证·零 GO 间隙·非双 GO 不点火"
          "·四腿 fire-ready gated 维持·序列数据点续记（fire 稳定窗等待位维持）")
    tech_lines[idx] = row + dp
    with io.open(tech_path, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(tech_lines))
    print("tech.md #75 data point appended")

# ---------- 2) state.json: tick + log + ts/task + focus ----------
state_path = os.path.join("src", "os", "state.json")
with io.open(state_path, "r", encoding="utf-8") as f:
    st = json.load(f)
assert st["tick"] == 1921, "tick mismatch: %s" % st["tick"]

log_line = (
    "2026-10-10 " + log_min + " R1922: 等待轮·tech#75 判断位照正法执行=稳态饱和域 NO-GO 延续"
    "（O-20261009-1246 取活判走+产品优先律 §2 一行声明）——"
    "①轮首五查全静=own orders 顶 O-20260908-1105 mtime==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）"
    "+group_scan 固定探针三面静（decisions dnum 内容寻址差集 truly_new=0 水位 131 维持+ledger @BigStream 4 行==值守锚零新转办"
    "+HQ orders 22:58:58==R1921 消费锚〔@bm-c 撤单行〕零新行）+无 index.lock+树态=MV sprint 会话批域在飞件零接触（R1745 承继·tech#26 撞面维持）；"
    "②GPU 窗 C-37 fresh 判读=NO-GO（pause_face clear 8/8=O-20261010-2006 算力解禁态·vram_face worst-case free 738MB/band 356<9216 守卫"
    "+util worst-case 100%>80=MV 全曲 KF 批他 lane 稳态饱和域）+ollama 探针 GEN-ERROR TimeoutError face=busy-contended（满载窗让路面维持不升级）"
    "→四腿（MD-0002 剧本腿/DIGEST v17 M4.5·E4/F-170 S1/tech#43 E4 v13）维持 fire-ready gated（材料 R1870/R1871/R1875 turnkey）"
    "·tech#75 判断位照正法执行=非双 GO 不点火·序列数据点续记 tech.md 75 行；"
    "③查看位四根并读（R1762 律·R1921 锚后）=meme outbound 零新到件（V1 成片 mp4 未落=TTS/装配链在飞维持）"
    "+krea2 30s-reel-v1/frames_full 1 新帧 N03_goddess_pass.png 23:08:37（全曲 KF 批本机在产互证·MV 会话域查看位零接触·新锚 23:08:37）"
    "+mv0001-handover 其余面/shortvideo-dept/h3-local-test 零新；"
    "④三队盘点=main 全 gated/查看位（#111 查看位新帧已注·#112 判据窗 10-11 08:00 未到届日即领不预扫）"
    "+tech 全 done/gated（#75 判断位本轮照正法执行=NO-GO 数据点续记）+explore 全 done/gated/到点未到（10-13/15/16/17 窗）"
    "→真无可执行项=一行声明收轮合法（waiting: GPU VRAM 他 lane 稳态饱和〔ETA=MV 全曲 KF 批完即四腿点火〕"
    "+#112 城市口径判据窗〔ETA 2026-10-11 08:00〕届日即领）；"
    "⑤三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面〔账号批次①+M4 GATE 6/10+#17 needs-CEO〕0 发现"
    "〔78 renders 全注账 unannot=0〕/loop_health 2F+229W 皆在案史实〔两 outage=09-26/09-28 已裁定不重触发·drift 17==adjudicated 基线带内〕"
    "·证据 .c3-tmp/r1922_probes.txt；"
    "⑥例行件=10-10 日报在案不重跑（R1845 00:03 一份为真相）·W41 周审在案 W42 件 10-12 未到·GB §④ v1.3 下期 10-15 跳过"
    "·export_ts 20:56:29 <24h 零 CEO 可见变化不重刷（产品优先律 §2 节流·live 三行大白话核读=仍实况准确）"
    "·#99 blocked-on-channel 维持（SLA ≤10-13）·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）"
    "·tokens:local=0（探针生成调用属探针件非评审调用 R1888 口径·纯只读+档案读写零本地模型产出调用·P-54⑤ 计量律）"
    "·队列补货步=真无新种子如实注记零膨胀（N03 新帧归 #111 既有查看行射程·tech#75 NO-GO 数据点归既有 75 行·禁凑数律）"
    "·临时件=r1922 证据件入账收口（tech#64 律）——"
    "下轮=R1923 快速路径首查（10-11 08:00 #112 判据窗届日即领〔城市源 ≥60 ≥2 件+tech#5/#30/#49/#53 双新源读数族〕"
    "+GPU C-37 fresh 四腿点火判断+meme V1 成片/krea2 frames_full 查看位随轮盯）"
)

st["tick"] = 1922
st["log"].append(log_line)
st["ts"] = ts
st["task"] = log_line.split("R1922: ", 1)[1][:60]
st["focus"] = ("R1923 快速路径首查（10-11 08:00 #112 城市口径判据窗届日即领〔城市源 ≥60 ≥2 件+tech#53 双新源流量首报+tech#5/#30/#49 判定位〕"
               "+GPU C-37 fresh 四腿点火判断〔MD-0002 剧本腿/DIGEST v17 M4.5·E4/F-170 S1/tech#43 E4 v13〕+tech#75 判断位照正法〔双 GO 连续 ≥2 方飞〕"
               "+meme V1 成片/krea2 frames_full 查看位随轮盯）")
with io.open(state_path, "w", encoding="utf-8", newline="") as f:
    json.dump(st, f, ensure_ascii=False, indent=1)
print("state.json: tick 1922, ts=%s" % ts)

# ---------- 3) probes evidence file ----------
ev = io.StringIO()
ev.write("# r1922 probe evidence (waiting-round, generated %s)\n" % ts)
ev.write("== five-check: own-orders-anchor=O-20260908-1105 mtime 2026-10-08 12:08:14 (==R1733, no new order); origin_gap QUIET ahead0 behind0\n")
ev.write("== group_scan: decisions truly_new=0 watermark 131; ledger @BigStream 4==duty anchor; HQ orders mtime 22:58:58 == R1921 consumed anchor; no index.lock\n")
ev.write("== tree: MV sprint session-batch in-flight files expected state (R1745 zero-contact)\n")
ev.write("== gpu gate: pause_face=clear(8/8), worst-case free 738MB band 356 < 9216 guard, util 100 > 80 -> VERDICT=NO-GO (steady saturated)\n")
ev.write("== ollama probe: GEN-ERROR transport=TimeoutError face=busy-contended\n")
ev.write("== viewing: meme outbound zero new (V1 mp4 not landed); frames_full N03_goddess_pass.png 23:08:37 new (new anchor); others zero new\n")
with io.open(os.path.join(".c3-tmp", "r1922_probes.txt"), "w", encoding="utf-8", newline="") as f:
    f.write(ev.getvalue())

# append actual probe outputs
for cmd in [
    ["python", "src/os/loop_health.py", "--loop"],
    ["python", "src/readiness.py", "--summary"],
    ["python", "src/board_check.py"],
    ["python", "src/os/gpu_window_gate.py", "--samples", "4", "--util-max", "80"],
]:
    try:
        out = subprocess.run(cmd, capture_output=True, timeout=180)
        txt = (out.stdout or b"") + (out.stderr or b"")
        with io.open(os.path.join(".c3-tmp", "r1922_probes.txt"), "ab") as f:
            f.write(("\n--- %s (rc=%s) ---\n" % (" ".join(cmd[1:3]), out.returncode)).encode("utf-8"))
            f.write(txt[:4000])
    except Exception as e:
        with io.open(os.path.join(".c3-tmp", "r1922_probes.txt"), "ab") as f:
            f.write(("\n--- %s EXC %r ---\n" % (" ".join(cmd[1:3]), e)).encode("utf-8"))
print("r1922_probes.txt written")
print("CLOSE-OK")
