# R1791 export surgery: restore 1789 results entry from HEAD verbatim, remove chips 1790 anomaly,
# keep results [.. 1786, 1789, 1790, 1791], refresh live lines + export_ts. Validated reload after write.
import json, subprocess, sys, io, time

EXPORT = "docs/status-export.json"
GIT = r"C:\Program Files\Git\cmd\git.exe"

# 1. original 1789 + 1790 texts from HEAD (verbatim fidelity)
head_raw = subprocess.run([GIT, "show", "HEAD:" + EXPORT], capture_output=True).stdout.decode("utf-8")
head = json.loads(head_raw)
r1789 = [e for e in head["results"] if e[0] == "1789"]
r1790_head = [c for c in head["chips"] if c[0] == "1790"]
if not r1789:
    print("FATAL: no 1789 entry in HEAD results"); sys.exit(1)
if not r1790_head:
    print("FATAL: no 1790 anomaly in HEAD chips"); sys.exit(1)
text_1789 = r1789[0][1]
text_1790 = r1790_head[0][1]
print("HEAD 1789 entry len:", len(text_1789))
print("HEAD 1790 anomaly len:", len(text_1790))

# 2. current file
cur = json.load(io.open(EXPORT, encoding="utf-8"))
r1791 = [e for e in cur["results"] if e[0] == "1791"]
if not r1791:
    print("FATAL: current results missing 1791 entry"); sys.exit(1)
text_1791 = r1791[0][1]

# 3. rebuild: chips = clean [name, live] pairs only; results tail = 1786, 1789(restored), 1790(plain), 1791
cur["chips"] = [c for c in cur["chips"] if c[0] != "1790"]
keep = [e for e in cur["results"] if e[0] not in ("1789", "1790", "1791")]
cur["results"] = keep + [["1789", text_1789], ["1790", text_1790], ["1791", text_1791]]

# 4. live three lines (F3 derive from R1791 reality)
cur["live"] = [
    "当前活：2026-10-09 05:5x R1791 生产轮·#108 漫剧 PoC T2I gate 升档收口起跑腿毕——三闸预核（「Qwen-Image-2.0」字面仓不存在→2.1 现行线定谳·Comfy-Org 官方打包 mod 2026-09-29）+路线裁决 GGUF→ComfyUI 原生量化三件套（0.37.0 native qwen_image21 源码实证·零节点依赖）+14.24GB 三件套 DETACHED 拉取在飞（~25MB/s 夜窗带）；AIHOT 08:00 compose 位首份真日报三问判据收官点维持（栈零干预·08:00 前禁重扫）",
    "最近实物：MD-0001《台风梅花夜》T2I 升档模型位拉取件在飞（2026-10-09 05:29 起飞·拉取日志 C:\\Users\\sjs20\\Desktop\\FluxGroup\\media\\BigStream\\data\\assets\\model-pulls\\qwenimage21-native-r1791.log·发射器同目录 pull_qwenimage_r1791.py·三件套落位 C:\\Agent\\ComfyUI\\models\\{diffusion_models,text_encoders,vae}\\·完成核随下轮·#108 判据窗 72h 至 ~10-11）",
    "下个里程碑：R1792 首读三项=①Qwen-Image-2.1 三件套完成核（DONE-OK+字节锚复核）②AIHOT 08:00 compose 位首份本地日报三问判据收官读数（须带真实况·窗 ≤10-10 12:00）③runner 原生 DiT 工作流适配+残余镜 03/10/11 重 roll→gate 复核 ≥8/9→合成→S2+E8→M4→F 登记（#108 判据窗 72h 至 ~10-11）+15:07 盘燃复测预警位（MV 产线减负案条件触发点）"
]

cur["export_ts"] = time.strftime("%Y-%m-%d %H:%M:%S")

# 5. write + validate
with io.open(EXPORT, "w", encoding="utf-8", newline="\n") as f:
    json.dump(cur, f, ensure_ascii=False, indent=1)
    f.write("\n")
chk = json.load(io.open(EXPORT, encoding="utf-8"))
print("RELOAD OK")
print("chips:", len(chk["chips"]), "entries; last:", chk["chips"][-1][0])
print("results ticks:", [r[0] for r in chk["results"]])
print("export_ts:", chk["export_ts"])
print("live lines:", len(chk["live"]))
