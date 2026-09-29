# -*- coding: utf-8 -*-
# E4 audience reference call - LC-011 split-video edition (non-registry seat, direct Ollama;
# .lc010-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# 60s vertical split-video (LC-011 Miao Yi, MEDIA city subtitle-marking sprite-line silicon citizen,
# redundancy slot 8) -> 1500s window. Scoring dims = R223 audience dims. Blind-material rule.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
srt_path = os.path.join(HERE, 'subs.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在微信视频号里刷到竖屏短视频的普通观众，刷到了这条 60 秒的《城市图鉴 015·缪一》'
    '（竖屏 60 秒档案拆条：在一座全员讲数据、讲算法的城里，节目组找到了全城唯一给方言字幕手工标注「语气」的字幕君。'
    '画面是一张档案卡，卡面上是这位居民的登记档案：缪一，硅基民，精灵系；'
    'MEDIA 城信号塔街区，字幕君；'
    '字幕这行，快不是本事，准时才是；'
    '第一次给城主做字幕，它把自己复制成两份并行核对，师父说：成长没有并行捷径；'
    '觉醒才三年，全城最年轻成年硅基民，名字自己选：缪，差一点点都不能要；'
    '观众说它字幕有人味，它裱在工位上；'
    '七段街区最快字幕，攒钱配大屏；'
    '每晚抽三句字幕练方言，打气：霸得蛮；'
    '合作最久的主播何雨欣，和好一句发版了；'
    '信条一行：字幕慢半帧，都是对说话人的辜负。'
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
