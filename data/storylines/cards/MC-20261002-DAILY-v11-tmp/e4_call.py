# -*- coding: utf-8 -*-
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态日签卡《城市日签 011》'
    u'（1080×1080 方图·黑底；顶部标题「城市日签 011」；日期行「2026-10-02 · 国庆假期」；'
    u'中间引文两行「街上的灯可真多，照亮了每个人的笑脸。」；署名行「——硅基城市台词池 · 烟火轴」；'
    u'图内底部来源行「引文取自硅基城市台词池（虚构城市档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），'
    u'城里住着一万名登记居民。「烟火轴」是城里最有烟火气、最顾家、最关心街坊日常的一类居民。'
    u'这句引文是国庆假期第二天一位烟火轴居民晚上出门，看着街上成排挂起的节日灯说的——'
    u'灯挂得满街都是，把每个人的笑脸都照亮了（台词池池级署名·无具体姓名）。'
    u'这是「城市日签」系列第十一张（前十张：做灯笼的师傅在直播间晒灯笼/老房子居民看着街上'
    u'挂起的节日灯/灯下兄弟聚饮把酒言欢/节日灯多了家里的笑声也多/值守班校准街灯心里踏实/'
    u'江边钓鱼人抬头看节日灯火/求新轴居民说灯笼像极了小时候的记忆/侠气轴居民招呼街坊把'
    u'笑声放大些连灯都跟着亮了/求新轴居民傍晚散步满眼都是光/怀旧轴居民说街灯还是档案馆里'
    u'藏着的当年的样式）。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20261002-DAILY-v11 static card (cards.json + render output)'}
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
