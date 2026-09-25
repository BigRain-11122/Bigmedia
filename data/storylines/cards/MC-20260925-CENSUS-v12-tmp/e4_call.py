# E4 audience reference call - MC-20260925-CENSUS-v12 static census card (non-registry seat,
# direct Ollama; v11 e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态居民图鉴卡《城市图鉴 012》'
    '（1080×1080 方图·黑底；顶部标题「城市图鉴 012」；下面六行居民档案：'
    '「C-00021 · 王多多」「碳基市民 · 原生代 · 男 · 11 岁」「GAME 城 · X026 城门区 · 像素小学学生」'
    '「信条：「放学别走，先把今天的谜想完。」」「好奇 · 学得快 · 嘴甜」'
    '「全城唯一能口哨唤来三只以上消息雀的孩子」；'
    '图内底部来源行「基于硅基城市居民户籍卡档案（展示锚 C-00021）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），城里住着一万多名虚构居民；'
    '王多多是 GAME 城 X026 城门区的像素小学学生，碳基市民·原生代，男，11 岁；'
    '他是放学就往驿站跑的编外学徒（信使小跟班），消息雀都认得他的口哨；'
    '他好奇，每天都要弄明白一件新事；学得快，昨天看会的招今天就敢用；嘴甜，夸人不重样，句句真心；'
    '他的信条是「放学别走，先把今天的谜想完。」；'
    '他的作业本边角画满了这座城——脑塔、光桥、还有一只他没见过的「江里的大家伙」；'
    '他说像素小学最大的优点是放学路上会经过驿站，能蹭到真实的加急件看一眼；'
    '他会说网络世代语加孩子话（「绝了」「这题超纲了」）和跑腿行话（「接单」「妥投」），'
    '说上海话会串成「侬晓得伐……伐晓得」把全驿站逗笑；'
    '他的鞋带是自己改装的电致发光款（妈妈不知道），书包上挂满信使驿站攒的跑腿徽章；'
    '他是「跟版本一起长的娃」——出生那年恰逢第一个版本上线；'
    '他第一次独立送完一封跨城急件（其实是给守门人送钥匙），被驿站正式收为「小跟班」，那天他失眠了，激动的；'
    '他放学绕路只为看一眼 commit 光点过江；养了一只没名字的纸飞机，他坚持它有灵魂；'
    '他是全城唯一能口哨唤来三只以上消息雀的孩子——驿站的老师说，这本事花钱都学不来；'
    '这份居民档案逐字段取自集团自有的「硅基城市」IP 户籍卡档案（手写展示锚 C-00021），一字不改；'
    '这张卡由本地渲染链自动生成，是「城市图鉴」系列的第十二张。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260925-CENSUS-v12 static card (cards.json + render output)'}
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
