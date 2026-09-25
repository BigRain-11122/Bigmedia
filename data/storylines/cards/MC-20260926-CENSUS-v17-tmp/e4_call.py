# E4 audience reference call - MC-20260926-CENSUS-v17 static census card (non-registry seat,
# direct Ollama; v16 e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态居民图鉴卡《城市图鉴 017》'
    '（1080×1080 方图·黑底；顶部标题「城市图鉴 017」；下面六行居民档案：'
    '「C-00026 · 高小满」「碳基市民 · 新市民派 · 女 · 22 岁」「江面与光桥 · 光桥市集 · 穿城信使」'
    '「信条：「急件不急，稳到才算到。」」「勤快 · 直性子 · 随缘」'
    '「全城唯一给每单写「一句话交货注脚」的信使」；'
    '图内底部来源行「基于硅基城市居民户籍卡档案（展示锚 C-00026）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），城里住着一万多名虚构居民；'
    '高小满是江面与光桥·光桥市集的穿城信使，碳基市民·新市民派，女·22 岁；'
    '她从江淮小城进城，头一个月在光桥市集摆摊卖家乡酱菜，把全城的路跑成了自己的手纹；'
    '后来驿站招信使，老板娘说「这闺女认路像认亲」；'
    '她说跑信使不图快钱——每一单背后都是一个「等着的人」，把东西稳稳交到手上，那声「多谢」比酱菜好卖；'
    '她的信条是「急件不急，稳到才算到。」；'
    '头一单加急件是给一位老人送药，跑丢了两次路，送到时天全黑，老人拉她吃了碗面——从此她给自己立规矩：单可以少接，接了必须稳到；'
    '她是全城口哨打得最响的姑娘，桥上的守夜灯灵都认得她那两声；'
    '她双肩包底永远有一把伞——不是给自己的，「桥上常有人淋着」；'
    '雨天单子最多，她说雨声是加班费；每送完一单在心里替收件人说一句「收到了」；'
    '休息日去江边教一个叫王多多的小孩认近道（「等他长到我这么高就转正」）；'
    '她是全城唯一给每单写「一句话交货注脚」的信使——像「今夜风大，交到本人手里」这样的字条，档案馆的年轻人专门收藏了一沓；'
    '这份居民档案逐字段取自集团自有的「硅基城市」IP 户籍卡档案（手写展示锚 C-00026），一字不改；'
    '这张卡由本地渲染链自动生成，是「城市图鉴」系列的第十七张。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260926-CENSUS-v17 static card (cards.json + render output)'}
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
