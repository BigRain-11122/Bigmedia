# -*- coding: utf-8 -*-
"""MV-0001《爱在西元前》风格测试片段·立意生成腿（Ollama qwen2.5:14b·本地零云）
CEO 令 P-2026-10-08-05 第四追加令：先出几十秒片段供看方向，再出完整版。
消费输入=R-20261008-mv-fandemand-01 粉丝需求谱（已归位）。"""
import json, urllib.request, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]  # media/BigStream/
OUT = pathlib.Path(__file__).parent
OUT.mkdir(parents=True, exist_ok=True)

FAN = """粉丝需求谱要点（集团调研件 R-20261008-mv-fandemand-01·B站A+豆瓣B+知乎C 三社群互证）：
1. 情感锚点=「两河文明知识考古浪漫」（楔形文字/汉谟拉比法典被粉丝当知识点背诵·B站热评21280赞）+入坑曲初恋记忆+「橱窗前凝视碑文/我欣赏你的脸」画面；原曲豆瓣9.2分。
2. 雷区=魔改歌词知识点/戏说法典/脱离歌词意象空堆设定（2019官方动画差评先例）。
3. 非写实热度=修复怀旧(986万播放)＞翻唱质感＞手书段落＞AI改编；「风格多元化可行但每段须锚回歌词原文」。"""

PROMPT = FAN + """
你是 BigStream 的 MV 立意师。为周杰伦《爱在西元前》改编 MV（非写实/风格多元/立意高级不低俗）出 5 个互不相同的立意方案。
硬约束：①立意高级、禁低俗（禁擦边/土味情爱/廉价梗）②每个方案锚定歌词原文意象（楔形文字/汉谟拉比/底格里斯河/美索不达米亚/橱窗凝视/祭司神殿等）③互相风格差异大（多元化）④方案要能落地为非写实视觉（说明视觉形态与主色调）⑤粉丝证据导向。
只输出 JSON 数组（UTF-8），每项字段：{"id": 1-5, "title": "四字内方案名", "logline": "一句话立意(30字内)", "visual": "视觉形态+主色调(40字内)", "anchor": "锚定的歌词/意象", "opening": "开场画面一句话(25字内)"}。不要输出其他文字。"""

def main():
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=json.dumps({"model": "qwen2.5:14b", "prompt": PROMPT,
                         "stream": False, "options": {"temperature": 0.8}}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        data = json.loads(r.read().decode("utf-8"))
    text = data.get("response", "")
    (OUT / "_ollama_raw.txt").write_text(text, encoding="utf-8")
    s, e = text.find("["), text.rfind("]")
    if s < 0 or e < 0:
        print("NO_JSON"); sys.exit(2)
    ideas = json.loads(text[s:e+1])
    (OUT / "concepts.json").write_text(json.dumps(ideas, ensure_ascii=False, indent=1), encoding="utf-8")
    print("OK", len(ideas), "ideas ->", OUT / "concepts.json")

if __name__ == "__main__":
    main()
