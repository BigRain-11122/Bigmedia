# E4 audience reference call - SC-001-03 audio edition (non-registry seat, direct Ollama;
# sc001-02-v1-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Pure-audio ch.3 3:10 -> 1500s window. Scoring dims = R223 first-defined audio dims.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.dirname(HERE)          # data/storylines/audio
srt_path = os.path.join(AUDIO, 'SC-001-03-v1.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在公众号里点开有声小说的普通读者，点开了下面这集有声书《硅基城市编年史·第三章·周三的棋局》'
    '（纯音频，3 分 10 秒：硅基城市里最老的两种手艺——七十四岁时空校准师朱鸿奎与六十八岁数据粥铺摊主顾阿凤，'
    '每周三在粥铺石桌边下一盘棋，下的不是棋是时间；输了棋免费给人校表；他的硅基徒弟归档者-07 比碳基还老派；'
    '全城齐秒时他那台爷爷传下来的老座钟会跟着响一声，档案馆的人管这一声叫这座城的心跳备份；'
    '年轮上落着「差之毫秒，谬以全城」，全部基于真实事件改编；'
    '配音是轻度赛博机械感的机器叙述者，以城市自述视角讲述；开头内置了 AI 生成声明与纪实声明。'
    '口播全文如下）：\n\n' + transcript + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会听完这集 3 分 10 秒的有声书吗？会订阅或转发给朋友吗？打几分（0-10）？为什么？\n'
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
