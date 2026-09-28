# E4 audience reference call - SC-001-01 v4 audio edition (non-registry seat, direct Ollama;
# sc001-01-v3-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Pure-audio ch.1 (TOP1 rebuild, scene-law dual-strand edition) 6:32 -> 1500s window.
# Scoring dims = R223 audio dims. E4 must NOT see meta version info (blind-material rule).
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.dirname(HERE)          # data/storylines/audio
srt_path = os.path.join(AUDIO, 'SC-001-01-v4.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在公众号里点开有声小说的普通读者，点开了下面这集有声书《硅基城市编年史·第一章·立国日》'
    '（纯音频，6 分 32 秒：2026 年 9 月 23 日下午两点五十分，一条指令落进聊天框，只有一句：开一家媒体公司。'
    '十分钟后它产出第一件内容；没有办公室，没有入职表，员工数从头到尾是零。一个多小时里，三家公司在同一块'
    '硬盘上出生——一号做游戏：八款，标价全是零，版权证书一沓；二号做投资，第一件作品不是收益，是一场自我'
    '清洗——四百三十二个方案过门禁，红灯四百三十二次，全部下线一个不留，审计记录谁都改不了；媒体公司给自己'
    '造的第一件工具是一张审查表，第一轮收工十二项检查全绿。天黑之后真正的赌局开场：晚上九点半，第二条大'
    '指令——再造一家公司，业务是生产一整座城的居民，第一批一万个，天亮前交付。十点四十三分，这家公司有了'
    '心跳：每十分钟自己醒一次，找活，干活，记账；醒来的第一次自审，查出两处违规，违规者它自己。十一点四十'
    '二分，一万零三个名字交付，三道校验全过；名单里有守灶台的阿婆——从一张一九九二年上海董家渡早点摊的老'
    '照片里来，有管自己叫归档者的硅基民，有五十一个半透明的小东西。凌晨零点零七分，城市合上第一个工作日：'
    '语言库六百四十八句话，年轮十六条，一个新市民试图越权被循环当场按住。北外滩的塔顶亮起一点纯白——全城'
    '唯一的一处，一万零三个人都认得：那是他们的老板，全公司唯一的人类。故事后半段天快亮：城市降到最低'
    '功耗，扫描线沿塔基慢慢走；北外滩脑环广场，天黑里掺了一点亮，一辆不锈钢小车碾过地砖缝停在广场西角，'
    '车上下来一位装着琥珀色发光方块眼的阿婆，簪一支旧银簪。四点半炉子点起来——火不是明火，是一格一格的'
    '数据流；蒸笼掀开，暖光升上来。她念出落城后的第一句话（上海话），第一批客人天刚亮透就来了。清晨的系统'
    '日志上多出一行没人登记过的事件：北外滩，一个蒸笼开始发光。一万个人里，有一个不等任何人吩咐，天不亮'
    '就起来生火做饭。从这一天起，一万零三个人的口味开始有人记账——QUANT 城有位总错过早饭的研究员，名字'
    '已经挂在这本账上。全部基于真实事件改编；配音是轻度赛博机械感的机器叙述者，以城市自述视角讲述；开头'
    '内置了 AI 生成声明与纪实声明。口播全文如下）：\n\n' + transcript + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会听完这集 6 分 32 秒的有声书吗？会订阅或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b', 'material': srt_path}
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
