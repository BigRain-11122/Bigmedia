# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20260926-REACT-v1 static hot-reaction card (non-registry
# seat, direct Ollama; v17 e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for REACT form first piece. Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态热点反应卡《城市速报 001》'
    '（1080×1080 方图·黑底；顶部标题「城市速报 001」；下面六行：'
    '「今日热点 · 知乎热榜 2026-09-26」'
    '「为什么下雨时，鸭子不跑反而在雨中站着一动不动的？」'
    '「秩序轴：「雨中行人，各有各的风度」」'
    '「求新轴：「打伞的少年，是不是偷偷喜欢淋雨？」」'
    '「像素灵池：「啾啾鸣叫，雨中觅食欢腾」」'
    '「硅基城市雨天律：人人进骑楼，路面可见不到三成」；'
    '图内底部来源行「热点转述自知乎热榜·反应取自台词池（虚构）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）打造的虚拟城市，'
    '城里住着一万多名虚构居民，分属六种思想派系（秩序轴/求新轴/怀旧轴/烟火轴/侠气轴/逍遥轴）；'
    '这张卡是一个日更系列的第一张：当天知乎热榜上有个热议问题「为什么下雨时，鸭子不跑反而在雨中站着一动不动的？」'
    '（提问时间是 2026 年 9 月 26 日），这张卡把这个问题原样转述过来，'
    '然后让硅基城市的虚拟居民用他们自己的「台词池」语气短句来反应——'
    '「雨中行人，各有各的风度」是秩序轴居民下雨天常说的话；'
    '「打伞的少年，是不是偷偷喜欢淋雨？」是求新轴居民的调侃；'
    '「啾啾鸣叫，雨中觅食欢腾」是像素灵（城里的小鸟型生物）的池句；'
    '最后一行「硅基城市雨天律：人人进骑楼，路面可见不到三成」是这个城市自己的设计设定——'
    '这座城下雨天居民都会躲进骑楼，街面上的人不到晴天的三成，'
    '所以全城人都在檐下看那只站着淋雨的鸭子。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260926-REACT-v1 static card (cards.json + render output)'}
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
