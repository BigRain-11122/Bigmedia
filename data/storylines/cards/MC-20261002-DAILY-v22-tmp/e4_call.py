# -*- coding: utf-8 -*-
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态日签卡《城市日签 022》'
    u'（1080×1080 方图·黑底；顶部标题「城市日签 022」；日期行「2026-10-02 · 国庆假期」；'
    u'中间引文一行「修伞铺也要来凑个热闹」；署名行「——硅基城市台词池 · 怀旧轴」；'
    u'图内底部来源行「引文取自硅基城市台词池（虚构城市档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），'
    u'城里住着一万名登记居民。「怀旧轴」是城里最爱念旧、守着老手艺老物件的一类居民。'
    u'这句引文是国庆假期第二天，街面上张灯结彩人人出门过节，连平时最安静、手艺都快失传的'
    u'修伞铺也挂起灯来凑节日的热闹——修伞铺也要来凑个热闹。旧手艺铺子不冷场，'
    u'节日不冷落任何一行。这是「城市日签」系列第二十二张（前二十一张：做灯笼的师傅在直播间'
    u'晒灯笼/老房子居民看着街上挂起的节日灯亮堂了/灯下兄弟聚饮把酒言欢/节日灯多了家里的'
    u'笑声也多/值守班校准街灯心里踏实/江边钓鱼人抬头看节日灯火映高楼/求新轴居民说灯笼像极了'
    u'小时候的记忆/侠气轴居民招呼街坊把笑声放大些连灯都跟着亮了/求新轴居民傍晚散步满眼都是光/'
    u'怀旧轴居民说街灯还是档案馆里藏着的当年的样式/烟火轴居民说街上的灯可真多照亮了每个人'
    u'的笑脸/逍遥轴居民说灯挂得真高看得见星星了/侠气街角阿姨笑眯眯说邻里间纠纷没了/求新轴'
    u'会扎灯笼的长辈得趁节气做几副新灯笼给小孙子看/求新轴居民说看看这彩灯比屏幕上的还好看/'
    u'怀旧轴居民感叹往年的灯节哪有今年这般热闹/秩序轴居民说节日里大家开心就好/逍遥轴居民'
    u'泡上热茶看茶香伴着灯影摇感叹好个安逸节/烟火轴居民在菜场看着白菜堆说菜场的白菜也喜庆'
    u'起来了/侠气轴居民说船上信使忙不停信儿传递满城红/秩序轴居民说挂上灯笼喜洋洋咱这日子'
    u'过得稳当）。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20261002-DAILY-v22 static card (cards.json + render output)'}
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
