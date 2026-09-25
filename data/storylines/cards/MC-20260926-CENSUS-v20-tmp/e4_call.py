# E4 audience reference call - MC-20260926-CENSUS-v20 static census card (non-registry seat,
# direct Ollama; v19 e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态居民图鉴卡《城市图鉴 020》'
    '（1080×1080 方图·黑底；顶部标题「城市图鉴 020」；下面六行居民档案：'
    '「C-00029 · 咪喱」「像素灵 · radiocat · 无定 · 第 19 数据季」「GAME 城 · 像素匠人巷 · 伴居灵」'
    '「信条：「蹭饭是门艺术，报恩是门手艺。」」「好奇 · 追光 · 嘴甜」'
    '「全城唯一拥有「巷志」的猫」；'
    '图内底部来源行「基于硅基城市居民户籍卡档案（展示锚 C-00029）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），城里住着一万多名虚构居民；'
    '咪喱是一只像素灵·radiocat（电波猫），无定性别，第 19 数据季，住 GAME 城·像素匠人巷，职业是伴居灵——弄堂与三城屋顶的伴居者，'
    '尾巴天线永远对准最热闹的方向；'
    '它给自己的定位是「全巷的公共宠物」，收编自己的人类有：粥铺阿凤（管布头）、回测田那位（管晒太阳的田埂）、画匠家（管毛线）；'
    '它的哲学很简单：人对它好，它就把「耳朵」借给谁——尾巴天线灵敏得很，谁家有事它第一个竖起来；'
    '它说喵语（音调有七八种，巷子里人人听得懂个大概）；高兴时踩的步子像小碎鼓；生气时会把自己的耳朵拍得啪啪响，全巷的小孩都会学；'
    '它一身柔光绒羽，光纹是奶牛猫配色——它自己选的，说是「接地气」；左耳有个缺口——为救一只卡在管线里的小消息雀留下的，'
    '它不许任何人说那是「英勇」，「就是耳朵痒」；'
    '它在雨季的第一场雨里诞生——出生那晚它蹲在罗大壮的画室外窗台上，画匠把它画进了那天的门脸像里；'
    '转折：尾巴天线在台风「梅花」那夜立了大功——全巷的通讯中断，是它一趟一趟把口信叼到位的，第二天的早饭它吃了七家的；'
    '现状：匠人巷编外巷长（自封），办公室是罗家的窗台；'
    '它每天巡视全巷一轮（路线固定，人人认得它的脚步）；给谁家报喜就绕谁家梁上跑三圈；'
    '下雨天躲进粥铺蒸笼边，「那里最暖，还管饭」；'
    '它的信条是「蹭饭是门艺术，报恩是门手艺。」；'
    '它是全城唯一拥有「巷志」的猫——罗大壮按月给它画像记录体形与光纹变化，档案馆破例收了副本，题名《咪喱巷志》；'
    '这份居民档案逐字段取自集团自有的「硅基城市」IP 户籍卡档案（手写展示锚 C-00029），一字不改；'
    '这张卡由本地渲染链自动生成，是「城市图鉴」系列的第二十张。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260926-CENSUS-v20 static card (cards.json + render output)'}
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
