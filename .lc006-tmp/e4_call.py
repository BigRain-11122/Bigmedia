# -*- coding: utf-8 -*-
# E4 audience reference call - LC-006 split-video edition (non-registry seat, direct Ollama;
# .lc005-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# 60s vertical split-video (LC-006 Lamp No.14, redundancy-expansion slot 3) -> 1500s window.
# Scoring dims = R223 audience dims. E4 must NOT see meta version info (blind-material rule).
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
srt_path = os.path.join(HERE, 'subs.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在微信视频号里刷到竖屏短视频的普通观众，刷到了这条 60 秒的《城市图鉴 019·十四号路灯》'
    '（竖屏 60 秒档案拆条：在一座全员讲数据、讲算法的城里，节目组找到了全城唯一在台风夜把自己亮度开满格的'
    '灯灵。画面是一张档案卡，卡面上是这位灯灵的登记档案：十四号路灯，像素灵，夜灯员，独行客的护送者，'
    '天亮交晨；全城对频那一秒它亮起，编号十四；它照着桥上哭的年轻人坐到天亮，那人鞠躬；它把外环照成白昼，'
    '检修日志超载运行、无损耗、原因不明，它说知道，不能说；灯罩补丁是台风梅花留的，疤是资历；'
    '经过的人，多亮一档，夜宵摊，再亮半档；雾天和渡轮船长陆海峰对暗号，两长一短：这段有我；'
    '它最惦记跑夜单的高小满：伞在包里，永远不撑；信条一行：灯不问来路，只管照路。'
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
