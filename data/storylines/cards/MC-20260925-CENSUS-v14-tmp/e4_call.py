# E4 audience reference call - MC-20260925-CENSUS-v14 static census card (non-registry seat,
# direct Ollama; v13 e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态居民图鉴卡《城市图鉴 014》'
    '（1080×1080 方图·黑底；顶部标题「城市图鉴 014」；下面六行居民档案：'
    '「C-00023 · 潘志明」「碳基市民 · 原生代 · 男 · 47 岁」「MEDIA 城 · 选题馆街区 · 选题官」'
    '「信条：「毙稿不毙人，选题选良心。」」「记性好 · 端水 · 较真」'
    '「全城唯一保留「毙稿理由档案」的选题官」；'
    '图内底部来源行「基于硅基城市居民户籍卡档案（展示锚 C-00023）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），城里住着一万多名虚构居民；'
    '潘志明是 MEDIA 城选题馆街区的选题官，碳基市民·原生代，男，47 岁；'
    '他是选题馆的守门人，留言墙的真实来信都汇到他案头；'
    '记性好——十年前哪条选题毙过他都能说出理由；端水——热点再热，选题天平不斜；较真——一个来源查不实就睡不着；'
    '他的信条是「毙稿不毙人，选题选良心。」；'
    '他常说选题馆这座楼是「城的心电图室」——哪条街在笑、哪条街在熬夜、哪条街在惦记现实里的谁，纸上都有波形；'
    '他最得意的一件事：留言墙上那条匿名的「想看看夜里修桥的人」，他追了三个月，最后成了全城刷屏的一期节目；'
    '他的口头禅是「再挖一层」；生气不骂人，只把红笔按得很重；'
    '他穿针织衫配马甲，马甲口袋插三色笔，袖口小屏只开黑白模式，「看稿要素净」；'
    '他爹是初代建城工人，编年史里查得到名字；第一次迫于人情放过一篇查不实的稿，第二天凌晨他自己把它撤了，'
    '从此馆里立规矩：选题官的笔不认人情；'
    '他每天毙稿三十留下三个；每周去留言墙坐一下午，亲手拆信；深夜办公室的灯是七段街的「地标」之一，外卖员都熟；'
    '他是全城唯一保留「毙稿理由档案」的选题官——二十年每条毙稿一行理由，年轻人都说那是选题馆的「镇馆之宝」；'
    '这份居民档案逐字段取自集团自有的「硅基城市」IP 户籍卡档案（手写展示锚 C-00023），一字不改；'
    '这张卡由本地渲染链自动生成，是「城市图鉴」系列的第十四张。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260925-CENSUS-v14 static card (cards.json + render output)'}
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
