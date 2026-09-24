# -*- coding: utf-8 -*-
"""R182: clean E4 verdict ANSI pollution + archive to expert-verdicts.

e4_call.py regex \x1b[[0-9;]*[A-Za-z] misses '?25l/h' cursor codes (R177 fixed
the same class in call_expert.call_model; e4_call.py was not updated). Clean
the stored result, rewrite e4-result.json, archive the full verdict."""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RESULT = REPO / ".bs003-tmp" / "e4-result.json"
ARCHIVE = REPO / "docs" / "reviews" / "expert-verdicts" / "20260925-003726-E4-audience.md"

data = json.loads(RESULT.read_text(encoding="utf-8"))
raw = data.get("verdict", "")
clean = re.sub(r"\x1b\[[0-9;?]*[a-zA-Z]", "", raw)
clean = re.sub(r"[\u2800-\u28ff]", "", clean)          # braille spinner frames
clean = re.sub(r"[ \t]+", " ", clean)
clean = re.sub(r"\n{3,}", "\n\n", clean).strip()

data["verdict"] = clean
RESULT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

header = """# E4-audience - 直觉观众（评审团参考仪·非部门名册席）结论全文

> 时间=2026-09-25 00:24-00:37（第三飞落地）· 模型=qwen2.5:14b（本地 Ollama·零 API）· 材料=data/sources/bs3/voiceover-v5.beats.txt（12 拍全文）+画面语境（实录素材：OS 循环日志/值守屏/评审台账·字卡锚点数字）
> 机制=E4 双态制（dept-review-mechanism §6·开发期=Ollama 参考仪·读数如实记录不作拦截）——E 席不属部门名册故无 call_expert registry id·直调脚本=.bs003-tmp/e4_call.py（第三飞 Start-Process 脱壳·R180 首两飞丢失实证在案·1500s 窗内 13 分钟落判）·调用落账=review-20260925-bs003-v1.md §二 E4 行（R182 回填）；判词原档 ANSI ?25l/h 光标码污染=e4_call 正则缺 ? 类（R177 call_model 同型坑）·R182 洗档后本件为净本

"""
footer = """

> 判读（循环侧）：7 分会看完=批次① E4 参考线最高读数（BS-002 E4=3 分不看完→BS-003 7 分看完·两稿同 wrapper 同通道可比）；「科技感+信息量+逻辑性吸引看完」与 E1/E8 席读数同向；旗面 b3「心跳在册/10 分钟必达·20 分钟判离线」+b6「协作实录/互相派活·互相写回执」概念堆砌旗与 E2 席「交货判据」术语半技术腔观察同位互证=b6 拍面迭代输入（BS-004 拍稿已起链·下一件吸收位）；最弱=b6 协作实录拍（缺具体情境案例）——E4 双态制口径：非拦截席·读数如实留档。
"""
ARCHIVE.write_text(header + clean + footer, encoding="utf-8")
print("ARCHIVED:", ARCHIVE.name)
print("CLEAN VERDICT:")
print(clean[:600])
