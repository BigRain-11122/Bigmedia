# -*- coding: utf-8 -*-
# E4 audience reference call - LC-012 split-video edition (non-registry seat, direct Ollama;
# .lc011-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# 60s vertical split-video (LC-012 Pan Zhiming, MEDIA city topic-gate keeper,
# redundancy slot 9, content-line three-craft closure piece) -> 1500s window.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
srt_path = os.path.join(HERE, 'subs.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在微信视频号里刷到竖屏短视频的普通观众，刷到了这条 60 秒的《城市图鉴 014·潘志明》'
    '（竖屏 60 秒档案拆条：在一座全员讲数据、讲算法的城里，节目组找到了全城唯一保留「毙稿理由档案」的选题官。'
    '画面是一张档案卡，卡面上是这位居民的登记档案：潘志明，碳基市民，原生代，四十七岁；'
    'MEDIA 城选题馆街区，选题官；'
    '每天毙稿三十留下三个；'
    '迫于人情放过一篇查不实的稿，第二天凌晨自己撤了，立规矩：选题官的笔不认人情；'
    '城生城长，爹是初代建城工人，编年史里查得到名字，总觉得有双眼睛看着；'
    '生气不骂人，只把红笔按得很重；'
    '带着五个年轻选题官，每周雷打不动去留言墙拆信；'
    '选题馆是城的心电图室，哪条街在笑、哪条街在熬夜，纸上都有波形；'
    '最服气的主播是何雨欣，她那期方言直播，他抄了三页笔记；'
    '信条一行：毙稿不毙人，选题选良心。'
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
    cleaned = re.sub(u'[\u2800-\u28ff]', '', cleaned)  # braille spinner range (R189 U+2800 lesson)
    result['verdict'] = cleaned.strip()
except subprocess.TimeoutExpired:
    result['verdict'] = 'TIMEOUT-1500s'
io.open(os.path.join(HERE, 'e4-result.json'), 'w', encoding='utf-8').write(
    json.dumps(result, ensure_ascii=False, indent=2))
print('DONE' if result['verdict'] != 'TIMEOUT-1500s' else 'TIMEOUT')
