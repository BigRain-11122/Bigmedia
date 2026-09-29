# -*- coding: utf-8 -*-
# E4 audience reference call - LC-015 split-video edition (non-registry seat, direct Ollama;
# R726 LC-014 pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# 60s vertical split-video (LC-015 Zhu Hongkui, archive-district time-calibration watchmaker,
# redundancy slot 12, 7th character-chain dual-end cross-proof piece, F-010 audio-line same persona).
import io, json, os, re, subprocess, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
srt_path = os.path.join(ROOT, '.lc015-tmp', 'subs.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在微信视频号里刷到竖屏短视频的普通观众，刷到了这条 60 秒的《城市图鉴 015·朱鸿奎》'
    '（竖屏 60 秒档案拆条：在一座全员讲数据、讲算法的城里，节目组找到了全城唯一用机械钟声对时的修表匠。'
    '画面是一张档案卡，卡面上是这位居民的登记档案：朱鸿奎，碳基市民，七十四岁；'
    '档案馆区，时空校准师；'
    '只开一盏暖灯，强光看不清游丝；'
    '第一次给交易所时钟全城对时，误差压进微秒，他坐到天亮；'
    '从一九七五年钟表柜台合影进城，揣着没修完的最后一块表；'
    '再新的城，按老礼数过日子，数据对不上，觉都睡不好；'
    '两个徒弟，一个碳基，一个硅基；端三十年汤，一滴没洒过；每周三粥铺杀棋，输了免费校表；'
    '硅基徒弟归档者-07，比碳基的还像老派人；'
    '信条一行：差之毫秒，谬以全城。'
    '全部基于城市真实居民档案改编；配音是轻度赛博机械感的机器叙述者，以城市系统日志自述视角讲述；'
    '画面带 AI 生成标识。口播全文如下）：\n\n'
    + transcript + '\n\n'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会看完这 60 秒吗？会点赞或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b', 'material': srt_path}
try:
    p = subprocess.run(['ollama', 'run', 'qwen2.5:14b'], input=prompt.encode('utf-8'),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1500)
    raw = p.stdout.decode('utf-8', errors='replace')
    cleaned = re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', raw)
    cleaned = re.sub(u'[\u2800-\u28ff]', '', cleaned)  # braille spinner range (R189 lesson)
    result['verdict'] = cleaned.strip()
except subprocess.TimeoutExpired:
    result['verdict'] = 'TIMEOUT-1500s'
io.open(os.path.join(ROOT, '.c3-tmp', 'e4-result-r730.json'), 'w', encoding='utf-8').write(
    json.dumps(result, ensure_ascii=False, indent=2))
print('DONE' if result['verdict'] != 'TIMEOUT-1500s' else 'TIMEOUT')
