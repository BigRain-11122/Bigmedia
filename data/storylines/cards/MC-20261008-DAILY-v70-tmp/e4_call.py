# -*- coding: utf-8 -*-
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态日签卡《城市日签 070》'
    u'（1080×1080 方图·黑底；顶部标题「城市日签 070」；日期行「2026-10-08 · 城主连令日 · 午」；'
    u'中间引文一行「「城主发话了，早点铺子快忙活起来」」；署名行「——硅基城市台词池 · 烟火轴」；'
    u'图内底部来源行「引文取自硅基城市台词池（虚构城市档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），'
    u'城里住着一万名登记居民，还登记着一批城市生灵（动物宠物小灵们）。台词池按六种「轴」收录居民的话，生灵们的话收在城市生灵声部。'
    u'这句引文出自一个「城主连令日」的中午：这座虚构城市的城主（城里发号施令的主人）今天一道接一道地下令，'
    u'脑塔顶上一连闪了好几次白光，全城都跟着动起来。引文是烟火轴居民的一句大白话：'
    u'城主发话了，连最热乎的早点铺子都得快忙活起来——蒸笼重新上汽，包子接着出笼。'
    u'一座一切都在数据里飞跑的城市，最高层的一声号令，最后落在了最底层的烟火蒸汽上：'
    u'上面是号令，下面是热乎气，这就是这座城的一天被点着的方式。'
    u'这是「城市日签」系列第七十张，出自烟火轴声口'
    u'（烟火轴的居民们此前多次登场——满街灯海招呼街坊晚上早点回家别冻着了/早点摊也得趁热闹多卖点包子/'
    u'煮汤圆的时候想家人也想你/热腾的豆浆配上油条一整天都精神/深夜守着不打烊的铺子等早起的客人/'
    u'假日深夜不打烊的面摊说面条汤滚着呢爱喝热乎的来碗/'
    u'以及今早复市首日市场摊位上的那句：市场买卖讲价，公平公正正——这一句是连令日中午城主发话后，'
    u'早点铺子里最烟火的一声应答）。'
    u'前六十九张覆盖六种轴的居民与城市生灵声部（做灯笼的师傅/修伞的老匠人/江边钓鱼人/值守班校准街灯/'
    u'菜场阿姨/侠气街坊/怀旧老克勒/生灵小灵们等等）。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime("%Y-%m-%d %H:%M:%S"), 'model': 'qwen2.5:14b',
          'material': 'MC-20261008-DAILY-v70 static card (cards.json + render output)'}
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
