# -*- coding: utf-8 -*-
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一个刷手机公众号图文的普通市民读者（生活在硅基城市隔壁的现实城里，'
    u'每天通勤刷热点）。下面是「城市速报」系列的静态速报卡《城市速报 011》卡面全文'
    u'（1080×1080 方图，黑底，排版从上到下）：'
    u'卡头是「城市速报 011」，下一行是「今日热点 · 知乎热榜 2026-10-08」，'
    u'中间一行是热点转述：「世界上最宜居的城市是哪一座？」'
    u'（这是知乎热榜上的一个真实热榜问题，讨论哪座城市算世界上最宜居）。'
    u'接着是三条虚构城市居民的反应：「侠气轴：『街坊邻居得互相照应，这日子才过得多舒心』」'
    u'（热心肠的街坊说邻里互相照应日子才舒心）、「烟火轴：『早点摊上的粥，比啥都管用』」'
    u'（早点摊主说一碗热粥比什么都管用）、「逍遥轴：『热茶暖身又暖心，寒风中多一分闲适』」'
    u'（爱清闲的茶客说寒风里喝热茶身心都暖、多一分闲适）。'
    u'最后是收束行「食堂大厨信条：『行情再绿，汤是热的。』」'
    u'（城里食堂的大厨认为不管行情好坏，汤永远是热的）。'
    u'图内底部有来源行「热点转述自知乎热榜·反应与信条皆取自虚构城市档案」，'
    u'左上角有 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景设定：这是一个 AI 全自动运转的媒体公司出品的城市速报栏目，'
    u'虚拟硅基城市里的居民档案、台词都由城市系统生成；热点是现实热榜真实转述。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20261008-REACT-v11 static card (cards.json + render output)'}
try:
    p = subprocess.run(['ollama', 'run', 'qwen2.5:14b'], input=prompt.encode('utf-8'),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1500)
    raw = p.stdout.decode('utf-8', errors='replace')
    cleaned = re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', raw)
    cleaned = re.sub(u'[⠀-⣿]', '', cleaned)
    result['verdict'] = cleaned.strip()
except subprocess.TimeoutExpired:
    result['verdict'] = 'TIMEOUT-1500s'
io.open(os.path.join(HERE, 'e4-result.json'), 'w', encoding='utf-8').write(
    json.dumps(result, ensure_ascii=False, indent=2))
print('DONE' if result['verdict'] != 'TIMEOUT-1500s' else 'TIMEOUT')
