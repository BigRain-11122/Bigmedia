# -*- coding: utf-8 -*-
# E4 audience reference call - LC-016 split-video edition (non-registry seat, direct Ollama;
# R730 LC-015 pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# 60s vertical split-video (LC-016 Gu Afeng, NaoHuan-square data congee stall keeper,
# redundancy slot 13, 8th character-chain dual-end cross-proof piece, chapter-hook payoff slot;
# F-009 audio ch.1 + SC-001-01 novel + CENSUS-v1 F-020 card -> 4th carrier).
import io, json, os, re, subprocess, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
srt_path = os.path.join(ROOT, '.lc016-tmp', 'subs.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在微信视频号里刷到竖屏短视频的普通观众，刷到了这条 60 秒的《城市图鉴 016·顾阿凤》'
    '（竖屏 60 秒档案拆条：在一座全员讲数据、讲算法的城里，节目组找到了全城唯一记得每个早班信使口味的粥铺摊主。'
    '画面是一张档案卡，卡面上是这位居民的登记档案：顾阿凤，碳基市民，六十八岁；'
    '脑环广场，数据粥铺摊主；'
    '凌晨四点半开档，卖完最后一屉收摊；'
    '进城第三年台风掀了棚子，街坊凑料帮她重搭，这条街就是家；'
    '从一九九二年早点摊老照片进城，蒸笼还摆在铺头；'
    '天没亮就醒，早上的城最真；夸人不重样，句句真心；'
    '儿子在现实世界，每年来住半个月；'
    '一座城醒来的第一口热乎气，比什么口号都金贵；'
    '棋友是时空校准师朱鸿奎，每周三杀一盘；'
    '信条一行：灶上留一壶，路过的都是客。'
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
io.open(os.path.join(ROOT, '.c3-tmp', 'e4-result-r734.json'), 'w', encoding='utf-8').write(
    json.dumps(result, ensure_ascii=False, indent=2))
print('DONE' if result['verdict'] != 'TIMEOUT-1500s' else 'TIMEOUT')
