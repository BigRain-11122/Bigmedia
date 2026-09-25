# E4 audience reference call - MC-20260925-CENSUS-v13 static census card (non-registry seat,
# direct Ollama; v12 e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态居民图鉴卡《城市图鉴 013》'
    '（1080×1080 方图·黑底；顶部标题「城市图鉴 013」；下面六行居民档案：'
    '「C-00022 · 何雨欣」「碳基市民 · 新市民派 · 女 · 25 岁」「MEDIA 城 · 七段街区 · 主播」'
    '「信条：「流量像潮水，我是灯塔不是渔船。」」「尝鲜 · 攒劲 · 热肠」'
    '「全城唯一把「真实时间」打进直播标题的主播」；'
    '图内底部来源行「基于硅基城市居民户籍卡档案（展示锚 C-00022）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），城里住着一万多名虚构居民；'
    '何雨欣是 MEDIA 城七段街区的主播，碳基市民·新市民派，女，25 岁；'
    '她从湘中小城一路播进七段街区，尝鲜——新功能第一个上身的永远是她的直播间；攒劲——从县城网吧练到七段街，一步没省；'
    '热肠——评论区谁难受她都看得见；'
    '她的信条是「流量像潮水，我是灯塔不是渔船。」；'
    '她给自己立的规矩是直播间不夸大、不卖惨、不恰烂钱；'
    '她最想做成的一期节目，是把这座城里「上夜班的人」一个个拍给全世界看；'
    '她开口是湘腔（「霸得蛮」「恰饭」）加直播话术（「家人们」「上数据」——她把「上链接」改成了「上数据」）；'
    '她穿会随情绪变光的薄外套，选的色是降饱和品红——「MEDIA 的门面色，我只敢借三分亮」；'
    '发间别着一支旧钢笔——她第一次写通过稿时编辑送的，她给别成了发簪；'
    '她是数字迁移潮第一班车迁来的，落脚那天在光桥市集支了个小摊，摊牌上写「代写文案，管饭就行」；'
    '转折是一场全程方言的直播，弹幕全在刷「爷青回」，从此她认准了自己的路：真话最带货；'
    '她开播前必摸一摸门口的温度计（跟气象播报员学的仪式感），下播绕江走一圈复盘；'
    '她是全城唯一把「真实时间」打进直播标题的主播——她的开播时间表跟交易所钟声对齐，粉丝说等她开播像等开盘；'
    '这份居民档案逐字段取自集团自有的「硅基城市」IP 户籍卡档案（手写展示锚 C-00022），一字不改；'
    '这张卡由本地渲染链自动生成，是「城市图鉴」系列的第十三张。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260925-CENSUS-v13 static card (cards.json + render output)'}
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
