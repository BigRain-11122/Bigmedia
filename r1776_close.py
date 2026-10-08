# R1776 closeout: state.json tick/log/focus/ts/task + status-export refresh
import json
import os
import time

TS = time.strftime("%Y-%m-%d %H:%M:%S")

LOG_LINE = (
    "2026-10-08 " + TS.split(" ")[1] + " R1776: 生产轮·#109 夜窗腿起跑=27b GGUF 选档定谳 UD-Q2_K_XL+CosyVoice3 取件路径定夺+双下载在飞 27MB/s"
    "（R1775 下步指针③兑现·state 焦点夜窗位）——轮首五查静（origin_gap_check QUIET ahead=0 behind=0=R1500 前置位/decisions dnum 内容寻址差集 NEW=[] 水位 175 维持/ledger @BigStream 3 行==R1775 值锚静默转办/own orders 锚 O-20261008-1105 mtime 12:08==R1733 锚维持/无 index.lock/树态=mv0001 M+untracked bm-c sprint 承载预期态==R1775 同口径）"
    "+三探针基线平（board 0 FAIL 5 题 10 稿 5 in production/readiness 3 阻塞皆外部 CEO 件〔账号批次①+M4 GATE 6/10+#17〕0 发现/loop_health 2F+166W 契约基线持平零新增〔两 outage=09-26/09-28 史实已裁定+drift 带内 adjudicated 基线〕）"
    "+AIHOT 守卫核一行=栈三件全活（api 200 {ok,db:ok}+web 200+worker 39108 在役·GPU 6618MiB/12282MiB=磨链间隙轻载态·零干预纪律维持·明晨 08:00 compose 位首份真日报三问判据收官点不变·窗 ≤10-10 12:00）"
    "——主活三腿：①27b 选档定谳=hf-mirror API 实读正主仓 unsloth/Qwen3.8-27B-GGUF（6.5M 下载·lastModified 2026-08-20 世代新档·27 量化档全列）→**UD-Q2_K_XL 9.83GB 选中**（选档判据=本机 12282MiB 实测 Q2~Q4 带内最优：IQ3_XXS 10.93GB 起全卡告急 KV cache 无位·Q2_K_XL 独占窗可容 ~1.6GB KV=剧本重档 A/B 独占窗可行·27b 无法与 AIHOT 14b-8k 共驻=独占位模型定谳）+精确字节锚 9,828,981,664B+ETag 66781ed7+Accept-Ranges 断点续 200（三闸：能用=unsloth 官方 Dynamic 正仓 ✓/新旧 ✓/速度=起飞实测过闸）；"
    "②CosyVoice3-0.5B 取件路径定夺=hf-mirror 官方仓 FunAudioLLM/Fun-CosyVoice3-0.5B-2512 直拉快照（159,867 下载·2026-02-03 档·非 pip/git 全装=运行时装包归 #108 TTS 腿）·核心件集实测 8.76GB 全量>板面原估 1-2GB → 裁夺=最小推理集 ~5.76GB（llm.pt 2.02〔非 RL 档〕+flow.pt 1.33+flow.decoder.estimator.fp32.onnx 1.33+speech_tokenizer_v3.onnx 0.97〔非批档〕+hift.pt 0.083+campplus 0.028+configs 三件·llm.rl.pt/batch.onnx 变体档延后随 #108 按需补）；"
    "③双下载夜窗起飞=发射器 data/assets/model-pulls/pull_night_r1776.py（DETACHED|CREATE_NEW_PROCESS_GROUP|CREATE_NO_WINDOW 零窗 U060 合规·curl -L -C - --retry 8 断点续+逐件字节精确校验+ASCII 日志·27b 先拉 CosyVoice 集顺序续·起法=R1752 python 直起工艺）PID 57396 23:37:40 START·12s 295MB=27MB/s 起步实证（R1764 qwen3.5:9b 28MB/s 同位）·收账读数 34.5% 在飞（3,388,661,760B·~9.4MB/s 均速）"
    "——余腿=完成核（逐件字节校验+日志 DONE-OK 判读随下轮）+ollama create 27b Modelfile 派生（独占窗执行+共卡让路 nvidia-smi 前置）+加载试跑（#108 剧本重档 A/B 位就绪锚）"
    "·例行列=日报 10-08 在案不重跑/GB 闸 v1.3 10-15 距今 7 天内跳过/W41 周审在案/10-10 B3 W41 周更带外/HQ-FEEDBACK 不写（无集团层新 open 问题零膨胀）/tokens:local=0（脚本探针+HTTP 采集零模型调用·P-54 平）"
    "——下轮=R1777 路首读三项（双下载完成核/AIHOT 明晨 08:00 compose 位三问判据=须带真实况收账/#111 outbound 随轮盯）"
)

FOCUS = (
    "夜窗腿承接中·#109 双下载在飞（27b UD-Q2_K_XL 9.83GB 收账读数 34.5%+CosyVoice3 最小推理集 5.76GB 顺序续·PID 57396·余腿=完成核+Modelfile 派生+加载试跑随轮领=#108 剧本重档 A/B 位）"
    "·#107 AIHOT 静磨零干预（14b-8k scored 159/ge60=54·归组队列排空 ≈明晨 06:00·明晨 08:00 版窗 compose 位首份真日报三问判据收官〔质量问已过·窗 ≤10-10 12:00〕）"
    "·#110 余腿=UI 端点配置人工点+ComfyUI 桥+1 集实测"
    "·#111 bm-c MV 样图分镜在产（bm-a 查看位·CEO 三选项待勾选）"
    "·REACT-v12 10-09（F-167·日报先补产）"
    "·#99 blocked-on-channel（SLA ≤10-13）"
    "·git 一律 python subprocess 真实 git.exe（R1756/R1761 红注）"
)

# --- state.json ---
sp = r"src\os\state.json"
with open(sp, encoding="utf-8") as f:
    st = json.load(f)
st["tick"] = 1776
st["focus"] = FOCUS
st["ts"] = TS
st["task"] = LOG_LINE.split(" ", 3)[3][:60]
st.setdefault("log", []).append(LOG_LINE)
with open(sp, "w", encoding="utf-8") as f:
    json.dump(st, f, ensure_ascii=False, indent=1)
with open(sp, encoding="utf-8") as f:
    json.load(f)  # validate

# --- status-export.json ---
ep = r"docs\status-export.json"
with open(ep, encoding="utf-8") as f:
    ex = json.load(f)
ex["export_ts"] = TS
ex["outs"][0] = (
    "OS 循环 tick 1776，R1776 生产轮（#109 夜窗腿起跑：27b GGUF 选档定谳=unsloth/Qwen3.8-27B-GGUF UD-Q2_K_XL 9.83GB〔12282MiB 卡 Q2~Q4 带内最优·IQ3_XXS 10.93GB 起全卡告禁·独占位模型定谳〕+CosyVoice3-0.5B 取件路径定夺=官方仓 FunAudioLLM/Fun-CosyVoice3-0.5B-2512 直拉快照最小推理集 ~5.76GB〔核心件集实测 8.76GB>原估·rl/batch 变体档延后〕+双下载夜窗起飞 27MB/s〔PID 57396·收账读数 34.5% 在飞·三闸全预过：unsloth 官方+2026-08-20 新档+速度实测〕=#108 剧本重档 A/B 位就绪链）"
    "·AIHOT 静磨零干预（14b-8k scored 159/ge60=54·归组排空 ≈明晨 06:00→明晨 08:00 compose 位首份真日报三问判据收官·窗 ≤10-10 12:00）"
    "·MV 产线=bm-c 在产（bm-a 查看位·CEO 三选项 A/B/C 待勾选）·#99 blocked-on-channel（SLA ≤10-13）；当前活=夜窗双下载值守·下轮=下载完成核+AIHOT 明晨收官读数+#111 outbound 盯；最近实物=OH-20261008-bigstream.md+Toonflow 便携装机+AIHOT 全栈+MV 样片 v2；下个里程碑=AIHOT 首份本地日报三问〔明晨 08:00 compose 位·窗 ≤10-10 12:00〕"
)
ex["live"][0] = (
    "当前活：2026-10-08 23:4x R1776 生产轮=#109 夜窗腿起跑（27b 选档定谳 UD-Q2_K_XL 9.83GB+CosyVoice3 取件路径定夺=官方仓直拉快照最小推理集 5.76GB+双下载在飞 27MB/s·收账读数 34.5%）"
    "+AIHOT 静磨零干预（14b-8k scored 159/ge60=54·归组排空 ≈明晨 06:00→明晨 08:00 compose 位首份真日报三问判据收官〔质量问已过·窗 ≤10-10 12:00〕）"
    "·下轮=双下载完成核/AIHOT 明晨收官读数/#111 outbound 盯（bm-a 查看位）/#99 blocked-on-channel（SLA ≤10-13）"
)
ex["live"][1] = (
    "最近实物：Qwen3.8-27B-UD-Q2_K_XL GGUF+CosyVoice3 核心集夜窗下载在飞（23:37 起飞 27MB/s·data/assets/models/ gitignored 辖区·PID 57396）"
    "+OH-20261008-bigstream.md OSS 窗 5 切片 1 台账件（23:14·C:/Users/sjs20/Desktop/FluxGroup/cph4/oss-harvest/OH-20261008-bigstream.md）"
    "+Toonflow v2.0.4 便携装机+launch 核验毕（22:53·C:/Users/sjs20/tools/ToonFlow/app/toonflow·Ollama 端点 200）"
    "+qwen2.5:14b-8k 派生模型入库（21:4x·ollama 本地册）"
    "+AIHOT「雷达日报」全本地栈在役（api 3101+worker 39108+web 3100+PG 55432·scored 159 件 max 83.0）"
    "+MV 风格样图 5 张+分镜呈审包（18:23·CEO 三选项 A/B/C 待勾选·C:/Users/sjs20/Desktop/FluxGroup/fleet/mv0001-handover/outbound/REVIEW-PACKAGE-v1.md）"
    "+MV0001 样片 v2（14:0x·234.25s 720P 59 镜十场）+F-166 DAILY v70（13:20）+「板块十年」五件 F-160~F-164"
)
ex["live"][2] = (
    "下个里程碑：#109 双下载完成核+27b Modelfile 派生+加载试跑（ETA ~1h 内随轮领·#108 剧本重档 A/B 位就绪锚）"
    "+AIHOT 首份本地日报三问判据（归组排空 ≈明晨 06:00→selected 翻转核→明晨 08:00 版窗 compose 位→质量〔已过〕/聚簇/资源三问·窗 ≤10-10 12:00→过=接城市信源+换名换标/判负=关线留痕）"
    "+#110 Toonflow 余腿（UI 端点配置一次性人工点→1 集漫剧实测·72h 窗）"
    "+OSS w5 剩余切片（窗 10-08 21:40→10-11 21:40·视 #107 判据收官态定夺）"
    "+MV CEO 勾选三选项→视频段解冻→20 秒样片+REACT-v12 10-09（F-167·日报先补产）"
    "+#99 SLA ≤10-13+10-10 B3 W41+W42 周轮件 10-12+BigHouse P3 10-28"
)
with open(ep, "w", encoding="utf-8") as f:
    json.dump(ex, f, ensure_ascii=False, indent=1)
with open(ep, encoding="utf-8") as f:
    json.load(f)  # validate

print("close ok ts", TS, "tick", st["tick"], "task", st["task"])
print("27b partial bytes now", os.path.getsize(
    r"data\assets\models\Qwen3.8-27B-GGUF\Qwen3.8-27B-UD-Q2_K_XL.gguf"))
