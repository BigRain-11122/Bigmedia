# -*- coding: utf-8 -*-
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态热点反应卡《城市速报 013》'
    u'（1080×1080 方图·黑底；顶部标题「城市速报 013」；来源行「今日热点 · 知乎热榜 2026-10-10」；'
    u'热点标题两行「为什么很多人买新能源车之前很兴奋，/开了一年后却开始怀念燃油车？」；'
    u'下面三行城市居民反应：「求新轴：「新上市的玩意儿真让人眼睛都花了」」「怀旧轴：「老货郎说，旧物总比新玩意儿耐看」」'
    u'「秩序轴：「买卖交易，谨慎行事，别轻敌，得稳住」」；收束行「穿城信使信条：「急件不急，稳到才算到。」」；'
    u'图内底部声明行「热点转述自知乎热榜·反应与信条皆取自虚构城市档案」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），'
    u'城里住着一万名登记居民。台词池按六种「轴」收录居民的话，户籍卡记录每位居民的姓名职业和信条。'
    u'这张卡的玩法是「热点城市反应」：把当天知乎热榜上大家都在讨论的现实热点，'
    u'原样转述给虚构城市的居民，让他们用自己的话反应——所以热点是真实的、反应是虚构的，底部声明行就是这个意思。'
    u'今天的热点是：很多人买新能源车之前特别兴奋，开了一年之后却开始怀念燃油车，知乎上正在讨论为什么。'
    u'城市居民的三个反应：求新轴居民说新上市的玩意儿真让人眼睛都花了（新车上市看花眼=买之前兴奋的正身）；'
    u'怀旧轴的老货郎说旧物总比新玩意儿耐看（开一年后怀念燃油车的城市正身——旧物与新玩意儿正好对上燃油车与新能源车）；'
    u'秩序轴居民叮嘱买卖交易谨慎行事别轻敌得稳住（买大件的消费定力）。'
    u'收束的穿城信使是全城送急件的年轻姑娘，她的信条「急件不急，稳到才算到」——'
    u'她的看法：送急件和买新车学的是同一课，兴奋会退潮，稳稳当当到了才算真的到了。'
    u'这是「城市速报」系列第十三张，此前十二张覆盖过加油站 20 米之问/喝水解渴/国庆网红猫留守/'
    u'8.59 元香菜仅退款/哈基米肉鸽游戏等热点反应。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime("%Y-%m-%d %H:%M:%S"), 'model': 'qwen2.5:14b',
          'material': 'MC-20261010-REACT-v13 static card (cards.json + render output)'}
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
