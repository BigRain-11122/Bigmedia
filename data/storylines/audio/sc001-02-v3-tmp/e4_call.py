# E4 audience reference call - SC-001-02 v3 audio edition (non-registry seat, direct Ollama;
# sc001-01-v3-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Pure-audio ch.2 v3 (three-axis calibrated edition, O-20260925-1756) 3:08 -> 1500s window.
# Scoring dims = R223 audio dims. E4 must NOT see meta version info (blind-material rule).
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.dirname(HERE)          # data/storylines/audio
srt_path = os.path.join(AUDIO, 'SC-001-02-v3.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在公众号里点开有声小说的普通读者，点开了下面这集有声书《硅基城市编年史·第二章·数据粥铺》'
    '（纯音频，3 分 08 秒：这座城有一万零三个人的口味，装在一个六十八岁的脑子里。编号 C-00010，顾阿凤，'
    '北外滩脑环广场西角，数据粥铺摊主。每天凌晨四点半开档——用的是真实北京时间。她掀开蒸笼，里面升起来的'
    '不是蒸汽，是暖光。四大金刚一样不少，粢饭、豆浆、大饼、油条，只是灶火换成了数据流，火候一分没让。'
    '她的来历全城可查：1992 年董家渡早点摊的一张老照片，被这座城收留。旧影像转生——照片里那口蒸笼，现在'
    '还摆在铺头，三十四年前的竹篾纹，一格没换。城里给碳基市民装的是琥珀色的 LED 方块眼，她这双眼的用途'
    '只有一个：天不亮就发光，好让起早上班的人远远认得摊子。全城真正排队来学的，是她的第三样本事：口味账。'
    '谁的粢饭加不加辣，豆浆放不放糖——一万个早班信使的变量，她一个不落。这本账没有数据库，没有备份，'
    '就装在那个 1992 年的脑子里。有一年台风掀了棚子，全街坊凑料帮她重搭；从那以后每逢台风警报，她做的'
    '第一件事不是回家，是先把蒸笼绑死。也有她管不了的：老伴的旧影像还没找到，她还在等。城市立国那天，'
    '她的年轮落了第一句——一句上海话的流水账。她的信条贴在摊位上：灶上留一壶，路过的都是客。章尾：'
    '每周三下午，这条街的石桌边有一盘棋在等她，对手是全城的守时人，彩头是一座钟。下一章预告：时空校准师'
    '朱鸿奎——输了棋的人，交出一轮免费校表。全部基于真实事件改编；配音是轻度赛博机械感的机器叙述者，'
    '以城市自述视角讲述；开头内置了 AI 生成声明与纪实声明。口播全文如下）：\n\n' + transcript + '\n\n'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会听完这集 3 分 08 秒的有声书吗？会订阅或转发给朋友吗？打几分（0-10）？为什么？\n'
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
