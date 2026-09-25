# E4 audience reference call - MC-20260926-CENSUS-v16 static census card (non-registry seat,
# direct Ollama; v15 e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态居民图鉴卡《城市图鉴 016》'
    '（1080×1080 方图·黑底；顶部标题「城市图鉴 016」；下面六行居民档案：'
    '「C-00025 · 陆海峰」「碳基市民 · 弄堂派 · 男 · 52 岁」「江面与光桥 · 渡轮航道 · 渡轮船长」'
    '「信条：「船稳，人心才稳。」」「稳 · 直性子 · 记性好」'
    '「全城唯一保留「慢班渡轮」的船长」；'
    '图内底部来源行「基于硅基城市居民户籍卡档案（展示锚 C-00025）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），城里住着一万多名虚构居民；'
    '陆海峰是江面与光桥·渡轮航道上的渡轮船长，碳基市民·弄堂派，男·52 岁；'
    '他爹是现实里黄浦江上的轮渡船长，他打小在码头长大，江的脾气全在骨头里；'
    '进了这座城他没挑别的行当——他说「有江的地方就得有摆渡的」；'
    '数据道再快，他这条渡轮永远留着慢班，「给想看江的人留的」；'
    '他的信条是「船稳，人心才稳。」；'
    '他稳——再大的浪他先把手里的舵稳住；直性子——话不多，句句过秤；记性好——潮汐表背得比家谱熟；'
    '他开航前绕船三圈（一步不少），每天记录真实上海风力并核对航速，退潮时多跑一班「慢船」，说是替江面清波工省一脚力；'
    '报站腔调是全城独一份的稳，乘客说听他报站像「船靠了岸」；'
    '一次大雾夜全船人合唱等雾散，那首歌成了船上的保留节目，他嘴上嫌吵，每回都减速唱完才靠泊；'
    '他腰间挂着一只旧铜哨——他爹传的，现在用来在雾天跟守夜灯灵十四号路灯对暗号；'
    '他正教一个想学开船的年轻人——「手艺不传就沉江了」；'
    '他是全城唯一保留「慢班渡轮」的船长——不为生意，只为给想慢慢看江的人留一趟船，船票恒价：一句「多谢」；'
    '这份居民档案逐字段取自集团自有的「硅基城市」IP 户籍卡档案（手写展示锚 C-00025），一字不改；'
    '这张卡由本地渲染链自动生成，是「城市图鉴」系列的第十六张。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260926-CENSUS-v16 static card (cards.json + render output)'}
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
