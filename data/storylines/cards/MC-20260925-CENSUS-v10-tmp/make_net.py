# R300: build E4 net-verdict file for MC-20260925-CENSUS-v10 (file-to-file verbatim copy, no console Chinese)
import io, json

src = io.open(r"data\storylines\cards\MC-20260925-CENSUS-v10-tmp\e4-result.json", encoding="utf-8")
d = json.load(src)
verdict = d["verdict"]

out_path = r"docs\reviews\expert-verdicts\20260925-230734-E4-audience.md"
text = (
    "# E4-audience 参考仪净本 · MC-20260925-CENSUS-v10《城市图鉴 010·老晶振》（2026-09-25 23:07:34 落地·同轮回填·Start-Process 脱壳后台热载快落）\n"
    "\n"
    "> 席位：E4-audience 直觉观众（非名册席直调·qwen2.5:14b 本地 Ollama·dept-review §6 双态制·非拦截参考席）·wrapper=`data/storylines/cards/MC-20260925-CENSUS-v10-tmp/e4_call.py`（R299 同型·UTF-8 stdin 管道+ANSI/盲文清洗）·盲评材料律合规零嵌审计史。\n"
    "> 材料：静态居民图鉴卡 1080×1080（cards.json+渲染输出+图鉴语境背景段）。轮次：R300 同轮回填。\n"
    "\n"
    "## 判词（verbatim 净本）\n"
    "\n"
    + verdict + "\n"
)
io.open(out_path, "w", encoding="utf-8").write(text)
print("NET-OK", out_path)
