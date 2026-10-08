# -*- coding: utf-8 -*-
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态热点反应卡《城市速报 012》'
    u'（1080×1080 方图·黑底；顶部标题「城市速报 012」；来源行「今日热点 · 知乎热榜 2026-10-09」；'
    u'热点标题两行「车子熄火距加油站仅 20 米，加油员拒绝打散装汽油，/车主花 350 元拖车到加油站，到底是谁的问题？」；'
    u'下面三行城市居民反应：「秩序轴：「守门人说，规矩不能松」」「侠气轴：「有难处，找我准没错」」'
    u'「逍遥轴：「城主发令，咱悠着点」」；收束行「时空校准师信条：「差之毫秒，谬以全城。」」；'
    u'图内底部声明行「热点转述自知乎热榜·反应与信条皆取自虚构城市档案」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），'
    u'城里住着一万名登记居民。台词池按六种「轴」收录居民的话，户籍卡记录每位居民的姓名职业和信条。'
    u'这张卡的玩法是「热点城市反应」：把当天知乎热榜上大家都在讨论的现实热点，'
    u'原样转述给虚构城市的居民，让他们用自己的话反应——所以热点是真实的、反应是虚构的，底部声明行就是这个意思。'
    u'今天的热点是：一辆车在离加油站只有 20 米的地方熄火了，加油员按安全规定拒绝打散装汽油，'
    u'车主最后花 350 块钱叫拖车把车拖进加油站，网上正在吵「到底是谁的问题」。'
    u'城市居民的三个反应：秩序轴的守门人说规矩不能松（散装汽油是消防红线，守规矩的人不是刁难是守责）；'
    u'侠气轴居民说有难处找我准没错（对车主 20 米困境的热心回应——帮忙可以，红线不碰）；'
    u'逍遥轴居民说城主发令咱悠着点（350 块买个慢与稳，认了规则悠着点过日子）。'
    u'收束的时空校准师是城里管全城对时的老人，他的信条「差之毫秒，谬以全城」——'
    u'热点的荒诞感全在「仅 20 米」三个字：校准师的看法是红线上的距离不分大小，差之毫秒谬以全城，'
    u'加油员守的不是那 20 米，是全城的安全口子。'
    u'这是「城市速报」系列第十二张，此前十一张覆盖过宜居城市之问/破烂变黄金赛道/喝水解渴/'
    u'国庆网红猫留守/8.59 元香菜仅退款/哈基米肉鸽游戏等热点反应。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime("%Y-%m-%d %H:%M:%S"), 'model': 'qwen2.5:14b',
          'material': 'MC-20261009-REACT-v12 static card (cards.json + render output)'}
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
